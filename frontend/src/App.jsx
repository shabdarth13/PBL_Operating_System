import React, { useEffect, useRef, useState } from "react";
import "./terminal.css";

const BACKEND_URL = "http://127.0.0.1:5000/process-text";

export default function App() {
  const [listening, setListening] = useState(false);
  const [command, setCommand] = useState("");
  const [output, setOutput] = useState("");
  const [history, setHistory] = useState([]);
  const recognitionRef = useRef(null);
  const outputRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      recognitionRef.current = null;
      return;
    }
    const r = new SpeechRecognition();
    r.continuous = false;
    r.interimResults = false;
    r.lang = "en-US";
    recognitionRef.current = r;

    // cleanup on unmount
    return () => {
      try {
        r.onresult = null;
        r.onerror = null;
        r.onend = null;
        r.stop && r.stop();
      } catch {}
    };
  }, []);

  // tiny typing effect for output: appends text char by char
  const typeOutput = (text) => {
    setOutput("");
    let i = 0;
    const speed = 10; // ms per char
    const interval = setInterval(() => {
      setOutput((prev) => prev + text.charAt(i));
      i++;
      if (i >= text.length) clearInterval(interval);
      // scroll terminal while typing
      if (outputRef.current) {
        outputRef.current.scrollTop = outputRef.current.scrollHeight;
      }
    }, speed);
  };

  const startListening = () => {
    const r = recognitionRef.current;
    if (!r) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }

    setListening(true);
    setCommand("");
    setOutput("…listening");

    r.onresult = async (event) => {
      const voiceText = event.results[0][0].transcript;
      setCommand(voiceText);
      setListening(false);
      // send to backend
      await sendToBackend(voiceText);
    };

    r.onerror = (ev) => {
      setListening(false);
      setOutput("Speech recognition error.");
    };

    r.onend = () => {
      setListening(false);
    };

    try {
      r.start();
    } catch (e) {
      // some browsers throw if start called twice
      console.warn("recognition start error", e);
    }
  };

  const sendToBackend = async (text) => {
    setOutput("Processing...");
    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        const txt = await res.text();
        typeOutput(`Error ${res.status}: ${txt}`);
        addHistory(text, `Error ${res.status}`);
        return;
      }

      const data = await res.json();
      const backendOutput = data.output ?? JSON.stringify(data);
      typeOutput(backendOutput);

      addHistory(text, backendOutput);
    } catch (err) {
      typeOutput("Error connecting to backend.");
      addHistory(text, "Connection error");
    }
  };

  const addHistory = (cmd, out) => {
    const ts = new Date().toLocaleTimeString();
    setHistory((h) => [{ cmd, out, ts }, ...h].slice(0, 20));
  };

  return (
    <div className="neon-app">
      <header className="neon-header">
        <div className="logo">
          <svg viewBox="0 0 24 24" className="logo-icon" aria-hidden>
            <path d="M12 2 L15 8 L22 9 L17 14 L18 21 L12 18 L6 21 L7 14 L2 9 L9 8 Z" />
          </svg>
          <div className="title">
            VocalShell <span className="muted">— Voice Operated CLI</span>
          </div>
        </div>
        <div className="status">
          <div className={`mic-glow ${listening ? "active" : ""}`}>
            <button
              className="mic-btn"
              onClick={startListening}
              disabled={listening}
              title="Start voice command"
            >
              <svg viewBox="0 0 24 24" className="mic-icon" aria-hidden>
                <path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3z" />
                <path d="M19 11a1 1 0 0 0-2 0 5 5 0 0 1-10 0 1 1 0 0 0-2 0 7 7 0 0 0 6 6.92V21h-3a1 1 0 0 0 0 2h8a1 1 0 0 0 0-2h-3v-3.08A7 7 0 0 0 19 11z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="neon-main">
        <section className="left">
          <div className="panel recognized">
            <h3>Recognized Command</h3>
            <div className="recognized-text">{command || "Say a command..."}</div>
          </div>

          <div className="panel terminal">
            <h3>Terminal Output</h3>
            <pre className="terminal-output" ref={outputRef}>
              {output || "Waiting for command..."}
            </pre>
          </div>
        </section>

        <aside className="right">
          <div className="panel history">
            <h3>Recent Commands</h3>
            <ul>
              {history.length === 0 && <li className="hint">No commands yet</li>}
              {history.map((h, i) => (
                <li key={i}>
                  <div className="hist-cmd">{h.cmd}</div>
                  <div className="hist-meta">
                    <span className="hist-time">{h.ts}</span>
                  </div>
                  <div className="hist-out">{h.out}</div>
                </li>
              ))}
            </ul>
          </div>

          <div className="panel tips">
            <h3>Tips</h3>
            <ul>
              <li>Start by saying: "list files" or "go to desktop"</li>
              <li>Use short, clear commands for best mapping</li>
              <li>Don’t say confidential commands while testing</li>
            </ul>
          </div>
        </aside>
      </main>

      <footer className="neon-footer">
        <span>VocalShell • Offline STT with Vosk • spaCy NLP</span>
      </footer>
    </div>
  );
}
