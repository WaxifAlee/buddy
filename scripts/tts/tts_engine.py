import pyttsx3

def speak(text: str):
    print(f"[DEBUG] Speaking: {text}")
    try:
        # ✅ Re-initialize engine every time
        engine = pyttsx3.init(driverName='sapi5')
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id if len(voices) > 0 else '')

        engine.say(text)
        engine.runAndWait()
        print("[Buddy Is Finished Speaking]")
        engine.stop()

    except Exception as e:
        print(f"[TTS Error] {e}")
