"""
WISE adapter: converts payload + patient context into S18 task format,
invokes S18 runtime via HTTP, persists result to AgentSession, returns structured result.
"""
import json
import os
import re
import threading
import time
from datetime import datetime
from uuid import uuid4

import requests

from app.db.models import AgentRun, AgentSession, RunArtifact

# #region agent log
DEBUG_LOG_PATH = os.environ.get("DEBUG_LOG_PATH", "debug-f905fa.log")
DEBUG_SESSION_LOG_PATH = "debug-70a340.log"
DEBUG_SESSION_ID = "70a340"
def _debug_log(message: str, data: dict, hypothesis_id: str, run_id: str = ""):
    try:
        payload = {"sessionId": "f905fa", "runId": run_id, "hypothesisId": hypothesis_id, "location": "wise_adapter.py", "message": message, "data": data, "timestamp": int(time.time() * 1000)}
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")
    except Exception:
        pass
# #endregion

# #region agent log
def _debug_session_log(message: str, data: dict, hypothesis_id: str, run_id: str = ""):
    try:
        payload = {
            "sessionId": DEBUG_SESSION_ID,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": "wise_adapter.py",
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        line = json.dumps(payload, default=str) + "\n"
        candidate_paths = ["/workspace/debug-70a340.log", DEBUG_SESSION_LOG_PATH]
        for p in candidate_paths:
            try:
                with open(p, "a", encoding="utf-8") as f:
                    f.write(line)
            except Exception:
                pass
    except Exception:
        pass
# #endregion

S18_BASE_URL = os.environ.get("S18_BASE_URL", "http://s18share-api:8000")
S18_POLL_INTERVAL_SEC = float(os.environ.get("S18_POLL_INTERVAL_SEC", "2.0"))


def _get_poll_timeout_sec() -> float:
    """Total wait timeout for polling GET /runs/{id}. Use config (env RUN_POLL_TIMEOUT_SECONDS or settings.json)."""
    from app.core.config import settings
    return float(settings.run_poll_timeout_seconds)


def _s18_auth_headers(access_token: str | None = None) -> dict:
    """Build optional S18 auth headers from request/env token."""
    token = access_token or (
        os.environ.get("S18_BEARER_TOKEN")
        or os.environ.get("S18_AUTH_TOKEN")
        or os.environ.get("S18_API_KEY")
    )
    if token:
        bearer = f"Bearer {token}"
        return {
            "Authorization": bearer,
            # Some S18 deployments read forwarded auth header.
            "X-Forwarded-Authorization": bearer,
        }
    return {}


def _payload_to_query(payload, patient_id: str, execution_mode: str = "full") -> str:
    """Turn payload (e.g. CBCInput or dict) into a single query string with patient context."""
    if hasattr(payload, "model_dump"):
        body = payload.model_dump()
    elif isinstance(payload, dict):
        body = payload
    else:
        body = {"payload": str(payload)}
    mode = (execution_mode or "full").strip().lower()
    if mode not in {"fast", "full"}:
        mode = "full"
    return f"[Patient ID: {patient_id}] [Execution Mode: {mode}] Request: {json.dumps(body)}"


def _normalize_execution_mode(execution_mode: str) -> str:
    mode = (execution_mode or "full").strip().lower()
    if mode not in {"fast", "full"}:
        mode = "full"
    return mode


def _mental_health_to_query(payload, patient_id: str, execution_mode: str, local_screening: dict) -> str:
    """Build S18 query for mental health task with embedded local screening summary."""
    if hasattr(payload, "model_dump"):
        patient_payload = payload.model_dump()
    elif isinstance(payload, dict):
        patient_payload = payload
    else:
        patient_payload = {"payload": str(payload)}
    mode = _normalize_execution_mode(execution_mode)
    body = {
        "task": "mental_health",
        "patient_payload": patient_payload,
        "local_screening": local_screening,
    }
    screening_json = json.dumps(local_screening, default=str)
    return (
        f"[Task: mental_health] [Patient ID: {patient_id}] "
        f"[Local screening: {screening_json}] [Execution Mode: {mode}] "
        f"Request: {json.dumps(body, default=str)}"
    )


def _run_s18_agent(
    query: str,
    patient_id: str,
    db,
    access_token: str | None,
    agent_name: str,
    agent_version: str = "v1",
    case_id: str | None = None,
    cancel_event: threading.Event | None = None,
    run_metadata: dict | None = None,
    *,
    log_entry_label: str = "run_s18_agent",
) -> dict:
    """
    POST /runs, poll, map to risk_level/confidence/flags, persist AgentSession.
    Returns public fields only (no s18_status).
    """
    # #region agent log
    _debug_log(
        f"{log_entry_label}: query built",
        {
            "query_preview": query[:300] + "..." if len(query) > 300 else query,
            "S18_BASE_URL": S18_BASE_URL,
            "patient_id": patient_id,
            "agent_name": agent_name,
        },
        "B",
        run_id="",
    )
    _debug_session_log(
        f"{log_entry_label} entry",
        {
            "patient_id_len": len(str(patient_id or "")),
            "s18_base_url": S18_BASE_URL,
            "execution_query_len": len(query),
            "is_host_docker_internal": "host.docker.internal" in S18_BASE_URL,
            "uses_request_token": bool(access_token),
            "agent_name": agent_name,
        },
        "H1;H2;H4",
        run_id="",
    )
    # #endregion
    try:
        run_id = _invoke_s18_run(query, access_token=access_token, run_metadata=run_metadata)
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
            agent_name=agent_name,
            agent_version=agent_version,
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            flags=result["flags"],
            timestamp=datetime.utcnow(),
        )
        if db is not None:
            db.add(record)
            if case_id:
                db.add(
                    AgentRun(
                        id=str(uuid4()),
                        case_id=case_id,
                        session_id=result["session_id"],
                        s18_run_id=None,
                        agent_name=agent_name,
                        status="failed",
                        started_at=datetime.utcnow(),
                        finished_at=datetime.utcnow(),
                        error_text="s18_start_error",
                        metrics={"flags": result["flags"]},
                        created_at=datetime.utcnow(),
                    )
                )
            db.commit()
        return {k: v for k, v in result.items() if k != "s18_status"}

    try:
        s18_data = _poll_s18_run(run_id, access_token=access_token, cancel_event=cancel_event)
    except (TimeoutError, requests.RequestException) as e:
        if isinstance(e, TimeoutError):
            result = {
                "risk_level": "Moderate",
                "confidence": 0.2,
                "flags": [
                    "s18_poll_timeout_soft_fallback",
                    f"s18_poll_error: {str(e)}",
                ],
                "session_id": run_id,
                "s18_status": "error",
            }
        else:
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
            agent_name=agent_name,
            agent_version=agent_version,
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            flags=result["flags"],
            timestamp=datetime.utcnow(),
        )
        if db is not None:
            db.add(record)
            if case_id:
                db.add(
                    AgentRun(
                        id=str(uuid4()),
                        case_id=case_id,
                        session_id=run_id,
                        s18_run_id=run_id,
                        agent_name=agent_name,
                        status="failed",
                        started_at=datetime.utcnow(),
                        finished_at=datetime.utcnow(),
                        error_text=str(e)[:500],
                        metrics={"flags": result["flags"]},
                        created_at=datetime.utcnow(),
                    )
                )
            db.commit()
        return {k: v for k, v in result.items() if k != "s18_status"}

    result = _s18_response_to_result(s18_data, run_id)
    session_id = result.get("session_id") or str(uuid4())

    record = AgentSession(
        session_id=session_id,
        patient_id=patient_id,
        agent_name=agent_name,
        agent_version=agent_version,
        risk_level=result["risk_level"],
        confidence=result["confidence"],
        flags=result["flags"],
        timestamp=datetime.utcnow(),
    )
    if db is not None:
        db.add(record)
        if case_id:
            run_row_id = str(uuid4())
            db.add(
                AgentRun(
                    id=run_row_id,
                    case_id=case_id,
                    session_id=session_id,
                    s18_run_id=run_id,
                    agent_name=agent_name,
                    status="completed",
                    started_at=datetime.utcnow(),
                    finished_at=datetime.utcnow(),
                    error_text=None,
                    metrics={"confidence": result["confidence"]},
                    created_at=datetime.utcnow(),
                )
            )
            db.add(
                RunArtifact(
                    id=str(uuid4()),
                    run_id=run_row_id,
                    artifact_type="wise_result",
                    storage_path=None,
                    payload={
                        "risk_level": result["risk_level"],
                        "confidence": result["confidence"],
                        "flags": result["flags"],
                        "recommendations": result.get("recommendations", []),
                    },
                    created_at=datetime.utcnow(),
                )
            )
        db.commit()

    return {
        "risk_level": result["risk_level"],
        "confidence": result["confidence"],
        "flags": result["flags"],
        "session_id": session_id,
        "recommendations": result.get("recommendations", []),
    }


def _invoke_s18_run(query: str, access_token: str | None = None, run_metadata: dict | None = None) -> str:
    """Start S18 run via POST /runs. Returns run_id."""
    url = f"{S18_BASE_URL}/runs"
    auth_env_presence = {
        "S18_API_KEY": bool(os.environ.get("S18_API_KEY")),
        "S18_AUTH_TOKEN": bool(os.environ.get("S18_AUTH_TOKEN")),
        "S18_BEARER_TOKEN": bool(os.environ.get("S18_BEARER_TOKEN")),
    }
    headers = _s18_auth_headers(access_token)
    # #region agent log
    _debug_session_log(
        "POST /runs about to execute",
        {
            "url": url,
            "query_len": len(query),
            "auth_env_presence": auth_env_presence,
            "has_authorization_header": "Authorization" in headers,
            "has_x_forwarded_authorization_header": "X-Forwarded-Authorization" in headers,
        },
        "H1;H2",
        run_id="",
    )
    # #endregion
    request_payload = {"query": query}
    if isinstance(run_metadata, dict):
        for key in (
            "integration_id",
            "workflow_id",
            "contract_version",
            "source_system",
            "external_event_id",
            "raw_payload",
            "consent_ref",
            "idempotency_key",
        ):
            value = run_metadata.get(key)
            if value is not None:
                request_payload[key] = value
    try:
        resp = requests.post(
            url,
            json=request_payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
    except requests.HTTPError as e:
        response = getattr(e, "response", None)
        status_code = response.status_code if response is not None else None
        body_preview = ""
        www_authenticate = None
        if response is not None:
            body_preview = (response.text or "")[:500]
            www_authenticate = response.headers.get("www-authenticate")
        # #region agent log
        _debug_session_log(
            "POST /runs HTTP error",
            {
                "url": url,
                "status_code": status_code,
                "www_authenticate": www_authenticate,
                "body_preview": body_preview,
                "auth_env_presence": auth_env_presence,
            },
            "H1;H2;H3;H4",
            run_id="",
        )
        # #endregion
        raise
    except requests.RequestException as e:
        # #region agent log
        _debug_session_log(
            "POST /runs request exception",
            {"url": url, "error_type": type(e).__name__, "error": str(e)},
            "H5",
            run_id="",
        )
        # #endregion
        raise

    data = resp.json()
    # #region agent log
    _debug_log("S18 POST /runs response", {"run_id": data.get("id"), "response_keys": list(data.keys()), "base_url": S18_BASE_URL, "query_preview": (query[:200] + "..." if len(query) > 200 else query)}, "B", run_id=data.get("id", ""))
    # #endregion
    return data["id"]


def _poll_s18_run(
    run_id: str,
    access_token: str | None = None,
    cancel_event: "threading.Event | None" = None,
) -> dict:
    """Poll GET /runs/{run_id} until status is completed or failed. Returns final response.

    If *cancel_event* is set by the caller (e.g. orchestrator timeout), the loop
    exits early with a TimeoutError so the background thread stops promptly
    instead of continuing to poll (and hold a DB connection) for minutes.
    """
    poll_timeout_sec = _get_poll_timeout_sec()
    deadline = time.monotonic() + poll_timeout_sec
    headers = _s18_auth_headers(access_token)
    while time.monotonic() < deadline:
        if cancel_event is not None and cancel_event.is_set():
            raise TimeoutError(f"S18 run {run_id} cancelled by caller (orchestrator timeout)")
        resp = requests.get(f"{S18_BASE_URL}/runs/{run_id}", headers=headers, timeout=10)
        if resp.status_code == 404:
            time.sleep(S18_POLL_INTERVAL_SEC)
            continue
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
        if cancel_event is not None:
            cancel_event.wait(S18_POLL_INTERVAL_SEC)
        else:
            time.sleep(S18_POLL_INTERVAL_SEC)
    raise TimeoutError(f"S18 run {run_id} did not complete within {poll_timeout_sec}s")


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


def _flags_to_list(flags: object) -> list:
    """Normalize flags to a list of strings. Accept list or dict (e.g. CBC-style)."""
    if isinstance(flags, list):
        return [str(x) for x in flags if x is not None]
    if isinstance(flags, dict):
        out = []
        for k, v in flags.items():
            if v is True:
                out.append(str(k))
            elif v is not False and v is not None:
                out.append(f"{k}: {v}")
        return out
    return []


def _dedupe_flags(flags: list[str]) -> list[str]:
    """Remove duplicate flags while preserving first-seen order."""
    seen: set[str] = set()
    out: list[str] = []
    for flag in flags:
        item = str(flag)
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _recommendations_to_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    return []


def _extract_recommendations_from_text(text: str) -> list[str]:
    if not isinstance(text, str) or not text.strip():
        return []
    lowered = text.lower()
    marker = "recommended next steps include"
    start = lowered.find(marker)
    if start == -1:
        return []
    chunk = text[start + len(marker):]
    chunk = chunk.split("\n", 1)[0]
    chunk = chunk.strip(" .:-")
    if not chunk:
        return []
    # Split on commas and conjunctions for short, UI-ready items.
    parts = re.split(r",|\band\b", chunk, flags=re.IGNORECASE)
    out: list[str] = []
    for part in parts:
        item = part.strip(" .;-")
        if item:
            out.append(item)
    return out


def _dedupe_recommendations(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        normalized = " ".join(str(item).split()).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(normalized)
    return out


def _detect_mh_plan_guard_applied(s18_data: dict) -> bool:
    """Detect whether S18 planner applied the mental-health routing guard."""
    if not isinstance(s18_data, dict):
        return False
    if s18_data.get("mental_health_plan_guard_applied") is True:
        return True

    graph = s18_data.get("graph") or {}
    if not isinstance(graph, dict):
        return False
    if graph.get("mental_health_plan_guard_applied") is True:
        return True

    nodes = graph.get("nodes") or graph.get("graph", {}).get("nodes") or []
    if not isinstance(nodes, list):
        return False
    for node in nodes:
        if not isinstance(node, dict):
            continue
        data = node.get("data") or {}
        if not isinstance(data, dict):
            continue
        for field in ("output", "result", "response", "value"):
            raw = data.get(field) or node.get(field)
            if isinstance(raw, dict) and raw.get("mental_health_plan_guard_applied") is True:
                return True
            if isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    continue
                if isinstance(parsed, dict) and parsed.get("mental_health_plan_guard_applied") is True:
                    return True
    return False


def _s18_response_to_result(s18_data: dict, run_id: str) -> dict:
    """Map S18 GET response to WISE result shape: risk_level, confidence, flags."""
    status = s18_data.get("status", "unknown")
    graph = s18_data.get("graph") or {}

    if status == "failed":
        # #region agent log
        _debug_log("_s18_response_to_result: status failed", {"s18_keys": list(s18_data.keys()), "has_error": "error" in s18_data, "has_message": "message" in s18_data, "graph_type": type(s18_data.get("graph")).__name__}, "A;C", run_id=run_id)
        # #endregion
        failure_reason = _extract_s18_failure_reason(s18_data)
        if failure_reason:
            try:
                parsed_reason = json.loads(failure_reason)
            except Exception:
                parsed_reason = None
            if isinstance(parsed_reason, dict) and isinstance(parsed_reason.get("plan_graph"), dict):
                flags = ["s18_planner_payload_in_failure", "s18_soft_fallback_applied"]
                flags.append("s18_reason: planner payload returned in failure path")
                return {
                    "risk_level": "Moderate",
                    "confidence": 0.35,
                    "flags": flags,
                    "session_id": run_id,
                    "s18_status": status,
                }
        if failure_reason and "missing plan_graph" in failure_reason.lower():
            flags = ["s18_planner_contract_error", "s18_soft_fallback_applied"]
            flags.append(f"s18_reason: {failure_reason[:500]}")
            return {
                "risk_level": "Moderate",
                "confidence": 0.25,
                "flags": flags,
                "session_id": run_id,
                "s18_status": status,
            }
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

    # completed: derive from top-level result first, then from graph nodes
    risk_level = "Moderate"
    confidence = 0.8
    flags: list[str] = []
    recommendations: list[str] = []

    def apply_output(out: dict | None) -> None:
        nonlocal risk_level, confidence, flags, recommendations
        if not isinstance(out, dict):
            return
        if out.get("risk_level"):
            risk_level = out["risk_level"]
        if out.get("confidence") is not None:
            try:
                confidence = float(out["confidence"])
            except (TypeError, ValueError):
                pass
        fl = out.get("flags")
        if fl is not None:
            flags.extend(_flags_to_list(fl))
        recommendations.extend(_recommendations_to_list(out.get("recommendations")))
        recommendations.extend(_recommendations_to_list(out.get("next_steps")))
        recommendations.extend(_extract_recommendations_from_text(str(out.get("response", ""))))

    # Top-level: some S18 responses put final result in output/result/response/data
    for key in ("output", "result", "response", "data"):
        raw = s18_data.get(key)
        if raw is None:
            continue
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                continue
        if isinstance(raw, dict):
            apply_output(raw)
            break

    # Graph nodes: collect from each node's data.output, data.result, or output
    if isinstance(graph, dict):
        nodes = graph.get("nodes") or graph.get("graph", {}).get("nodes") or []
        for node in nodes:
            if not isinstance(node, dict):
                continue
            data = node.get("data") or {}
            for field in ("output", "result", "response", "value"):
                raw = data.get(field) or node.get(field)
                if raw is None:
                    continue
                if isinstance(raw, str):
                    try:
                        raw = json.loads(raw)
                    except (json.JSONDecodeError, TypeError):
                        continue
                if isinstance(raw, dict):
                    apply_output(raw)
                    break

    if _detect_mh_plan_guard_applied(s18_data):
        flags.append("mental_health_plan_guard_applied")
    flags = _dedupe_flags(flags)
    recommendations = _dedupe_recommendations(recommendations)

    # #region agent log — log what we extracted for debugging empty flags
    _debug_log(
        "S18 completed result",
        {
            "run_id": run_id,
            "risk_level": risk_level,
            "confidence": confidence,
            "flags_count": len(flags),
            "flags_preview": flags[:20] if flags else [],
            "recommendations_count": len(recommendations),
            "recommendations_preview": recommendations[:10] if recommendations else [],
            "graph_keys": list(graph.keys()) if isinstance(graph, dict) else [],
            "nodes_count": len(graph.get("nodes") or []) if isinstance(graph, dict) else 0,
        },
        "A;C",
        run_id=run_id,
    )
    # #endregion

    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "flags": flags,
        "recommendations": recommendations,
        "session_id": run_id,
        "s18_status": status,
    }


def run_wise_agent(
    payload,
    patient_id,
    db=None,
    access_token: str | None = None,
    execution_mode: str = "full",
    case_id: str | None = None,
    cancel_event: threading.Event | None = None,
    run_metadata: dict | None = None,
):
    """
    Convert payload into S18 task format, invoke S18 runtime via HTTP,
    persist result to AgentSession, return structured result.
    """
    query = _payload_to_query(payload, patient_id, execution_mode=execution_mode)
    return _run_s18_agent(
        query,
        patient_id,
        db,
        access_token,
        "wise_agent",
        "v1",
        case_id=case_id,
        cancel_event=cancel_event,
        run_metadata=run_metadata,
        log_entry_label="run_wise_agent",
    )


def run_mental_health_wise(
    payload,
    patient_id: str,
    local_screening: dict,
    db=None,
    access_token: str | None = None,
    execution_mode: str = "full",
    case_id: str | None = None,
    cancel_event: threading.Event | None = None,
    run_metadata: dict | None = None,
):
    """
    Mental health S18 pass: query tags [Task: mental_health] and embeds local screening summary.
    Persists AgentSession with agent_name mental_health_wise.
    """
    query = _mental_health_to_query(payload, patient_id, execution_mode, local_screening)
    return _run_s18_agent(
        query,
        patient_id,
        db,
        access_token,
        "mental_health_wise",
        "v1",
        case_id=case_id,
        cancel_event=cancel_event,
        run_metadata=run_metadata,
        log_entry_label="run_mental_health_wise",
    )
