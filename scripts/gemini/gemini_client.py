import requests

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "[Gemini Error] API key missing."

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=10
        )
        response.raise_for_status()

        candidates = response.json().get("candidates", [])
        if not candidates:
            return "[Gemini Error] No candidates returned."

        return candidates[0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        return f"[Gemini Request Failed] {str(e)}"
    except Exception as e:
        return f"[Gemini Unknown Error] {str(e)}"
