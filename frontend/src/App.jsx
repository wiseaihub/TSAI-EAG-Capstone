import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

// 🔹 Replace with your values
const supabaseUrl = "https://lfjihuzcshjpggtdrtne.supabase.co";
const supabaseAnonKey = "sb_publishable_VdhxbJsy2M4EZrHF77DQ8g_65HTEosc";

const supabase = createClient(supabaseUrl, supabaseAnonKey);
const debugSession = async () => {
  const { data } = await supabase.auth.getSession();
  console.log("SESSION:", data);
};

<button onClick={debugSession}>Debug Session</button>


function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);

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
