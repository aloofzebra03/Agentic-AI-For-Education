import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = ".env", override=True)

AVAILABLE_MODELS = [
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
]

# Default model
DEFAULT_MODEL = "gemma-4-31b-it"

# Rate limits per model (requests per minute and per day)
# RATE_LIMITS = {
#     "gemini-2.5-flash": {
#         "per_minute": 5,
#         "per_day": 20
#     },
#     "gemini-2.5-flash-lite": {
#         "per_minute": 10,
#         "per_day": 20
#     },  
#     "gemma-3-27b-it": {
#         "per_minute": 30,
#         "per_day": 14400
#     }
# }

RATE_LIMITS = {
    "gemini-2.5-flash": {
        "per_minute": 5,
        "per_day": 20
    },
    "gemini-2.5-flash-lite": {
        "per_minute": 10,
        "per_day": 20
    },  
    "gemma-4-26b-a4b-it": {
        "per_minute": 15,
        "per_day": 1500
    },
    "gemma-4-31b-it": {
        "per_minute": 15,
        "per_day": 1500
    },
    "gemini-3.1-flash-lite": {
        "per_minute": 15,
        "per_day": 500
    },

}


# API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
