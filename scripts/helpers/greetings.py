import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Hello"

def generate_greeting():
    name = os.getenv("USER_NAME", "Sir")
    greeting = get_time_of_day()
    return f"{greeting}, Mr. {name}. I hope you're having a wonderful day. How can I assist you?"
