"""
Local PHQ-9 / GAD-7 screening with deterministic cutoffs.

Severity bands follow widely used cut points (Kroenke et al., PHQ-9 and GAD-7):
- PHQ-9: 5–9 mild, 10–14 moderate, 15–19 moderately severe, 20–27 severe.
- GAD-7: 5–9 mild, 10–14 moderate, 15–21 severe.

Risk levels for this API aggregate instruments as:
- High: crisis flags, or PHQ-9 ≥ 20, or GAD-7 ≥ 15
- Moderate: otherwise PHQ-9 ≥ 10 or GAD-7 ≥ 10
- Low: remaining cases
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.db.models import AgentSession
from app.schemas.mental_health import MentalHealthInput

# Reference cutoffs (documentation; scoring logic uses the constants below)
PHQ9_MODERATE = 10
PHQ9_SEVERE = 20
GAD7_MODERATE = 10
GAD7_SEVERE = 15

AGENT_NAME = "mental_health_screening"
AGENT_VERSION = "v1"

DEFAULT_DISCLAIMER = (
    "This screening is not a diagnosis. Results are informational; consult a qualified clinician."
)
DEFAULT_CRISIS_MESSAGE = (
    "If you are at immediate risk, contact local emergency services or a crisis helpline. "
    "This application is not a substitute for emergency or mental health care."
)


def _phq9_band(total: int) -> str:
    if total < 5:
        return "minimal"
    if total < 10:
        return "mild"
    if total < 15:
        return "moderate"
    if total < 20:
        return "moderately_severe"
    return "severe"


def _gad7_band(total: int) -> str:
    if total < 5:
        return "minimal"
    if total < 10:
        return "mild"
    if total < 15:
        return "moderate"
    return "severe"


def _band_to_display(band: str) -> str:
    """Human-readable band for UI (e.g. moderately_severe -> Moderately severe)."""
    return band.replace("_", " ").strip().title()


def _mh_display_labels(
    *,
    phq9_total: int | None,
    gad7_total: int | None,
    crisis: bool,
    suicidal_ideation: bool,
    self_harm_intent: bool,
) -> list[str]:
    """Short, screening-oriented labels parallel to machine-readable flags."""
    out: list[str] = []
    if crisis:
        if suicidal_ideation:
            out.append("Crisis: suicidal ideation reported — seek urgent in-person or emergency care.")
        if self_harm_intent:
            out.append("Crisis: self-harm intent reported — seek urgent in-person or emergency care.")
        if not suicidal_ideation and not self_harm_intent:
            out.append("Crisis pathway triggered — follow local escalation protocol.")
        return out

    if phq9_total is not None:
        b = _phq9_band(phq9_total)
        out.append(
            f"PHQ-9 ({phq9_total}): {_band_to_display(b)} depressive symptom severity (screening, not a diagnosis)."
        )
    if gad7_total is not None:
        b = _gad7_band(gad7_total)
        out.append(
            f"GAD-7 ({gad7_total}): {_band_to_display(b)} anxiety symptom severity (screening, not a diagnosis)."
        )
    return out


def _mh_recommendations(
    *,
    phq9_total: int | None,
    gad7_total: int | None,
    crisis: bool,
    suicidal_ideation: bool,
    self_harm_intent: bool,
) -> list[str]:
    recs: list[str] = []
    if crisis:
        if suicidal_ideation or self_harm_intent:
            recs.append("Urgent in-person or emergency mental-health evaluation is recommended.")
        recs.append("Activate crisis escalation protocol and supervised safety planning.")
        return recs

    if phq9_total is not None and phq9_total >= PHQ9_MODERATE:
        recs.append("Schedule clinician follow-up for depressive symptom assessment and support options.")
    if gad7_total is not None and gad7_total >= GAD7_MODERATE:
        recs.append("Schedule follow-up for anxiety symptom assessment and coping plan review.")
    if phq9_total is not None or gad7_total is not None:
        recs.append("Repeat PHQ-9/GAD-7 at follow-up to monitor trend over time.")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in recs:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _compute_phq9_total(payload: MentalHealthInput) -> int | None:
    if payload.phq9_items is not None:
        return sum(int(x) for x in payload.phq9_items)
    return payload.phq9_total


def run_mental_health_screening(
    payload: MentalHealthInput,
    db,
    patient_id: str,
) -> dict[str, Any]:
    """
    Score PHQ-9 / GAD-7 locally, persist AgentSession, return result dict for API + optional S18 handoff.

    Crisis fields (suicidal ideation, self-harm intent) force High risk regardless of scores.
    """
    phq9_total = _compute_phq9_total(payload)
    gad7_total = payload.gad7_total

    flags: list[str] = []
    if payload.suicidal_ideation:
        flags.append("suicidal_ideation_reported")
    if payload.self_harm_intent:
        flags.append("self_harm_intent_reported")

    crisis = payload.suicidal_ideation or payload.self_harm_intent
    if crisis:
        flags.append("crisis_referral")
        risk_level = "High"
        confidence = 0.92
    else:
        high_score = False
        mod_score = False
        if phq9_total is not None:
            flags.append(f"phq9_total:{phq9_total}")
            flags.append(f"phq9_severity:{_phq9_band(phq9_total)}")
            if phq9_total >= PHQ9_SEVERE:
                high_score = True
            elif phq9_total >= PHQ9_MODERATE:
                mod_score = True
        if gad7_total is not None:
            flags.append(f"gad7_total:{gad7_total}")
            flags.append(f"gad7_severity:{_gad7_band(gad7_total)}")
            if gad7_total >= GAD7_SEVERE:
                high_score = True
            elif gad7_total >= GAD7_MODERATE:
                mod_score = True

        if high_score:
            risk_level = "High"
            confidence = 0.88
        elif mod_score:
            risk_level = "Moderate"
            confidence = 0.78
        else:
            risk_level = "Low"
            confidence = 0.72

    session_id = str(uuid4())
    record = AgentSession(
        session_id=session_id,
        patient_id=patient_id,
        agent_name=AGENT_NAME,
        agent_version=AGENT_VERSION,
        risk_level=risk_level,
        confidence=confidence,
        flags=flags,
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.add(record)
    db.commit()

    disclaimer = os.environ.get("MH_DISCLAIMER_TEXT", DEFAULT_DISCLAIMER)
    crisis_message: str | None = None
    if crisis:
        crisis_message = os.environ.get("MH_CRISIS_ESCALATION_MESSAGE", DEFAULT_CRISIS_MESSAGE)

    display_labels = _mh_display_labels(
        phq9_total=phq9_total,
        gad7_total=gad7_total,
        crisis=crisis,
        suicidal_ideation=payload.suicidal_ideation,
        self_harm_intent=payload.self_harm_intent,
    )
    recommendations = _mh_recommendations(
        phq9_total=phq9_total,
        gad7_total=gad7_total,
        crisis=crisis,
        suicidal_ideation=payload.suicidal_ideation,
        self_harm_intent=payload.self_harm_intent,
    )

    return {
        "session_id": session_id,
        "risk_level": risk_level,
        "confidence": confidence,
        "flags": flags,
        "display_labels": display_labels,
        "recommendations": recommendations,
        "phq9_total": phq9_total,
        "gad7_total": gad7_total,
        "phq9_band": _phq9_band(phq9_total) if phq9_total is not None else None,
        "gad7_band": _gad7_band(gad7_total) if gad7_total is not None else None,
        "crisis": crisis,
        "disclaimer": disclaimer,
        "crisis_message": crisis_message,
    }


def screening_summary_for_s18(screening_result: dict[str, Any]) -> dict[str, Any]:
    """Subset of local screening safe to embed in S18 query JSON."""
    keys = (
        "session_id",
        "risk_level",
        "confidence",
        "flags",
        "display_labels",
        "recommendations",
        "phq9_total",
        "gad7_total",
        "phq9_band",
        "gad7_band",
        "crisis",
    )
    return {k: screening_result[k] for k in keys if k in screening_result}
