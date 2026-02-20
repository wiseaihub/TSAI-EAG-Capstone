from datetime import datetime
import uuid
from app.agents.base_agent import BaseAgent

class CBCAgent(BaseAgent):
    name = "cbc_agent"
    version = "1.0.0"

    def analyze(self, data):
        flags = []
        risk_score = 0

        if data.hemoglobin < 8:
            flags.append("Severe anemia")
            risk_score += 2
        elif data.hemoglobin < 11:
            flags.append("Mild anemia")
            risk_score += 1

        if data.wbc > 11000:
            flags.append("Leukocytosis")
            risk_score += 1

        if data.platelets < 150000:
            flags.append("Thrombocytopenia")
            risk_score += 1

        if risk_score >= 3:
            risk_level = "High"
        elif risk_score >= 1:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        confidence = round(min(0.6 + risk_score * 0.1, 0.95), 2)

        return {
            "session_id": str(uuid.uuid4()),
            "agent_name": self.name,
            "agent_version": self.version,
            "risk_level": risk_level,
            "flags": flags,
            "confidence": confidence,
            "timestamp": datetime.utcnow()
        }
