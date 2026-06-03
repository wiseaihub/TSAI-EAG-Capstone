"""Unit tests for WISE adapter result normalization and cancel-event."""

import threading
import time

from app.agents.wise_adapter import _s18_response_to_result, _poll_s18_run


def test_s18_response_to_result_dedupes_flags_across_sources():
    """Top-level and node-level duplicate flags should be returned once."""
    s18_data = {
        "status": "completed",
        "output": {
            "risk_level": "high",
            "confidence": 0.95,
            "flags": ["low_hemoglobin", "high_wbc"],
        },
        "graph": {
            "nodes": [
                {
                    "data": {
                        "output": {
                            "risk_level": "high",
                            "confidence": 0.95,
                            "flags": ["low_hemoglobin", "high_wbc"],
                        }
                    }
                }
            ]
        },
    }

    result = _s18_response_to_result(s18_data, run_id="run-1")

    assert result["flags"] == ["low_hemoglobin", "high_wbc"]


def test_s18_response_to_result_extracts_recommendations_from_response_text():
    s18_data = {
        "status": "completed",
        "graph": {
            "nodes": [
                {
                    "data": {
                        "output": {
                            "risk_level": "high",
                            "confidence": 0.95,
                            "flags": ["low_hemoglobin", "high_wbc"],
                            "response": (
                                "Initial assessment indicates anemia and potential inflammation. "
                                "Recommended next steps include CMP, iron studies, peripheral blood smear, "
                                "and infection testing."
                            ),
                        }
                    }
                }
            ]
        },
    }

    result = _s18_response_to_result(s18_data, run_id="run-2")

    assert "CMP" in result["recommendations"]
    assert "iron studies" in result["recommendations"]
    assert "peripheral blood smear" in result["recommendations"]


def test_poll_s18_run_exits_on_cancel_event(monkeypatch):
    """When cancel_event is set before the first poll iteration,
    _poll_s18_run should raise TimeoutError within ~0s, not sleep
    for the full poll timeout."""
    monkeypatch.setattr("app.agents.wise_adapter._get_poll_timeout_sec", lambda: 300)

    cancel = threading.Event()
    cancel.set()

    start = time.monotonic()
    try:
        _poll_s18_run("fake-run-id", access_token=None, cancel_event=cancel)
        assert False, "Expected TimeoutError"
    except TimeoutError as e:
        elapsed = time.monotonic() - start
        assert "cancelled by caller" in str(e)
        assert elapsed < 2.0, f"Should exit immediately but took {elapsed:.1f}s"


def test_s18_response_to_result_collects_narrative_kb_and_rationale_fields():
    """Rationale, citations, RAG-style chunks, and long narrative strings surface for the UI."""
    s18_data = {
        "status": "completed",
        "graph": {
            "nodes": [
                {
                    "data": {
                        "output": {
                            "risk_level": "Moderate",
                            "confidence": 0.72,
                            "flags": ["mock_mh"],
                            "rationale_lines": ["PHQ-9 band suggests follow-up correlation."],
                            "evidence_citations": ["Screening thresholds per Kroenke et al."],
                            "retrieved_chunks": [
                                {"text": "Major depressive disorder diagnostic criteria excerpt for pilot display."},
                            ],
                            "narrative_text": ("Synthetic narrative tying screening scores to clinician-facing summary text " * 3),
                        },
                    },
                },
            ],
        },
    }

    result = _s18_response_to_result(s18_data, run_id="run-mh-kb")

    rationale = result.get("rationale_lines") or []
    assert rationale and "PHQ-9 band" in rationale[0]
    cites = result.get("evidence_citations") or []
    assert any("Kroenke" in c for c in cites)
    assert any("Major depressive" in c or "[KB excerpt]" in c for c in cites)
    snippets = result.get("kb_snippets") or []
    assert snippets and "Major depressive" in snippets[0]
    assert result.get("wise_narrative") and len(result["wise_narrative"]) > 120


def test_s18_response_to_result_exposes_mh_plan_guard_marker():
    s18_data = {
        "status": "completed",
        "graph": {
            "nodes": [
                {
                    "id": "Query",
                    "data": {
                        "output": {
                            "plan_graph": {"nodes": [], "edges": []},
                            "mental_health_plan_guard_applied": True,
                        }
                    },
                },
                {
                    "id": "T001",
                    "data": {
                        "output": {
                            "risk_level": "moderate",
                            "confidence": 0.8,
                            "flags": ["mock_s18"],
                        }
                    },
                },
            ]
        },
    }

    result = _s18_response_to_result(s18_data, run_id="run-mh-guard")

    assert "mental_health_plan_guard_applied" in result["flags"]
