import queue
import sounddevice as sd
import vosk
import sys
import json

from gemini.gemini_client import ask_gemini
from tts.tts_engine import speak
from helpers import sanitize_response

model = vosk.Model("voice/vosk-model-small-en-us-0.15")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback,
):
    print('\n🎧 [Buddy is listening for "Buddy"...]\n')

    rec = vosk.KaldiRecognizer(model, 16000)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "buddy" in result.get("text", "").lower():
                print("\n[Buddy Activated, Mr. Wasif!]")
                speak("How can I help you Mr. Wasif?")

                try:
                    user_input = input("🗣️ You: ")
                    print("🤖 Thinking...")
                    response = ask_gemini(user_input)

                    print(f"\nBuddy: {response}\n")
                    if response:
                        safe_response = sanitize_response(response)
                        print(f"[SPEAKING]: {safe_response}")
                        speak(safe_response)
                    else:
                        speak("Sorry my brain is not working right now.")

                except Exception as e:
                    print(f"[Error] {e}")
