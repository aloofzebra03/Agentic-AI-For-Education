import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = ".env", override=True)

AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemma-3-27b-it",
]

# Default model
DEFAULT_MODEL = "gemma-3-27b-it"

# Rate limits per model (requests per minute and per day)
RATE_LIMITS = {
    "gemini-2.5-flash": {
        "per_minute": 300,
        "per_day": 2
    },
    "gemini-2.5-flash-lite": {
        "per_minute": 300,
        "per_day": 2
    },  
    "gemma-3-27b-it": {
        "per_minute": 300,
        "per_day": 2
    }
}

# API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
