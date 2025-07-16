import os
import sys

from gemini_client import ask_gemini  # ✅ Import directly from file in same folder

reply = ask_gemini("How are you feeling today, Buddy?")
print("Gemini says:", reply)
