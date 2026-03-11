"""Tests for mock EHR API endpoints (patient, vitals, lab fetch)."""

import pytest
from fastapi.testclient import TestClient

from app.api.mock_ehr import router as mock_ehr_router
from fastapi import FastAPI

# Minimal app with only mock EHR router - no DB/auth deps
app = FastAPI()
app.include_router(mock_ehr_router)
client = TestClient(app)


def test_fetch_patient():
    """GET /patients/{patient_id} returns sample patient data."""
    r = client.get("/patients/patient-123")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "patient-123"
    assert data["external_id"] == "ext-patient-123"
    assert "created_at" in data
    assert "updated_at" in data


def test_fetch_vitals():
    """GET /patients/{patient_id}/vitals returns sample vitals readings."""
    r = client.get("/patients/patient-456/vitals")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    v = data[0]
    assert v["systolic_bp"] == 120
    assert v["diastolic_bp"] == 80
    assert v["temp_c"] == 36.6
    assert v["pulse"] == 72
    assert v["spo2"] == 98.0
    assert "timestamp" in v

    # Extended vitals fields from UI should be present (even if null in mock)
    assert "height_cm" in v
    assert "weight_kg" in v
    assert "head_circumference_cm" in v
    assert "respiratory_rate" in v
    assert "blood_sugar_before_meal_mgdl" in v
    assert "blood_sugar_after_meal_mgdl" in v


def test_fetch_labs(monkeypatch):
    """GET /patients/{patient_id}/labs returns sample lab results."""
    monkeypatch.setattr(
        "app.api.mock_ehr.run_wise_agent",
        lambda payload, patient_id, db=None: {"risk_level": "Moderate", "confidence": 0.8, "flags": []},
    )
    r = client.get("/patients/patient-789/labs")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    names = [item["name"] for item in data]
    assert "Hemoglobin" in names
    assert "WBC" in names
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "value" in item
        assert "unit" in item
        assert "date" in item


def test_fetch_labs_calls_wise_adapter(monkeypatch):
    """GET /patients/{patient_id}/labs triggers WWISE adapter invocation."""
    called = {"count": 0, "patient_id": None}

    def _fake_run_wise_agent(payload, patient_id, db=None):
        called["count"] += 1
        called["patient_id"] = patient_id
        return {"risk_level": "Moderate", "confidence": 0.8, "flags": []}

    monkeypatch.setattr("app.api.mock_ehr.run_wise_agent", _fake_run_wise_agent)

    r = client.get("/patients/patient-999/labs")
    assert r.status_code == 200
    assert called["count"] == 1
    assert called["patient_id"] == "patient-999"
