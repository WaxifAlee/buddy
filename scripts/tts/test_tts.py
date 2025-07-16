import os
import sys

# Dynamically add root dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from scripts.tts.tts_engine import speak

speak("Hello Mr. Wasif. I am now able to speak. Let’s take over the world.")
