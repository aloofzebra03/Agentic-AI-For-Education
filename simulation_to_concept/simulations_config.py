"""
Simulations Configuration
=========================
Contains metadata, parameters, and concepts for all available simulations.
Allows the teaching agent to work with multiple simulations dynamically.
"""

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

SIMULATIONS = {
    "simple_pendulum": {
        "title": "Time & Pendulums",
        "file": "simulations/simple_pendulum.html",
        "description": """
An interactive pendulum simulation where you can control pendulum length 
and number of oscillations to demonstrate how time period is measured 
and how it depends on length.

What can be demonstrated:
- Oscillatory motion (back and forth swinging)
- Measurement of time using oscillations
- Effect of pendulum length on time period
- Difference between total time and time period
- Stability of measurement using multiple oscillations
""",
        "cannot_demonstrate": [
            "Effect of mass on time period",
            "Effect of gravity on time period",
            "Damping or energy loss"
        ],
        "initial_params": {
            "length": 5,
            "number_of_oscillations": 10
        },
        "parameter_info": {
            "length": {
                "label": "Pendulum Length",
                "range": "1-10 units",
                "url_key": "length",
                "effect": "Longer = slower swings (longer period), Shorter = faster swings (shorter period)"
            },
            "number_of_oscillations": {
                "label": "Oscillations to Observe",
                "range": "5-50 count",
                "url_key": "oscillations",
                "effect": "More oscillations = more total time, but time period stays the same"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Time Period of a Pendulum",
                "description": "How the length of a pendulum affects how long it takes to complete one swing.",
                "key_insight": "Longer pendulum = longer time period (slower swings)",
                "related_params": ["length"]
            },
            {
                "id": 2,
                "title": "Measuring Time with Multiple Oscillations",
                "description": "Why observing multiple swings gives a more accurate measurement of the time period.",
                "key_insight": "Multiple oscillations reduce measurement error and show consistency",
                "related_params": ["number_of_oscillations"]
            }
        ]
    },
    
    "earth_rotation_revolution": {
        "title": "Earth's Rotation & Revolution",
        "file": "simulations/rotAndRev.html",
        "description": """
An interactive simulation demonstrating Earth's rotation (day/night cycle) 
and revolution around the Sun (seasons), including the effect of axial tilt.

What can be demonstrated:
- Day and night cycle from Earth's rotation
- Seasonal changes from Earth's revolution and axial tilt
- Effect of axial tilt on seasons
- Relationship between rotation speed and day length
- Relationship between revolution speed and year length
""",
        "cannot_demonstrate": [
            "Moon phases or lunar orbit",
            "Solar and lunar eclipses",
            "Tides"
        ],
        "initial_params": {
            "rotationSpeed": 50,
            "axialTilt": 23.5,
            "revolutionSpeed": 50
        },
        "parameter_info": {
            "rotationSpeed": {
                "label": "Rotation Speed",
                "range": "0-100%",
                "url_key": "rotationSpeed",
                "effect": "Controls how fast Earth spins (day/night cycle speed)"
            },
            "axialTilt": {
                "label": "Axial Tilt Angle",
                "range": "0-30 degrees",
                "url_key": "axialTilt",
                "effect": "Affects seasons - more tilt = more extreme seasons, no tilt = no seasons"
            },
            "revolutionSpeed": {
                "label": "Revolution Speed",
                "range": "0-100%",
                "url_key": "revolutionSpeed",
                "effect": "Controls how fast Earth orbits the Sun (year length)"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Earth's Rotation and Day/Night",
                "description": "How Earth's spinning on its axis creates the day and night cycle.",
                "key_insight": "Earth's rotation causes day and night - one complete rotation = one day",
                "related_params": ["rotationSpeed"]
            },
            {
                "id": 2,
                "title": "Axial Tilt and Seasons",
                "description": "How Earth's tilted axis causes different seasons throughout the year.",
                "key_insight": "Axial tilt causes seasons - more tilt = more extreme seasonal differences",
                "related_params": ["axialTilt", "revolutionSpeed"]
            },
            {
                "id": 3,
                "title": "Revolution Around the Sun",
                "description": "How Earth's orbit around the Sun, combined with axial tilt, creates yearly seasonal cycles.",
                "key_insight": "Revolution + axial tilt creates seasons - one complete orbit = one year",
                "related_params": ["revolutionSpeed", "axialTilt"]
            }
        ]
    },
    
    "light_shadows": {
        "title": "Light & Shadows",
        "file": "simulations/lightsShadows.html",
        "description": """
An interactive simulation exploring how light creates shadows and how 
shadow properties change based on light source distance, object properties, 
and object size.

What can be demonstrated:
- Shadow formation from light blocking
- Effect of light distance on shadow size
- Effect of object size on shadow size
- Different shadow properties (opaque, translucent, transparent)
- Relationship between light rays and shadow boundaries
""",
        "cannot_demonstrate": [
            "Color effects or refraction",
            "Multiple light sources",
            "Reflection from mirrors"
        ],
        "initial_params": {
            "lightDistance": 5,
            "objectType": "Opaque",
            "objectSize": 5
        },
        "parameter_info": {
            "lightDistance": {
                "label": "Light Distance",
                "range": "1-10 units",
                "url_key": "lightDistance",
                "effect": "Closer light = larger shadow, Further light = smaller shadow"
            },
            "objectType": {
                "label": "Object Type",
                "range": "Opaque, Translucent, Transparent",
                "url_key": "objectType",
                "effect": "Opaque = dark shadow, Translucent = lighter fuzzy shadow, Transparent = no shadow"
            },
            "objectSize": {
                "label": "Object Size",
                "range": "1-10 units",
                "url_key": "objectSize",
                "effect": "Larger object = larger shadow, Smaller object = smaller shadow"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Shadow Formation",
                "description": "How shadows are created when objects block light.",
                "key_insight": "Opaque objects block light completely, creating shadows",
                "related_params": ["objectType"]
            },
            {
                "id": 2,
                "title": "Light Distance and Shadow Size",
                "description": "How the distance of the light source affects the size of the shadow.",
                "key_insight": "Closer light source = larger shadow (light rays are more divergent)",
                "related_params": ["lightDistance"]
            },
            {
                "id": 3,
                "title": "Object Properties and Shadows",
                "description": "How different object types (opaque, translucent, transparent) create different shadow characteristics.",
                "key_insight": "Material transparency affects shadow darkness - opaque blocks most, transparent blocks none",
                "related_params": ["objectType", "objectSize"]
            }
        ]
    }
}

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_simulation(simulation_id: str) -> dict:
    """Get a specific simulation configuration."""
    return SIMULATIONS.get(simulation_id, None)

def get_all_simulations() -> dict:
    """Get all available simulations."""
    return SIMULATIONS

def get_simulation_list() -> list:
    """Get list of available simulation IDs and titles."""
    return [
        {"id": sim_id, "title": config["title"]} 
        for sim_id, config in SIMULATIONS.items()
    ]

def get_parameter_info(simulation_id: str) -> dict:
    """Get parameter information for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["parameter_info"] if sim else {}

def get_concepts(simulation_id: str) -> list:
    """Get concepts for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["concepts"] if sim else []

def get_initial_params(simulation_id: str) -> dict:
    """Get initial parameters for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["initial_params"] if sim else {}


# ═══════════════════════════════════════════════════════════════════════
# QUIZ QUESTIONS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

QUIZ_QUESTIONS = {
    "simple_pendulum": [
        {
            "id": "pendulum_q1",
            "challenge": "Can you make the pendulum swing slower? Set the pendulum length to 8 units or more to increase the time period.",
            "target_parameters": ["length"],
            "success_rule": {
                "conditions": [
                    {"parameter": "length", "operator": ">=", "value": 8}
                ],
                "scoring": {
                    "perfect": 1.0,    # length >= 8
                    "partial": 0.6,    # length >= 6
                    "wrong": 0.3       # length < 6
                },
                "thresholds": {
                    "perfect": {"length": 8},
                    "partial": {"length": 6}
                }
            },
            "hints": {
                "attempt_1": "Think about what makes a pendulum swing slower. Which parameter affects the time period?",
                "attempt_2": "Remember from our lesson: longer pendulums take more time per swing. Try increasing the length parameter.",
                "attempt_3": "Set the length to 8 or higher to make the pendulum swing slowly."
            },
            "concept_reminder": "The time period of a pendulum depends on its length. A longer pendulum swings slower (longer time period), while a shorter pendulum swings faster (shorter time period)."
        },
        {
            "id": "pendulum_q2",
            "challenge": "Set the pendulum to complete exactly 5 oscillations. Can you make it swing as fast as possible while counting 5 swings?",
            "target_parameters": ["number_of_oscillations", "length"],
            "success_rule": {
                "conditions": [
                    {"parameter": "number_of_oscillations", "operator": "==", "value": 5},
                    {"parameter": "length", "operator": "<=", "value": 3}
                ],
                "scoring": {
                    "perfect": 1.0,    # oscillations == 5 AND length <= 3
                    "partial": 0.6,    # oscillations == 5 only
                    "wrong": 0.3       # neither condition met
                },
                "thresholds": {
                    "perfect": {"number_of_oscillations": 5, "length": 3},
                    "partial": {"number_of_oscillations": 5}
                }
            },
            "hints": {
                "attempt_1": "You need to set the number of oscillations to exactly 5, and make the pendulum swing quickly.",
                "attempt_2": "Remember: shorter pendulums swing faster! Try reducing the length while keeping oscillations at 5.",
                "attempt_3": "Set number_of_oscillations to 5 and length to 3 or less for the fastest swings."
            },
            "concept_reminder": "The number of oscillations determines how many swings we count, while length affects how fast each swing happens. Shorter pendulums complete multiple swings in less total time."
        }
    ],
    
    "earth_rotation_revolution": [
        {
            "id": "earth_q1",
            "challenge": "Can you make it nighttime for the observer on Earth? Adjust the rotation to show darkness.",
            "target_parameters": ["rotation_angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "rotation_angle", "operator": ">=", "value": 90},
                    {"parameter": "rotation_angle", "operator": "<=", "value": 270}
                ],
                "scoring": {
                    "perfect": 1.0,    # 90° <= rotation <= 270° (night side)
                    "partial": 0.6,    # close to night (60-90° or 270-300°)
                    "wrong": 0.3       # day side
                },
                "thresholds": {
                    "perfect": {"rotation_angle_min": 90, "rotation_angle_max": 270},
                    "partial": {"rotation_angle_min": 60, "rotation_angle_max": 300}
                }
            },
            "hints": {
                "attempt_1": "Think about when your side of Earth faces away from the Sun. What angle makes it night?",
                "attempt_2": "Earth's rotation causes day and night. Try rotating so the observer faces away from the Sun (between 90° and 270°).",
                "attempt_3": "Set rotation angle between 90° and 270° to place the observer on the night side."
            },
            "concept_reminder": "Earth's rotation on its axis causes day and night. When your location faces the Sun, it's day. When facing away from the Sun (opposite side), it's night."
        },
        {
            "id": "earth_q2",
            "challenge": "Position Earth in winter (for the Northern Hemisphere). Show Earth at the correct position in its orbit.",
            "target_parameters": ["revolution_angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "revolution_angle", "operator": ">=", "value": 250},
                    {"parameter": "revolution_angle", "operator": "<=", "value": 290}
                ],
                "scoring": {
                    "perfect": 1.0,    # ~270° (winter solstice)
                    "partial": 0.6,    # close to winter position
                    "wrong": 0.3       # wrong season
                },
                "thresholds": {
                    "perfect": {"revolution_angle_min": 250, "revolution_angle_max": 290},
                    "partial": {"revolution_angle_min": 230, "revolution_angle_max": 310}
                }
            },
            "hints": {
                "attempt_1": "In winter, the Northern Hemisphere tilts away from the Sun. Where should Earth be in its orbit?",
                "attempt_2": "Remember: Earth's tilt combined with its position in orbit creates seasons. Try around 270° for winter.",
                "attempt_3": "Set revolution angle between 250° and 290° to show Earth in winter position."
            },
            "concept_reminder": "Earth's revolution around the Sun, combined with its tilted axis, causes seasons. In winter, your hemisphere tilts away from the Sun, receiving less direct sunlight."
        }
    ],
    
    "light_shadows": [
        {
            "id": "light_q1",
            "challenge": "Create a partial shadow (penumbra). Adjust the light size to show both dark and lighter shadow regions.",
            "target_parameters": ["light_size"],
            "success_rule": {
                "conditions": [
                    {"parameter": "light_size", "operator": ">=", "value": 3}
                ],
                "scoring": {
                    "perfect": 1.0,    # light_size >= 3 (clear penumbra)
                    "partial": 0.6,    # light_size >= 2 (some penumbra)
                    "wrong": 0.3       # light_size < 2 (sharp shadow)
                },
                "thresholds": {
                    "perfect": {"light_size": 3},
                    "partial": {"light_size": 2}
                }
            },
            "hints": {
                "attempt_1": "A partial shadow forms when the light source is large. How big should the light be?",
                "attempt_2": "Larger light sources create softer shadows with partial shadow regions (penumbra). Try increasing light size.",
                "attempt_3": "Set light size to 3 or more to create a clear partial shadow (penumbra) around the dark shadow (umbra)."
            },
            "concept_reminder": "The size of the light source affects shadow sharpness. Large light sources create soft shadows with partial shadow regions (penumbra), while small light sources create sharp shadows."
        },
        {
            "id": "light_q2",
            "challenge": "Make the shadow as long as possible. Position the light to create the longest shadow.",
            "target_parameters": ["light_distance"],
            "success_rule": {
                "conditions": [
                    {"parameter": "light_distance", "operator": "<=", "value": 3}
                ],
                "scoring": {
                    "perfect": 1.0,    # light_distance <= 3 (very long shadow)
                    "partial": 0.6,    # light_distance <= 5 (longer shadow)
                    "wrong": 0.3       # light_distance > 5 (short shadow)
                },
                "thresholds": {
                    "perfect": {"light_distance": 3},
                    "partial": {"light_distance": 5}
                }
            },
            "hints": {
                "attempt_1": "Shadow length depends on how close or far the light is. What distance creates the longest shadow?",
                "attempt_2": "When light is closer to the object, shadows appear longer. Try moving the light closer.",
                "attempt_3": "Set light distance to 3 or less to create the longest possible shadow."
            },
            "concept_reminder": "Shadow length depends on the distance between the light source and the object. Closer light sources create longer shadows, while farther light sources create shorter shadows."
        }
    ]
}


def get_quiz_questions(simulation_id: str) -> list:
    """Get quiz questions for a specific simulation."""
    return QUIZ_QUESTIONS.get(simulation_id, [])
