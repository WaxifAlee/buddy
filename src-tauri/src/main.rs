#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::{Command, Stdio};
use std::io::{BufRead, BufReader};
use tauri::Emitter;
use serde_json::json;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            use std::env;

            let app_handle = app.handle().clone();

            // Get the current directory and find the project root
            let current_dir = env::current_dir().expect("Failed to get current directory");
            println!("Current directory: {:?}", current_dir);
            
            // Find the project root directory (the one containing scripts/ and voice/)
            let project_root = if current_dir.join("scripts").exists() {
                // We're already in the project root
                current_dir.clone()
            } else if current_dir.join("..").join("scripts").exists() {
                // We're in src-tauri, go up one level
                current_dir.join("..").canonicalize()
                    .expect("Failed to canonicalize parent directory")
            } else if current_dir.join("..").join("..").join("scripts").exists() {
                // We're in src-tauri/src, go up two levels
                current_dir.join("..").join("..").canonicalize()
                    .expect("Failed to canonicalize parent directory")
            } else {
                panic!("Could not find project root directory with scripts/ folder");
            };

            println!("Project root: {:?}", project_root);

            // Test event emission
            println!("About to emit startup event");
            let _ = app_handle.emit("buddy-status", json!({
                "status": "starting",
                "message": "Buddy is starting up..."
            }));
            println!("Emitted startup event");

            // Also emit a simple test event
            let _ = app_handle.emit("python-output", json!({
                "output": "Test: Rust backend is running"
            }));
            println!("Emitted test event");

            // Construct the script path
            let script_path = project_root.join("scripts").join("wake_listener.py");
            
            if !script_path.exists() {
                panic!("wake_listener.py not found at: {:?}", script_path);
            }

            println!("Using script path: {:?}", script_path);

            // Verify that the voice model directory exists
            let voice_model_path = project_root.join("voice").join("vosk-model-small-en-us-0.15");
            if !voice_model_path.exists() {
                panic!("Voice model not found at: {:?}", voice_model_path);
            }

            println!("Voice model found at: {:?}", voice_model_path);

            // Clone the app handle for event emission
            let app_handle = app.handle().clone();

            tauri::async_runtime::spawn(async move {
                // Emit test events to verify event system works
                println!("Starting event emission test...");
                
                let _ = app_handle.emit("buddy-status", json!({
                    "status": "testing",
                    "message": "Event system test in progress..."
                }));
                
                // Wait 2 seconds
                std::thread::sleep(std::time::Duration::from_secs(2));
                
                let _ = app_handle.emit("user-input", json!({
                    "input": "Test user input"
                }));
                
                // Wait 1 second
                std::thread::sleep(std::time::Duration::from_secs(1));
                
                let _ = app_handle.emit("buddy-response", json!({
                    "response": "Test buddy response"
                }));
                
                println!("Event emission test completed");
                
                // Now try to run the Python script
                let python_commands = ["python", "python3", "py"];
                let mut child = None;
                
                for py_cmd in &python_commands {
                    match Command::new(py_cmd)
                        .arg(&script_path)
                        .current_dir(&project_root)
                        .stdout(Stdio::piped())
                        .stderr(Stdio::piped())
                        .spawn()
                    {
                        Ok(process) => {
                            println!("Successfully started Python script with: {}", py_cmd);
                            child = Some(process);
                            break;
                        }
                        Err(e) => {
                            println!("Failed to start with {}: {}", py_cmd, e);
                        }
                    }
                }

                if let Some(mut child) = child {
                    // Handle stdout
                    if let Some(stdout) = child.stdout.take() {
                        let reader = BufReader::new(stdout);
                        let app_handle_clone = app_handle.clone();
                        
                        tauri::async_runtime::spawn(async move {
                            for line in reader.lines() {
                                if let Ok(line) = line {
                                    println!("[PYTHON]: {}", line);
                                    
                                    // Emit different events based on the content
                                    if line.contains("🎧 [Buddy is listening for \"Buddy\"...]") {
                                        println!("Emitting buddy-status: listening");
                                        let _ = app_handle_clone.emit("buddy-status", json!({
                                            "status": "listening",
                                            "message": "Buddy is listening for wake word..."
                                        }));
                                    } else if line.contains("[Buddy Activated, Mr. Wasif!]") {
                                        println!("Emitting buddy-status: activated");
                                        let _ = app_handle_clone.emit("buddy-status", json!({
                                            "status": "activated",
                                            "message": "Buddy has been activated!"
                                        }));
                                    } else if line.contains("🗣️ You:") {
                                        let user_input = line.replace("🗣️ You: ", "");
                                        println!("Emitting user-input: {}", user_input);
                                        let _ = app_handle_clone.emit("user-input", json!({
                                            "input": user_input
                                        }));
                                    } else if line.contains("🤖 Thinking...") {
                                        println!("Emitting buddy-status: thinking");
                                        let _ = app_handle_clone.emit("buddy-status", json!({
                                            "status": "thinking",
                                            "message": "Buddy is thinking..."
                                        }));
                                    } else if line.contains("[SPEAKING]:") {
                                        let response = line.replace("[SPEAKING]: ", "");
                                        println!("Emitting buddy-response: {}", response);
                                        let _ = app_handle_clone.emit("buddy-response", json!({
                                            "response": response
                                        }));
                                    } else if line.contains("[System Error]") {
                                        println!("Emitting buddy-error: {}", line);
                                        let _ = app_handle_clone.emit("buddy-error", json!({
                                            "error": line
                                        }));
                                    }
                                    
                                    // Emit raw output for debugging
                                    let _ = app_handle_clone.emit("python-output", json!({
                                        "output": line
                                    }));
                                }
                            }
                        });
                    }

                    // Handle stderr
                    if let Some(stderr) = child.stderr.take() {
                        let reader = BufReader::new(stderr);
                        
                        tauri::async_runtime::spawn(async move {
                            for line in reader.lines() {
                                if let Ok(line) = line {
                                    println!("[PYTHON ERROR]: {}", line);
                                    let _ = app_handle.emit("python-error", json!({
                                        "error": line
                                    }));
                                }
                            }
                        });
                    }

                    // Wait for the process to complete
                    let _ = child.wait();
                } else {
                    println!("Failed to start Python script with any command!");
                    let _ = app_handle.emit("buddy-error", json!({
                        "error": "Failed to start Python script. Please ensure Python is installed."
                    }));
                }
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
