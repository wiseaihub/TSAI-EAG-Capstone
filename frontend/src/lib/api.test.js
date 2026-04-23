import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { analyzeCbc, analyzeMh, fetchCurrentUser, fetchRecentAgentSessions, getApiBase } from "./api";

function jsonResponse(body, init = {}) {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    statusText: init.statusText ?? "OK",
    headers: { "Content-Type": "application/json", ...(init.headers || {}) },
  });
}

describe("getApiBase", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("uses VITE_API_URL when provided", () => {
    vi.stubEnv("VITE_API_URL", "https://api.example.test");
    expect(getApiBase()).toBe("https://api.example.test");
  });

  it("defaults to localhost:8000 otherwise", () => {
    vi.stubEnv("VITE_API_URL", "");
    expect(getApiBase()).toBe("http://localhost:8000");
  });
});

describe("analyzeCbc", () => {
  beforeEach(() => {
    vi.stubEnv("VITE_API_URL", "https://api.example.test");
  });
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("POSTs JSON payload with Authorization bearer and fast-mode query param", async () => {
    const fetchMock = vi.fn(async () => jsonResponse({ result: "ok" }));
    vi.stubGlobal("fetch", fetchMock);

    const response = await analyzeCbc({
      token: "abc.def.ghi",
      payload: { hemoglobin: 12.3 },
      fastMode: true,
      timeoutMs: 5000,
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("https://api.example.test/analyze?fast=true");
    expect(init.method).toBe("POST");
    expect(init.headers.Authorization).toBe("Bearer abc.def.ghi");
    expect(init.headers["Content-Type"]).toBe("application/json");
    expect(JSON.parse(init.body)).toEqual({ hemoglobin: 12.3 });
    expect(response.ok).toBe(true);
    expect(response.data).toEqual({ result: "ok" });
  });

  it("normalizes non-ok responses into { ok: false, data: { status, error } }", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => jsonResponse({ detail: "forbidden" }, { status: 403, statusText: "Forbidden" }))
    );

    const response = await analyzeCbc({
      token: "t",
      payload: {},
      fastMode: false,
      timeoutMs: 5000,
    });

    expect(response.ok).toBe(false);
    expect(response.data.status).toBe(403);
    expect(response.data.error).toBe("forbidden");
  });

  it("reads the X-Poll-Timeout-Seconds response header when present", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async () =>
          new Response(JSON.stringify({ ok: true }), {
            status: 200,
            headers: { "Content-Type": "application/json", "X-Poll-Timeout-Seconds": "600" },
          })
      )
    );

    const response = await analyzeCbc({ token: "t", payload: {}, fastMode: false, timeoutMs: 1000 });
    expect(response.pollTimeoutSeconds).toBe(600);
  });
});

describe("analyzeMh", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("hits /mental-health/analyze with bearer token", async () => {
    vi.stubEnv("VITE_API_URL", "https://api.example.test");
    const fetchMock = vi.fn(async () => jsonResponse({ screening: { risk_level: "low" } }));
    vi.stubGlobal("fetch", fetchMock);

    await analyzeMh({ token: "tkn", payload: { phq9: [] }, timeoutMs: 1000 });

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("https://api.example.test/mental-health/analyze");
    expect(init.headers.Authorization).toBe("Bearer tkn");
  });
});

describe("fetchRecentAgentSessions", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("throws when the response is not ok", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("", { status: 500, statusText: "Server Error" }))
    );
    await expect(fetchRecentAgentSessions("tkn")).rejects.toThrow(/500/);
  });
});

describe("fetchCurrentUser", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("returns the parsed user on 200", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => jsonResponse({ app_role: "doctor", email: "doc@wise.test" }))
    );
    const profile = await fetchCurrentUser("tkn");
    expect(profile.app_role).toBe("doctor");
  });

  it("throws a labeled error on non-ok responses", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => jsonResponse({ detail: "no profile" }, { status: 404, statusText: "Not Found" }))
    );
    await expect(fetchCurrentUser("tkn")).rejects.toThrow(/no profile/);
  });
});
