"""Mental health local screening and query tagging."""

import json
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from app.agents.wise_adapter import _mental_health_to_query
from app.schemas.mental_health import MentalHealthInput
from app.services.mental_health_service import (
    run_mental_health_screening,
    screening_summary_for_s18,
)


def _db():
    return MagicMock()


def test_phq9_moderate_gad_minimal():
    p = MentalHealthInput(phq9_total=12, gad7_total=4)
    r = run_mental_health_screening(p, _db(), "patient-1")
    assert r["risk_level"] == "Moderate"
    assert r["phq9_band"] == "moderate"
    assert "phq9_total:12" in r["flags"]
    assert isinstance(r.get("display_labels"), list)
    assert any("PHQ-9 (12)" in x for x in r["display_labels"])
    assert isinstance(r.get("recommendations"), list)
    assert len(r["recommendations"]) >= 1


def test_phq9_severe_high_risk():
    p = MentalHealthInput(phq9_total=21, gad7_total=4)
    r = run_mental_health_screening(p, _db(), "patient-1")
    assert r["risk_level"] == "High"
    assert r["phq9_band"] == "severe"


def test_gad7_severe_high_risk():
    p = MentalHealthInput(phq9_total=4, gad7_total=16)
    r = run_mental_health_screening(p, _db(), "patient-1")
    assert r["risk_level"] == "High"
    assert r["gad7_band"] == "severe"


def test_crisis_overrides_scores():
    p = MentalHealthInput(phq9_total=4, gad7_total=4, suicidal_ideation=True)
    r = run_mental_health_screening(p, _db(), "patient-1")
    assert r["risk_level"] == "High"
    assert r["crisis"] is True
    assert "crisis_referral" in r["flags"]
    assert r["crisis_message"] is not None
    assert any("Urgent in-person" in x for x in r.get("recommendations", []))


def test_phq9_items_matches_total():
    items = [0, 0, 0, 0, 0, 0, 0, 0, 2]
    p = MentalHealthInput(phq9_items=items, gad7_total=4)
    r = run_mental_health_screening(p, _db(), "patient-1")
    assert r["phq9_total"] == 2
    assert r["risk_level"] == "Low"


def test_schema_requires_at_least_one_instrument():
    with pytest.raises(ValidationError):
        MentalHealthInput()


def test_schema_rejects_both_phq9_total_and_items():
    with pytest.raises(ValidationError):
        MentalHealthInput(phq9_total=10, phq9_items=[0] * 9, gad7_total=4)


def test_screening_summary_for_s18_keys():
    screening = {
        "session_id": "s1",
        "risk_level": "Low",
        "confidence": 0.7,
        "flags": ["a"],
        "display_labels": ["PHQ-9 (5): Mild depressive symptom severity (screening, not a diagnosis)."],
        "recommendations": ["Repeat PHQ-9/GAD-7 at follow-up to monitor trend over time."],
        "phq9_total": 5,
        "gad7_total": 4,
        "phq9_band": "mild",
        "gad7_band": "minimal",
        "crisis": False,
    }
    s = screening_summary_for_s18(screening)
    assert "phq9_total" in s
    assert "crisis" in s
    assert s.get("display_labels") == screening["display_labels"]
    assert s.get("recommendations") == screening["recommendations"]


def test_mental_health_query_contains_task_tag():
    p = MentalHealthInput(phq9_total=10, gad7_total=5)
    local = {"risk_level": "Moderate", "session_id": "x"}
    q = _mental_health_to_query(p, "pid-9", "full", local)
    assert "[Task: mental_health]" in q
    assert "pid-9" in q
    body = json.loads(q.split("Request: ", 1)[1])
    assert body["task"] == "mental_health"
    assert "local_screening" in body
