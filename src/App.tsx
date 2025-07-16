import { useEffect, useState } from "react";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api/core";

function App() {
  const [status, setStatus] = useState("Initializing...");
  const [userInput, setUserInput] = useState("");
  const [buddyResponse, setBuddyResponse] = useState("");
  const [errors, setErrors] = useState("");
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const setupListeners = async () => {
      const unlistenStatus = await listen("buddy-status", (event) => {
        const payload = event.payload as any;
        console.log("Status event received:", payload);
        setStatus(`${payload.status}: ${payload.message}`);
        setIsConnected(true);
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
      });

      const unlistenBuddyError = await listen("buddy-error", (event) => {
        const payload = event.payload as any;
        console.log("Buddy error event received:", payload);
        setErrors(payload.error);
      });

      const unlistenPythonOutput = await listen("python-output", (event) => {
        console.log("[Python Output]", event.payload);
      });

      const unlistenPythonError = await listen("python-error", (event) => {
        console.error("[Python Error]", event.payload);
      });

      // Return cleanup function
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

  const testEvents = () => {
    console.log("Testing events...");
    // Simulate the events that should be coming from Python
    setStatus("testing: Manual test initiated");
    setTimeout(() => setUserInput("Hello Buddy"), 1000);
    setTimeout(() => setBuddyResponse("Hello! How can I help you?"), 2000);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>🧠 Buddy AI</h1>
      <p>
        <strong>Connection:</strong>{" "}
        <span style={{ color: isConnected ? "green" : "red" }}>
          {isConnected ? "Connected" : "Disconnected"}
        </span>
      </p>
      <p>
        <strong>Status:</strong> {status}
      </p>
      <p>
        <strong>You said:</strong> {userInput}
      </p>
      <p>
        <strong>Buddy replied:</strong> {buddyResponse}
      </p>
      {errors && (
        <p style={{ color: "red" }}>
          <strong>Error:</strong> {errors}
        </p>
      )}
      <button
        onClick={testEvents}
        style={{ margin: "10px", padding: "10px 20px" }}
      >
        Test Events
      </button>
    </div>
  );
}

export default App;
