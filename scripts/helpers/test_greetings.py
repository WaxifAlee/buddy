import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from greetings import generate_greeting
from scripts.tts.tts_engine import speak

greeting = generate_greeting()
speak(greeting)
