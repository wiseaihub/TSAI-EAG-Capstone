import { useEffect, useMemo, useState } from "react";
import { Activity, BrainCircuit, FlaskConical } from "lucide-react";
import { AccountHeader, LoginPanel, PasswordRecoveryPanel } from "./features/auth/auth-gate";
import { CbcWorkflow } from "./features/cbc/cbc-workflow";
import { MentalHealthWorkflow } from "./features/mental-health/mh-workflow";
import { SessionTimeline } from "./features/sessions/session-timeline";
import { QuickSummaryCard } from "./features/shared/quick-summary-card";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Separator } from "./components/ui/separator";
import {
  analyzeCbc,
  analyzeMh,
  fetchCurrentUser,
  fetchHealthConfig,
  fetchRecentAgentSessions,
} from "./lib/api";
import { supabase } from "./lib/supabase";

const PASSWORD_RECOVERY_STORAGE_KEY = "wise_password_recovery";

function readPasswordRecoveryFlag() {
  try {
    return typeof sessionStorage !== "undefined" && sessionStorage.getItem(PASSWORD_RECOVERY_STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [recoveryPassword, setRecoveryPassword] = useState("");
  const [recoveryConfirm, setRecoveryConfirm] = useState("");
  const [passwordRecovery, setPasswordRecovery] = useState(readPasswordRecoveryFlag);
  const [authError, setAuthError] = useState("");
  const [infoMessage, setInfoMessage] = useState("");
  const [userProfile, setUserProfile] = useState(null);
  const [roleLoading, setRoleLoading] = useState(false);
  const [roleError, setRoleError] = useState("");
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
    const hash = window.location.hash.replace(/^#/, "");
    const hashParams = new URLSearchParams(hash);
    if (hashParams.get("type") === "recovery") {
      try {
        sessionStorage.setItem(PASSWORD_RECOVERY_STORAGE_KEY, "1");
      } catch {
        /* ignore */
      }
      setPasswordRecovery(true);
    }

    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      if (!data.session) {
        const h = window.location.hash.replace(/^#/, "");
        const hasRecoveryHash = new URLSearchParams(h).get("type") === "recovery";
        if (!hasRecoveryHash) {
          try {
            sessionStorage.removeItem(PASSWORD_RECOVERY_STORAGE_KEY);
          } catch {
            /* ignore */
          }
          setPasswordRecovery(false);
        }
      }
    });
    const { data: listener } = supabase.auth.onAuthStateChange((event, nextSession) => {
      if (event === "PASSWORD_RECOVERY") {
        try {
          sessionStorage.setItem(PASSWORD_RECOVERY_STORAGE_KEY, "1");
        } catch {
          /* ignore */
        }
        setPasswordRecovery(true);
      }
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
    if (!session?.access_token) {
      setUserProfile(null);
      setRoleError("");
      return;
    }
    setRoleLoading(true);
    setRoleError("");
    fetchCurrentUser(session.access_token)
      .then((profile) => {
        setUserProfile(profile || null);
      })
      .catch((error) => {
        setUserProfile(null);
        setRoleError(error?.message || "Failed to resolve account role.");
      })
      .finally(() => {
        setRoleLoading(false);
      });
  }, [session?.access_token]);

  useEffect(() => {
    if (!session?.access_token) return;
    if (userProfile?.app_role !== "doctor") return;
    refreshSessions(session.access_token);
  }, [session?.access_token, userProfile?.app_role]);

  const roleCopy = useMemo(() => {
    if (userProfile?.app_role === "doctor") {
      return "Doctor access is enabled for clinical workflows and decision-support tools.";
    }
    if (userProfile?.app_role === "patient") {
      return "Patient account detected. Clinical doctor workflows are restricted.";
    }
    return "Account role could not be determined.";
  }, [userProfile?.app_role]);

  async function login() {
    setAuthError("");
    setInfoMessage("");
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      setAuthError(error.message);
    }
  }

  async function signUp() {
    setAuthError("");
    setInfoMessage("");
    if (password !== confirmPassword) {
      setAuthError("Passwords do not match.");
      return;
    }
    if (password.length < 6) {
      setAuthError("Password must be at least 6 characters.");
      return;
    }
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/`,
      },
    });
    if (error) {
      setAuthError(error.message);
      return;
    }
    if (data.user && !data.session) {
      setInfoMessage(
        "If this email can receive confirmation, check your inbox and spam folder before signing in."
      );
    }
  }

  async function forgotPassword() {
    setAuthError("");
    setInfoMessage("");
    const trimmed = email.trim();
    if (!trimmed) {
      setAuthError("Enter your email address.");
      return;
    }
    const { error } = await supabase.auth.resetPasswordForEmail(trimmed, {
      redirectTo: `${window.location.origin}/`,
    });
    if (error) {
      setAuthError(error.message);
      return;
    }
    setInfoMessage("If an account exists for that email, you will receive a reset link shortly.");
  }

  async function completePasswordRecovery() {
    setAuthError("");
    if (recoveryPassword !== recoveryConfirm) {
      setAuthError("Passwords do not match.");
      return;
    }
    if (recoveryPassword.length < 6) {
      setAuthError("Password must be at least 6 characters.");
      return;
    }
    const { error } = await supabase.auth.updateUser({ password: recoveryPassword });
    if (error) {
      setAuthError(error.message);
      return;
    }
    try {
      sessionStorage.removeItem(PASSWORD_RECOVERY_STORAGE_KEY);
    } catch {
      /* ignore */
    }
    setPasswordRecovery(false);
    setRecoveryPassword("");
    setRecoveryConfirm("");
  }

  async function logout() {
    try {
      sessionStorage.removeItem(PASSWORD_RECOVERY_STORAGE_KEY);
    } catch {
      /* ignore */
    }
    setPasswordRecovery(false);
    await supabase.auth.signOut();
    setUserProfile(null);
    setRoleLoading(false);
    setRoleError("");
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
    if (userProfile?.app_role !== "doctor") {
      setCbcState({
        loading: false,
        result: null,
        error: "Doctor role required for CBC analysis.",
        hint: "You can view workflows, but only doctor accounts can run clinical analysis.",
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
        const forbidden = response.data?.status === 403;
        setCbcState({
          loading: false,
          result: null,
          error: forbidden ? "Doctor role required for CBC analysis." : String(response.data?.error || "Request failed"),
          hint: forbidden ? "Use a provisioned doctor account to access this workflow." : "Review backend logs if this persists.",
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
    if (userProfile?.app_role !== "doctor") {
      setMhState({
        loading: false,
        result: null,
        error: "Doctor role required for mental health screening.",
        hint: "You can view workflows, but only doctor accounts can run clinical analysis.",
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
        const forbidden = response.data?.status === 403;
        setMhState({
          loading: false,
          result: null,
          error: forbidden
            ? "Doctor role required for mental health screening."
            : String(response.data?.error || "Request failed"),
          hint: forbidden
            ? "Use a provisioned doctor account to access this workflow."
            : "Validate PHQ-9/GAD-7 inputs and retry.",
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

  if (passwordRecovery) {
    return (
      <main className="mx-auto max-w-7xl px-5 pb-16 pt-10 md:px-8">
        <PasswordRecoveryPanel
          newPassword={recoveryPassword}
          confirmPassword={recoveryConfirm}
          authError={authError}
          onNewPasswordChange={setRecoveryPassword}
          onConfirmPasswordChange={setRecoveryConfirm}
          onSubmit={completePasswordRecovery}
        />
      </main>
    );
  }

  if (!session) {
    return (
      <main className="mx-auto max-w-7xl px-5 pb-16 pt-10 md:px-8">
        <LoginPanel
          email={email}
          password={password}
          confirmPassword={confirmPassword}
          authError={authError}
          infoMessage={infoMessage}
          onEmailChange={setEmail}
          onPasswordChange={setPassword}
          onConfirmPasswordChange={setConfirmPassword}
          onLogin={login}
          onSignUp={signUp}
          onForgotPassword={forgotPassword}
          onClearMessages={() => {
            setAuthError("");
            setInfoMessage("");
          }}
        />
      </main>
    );
  }

  if (roleLoading) {
    return (
      <main className="mx-auto max-w-7xl px-5 pb-16 pt-10 md:px-8">
        <AccountHeader session={session} onLogout={logout} />
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="text-lg">Loading account access</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[var(--muted-foreground)]">Verifying your role and access policy...</p>
          </CardContent>
        </Card>
      </main>
    );
  }

  if (roleError || !userProfile?.app_role) {
    return (
      <main className="mx-auto max-w-7xl px-5 pb-16 pt-10 md:px-8">
        <AccountHeader session={session} onLogout={logout} />
        <Alert variant="destructive" className="mt-6">
          <AlertTitle>Access setup required</AlertTitle>
          <AlertDescription>{roleError || "Your account role is not provisioned yet."}</AlertDescription>
        </Alert>
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
            <CardTitle className="text-base md:text-lg">Account Role</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm font-medium">
              Signed in role: {userProfile?.app_role === "doctor" ? "Doctor" : "Patient"}
            </p>
            <p className="text-sm leading-relaxed text-[var(--muted-foreground)]">{roleCopy}</p>
          </CardContent>
        </Card>
      </header>

      <QuickSummaryCard cbcResult={cbcState.result} mhResult={mhState.result} />

      <Alert>
        <Activity className="h-4 w-4" />
        <AlertTitle>Operational profile</AlertTitle>
        <AlertDescription>
          S18-enabled runs are long polling workflows. Current backend poll timeout is {pollTimeoutSeconds} seconds.
        </AlertDescription>
      </Alert>
      {userProfile?.app_role === "patient" ? (
        <Alert variant="warning">
          <AlertTitle>Patient access mode</AlertTitle>
          <AlertDescription>
            Workflow cards are visible for review. Running CBC and mental health analysis requires a doctor account.
          </AlertDescription>
        </Alert>
      ) : null}

      <section className="grid gap-7 xl:grid-cols-[2fr,1fr]">
        <div className="space-y-7">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.12em] text-slate-600">
              <FlaskConical className="h-4 w-4" />
              CBC
            </div>
            <CbcWorkflow
              mode={userProfile?.app_role === "doctor" ? "doctor" : "patient"}
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
              mode={userProfile?.app_role === "doctor" ? "doctor" : "patient"}
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
