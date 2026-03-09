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
    },
    
    "angle_sum_property": {
        "name": "Triangle Angle Sum",
        "description": "Explore how triangle interior angles always sum to 180°",
        "base_url": f"{GITHUB_PAGES_BASE}/AngleSumProperty.html",
        "parameters": [
            {
                "name": "vertexA_y",
                "display_name": "Top Vertex (A) Height",
                "default": 150,
                "min": 50,
                "max": 550,
                "unit": "pixels",
                "url_param": "vertexA_y"
            },
            {
                "name": "vertexB_x",
                "display_name": "Left Vertex (B) Position",
                "default": 200,
                "min": 50,
                "max": 950,
                "unit": "pixels",
                "url_param": "vertexB_x"
            },
            {
                "name": "vertexC_x",
                "display_name": "Right Vertex (C) Position",
                "default": 800,
                "min": 50,
                "max": 950,
                "unit": "pixels",
                "url_param": "vertexC_x"
            },
            {
                "name": "show_proof_lines",
                "display_name": "Show Geometric Proof",
                "default": False,
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "show_proof_lines",
                "options": [True, False]
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Triangle Angle Sum"
    },
    
    "parallel_lines_angles": {
        "name": "Parallel Lines & Transversal",
        "description": "Explore angle relationships when a transversal crosses parallel lines",
        "base_url": f"{GITHUB_PAGES_BASE}/parallel-angles-interactive.html",
        "parameters": [
            {
                "name": "angle",
                "display_name": "Transversal Angle",
                "default": 60,
                "min": 20,
                "max": 160,
                "unit": "degrees",
                "url_param": "angle"
            },
            {
                "name": "phase",
                "display_name": "Phase",
                "default": "explore",
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "phase",
                "options": ["explore", "quiz"]
            },
            {
                "name": "highlightPair",
                "display_name": "Highlight Angle Pair",
                "default": None,
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "highlightPair",
                "options": [None, "1-5", "2-6", "3-7", "4-8", "3-5", "4-6", "3-6", "4-5"]
            },
            {
                "name": "showRelationships",
                "display_name": "Show Relationships",
                "default": True,
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "showRelationships",
                "options": [True, False]
            },
            {
                "name": "lockAngle",
                "display_name": "Lock Angle",
                "default": False,
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "lockAngle",
                "options": [True, False]
            }
        ],
        "auto_start_param": None,
        "topic": "Parallel Lines & Transversal"
    },
    
    "angle_sum_interactive": {
        "name": "Interactive Triangle Angles",
        "description": "Adjust angles to reshape triangle and see they always sum to 180°",
        "base_url": f"{GITHUB_PAGES_BASE}/angle-sum-property.html",
        "parameters": [
            {
                "name": "angleA",
                "display_name": "Angle A (Red)",
                "default": 60,
                "min": 10,
                "max": 170,
                "unit": "degrees",
                "url_param": "angleA"
            },
            {
                "name": "angleB",
                "display_name": "Angle B (Blue)",
                "default": 60,
                "min": 10,
                "max": 170,
                "unit": "degrees",
                "url_param": "angleB"
            },
            {
                "name": "angleC",
                "display_name": "Angle C (Green)",
                "default": 60,
                "min": 10,
                "max": 170,
                "unit": "degrees",
                "url_param": "angleC"
            },
            {
                "name": "autoInteract",
                "display_name": "Show Discovery Message",
                "default": False,
                "min": None,
                "max": None,
                "unit": "",
                "url_param": "autoInteract",
                "options": [True, False]
            }
        ],
        "auto_start_param": None,
        "topic": "Interactive Triangle Angles"
    },
    
    "speed_race": {
        "name": "Speed, Distance & Time Race",
        "description": "Race simulation comparing speeds of walker, cyclist, car, and train",
        "base_url": f"{GITHUB_PAGES_BASE}/simulation_7_speed_race.html",
        "parameters": [
            {
                "name": "speedWalker",
                "display_name": "Walker Speed",
                "default": 5,
                "min": 1,
                "max": 10,
                "unit": "km/h",
                "url_param": "speedWalker"
            },
            {
                "name": "speedCyclist",
                "display_name": "Cyclist Speed",
                "default": 20,
                "min": 5,
                "max": 40,
                "unit": "km/h",
                "url_param": "speedCyclist"
            },
            {
                "name": "speedCar",
                "display_name": "Car Speed",
                "default": 60,
                "min": 20,
                "max": 120,
                "unit": "km/h",
                "url_param": "speedCar"
            },
            {
                "name": "speedTrain",
                "display_name": "Train Speed",
                "default": 100,
                "min": 50,
                "max": 200,
                "unit": "km/h",
                "url_param": "speedTrain"
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Speed, Distance & Time"
    },
    
    "time_units": {
        "name": "Time Units Converter",
        "description": "Convert between different units of time (hours, minutes, seconds, milliseconds)",
        "base_url": f"{GITHUB_PAGES_BASE}/simulation_5_time_units.html",
        "parameters": [
            {
                "name": "timeValue",
                "display_name": "Time Value",
                "default": 1,
                "min": 0.1,
                "max": 100,
                "unit": "",
                "url_param": "timeValue"
            },
            {
                "name": "timeUnit",
                "display_name": "Time Unit",
                "default": "s",
                "options": ["h", "min", "s", "ms"],
                "option_labels": ["hours (h)", "minutes (min)", "seconds (s)", "milliseconds (ms)"],
                "url_param": "timeUnit"
            }
        ],
        "auto_start_param": None,
        "topic": "Time Units & SI Standards"
    },
    
    "speed_calculator": {
        "name": "Speed Calculator",
        "description": "Calculate speed, distance, or time using the speed formula",
        "base_url": f"{GITHUB_PAGES_BASE}/simulation_6_speed_calculator.html",
        "parameters": [
            {
                "name": "calculationMode",
                "display_name": "Calculation Mode",
                "default": "speed",
                "options": ["speed", "distance", "time"],
                "option_labels": ["Find Speed", "Find Distance", "Find Time"],
                "url_param": "calculationMode"
            },
            {
                "name": "distance",
                "display_name": "Distance (km)",
                "default": 100,
                "min": 1,
                "max": 1000,
                "unit": "km",
                "url_param": "distance"
            },
            {
                "name": "time",
                "display_name": "Time (hours)",
                "default": 2,
                "min": 0.1,
                "max": 100,
                "unit": "h",
                "url_param": "time"
            },
            {
                "name": "speed",
                "display_name": "Speed (km/h)",
                "default": 50,
                "min": 1,
                "max": 1000,
                "unit": "km/h",
                "url_param": "speed"
            }
        ],
        "auto_start_param": None,
        "topic": "Speed, Distance & Time Relationships"
    },
    
    "simple_pendulum_new": {
        "name": "Simple Pendulum Interactive",
        "description": "Explore how length and mass affect pendulum oscillations. Discover why time period depends only on length!",
        "base_url": f"{GITHUB_PAGES_BASE}/simulation_3_pendulum.html",
        "parameters": [
            {
                "name": "length",
                "type": "slider",
                "display_name": "String Length (cm)",
                "default": 100,
                "min": 50,
                "max": 200,
                "unit": "cm",
                "url_param": "length"
            },
            {
                "name": "mass",
                "type": "slider",
                "display_name": "Bob Mass (g)",
                "default": 100,
                "min": 50,
                "max": 200,
                "unit": "g",
                "url_param": "mass"
            }
        ],
        "auto_start_param": "autoStart",
        "topic": "Oscillatory Motion & Time Period"
    },
    
    "brackets_signs": {
        "name": "Brackets & Sign Rules",
        "description": "Learn when to flip signs and when to keep them when removing brackets in algebra",
        "base_url": f"{GITHUB_PAGES_BASE}/ch2_sim2_brackets_signs.html",
        "parameters": [
            {
                "name": "mode",
                "type": "select",
                "display_name": "Mode",
                "default": "learn",
                "options": ["learn", "quiz"],
                "option_labels": ["Learn (Examples)", "Quiz (Test Yourself)"],
                "url_param": "mode"
            },
            {
                "name": "problemIndex",
                "type": "slider",
                "display_name": "Example Number",
                "default": 0,
                "min": 0,
                "max": 9,
                "unit": "",
                "url_param": "problemIndex"
            }
        ],
        "auto_start_param": None,
        "topic": "Algebra - Brackets & Sign Rules"
    },
    
    "distributive": {
        "name": "Distributive Property",
        "description": "Understand a × (b + c) = a × b + a × c through dot arrays, area models, and mental math",
        "base_url": f"{GITHUB_PAGES_BASE}/ch2_sim3_distributive.html",
        "parameters": [
            {
                "name": "mode",
                "type": "select",
                "display_name": "Visualization Mode",
                "default": "dots",
                "options": ["dots", "area", "mental", "quiz"],
                "option_labels": ["Dot Array", "Area Model", "Mental Math", "Quiz"],
                "url_param": "mode"
            },
            {
                "name": "a",
                "type": "slider",
                "display_name": "a (rows/multiplier)",
                "default": 3,
                "min": 1,
                "max": 8,
                "unit": "",
                "url_param": "a"
            },
            {
                "name": "b",
                "type": "slider",
                "display_name": "b (blue columns/first addend)",
                "default": 4,
                "min": 1,
                "max": 10,
                "unit": "",
                "url_param": "b"
            },
            {
                "name": "c",
                "type": "slider",
                "display_name": "c (green columns/second addend)",
                "default": 6,
                "min": 1,
                "max": 10,
                "unit": "",
                "url_param": "c"
            },
            {
                "name": "mentalMathIndex",
                "type": "slider",
                "display_name": "Mental Math Example",
                "default": 0,
                "min": 0,
                "max": 4,
                "unit": "",
                "url_param": "mentalMathIndex"
            },
            {
                "name": "quizIndex",
                "type": "slider",
                "display_name": "Quiz Question",
                "default": 0,
                "min": 0,
                "max": 9,
                "unit": "",
                "url_param": "quizIndex"
            }
        ],
        "auto_start_param": None,
        "topic": "Algebra - Distributive Property"
    }
}


# =============================================================================
# DEFAULT SIMULATION
# =============================================================================
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
            
            # Convert Python booleans to lowercase for JavaScript compatibility
            if isinstance(value, bool):
                value = "true" if value else "false"
            
            query_parts.append(f"{url_name}={value}")
    
    # Add auto-start if enabled and configured
    if auto_start and config.get("auto_start_param"):
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
