from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import bindparam, func, text
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.models import KbEntry, KbFeedback, KbQueryLog
from app.db.rls_context import apply_supabase_jwt_claims
from app.db.session import get_db
from app.schemas.kb import (
    KbFeedbackRequest,
    KbFeedbackResponse,
    KbQueryRequest,
    KbQueryResponse,
    KbQueryResult,
    KbSaveRequest,
    KbSaveResponse,
)

router = APIRouter(prefix="/kb", tags=["KnowledgeBank"])


def _clamp01(val: float) -> float:
    if val < 0.0:
        return 0.0
    if val > 1.0:
        return 1.0
    return float(val)


def _normalize_role(role: str) -> str:
    r = (role or "").strip().lower()
    if r not in {"patient", "doctor", "system"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    return r


def _normalize_layer(layer: str) -> str:
    l = (layer or "").strip().lower()
    if l not in {"web_research", "product_kb", "doctor_context", "patient_context"}:
        raise HTTPException(status_code=400, detail="Invalid layer")
    return l


def _default_layer_order_for_role(role: str) -> list[str]:
    if role == "doctor":
        return ["doctor_context", "patient_context", "product_kb", "web_research"]
    return ["patient_context", "doctor_context", "product_kb", "web_research"]


def _compute_entry_confidence(db: Session, entry_id: str) -> tuple[float, float]:
    entry = db.query(KbEntry).filter(KbEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="KB entry not found")

    agg = (
        db.query(
            func.count(KbFeedback.id),
            func.avg(KbFeedback.rating),
        )
        .filter(KbFeedback.entry_id == entry_id)
        .first()
    )
    n = int(agg[0] or 0)
    avg_rating = float(agg[1] or 0.0)
    base = float(entry.base_confidence or 0.5)

    if n <= 0:
        feedback_norm = 0.0
        strength = 0.0
    else:
        feedback_norm = (avg_rating - 3.0) / 2.0
        sqrt_n = n ** 0.5
        strength = float(sqrt_n / (sqrt_n + 2.0))

    new_conf = _clamp01(base + (0.4 * feedback_norm * strength))
    entry.feedback_score = float(feedback_norm)
    entry.confidence = float(new_conf)
    entry.updated_at = datetime.utcnow()
    return float(base), float(new_conf)


@router.post("/save", response_model=KbSaveResponse)
def kb_save(
    payload: KbSaveRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = str(user.get("sub") or "").strip()
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    apply_supabase_jwt_claims(db, user_id)

    role = _normalize_role(payload.role)
    if role == "system":
        raise HTTPException(status_code=400, detail="Role must be patient or doctor")
    layer = _normalize_layer(payload.layer)

    is_shared = bool(payload.is_shared)
    if is_shared and layer != "product_kb":
        raise HTTPException(status_code=400, detail="Only product_kb entries can be shared")

    patient_id: str | None = None
    doctor_id: str | None = None
    if layer == "patient_context":
        patient_id = user_id
    if layer == "doctor_context":
        doctor_id = user_id

    entry_id = str(uuid4())
    base_conf = float(payload.base_confidence) if payload.base_confidence is not None else 0.5
    base_conf = _clamp01(base_conf)

    tags: list[str] | None = None
    if payload.tags is not None:
        tags = [" ".join(str(t).split()).strip() for t in payload.tags]
        tags = [t for t in tags if t]
        if not tags:
            tags = None

    row = KbEntry(
        id=entry_id,
        owner_user_id=user_id,
        role=role,
        layer=layer,
        patient_id=patient_id,
        doctor_id=doctor_id,
        title=payload.title,
        content=payload.content,
        source_type=payload.source_type,
        source_url=payload.source_url,
        source_domain=payload.source_domain,
        source_ref=payload.source_ref,
        tags=tags,
        metadata_=payload.metadata,
        is_shared=is_shared,
        base_confidence=base_conf,
        feedback_score=0.0,
        confidence=base_conf,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()

    return KbSaveResponse(id=entry_id, confidence=float(row.confidence or base_conf))


@router.post("/query", response_model=KbQueryResponse)
def kb_query(
    payload: KbQueryRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = str(user.get("sub") or "").strip()
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    apply_supabase_jwt_claims(db, user_id)

    role = _normalize_role(payload.role)
    if role == "system":
        raise HTTPException(status_code=400, detail="Role must be patient or doctor")

    q = " ".join(payload.query_text.split()).strip()
    if not q:
        raise HTTPException(status_code=400, detail="query_text is required")

    layer_order = payload.layer_order or _default_layer_order_for_role(role)
    layers = payload.layers or layer_order
    norm_layers: list[str] = []
    for l in layers:
        nl = _normalize_layer(l)
        if nl not in norm_layers:
            norm_layers.append(nl)

    filters: dict[str, Any] = {}
    if payload.source_domain:
        filters["source_domain"] = payload.source_domain
    if payload.tags_any:
        filters["tags_any"] = payload.tags_any

    dialect = getattr(getattr(db, "bind", None), "dialect", None)
    is_pg = bool(dialect and getattr(dialect, "name", "") == "postgresql")

    def _apply_tags_any_python_filter(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not payload.tags_any:
            return items
        want = {" ".join(str(t).split()).strip().lower() for t in payload.tags_any if str(t).strip()}
        if not want:
            return items
        out: list[dict[str, Any]] = []
        for it in items:
            tags_val = it.get("tags")
            if not isinstance(tags_val, list):
                continue
            have = {" ".join(str(t).split()).strip().lower() for t in tags_val if str(t).strip()}
            if have.intersection(want):
                out.append(it)
        return out

    if is_pg:
        where_extra = ""
        params = {"q": q, "layers": norm_layers, "limit": int(payload.limit)}
        if payload.source_domain:
            where_extra += " AND source_domain = :source_domain"
            params["source_domain"] = payload.source_domain

        stmt = text(
            f"""
            SELECT
            id,
            layer,
            title,
            content,
            source_url,
            source_domain,
            tags,
            metadata,
            confidence,
            ts_rank_cd(
                to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')),
                plainto_tsquery('english', :q)
            ) AS text_rank
            FROM kb_entries
            WHERE
            layer IN :layers
            AND to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')) @@ plainto_tsquery('english', :q)
            {where_extra}
            ORDER BY (
            (confidence * 0.75) +
            (
                ts_rank_cd(
                to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')),
                plainto_tsquery('english', :q)
                ) * 0.25
            )
            ) DESC,
            created_at DESC
            LIMIT :limit
            """
        ).bindparams(bindparam("layers", expanding=True))

    raw_rows = db.execute(stmt, params).mappings().all()
    rows = _apply_tags_any_python_filter([dict(r) for r in raw_rows])
    results: list[KbQueryResult] = []
    for r in rows:
        tags = r.get("tags")
        if isinstance(tags, list):
            norm_tags = [" ".join(str(t).split()).strip() for t in tags]
            tags = [t for t in norm_tags if t] or None
        else:
            tags = None

        results.append(
            KbQueryResult(
                id=str(r.get("id")),
                layer=str(r.get("layer")),
                title=r.get("title"),
                content=str(r.get("content") or ""),
                source_url=r.get("source_url"),
                source_domain=r.get("source_domain"),
                tags=tags,
                metadata=r.get("metadata") if isinstance(r.get("metadata"), dict) else None,
                confidence=float(r.get("confidence") or 0.0),
            )
        )

    response_conf = _clamp01(max((r.confidence for r in results), default=0.0))

    log = KbQueryLog(
        user_id=user_id,
        role=role,
        query_text=q,
        layer_order=layer_order,
        filters=filters or None,
        result_entry_ids=[r.id for r in results],
        response_confidence=response_conf,
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return KbQueryResponse(results=results, response_confidence=response_conf)


@router.post("/feedback", response_model=KbFeedbackResponse)
def kb_feedback(
    payload: KbFeedbackRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = str(user.get("sub") or "").strip()
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    apply_supabase_jwt_claims(db, user_id)

    role = _normalize_role(payload.role)
    if role == "system":
        raise HTTPException(status_code=400, detail="Role must be patient or doctor")

    entry = db.query(KbEntry).filter(KbEntry.id == payload.entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="KB entry not found")

    conf_before = float(entry.confidence or entry.base_confidence or 0.5)
    fb = KbFeedback(
        entry_id=payload.entry_id,
        user_id=user_id,
        role=role,
        rating=int(payload.rating),
        confidence_before=conf_before,
        confidence_after=None,
        comment=payload.comment,
        correction=payload.correction,
        created_at=datetime.utcnow(),
    )
    db.add(fb)
    db.flush()

    _, conf_after = _compute_entry_confidence(db, payload.entry_id)
    fb.confidence_after = conf_after
    db.commit()

    return KbFeedbackResponse(
        entry_id=payload.entry_id,
        confidence_before=conf_before,
        confidence_after=conf_after,
    )
