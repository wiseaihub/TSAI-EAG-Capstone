from datetime import datetime
from uuid import uuid4
from app.db.models import AgentSession


def run_cbc(payload, db, patient_id):

    # 🔹 Step 1 — Run your analysis logic
    result = {
        "risk_level": "high" if payload.hemoglobin < 8 else "normal",
        "confidence": 0.85,
        "flags": {
            "low_hemoglobin": payload.hemoglobin < 8,
            "high_wbc": payload.wbc > 11000,
        },
    }

    # 🔹 Step 2 — Save to DB
    record = AgentSession(
        session_id=str(uuid4()),
        patient_id=patient_id,
        agent_name="cbc_agent",
        agent_version="v1",
        risk_level=result["risk_level"],
        confidence=result["confidence"],
        flags=result["flags"],
        timestamp=datetime.utcnow(),
    )

    db.add(record)
    db.commit()

    # 🔹 Step 3 — Return result
    return result
