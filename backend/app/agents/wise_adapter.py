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

# #region agent log
DEBUG_LOG_PATH = os.environ.get("DEBUG_LOG_PATH", "debug-f905fa.log")
def _debug_log(message: str, data: dict, hypothesis_id: str, run_id: str = ""):
    try:
        payload = {"sessionId": "f905fa", "runId": run_id, "hypothesisId": hypothesis_id, "location": "wise_adapter.py", "message": message, "data": data, "timestamp": int(time.time() * 1000)}
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")
    except Exception:
        pass
# #endregion

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
    # #region agent log
    _debug_log("S18 POST /runs response", {"run_id": data.get("id"), "response_keys": list(data.keys()), "base_url": S18_BASE_URL, "query_preview": (query[:200] + "..." if len(query) > 200 else query)}, "B", run_id=data.get("id", ""))
    # #endregion
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
            # #region agent log
            safe = {"status": status, "keys": list(data.keys())}
            if status == "failed":
                safe["error"] = data.get("error")
                safe["message"] = data.get("message")
                if data.get("graph"):
                    g = data.get("graph") if isinstance(data.get("graph"), dict) else {}
                    safe["graph_keys"] = list(g.keys()) if g else []
                    safe["graph_error"] = g.get("error") or g.get("message")
                    nodes = g.get("nodes") or []
                    if not isinstance(nodes, list):
                        nodes = []
                    safe["node_summaries"] = [{"id": n.get("id"), "data_keys": list((n.get("data") or {}).keys()), "data_error": (n.get("data") or {}).get("error"), "data_output_preview": str((n.get("data") or {}).get("output"))[:200] if (n.get("data") or {}).get("output") is not None else None} for n in nodes[:10] if isinstance(n, dict)]
            _debug_log("S18 poll final response", safe, "A;C;D;E", run_id=run_id)
            # #endregion
            return data
        time.sleep(S18_POLL_INTERVAL_SEC)
    raise TimeoutError(f"S18 run {run_id} did not complete within {S18_POLL_TIMEOUT_SEC}s")


def _extract_s18_failure_reason(s18_data: dict) -> str | None:
    """Extract failure reason from S18 response when status is failed."""
    reason = s18_data.get("error") or s18_data.get("message")
    if isinstance(reason, str) and reason.strip():
        return reason.strip()
    graph = s18_data.get("graph") or {}
    if isinstance(graph, dict):
        reason = graph.get("error") or graph.get("message")
        if isinstance(reason, str) and reason.strip():
            return reason.strip()
        nodes = graph.get("nodes") or []
        if isinstance(nodes, list):
            for n in nodes:
                if not isinstance(n, dict):
                    continue
                data = n.get("data") or {}
                reason = data.get("error") or (data.get("output") if isinstance(data.get("output"), str) else None)
                if isinstance(reason, str) and reason.strip():
                    return reason.strip()
    return None


def _s18_response_to_result(s18_data: dict, run_id: str) -> dict:
    """Map S18 GET response to WISE result shape: risk_level, confidence, flags."""
    status = s18_data.get("status", "unknown")
    graph = s18_data.get("graph") or {}

    if status == "failed":
        # #region agent log
        _debug_log("_s18_response_to_result: status failed", {"s18_keys": list(s18_data.keys()), "has_error": "error" in s18_data, "has_message": "message" in s18_data, "graph_type": type(s18_data.get("graph")).__name__}, "A;C", run_id=run_id)
        # #endregion
        failure_reason = _extract_s18_failure_reason(s18_data)
        flags = ["s18_run_failed"]
        if failure_reason:
            flags.append(f"s18_reason: {failure_reason[:500]}")
        return {
            "risk_level": "High",
            "confidence": 0.0,
            "flags": flags,
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
    # #region agent log
    _debug_log("run_wise_agent: query built", {"query_preview": query[:300] + "..." if len(query) > 300 else query, "S18_BASE_URL": S18_BASE_URL, "patient_id": patient_id}, "B", run_id="")
    # #endregion
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
