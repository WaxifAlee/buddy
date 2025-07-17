import { useEffect, useState } from "react";
import { listen } from "@tauri-apps/api/event";

import "./App.css"; // Create this for styling

function App() {
  const [status, setStatus] = useState("Initializing...");
  const [userInput, setUserInput] = useState("");
  const [buddyResponse, setBuddyResponse] = useState("");
  const [errors, setErrors] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [isListening, setIsListening] = useState(false);

  useEffect(() => {
    const setupListeners = async () => {
      const unlistenStatus = await listen("buddy-status", (event) => {
        const payload = event.payload as any;
        console.log("Status event received:", payload);
        setStatus(payload.message || "");
        setIsConnected(true);
        setIsThinking(payload.status === "thinking");
        setIsListening(payload.status === "listening");
      });

      const unlistenUserInput = await listen("user-input", (event) => {
        const payload = event.payload as any;
        console.log("User input event received:", payload);
        setUserInput(payload.input);
      });

      const unlistenBuddyResponse = await listen("buddy-response", (event) => {
        const payload = event.payload as any;
        console.log("Buddy response event received:", payload);
        setBuddyResponse(payload.response);
        setIsThinking(false);
      });

      const unlistenBuddyError = await listen("buddy-error", (event) => {
        const payload = event.payload as any;
        console.log("Buddy error event received:", payload);
        setErrors(payload.error);
        setIsThinking(false);
      });

      const unlistenPythonOutput = await listen("python-output", (event) => {
        console.log("[Python Output]", event.payload);
      });

      const unlistenPythonError = await listen("python-error", (event) => {
        console.error("[Python Error]", event.payload);
      });

      return () => {
        unlistenStatus();
        unlistenUserInput();
        unlistenBuddyResponse();
        unlistenBuddyError();
        unlistenPythonOutput();
        unlistenPythonError();
      };
    };

    setupListeners();
  }, []);

  return (
    <div className="app">
      <div className="glass-container">
        <h1 className="logo">🧠 Buddy AI</h1>
        <p>
          <strong>Connection:</strong>{" "}
          <span
            className={isConnected ? "status-connected" : "status-disconnected"}
          >
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </p>

        <p>
          <strong>Status:</strong> {status}
        </p>

        {isListening && (
          <div className="waveform">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}

        <p>
          <strong>You said:</strong> {userInput}
        </p>

        <p>
          <strong>Buddy replied:</strong>{" "}
          {isThinking ? (
            <span className="dots">
              <span>.</span>
              <span>.</span>
              <span>.</span>
            </span>
          ) : (
            buddyResponse
          )}
        </p>

        {errors && (
          <p className="error">
            <strong>Error:</strong> {errors}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
