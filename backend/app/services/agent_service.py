from datetime import datetime
from uuid import uuid4

from app.agents.cbc_agent import CBCAgent
from app.db.models import AgentRun, AgentSession, RunArtifact

_cbc_agent = CBCAgent()

_SEX_DISPLAY = {
    "male": "Male",
    "female": "Female",
    "third_gender": "Third gender",
}


def _format_sex_for_display(raw: str) -> str:
    key = raw.strip().lower()
    if key in _SEX_DISPLAY:
        return _SEX_DISPLAY[key]
    return raw.strip().replace("_", " ").title()


def _cbc_display_labels(payload) -> list[str]:
    """Human-readable echo of submitted labs (parity with mental health display_labels)."""
    out: list[str] = []
    sex = getattr(payload, "sex", None)
    if sex is not None and str(sex).strip():
        out.append(f"Sex for interpretation: {_format_sex_for_display(str(sex))}")

    hb = getattr(payload, "hemoglobin", None)
    if hb is not None:
        hb_s = f"{hb:g}" if isinstance(hb, (int, float)) else str(hb)
        out.append(f"Hemoglobin: {hb_s} g/dL")

    wbc = getattr(payload, "wbc", None)
    if wbc is not None:
        wbc_s = f"{wbc:g}" if isinstance(wbc, (int, float)) else str(wbc)
        out.append(f"WBC: {wbc_s} per µL")

    rbc = getattr(payload, "rbc", None)
    if rbc is not None:
        rbc_s = f"{rbc:g}" if isinstance(rbc, (int, float)) else str(rbc)
        out.append(f"RBC: {rbc_s} million/µL")

    plt = getattr(payload, "platelets", None)
    if plt is not None:
        p_s = f"{plt:g}" if isinstance(plt, (int, float)) else str(plt)
        out.append(f"Platelets: {p_s} per µL")

    return out


def _cbc_input_echo(payload) -> dict:
    """Structured copy of submitted CBC fields for API consumers (mirrors MH phq9_total / gad7_total)."""
    sex = getattr(payload, "sex", None)
    return {
        "sex": str(sex).strip() if sex is not None and str(sex).strip() else None,
        "hemoglobin": getattr(payload, "hemoglobin", None),
        "wbc": getattr(payload, "wbc", None),
        "rbc": getattr(payload, "rbc", None),
        "platelets": getattr(payload, "platelets", None),
    }


def _cbc_recommendations(payload, flags: list[str]) -> list[str]:
    recs: list[str] = []
    hb = getattr(payload, "hemoglobin", None)
    wbc = getattr(payload, "wbc", None)

    if hb is not None and hb < 8:
        recs.append("Urgent in-person clinical evaluation for severe anemia context.")
    if hb is not None and hb < 11:
        recs.append("Order iron studies and peripheral blood smear to evaluate anemia cause.")
    if wbc is not None and wbc > 11000:
        recs.append("Evaluate for infection/inflammation (targeted history, exam, and infection testing).")
    if "Severe anemia" in flags or "Mild anemia" in flags:
        recs.append("Consider CMP and detailed clinical history to identify contributing factors.")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in recs:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def run_cbc(payload, db, patient_id, case_id: str | None = None):
    """
    CBC analysis using the same rule set and human-readable flag strings as CBCAgent
    (e.g. Severe anemia, Leukocytosis).
    """
    analysis = _cbc_agent.analyze(payload)
    recommendations = _cbc_recommendations(payload, analysis["flags"])
    display_labels = _cbc_display_labels(payload)
    input_echo = _cbc_input_echo(payload)

    record = AgentSession(
        session_id=analysis["session_id"],
        patient_id=patient_id,
        agent_name=_cbc_agent.name,
        agent_version=_cbc_agent.version,
        risk_level=analysis["risk_level"],
        confidence=analysis["confidence"],
        flags=analysis["flags"],
        timestamp=analysis["timestamp"],
    )

    db.add(record)

    if case_id:
        run_id = str(uuid4())
        run_payload = {
            "risk_level": analysis["risk_level"],
            "confidence": analysis["confidence"],
            "flags": analysis["flags"],
            "recommendations": recommendations,
            "display_labels": display_labels,
            "input_echo": input_echo,
        }
        db.add(
            AgentRun(
                id=run_id,
                case_id=case_id,
                session_id=analysis["session_id"],
                s18_run_id=None,
                agent_name=_cbc_agent.name,
                status="completed",
                started_at=analysis["timestamp"],
                finished_at=analysis["timestamp"],
                error_text=None,
                metrics={"confidence": analysis["confidence"]},
                created_at=analysis["timestamp"],
            )
        )
        db.flush()
        db.add(
            RunArtifact(
                id=str(uuid4()),
                run_id=run_id,
                artifact_type="cbc_result",
                storage_path=None,
                payload=run_payload,
                created_at=datetime.utcnow(),
            )
        )

    db.commit()

    return {
        "session_id": analysis["session_id"],
        "risk_level": analysis["risk_level"],
        "confidence": analysis["confidence"],
        "flags": analysis["flags"],
        "recommendations": recommendations,
        "display_labels": display_labels,
        **input_echo,
    }
