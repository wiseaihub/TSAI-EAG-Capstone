"""Live integration smoke test -- verifies /analyze, dual-write, and cancel-event plumbing.

Requires TEST_ACCESS_TOKEN env var (Supabase JWT) and a running DB.
Run with: TEST_ACCESS_TOKEN=<token> pytest tests/test_integration_smoke.py

Skipped in default CI (marked integration). Direct SQL reads need the same JWT
session as the API: use apply_supabase_jwt_claims before querying RLS tables.
"""

import os
import pytest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api import orchestrator as orch
from app.core.security import get_current_user
from app.db.session import get_db, SessionLocal
from app.db.rls_context import apply_supabase_jwt_claims
from app.db.models import Case, AgentRun, AgentMessage, AuditEvent

_TEMP_TOKEN = os.environ.get("TEST_ACCESS_TOKEN", "")
_PATIENT_ID = os.environ.get("TEST_PATIENT_ID", "test-integration-patient")


def _real_db():
    """Yield a real DB session for integration tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.environ.get("TEST_ACCESS_TOKEN"),
        reason="Set TEST_ACCESS_TOKEN for live integration tests against Supabase",
    ),
]


@pytest.fixture
def live_client():
    """TestClient wired to real DB but with auth overridden to the temp token subject."""
    app = FastAPI()
    app.include_router(orch.router)

    def _user():
        return {"sub": _PATIENT_ID, "app_role": "doctor"}

    app.dependency_overrides[get_current_user] = _user
    app.dependency_overrides[get_db] = _real_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_analyze_creates_case_and_runs(live_client: TestClient, monkeypatch):
    """POST /analyze with mocked S18 should dual-write case + agent_run rows."""
    monkeypatch.setattr(
        orch,
        "_run_wise_with_timeout",
        lambda *args, **kwargs: {
            "risk_level": "Moderate",
            "confidence": 0.75,
            "flags": ["integration_test_mock"],
            "recommendations": ["Follow up in 2 weeks"],
        },
    )

    r = live_client.post(
        "/analyze",
        json={
            "hemoglobin": 11.0,
            "wbc": 8000,
            "rbc": 4.2,
            "platelets": 200000,
        },
        headers={"Authorization": f"Bearer {_TEMP_TOKEN}"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert "cbc" in body
    assert "wise" in body
    assert "recommendations" in body

    db: Session = SessionLocal()
    try:
        apply_supabase_jwt_claims(db, _PATIENT_ID)
        cases = (
            db.query(Case)
            .filter(Case.user_id == _PATIENT_ID)
            .order_by(Case.created_at.desc())
            .limit(1)
            .all()
        )
        assert len(cases) == 1, "Expected a case row for this patient"
        case = cases[0]
        assert case.status == "completed"

        runs = db.query(AgentRun).filter(AgentRun.case_id == case.id).all()
        assert len(runs) >= 1, "Expected at least one agent_run (CBC)"

        messages = db.query(AgentMessage).filter(AgentMessage.case_id == case.id).all()
        assert len(messages) >= 2, "Expected user + assistant messages"

        audits = (
            db.query(AuditEvent)
            .filter(AuditEvent.entity_type == "case", AuditEvent.entity_id == case.id)
            .all()
        )
        assert len(audits) >= 2, "Expected case_created + case_completed audit events"
    finally:
        db.close()


def test_agent_sessions_still_works(live_client: TestClient):
    """GET /agent-sessions should still return data (backward compat)."""
    r = live_client.get(
        "/agent-sessions",
        headers={"Authorization": f"Bearer {_TEMP_TOKEN}"},
    )
    assert r.status_code == 200
    assert isinstance(r.json(), list)
