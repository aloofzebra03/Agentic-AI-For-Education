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

# =============================================================================
# PARALLEL LINES & TRANSVERSAL SIMULATION
# =============================================================================
SIMULATIONS["parallel_lines_angles"] = {
    "title": "Parallel Lines & Transversal",
    "file": "simulations/parallel-angles-interactive.html",
    "description": """
An interactive simulation where you explore angle relationships when a transversal 
line crosses two parallel lines. Drag the purple transversal to change its angle 
and observe how all 8 angles change together. Discover why corresponding angles are equal, 
alternate interior angles are equal, and co-interior angles sum to 180°.
    """.strip(),
    "concepts": [
        {
            "id": 1,
            "title": "Corresponding Angles",
            "description": "Understanding angle relationships when a transversal cuts parallel lines - corresponding angles are in matching positions.",
            "key_insight": "When a transversal crosses parallel lines, angles in the same position at each intersection are always equal (∠1 = ∠5, ∠2 = ∠6, ∠3 = ∠7, ∠4 = ∠8)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 2,
            "title": "Alternate Interior Angles",
            "description": "Exploring angles on opposite sides of a transversal between parallel lines.",
            "key_insight": "Angles on opposite sides of the transversal, between the parallel lines, are always equal (∠3 = ∠5, ∠4 = ∠6)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 3,
            "title": "Co-interior Angles (Consecutive Interior)",
            "description": "Investigating angles on the same side of a transversal between parallel lines.",
            "key_insight": "Angles on the same side of the transversal, between parallel lines, always sum to 180° (∠3 + ∠6 = 180°, ∠4 + ∠5 = 180°)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 4,
            "title": "Vertically Opposite Angles",
            "description": "Understanding angle relationships at the intersection of two lines.",
            "key_insight": "When two lines intersect, angles opposite each other are always equal (∠1 = ∠4, ∠2 = ∠3, ∠5 = ∠8, ∠6 = ∠7)",
            "related_params": ["angle"]
        }
    ],
    "cannot_demonstrate": [
        "Non-parallel lines",
        "More than two parallel lines",
        "Curved transversal",
        "Angles with non-Euclidean geometry",
        "Perpendicular relationships between the parallel lines"
    ],
    "initial_params": {
        "angle": 60,
        "phase": "explore",
        "highlightPair": None,
        "showRelationships": True,
        "lockAngle": False
    },
    "parameter_info": {
        "angle": {
            "label": "Transversal Angle",
            "range": "20-160 degrees",
            "url_key": "angle",
            "effect": "Changes the acute angle of the transversal line crossing the parallel lines"
        },
        "phase": {
            "label": "Phase",
            "range": "explore, quiz",
            "url_key": "phase",
            "effect": "Switches between exploration mode and built-in quiz mode"
        },
        "highlightPair": {
            "label": "Highlight Angle Pair",
            "range": "None, '1-5', '2-6', '3-7', '4-8', '3-5', '4-6', '3-6', '4-5'",
            "url_key": "highlightPair",
            "effect": "Highlights specific angle pair to focus student attention on relationships"
        },
        "showRelationships": {
            "label": "Show Relationships",
            "range": "true/false",
            "url_key": "showRelationships",
            "effect": "Shows or hides the relationship cards explaining angle types (corresponding, alternate, co-interior)"
        },
        "lockAngle": {
            "label": "Lock Angle",
            "range": "true/false",
            "url_key": "lockAngle",
            "effect": "Prevents student from dragging transversal - useful for demonstrations"
        }
    }
}

# =============================================================================
# SPEED RACE SIMULATION
# =============================================================================
SIMULATIONS["speed_race"] = {
    "title": "Speed, Distance & Time Race",
    "file": "simulations/simulation_7_speed_race.html",
    "description": """
An interactive race simulation where four different modes of transport (walker, cyclist, car, train) 
compete to travel 1 kilometer. Students can adjust the speed of each racer to understand the 
relationship between speed, distance, and time.

What can be demonstrated:
- Relationship between speed and time for fixed distance (Time = Distance ÷ Speed)
- Comparing different speeds and their effects on travel time
- Real-world speed concepts with familiar modes of transport
- How increasing speed decreases time for the same distance
- Mathematical calculation: Time = Distance ÷ Speed
""",
        "cannot_demonstrate": [
            "Acceleration or changing speeds during race",
            "Different distances for different racers",
            "Energy consumption or fuel efficiency",
            "Traffic conditions or obstacles"
        ],
        "initial_params": {
            "speedWalker": 5,
            "speedCyclist": 20,
            "speedCar": 60,
            "speedTrain": 100
        },
        "parameter_info": {
            "speedWalker": {
                "label": "Walker Speed",
                "range": "1-10 km/h",
                "min": 1,
                "max": 10,
                "url_key": "speedWalker",
                "effect": "Controls how fast the walker moves (typical walking speed: 5 km/h)"
            },
            "speedCyclist": {
                "label": "Cyclist Speed",
                "range": "5-40 km/h",
                "min": 5,
                "max": 40,
                "url_key": "speedCyclist",
                "effect": "Controls how fast the cyclist moves (typical cycling speed: 20 km/h)"
            },
            "speedCar": {
                "label": "Car Speed",
                "range": "20-120 km/h",
                "min": 20,
                "max": 120,
                "url_key": "speedCar",
                "effect": "Controls how fast the car moves (typical city car speed: 60 km/h)"
            },
            "speedTrain": {
                "label": "Train Speed",
                "range": "50-200 km/h",
                "min": 50,
                "max": 200,
                "url_key": "speedTrain",
                "effect": "Controls how fast the train moves (typical train speed: 100 km/h)"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Speed and Time Relationship",
                "description": "Understanding how speed affects the time taken to cover a fixed distance.",
                "key_insight": "Higher speed means less time to cover the same distance. Time = Distance ÷ Speed",
                "related_params": ["speedWalker", "speedCyclist", "speedCar", "speedTrain"]
            },
            {
                "id": 2,
                "title": "Calculating Travel Time",
                "description": "Learning to calculate time when distance and speed are known.",
                "key_insight": "For 1 km at 5 km/h: Time = 1 ÷ 5 = 0.2 hours = 12 minutes. Double the speed, halve the time!",
                "related_params": ["speedWalker", "speedCyclist", "speedCar", "speedTrain"]
            },
            {
                "id": 3,
                "title": "Comparing Different Speeds",
                "description": "Comparing how different speeds affect arrival times in a race scenario.",
                "key_insight": "The racer with the highest speed finishes first. A train at 100 km/h is 20 times faster than a walker at 5 km/h",
                "related_params": ["speedWalker", "speedCyclist", "speedCar", "speedTrain"]
            },
            {
                "id": 4,
                "title": "Real-World Speed Context",
                "description": "Understanding typical speeds of different modes of transport in everyday life.",
                "key_insight": "Walking ≈ 5 km/h, Cycling ≈ 20 km/h, Car ≈ 60 km/h, Train ≈ 100 km/h - each is progressively faster",
                "related_params": ["speedWalker", "speedCyclist", "speedCar", "speedTrain"]
            }
        ]
}

# =============================================================================
# TIME UNITS CONVERTER SIMULATION
# =============================================================================
SIMULATIONS["time_units"] = {
    "title": "Time Units Converter",
    "file": "simulations/simulation_5_time_units.html",
    "description": """
An interactive time units converter that helps students understand the SI unit of time 
and conversions between different time units (hours, minutes, seconds, milliseconds). 
Students can input a time value in one unit and see equivalent values in all other units.

What can be demonstrated:
- The second (s) is the SI unit of time
- Conversion between hours, minutes, seconds, and milliseconds
- Proper SI notation for time units (s, min, h, ms - not sec, mins, hrs)
- Practical applications of small time units in sports, medicine, computers, and music
- Mathematical relationships: 1 hour = 60 minutes = 3600 seconds
""",
    "cannot_demonstrate": [
        "Time periods longer than hours (days, months, years)",
        "Time zones or local time differences",
        "Calendar systems or date calculations",
        "Historical timekeeping methods"
    ],
    "initial_params": {
        "timeValue": 1,
        "timeUnit": "s"
    },
    "parameter_info": {
        "timeValue": {
            "label": "Time Value",
            "range": "0.001-10000",
            "min": 0.001,
            "max": 10000,
            "url_key": "timeValue",
            "effect": "The numeric value of time to convert to different units"
        },
        "timeUnit": {
            "label": "Time Unit",
            "range": "h, min, s, ms",
            "url_key": "timeUnit",
            "effect": "The unit of the input time: h (hours), min (minutes), s (seconds), ms (milliseconds)"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "SI Unit of Time (Second)",
            "description": "Understanding that the second is the fundamental SI unit for measuring time.",
            "key_insight": "The second (s) is the SI base unit for time. All other time units are derived from seconds: 60s = 1min, 3600s = 1h",
            "related_params": ["timeValue", "timeUnit"]
        },
        {
            "id": 2,
            "title": "Time Unit Conversions",
            "description": "Learning to convert between different units of time using conversion factors.",
            "key_insight": "1 hour = 60 minutes, 1 minute = 60 seconds, 1 second = 1000 milliseconds. Use multiplication/division to convert between units",
            "related_params": ["timeValue", "timeUnit"]
        },
        {
            "id": 3,
            "title": "Proper SI Notation for Time",
            "description": "Using correct standardized symbols for time units without periods or pluralization.",
            "key_insight": "Correct notation: s (not sec), min (not mins), h (not hr/hrs), ms (not msec). SI symbols are always singular and without periods",
            "related_params": ["timeUnit"]
        },
        {
            "id": 4,
            "title": "Applications of Small Time Units",
            "description": "Understanding why milliseconds and smaller units are important in real-world applications.",
            "key_insight": "Milliseconds matter in Olympic sports (race results), medicine (ECG), computers (processor speed), and music (digital recording samples)",
            "related_params": ["timeValue", "timeUnit"]
        }
    ]
}

# =============================================================================
# SPEED CALCULATOR SIMULATION
# =============================================================================
SIMULATIONS["speed_calculator"] = {
    "title": "Speed Calculator",
    "file": "simulations/simulation_6_speed_calculator.html",
    "description": """
An interactive calculator that helps students understand the relationship between speed, 
distance, and time. Students can calculate any one variable when the other two are known, 
reinforcing the formula Speed = Distance ÷ Time and its rearrangements.

What can be demonstrated:
- Speed calculation: Speed = Distance ÷ Time
- Distance calculation: Distance = Speed × Time
- Time calculation: Time = Distance ÷ Speed
- Real-world speed values for different modes of transport
- Unit conversion between km/h and m/s
- Working steps showing the calculation process
""",
    "cannot_demonstrate": [
        "Acceleration or changing speeds",
        "Force or momentum calculations",
        "Energy or power calculations",
        "Relative motion or reference frames"
    ],
    "initial_params": {
        "calculationMode": "speed",
        "distance": 100,
        "time": 2,
        "speed": 50
    },
    "parameter_info": {
        "calculationMode": {
            "label": "Calculation Mode",
            "range": "speed, distance, time",
            "url_key": "calculationMode",
            "effect": "Determines which variable to calculate: 'speed' (find speed), 'distance' (find distance), or 'time' (find time)"
        },
        "distance": {
            "label": "Distance",
            "range": "1-1000 km",
            "min": 1,
            "max": 1000,
            "url_key": "distance",
            "effect": "The distance traveled in kilometers (used when calculating speed or time)"
        },
        "time": {
            "label": "Time",
            "range": "0.1-100 hours",
            "min": 0.1,
            "max": 100,
            "url_key": "time",
            "effect": "The time taken in hours (used when calculating speed or distance)"
        },
        "speed": {
            "label": "Speed",
            "range": "1-1000 km/h",
            "min": 1,
            "max": 1000,
            "url_key": "speed",
            "effect": "The speed in kilometers per hour (used when calculating distance or time)"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Speed Formula and Its Meaning",
            "description": "Understanding what speed is and how it relates to distance and time.",
            "key_insight": "Speed = Distance ÷ Time. Speed tells us how fast something moves by showing how much distance is covered per unit of time",
            "related_params": ["calculationMode", "distance", "time", "speed"]
        },
        {
            "id": 2,
            "title": "Calculating Speed from Distance and Time",
            "description": "Learning to find speed when distance and time are known.",
            "key_insight": "To find speed, divide distance by time. For example: 100 km ÷ 2 hours = 50 km/h. The object travels 50 km every hour",
            "related_params": ["calculationMode", "distance", "time"]
        },
        {
            "id": 3,
            "title": "Rearranging the Formula for Distance",
            "description": "Using the speed formula to find distance when speed and time are known.",
            "key_insight": "Distance = Speed × Time. Multiply speed by time to find total distance. For example: 50 km/h × 3 hours = 150 km",
            "related_params": ["calculationMode", "speed", "time"]
        },
        {
            "id": 4,
            "title": "Rearranging the Formula for Time",
            "description": "Using the speed formula to find time when distance and speed are known.",
            "key_insight": "Time = Distance ÷ Speed. Divide distance by speed to find time needed. For example: 200 km ÷ 100 km/h = 2 hours",
            "related_params": ["calculationMode", "distance", "speed"]
        }
    ]
}

# =============================================================================
# SIMPLE PENDULUM NEW SIMULATION
# =============================================================================
SIMULATIONS["simple_pendulum_new"] = {
    "title": "Simple Pendulum Interactive",
    "file": "simulations/simulation_3_pendulum.html",
    "description": """
An interactive simple pendulum simulation where students can adjust the string length and 
bob mass to explore oscillatory motion. The simulation demonstrates the key physics principle: 
time period depends ONLY on length, NOT on mass.

What can be demonstrated:
- Simple harmonic motion (oscillation)
- Effect of string length on time period (T = 2π√(L/g))
- Independence of time period from mass
- Relationship between time period and frequency
- Real-time tracking of oscillations
- Mean position and extreme positions
""",
    "cannot_demonstrate": [
        "Effect of amplitude on time period (for small angles)",
        "Effect of gravity on time period",
        "Damping or air resistance",
        "Energy conversion (potential to kinetic)"
    ],
    "initial_params": {
        "length": 100,
        "mass": 100
    },
    "parameter_info": {
        "length": {
            "label": "String Length",
            "range": "50-200 cm",
            "min": 50,
            "max": 200,
            "url_key": "length",
            "effect": "Longer string = longer time period (slower oscillations). Time period increases with square root of length"
        },
        "mass": {
            "label": "Bob Mass",
            "range": "50-200 g",
            "min": 50,
            "max": 200,
            "url_key": "mass",
            "effect": "Mass does NOT affect time period! This is a key discovery - try changing mass and observe that period stays constant"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "What is a Simple Pendulum",
            "description": "Understanding the basic components and motion of a simple pendulum.",
            "key_insight": "A simple pendulum consists of a mass (bob) hanging from a string attached to a fixed point. When displaced, it swings back and forth in regular oscillations",
            "related_params": ["length", "mass"]
        },
        {
            "id": 2,
            "title": "Time Period and Its Formula",
            "description": "Learning the mathematical relationship that determines how long one complete oscillation takes.",
            "key_insight": "Time period T = 2π√(L/g), where L is length and g is gravity (9.8 m/s²). The period depends only on length, not on mass!",
            "related_params": ["length"]
        },
        {
            "id": 3,
            "title": "Effect of Length on Oscillation",
            "description": "Discovering how changing the string length changes the oscillation speed.",
            "key_insight": "Longer pendulums swing more slowly (longer period), shorter pendulums swing faster (shorter period). The relationship follows a square root pattern",
            "related_params": ["length"]
        },
        {
            "id": 4,
            "title": "Mass Independence - A Surprising Discovery",
            "description": "Understanding why mass doesn't affect the time period of a pendulum.",
            "key_insight": "The time period is independent of mass! A heavy bob and light bob swing at the same rate if the length is the same. This is why pendulums are reliable for timekeeping",
            "related_params": ["mass", "length"]
        }
    ]
}

# =============================================================================
# BRACKETS & SIGN RULES SIMULATION
# =============================================================================
SIMULATIONS["brackets_signs"] = {
    "title": "Brackets & Sign Rules",
    "file": "simulations/ch2_sim2_brackets_signs.html",
    "description": """
An interactive simulation teaching the fundamental rules of bracket removal in algebra.
Students learn when to flip signs and when to keep them based on what comes before the brackets.

What can be demonstrated:
- Removing brackets when preceded by a minus sign (signs flip)
- Removing brackets when preceded by a plus sign (signs stay same)
- Step-by-step explanation of sign changes
- Multiple examples with varying complexity
- Quiz mode to test understanding
- Real arithmetic evaluation showing both forms are equal
""",
    "cannot_demonstrate": [
        "Multiplication of brackets (distributive property)",
        "Nested brackets (brackets within brackets)",
        "Algebraic expressions with variables",
        "Brackets with coefficients (e.g., 2(x + 3))"
    ],
    "initial_params": {
        "mode": "learn",
        "problemIndex": 0
    },
    "parameter_info": {
        "mode": {
            "label": "Mode",
            "range": "learn or quiz",
            "options": ["learn", "quiz"],
            "url_key": "mode",
            "effect": "Learn mode shows examples with step-by-step explanations. Quiz mode tests understanding with multiple choice questions"
        },
        "problemIndex": {
            "label": "Problem/Example Number",
            "range": "0-9",
            "min": 0,
            "max": 9,
            "url_key": "problemIndex",
            "effect": "In Learn mode: selects which example to display (10 examples total). Different examples show various cases of sign flipping and keeping"
        }
    },
    "problem_examples": [
        {"index": 0, "expression": "200 − (40 + 3)", "result": "200 − 40 − 3 = 157", "rule": "minus", "explanation": "Minus before bracket → signs flip"},
        {"index": 1, "expression": "500 − (250 − 100)", "result": "500 − 250 + 100 = 350", "rule": "minus", "explanation": "Minus before bracket → signs flip (tricky: −100 becomes +100)"},
        {"index": 2, "expression": "100 − (15 + 56)", "result": "100 − 15 − 56 = 29", "rule": "minus", "explanation": "Minus before bracket → signs flip"},
        {"index": 3, "expression": "28 + (35 − 10)", "result": "28 + 35 − 10 = 53", "rule": "plus", "explanation": "Plus before bracket → signs stay the same"},
        {"index": 4, "expression": "24 + (6 − 4)", "result": "24 + 6 − 4 = 26", "rule": "plus", "explanation": "Plus before bracket → signs stay the same"},
        {"index": 5, "expression": "24 − (6 + 4)", "result": "24 − 6 − 4 = 14", "rule": "minus", "explanation": "Minus before bracket → signs flip"},
        {"index": 6, "expression": "27 − (8 + 3)", "result": "27 − 8 − 3 = 16", "rule": "minus", "explanation": "Minus before bracket → signs flip"},
        {"index": 7, "expression": "27 − (8 − 3)", "result": "27 − 8 + 3 = 22", "rule": "minus", "explanation": "Minus before bracket → both signs flip"},
        {"index": 8, "expression": "14 − (12 − 10)", "result": "14 − 12 + 10 = 12", "rule": "minus", "explanation": "Minus before bracket → both signs flip"},
        {"index": 9, "expression": "14 − (−12 − 10)", "result": "14 + 12 + 10 = 36", "rule": "minus", "explanation": "Minus before bracket → negative numbers become positive"}
    ],
    "concepts": [
        {
            "id": 1,
            "title": "Understanding Brackets in Arithmetic",
            "description": "Learning what brackets represent and why we need rules to remove them.",
            "key_insight": "Brackets group terms together. When we remove brackets, we must follow specific rules to maintain the expression's value. The sign before the bracket determines what happens to signs inside",
            "related_params": ["mode", "problemIndex"]
        },
        {
            "id": 2,
            "title": "The Minus-Before-Bracket Rule",
            "description": "Discovering that a minus sign before brackets flips all signs inside.",
            "key_insight": "When there's a MINUS before brackets, every sign inside FLIPS: + becomes −, and − becomes +. Example: 100 − (40 + 3) = 100 − 40 − 3. This is because we're subtracting everything in the brackets",
            "related_params": ["problemIndex"]
        },
        {
            "id": 3,
            "title": "The Plus-Before-Bracket Rule",
            "description": "Understanding that a plus sign before brackets means signs stay the same.",
            "key_insight": "When there's a PLUS before brackets, signs inside STAY THE SAME: just remove the brackets. Example: 28 + (35 − 10) = 28 + 35 − 10. Adding a group doesn't change the signs",
            "related_params": ["problemIndex"]
        },
        {
            "id": 4,
            "title": "Why Signs Flip - The Logic Behind It",
            "description": "Understanding the mathematical reasoning for sign changes.",
            "key_insight": "Subtracting a sum means subtracting each part. Subtracting a difference means subtract the first but ADD the second (you subtracted too much!). Example: 500 − (250 − 100) = 500 − 250 + 100, because you need to add back the 100 you removed",
            "related_params": ["problemIndex"]
        }
    ]
}

# ---------------------------------------------------------------------------
# DISTRIBUTIVE PROPERTY SIMULATION
# ---------------------------------------------------------------------------

SIMULATIONS["distributive"] = {
    "id": "distributive",
    "title": "Distributive Property",
    "file": "simulations/ch2_sim3_distributive.html",
    "description": "Understand the distributive property: a × (b + c) = a × b + a × c through multiple visual representations and mental math applications",
    "url": "https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/ch2_sim3_distributive.html",
    "cannot_demonstrate": [
        "Factoring expressions (reverse of distributive property)",
        "Distributive property with division",
        "Distributive property with three or more terms inside brackets",
        "Algebraic expressions with variables only (this uses concrete numbers)",
        "FOIL method for binomial multiplication"
    ],
    "initial_params": {
        "mode": "dots",
        "a": 3,
        "b": 4,
        "c": 6,
        "mentalMathIndex": 0,
        "quizIndex": 0
    },
    "parameter_info": {
        "mode": {
            "label": "Visualization Mode",
            "range": "dots, area, mental, or quiz",
            "options": ["dots", "area", "mental", "quiz"],
            "url_key": "mode",
            "effect": "dots: Visual dot array showing a×(b+c) split into colored groups. area: Rectangle area model. mental: Mental math examples using distributive property. quiz: Practice questions"
        },
        "a": {
            "label": "Multiplier (rows)",
            "range": "1-8",
            "min": 1,
            "max": 8,
            "url_key": "a",
            "effect": "Number of rows in array or height of rectangle. This is the number being distributed across the sum (b + c)"
        },
        "b": {
            "label": "First Addend (blue columns)",
            "range": "1-10",
            "min": 1,
            "max": 10,
            "url_key": "b",
            "effect": "Number of blue columns/width. First number in the sum being multiplied. Forms the first product: a × b"
        },
        "c": {
            "label": "Second Addend (green columns)",
            "range": "1-10",
            "min": 1,
            "max": 10,
            "url_key": "c",
            "effect": "Number of green columns/width. Second number in the sum being multiplied. Forms the second product: a × c"
        },
        "mentalMathIndex": {
            "label": "Mental Math Example",
            "range": "0-4",
            "min": 0,
            "max": 4,
            "url_key": "mentalMathIndex",
            "effect": "Selects which mental math example to display (5 examples: 97×25, 95×8, 104×15, 49×50, 998×7). Each shows how to use distributive property for quick calculations"
        },
        "quizIndex": {
            "label": "Quiz Question",
            "range": "0-9",
            "min": 0,
            "max": 9,
            "url_key": "quizIndex",
            "effect": "Selects which quiz question to display (10 questions total with progressive difficulty)"
        }
    },
    "parameters": [
        {
            "name": "mode",
            "type": "select",
            "description": "Visualization/teaching mode",
            "options": ["dots", "area", "mental", "quiz"],
            "default": "dots",
            "range": None
        },
        {
            "name": "a",
            "type": "number",
            "description": "Number of rows in the array (multiplier)",
            "options": None,
            "default": 3,
            "range": {"min": 1, "max": 8, "step": 1}
        },
        {
            "name": "b",
            "type": "number",
            "description": "Number of blue columns (first addend)",
            "options": None,
            "default": 4,
            "range": {"min": 1, "max": 10, "step": 1}
        },
        {
            "name": "c",
            "type": "number",
            "description": "Number of green columns (second addend)",
            "options": None,
            "default": 6,
            "range": {"min": 1, "max": 10, "step": 1}
        },
        {
            "name": "mentalMathIndex",
            "type": "number",
            "description": "Which mental math example to show (0-4)",
            "options": None,
            "default": 0,
            "range": {"min": 0, "max": 4, "step": 1}
        },
        {
            "name": "quizIndex",
            "type": "number",
            "description": "Quiz question index (0-9)",
            "options": None,
            "default": 0,
            "range": {"min": 0, "max": 9, "step": 1}
        }
    ],
    "mental_math_examples": [
        {
            "index": 0,
            "problem": "97 × 25",
            "decomposition": "(100 − 3) × 25",
            "explanation": "Break 97 into 100 − 3, then distribute: 100×25 − 3×25 = 2500 − 75 = 2425",
            "result": 2425
        },
        {
            "index": 1,
            "problem": "95 × 8",
            "decomposition": "(100 − 5) × 8",
            "explanation": "Break 95 into 100 − 5, then distribute: 100×8 − 5×8 = 800 − 40 = 760",
            "result": 760
        },
        {
            "index": 2,
            "problem": "104 × 15",
            "decomposition": "(100 + 4) × 15",
            "explanation": "Break 104 into 100 + 4, then distribute: 100×15 + 4×15 = 1500 + 60 = 1560",
            "result": 1560
        },
        {
            "index": 3,
            "problem": "49 × 50",
            "decomposition": "(50 − 1) × 50",
            "explanation": "Break 49 into 50 − 1, then distribute: 50×50 − 1×50 = 2500 − 50 = 2450",
            "result": 2450
        },
        {
            "index": 4,
            "problem": "998 × 7",
            "decomposition": "(1000 − 2) × 7",
            "explanation": "Break 998 into 1000 − 2, then distribute: 1000×7 − 2×7 = 7000 − 14 = 6986",
            "result": 6986
        }
    ],
    "concepts": [
        {
            "id": 1,
            "title": "Understanding the Distributive Property",
            "description": "The fundamental rule: multiplying a sum equals the sum of the individual products.",
            "key_insight": "The distributive property states: a × (b + c) = a × b + a × c. This means when you multiply a number by a sum, you can either: 1) Add first, then multiply, OR 2) Multiply each addend separately, then add the products. Both give the same answer!",
            "related_params": ["a", "b", "c"]
        },
        {
            "id": 2,
            "title": "Dot Array Visualization",
            "description": "Understanding distributive property through arranged dots in rows and columns.",
            "key_insight": "In dot array mode, you see 'a' rows with (b + c) columns. The dots split into BLUE (a rows × b columns) and GREEN (a rows × c columns). Total dots = a × (b + c) = (a × b) + (a × c). Example: 3 rows of 10 dots (4 blue + 6 green) = 3×10 = 3×4 + 3×6 = 12 + 18 = 30 dots",
            "related_params": ["mode", "a", "b", "c"]
        },
        {
            "id": 3,
            "title": "Area Model Visualization",
            "description": "Understanding distributive property through rectangle areas divided into sections.",
            "key_insight": "In area model mode, a rectangle with height 'a' and width (b + c) splits into two smaller rectangles: BLUE area = a × b square units, GREEN area = a × c square units. Total area = a × (b + c) = (a × b) + (a × c). Example: A 4×9 rectangle splits into 4×5=20 blue squares plus 4×4=16 green squares = 36 total",
            "related_params": ["mode", "a", "b", "c"]
        },
        {
            "id": 4,
            "title": "Mental Math with Distributive Property",
            "description": "Using the distributive property to make multiplication easier by breaking numbers into friendlier parts.",
            "key_insight": "The distributive property enables mental math shortcuts! Break hard numbers into easy ones near multiples of 10, 100, or 1000. Example: 97×25 seems hard, but think '97 = 100 − 3', so 97×25 = (100−3)×25 = 100×25 − 3×25 = 2500 − 75 = 2425. Works with addition too: 104×15 = (100+4)×15 = 1500 + 60 = 1560",
            "related_params": ["mode", "mentalMathIndex"]
        },
        {
            "id": 5,
            "title": "Distributive Property with Subtraction",
            "description": "The distributive property works with subtraction too: a × (b − c) = a × b − a × c",
            "key_insight": "Subtraction distributes just like addition! When you have a × (b − c), multiply both parts: a × b minus a × c. Example: 5 × (9 − 2) = 5 × 9 − 5 × 2 = 45 − 10 = 35. This is the same as 5 × 7 = 35. The property works whether you add or subtract inside the brackets",
            "related_params": ["mode", "mentalMathIndex"]
        },
        {
            "id": 6,
            "title": "Why It Works - The Mathematical Reason",
            "description": "Understanding why the distributive property is always true.",
            "key_insight": "Imagine buying 'a' bags, each containing 'b' red candies and 'c' blue candies. Total candies = a × (b + c). But you could also count: red candies = a × b, blue candies = a × c, then add them. It's the same total! The property works because multiplication represents repeated addition, and order doesn't matter in addition",
            "related_params": ["a", "b", "c"]
        }
    ]
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
            "challenge": "Can you make the pendulum swing slower? Apply what you learned about how pendulum characteristics affect its motion.",
            "target_parameters": ["length"],
            "success_rule": {
                "conditions": [],  # No hard conditions, just optimize
                "optimization_target": {
                    "parameter": "length",
                    "objective": "maximize"  # Make it as long as possible for slowest swings
                },
                "tolerances": {
                    "perfect": 0.15,  # Within 15% of maximum
                    "partial": 0.35   # Within 35% of maximum
                },
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                }
            },
            "hints": {
                "attempt_1": "Think about what makes a pendulum swing slower. Which parameter affects the time period?",
                "attempt_2": "Remember from our lesson: longer pendulums take more time per swing. Try significantly increasing the length.",
                "attempt_3": "Make the pendulum much longer - try a high length value to achieve a slower swing."
            },
            "concept_reminder": "The time period of a pendulum depends on its length. A longer pendulum swings slower (longer time period), while a shorter pendulum swings faster (shorter time period)."
        },
        {
            "id": "pendulum_q2",
            "challenge": "Set the pendulum to complete exactly 5 oscillations. Can you make it swing as fast as possible while counting 5 swings?",
            "target_parameters": ["number_of_oscillations", "length"],
            "success_rule": {
                "conditions": [
                    {"parameter": "number_of_oscillations", "operator": "==", "value": 5}
                ],
                "optimization_target": {
                    "parameter": "length",
                    "objective": "minimize"  # Make it as short as possible for fastest swings
                },
                "tolerances": {
                    "perfect": 0.15,  # Within 15% of optimal (min value)
                    "partial": 0.35   # Within 35% of optimal
                },
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                }
            },
            "hints": {
                "attempt_1": "You need to set the number of oscillations to exactly 5, and make the pendulum swing quickly.",
                "attempt_2": "Remember: shorter pendulums swing faster! Try reducing the length significantly while keeping oscillations at 5.",
                "attempt_3": "Set oscillations to exactly 5 and make the length very short for the fastest swings."
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
    ],
    
    "angle_sum_property": [
        {
            "id": "angle_q1",
            "challenge": "Show the geometric proof! Enable the proof visualization to understand why triangle angles always sum to 180 degrees.",
            "target_parameters": ["show_proof_lines"],
            "success_rule": {
                "conditions": [
                    {"parameter": "show_proof_lines", "operator": "==", "value": True}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.0,
                    "wrong": 0.0
                },
                "thresholds": {
                    "perfect": {"show_proof_lines": True}
                }
            },
            "hints": {
                "attempt_1": "You need to enable the proof visualization. Look for the control to show the proof steps.",
                "attempt_2": "The proof uses a parallel line through the top vertex. Try turning on the proof display.",
                "attempt_3": "Set 'Show Proof Steps' to true to reveal the parallel line and alternate angles that prove the angle sum property."
            },
            "concept_reminder": "The parallel line proof shows that the three angles of a triangle can be rearranged at one vertex to form a straight line (180°), using the property of alternate interior angles formed by parallel lines."
        },
        {
            "id": "angle_q2",
            "challenge": "Verify the angle sum property yourself! Change the triangle shape and observe that the angle sum always remains 180 degrees, no matter what.",
            "target_parameters": ["vertexA_y", "vertexC_x"],
            "success_rule": {
                "conditions": [
                    {"parameter": "vertexA_y", "operator": "!=", "value": 150},
                    {"parameter": "vertexC_x", "operator": "!=", "value": 800}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"any_changed": True}
                }
            },
            "hints": {
                "attempt_1": "Try moving the triangle vertices to create a different shape. Does the angle sum still equal 180°?",
                "attempt_2": "Change the position of vertex A or vertex C to make a different triangle. The angle sum should remain constant.",
                "attempt_3": "Adjust any vertex position to verify that triangle angles always sum to 180° regardless of the shape."
            },
            "concept_reminder": "The angle sum property is universal for all triangles. No matter if it's equilateral, isosceles, scalene, acute, or obtuse - the interior angles always add up to exactly 180 degrees."
        }
    ],
    
    "parallel_lines_angles": [
        {
            "id": "parallel_q1",
            "challenge": "The obtuse angle ∠6 (blue, bottom-left) needs to be exactly 125°. Calculate the transversal angle needed and set it. Remember: acute + obtuse = 180°",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 53},
                    {"parameter": "angle", "operator": "<=", "value": 57}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 55},
                    "partial": {"angle": 54}
                }
            },
            "hints": {
                "attempt_1": "∠6 is an obtuse angle. If the obtuse angle is 125°, what must the acute angle be?",
                "attempt_2": "Use the formula: acute angle = 180° - obtuse angle. Calculate: 180° - 125° = ?",
                "attempt_3": "The acute angle (transversal angle) = 180° - 125° = 55°. Set the transversal to 55°."
            },
            "concept_reminder": "At any intersection, acute and obtuse angles are supplementary (sum to 180°). If you know one, you can calculate the other."
        },
        {
            "id": "parallel_q2",
            "challenge": "In a real-world measurement, you found ∠1 (red, top-right) to be 42°. Since ∠1 and ∠5 are corresponding angles and must be equal, set the transversal to match this measurement.",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 40},
                    {"parameter": "angle", "operator": "<=", "value": 44}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 42},
                    "partial": {"angle": 41}
                }
            },
            "hints": {
                "attempt_1": "∠1 is an acute angle (red color). What is the relationship between ∠1 and the transversal angle?",
                "attempt_2": "∠1 IS the acute angle at the top intersection. The acute angle equals the transversal angle directly.",
                "attempt_3": "Since ∠1 = 42° and ∠1 is acute, simply set the transversal to 42°."
            },
            "concept_reminder": "Corresponding angles (like ∠1 and ∠5) are in the same position at each intersection and are always equal when lines are parallel."
        },
        {
            "id": "parallel_q3",
            "challenge": "You need the obtuse angle ∠4 (orange, top-right) to be exactly 138°. Calculate what the transversal angle should be and set it.",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 40},
                    {"parameter": "angle", "operator": "<=", "value": 44}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 42},
                    "partial": {"angle": 41}
                }
            },
            "hints": {
                "attempt_1": "∠4 is an obtuse angle (orange color). How do you find the acute angle from an obtuse angle?",
                "attempt_2": "Calculate: acute angle = 180° - obtuse angle = 180° - 138° = ?",
                "attempt_3": "The calculation gives: 180° - 138° = 42°. Set the transversal to 42°."
            },
            "concept_reminder": "Obtuse angles and their adjacent acute angles are supplementary. Knowing one lets you calculate the other using: acute = 180° - obtuse."
        },
        {
            "id": "parallel_q4",
            "challenge": "Co-interior angles ∠3 and ∠6 always sum to 180°. If you need ∠3 (green, top-left) to be 67°, what transversal angle achieves this? Set it!",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 65},
                    {"parameter": "angle", "operator": "<=", "value": 69}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 67},
                    "partial": {"angle": 66}
                }
            },
            "hints": {
                "attempt_1": "First, determine: Is ∠3 an acute angle or an obtuse angle? Look at the color coding.",
                "attempt_2": "∠3 (green) is an ACUTE angle. The acute angles equal the transversal angle directly.",
                "attempt_3": "Since ∠3 is acute and needs to be 67°, set the transversal to 67°. Then ∠6 will be 180° - 67° = 113°."
            },
            "concept_reminder": "Co-interior angles are on the same side of the transversal, between parallel lines. They always sum to 180° (supplementary)."
        },
        {
            "id": "parallel_q5",
            "challenge": "Alternate interior angles ∠4 and ∠6 are always equal. If ∠4 (orange, obtuse) needs to be 152°, calculate the required transversal angle. This requires two steps!",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 26},
                    {"parameter": "angle", "operator": "<=", "value": 30}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 28},
                    "partial": {"angle": 27}
                }
            },
            "hints": {
                "attempt_1": "∠4 is obtuse (orange). If ∠4 = 152°, what is the acute angle at that intersection?",
                "attempt_2": "Step 1: Calculate acute angle = 180° - 152° = 28°. The transversal angle equals the acute angle.",
                "attempt_3": "The transversal angle is 28°. This makes ∠4 = 152° and ∠6 = 152° (they're alternate interior angles)."
            },
            "concept_reminder": "Alternate interior angles are on opposite sides of the transversal, between the parallel lines. They are always equal, regardless of being acute or obtuse."
        }
    ]
}

# ═══════════════════════════════════════════════════════════════════════
# INTERACTIVE ANGLE SUM PROPERTY QUIZ QUESTIONS
# ═══════════════════════════════════════════════════════════════════════

QUIZ_QUESTIONS["angle_sum_interactive"] = [
    {
        "id": "angle_sum_q1",
        "challenge": "Create a right triangle! Set angle B (blue) to exactly 90 degrees. Remember: the angles must still sum to 180°!",
        "target_parameters": ["angleB"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleB", "operator": ">=", "value": 88},
                {"parameter": "angleB", "operator": "<=", "value": 92}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"angleB_min": 89, "angleB_max": 91},
                "partial": {"angleB_min": 88, "angleB_max": 92}
            }
        },
        "hints": {
            "attempt_1": "To make a right angle (90°) at point B, change angle B to 90°. A right triangle has one 90° angle!",
            "attempt_2": "Set angle B = 90. The other two angles will automatically adjust to maintain the 180° sum.",
            "attempt_3": "Try setting angle B to exactly 90 degrees. You can also adjust angles A or C, and B will recalculate."
        },
        "concept_reminder": "A right triangle has one angle equal to 90 degrees. The other two angles must be acute and add up to 90° (since all three must sum to 180°). This creates special angle relationships useful in trigonometry!"
    },
    {
        "id": "angle_sum_q2",
        "challenge": "If angle A is 45° and angle C is 65°, what should angle B be? Calculate it first, then set the angles to create this triangle. Check your mental math!",
        "target_parameters": ["angleA", "angleC"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleA", "operator": ">=", "value": 43},
                {"parameter": "angleA", "operator": "<=", "value": 47},
                {"parameter": "angleC", "operator": ">=", "value": 63},
                {"parameter": "angleC", "operator": "<=", "value": 67}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"angleA_min": 44, "angleA_max": 46, "angleC_min": 64, "angleC_max": 66},
                "partial": {"angleA_min": 43, "angleA_max": 47, "angleC_min": 63, "angleC_max": 67}
            }
        },
        "hints": {
            "attempt_1": "First, calculate: If A = 45° and C = 65°, then B = 180° - 45° - 65° = ?",
            "attempt_2": "The answer is B = 70°. Now set angle A = 45° and angle C = 65°. Angle B will automatically become 70°!",
            "attempt_3": "Set angleA to 45 degrees and angleC to 65 degrees. Watch angle B update to 70° automatically."
        },
        "concept_reminder": "To find an unknown angle in a triangle: subtract the two known angles from 180°. This is one of the most useful applications of the angle sum property in geometry problems!"
    },
    {
        "id": "angle_sum_q3",
        "challenge": "Create an obtuse triangle! An obtuse triangle has ONE angle greater than 90°. Make angle C (green) the obtuse angle - set it to around 120°.",
        "target_parameters": ["angleC"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleC", "operator": ">=", "value": 115},
                {"parameter": "angleC", "operator": "<=", "value": 125}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"angleC_min": 118, "angleC_max": 122},
                "partial": {"angleC_min": 115, "angleC_max": 125}
            }
        },
        "hints": {
            "attempt_1": "An obtuse angle is greater than 90°. Set angle C to a value larger than 90°, like 120°.",
            "attempt_2": "Try setting angle C = 120. Watch how angles A and B automatically adjust to keep the sum at 180°.",
            "attempt_3": "Set angleC to 120 degrees. The triangle will reshape to show an obtuse angle at vertex C."
        },
        "concept_reminder": "An obtuse triangle has one angle > 90° (obtuse) and two angles < 90° (acute). The two acute angles must be small enough that all three still sum to 180°. Notice how the other angles get smaller as C becomes larger!"
    },
    {
        "id": "angle_sum_q4",
        "challenge": "Create an isosceles triangle where two angles are equal! Make angles A and C both approximately 50°. What will angle B be?",
        "target_parameters": ["angleA", "angleC"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleA", "operator": ">=", "value": 48},
                {"parameter": "angleA", "operator": "<=", "value": 52},
                {"parameter": "angleC", "operator": ">=", "value": 48},
                {"parameter": "angleC", "operator": "<=", "value": 52}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"angleA_min": 49, "angleA_max": 51, "angleC_min": 49, "angleC_max": 51},
                "partial": {"angleA_min": 48, "angleA_max": 52, "angleC_min": 48, "angleC_max": 52}
            }
        },
        "hints": {
            "attempt_1": "Isosceles triangles have two equal angles. You need A and C both around 50°. If A = C = 50°, what must B be?",
            "attempt_2": "Calculate: If A = 50° and C = 50°, then B = 180° - 50° - 50° = 80°. Set angleA = 50 and angleC = 50.",
            "attempt_3": "Set angleA to 50 degrees and angleC to 50 degrees. Watch angle B automatically become 80°!"
        },
        "concept_reminder": "Isosceles triangles have two equal sides and two equal angles. The equal angles are opposite the equal sides. This creates beautiful symmetry and is very common in geometry!"
    },
    {
        "id": "angle_sum_q5",
        "challenge": "Make the triangle as 'flat' as possible! Create a very flat triangle where one angle is very small (less than 20°). How do the other angles change?",
        "target_parameters": ["angleA"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleA", "operator": "<=", "value": 20}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"angleA_max": 15},
                "partial": {"angleA_max": 20}
            }
        },
        "hints": {
            "attempt_1": "To make a flat triangle, set angle A to a very small value like 15°. Watch how angles B and C adjust!",
            "attempt_2": "Try setting angle A to 10 degrees. The other two angles will become very large to maintain the 180° sum.",
            "attempt_3": "Set angleA to a value between 10-15 degrees. This creates a flat triangle with a tiny angle at vertex A."
        },
        "concept_reminder": "When a triangle becomes very flat, one angle becomes very small (approaching 0°), and the other two angles become very large (approaching 180° total). This demonstrates how angles adjust to maintain the 180° sum no matter what!"
    },
    {
        "id": "angle_sum_q6",
        "challenge": "Advanced challenge! Create a triangle where all three angles are different but close to each other - get each angle between 55° and 65°. Can you balance them?",
        "target_parameters": ["angleA", "angleB"],
        "success_rule": {
            "conditions": [
                {"parameter": "angleA", "operator": ">=", "value": 55},
                {"parameter": "angleA", "operator": "<=", "value": 65},
                {"parameter": "angleB", "operator": ">=", "value": 55},
                {"parameter": "angleB", "operator": "<=", "value": 65},
                {"parameter": "angleC", "operator": ">=", "value": 55},
                {"parameter": "angleC", "operator": "<=", "value": 65}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"all_between_55_65": True},
                "partial": {"all_between_50_70": True}
            }
        },
        "hints": {
            "attempt_1": "If all three angles are about equal (around 60° each), you'd have an equilateral triangle. Aim for angles close to 60°.",
            "attempt_2": "Try setting angle A = 60° and angle B = 60°. Angle C will automatically become 60° too!",
            "attempt_3": "Set angleA to 60 and angleB to 60 for a perfect equilateral triangle where all angles equal 60°."
        },
        "concept_reminder": "When all three angles are equal (60° each), you have an equilateral triangle - the most symmetric triangle. This happens when all three sides are also equal in length. It's the perfect balance!"
    }
]

QUIZ_QUESTIONS["speed_race"] = [
    {
        "id": "speed_q1",
        "challenge": "Make the cyclist finish the 1 km race in exactly 3 minutes (180 seconds). What speed should the cyclist have?",
        "target_parameters": ["speedCyclist"],
        "success_rule": {
            "conditions": [
                {"parameter": "speedCyclist", "operator": ">=", "value": 19},
                {"parameter": "speedCyclist", "operator": "<=", "value": 21}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            },
            "thresholds": {
                "perfect": {"speedCyclist_min": 19.5, "speedCyclist_max": 20.5},
                "partial": {"speedCyclist_min": 18, "speedCyclist_max": 22}
            }
        },
        "hints": {
            "attempt_1": "Think about the formula: Time = Distance ÷ Speed, so Speed = Distance ÷ Time. Distance is 1 km, time is 3 minutes = 0.05 hours.",
            "attempt_2": "Convert 3 minutes to hours: 3/60 = 0.05 hours. Then Speed = 1 km ÷ 0.05 hours = 20 km/h.",
            "attempt_3": "Set speedCyclist to 20 km/h. At this speed, the cyclist covers 1 km in exactly 3 minutes (180 seconds)."
        },
        "concept_reminder": "To find speed when you know distance and time: Speed = Distance ÷ Time. Remember to keep units consistent - if distance is in km and time in hours, speed will be in km/h. 3 minutes = 0.05 hours, so 1 km ÷ 0.05 hours = 20 km/h."
    },
    {
        "id": "speed_q2",
        "challenge": "Set the speeds so that the car finishes exactly twice as fast as the cyclist. If the cyclist is at 20 km/h, what should the car's speed be?",
        "target_parameters": ["speedCyclist", "speedCar"],
        "success_rule": {
            "conditions": [
                {"parameter": "speedCyclist", "operator": ">=", "value": 18},
                {"parameter": "speedCyclist", "operator": "<=", "value": 22},
                {"parameter": "speedCar", "operator": ">=", "value": 36},
                {"parameter": "speedCar", "operator": "<=", "value": 44}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"speedCyclist_min": 19, "speedCyclist_max": 21, "speedCar_min": 38, "speedCar_max": 42},
                "partial": {"speedCyclist_min": 18, "speedCyclist_max": 22, "speedCar_min": 35, "speedCar_max": 45}
            }
        },
        "hints": {
            "attempt_1": "If the car finishes twice as fast, it takes half the time. To take half the time for the same distance, the car must go twice as fast.",
            "attempt_2": "Twice as fast means double the speed. If cyclist = 20 km/h, then car = 2 × 20 = 40 km/h.",
            "attempt_3": "Set speedCyclist to 20 and speedCar to 40. The car's speed is double, so it finishes in half the time!"
        },
        "concept_reminder": "When speed doubles, time halves (for the same distance). If you want to finish twice as fast, you need to go twice as fast. This inverse relationship is key: Time = Distance ÷ Speed."
    },
    {
        "id": "speed_q3",
        "challenge": "Make all four racers finish within a 10-second window of each other. Set their speeds close enough so the race is very tight!",
        "target_parameters": ["speedWalker", "speedCyclist", "speedCar", "speedTrain"],
        "success_rule": {
            "conditions": [
                {"parameter": "speedWalker", "operator": ">=", "value": 95},
                {"parameter": "speedWalker", "operator": "<=", "value": 105},
                {"parameter": "speedCyclist", "operator": ">=", "value": 95},
                {"parameter": "speedCyclist", "operator": "<=", "value": 105},
                {"parameter": "speedCar", "operator": ">=", "value": 95},
                {"parameter": "speedCar", "operator": "<=", "value": 105},
                {"parameter": "speedTrain", "operator": ">=", "value": 95},
                {"parameter": "speedTrain", "operator": "<=", "value": 105}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            },
            "thresholds": {
                "perfect": {"all_between_98_102": True},
                "partial": {"all_between_95_105": True}
            }
        },
        "hints": {
            "attempt_1": "For a very close race, all speeds should be nearly equal. Try setting all four speeds to similar values around 100 km/h.",
            "attempt_2": "Set all speeds close to 100 km/h - perhaps 98, 99, 100, and 101. Small speed differences = small time differences!",
            "attempt_3": "Set speedWalker=98, speedCyclist=99, speedCar=100, speedTrain=101. All speeds are within 3 km/h, making for a very tight race!"
        },
        "concept_reminder": "When speeds are close, finish times are close! Small differences in speed create small differences in time. At 100 km/h, 1 km takes 36 seconds. At 99 km/h, it takes 36.4 seconds - only 0.4 seconds difference!"
    },
    {
        "id": "speed_q4",
        "challenge": "Make the walker finish the 1 km race in under 6 minutes. What's the minimum speed needed?",
        "target_parameters": ["speedWalker"],
        "success_rule": {
            "conditions": [
                {"parameter": "speedWalker", "operator": ">=", "value": 10}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"speedWalker_min": 10},
                "partial": {"speedWalker_min": 9.5}
            }
        },
        "hints": {
            "attempt_1": "6 minutes = 0.1 hours. To cover 1 km in 0.1 hours, the speed must be at least 1 km ÷ 0.1 hours = 10 km/h.",
            "attempt_2": "The walker needs to go at least 10 km/h to finish in 6 minutes or less. Try setting speedWalker to 10.",
            "attempt_3": "Set speedWalker to 10 km/h. At this speed, the walker covers 1 km in exactly 6 minutes (360 seconds)."
        },
        "concept_reminder": "To find the minimum speed needed for a certain time: Speed = Distance ÷ Time. For 1 km in 6 minutes (0.1 hours), speed must be at least 1 ÷ 0.1 = 10 km/h. Faster speeds mean even shorter times!"
    }
]

# =============================================================================
# TIME UNITS QUIZ QUESTIONS
# =============================================================================
QUIZ_QUESTIONS["time_units"] = [
    {
        "id": "time_q1",
        "challenge": "Convert 5 minutes into seconds. Enter 5 as the time value and select 'minutes' as the unit to see the conversion.",
        "target_parameters": ["timeValue", "timeUnit"],
        "success_rule": {
            "conditions": [
                {"parameter": "timeValue", "operator": ">=", "value": 4.5},
                {"parameter": "timeValue", "operator": "<=", "value": 5.5},
                {"parameter": "timeUnit", "operator": "==", "value": "min"}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"timeValue_min": 4.9, "timeValue_max": 5.1, "timeUnit": "min"},
                "partial": {"timeValue_min": 4.5, "timeValue_max": 5.5, "timeUnit": "min"}
            }
        },
        "hints": {
            "attempt_1": "Set the time value to 5 and choose 'minutes' from the dropdown. The converter will show you the equivalent in seconds.",
            "attempt_2": "Remember: 1 minute = 60 seconds. So 5 minutes = 5 × 60 = 300 seconds.",
            "attempt_3": "Set timeValue to 5 and timeUnit to 'min'. Look at the seconds result - it should show 300 seconds!"
        },
        "concept_reminder": "To convert minutes to seconds, multiply by 60. Each minute contains 60 seconds. So 5 minutes = 5 × 60 = 300 seconds."
    },
    {
        "id": "time_q2",
        "challenge": "How many hours are in 7200 seconds? Enter 7200 as the time value and select 'seconds' to find out.",
        "target_parameters": ["timeValue", "timeUnit"],
        "success_rule": {
            "conditions": [
                {"parameter": "timeValue", "operator": ">=", "value": 7000},
                {"parameter": "timeValue", "operator": "<=", "value": 7400},
                {"parameter": "timeUnit", "operator": "==", "value": "s"}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"timeValue_min": 7150, "timeValue_max": 7250, "timeUnit": "s"},
                "partial": {"timeValue_min": 7000, "timeValue_max": 7400, "timeUnit": "s"}
            }
        },
        "hints": {
            "attempt_1": "Set the time value to 7200 and choose 'seconds' from the dropdown. Look at the hours result.",
            "attempt_2": "To convert seconds to hours: divide by 3600 (since 1 hour = 3600 seconds). 7200 ÷ 3600 = 2 hours.",
            "attempt_3": "Set timeValue to 7200 and timeUnit to 's'. The hours display should show 2.00 hours!"
        },
        "concept_reminder": "To convert seconds to hours, divide by 3600. Since 1 hour = 60 minutes and 1 minute = 60 seconds, 1 hour = 60 × 60 = 3600 seconds. So 7200 seconds = 7200 ÷ 3600 = 2 hours."
    },
    {
        "id": "time_q3",
        "challenge": "Express 2.5 hours in milliseconds. Set the time value to 2.5 hours and observe the millisecond conversion.",
        "target_parameters": ["timeValue", "timeUnit"],
        "success_rule": {
            "conditions": [
                {"parameter": "timeValue", "operator": ">=", "value": 2.3},
                {"parameter": "timeValue", "operator": "<=", "value": 2.7},
                {"parameter": "timeUnit", "operator": "==", "value": "h"}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"timeValue_min": 2.4, "timeValue_max": 2.6, "timeUnit": "h"},
                "partial": {"timeValue_min": 2.3, "timeValue_max": 2.7, "timeUnit": "h"}
            }
        },
        "hints": {
            "attempt_1": "Set the time value to 2.5 and select 'hours' from the dropdown. Check the milliseconds result.",
            "attempt_2": "1 hour = 3600 seconds, and 1 second = 1000 milliseconds. So 1 hour = 3,600,000 milliseconds. Therefore, 2.5 hours = 2.5 × 3,600,000 = 9,000,000 milliseconds.",
            "attempt_3": "Set timeValue to 2.5 and timeUnit to 'h'. The converter shows 9,000,000 ms (9 million milliseconds)!"
        },
        "concept_reminder": "To convert hours to milliseconds: multiply by 3,600,000 (1 hour = 3600 seconds, and 1 second = 1000 ms). So 2.5 hours = 2.5 × 3,600,000 = 9,000,000 milliseconds."
    },
    {
        "id": "time_q4",
        "challenge": "Olympic sprinters finish the 100m race in about 10 seconds. How many milliseconds is that? Enter 10 seconds to find out.",
        "target_parameters": ["timeValue", "timeUnit"],
        "success_rule": {
            "conditions": [
                {"parameter": "timeValue", "operator": ">=", "value": 9.5},
                {"parameter": "timeValue", "operator": "<=", "value": 10.5},
                {"parameter": "timeUnit", "operator": "==", "value": "s"}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"timeValue_min": 9.8, "timeValue_max": 10.2, "timeUnit": "s"},
                "partial": {"timeValue_min": 9.5, "timeValue_max": 10.5, "timeUnit": "s"}
            }
        },
        "hints": {
            "attempt_1": "Set the time value to 10 and select 'seconds' as the unit. Check the milliseconds result.",
            "attempt_2": "Each second contains 1000 milliseconds. So 10 seconds = 10 × 1000 = 10,000 milliseconds.",
            "attempt_3": "Set timeValue to 10 and timeUnit to 's'. The result shows 10,000 milliseconds - Olympic races are decided by milliseconds!"
        },
        "concept_reminder": "1 second = 1000 milliseconds. This is why Olympic sprint times are often measured to the thousandth of a second (milliseconds) - because races are so close! 10 seconds = 10,000 milliseconds."
    }
]

# =============================================================================
# SPEED CALCULATOR QUIZ QUESTIONS
# =============================================================================
QUIZ_QUESTIONS["speed_calculator"] = [
    {
        "id": "calc_q1",
        "challenge": "A car travels 150 km in 3 hours. Calculate the speed by setting calculationMode to 'speed', distance to 150, and time to 3.",
        "target_parameters": ["calculationMode", "distance", "time"],
        "success_rule": {
            "conditions": [
                {"parameter": "calculationMode", "operator": "==", "value": "speed"},
                {"parameter": "distance", "operator": ">=", "value": 145},
                {"parameter": "distance", "operator": "<=", "value": 155},
                {"parameter": "time", "operator": ">=", "value": 2.8},
                {"parameter": "time", "operator": "<=", "value": 3.2}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"calculationMode": "speed", "distance_min": 148, "distance_max": 152, "time_min": 2.9, "time_max": 3.1},
                "partial": {"calculationMode": "speed", "distance_min": 145, "distance_max": 155, "time_min": 2.8, "time_max": 3.2}
            }
        },
        "hints": {
            "attempt_1": "Select 'Find Speed' mode, then set distance to 150 km and time to 3 hours. The calculator will show: Speed = 150 ÷ 3 = 50 km/h.",
            "attempt_2": "Speed = Distance ÷ Time. When distance is 150 km and time is 3 hours, speed = 150 ÷ 3 = 50 km/h.",
            "attempt_3": "Set calculationMode to 'speed', distance to 150, and time to 3. The result shows 50 km/h!"
        },
        "concept_reminder": "To find speed, divide distance by time. Speed = Distance ÷ Time. This tells us how many kilometers are covered per hour. 150 km ÷ 3 h = 50 km/h."
    },
    {
        "id": "calc_q2",
        "challenge": "A train travels at 80 km/h for 4 hours. Find the distance traveled by switching to 'Find Distance' mode with speed 80 and time 4.",
        "target_parameters": ["calculationMode", "speed", "time"],
        "success_rule": {
            "conditions": [
                {"parameter": "calculationMode", "operator": "==", "value": "distance"},
                {"parameter": "speed", "operator": ">=", "value": 75},
                {"parameter": "speed", "operator": "<=", "value": 85},
                {"parameter": "time", "operator": ">=", "value": 3.8},
                {"parameter": "time", "operator": "<=", "value": 4.2}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"calculationMode": "distance", "speed_min": 78, "speed_max": 82, "time_min": 3.9, "time_max": 4.1},
                "partial": {"calculationMode": "distance", "speed_min": 75, "speed_max": 85, "time_min": 3.8, "time_max": 4.2}
            }
        },
        "hints": {
            "attempt_1": "Click 'Find Distance' tab, then set speed to 80 km/h and time to 4 hours. The formula is: Distance = Speed × Time.",
            "attempt_2": "Distance = Speed × Time. When speed is 80 km/h and time is 4 hours, distance = 80 × 4 = 320 km.",
            "attempt_3": "Set calculationMode to 'distance', speed to 80, and time to 4. The result shows 320 km!"
        },
        "concept_reminder": "To find distance, multiply speed by time. Distance = Speed × Time. If you travel at 80 km/h for 4 hours, you cover 80 × 4 = 320 km."
    },
    {
        "id": "calc_q3",
        "challenge": "You need to travel 360 km at a speed of 90 km/h. Calculate how long it will take by switching to 'Find Time' mode with distance 360 and speed 90.",
        "target_parameters": ["calculationMode", "distance", "speed"],
        "success_rule": {
            "conditions": [
                {"parameter": "calculationMode", "operator": "==", "value": "time"},
                {"parameter": "distance", "operator": ">=", "value": 350},
                {"parameter": "distance", "operator": "<=", "value": 370},
                {"parameter": "speed", "operator": ">=", "value": 85},
                {"parameter": "speed", "operator": "<=", "value": 95}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"calculationMode": "time", "distance_min": 355, "distance_max": 365, "speed_min": 88, "speed_max": 92},
                "partial": {"calculationMode": "time", "distance_min": 350, "distance_max": 370, "speed_min": 85, "speed_max": 95}
            }
        },
        "hints": {
            "attempt_1": "Click 'Find Time' tab, then set distance to 360 km and speed to 90 km/h. The formula is: Time = Distance ÷ Speed.",
            "attempt_2": "Time = Distance ÷ Speed. When distance is 360 km and speed is 90 km/h, time = 360 ÷ 90 = 4 hours.",
            "attempt_3": "Set calculationMode to 'time', distance to 360, and speed to 90. The result shows 4 hours!"
        },
        "concept_reminder": "To find time, divide distance by speed. Time = Distance ÷ Speed. At 90 km/h, covering 360 km takes 360 ÷ 90 = 4 hours."
    },
    {
        "id": "calc_q4",
        "challenge": "A cyclist wants to travel 60 km in exactly 2.5 hours. What speed is needed? Use 'Find Speed' mode with distance 60 and time 2.5.",
        "target_parameters": ["calculationMode", "distance", "time"],
        "success_rule": {
            "conditions": [
                {"parameter": "calculationMode", "operator": "==", "value": "speed"},
                {"parameter": "distance", "operator": ">=", "value": 58},
                {"parameter": "distance", "operator": "<=", "value": 62},
                {"parameter": "time", "operator": ">=", "value": 2.3},
                {"parameter": "time", "operator": "<=", "value": 2.7}
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"calculationMode": "speed", "distance_min": 59, "distance_max": 61, "time_min": 2.4, "time_max": 2.6},
                "partial": {"calculationMode": "speed", "distance_min": 58, "distance_max": 62, "time_min": 2.3, "time_max": 2.7}
            }
        },
        "hints": {
            "attempt_1": "Select 'Find Speed' mode, then set distance to 60 km and time to 2.5 hours. Speed = Distance ÷ Time.",
            "attempt_2": "Speed = 60 km ÷ 2.5 hours = 24 km/h. The cyclist needs to maintain 24 km/h to cover 60 km in 2.5 hours.",
            "attempt_3": "Set calculationMode to 'speed', distance to 60, and time to 2.5. The result shows 24 km/h!"
        },
        "concept_reminder": "To find required speed, divide distance by available time. Speed = Distance ÷ Time. To travel 60 km in 2.5 hours, you need: 60 ÷ 2.5 = 24 km/h."
    }
]

# =============================================================================
# SIMPLE PENDULUM NEW - QUIZ QUESTIONS
# =============================================================================
QUIZ_QUESTIONS["simple_pendulum_new"] = [
    {
        "id": "pendulum_q1",
        "challenge": "Set the pendulum length to 150 cm and observe the time period. Notice how the time period increases with length.",
        "target_parameters": ["length"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": ">=", "value": 145},
                {"parameter": "length", "operator": "<=", "value": 155}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"length_min": 148, "length_max": 152},
                "partial": {"length_min": 145, "length_max": 155}
            }
        },
        "hints": {
            "attempt_1": "Use the 'String Length' slider to adjust the length to 150 cm. Watch the time period value update.",
            "attempt_2": "Move the slider on the left side labeled 'String Length' until the display shows 150 cm.",
            "attempt_3": "Set length to 150 cm. The time period will be approximately 2.47 seconds (calculated from T = 2π√(L/g))."
        },
        "concept_reminder": "The time period of a pendulum increases with length. A longer string means slower oscillations. The formula is T = 2π√(L/g), where L is length."
    },
    {
        "id": "pendulum_q2",
        "challenge": "Now change the bob mass to 150 g (keeping length at 150 cm). Notice that the time period DOES NOT change! This proves mass doesn't affect the period.",
        "target_parameters": ["length", "mass"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": ">=", "value": 145},
                {"parameter": "length", "operator": "<=", "value": 155},
                {"parameter": "mass", "operator": ">=", "value": 145},
                {"parameter": "mass", "operator": "<=", "value": 155}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"length_min": 148, "length_max": 152, "mass_min": 148, "mass_max": 152},
                "partial": {"length_min": 145, "length_max": 155, "mass_min": 145, "mass_max": 155}
            }
        },
        "hints": {
            "attempt_1": "Keep length at 150 cm, then use the 'Bob Mass' slider to set mass to 150 g. Observe that time period stays the same!",
            "attempt_2": "Use the right slider (Bob Mass) to change mass to 150 g. The time period won't change because mass doesn't appear in the formula T = 2π√(L/g).",
            "attempt_3": "Set mass to 150 g while keeping length at 150 cm. This demonstrates the key principle: time period is independent of mass!"
        },
        "concept_reminder": "Time period depends ONLY on length, NOT on mass! The formula T = 2π√(L/g) has no mass term. Heavy and light bobs swing at the same rate if length is the same."
    },
    {
        "id": "pendulum_q3",
        "challenge": "Now set the pendulum length to 50 cm (minimum) and observe how the time period decreases. Shorter pendulum = faster oscillations.",
        "target_parameters": ["length"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": ">=", "value": 50},
                {"parameter": "length", "operator": "<=", "value": 55}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"length_min": 50, "length_max": 52},
                "partial": {"length_min": 50, "length_max": 55}
            }
        },
        "hints": {
            "attempt_1": "Move the 'String Length' slider all the way to the left to set it to 50 cm (the minimum value).",
            "attempt_2": "Set length to 50 cm. You'll see the time period is much shorter now - about 1.43 seconds compared to 2.47 seconds at 150 cm.",
            "attempt_3": "Drag the length slider to 50 cm. Notice the faster oscillations and shorter time period!"
        },
        "concept_reminder": "Shorter pendulums have shorter time periods (faster oscillations). The relationship is T = 2π√(L/g), so T is proportional to √L."
    },
    {
        "id": "pendulum_q4",
        "challenge": "Set length to 200 cm (maximum) to see the longest time period. This demonstrates the square root relationship between length and period.",
        "target_parameters": ["length"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": ">=", "value": 195},
                {"parameter": "length", "operator": "<=", "value": 200}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"length_min": 199, "length_max": 200},
                "partial": {"length_min": 195, "length_max": 200}
            }
        },
        "hints": {
            "attempt_1": "Move the 'String Length' slider all the way to the right to set it to 200 cm (the maximum value).",
            "attempt_2": "Set length to 200 cm. The time period will be approximately 2.85 seconds - the longest possible in this simulation.",
            "attempt_3": "Drag the length slider to maximum (200 cm). Notice the very slow oscillations!"
        },
        "concept_reminder": "The longest pendulum (200 cm) has the longest time period. Length and period follow T = 2π√(L/g). Doubling length increases period by √2 ≈ 1.41 times."
    }
]

# =============================================================================
# BRACKETS & SIGN RULES - QUIZ QUESTIONS
# =============================================================================
QUIZ_QUESTIONS["brackets_signs"] = [
    {
        "id": "brackets_q1",
        "challenge": "Let's start by examining a basic case where MINUS comes before the bracket. Look at the first example (200 − (40 + 3)) which shows how signs flip.",
        "target_parameters": ["mode", "problemIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "learn"},
                {"parameter": "problemIndex", "operator": "==", "value": 0}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "learn", "problemIndex": 0},
                "partial": {"mode": "learn"}
            }
        },
        "hints": {
            "attempt_1": "Make sure you're in 'Learn' mode (not Quiz mode) and the slider or presets show the first example: 200 − (40 + 3).",
            "attempt_2": "Click the 'Learn' tab at the top if you're in Quiz mode. The first example demonstrates the minus-before-bracket rule.",
            "attempt_3": "Set mode to 'learn' and select problem 0 (the first example). This shows: 200 − (40 + 3) = 200 − 40 − 3 = 157."
        },
        "concept_reminder": "When MINUS comes before the bracket, all signs inside FLIP: +40 becomes −40, +3 becomes −3. This is the fundamental rule of bracket removal."
    },
    {
        "id": "brackets_q2",
        "challenge": "Now examine example 4 (28 + (35 − 10)) which shows the PLUS-before-bracket case. Notice how signs STAY THE SAME when there's a plus before the bracket.",
        "target_parameters": ["mode", "problemIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "learn"},
                {"parameter": "problemIndex", "operator": "==", "value": 3}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "learn", "problemIndex": 3},
                "partial": {"mode": "learn"}
            }
        },
        "hints": {
            "attempt_1": "Stay in Learn mode and select example 4 (the slider should be at position 3, or click the '28 + (35 − 10)' preset button).",
            "attempt_2": "Use the 'Expression' slider to move to problem 4 (position 3 on the slider: 0, 1, 2, 3...). Or click the preset button showing this expression.",
            "attempt_3": "Problem index 3 shows: 28 + (35 − 10) = 28 + 35 − 10 = 53. Plus before bracket means signs stay the same!"
        },
        "concept_reminder": "When PLUS comes before the bracket, signs inside STAY THE SAME: just remove the brackets. +35 stays +35, −10 stays −10."
    },
    {
        "id": "brackets_q3",
        "challenge": "Look at the tricky case in example 2 (500 − (250 − 100)). This shows why understanding sign flipping is crucial: both signs flip, so −100 becomes +100!",
        "target_parameters": ["mode", "problemIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "learn"},
                {"parameter": "problemIndex", "operator": "==", "value": 1}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "learn", "problemIndex": 1},
                "partial": {"mode": "learn"}
            }
        },
        "hints": {
            "attempt_1": "Select example 2 (problem index 1) in Learn mode. This is the classic case: 500 − (250 − 100).",
            "attempt_2": "Move the slider to position 1, or click the '500 − (250 − 100)' preset button.",
            "attempt_3": "Problem 1 shows: 500 − (250 − 100) = 500 − 250 + 100 = 350. Because of the minus before bracket, +250→−250 AND −100→+100!"
        },
        "concept_reminder": "Subtracting a difference requires careful attention: the minus before bracket flips BOTH signs. This is why −100 becomes +100 (you need to add back what you over-subtracted)."
    },
    {
        "id": "brackets_q4",
        "challenge": "Now test your understanding! Switch to Quiz mode and try answering the multiple choice questions. This will help solidify your knowledge of bracket removal rules.",
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "quiz"}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            },
            "thresholds": {
                "perfect": {"mode": "quiz"},
                "partial": {}
            }
        },
        "hints": {
            "attempt_1": "Click the 'Quiz' tab at the top of the simulation to switch from Learn mode to Quiz mode.",
            "attempt_2": "Look for the mode tabs near the top - click 'Quiz' to enter quiz mode where you can test yourself.",
            "attempt_3": "Switch to Quiz mode by clicking the Quiz tab. You'll get multiple choice questions to practice bracket removal!"
        },
        "concept_reminder": "Quiz mode tests your understanding with random questions. Remember: MINUS before bracket → signs FLIP; PLUS before bracket → signs STAY."
    }
]

# =============================================================================
# DISTRIBUTIVE PROPERTY - QUIZ QUESTIONS
# =============================================================================
QUIZ_QUESTIONS["distributive"] = [
    {
        "id": "distributive_q1",
        "challenge": "Let's explore the dot array visualization. Set mode to 'dots' with a=2, b=3, c=5. Count the blue and green dots to see how they add up to the total.",
        "target_parameters": ["mode", "a", "b", "c"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "dots"},
                {"parameter": "a", "operator": "==", "value": 2},
                {"parameter": "b", "operator": "==", "value": 3},
                {"parameter": "c", "operator": "==", "value": 5}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "dots", "a": 2, "b": 3, "c": 5},
                "partial": {"mode": "dots"}
            }
        },
        "hints": {
            "attempt_1": "Click the 'Dot Array' tab, then set the sliders: a (rows) = 2, b (blue columns) = 3, c (green columns) = 5.",
            "attempt_2": "You should see 2 rows with 3 blue dots and 5 green dots in each row. That's 2×(3+5) = 2×8 = 16 dots total!",
            "attempt_3": "Set a=2, b=3, c=5 in Dot Array mode. You'll see: 2×3 = 6 blue dots, 2×5 = 10 green dots, total = 16 dots. This shows 2×(3+5) = 2×3 + 2×5."
        },
        "concept_reminder": "The dot array shows how a×(b+c) splits visually: 'a' rows of 'b' blue dots plus 'a' rows of 'c' green dots. Total = a×b + a×c."
    },
    {
        "id": "distributive_q2",
        "challenge": "Switch to 'area' mode to see the same concept as a rectangle split into two colored sections. Keep a=2, b=3, c=5 to see the area model.",
        "target_parameters": ["mode", "a", "b", "c"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "area"},
                {"parameter": "a", "operator": "==", "value": 2},
                {"parameter": "b", "operator": "==", "value": 3},
                {"parameter": "c", "operator": "==", "value": 5}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "area", "a": 2, "b": 3, "c": 5},
                "partial": {"mode": "area"}
            }
        },
        "hints": {
            "attempt_1": "Click the 'Area Model' tab while keeping a=2, b=3, c=5. You'll see a rectangle divided into blue and green sections.",
            "attempt_2": "The area model shows a 2×8 rectangle split into: blue section (2×3=6 squares) + green section (2×5=10 squares) = 16 total.",
            "attempt_3": "Switch to Area Model mode. The rectangle has height 2 and width 8 (3+5), with blue area=6 and green area=10. Same distributive property, different visualization!"
        },
        "concept_reminder": "The area model demonstrates that a rectangle of dimensions a × (b+c) equals the sum of two rectangles: a×b plus a×c. Both visualizations prove the same algebraic truth."
    },
    {
        "id": "distributive_q3",
        "challenge": "Now try a larger example to see the pattern holds. Set a=4, b=6, c=7 in either dots or area mode. Notice how the blue and green parts add up correctly.",
        "target_parameters": ["a", "b", "c"],
        "success_rule": {
            "conditions": [
                {"parameter": "a", "operator": "==", "value": 4},
                {"parameter": "b", "operator": "==", "value": 6},
                {"parameter": "c", "operator": "==", "value": 7}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.7,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"a": 4, "b": 6, "c": 7},
                "partial": {"a": 4}
            }
        },
        "hints": {
            "attempt_1": "Set the sliders to a=4, b=6, c=7. This gives you 4×(6+7) = 4×13 = 52 total.",
            "attempt_2": "You should see: blue part = 4×6 = 24, green part = 4×7 = 28, total = 52. The equation is 4×(6+7) = 4×6 + 4×7.",
            "attempt_3": "With a=4, b=6, c=7, the visualization shows 52 dots or 52 square units: 24 blue + 28 green. This demonstrates the distributive property with larger numbers."
        },
        "concept_reminder": "The distributive property works for any numbers, not just small ones! Whether 2×(3+5) or 4×(6+7), the rule a×(b+c) = a×b + a×c always holds."
    },
    {
        "id": "distributive_q4",
        "challenge": "Let's explore mental math! Switch to 'mental' mode and select the first example (97 × 25) to see how distributive property makes hard multiplication easier.",
        "target_parameters": ["mode", "mentalMathIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "mental"},
                {"parameter": "mentalMathIndex", "operator": "==", "value": 0}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "mental", "mentalMathIndex": 0},
                "partial": {"mode": "mental"}
            }
        },
        "hints": {
            "attempt_1": "Click the 'Mental Math' tab, then select the first button showing '97×25'.",
            "attempt_2": "97×25 seems hard, but 97 = 100 − 3, so we can compute: (100−3)×25 = 100×25 − 3×25 = 2500 − 75 = 2425!",
            "attempt_3": "Select mental math example 0 (97×25). The steps show decomposition into (100−3)×25, then distribution: 2500 − 75 = 2425."
        },
        "concept_reminder": "Mental math uses distributive property to break hard numbers into easy ones. 97 is close to 100, so we compute with 100 and subtract the difference. This is the power of a×(b−c) = a×b − a×c!"
    },
    {
        "id": "distributive_q5",
        "challenge": "Try another mental math example: 104 × 15 (example index 2). This one uses ADDITION instead of subtraction. See how 104 = 100 + 4 makes it easier.",
        "target_parameters": ["mode", "mentalMathIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "mental"},
                {"parameter": "mentalMathIndex", "operator": "==", "value": 2}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "mental", "mentalMathIndex": 2},
                "partial": {"mode": "mental"}
            }
        },
        "hints": {
            "attempt_1": "In Mental Math mode, click the third button showing '104×15' (that's index 2: the examples go 0, 1, 2...).",
            "attempt_2": "104 = 100 + 4, so: (100+4)×15 = 100×15 + 4×15 = 1500 + 60 = 1560. Much easier than multiplying 104×15 directly!",
            "attempt_3": "Select example 2 (104×15). The decomposition shows (100+4)×15 = 1500 + 60 = 1560. This demonstrates a×(b+c) = a×b + a×c with real numbers."
        },
        "concept_reminder": "The distributive property works with both addition and subtraction! 104 is slightly over 100, so we add the extra: (100+4)×15 = 100×15 + 4×15."
    },
    {
        "id": "distributive_q6",
        "challenge": "Test your understanding! Switch to Quiz mode to answer questions about filling in missing operators and numbers in distributive equations.",
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "quiz"}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            },
            "thresholds": {
                "perfect": {"mode": "quiz"},
                "partial": {}
            }
        },
        "hints": {
            "attempt_1": "Click the 'Quiz' tab at the top to switch to quiz mode and test yourself with multiple choice questions.",
            "attempt_2": "Quiz mode will ask you to fill in missing operators (+, −, ×) or numbers. Use what you learned from the visualizations!",
            "attempt_3": "Switch to Quiz mode to practice. Remember: when you distribute over addition, use +; when you distribute over subtraction, use −."
        },
        "concept_reminder": "The quiz tests whether you understand: 1) What operator to use when distributing (+ or −), 2) Which number distributes to each term, 3) How to decompose numbers for mental math."
    },
    {
        "id": "distributive_q7",
        "challenge": "Back to dot array mode: try setting a=3, b=4, c=4 to see a symmetrical pattern where the blue and green parts are equal.",
        "target_parameters": ["mode", "a", "b", "c"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "dots"},
                {"parameter": "a", "operator": "==", "value": 3},
                {"parameter": "b", "operator": "==", "value": 4},
                {"parameter": "c", "operator": "==", "value": 4}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "dots", "a": 3, "b": 4, "c": 4},
                "partial": {"mode": "dots", "b": 4, "c": 4}
            }
        },
        "hints": {
            "attempt_1": "Go back to Dot Array mode and set a=3, b=4, c=4. You'll see equal numbers of blue and green dots.",
            "attempt_2": "With b=c=4, you get 3×4 = 12 blue dots and 3×4 = 12 green dots. Total = 24 dots. Notice the symmetry!",
            "attempt_3": "Set a=3, b=4, c=4. This shows 3×(4+4) = 3×8 = 24, which equals 3×4 + 3×4 = 12 + 12. When b=c, the parts are equal!"
        },
        "concept_reminder": "When b equals c, the distributive property shows: a×(b+c) = a×b + a×c = a×b + a×b = 2×(a×b). This is a special symmetric case."
    },
    {
        "id": "distributive_q8",
        "challenge": "Explore the most complex mental math example: 998 × 7 (example index 4). This uses a very large decomposition: 998 = 1000 − 2.",
        "target_parameters": ["mode", "mentalMathIndex"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "mental"},
                {"parameter": "mentalMathIndex", "operator": "==", "value": 4}
            ],
            "logic": "ALL"
        },
        "scoring": {
            "weights": {
                "perfect": 1.0,
                "partial": 0.6,
                "wrong": 0.3
            },
            "thresholds": {
                "perfect": {"mode": "mental", "mentalMathIndex": 4},
                "partial": {"mode": "mental"}
            }
        },
        "hints": {
            "attempt_1": "In Mental Math mode, click the last button (fifth one) showing '998×7'. That's example index 4.",
            "attempt_2": "998 is very close to 1000, so: 998 = 1000 − 2. Then (1000−2)×7 = 1000×7 − 2×7 = 7000 − 14 = 6986!",
            "attempt_3": "Select example 4 (998×7). Decomposition: (1000−2)×7 = 7000 − 14 = 6986. This shows how powerful the distributive property is for mental calculation!"
        },
        "concept_reminder": "Even with very large numbers, the distributive property makes mental math possible. 998×7 looks hard, but thinking '1000−2' makes it: 7000 − 14 = 6986. Simple!"
    }
]
    
    # ═══════════════════════════════════════════════════════════════════════
    # ANGLE SUM PROPERTY SIMULATION (in SIMULATIONS dict above)
    # ═══════════════════════════════════════════════════════════════════════

SIMULATIONS["angle_sum_property"] = {
    "title": "Triangle Angle Sum",
    "file": "simulations/AngleSumProperty.html",
    "description": """
An interactive triangle simulation where you can drag vertices to change 
the triangle's shape and observe that the sum of interior angles always 
equals 180 degrees. Includes a geometric proof using parallel lines.

What can be demonstrated:
- Triangle interior angles sum to 180°
- Angle sum remains constant regardless of triangle shape
- Geometric proof using parallel lines and alternate angles
- Relationship between triangle angles and parallel line properties
""",
    "cannot_demonstrate": [
        "Exterior angles",
        "Triangle area calculations",
        "Side length relationships",
        "Pythagorean theorem"
    ],
    "initial_params": {
        "vertexA_x": 500,
        "vertexA_y": 150,
        "vertexB_x": 200,
        "vertexB_y": 450,
        "vertexC_x": 800,
        "vertexC_y": 450,
        "show_proof_lines": False
    },
    "parameter_info": {
        "show_proof_lines": {
            "label": "Show Proof Steps",
            "range": "true/false",
            "url_key": "show_proof_lines",
            "effect": "Shows parallel line through vertex A and demonstrates alternate angles proof"
        },
        "vertexA_x": {
            "label": "Vertex A X Position",
            "range": "50-950 pixels",
            "url_key": "vertexA_x",
            "effect": "Horizontal position of top vertex A"
        },
        "vertexA_y": {
            "label": "Vertex A Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexA_y",
            "effect": "Vertical position of top vertex A"
        },
        "vertexB_x": {
            "label": "Vertex B X Position",
            "range": "50-950 pixels",
            "url_key": "vertexB_x",
            "effect": "Horizontal position of bottom-left vertex B"
        },
        "vertexB_y": {
            "label": "Vertex B Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexB_y",
            "effect": "Vertical position of bottom-left vertex B"
        },
        "vertexC_x": {
            "label": "Vertex C X Position",
            "range": "50-950 pixels",
            "url_key": "vertexC_x",
            "effect": "Horizontal position of bottom-right vertex C"
        },
        "vertexC_y": {
            "label": "Vertex C Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexC_y",
            "effect": "Vertical position of bottom-right vertex C"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Triangle Angle Sum Property",
            "description": "The sum of the three interior angles in any triangle is always 180 degrees, regardless of the triangle's shape or size.",
            "key_insight": "No matter how you change the triangle shape, angle A + angle B + angle C always equals 180°",
            "related_params": ["vertexA_x", "vertexA_y", "vertexB_x", "vertexB_y", "vertexC_x", "vertexC_y"]
        },
        {
            "id": 2,
            "title": "Parallel Lines and Alternate Angles",
            "description": "When a line intersects two parallel lines, it creates alternate interior angles that are equal. This property helps prove the angle sum theorem.",
            "key_insight": "A line parallel to the base through vertex A creates alternate angles equal to angles B and C",
            "related_params": ["show_proof_lines"]
        },
        {
            "id": 3,
            "title": "Geometric Proof Visualization",
            "description": "The parallel line proof shows that all three angles can be rearranged at one vertex to form a straight line (180°), proving the angle sum property.",
            "key_insight": "When you show the proof, angles B and C appear at vertex A as alternate angles, and together with angle A, they form a straight line",
            "related_params": ["show_proof_lines"]
        }
    ]
}

# ═══════════════════════════════════════════════════════════════════════
# INTERACTIVE ANGLE SUM PROPERTY SIMULATION (New Version)
# ═══════════════════════════════════════════════════════════════════════

SIMULATIONS["angle_sum_interactive"] = {
    "title": "Interactive Triangle Angles",
    "file": "simulations/angle-sum-property.html",
    "description": """
A modern, touch-friendly interactive simulation where you drag point C to 
reshape the triangle and observe in real-time how the three angles change 
while their sum remains constant at 180°. Features live angle displays, 
visual angle arcs, and instant feedback.

What can be demonstrated:
- Triangle interior angles always sum to 180°
- Real-time angle measurement as you reshape the triangle
- Visual representation of each angle with color-coded arcs
- Angle sum property holds for all triangle types (acute, right, obtuse)
- Interactive discovery of angle relationships
""",
    "cannot_demonstrate": [
        "Exterior angles",
        "Triangle inequality theorem",
        "Side length relationships",
        "Area calculations",
        "Parallel line proof method"
    ],
    "initial_params": {
        "angleA": 60,
        "angleB": 60,
        "angleC": 60,
        "autoInteract": False
    },
    "parameter_info": {
        "angleA": {
            "label": "Angle A",
            "range": "10-170 degrees",
            "url_key": "angleA",
            "effect": "The angle at vertex A (top vertex, shown in red). Adjusting this reshapes the triangle while maintaining the 180° sum."
        },
        "angleB": {
            "label": "Angle B",
            "range": "10-170 degrees",
            "url_key": "angleB",
            "effect": "The angle at vertex B (left vertex, shown in blue). Adjusting this reshapes the triangle while maintaining the 180° sum."
        },
        "angleC": {
            "label": "Angle C",
            "range": "10-170 degrees",
            "url_key": "angleC",
            "effect": "The angle at vertex C (draggable vertex, shown in green). This is automatically calculated to ensure angles sum to 180°."
        },
        "autoInteract": {
            "label": "Auto Show Discovery",
            "range": "true/false",
            "url_key": "autoInteract",
            "effect": "If true, shows the discovery message immediately without requiring interaction"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Triangle Angle Sum is Always 180°",
            "description": "The fundamental property that the three interior angles of any triangle always sum to exactly 180 degrees, regardless of the triangle's shape or size.",
            "key_insight": "No matter how you change the angles, angle A + angle B + angle C = 180° always",
            "related_params": ["angleA", "angleB", "angleC"]
        },
        {
            "id": 2,
            "title": "Finding Unknown Angles",
            "description": "If you know any two angles in a triangle, you can always find the third angle by subtracting their sum from 180 degrees.",
            "key_insight": "Third angle = 180° - (first angle + second angle). This works for ALL triangles!",
            "related_params": ["angleA", "angleB", "angleC"]
        },
        {
            "id": 3,
            "title": "Triangle Types and Angles",
            "description": "Triangles can be classified by their angles: acute (all angles < 90°), right (one angle = 90°), obtuse (one angle > 90°), but they all follow the 180° rule.",
            "key_insight": "Change the angles to create different triangle types - notice how they adjust to maintain the 180° sum",
            "related_params": ["angleA", "angleB", "angleC"]
        },
        {
            "id": 4,
            "title": "Angle Measurement and Visualization",
            "description": "Understanding how angles are measured at each vertex and how they relate to the triangle's overall shape.",
            "key_insight": "Each colored arc shows the angle at that vertex - red for A, blue for B, green for C",
            "related_params": ["angleA", "angleB", "angleC"]
        }
    ]
}


def get_quiz_questions(simulation_id: str) -> list:
    """Get quiz questions for a specific simulation."""
    return QUIZ_QUESTIONS.get(simulation_id, [])
