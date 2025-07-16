# scripts/wake_listener.py
import queue
import sounddevice as sd
import vosk
import sys
import json
import time

from gemini.gemini_client import ask_gemini
from tts.tts_engine import speak
from helpers.sanatize_response import sanitize_response
from helpers.greetings import generate_greeting
from helpers.listen import listen_for_command

model = vosk.Model("voice/vosk-model-small-en-us-0.15")

def passive_listen():
    q = queue.Queue()
    rec = vosk.KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status):
        if status:
            print("[Passive Error]:", status, file=sys.stderr)
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        print('\n🎧 [Buddy is listening for "Buddy"...]\n')
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "buddy" in result.get("text", "").lower():
                    # Clear the queue to prevent audio contamination
                    while not q.empty():
                        try:
                            q.get_nowait()
                        except queue.Empty:
                            break
                    # Also reset the recognizer to clear any internal state
                    rec = vosk.KaldiRecognizer(model, 16000)
                    return True

# Main loop
while True:
    try:
        if passive_listen():
            print("\n[Buddy Activated, Mr. Wasif!]")
            
            # Add a small delay to ensure proper cleanup
            time.sleep(0.5)
            
            greeting = generate_greeting()
            speak(greeting)

            user_input = listen_for_command(timeout=10)
            print(f"🗣️ You: {user_input}")
            
            if user_input.strip():  # Only proceed if we got actual input
                print("🤖 Thinking...")

                response = ask_gemini(user_input)

                if response:
                    safe_response = sanitize_response(response)
                    print(f"[SPEAKING]: {safe_response}")
                    speak(safe_response)
                else:
                    speak("Sorry my brain is not working right now.")
            else:
                print("🤖 No command detected, going back to listening...")
                
    except Exception as e:
        print(f"[System Error] {e}")
        time.sleep(1)  # Brief pause before retrying
