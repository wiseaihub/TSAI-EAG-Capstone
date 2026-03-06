import { useEffect, useState } from "react";
import { supabase } from "./lib/supabase";


function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [sessionDebug, setSessionDebug] = useState(null);

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

    const token = session.access_token;
    console.log("TOKEN:", token);

    const response = await fetch("http://localhost:8000/cbc/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // 🔥 JWT sent here
      },
      body: JSON.stringify({
        hemoglobin: 7.5,
        wbc: 15000,
        rbc: 4.2,
        platelets: 120000,
      }),
    });

    const data = await response.json();
    setResult(data);
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
          <button onClick={analyze}>Run CBC Analysis</button>

          {result && (
            <pre style={{ marginTop: "20px" }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </>
      )}
    </div>
  );
}

export default App;
