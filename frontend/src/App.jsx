import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000/translate";

const LEVELS = [
  { id: "beginner", label: "Beginner" },
  { id: "intermediate", label: "Intermediate" },
];

function App() {
  const [text, setText] = useState("");
  const [level, setLevel] = useState("beginner");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="watermark" aria-hidden="true">अ</div>

      <header className="hero">
        <p className="wordmark">
          नेपाली<span>Tech</span>
        </p>
        <h1>Say it in Nepali. Understand it too.</h1>
        <p className="lede">
          Paste a technical sentence in English. Get a Nepali translation
          and a plain-language explanation beside it.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="form">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
          placeholder="A neural network is a computational model inspired by the human brain."
        />

        <div className="form-row">
          <div className="segmented" role="group" aria-label="Explanation level">
            {LEVELS.map(({ id, label }) => (
              <button
                key={id}
                type="button"
                className={level === id ? "active" : ""}
                aria-pressed={level === id}
                onClick={() => setLevel(id)}
              >
                {label}
              </button>
            ))}
          </div>

          <button
            type="submit"
            className="submit"
            disabled={loading || !text.trim()}
          >
            {loading ? "Translating" : "Translate & Simplify"}
          </button>
        </div>
      </form>

      {error && (
        <p className="error">
          Something went wrong. Check that the backend is running, then try
          again.
        </p>
      )}

      {loading && (
        <div className="skeleton" aria-hidden="true">
          <div className="skeleton-line long" />
          <div className="skeleton-line" />
          <div className="skeleton-line short" />
        </div>
      )}

      {result && !loading && (
        <div className="results">
          <p className="detected">
            Detected input: {result.detected_language === "nepali" ? "Nepali" : "English"}
          </p>

          <section className="translation">
            <h2>
              {result.detected_language === "nepali"
                ? "English translation"
                : "Nepali translation"}
            </h2>
            <blockquote
              lang={result.detected_language === "nepali" ? "en" : "ne"}
            >
              {result.translation}
            </blockquote>
          </section>

          <section className="explanation">
            <h2>In plain words</h2>
            <p>{result.simple_explanation_ne}</p>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;