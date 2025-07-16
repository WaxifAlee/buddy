import re

def sanitize_response(text: str) -> str:
    # Remove markdown (**, *, bullets, etc.)
    text = re.sub(r"[*_`>#\-]", "", text)
    # Remove numbered lists like "1. " or "2) "
    text = re.sub(r"\d+[\.\)]\s*", "", text)
    # Collapse newlines
    text = text.replace("\n", " ").strip()
    return text[:500]  # limit to 500 chars to be safe
