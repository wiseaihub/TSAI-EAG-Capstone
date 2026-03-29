import { useEffect, useMemo, useState } from "react";
import { Activity, BrainCircuit, FlaskConical } from "lucide-react";
import { AccountHeader, LoginPanel } from "./features/auth/auth-gate";
import { CbcWorkflow } from "./features/cbc/cbc-workflow";
import { ModeSwitcher } from "./features/layout/mode-switcher";
import { MentalHealthWorkflow } from "./features/mental-health/mh-workflow";
import { SessionTimeline } from "./features/sessions/session-timeline";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Separator } from "./components/ui/separator";
import {
  analyzeCbc,
  analyzeMh,
  fetchHealthConfig,
  fetchRecentAgentSessions,
} from "./lib/api";
import { supabase } from "./lib/supabase";

function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [mode, setMode] = useState("doctor");
  const [pollTimeoutSeconds, setPollTimeoutSeconds] = useState(900);

  const [cbcState, setCbcState] = useState({
    loading: false,
    result: null,
    error: "",
    hint: "",
  });
  const [mhState, setMhState] = useState({
    loading: false,
    result: null,
    error: "",
    hint: "",
  });
  const [sessionsState, setSessionsState] = useState({
    loading: false,
    sessions: [],
    error: "",
  });

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
    });
    const { data: listener } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
    });
    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  useEffect(() => {
    fetchHealthConfig()
      .then((data) => {
        if (typeof data?.pollTimeoutSeconds === "number" && data.pollTimeoutSeconds >= 60) {
          setPollTimeoutSeconds(data.pollTimeoutSeconds);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!session?.access_token) return;
    refreshSessions(session.access_token);
  }, [session?.access_token]);

  const modeCopy = useMemo(() => {
    if (mode === "doctor") {
      return "Doctor view emphasizes concise risk summaries and decision-support details.";
    }
    return "Patient view uses guided language and stronger context around safety and escalation.";
  }, [mode]);

  async function login() {
    setAuthError("");
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      setAuthError(error.message);
    }
  }

  async function logout() {
    await supabase.auth.signOut();
    setCbcState({ loading: false, result: null, error: "", hint: "" });
    setMhState({ loading: false, result: null, error: "", hint: "" });
    setSessionsState({ loading: false, sessions: [], error: "" });
  }

  async function refreshSessions(token) {
    if (!token) return;
    setSessionsState((prev) => ({ ...prev, loading: true, error: "" }));
    try {
      const sessions = await fetchRecentAgentSessions(token);
      setSessionsState({ loading: false, sessions, error: "" });
    } catch (error) {
      setSessionsState((prev) => ({
        ...prev,
        loading: false,
        error: error?.message || "Failed to fetch sessions.",
      }));
    }
  }

  async function runCbc({ payload, fastMode, timeoutMs }) {
    if (!session?.access_token) {
      setCbcState({
        loading: false,
        result: null,
        error: "Please sign in before submitting CBC analysis.",
        hint: "",
      });
      return;
    }

    setCbcState({ loading: true, result: null, error: "", hint: "" });
    try {
      const response = await analyzeCbc({
        token: session.access_token,
        payload,
        fastMode,
        timeoutMs,
      });
      if (response.pollTimeoutSeconds && response.pollTimeoutSeconds >= 60) {
        setPollTimeoutSeconds(response.pollTimeoutSeconds);
      }
      if (response.ok) {
        setCbcState({ loading: false, result: response.data, error: "", hint: "" });
      } else {
        setCbcState({
          loading: false,
          result: null,
          error: String(response.data?.error || "Request failed"),
          hint: "Review backend logs if this persists.",
        });
      }
      refreshSessions(session.access_token);
    } catch (error) {
      const isTimeout = error?.name === "AbortError";
      setCbcState({
        loading: false,
        result: null,
        error: isTimeout ? "CBC request timed out." : "CBC request failed.",
        hint: isTimeout
          ? "The backend may still be processing S18. Retry or use fast mode."
          : "Check backend availability and authentication.",
      });
    }
  }

  async function runMentalHealth({ payload, timeoutMs }) {
    if (!session?.access_token) {
      setMhState({
        loading: false,
        result: null,
        error: "Please sign in before running mental health screening.",
        hint: "",
      });
      return;
    }

    setMhState({ loading: true, result: null, error: "", hint: "" });
    try {
      const response = await analyzeMh({
        token: session.access_token,
        payload,
        timeoutMs,
      });
      if (response.pollTimeoutSeconds && response.pollTimeoutSeconds >= 60) {
        setPollTimeoutSeconds(response.pollTimeoutSeconds);
      }
      if (response.ok) {
        setMhState({ loading: false, result: response.data, error: "", hint: "" });
      } else {
        setMhState({
          loading: false,
          result: null,
          error: String(response.data?.error || "Request failed"),
          hint: "Validate PHQ-9/GAD-7 inputs and retry.",
        });
      }
      refreshSessions(session.access_token);
    } catch (error) {
      const isTimeout = error?.name === "AbortError";
      setMhState({
        loading: false,
        result: null,
        error: isTimeout ? "Mental health request timed out." : "Mental health request failed.",
        hint: isTimeout
          ? "S18 narrative pass can take several minutes. Try local-only mode if needed."
          : "Check backend availability and authentication.",
      });
    }
  }

  if (!session) {
    return (
      <main className="mx-auto max-w-7xl px-5 pb-16 pt-10 md:px-8">
        <LoginPanel
          email={email}
          password={password}
          authError={authError}
          onEmailChange={setEmail}
          onPasswordChange={setPassword}
          onLogin={login}
        />
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl space-y-8 px-5 pb-16 pt-10 md:px-8">
      <header className="space-y-5">
        <div className="rounded-2xl border border-slate-700/20 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 px-7 py-7 text-white shadow-[0_18px_40px_rgba(15,23,42,0.28)] md:px-8 md:py-8">
          <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">WISE Clinical Intelligence Portal</h1>
          <p className="mt-3 max-w-3xl text-sm leading-relaxed text-slate-100/90 md:text-[15px]">
            Unified CBC and Mental Health workflows powered by local engines plus optional S18 narrative support.
          </p>
        </div>
        <AccountHeader session={session} onLogout={logout} />
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base md:text-lg">Workflow Mode</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <ModeSwitcher mode={mode} onModeChange={setMode} />
            <p className="text-sm leading-relaxed text-[var(--muted-foreground)]">{modeCopy}</p>
          </CardContent>
        </Card>
      </header>

      <Alert>
        <Activity className="h-4 w-4" />
        <AlertTitle>Operational profile</AlertTitle>
        <AlertDescription>
          S18-enabled runs are long polling workflows. Current backend poll timeout is {pollTimeoutSeconds} seconds.
        </AlertDescription>
      </Alert>

      <section className="grid gap-7 xl:grid-cols-[2fr,1fr]">
        <div className="space-y-7">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.12em] text-slate-600">
              <FlaskConical className="h-4 w-4" />
              CBC
            </div>
            <CbcWorkflow
              mode={mode}
              pollTimeoutSeconds={pollTimeoutSeconds}
              state={cbcState}
              onAnalyze={runCbc}
            />
          </div>
          <Separator />
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.12em] text-slate-600">
              <BrainCircuit className="h-4 w-4" />
              Mental Health
            </div>
            <MentalHealthWorkflow
              mode={mode}
              pollTimeoutSeconds={pollTimeoutSeconds}
              state={mhState}
              onAnalyze={runMentalHealth}
            />
          </div>
        </div>
        <div>
          <SessionTimeline
            sessions={sessionsState.sessions}
            loading={sessionsState.loading}
            error={sessionsState.error}
            onRefresh={() => refreshSessions(session.access_token)}
          />
        </div>
      </section>
    </main>
  );
}

export default App;
