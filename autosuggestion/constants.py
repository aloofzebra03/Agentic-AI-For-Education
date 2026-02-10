"""Constants for autosuggestion module.

This module contains all constant values used across the autosuggestion system:
- Kannada translation cache for predefined suggestions
- Node-specific special handling mappings
- Suppression patterns for question detection
"""

from typing import Dict, Optional, List

# ─── Kannada Translation Cache ────────────────────────────────────────────
# Precomputed translations to avoid repeated Azure API calls
# These translations must stay in sync with POSITIVE_POOL, NEGATIVE_POOL, 
# and SPECIAL_HANDLING_POOL from utils.shared_utils

KANNADA_AUTOSUGGESTION_CACHE: Dict[str, str] = {
    # Positive pool translations
    "I understand, continue": "ನನಗೆ ಅರ್ಥವಾಗಿದೆ, ಮುಂದುವರಿಸಿ",
    "Yes, got it": "ಹೌದು, ಅರ್ಥವಾಯಿತು",
    "That makes sense": "ಅದು ಅರ್ಥಪೂರ್ಣವಾಗಿದೆ",
    "Let's proceed further": "ಮುಂದೆ ಮುಂದುವರಿಯೋಣ",
    "I'm following along": "ನಾನು ಅನುಸರಿಸುತ್ತಿದ್ದೇನೆ",
    
    # Negative pool translations
    "I'm not sure": "ನನಗೆ ಖಚಿತವಿಲ್ಲ",
    "I don't know": "ನನಗೆ ಗೊತ್ತಿಲ್ಲ",
    "I'm confused": "ನನಗೆ ಗೊಂದಲವಾಗಿದೆ",
    "Not very clear": "ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ",
    "Can you explain differently?": "ನೀವು ವಿಭಿನ್ನವಾಗಿ ವಿವರಿಸಬಹುದೇ?",
    
    # Special handling pool translations
    "Can you give me a hint?": "ನೀವು ನನಗೆ ಸುಳಿವು ನೀಡಬಹುದೇ?",
    "Can you explain that simpler?": "ನೀವು ಅದನ್ನು ಸರಳವಾಗಿ ವಿವರಿಸಬಹುದೇ?",
    "Give me an example": "ನನಗೆ ಉದಾಹರಣೆ ನೀಡಿ",
}

# ─── Node-Specific Special Handling ───────────────────────────────────────
# Maps each pedagogical node to its special handling autosuggestion
# "random" is a special flag indicating random selection from all options

NODE_SPECIAL_HANDLING: Dict[str, Optional[str]] = {
    "APK": "Can you give me a hint?",
    "CI": "Can you explain that simpler?",
    "GE": "random",  # Special flag: randomly select from SPECIAL_HANDLING_POOL
    "AR": "Can you give me a hint?",
    "TC": None,      # No special handling for TC node
    "RLC": None,     # No special handling for RLC node
}

# ─── Suppression Patterns ──────────────────────────────────────────────────
# Regex patterns that trigger suppression of positive autosuggestions
# When agent output matches any pattern, positive suggestion is set to None

SUPPRESSION_PATTERNS: List[str] = [
    r'\?',              # Question mark anywhere in output
    r'let\s+me\s+think' # "let me think" in any variation (case-insensitive)
]
