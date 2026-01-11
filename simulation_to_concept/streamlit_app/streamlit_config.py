"""
Streamlit App Configuration
===========================
Centralized configuration for simulations and app settings.
Easy to add new simulations here.
"""

# =============================================================================
# GITHUB PAGES BASE URL
# =============================================================================
GITHUB_PAGES_BASE = "https://imhv0609.github.io/simulation_to_concept_version3_github/simulations"

# =============================================================================
# SIMULATION CONFIGURATIONS
# =============================================================================
# Each simulation has:
# - name: Display name
# - base_url: GitHub Pages URL
# - parameters: List of parameter configs with name, default, min, max
# - url_param_names: How params are named in the URL (may differ from internal names)

SIMULATIONS = {
    "simple_pendulum": {
        "name": "Time & Pendulums",
        "description": "Explore how pendulum length affects time period",
        "base_url": f"{GITHUB_PAGES_BASE}/simple_pendulum.html",
        "parameters": [
            {
                "name": "length",
                "display_name": "Pendulum Length",
                "default": 5,
                "min": 1,
                "max": 10,
                "unit": "units",
                "url_param": "length"
            },
            {
                "name": "number_of_oscillations",
                "display_name": "Number of Oscillations",
                "default": 10,
                "min": 5,
                "max": 50,
                "unit": "count",
                "url_param": "oscillations"
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Time & Pendulums"
    },
    
    "earth_rotation_revolution": {
        "name": "Earth's Rotation & Revolution",
        "description": "Explore day/night cycles, seasons, and axial tilt",
        "base_url": f"{GITHUB_PAGES_BASE}/rotAndRev.html",
        "parameters": [
            {
                "name": "rotationSpeed",
                "display_name": "Rotation Speed",
                "default": 50,
                "min": 0,
                "max": 100,
                "unit": "%",
                "url_param": "rotationSpeed"
            },
            {
                "name": "axialTilt",
                "display_name": "Axial Tilt",
                "default": 23.5,
                "min": 0,
                "max": 30,
                "unit": "°",
                "url_param": "axialTilt"
            },
            {
                "name": "revolutionSpeed",
                "display_name": "Revolution Speed",
                "default": 50,
                "min": 0,
                "max": 100,
                "unit": "%",
                "url_param": "revolutionSpeed"
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Earth's Rotation & Revolution"
    },
    
    "light_shadows": {
        "name": "Light & Shadows",
        "description": "Explore how light creates shadows and shadow properties",
        "base_url": f"{GITHUB_PAGES_BASE}/lightsShadows.html",
        "parameters": [
            {
                "name": "lightDistance",
                "display_name": "Light Distance",
                "default": 5,
                "min": 1,
                "max": 10,
                "unit": "units",
                "url_param": "lightDistance"
            },
            {
                "name": "objectType",
                "display_name": "Object Type",
                "default": "Opaque",
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "objectType",
                "options": ["Opaque", "Translucent", "Transparent"]
            },
            {
                "name": "objectSize",
                "display_name": "Object Size",
                "default": 5,
                "min": 1,
                "max": 10,
                "unit": "units",
                "url_param": "objectSize"
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Light & Shadows"
    }
}

# =============================================================================
# DEFAULT SIMULATION
# =============================================================================
DEFAULT_SIMULATION = "simple_pendulum"

# =============================================================================
# UI SETTINGS
# =============================================================================
UI_CONFIG = {
    "page_title": "🎓 Adaptive Physics Tutor",
    "page_icon": "🎓",
    "layout": "wide",
    
    # Simulation display
    "simulation_height": 700,
    "simulation_width": "100%",
    
    # Chat settings
    "max_chat_history": 50,  # Messages to keep in view
    
    # Colors
    "teacher_bg_color": "#e3f2fd",  # Light blue
    "student_bg_color": "#f5f5f5",  # Light gray
    "system_bg_color": "#fff3e0",   # Light orange
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_simulation_config(sim_key: str) -> dict:
    """Get configuration for a specific simulation."""
    return SIMULATIONS.get(sim_key, SIMULATIONS[DEFAULT_SIMULATION])


def build_simulation_url(sim_key: str, params: dict, auto_start: bool = True) -> str:
    """
    Build the full URL for a simulation with parameters.
    
    Args:
        sim_key: Key of the simulation (e.g., "simple_pendulum")
        params: Dictionary of parameter values (using internal names)
        auto_start: Whether to auto-start the simulation
        
    Returns:
        Full URL with query parameters
    """
    config = get_simulation_config(sim_key)
    base_url = config["base_url"]
    
    # Build query params
    query_parts = []
    
    # Add simulation parameters
    for param_config in config["parameters"]:
        internal_name = param_config["name"]
        url_name = param_config["url_param"]
        
        if internal_name in params:
            value = params[internal_name]
            query_parts.append(f"{url_name}={value}")
    
    # Add auto-start if enabled
    if auto_start and "auto_start_param" in config:
        query_parts.append(f"{config['auto_start_param']}=true")
    
    # Combine
    if query_parts:
        return f"{base_url}?{'&'.join(query_parts)}"
    return base_url


def get_available_simulations() -> list:
    """Get list of available simulation keys and names."""
    return [(key, config["name"]) for key, config in SIMULATIONS.items()]


def get_default_params(sim_key: str) -> dict:
    """Get default parameter values for a simulation."""
    config = get_simulation_config(sim_key)
    return {
        param["name"]: param["default"] 
        for param in config["parameters"]
    }
