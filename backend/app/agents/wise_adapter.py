"""
WISE adapter: converts payload + patient context into S18 task format,
invokes S18 runtime via HTTP, persists result to AgentSession, returns structured result.
"""
import json
import os
import time
from datetime import datetime
from uuid import uuid4

import requests

from app.db.models import AgentSession

S18_BASE_URL = os.environ.get("S18_BASE_URL", "http://localhost:8001")
S18_POLL_INTERVAL_SEC = float(os.environ.get("S18_POLL_INTERVAL_SEC", "2.0"))
S18_POLL_TIMEOUT_SEC = float(os.environ.get("S18_POLL_TIMEOUT_SEC", "120.0"))


def _payload_to_query(payload, patient_id: str) -> str:
    """Turn payload (e.g. CBCInput or dict) into a single query string with patient context."""
    if hasattr(payload, "model_dump"):
        body = payload.model_dump()
    elif isinstance(payload, dict):
        body = payload
    else:
        body = {"payload": str(payload)}
    return f"[Patient ID: {patient_id}] Request: {json.dumps(body)}"


def _invoke_s18_run(query: str) -> str:
    """Start S18 run via POST /runs. Returns run_id."""
    resp = requests.post(
        f"{S18_BASE_URL}/runs",
        json={"query": query},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["id"]


def _poll_s18_run(run_id: str) -> dict:
    """Poll GET /runs/{run_id} until status is completed or failed. Returns final response."""
    deadline = time.monotonic() + S18_POLL_TIMEOUT_SEC
    while time.monotonic() < deadline:
        resp = requests.get(f"{S18_BASE_URL}/runs/{run_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")
        if status in ("completed", "failed"):
            return data
        time.sleep(S18_POLL_INTERVAL_SEC)
    raise TimeoutError(f"S18 run {run_id} did not complete within {S18_POLL_TIMEOUT_SEC}s")


def _s18_response_to_result(s18_data: dict, run_id: str) -> dict:
    """Map S18 GET response to WISE result shape: risk_level, confidence, flags."""
    status = s18_data.get("status", "unknown")
    graph = s18_data.get("graph") or {}

    if status == "failed":
        return {
            "risk_level": "High",
            "confidence": 0.0,
            "flags": ["s18_run_failed"],
            "session_id": run_id,
            "s18_status": status,
        }

    # completed: derive from graph if possible (node outputs, etc.)
    risk_level = "Moderate"
    confidence = 0.8
    flags = []

    if isinstance(graph, dict):
        nodes = graph.get("nodes") or graph.get("graph", {}).get("nodes") or []
        for node in nodes:
            if isinstance(node, dict):
                out = node.get("data", {}).get("output") or node.get("output")
                if isinstance(out, dict):
                    if out.get("risk_level"):
                        risk_level = out["risk_level"]
                    if out.get("confidence") is not None:
                        confidence = float(out["confidence"])
                    if isinstance(out.get("flags"), list):
                        flags = out["flags"]

    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "flags": flags if flags else [],
        "session_id": run_id,
        "s18_status": status,
    }


def run_wise_agent(payload, patient_id, db):
    """
    Convert payload into S18 task format, invoke S18 runtime via HTTP,
    persist result to AgentSession, return structured result.
    """
    query = _payload_to_query(payload, patient_id)

    try:
        run_id = _invoke_s18_run(query)
    except requests.RequestException as e:
        result = {
            "risk_level": "High",
            "confidence": 0.0,
            "flags": [f"s18_start_error: {str(e)}"],
            "session_id": str(uuid4()),
            "s18_status": "error",
        }
        record = AgentSession(
            session_id=result["session_id"],
            patient_id=patient_id,
            agent_name="wise_agent",
            agent_version="v1",
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            flags=result["flags"],
            timestamp=datetime.utcnow(),
        )
        db.add(record)
        db.commit()
        return {k: v for k, v in result.items() if k != "s18_status"}

    try:
        s18_data = _poll_s18_run(run_id)
    except (TimeoutError, requests.RequestException) as e:
        result = {
            "risk_level": "High",
            "confidence": 0.0,
            "flags": [f"s18_poll_error: {str(e)}"],
            "session_id": run_id,
            "s18_status": "error",
        }
        record = AgentSession(
            session_id=run_id,
            patient_id=patient_id,
            agent_name="wise_agent",
            agent_version="v1",
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            flags=result["flags"],
            timestamp=datetime.utcnow(),
        )
        db.add(record)
        db.commit()
        return {k: v for k, v in result.items() if k != "s18_status"}

    result = _s18_response_to_result(s18_data, run_id)
    session_id = result.get("session_id") or str(uuid4())


    record = AgentSession(
        session_id=session_id,
        patient_id=patient_id,
        agent_name="wise_agent",
        agent_version="v1",
        risk_level=result["risk_level"],
        confidence=result["confidence"],
        flags=result["flags"],
        timestamp=datetime.utcnow(),
    )
    db.add(record)
    db.commit()

    return {
        "risk_level": result["risk_level"],
        "confidence": result["confidence"],
        "flags": result["flags"],
    }
