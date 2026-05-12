"""CBC agent_service enrichment fields for pilot transparency."""

from unittest.mock import MagicMock

from app.schemas.cbc import CBCInput
from app.services.agent_service import run_cbc


def test_run_cbc_includes_disclaimer_rationale_evidence():
    db = MagicMock()
    payload = CBCInput(hemoglobin=7.5, wbc=7000, rbc=4.5, platelets=200000)
    r = run_cbc(payload, db, "patient-demo")

    assert "disclaimer" in r and r["disclaimer"]
    assert "rationale_lines" in r and isinstance(r["rationale_lines"], list)
    assert any("8 g/dL" in line or "Severe" in line for line in r["rationale_lines"])
    assert "evidence_citations" in r and len(r["evidence_citations"]) >= 1
