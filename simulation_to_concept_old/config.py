"""
Configuration for Version 3 Teaching Agent
==========================================
Handles LLM setup, environment variables, and constants.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from simulation_to_concept.simulations_config import get_simulation, get_simulation_list
from langchain_google_genai import ChatGoogleGenerativeAI
from api_tracker_utils.tracker import track_model_call, get_next_available_api_model_pair

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
    print(f"✅ Config loaded: MaxExchanges={MAX_EXCHANGES}")
    print(f"✅ Current Simulation: {TOPIC_TITLE} ({CURRENT_SIMULATION_ID})")
    print(f"✅ LLM selection handled by api_tracker_utils (GOOGLE_API_KEY_1 ... _7)")
    return True


# ═══════════════════════════════════════════════════════════════════════
# LLM FACTORY (tracker-backed)
# ═══════════════════════════════════════════════════════════════════════

def get_llm(temperature: float = TEMPERATURE) -> ChatGoogleGenerativeAI:
    """
    Get a configured LLM instance using the api_tracker_utils tracker.

    The tracker automatically selects the optimal API key and model
    from GOOGLE_API_KEY_1 ... GOOGLE_API_KEY_7 based on rate limits
    and load balancing.

    Args:
        temperature: Sampling temperature (default from env/config).

    Returns:
        ChatGoogleGenerativeAI instance ready to call .invoke() on.

    Raises:
        MinuteLimitExhaustedError: All API-model pairs hit per-minute limit.
        DayLimitExhaustedError:    All API-model pairs hit daily limit.
    """
    selected_api_key, selected_model = get_next_available_api_model_pair()
    print(f"🔑 [get_llm] Using ...{selected_api_key[-6:]} with model: {selected_model}")

    # Track BEFORE invocation for accurate rate limiting
    track_model_call(selected_api_key, selected_model)

    return ChatGoogleGenerativeAI(
        model=selected_model,
        api_key=selected_api_key,
        temperature=temperature,
    )

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION HOSTING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# GitHub Pages base URL (set in .env for production, None for local dev)
GITHUB_PAGES_BASE_URL = os.getenv("GITHUB_PAGES_BASE_URL", "https://imhv0609.github.io/simulation_to_concept_version3_github")

def get_simulation_base_url(simulation_id: str = None) -> str:
    """
    Get the base URL for simulations based on environment.
    
    Args:
        simulation_id: Which simulation to get URL for. If None, uses CURRENT_SIMULATION_ID.
    
    Returns GitHub Pages URL if GITHUB_PAGES_BASE_URL is set,
    otherwise returns relative path for local development.
    """
    # Dynamically get the simulation file based on simulation_id
    if simulation_id:
        sim_config = get_simulation(simulation_id)
        sim_file = sim_config["file"] if sim_config else SIMULATION_FILE
    else:
        sim_file = SIMULATION_FILE
    
    if GITHUB_PAGES_BASE_URL:
        # Production: Use GitHub Pages with full path
        return f"{GITHUB_PAGES_BASE_URL.rstrip('/')}/{sim_file}"
    else:
        # Local development: Use relative path
        return sim_file

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION URL BUILDING
# ═══════════════════════════════════════════════════════════════════════

def build_simulation_url(params: dict, autostart: bool = True, base_url: str = None, simulation_id: str = None) -> str:
    """
    Build simulation URL with parameters dynamically.
    
    Args:
        params: Dictionary of parameters to pass to simulation
        autostart: Whether to auto-start the simulation
        base_url: Optional base URL override (for custom hosting)
        simulation_id: Which simulation to build URL for (required for correct URL)
    
    Returns:
        Complete URL with query parameters
    """
    # Use provided base_url, or get dynamically based on simulation_id
    if base_url is None:
        base_url = get_simulation_base_url(simulation_id)
    
    # Get parameter info for this specific simulation (for URL key mapping)
    if simulation_id:
        sim_config = get_simulation(simulation_id)
        param_info = sim_config.get("parameter_info", {}) if sim_config else PARAMETER_INFO
    else:
        param_info = PARAMETER_INFO
    
    # Build query string from parameters
    query_params = []
    for param_name, param_value in params.items():
        # Get the URL key from parameter info
        info = param_info.get(param_name, {})
        url_key = info.get("url_key", param_name)
        query_params.append(f"{url_key}={param_value}")
    
    # Add autostart if requested
    if autostart:
        query_params.append("autoStart=true")
    
    # Construct final URL
    url = f"{base_url}?{'&'.join(query_params)}"
    print("base url:", base_url)
    print("params:", query_params)
    print(f"🔗 Built simulation URL: {url}")
    return url

# Legacy variable for backward compatibility
SIMULATION_BASE_URL = get_simulation_base_url()
