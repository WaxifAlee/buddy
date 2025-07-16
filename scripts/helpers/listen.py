# scripts/helpers/listen.py
import queue
import sys
import json
import time
import sounddevice as sd
import vosk

model = vosk.Model("voice/vosk-model-small-en-us-0.15")

def listen_for_command(timeout=10):
    q = queue.Queue()
    rec = vosk.KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status):
        if status:
            print("[VOSK Error]:", status, file=sys.stderr, flush=True)
        q.put(bytes(indata))

    print("[🎤 Listening for your command...]", flush=True)

    start_time = time.time()
    final_result = ""

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        while True:
            current_time = time.time()
            if (current_time - start_time) > timeout:
                print("[🎤 Timeout reached]", flush=True)
                break
            
            try:
                data = q.get(timeout=1)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:  # Only break if we actually got some text
                        final_result = text
                        break
                else:
                    # Process partial results to check for speech
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        start_time = current_time  # Reset timeout if we detect speech
                        
            except queue.Empty:
                continue

    # Get any remaining result
    if not final_result:
        final_result = json.loads(rec.FinalResult()).get("text", "").strip()

    return final_result

