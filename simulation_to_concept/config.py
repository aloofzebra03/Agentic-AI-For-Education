"""
Configuration for Version 3 Teaching Agent
==========================================
Handles LLM setup, environment variables, and constants.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from simulation_to_concept.simulations_config import get_simulation, get_simulation_list

# Load environment variables
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

# ═══════════════════════════════════════════════════════════════════════
# LLM CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemma-3-27b-it")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# ═══════════════════════════════════════════════════════════════════════
# TEACHING AGENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# Guardrails
MAX_EXCHANGES = int(os.getenv("MAX_EXCHANGES", "6"))      # Absolute ceiling per concept
SCAFFOLD_TRIGGER = int(os.getenv("SCAFFOLD_TRIGGER", "3"))  # Break down after this many tries

# Understanding Levels
UNDERSTANDING_LEVELS = ["none", "partial", "mostly", "complete"]

# Teacher Modes
TEACHER_MODES = ["encouraging", "challenging", "simplifying"]

# Teaching Strategies
STRATEGIES = [
    "continue",         # Keep current approach
    "try_different",    # Change explanation style
    "scaffold",         # Break into sub-concepts
    "give_hint",        # More direct guidance
    "summarize_advance" # Wrap up and move on
]

# ═══════════════════════════════════════════════════════════════════════
# CURRENT SIMULATION SELECTION
# ═══════════════════════════════════════════════════════════════════════

# Select which simulation to use (can be changed at runtime)
CURRENT_SIMULATION_ID = os.getenv("SIMULATION_ID", "simple_pendulum")

# Load current simulation configuration dynamically
_current_sim = get_simulation(CURRENT_SIMULATION_ID)

if not _current_sim:
    raise ValueError(f"Simulation '{CURRENT_SIMULATION_ID}' not found in simulations_config.py")

# Export simulation-specific variables for backward compatibility
TOPIC_TITLE = _current_sim["title"]
TOPIC_DESCRIPTION = _current_sim["description"]
CANNOT_DEMONSTRATE = _current_sim["cannot_demonstrate"]
INITIAL_PARAMS = _current_sim["initial_params"]
PARAMETER_INFO = _current_sim["parameter_info"]
PRE_DEFINED_CONCEPTS = _current_sim["concepts"]
SIMULATION_FILE = _current_sim["file"]

# ═══════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate that required configuration is present."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in .env file")
    print(f"✅ Config loaded: Model={GEMINI_MODEL}, MaxExchanges={MAX_EXCHANGES}")
    print(f"✅ Current Simulation: {TOPIC_TITLE} ({CURRENT_SIMULATION_ID})")
    return True

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION HOSTING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# GitHub Pages base URL (set in .env for production, None for local dev)
GITHUB_PAGES_BASE_URL = os.getenv("GITHUB_PAGES_BASE_URL", None)

def get_simulation_base_url() -> str:
    """
    Get the base URL for simulations based on environment.
    
    Returns GitHub Pages URL if GITHUB_PAGES_BASE_URL is set,
    otherwise returns relative path for local development.
    """
    if GITHUB_PAGES_BASE_URL:
        # Production: Use GitHub Pages
        return f"{GITHUB_PAGES_BASE_URL}/{SIMULATION_FILE}"
    else:
        # Local development: Use relative path
        return SIMULATION_FILE

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION URL BUILDING
# ═══════════════════════════════════════════════════════════════════════

def build_simulation_url(params: dict, autostart: bool = True, base_url: str = None) -> str:
    """
    Build simulation URL with parameters dynamically.
    
    Args:
        params: Dictionary of parameters to pass to simulation
        autostart: Whether to auto-start the simulation
        base_url: Optional base URL override (for custom hosting)
    
    Returns:
        Complete URL with query parameters
    """
    # Use provided base_url, or get from environment, or use relative path
    if base_url is None:
        base_url = get_simulation_base_url()
    
    # Build query string from parameters
    query_params = []
    for param_name, param_value in params.items():
        # Get the URL key from PARAMETER_INFO
        param_info = PARAMETER_INFO.get(param_name, {})
        url_key = param_info.get("url_key", param_name)
        query_params.append(f"{url_key}={param_value}")
    
    # Add autostart if requested
    if autostart:
        query_params.append("autoStart=true")
    
    # Construct final URL
    url = f"{base_url}?{'&'.join(query_params)}"
    return url

# Legacy variable for backward compatibility
SIMULATION_BASE_URL = get_simulation_base_url()
