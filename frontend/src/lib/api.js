const DEFAULT_API_BASE = "http://localhost:8000";

export function getApiBase() {
  return import.meta.env.VITE_API_URL || DEFAULT_API_BASE;
}

function normalizeErrorPayload(status, err) {
  const detail = err?.detail;
  if (typeof detail === "object" && detail != null) {
    return {
      error: detail?.error || status,
      status,
      traceback: detail?.traceback,
      type: detail?.type,
    };
  }

  return {
    error: detail || status,
    status,
  };
}

async function parseJsonResponse(response) {
  if (response.ok) {
    return {
      ok: true,
      data: await response.json(),
      pollTimeoutSeconds: Number(response.headers.get("X-Poll-Timeout-Seconds")) || null,
    };
  }

  const err = await response.json().catch(() => ({ detail: response.statusText }));
  return {
    ok: false,
    data: normalizeErrorPayload(response.status, err),
    pollTimeoutSeconds: Number(response.headers.get("X-Poll-Timeout-Seconds")) || null,
  };
}

export async function fetchHealthConfig() {
  const response = await fetch(`${getApiBase()}/health`);
  const data = await response.json();
  return {
    pollTimeoutSeconds: data?.poll_timeout_seconds,
  };
}

export async function analyzeCbc({ token, payload, fastMode, timeoutMs }) {
  const controller = new AbortController();
  let timeoutId;
  try {
    timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    const response = await fetch(`${getApiBase()}/analyze?fast=${fastMode}`, {
      method: "POST",
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });
    return await parseJsonResponse(response);
  } finally {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

export async function analyzeMh({ token, payload, timeoutMs }) {
  const controller = new AbortController();
  let timeoutId;
  try {
    timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    const response = await fetch(`${getApiBase()}/mental-health/analyze`, {
      method: "POST",
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });
    return await parseJsonResponse(response);
  } finally {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

export async function fetchRecentAgentSessions(token) {
  const response = await fetch(`${getApiBase()}/agent-sessions`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Unable to fetch sessions (${response.status})`);
  }
  return await response.json();
}

export async function fetchCurrentUser(token) {
  const response = await fetch(`${getApiBase()}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const parsed = await parseJsonResponse(response);
  if (!parsed.ok) {
    const err = new Error(String(parsed.data?.error || "Unable to fetch current user"));
    err.status = parsed.data?.status || response.status;
    throw err;
  }
  return parsed.data;
}
