import { useEffect, useState } from "react";
import { supabase } from "./lib/supabase";


function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [sessionDebug, setSessionDebug] = useState(null);
  const [agentSessions, setAgentSessions] = useState(null);

  // CBC input values (defaults from schema examples)
  const [hemoglobin, setHemoglobin] = useState(13.5);
  const [wbc, setWbc] = useState(7000);
  const [rbc, setRbc] = useState(4.5);
  const [platelets, setPlatelets] = useState(250000);
  const [fastMode, setFastMode] = useState(true); // Fast WISE mode (single-agent in S18)
  const [pollTimeoutSeconds, setPollTimeoutSeconds] = useState(300); // min 300s for /analyze so long runs aren't cut off

  // 🔥 Check session on load
  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
    });

    const { data: listener } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
      }
    );

    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  // Fetch backend health to get poll_timeout_seconds (used for /analyze fetch timeout)
  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
    fetch(`${apiBase}/health`)
      .then((r) => r.json())
      .then((data) => {
        const sec = data?.poll_timeout_seconds;
        if (typeof sec === "number" && sec >= 300) setPollTimeoutSeconds(sec);
      })
      .catch(() => {});
  }, []);

  // 🔐 Login
  const login = async () => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      alert(error.message);
    }
  };

  // 🚪 Logout
  const logout = async () => {
    await supabase.auth.signOut();
  };

  const debugSession = async () => {
    const { data, error } = await supabase.auth.getSession();
    if (error) {
      setSessionDebug({ error: error.message });
      return;
    }
    setSessionDebug(data);
  };

  // 🧪 Call Backend Analyze
  const analyze = async () => {
    if (!session) {
      alert("Please login first");
      return;
    }

    setAnalyzing(true);
    setResult(null);
    const token = session.access_token;
    const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";

    const controller = new AbortController();
    let timeoutId;
    // Fast mode still runs WISE (single-agent), so avoid short abort windows.
    // Keep full mode at poll timeout floor; fast mode uses a shorter but safe floor.
    const timeoutMs = fastMode
      ? Math.max(120000, Math.floor((pollTimeoutSeconds * 1000) / 2))
      : Math.max(300000, pollTimeoutSeconds * 1000);
    try {
      timeoutId = setTimeout(() => controller.abort(), timeoutMs);
      const response = await fetch(`${apiBase}/analyze?fast=${fastMode}`, {
        method: "POST",
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          hemoglobin: parseFloat(hemoglobin) || 0,
          wbc: parseFloat(wbc) || 0,
          rbc: parseFloat(rbc) || 0,
          platelets: parseFloat(platelets) || 0,
        }),
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: response.statusText }));
        const detail = err?.detail;
        setResult({
          error: typeof detail === "object" ? detail?.error || response.status : detail || response.status,
          status: response.status,
          ...(typeof detail === "object" && { traceback: detail?.traceback, type: detail?.type }),
        });
      } else {
        const data = await response.json();
        setResult(data);
      }
      fetchAgentSessions();
    } catch (e) {
      if (timeoutId) clearTimeout(timeoutId);
      const isTimeout = e?.name === "AbortError";
      setResult({
        error: isTimeout ? "Request timed out" : "Request failed",
        message: e?.message || String(e),
        hint: isTimeout
          ? "Backend took too long. Try again or check S18/WISE service."
          : "Check that the backend is running on port 8000.",
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const fetchAgentSessions = async () => {
    if (!session) return;
    const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
    try {
      const r = await fetch(`${apiBase}/agent-sessions`, {
        headers: { Authorization: `Bearer ${session.access_token}` },
      });
      if (r.ok) setAgentSessions(await r.json());
    } catch (e) {
      setAgentSessions({ error: String(e) });
    }
  };

  // 🖥 UI
  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>WISE AI</h1>

      {!session ? (
        <>
          <h3>Login</h3>
          <input
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />
          <br /><br />
          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <br /><br />
          <button onClick={login}>Login</button>
        </>
      ) : (
        <>
          <p>Logged in as: {session.user.email}</p>
          <button onClick={logout}>Logout</button>
          <button onClick={debugSession} style={{ marginLeft: "12px" }}>
            Debug Session
          </button>

          {sessionDebug && (
            <pre style={{ marginTop: "12px" }}>
              {JSON.stringify(sessionDebug, null, 2)}
            </pre>
          )}

          <hr />

          <h3>CBC Analyze</h3>
          <div style={{ marginBottom: "16px" }}>
            <label style={{ display: "block", marginBottom: "8px" }}>
              Hemoglobin (g/dL):{" "}
              <input
                type="number"
                step="0.1"
                value={hemoglobin}
                onChange={(e) => setHemoglobin(e.target.value)}
                style={{ width: "100px", marginLeft: "8px" }}
              />
            </label>
            <label style={{ display: "block", marginBottom: "8px" }}>
              WBC (per µL):{" "}
              <input
                type="number"
                step="100"
                value={wbc}
                onChange={(e) => setWbc(e.target.value)}
                style={{ width: "120px", marginLeft: "8px" }}
              />
            </label>
            <label style={{ display: "block", marginBottom: "8px" }}>
              RBC (million/µL):{" "}
              <input
                type="number"
                step="0.1"
                value={rbc}
                onChange={(e) => setRbc(e.target.value)}
                style={{ width: "100px", marginLeft: "8px" }}
              />
            </label>
            <label style={{ display: "block", marginBottom: "8px" }}>
              Platelets (per µL):{" "}
              <input
                type="number"
                step="1000"
                value={platelets}
                onChange={(e) => setPlatelets(e.target.value)}
                style={{ width: "120px", marginLeft: "8px" }}
              />
            </label>
            <label style={{ display: "block", marginTop: "12px" }}>
              <input
                type="checkbox"
                checked={fastMode}
                onChange={(e) => setFastMode(e.target.checked)}
              />
              {" "}Fast mode (single-agent WISE flow) — quicker results
            </label>
          </div>
          <button onClick={analyze} disabled={analyzing}>
            {analyzing ? "Analyzing..." : "Run CBC Analysis"}
          </button>
          {analyzing && (
            <p style={{ marginTop: "8px", color: "#666", fontSize: "14px" }}>
              {fastMode
                ? "Fast WISE mode usually completes quicker, but may take up to ~2 minutes."
                : "Full WISE analysis may take 1–3 minutes. Please do not refresh."}
            </p>
          )}

          {result && (
            <div style={{ marginTop: "20px" }}>
              <pre style={{ marginBottom: "16px" }}>
                {JSON.stringify(result, null, 2)}
              </pre>
              {result.wise != null && (
                <div style={{ marginTop: "12px", padding: "12px", background: "#f5f5f5", borderRadius: "8px" }}>
                  <strong>WISE flags</strong>{" "}
                  {Array.isArray(result.wise.flags) && result.wise.flags.length > 0 ? (
                    <ul style={{ margin: "8px 0 0 0", paddingLeft: "20px" }}>
                      {result.wise.flags.map((f, i) => (
                        <li key={i}>{String(f)}</li>
                      ))}
                    </ul>
                  ) : (
                    <span style={{ color: "#666" }}>
                      {Array.isArray(result.wise.flags) ? "(none)" : `(${typeof result.wise.flags})`}
                    </span>
                  )}
                </div>
              )}
            </div>
          )}

          <h3 style={{ marginTop: "24px" }}>Recent agent sessions (DB)</h3>
          <button onClick={fetchAgentSessions}>Refresh sessions</button>
          {agentSessions != null && (
            <pre style={{ marginTop: "12px", fontSize: "12px" }}>
              {typeof agentSessions === "object" && !agentSessions.error
                ? JSON.stringify(agentSessions, null, 2)
                : String(agentSessions)}
            </pre>
          )}
        </>
      )}
    </div>
  );
}

export default App;
