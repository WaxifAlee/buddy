import queue
import sounddevice as sd
import vosk
import sys
import json

model = vosk.Model("../voice/vosk-model-small-en-us-0.15")
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
    print('\n[🎧 Listening for wake word "Buddy"...]\n')

    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "buddy" in result.get("text", "").lower():
                print("\n[🎙️ Buddy Activated, Mr. Wasif!]\n")
                # Future: Trigger Tauri event or Gemini call
