"""Unit tests for WISE adapter result normalization."""

from app.agents.wise_adapter import _s18_response_to_result


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
