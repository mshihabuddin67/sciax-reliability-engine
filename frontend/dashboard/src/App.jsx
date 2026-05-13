import { useState } from "react";

const API_URL = "https://sciax-reliability-engine.onrender.com/analyze";
const API_KEY = "sciax-demo-key-123";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": API_KEY,
        },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "API Error" });
    }

    setLoading(false);
  };

  const getColor = (risk) => {
    if (risk === "High") return "red";
    if (risk === "Medium") return "orange";
    return "green";
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>S-CIAX Dashboard</h1>

      <textarea
        style={styles.input}
        placeholder="Enter text for analysis..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button style={styles.button} onClick={analyzeText}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div style={styles.card}>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <>
              <h2 style={{ color: getColor(result.risk_level) }}>
                Risk: {result.risk_level}
              </h2>

              <p>Stability: {result.stability_score}</p>
              <p>Conflict: {result.conflict_score}</p>

              <p style={styles.reason}>
                {result.reason}
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Arial",
    textAlign: "center",
    padding: "40px",
    backgroundColor: "#0f172a",
    minHeight: "100vh",
    color: "white",
  },
  title: {
    fontSize: "32px",
    marginBottom: "20px",
  },
  input: {
    width: "80%",
    height: "120px",
    padding: "10px",
    borderRadius: "10px",
    border: "none",
    marginBottom: "15px",
  },
  button: {
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#3b82f6",
    color: "white",
    cursor: "pointer",
    marginBottom: "20px",
  },
  card: {
    marginTop: "20px",
    padding: "20px",
    borderRadius: "12px",
    backgroundColor: "#1e293b",
    width: "80%",
    marginLeft: "auto",
    marginRight: "auto",
  },
  reason: {
    marginTop: "10px",
    fontStyle: "italic",
    color: "#cbd5e1",
  },
};
