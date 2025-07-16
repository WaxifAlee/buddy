import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)     # Speed of speech
engine.setProperty('volume', 1.0)   # Full volume

# Optional: Set voice (Windows usually has 0 = male, 1 = female)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[0].id)  # Try male voice

def speak(text: str):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error] {e}")
