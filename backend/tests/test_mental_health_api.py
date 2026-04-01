"""HTTP-level tests for POST /mental-health/analyze (auth + DB overridden)."""

from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security import HTTPAuthorizationCredentials

from app.api import orchestrator as orch
from app.core.security import get_current_user
from app.db.session import get_db


@pytest.fixture
def mh_client():
    app = FastAPI()
    app.include_router(orch.router)

    def _user():
        return {"sub": "test-mh-doctor", "app_role": "doctor"}

    def _db():
        yield MagicMock()

    def _bearer():
        return HTTPAuthorizationCredentials(scheme="Bearer", credentials="test-token")

    app.dependency_overrides[get_current_user] = _user
    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[orch.security] = _bearer

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_mental_health_analyze_local_only(mh_client: TestClient):
    """include_s18=false returns screening only, no wise block."""
    r = mh_client.post(
        "/mental-health/analyze",
        json={
            "phq9_total": 12,
            "gad7_total": 5,
            "include_s18": False,
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "screening" in data
    assert data["screening"]["risk_level"] == "Moderate"
    assert "phq9_total" in data["screening"]
    assert "disclaimer" in data["screening"]
    assert "wise" not in data
    assert r.headers.get("X-Poll-Timeout-Seconds")


def test_mental_health_analyze_crisis(mh_client: TestClient):
    r = mh_client.post(
        "/mental-health/analyze",
        json={
            "phq9_total": 4,
            "gad7_total": 4,
            "suicidal_ideation": True,
            "include_s18": False,
        },
    )
    assert r.status_code == 200
    s = r.json()["screening"]
    assert s["risk_level"] == "High"
    assert s["crisis"] is True
    assert s.get("crisis_message")


def test_mental_health_analyze_with_s18_mocked(mh_client: TestClient, monkeypatch):
    """When include_s18=true, wise block is present; S18 call mocked."""
    monkeypatch.setattr(
        orch,
        "_run_mh_wise_with_timeout",
        lambda *args, **kwargs: {
            "risk_level": "Moderate",
            "confidence": 0.75,
            "flags": ["mock_s18"],
        },
    )
    r = mh_client.post(
        "/mental-health/analyze",
        json={
            "phq9_total": 10,
            "gad7_total": 8,
            "include_s18": True,
            "fast": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "screening" in body
    assert "wise" in body
    assert body["wise"]["flags"] == ["mock_s18"]
