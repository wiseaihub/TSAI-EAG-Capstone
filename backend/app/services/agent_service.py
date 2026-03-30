from datetime import datetime
from uuid import uuid4

from app.agents.cbc_agent import CBCAgent
from app.db.models import AgentRun, AgentSession, RunArtifact

_cbc_agent = CBCAgent()


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
    }
