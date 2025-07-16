import os
import sys

# Add buddy/ to sys.path manually
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from gemini.gemini_client import ask_gemini

reply = ask_gemini("How are you feeling today, Buddy?")
print("Gemini says:", reply)
