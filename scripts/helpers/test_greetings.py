from greetings import generate_greeting
from tts.tts_engine import speak

greeting = generate_greeting()
print("[DEBUG] Greeting:", greeting)
speak(greeting)
