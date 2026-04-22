"""
Simulations Configuration - Kannada (ಕನ್ನಡ)
=============================================
Contains metadata, parameters, concepts, and quiz questions for
Kannada-medium simulations designed for native-language learners.

These simulations have their UI, labels, and instructions written in Kannada.
The agent pipeline continues to operate in English for consistent evaluation;
the translation layer handles student-facing communication in Kannada.

Each entry follows the EXACT same structure as simulations_config.py so that
all existing helper functions (get_simulation, get_quiz_questions, etc.) work
transparently after this file is merged at runtime.

This file is imported and merged into simulations_config.py at the bottom of
that file via:
    from simulations_config_kannada import SIMULATIONS_KN, QUIZ_QUESTIONS_KN
    SIMULATIONS.update(SIMULATIONS_KN)
    QUIZ_QUESTIONS.update(QUIZ_QUESTIONS_KN)
"""

# ═══════════════════════════════════════════════════════════════════════
# KANNADA SIMULATION DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

SIMULATIONS_KN = {}


# =============================================================================
# INDUSTRIAL WASTE TREATMENT SIMULATION
# ಕೈಗಾರಿಕಾ ತ್ಯಾಜ್ಯ ಚಿಕಿತ್ಸೆ – ನಮ್ಮ ನೀರನ್ನು ರಕ್ಷಿಸುವುದು
# Science Chapter 2 – Acids, Bases and Salts (Neutralization)
# =============================================================================
SIMULATIONS_KN["industrial_waste_treatment_kn"] = {
    "title": "ಕೈಗಾರಿಕಾ ತ್ಯಾಜ್ಯ ಚಿಕಿತ್ಸೆ (Industrial Waste Treatment)",

    # Mark as Kannada so the sidebar can group it separately
    "language": "kannada",

    # Relative path from the project root — matches the folder structure
    "file": "simulations_kannada/science_chapter2_simulation10_industrial_waste_treatment_kn.html",

    "description": """
An interactive Kannada-language simulation demonstrating how acidic industrial
waste must be neutralised with a base (alkali) before being discharged into a river.

Students experience two contrasting scenarios:
- Releasing UNTREATED acidic waste (pH 3) directly into the river
  → fish die, water turns dark, status: disaster (ಅನಾಹುತ)
- NEUTRALISING the acidic waste with alkali (pH rises to 7) before release
  → river stays clean, fish survive, status: safe (ಸುರಕ್ಷಿತ)

The simulation teaches:
- Neutralisation reaction: acid + base → salt + water
- pH scale: acidic (pH 3) vs neutral (pH 7) vs safe water
- Environmental responsibility: mandatory waste treatment before discharge
- Real-world connection: factory regulations requiring effluent treatment

The simulation UI, labels, and narrative are entirely in Kannada for native
language learners. Driving parameters are exposed via URL query strings so
the teaching agent can set the demonstration state directly.
""",

    "cannot_demonstrate": [
        "Specific balanced chemical equations for neutralisation",
        "Effect of alkaline (basic) waste on the river",
        "Intermediate partial-neutralisation pH states",
        "Multiple simultaneous acid-base scenarios",
        "Quantitative measurement of reagent amounts",
        "Any chemical other than a generic acid/alkali pair"
    ],

    # ── Agent-controllable parameters ──────────────────────────────────────
    # initialState : string  – controls which demonstration state to auto-load
    # showHints    : bool    – toggles the explanatory insight box in the UI
    "initial_params": {
        "initialState": "initial",
        "showHints": True
    },

    "parameter_info": {
        "initialState": {
            "label": "Simulation State",
            "range": "initial, polluted, treated",
            "url_key": "initialState",
            "effect": (
                "Sets which state the simulation auto-loads into on page open.\n"
                "  'initial'  → clean river, healthy fish, pH 7 (default starting view)\n"
                "  'polluted' → untreated acidic waste (pH 3) released; fish die, river darkens\n"
                "  'treated'  → acidic waste neutralised with alkali (pH → 7) before release; river safe"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the insight explanation box inside the simulation.\n"
                "  true  → show the 'Why treatment matters' explanation panel (default)\n"
                "  false → hide the explanation panel (cleaner view for focused observation)"
            )
        }
    },

    # ── Teaching concepts ───────────────────────────────────────────────────
    # 3 concepts in progression: problem → solution → broader understanding
    "concepts": [
        {
            "id": 1,
            "title": "Acidic Industrial Waste and Its Harm",
            "description": (
                "Understanding why untreated acidic industrial waste is dangerous to "
                "aquatic ecosystems and the living organisms that depend on rivers."
            ),
            "key_insight": (
                "Factory effluent is often strongly acidic (pH around 3). Discharging it "
                "untreated destroys the gills of fish and other aquatic life, killing them. "
                "A pH of 3 is 10,000 times more acidic than neutral water (pH 7)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Neutralisation: The Solution to Acidic Waste",
            "description": (
                "How adding a base (alkali) to acidic industrial waste chemically neutralises "
                "it — raising the pH to 7 so the water is safe to release into the river."
            ),
            "key_insight": (
                "Neutralisation reaction: Acid + Base → Salt + Water. "
                "Adding alkali (like lime / calcium hydroxide) to acidic factory waste "
                "converts it from pH 3 to pH 7 (neutral), making it safe for aquatic life."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Environmental Responsibility and pH",
            "description": (
                "How the pH scale measures acidity and alkalinity, and why environmental "
                "regulations require factories to treat their waste before discharge."
            ),
            "key_insight": (
                "pH 7 is neutral — the safe level for rivers and aquatic life. "
                "Factories are legally required to neutralise acidic waste before releasing it. "
                "This is a direct application of the acid-base neutralisation concept "
                "to real-world environmental protection."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════
# QUIZ QUESTIONS — KANNADA SIMULATIONS
# ═══════════════════════════════════════════════════════════════════════

QUIZ_QUESTIONS_KN = {}


# =============================================================================
# INDUSTRIAL WASTE TREATMENT — QUIZ QUESTIONS
# 3 questions: observe harm → show correct treatment → verify clean state
#
# Quiz parameters:
#   initialState (string): 'initial' | 'polluted' | 'treated'
#   The student selects from a dropdown in the Streamlit quiz UI.
#   The simulation iframe reflects the chosen state via URL param ?initialState=…
#   Evaluation uses string equality (handled by quiz_rules.py string fallback).
# =============================================================================

QUIZ_QUESTIONS_KN["industrial_waste_treatment_kn"] = [

    # ── Q1: Show the HARMFUL scenario ──────────────────────────────────────
    {
        "id": "waste_kn_q1",
        "challenge": (
            "Show what happens when acidic industrial waste is released into the "
            "river WITHOUT any treatment. Set the simulation to demonstrate the "
            "harmful effect of untreated acid discharge on the river and fish.\n\n"
            "(ಚಿಕಿತ್ಸೆ ಇಲ್ಲದ ಆಮ್ಲೀಯ ತ್ಯಾಜ್ಯ ನದಿಗೆ ಬಿಟ್ಟರೆ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "polluted"
                }
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            }
        },
        "hints": {
            "attempt_1": (
                "Use the dropdown in Streamlit to select 'polluted' as the Simulation State. "
                "This will show the untreated acidic waste (pH 3) being released into the "
                "river — watch what happens to the fish."
            ),
            "attempt_2": (
                "Set 'initialState' to 'polluted'. The simulation will show: waste flows in, "
                "river turns dark, fish die. This is the result of uncontrolled acid discharge."
            ),
            "attempt_3": (
                "Select 'polluted' from the Simulation State dropdown. "
                "You will see the disaster scenario: acidic waste (pH 3) kills the fish "
                "by destroying their gills."
            )
        },
        "concept_reminder": (
            "Untreated acidic industrial waste has a very low pH (around 3). "
            "When released directly into rivers, the acid destroys fish gills and kills "
            "aquatic life. This is why factories must NEVER discharge untreated effluent. "
            "(ಅನಾಹುತ! ಚಿಕಿತ್ಸೆ ಇಲ್ಲದ ಆಮ್ಲೀಯ ತ್ಯಾಜ್ಯ ಮೀನುಗಳನ್ನು ಸಾಯಿಸುತ್ತದೆ!)"
        )
    },

    # ── Q2: Show the CORRECT treatment scenario ────────────────────────────
    {
        "id": "waste_kn_q2",
        "challenge": (
            "Now show the CORRECT procedure: demonstrate how proper neutralisation "
            "treatment makes the waste safe before it enters the river. "
            "Set the simulation to show the treated outcome.\n\n"
            "(ಸರಿಯಾದ ಚಿಕಿತ್ಸೆ ಮಾಡಿದ ನಂತರ ನೀರು ಸುರಕ್ಷಿತವಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "treated"
                }
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            }
        },
        "hints": {
            "attempt_1": (
                "Select 'treated' from the Simulation State dropdown. "
                "This shows neutralisation in action: alkali is added to the acidic waste, "
                "raising pH from 3 to 7 (neutral), making the water safe for aquatic life."
            ),
            "attempt_2": (
                "Set 'initialState' to 'treated'. You will see the correct procedure: "
                "first the waste is released (acidic), then alkali is added for neutralisation "
                "(acid + base → salt + water), and finally the river stays clean."
            ),
            "attempt_3": (
                "Choose 'treated' as the Simulation State. "
                "The treated scenario shows: alkali neutralises the acid, pH becomes 7, "
                "fish survive, river remains clean — the success of proper waste management."
            )
        },
        "concept_reminder": (
            "Neutralisation: Acid + Base → Salt + Water. "
            "Adding alkali (base) to acidic industrial waste brings the pH from 3 to 7 "
            "(neutral). Water at pH 7 is safe for fish and aquatic life. "
            "This is the core of industrial effluent treatment. "
            "(ಯಶಸ್ಸು! ಕ್ಷಾರ ಸೇರಿಸಿ ತಟಸ್ಥೀಕರಣ ಮಾಡಿದ ನೀರು pH 7 ಆಗಿ ಸುರಕ್ಷಿತವಾಗುತ್ತದೆ!)"
        )
    },

    # ── Q3: Identify the clean baseline ────────────────────────────────────
    {
        "id": "waste_kn_q3",
        "challenge": (
            "Show the INITIAL clean state of the river — before any industrial "
            "discharge occurs. This represents the healthy ecosystem that proper "
            "waste management protects.\n\n"
            "(ಯಾವುದೇ ತ್ಯಾಜ್ಯ ಬಿಡುಗಡೆ ಮೊದಲು ನದಿಯ ಸ್ಥಿತಿ ಹೇಗಿರುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "initial"
                }
            ],
            "scoring": {
                "perfect": 1.0,
                "partial": 0.5,
                "wrong": 0.2
            }
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' from the Simulation State dropdown. "
                "This shows the starting state: a clean river at pH 7 with healthy fish "
                "— the natural state that waste treatment is designed to preserve."
            ),
            "attempt_2": (
                "Set 'initialState' to 'initial'. You will see the clean river before "
                "any factory discharge. Notice the pH is already 7 (neutral) and fish are "
                "swimming healthily."
            ),
            "attempt_3": (
                "Choose 'initial' to display the pristine river (pH 7, healthy fish). "
                "This is the ecosystem we must protect through mandatory waste treatment."
            )
        },
        "concept_reminder": (
            "A healthy river ecosystem has a pH of around 7 (neutral). "
            "Fish and aquatic organisms can only survive within a narrow pH range close to 7. "
            "Industrial waste treatment ensures that discharge maintains this safe pH, "
            "protecting aquatic biodiversity and water quality. "
            "(ಆರೋಗ್ಯಕರ ನದಿ pH 7 ಇರುತ್ತದೆ — ಮೀನುಗಳಿಗೆ ಮತ್ತು ಜಲಚರ ಜೀವಿಗಳಿಗೆ ಸುರಕ್ಷಿತ.)"
        )
    }
]


# =============================================================================
# TURMERIC INDICATOR SIMULATION
# ಹಲ್ದಿ ಸೂಚಕ – ಕ್ಷಾರ ಮಾತ್ರ ಗುರುತಿಸುವ ಭಾಗಶಃ ಸೂಚಕ
# Science Chapter 2 – Natural Indicators (partial indicator concept)
# =============================================================================
SIMULATIONS_KN["turmeric_indicator_kn"] = {
    "title": "ಹಲ್ದಿ ಸೂಚಕ (Turmeric Indicator)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation5_turmeric_indicator_kn.html",
    "description": (
        "Kannada simulation: students test household solutions on turmeric paper and "
        "observe that turmeric turns red/brown ONLY with bases. Both acids and neutral "
        "substances leave it yellow — making turmeric a PARTIAL indicator."
    ),
    "cannot_demonstrate": [
        "Distinguishing acids from neutral substances (turmeric stays yellow for both)",
        "Quantitative pH measurement"
    ],
    "initial_params": {"initialState": "basic", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Solution Type",
            "range": "acidic, basic, neutral",
            "url_key": "initialState",
            "effect": (
                "Selects a solution and auto-runs the turmeric test.\n"
                "  'acidic'  → lemon juice — turmeric stays yellow (no change)\n"
                "  'basic'   → soap solution — turmeric turns red/brown\n"
                "  'neutral' → tap water — turmeric stays yellow (same as acid!)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight box and limitation box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Turmeric Detects Bases: Turns Red or Brown",
            "description": (
                "Turmeric paper turns red/reddish-brown when it contacts a basic solution. "
                "Curcumin (the yellow pigment) changes structure in alkaline environments."
            ),
            "key_insight": (
                "Bases turn turmeric RED/BROWN. Soap, baking soda, and lime water all "
                "cause this colour change. The stronger the base, the deeper the red."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Turmeric Cannot Distinguish Acids from Neutral Substances",
            "description": (
                "Unlike litmus, turmeric stays yellow with BOTH acids and neutral substances. "
                "It is therefore a PARTIAL indicator — it can only confirm a base."
            ),
            "key_insight": (
                "Turmeric is PARTIAL: base → red/brown, acid/neutral → yellow. "
                "If turmeric stays yellow, you cannot tell whether the substance is acidic "
                "or neutral without a different test."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Real-World: Soap Stains on Turmeric Fabric Turn Red",
            "description": (
                "Soap (alkaline) reacts with turmeric stains on clothing producing "
                "a red/brown colour — the same reaction seen in the simulation."
            ),
            "key_insight": (
                "Soap is alkaline; curcumin on fabric reacts with the alkali and turns red. "
                "This is a real-world natural indicator showing acid-base behaviour."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["turmeric_indicator_kn"] = [
    {
        "id": "turmeric_q1",
        "challenge": (
            "Set the simulation to demonstrate what happens when a BASIC (alkaline) solution "
            "is added to turmeric paper. Show the characteristic colour change.\n\n"
            "(ಕ್ಷಾರ ದ್ರಾವಣ ಹಲ್ದಿ ಕಾಗದಕ್ಕೆ ಸೋಕಿದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' as the Simulation State — soap solution on turmeric produces a dramatic red/brown colour change.",
            "attempt_2": "Set 'initialState' to 'basic'. Curcumin reacts with alkaline solutions to turn red/brown.",
            "attempt_3": "Choose 'basic': soap turns turmeric red/brown — the definitive sign of a base."
        },
        "concept_reminder": (
            "Turmeric turns RED/BROWN with bases. Curcumin changes structure in alkaline conditions. "
            "Soap, baking soda, and lime water all produce this change. "
            "(ಕ್ಷಾರ ಹಲ್ದಿಯನ್ನು ಕೆಂಪಾಗಿಸುತ್ತದೆ!)"
        )
    },
    {
        "id": "turmeric_q2",
        "challenge": (
            "Show what happens when an ACIDIC solution is added to turmeric paper. "
            "Observe whether the colour changes — what does this reveal about turmeric as an indicator?\n\n"
            "(ಆಮ್ಲ ದ್ರಾವಣ ಹಲ್ದಿ ಕಾಗದಕ್ಕೆ ಸೋಕಿದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' — lemon juice on turmeric. Notice NO colour change occurs; turmeric stays yellow.",
            "attempt_2": "Set 'initialState' to 'acidic'. Turmeric stays yellow with acids — proving it is a partial indicator.",
            "attempt_3": "Choose 'acidic': turmeric stays yellow with lemon juice; acids do NOT trigger the colour change."
        },
        "concept_reminder": (
            "Turmeric stays YELLOW with acids — no change. "
            "This is turmeric's limitation: acids and neutral substances both leave it yellow. "
            "(ಆಮ್ಲ ಹಲ್ದಿಯನ್ನು ಹಳದಿ ಉಳಿಸುತ್ತದೆ — ಬದಲಾವಣೆ ಇಲ್ಲ!)"
        )
    },
    {
        "id": "turmeric_q3",
        "challenge": (
            "Show what happens with a NEUTRAL substance on turmeric paper. "
            "Explain why this makes turmeric a PARTIAL indicator.\n\n"
            "(ತಟಸ್ಥ ದ್ರಾವಣ ಹಲ್ದಿ ಕಾಗದಕ್ಕೆ ಸೋಕಿದಾಗ ಏನಾಗುತ್ತದೆ — ಹಲ್ದಿ ಯಾಕೆ ಭಾಗಶಃ ಸೂಚಕ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "neutral"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'neutral' — tap water on turmeric. It stays yellow, identical to the acid result.",
            "attempt_2": "Set 'initialState' to 'neutral'. Same yellow as an acid — making it impossible to distinguish them.",
            "attempt_3": "Choose 'neutral': tap water leaves turmeric yellow, same as an acid, proving turmeric cannot tell them apart."
        },
        "concept_reminder": (
            "Neutral substances leave turmeric YELLOW — same as acids. "
            "Turmeric is PARTIAL: confirms base (red/brown) but cannot separate acid from neutral. "
            "A COMPLETE indicator (litmus, rose extract) distinguishes all three types. "
            "(ಹಲ್ದಿ ಭಾಗಶಃ ಸೂಚಕ — ಕ್ಷಾರ ಮಾತ್ರ ಗುರುತಿಸಬಲ್ಲದು!)"
        )
    }
]


# =============================================================================
# RED ROSE INDICATOR SIMULATION
# ಕೆಂಪು ಗುಲಾಬಿ ಸೂಚಕ – ಪೂರ್ಣ ನೈಸರ್ಗಿಕ ಸೂಚಕ (ಆಮ್ಲ, ಕ್ಷಾರ, ತಟಸ್ಥ ಎಲ್ಲ ಗುರುತಿಸಬಲ್ಲದು)
# Science Chapter 2 – Natural Indicators (complete indicator)
# =============================================================================
SIMULATIONS_KN["red_rose_indicator_kn"] = {
    "title": "ಕೆಂಪು ಗುಲಾಬಿ ಸೂಚಕ (Red Rose Indicator)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation4_red_rose_indicator_kn.html",
    "description": (
        "Kannada simulation: students test household solutions with rose petal extract and "
        "observe three distinct colours — red (acid), green (base), pink (neutral). "
        "Rose extract is a COMPLETE indicator containing anthocyanins that respond to both "
        "acids and bases, unlike turmeric which only responds to bases."
    ),
    "cannot_demonstrate": [
        "Quantitative pH values",
        "Direct comparison with litmus paper side-by-side",
        "Effect of highly concentrated acids or bases"
    ],
    "initial_params": {"initialState": "acidic", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Solution Type",
            "range": "acidic, basic, neutral",
            "url_key": "initialState",
            "effect": (
                "Selects a solution and auto-runs the colour test.\n"
                "  'acidic'  → lemon juice — rose extract turns RED\n"
                "  'basic'   → soap solution — rose extract turns GREEN\n"
                "  'neutral' → tap water — rose extract stays PINK (no change)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Acids Turn Rose Extract Red",
            "description": (
                "Rose petal extract turns bright red when added to an acidic solution. "
                "H⁺ ions from the acid cause anthocyanin pigment to shift to its red form."
            ),
            "key_insight": (
                "Acids → rose extract turns RED. Lemon juice, vinegar, orange juice all "
                "produce this colour change. Easy identification of an acid."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Bases Turn Rose Extract Green",
            "description": (
                "Rose petal extract turns green when added to a basic (alkaline) solution. "
                "OH⁻ ions cause anthocyanin to shift to its green form."
            ),
            "key_insight": (
                "Bases → rose extract turns GREEN — the most striking change. "
                "Soap, baking soda, and lime water all produce green. "
                "Green is the exact opposite of the acid red."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Rose Extract is a Complete Indicator",
            "description": (
                "Unlike turmeric (partial), rose extract shows three distinct colours: "
                "red (acid), green (base), pink/unchanged (neutral)."
            ),
            "key_insight": (
                "Rose stays PINK with neutral substances. "
                "RED=acid, GREEN=base, PINK=neutral — three distinct results. "
                "This makes rose extract as powerful as litmus, using natural materials."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["red_rose_indicator_kn"] = [
    {
        "id": "rose_q1",
        "challenge": (
            "Show what colour change happens when an ACID is added to red rose petal extract. "
            "Set the simulation to demonstrate the acid colour response.\n\n"
            "(ಆಮ್ಲ ಸೇರಿಸಿದಾಗ ಗುಲಾಬಿ ಸಾರ ಯಾವ ಬಣ್ಣಕ್ಕೆ ಬದಲಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' as the Simulation State — lemon juice turns rose extract RED.",
            "attempt_2": "Set 'initialState' to 'acidic'. Anthocyanins shift to red form with H⁺ ions from acids.",
            "attempt_3": "Choose 'acidic': lemon juice turns rose extract RED — confirming it is an acid."
        },
        "concept_reminder": (
            "Acids turn rose extract RED. Anthocyanin reacts with H⁺ ions to produce red colour. "
            "Lemon, vinegar, orange juice all turn it red. "
            "(ಆಮ್ಲ ಗುಲಾಬಿ ಸಾರವನ್ನು ಕೆಂಪಾಗಿಸುತ್ತದೆ!)"
        )
    },
    {
        "id": "rose_q2",
        "challenge": (
            "Show what colour change happens when a BASE is added to red rose petal extract. "
            "Demonstrate the dramatic colour response that identifies a base.\n\n"
            "(ಕ್ಷಾರ ಸೇರಿಸಿದಾಗ ಗುಲಾಬಿ ಸಾರ ಯಾವ ಬಣ್ಣಕ್ಕೆ ಬದಲಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' — soap turns rose extract from pink to GREEN.",
            "attempt_2": "Set 'initialState' to 'basic'. OH⁻ ions from bases cause the striking green colour.",
            "attempt_3": "Choose 'basic': soap turns rose extract GREEN — confirming it is a base."
        },
        "concept_reminder": (
            "Bases turn rose extract GREEN — the most distinctive change. "
            "OH⁻ ions shift anthocyanin to green form. Soap, baking soda, lime water all go green. "
            "(ಕ್ಷಾರ ಗುಲಾಬಿ ಸಾರವನ್ನು ಹಸಿರಾಗಿಸುತ್ತದೆ!)"
        )
    },
    {
        "id": "rose_q3",
        "challenge": (
            "Show what happens with a NEUTRAL substance and explain why rose extract is a "
            "COMPLETE indicator (unlike turmeric, which is only partial).\n\n"
            "(ತಟಸ್ಥ ದ್ರಾವಣದೊಂದಿಗೆ ಏನಾಗುತ್ತದೆ, ಮತ್ತು ಗುಲಾಬಿ ಸಾರ ಪೂರ್ಣ ಸೂಚಕ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "neutral"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'neutral' — tap water leaves rose extract PINK; neutral substances cause no change.",
            "attempt_2": "Set 'initialState' to 'neutral'. Rose stays pink — three distinct colours, one per type = complete indicator.",
            "attempt_3": "Choose 'neutral': tap water keeps rose extract pink, confirming neutrals don't react with anthocyanins."
        },
        "concept_reminder": (
            "Neutral substances leave rose extract PINK (unchanged). "
            "RED=acid, GREEN=base, PINK=neutral — three distinct results makes it a COMPLETE indicator. "
            "Compare: turmeric stays yellow for BOTH acids and neutrals (partial). "
            "(ಗುಲಾಬಿ ಸಾರ ಪೂರ್ಣ ಸೂಚಕ: ಕೆಂಪು=ಆಮ್ಲ, ಹಸಿರು=ಕ್ಷಾರ, ಗುಲಾಬಿ=ತಟಸ್ಥ!)"
        )
    }
]


# =============================================================================
# PROPERTIES OF ACIDS AND BASES SIMULATION
# ಆಮ್ಲಗಳು ಮತ್ತು ಕ್ಷಾರಗಳ ಗುಣಗಳು – ಹೋಲಿಕೆ ಮಾಡಿ ಕಲಿಯಿರಿ
# Science Chapter 2 – Properties comparison with misconception correction
# =============================================================================
SIMULATIONS_KN["properties_acids_bases_kn"] = {
    "title": "ಆಮ್ಲ ಮತ್ತು ಕ್ಷಾರ ಗುಣಗಳು (Properties of Acids & Bases)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation3_properties_acids_bases_kn.html",
    "description": (
        "Kannada tab-based simulation comparing properties of acids vs bases. "
        "Two interactive panels show: acids (sour taste, blue litmus → red, corrosive) "
        "and bases (bitter/slippery, red litmus → blue). A substance quiz lets students "
        "classify common items. Key misconception: bitter taste ≠ necessarily a base "
        "(demonstrated via bitter gourd which is NOT a base)."
    ),
    "cannot_demonstrate": [
        "Quantitative pH values",
        "Chemical equations for reactions",
        "Neutralisation between acids and bases"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Panel to Show",
            "range": "initial, acids, bases",
            "url_key": "initialState",
            "effect": (
                "Controls which tab panel is active on load.\n"
                "  'initial' → loads with acids tab showing (default)\n"
                "  'acids'   → clicks the Acids tab showing acid properties\n"
                "  'bases'   → clicks the Bases tab showing base properties"
            )
        },
        "showHints": {
            "label": "Show Concept Card",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Properties of Acids",
            "description": (
                "Acids: sour taste, turn blue litmus red, can corrode metals. "
                "Examples: citric acid (lemon), acetic acid (vinegar), lactic acid (curd)."
            ),
            "key_insight": (
                "Key acid properties: (1) Sour taste. (2) Blue litmus → RED. (3) Corrosive. "
                "Acids release H⁺ ions in solution."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Properties of Bases",
            "description": (
                "Bases: bitter taste, soapy/slippery touch, turn red litmus blue. "
                "Examples: baking soda, soap, lime water, antacids."
            ),
            "key_insight": (
                "Key base properties: (1) Bitter taste. (2) Slippery/soapy touch — reacts with "
                "skin oils. (3) Red litmus → BLUE. Bases release OH⁻ ions in solution."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Misconception: Bitter Taste Does Not Always Mean Basic",
            "description": (
                "Bitter gourd tastes bitter but is NOT a base. "
                "Bitterness is a property of bases but not all bitter things are bases."
            ),
            "key_insight": (
                "Always use litmus or an indicator to confirm whether something is a base. "
                "Bitter gourd's bitterness comes from glucoside compounds, not from being alkaline. "
                "Test with litmus, not just taste."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["properties_acids_bases_kn"] = [
    {
        "id": "props_q1",
        "challenge": (
            "Navigate the simulation to show the PROPERTIES OF ACIDS panel. "
            "Explore the key characteristics that define acids.\n\n"
            "(ಆಮ್ಲಗಳ ಗುಣಗಳ ಪ್ಯಾನಲ್ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acids"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acids' as the Simulation State to activate the Acids panel — sour taste, blue litmus → red, and corrosive.",
            "attempt_2": "Set 'initialState' to 'acids'. The simulation clicks the acids tab and shows all three key acid properties.",
            "attempt_3": "Choose 'acids': the acids panel shows sour taste, litmus effect, and common examples."
        },
        "concept_reminder": (
            "Acids: (1) SOUR taste. (2) Blue litmus → RED. (3) Corrosive. "
            "Examples: citric acid (lemon), acetic acid (vinegar), lactic acid (curd). "
            "(ಆಮ್ಲ: ಹುಳಿ ರುಚಿ, ನೀಲಿ ಲಿಟ್ಮಸ್ → ಕೆಂಪು!)"
        )
    },
    {
        "id": "props_q2",
        "challenge": (
            "Show the PROPERTIES OF BASES panel. "
            "Explore how bases differ from acids in their characteristics.\n\n"
            "(ಕ್ಷಾರಗಳ ಗುಣಗಳ ಪ್ಯಾನಲ್ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "bases"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'bases' — the Bases panel shows bitter taste, slippery touch, and red litmus → blue.",
            "attempt_2": "Set 'initialState' to 'bases'. The bases tab shows all three key properties of bases.",
            "attempt_3": "Choose 'bases': bitter taste, soapy touch, and red litmus turning blue."
        },
        "concept_reminder": (
            "Bases: (1) BITTER taste. (2) SLIPPERY/SOAPY touch — reacts with skin oils. "
            "(3) Red litmus → BLUE. Examples: baking soda, soap, lime water. "
            "(ಕ್ಷಾರ: ಕಹಿ ರುಚಿ, ಜಾರುವ ಸ್ಪರ್ಶ, ಕೆಂಪು ಲಿಟ್ಮಸ್ → ನೀಲಿ!)"
        )
    },
    {
        "id": "props_q3",
        "challenge": (
            "Return to the INITIAL view. Reflect: what is the key litmus difference "
            "between acids and bases?\n\n"
            "(ಪ್ರಾರಂಭ ಸ್ಥಿತಿಗೆ ಹಿಂದಿರಿ ಮತ್ತು ಆಮ್ಲ-ಕ್ಷಾರ ಲಿಟ್ಮಸ್ ವ್ಯತ್ಯಾಸ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "initial"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'initial' to see the default acids tab view. Then reflect on both panels.",
            "attempt_2": "Set 'initialState' to 'initial'. The acids panel loads as the starting reference point.",
            "attempt_3": "Choose 'initial' to reset to the starting view where both tabs are available to compare."
        },
        "concept_reminder": (
            "Acids: Blue litmus → RED. Bases: Red litmus → BLUE. Neutrals: NEITHER changes. "
            "Also: bitter taste ≠ base (e.g. bitter gourd is NOT a base — test with litmus!). "
            "(ಆಮ್ಲ ↔ ಕ್ಷಾರ: ಎದುರು ಲಿಟ್ಮಸ್ ಕ್ರಿಯೆಗಳು!)"
        )
    }
]


# =============================================================================
# LITMUS INDICATOR SIMULATION
# ಲಿಟ್ಮಸ್ ಪೇಪರ್ ಪರೀಕ್ಷೆ – ಶಾಸ್ತ್ರೀಯ ಆಮ್ಲ-ಕ್ಷಾರ ಸೂಚಕ
# Science Chapter 2 – Litmus as the standard complete indicator
# =============================================================================
SIMULATIONS_KN["litmus_indicator_kn"] = {
    "title": "ಲಿಟ್ಮಸ್ ಕಾಗದ ಪರೀಕ್ಷೆ (Litmus Paper Test)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation2_litmus_indicator_kn.html",
    "description": (
        "Kannada simulation of the classic litmus paper test. Blue and red litmus papers "
        "are dipped simultaneously into a chosen solution. Students observe: acid = blue → red, "
        "base = red → blue, neutral = neither changes. Tests 9 common solutions. "
        "Litmus is a COMPLETE indicator derived from lichen."
    ),
    "cannot_demonstrate": [
        "Quantitative pH values",
        "Other indicator types (phenolphthalein, universal indicator)",
        "Concentration effects on colour intensity"
    ],
    "initial_params": {"initialState": "acidic", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Solution Type",
            "range": "acidic, basic, neutral",
            "url_key": "initialState",
            "effect": (
                "Selects a solution and auto-runs the litmus dip animation.\n"
                "  'acidic'  → lemon juice: blue paper turns RED, red unchanged\n"
                "  'basic'   → soap: red paper turns BLUE, blue unchanged\n"
                "  'neutral' → tap water: NEITHER paper changes colour"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Acids Turn Blue Litmus Red",
            "description": (
                "Blue litmus paper turns red in acidic solutions. "
                "H⁺ ions released by acids cause this colour change. "
                "Red litmus stays red in acids."
            ),
            "key_insight": (
                "Blue → RED in acids. This is the classic acid test. "
                "Lemon juice, vinegar, curd all turn blue litmus red."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Bases Turn Red Litmus Blue",
            "description": (
                "Red litmus paper turns blue in basic (alkaline) solutions. "
                "OH⁻ ions cause this colour change. Blue litmus stays blue in bases."
            ),
            "key_insight": (
                "Red → BLUE in bases. This is the classic base test. "
                "Soap, baking soda, lime water all turn red litmus blue."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Neutral Substances: No Change in Either Litmus",
            "description": (
                "Neither litmus paper changes in neutral solutions. "
                "Absence of change is itself a result."
            ),
            "key_insight": (
                "Neutral → NO change in either litmus. pH 7 means equal H⁺ and OH⁻. "
                "Three distinct outcomes make litmus a COMPLETE indicator."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["litmus_indicator_kn"] = [
    {
        "id": "litmus_q1",
        "challenge": (
            "Show the litmus paper test result for an ACID. Demonstrate what happens to "
            "both blue and red litmus papers in an acidic solution.\n\n"
            "(ಆಮ್ಲ ದ್ರಾವಣದಲ್ಲಿ ಲಿಟ್ಮಸ್ ಕಾಗದ ಮುಳುಗಿಸಿದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' — lemon juice used. Blue litmus turns red, red litmus stays unchanged.",
            "attempt_2": "Set 'initialState' to 'acidic'. Classic result: blue → RED confirms acid.",
            "attempt_3": "Choose 'acidic': lemon juice gives the acid result — BLUE turns RED."
        },
        "concept_reminder": (
            "Acids turn BLUE litmus RED. Red litmus stays unchanged. "
            "H⁺ ions from acids cause blue litmus to change to red. "
            "(ಆಮ್ಲ: ನೀಲಿ ಲಿಟ್ಮಸ್ → ಕೆಂಪು!)"
        )
    },
    {
        "id": "litmus_q2",
        "challenge": (
            "Show the litmus paper test result for a BASE. Demonstrate what both "
            "litmus papers do in an alkaline solution.\n\n"
            "(ಕ್ಷಾರ ದ್ರಾವಣದಲ್ಲಿ ಲಿಟ್ಮಸ್ ಕಾಗದ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' — soap used. Red litmus turns BLUE, blue litmus stays unchanged.",
            "attempt_2": "Set 'initialState' to 'basic'. Base result: red → BLUE confirms base.",
            "attempt_3": "Choose 'basic': soap gives the base result — RED turns BLUE."
        },
        "concept_reminder": (
            "Bases turn RED litmus BLUE. Blue litmus stays unchanged. "
            "OH⁻ ions from bases cause red litmus to turn blue. "
            "(ಕ್ಷಾರ: ಕೆಂಪು ಲಿಟ್ಮಸ್ → ನೀಲಿ!)"
        )
    },
    {
        "id": "litmus_q3",
        "challenge": (
            "Show the litmus result for a NEUTRAL substance and explain how this makes "
            "litmus a COMPLETE indicator.\n\n"
            "(ತಟಸ್ಥ ದ್ರಾವಣದಲ್ಲಿ ಲಿಟ್ಮಸ್ ಕಾಗದ ಏನಾಗುತ್ತದೆ — ಲಿಟ್ಮಸ್ ಪೂರ್ಣ ಸೂಚಕ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "neutral"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'neutral' — tap water used. NEITHER paper changes. Both stay their original colour.",
            "attempt_2": "Set 'initialState' to 'neutral'. No colour change confirms neutrality.",
            "attempt_3": "Choose 'neutral': tap water gives no change in either paper — neutral result."
        },
        "concept_reminder": (
            "Neutral → NEITHER litmus changes. Blue stays blue, red stays red. "
            "Three outcomes: Blue→Red=acid, Red→Blue=base, No change=neutral. "
            "This makes litmus a COMPLETE indicator. pH 7 = neutral. "
            "(ತಟಸ್ಥ: ಯಾವ ಲಿಟ್ಮಸ್ ಕಾಗದವೂ ಬಣ್ಣ ಬದಲಾಯಿಸಲ್ಲ!)"
        )
    }
]


# =============================================================================
# HIDDEN MESSAGE SIMULATION
# ಗುಪ್ತ ಸಂದೇಶ ಬಹಿರಂಗ – ಆಮ್ಲ-ಕ್ಷಾರ ಸೂಚಕ ಪರಿಚಯ
# Science Chapter 2 – Chapter-opening indicator demonstration
# =============================================================================
SIMULATIONS_KN["hidden_message_kn"] = {
    "title": "ಗುಪ್ತ ಸಂದೇಶ ಬಹಿರಂಗ (Hidden Message Reveal)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation1_hidden_message_kn.html",
    "description": (
        "Kannada chapter-opening simulation: a message written with invisible alkaline "
        "ink (base) is revealed by spraying an indicator (phenolphthalein) 3 times. "
        "Characters Ashwin and Kirti observe the science fair demonstration. "
        "Creates curiosity about why indicators change colour with acids and bases."
    ),
    "cannot_demonstrate": [
        "Specific chemistry of phenolphthalein",
        "What happens with acidic invisible ink",
        "Quantitative colour change data"
    ],
    "initial_params": {"initialState": "hidden", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Reveal State",
            "range": "hidden, revealing, revealed",
            "url_key": "initialState",
            "effect": (
                "Controls how many indicator sprays are applied on page load.\n"
                "  'hidden'    → blank paper, 0 sprays (default)\n"
                "  'revealing' → 1 spray — message partially visible (33%)\n"
                "  'revealed'  → 3 sprays — message fully visible (100%)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight explanation box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Indicators Change Colour in the Presence of Acids or Bases",
            "description": (
                "An indicator is a substance that changes colour when it contacts an acid or base. "
                "The spray in this simulation reacts with the base ink to produce colour."
            ),
            "key_insight": (
                "Indicators are our tools for detecting acids and bases. "
                "The colour change is a chemical reaction, not just physical mixing. "
                "Different indicators respond to acids, bases, or both."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Invisible Ink: Base + Indicator = Visible Message",
            "description": (
                "The message was written with a BASE solution (e.g. baking soda water) "
                "which dries clear. Spraying an indicator reveals it through colour change."
            ),
            "key_insight": (
                "Base (invisible) + Indicator → colour change (visible). "
                "This is acid-base chemistry applied to: science demos, invisible ink, "
                "surface testing for base residues."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Real-World: Invisible Ink Uses Acid-Base Chemistry",
            "description": (
                "Historically, lemon juice (acid ink) or baking soda (base ink) "
                "were used as invisible inks, revealed by the appropriate indicator."
            ),
            "key_insight": (
                "Lemon juice ink: revealed by alkaline indicator or heat. "
                "Baking soda ink: revealed by acidic indicator (like red cabbage juice). "
                "Acid-base chemistry has practical real-world applications beyond the lab."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["hidden_message_kn"] = [
    {
        "id": "hidden_q1",
        "challenge": (
            "Show the INITIAL state of the paper — before any indicator is sprayed. "
            "This represents the completely invisible hidden message.\n\n"
            "(ಸೂಚಕ ಸಿಂಪಡಿಸುವ ಮೊದಲು ಕಾಗದ ಹೇಗಿರುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "hidden"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'hidden' — the paper appears blank; the base ink is invisible before any indicator reaction.",
            "attempt_2": "Set 'initialState' to 'hidden'. No indicator applied yet, so no colour change, no visible message.",
            "attempt_3": "Choose 'hidden': blank paper state showing how base ink is truly invisible when dry."
        },
        "concept_reminder": (
            "The message is written with BASE solution. When dry, base is colourless and invisible. "
            "No indicator applied = no colour change = invisible message. "
            "Dilute bases are often colourless in solution. "
            "(ಗುಪ್ತ ಸಂದೇಶ: ಕ್ಷಾರ ಒಣಗಿದಾಗ ಅದೃಶ್ಯ!)"
        )
    },
    {
        "id": "hidden_q2",
        "challenge": (
            "Show the COMPLETELY REVEALED state — after full indicator treatment. "
            "Demonstrate how the indicator reacts with the base to make the message fully visible.\n\n"
            "(ಸೂಚಕ ಸಿಂಪಡಿಸಿದ ನಂತರ ಸಂದೇಶ ಸಂಪೂರ್ಣ ಬಹಿರಂಗ ಆಗುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "revealed"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'revealed' — all 3 sprays applied automatically and 'ವಿಜ್ಞಾನ ಮೇಳ!' becomes fully visible.",
            "attempt_2": "Set 'initialState' to 'revealed'. Complete reveal shows indicator reacting fully with all base molecules.",
            "attempt_3": "Choose 'revealed': 3 sprays show the full message — indicator + base = colour change."
        },
        "concept_reminder": (
            "3 indicator sprays reveal the full message. "
            "Indicator + Base → coloured compound exactly where base was applied. "
            "This is COLOUR CHANGE REACTION: Indicator + Base → visible coloured product. "
            "(ಸೂಚಕ + ಕ್ಷಾರ → ಬಣ್ಣ ಬದಲಾವಣೆ → ಗುಪ್ತ ಸಂದೇಶ ಬಹಿರಂಗ!)"
        )
    },
    {
        "id": "hidden_q3",
        "challenge": (
            "Show the PARTIALLY REVEALED state — after just one spray. "
            "Demonstrate how the colour change builds gradually.\n\n"
            "(ಒಂದು ಸಿಂಪಡಿಕೆಯ ನಂತರ ಸಂದೇಶ ಭಾಗಶಃ ಕಾಣಿಸುವ ಸ್ಥಿತಿ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "revealing"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'revealing' — one spray applied; message appears faintly showing partial colour change.",
            "attempt_2": "Set 'initialState' to 'revealing'. After 1 spray, partial visibility shows the reaction is gradual.",
            "attempt_3": "Choose 'revealing': one spray gives a faint glimpse — reaction in progress but not complete."
        },
        "concept_reminder": (
            "After one spray, the message is partially visible — faint but detectable. "
            "More indicator → more reaction → more colour → clearer message. "
            "The indicator must contact all base molecules in the ink for full visibility. "
            "(ಒಂದು ಸಿಂಪಡಿಕೆ: ಭಾಗಶಃ ಬಹಿರಂಗ — ಪ್ರತಿಕ್ರಿಯೆ ಮುಂದುವರಿಯುತ್ತಿದೆ!)"
        )
    }
]


# =============================================================================
# OLFACTORY INDICATOR SIMULATION (sim6)
# ಘ್ರಾಣ ಸೂಚಕ – ಈರುಳ್ಳಿ ವಾಸನೆಯಿಂದ ಆಮ್ಲ/ಕ್ಷಾರ ಗುರುತಿಸಿ
# =============================================================================
SIMULATIONS_KN["olfactory_indicator_kn"] = {
    "title": "ಘ್ರಾಣ ಸೂಚಕ (Olfactory Indicator)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation6_olfactory_indicator_kn.html",
    "description": (
        "Kannada simulation: students mix household solutions with cut onion and observe "
        "whether the pungent smell remains (acid) or disappears (base). Onion's sulfur "
        "compounds are neutralised by bases but not by acids — making onion a natural "
        "olfactory indicator."
    ),
    "cannot_demonstrate": [
        "Neutral substance — neither preserves nor eliminates smell distinctly",
        "Quantitative measurement of smell intensity"
    ],
    "initial_params": {"initialState": "basic", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Solution Type",
            "range": "acidic, basic",
            "url_key": "initialState",
            "effect": (
                "Selects a solution and auto-runs the mixing test.\n"
                "  'acidic' → tamarind water — smell stays strong (acid confirmed)\n"
                "  'basic'  → baking soda — smell disappears (base confirmed)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the key insight box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "ಘ್ರಾಣ ಸೂಚಕ: ಆಮ್ಲ ವಾಸನೆ ಉಳಿಸುತ್ತದೆ (Acids Preserve Onion Smell)",
            "description": (
                "Acids do NOT react with onion's sulfur compounds. When an acid solution "
                "is mixed with cut onion the pungent smell remains unchanged."
            ),
            "key_insight": (
                "Acid + Onion → Strong smell persists. Lemon, vinegar, tamarind — "
                "all leave onion smell intact. This is how onion detects an acid."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "ಘ್ರಾಣ ಸೂಚಕ: ಕ್ಷಾರ ವಾಸನೆ ನಾಶ ಮಾಡುತ್ತದೆ (Bases Destroy Onion Smell)",
            "description": (
                "Bases neutralise onion's allyl sulfide compounds. When a base is mixed "
                "with cut onion the smell disappears within seconds."
            ),
            "key_insight": (
                "Base + Onion → Smell vanishes. Baking soda, soap — all eliminate the "
                "pungent odour via neutralisation. Confirmed base!"
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "ಪ್ರತ್ಯಕ್ಷ ಉದಾಹರಣೆ: ಬೇಕಿಂಗ್ ಸೋಡಾದೊಂದಿಗೆ ಈರುಳ್ಳಿ ಬೇಯಿಸುವುದು",
            "description": (
                "Cooking onion with baking soda (alkaline) reduces its pungency. "
                "The same neutralisation reaction seen in the simulation occurs in the kitchen."
            ),
            "key_insight": (
                "Real-world chemistry: alkaline baking soda neutralises onion sulfur compounds "
                "reducing sharpness. Acid-base indicators exist beyond the lab — they are in "
                "your kitchen too!"
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["olfactory_indicator_kn"] = [
    {
        "id": "olfactory_q1",
        "challenge": (
            "Show what happens when an ACID is mixed with cut onion using the olfactory "
            "indicator simulation. Does the smell remain or disappear?\n\n"
            "(ಆಮ್ಲ ಈರುಳ್ಳಿಯೊಂದಿಗೆ ಮಿಶ್ರಣ ಮಾಡಿದಾಗ ವಾಸನೆ ಉಳಿಯುತ್ತದೆಯೇ ಅಥವಾ ಅದೃಶ್ಯವಾಗುತ್ತದೆಯೇ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' as the Simulation State — tamarind water mixed with onion. Watch whether the smell icon keeps showing.",
            "attempt_2": "Set 'initialState' to 'acidic'. Acids do NOT neutralise sulfur compounds so the smell stays strong.",
            "attempt_3": "Choose 'acidic': acid + onion → smell remains. This is how we know it is an acid!"
        },
        "concept_reminder": (
            "Acids preserve onion smell. Tamarind, vinegar, lemon juice — none react "
            "with sulfur compounds. Smell stays = acid. "
            "(ಆಮ್ಲ + ಈರುಳ್ಳಿ → ವಾಸನೆ ಉಳಿಯುತ್ತದೆ!)"
        )
    },
    {
        "id": "olfactory_q2",
        "challenge": (
            "Show what happens when a BASE is mixed with cut onion. Demonstrate why "
            "onion is called an olfactory indicator.\n\n"
            "(ಕ್ಷಾರ ಈರುಳ್ಳಿಯೊಂದಿಗೆ ಮಿಶ್ರಣ ಮಾಡಿದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' — baking soda mixed with onion. The pungent smell disappears completely.",
            "attempt_2": "Set 'initialState' to 'basic'. Bases neutralise sulfur compounds → smell vanishes.",
            "attempt_3": "Choose 'basic': base + onion → smell disappears. A base is confirmed!"
        },
        "concept_reminder": (
            "Bases destroy onion smell via neutralisation. Baking soda, soap — "
            "all eliminate the pungent odour. No smell = base. "
            "(ಕ್ಷಾರ + ಈರುಳ್ಳಿ → ವಾಸನೆ ಅದೃಶ್ಯ!)"
        )
    },
    {
        "id": "olfactory_q3",
        "challenge": (
            "Show the acid test again and explain: why is onion called a PARTIAL olfactory "
            "indicator (not a complete one)?\n\n"
            "(ಘ್ರಾಣ ಸೂಚಕ ಭಾಗಶಃ ಯಾಕೆ — ಪೂರ್ಣ ಸೂಚಕ ಅಲ್ಲ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' — observe that smell stays strong. Onion can identify acids (smell stays) and bases (smell goes), but NOT neutral substances.",
            "attempt_2": "Set 'initialState' to 'acidic'. Since onion stays smelly with acid AND neutral substances, it cannot distinguish between them.",
            "attempt_3": "Choose 'acidic': smell stays with acid. But neutral water also keeps the smell — so onion is partial, not complete."
        },
        "concept_reminder": (
            "Onion is a PARTIAL olfactory indicator: identifies bases (smell gone) but "
            "cannot distinguish acid from neutral (both keep the smell). "
            "Compare: litmus is complete — gives 3 distinct results. "
            "(ಘ್ರಾಣ ಸೂಚಕ: ಕ್ಷಾರ ಮಾತ್ರ ಖಚಿತಪಡಿಸಬಲ್ಲದು!)"
        )
    }
]


# =============================================================================
# NEUTRALISATION REACTION SIMULATION (sim7)
# ತಟಸ್ಥೀಕರಣ ಪ್ರತಿಕ್ರಿಯೆ – ಆಮ್ಲ + ಕ್ಷಾರ = ಉಪ್ಪು + ನೀರು
# =============================================================================
SIMULATIONS_KN["neutralisation_reaction_kn"] = {
    "title": "ತಟಸ್ಥೀಕರಣ ಪ್ರತಿಕ್ರಿಯೆ (Neutralisation Reaction)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation7_neutralisation_reaction_kn.html",
    "description": (
        "Kannada slider simulation: students adjust the acid-base ratio and observe "
        "the resulting pH. At equal proportions (slider ~50%) full neutralisation "
        "produces salt + water + heat at pH 7. Too much acid → acidic product; "
        "too much base → basic product. pH pointer, product indicators, and color-coded "
        "beakers make the stoichiometry visual."
    ),
    "cannot_demonstrate": [
        "Specific chemical equations (e.g. HCl + NaOH)",
        "Heat measurement in joules",
        "Effect of concentration on reaction rate"
    ],
    "initial_params": {"initialState": "neutral", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Reaction Outcome",
            "range": "acidic, neutral, basic",
            "url_key": "initialState",
            "effect": (
                "Sets the slider position and auto-runs the mixing reaction.\n"
                "  'acidic'  → slider at 20% (excess acid) — acidic product, pH ~3\n"
                "  'neutral' → slider at 50% (equal parts) — neutral, pH 7\n"
                "  'basic'   → slider at 80% (excess base) — basic product, pH ~11"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the key insight box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "ತಟಸ್ಥೀಕರಣ: ಆಮ್ಲ + ಕ್ಷಾರ → ಉಪ್ಪು + ನೀರು + ಶಾಖ",
            "description": (
                "When acid and base react in equal amounts they completely neutralise "
                "each other producing salt, water AND heat (exothermic reaction). "
                "The result is pH 7 — neutral."
            ),
            "key_insight": (
                "Equal acid + base = complete neutralisation → salt + water + heat. "
                "pH goes from acidic/basic extremes to exactly 7. "
                "Real example: antacid (base) neutralises excess stomach acid (HCl)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "ಅಸಮ ಅನುಪಾತ: ಹೆಚ್ಚು ಆಮ್ಲ ಅಥವಾ ಕ್ಷಾರ",
            "description": (
                "When acid is in excess the product is still acidic (pH < 7). "
                "When base is in excess the product is still basic (pH > 7). "
                "Only exact equal amounts give pH 7."
            ),
            "key_insight": (
                "Ratio matters! Excess acid → acidic product. Excess base → basic product. "
                "Perfect neutralisation requires stoichiometric equivalence."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "ವಾಸ್ತವ ಬಳಕೆ: ಆಮ್ಲನಿರೋಧಕಗಳು (Real-world: Antacids)",
            "description": (
                "Antacid tablets contain base (Mg(OH)₂) that neutralises excess stomach "
                "acid (HCl) using the same acid-base neutralisation chemistry demonstrated here."
            ),
            "key_insight": (
                "Stomach acid (HCl) + Antacid base → salt + water → relief. "
                "The same neutralisation equation applies: acid + base → salt + water. "
                "This is neutralisation chemistry in daily life."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["neutralisation_reaction_kn"] = [
    {
        "id": "neutralisation_q1",
        "challenge": (
            "Show the COMPLETE neutralisation scenario — the ideal case where acid and "
            "base fully cancel each other producing salt, water, and a neutral pH.\n\n"
            "(ಸಂಪೂರ್ಣ ತಟಸ್ಥೀಕರಣ ತೋರಿಸಿ — pH 7 ಆಗುವ ಅದರ್ಶ ಸ್ಥಿತಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "neutral"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'neutral' — slider goes to 50%, equal acid and base mix, pH pointer reaches exactly 7.",
            "attempt_2": "Set 'initialState' to 'neutral'. Equal proportions → complete neutralisation → salt + water + heat at pH 7.",
            "attempt_3": "Choose 'neutral': 50% base + 50% acid → perfect neutral result, all three products appear."
        },
        "concept_reminder": (
            "Complete neutralisation: Acid + Base (equal parts) → Salt + Water + Heat, pH = 7. "
            "The salt and water products light up. This is the ideal outcome. "
            "(ಸಮ ಭಾಗ ಆಮ್ಲ + ಕ್ಷಾರ → pH 7, ಸಂಪೂರ್ಣ ತಟಸ್ಥೀಕರಣ!)"
        )
    },
    {
        "id": "neutralisation_q2",
        "challenge": (
            "Show what happens when there is EXCESS ACID in the mixture — "
            "demonstrate that incomplete neutralisation still leaves an acidic product.\n\n"
            "(ಆಮ್ಲ ಹೆಚ್ಚಾದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' — slider moves to 20%, excess acid remains after base is exhausted, product pH ~3.",
            "attempt_2": "Set 'initialState' to 'acidic'. Not enough base to neutralise all acid → still acidic product.",
            "attempt_3": "Choose 'acidic': slider at 20% means very little base, lots of acid leftover. Result beaker stays orangey-red."
        },
        "concept_reminder": (
            "Excess acid → product is still acidic (pH < 7). Not enough base to neutralise everything. "
            "The remaining H⁺ ions keep the solution acidic. "
            "(ಆಮ್ಲ ಹೆಚ್ಚಾದರೆ ಫಲಿತಾಂಶ ಇನ್ನೂ ಆಮ್ಲೀಯ!)"
        )
    },
    {
        "id": "neutralisation_q3",
        "challenge": (
            "Show what happens when there is EXCESS BASE — demonstrate that too much "
            "base also prevents complete neutralisation.\n\n"
            "(ಕ್ಷಾರ ಹೆಚ್ಚಾದಾಗ ಏನಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' — slider moves to 80%, excess base remains, product pH ~11.",
            "attempt_2": "Set 'initialState' to 'basic'. Too much base means leftover OH⁻ ions → basic product.",
            "attempt_3": "Choose 'basic': 80% base means excess alkali. Result beaker turns blue and pH > 9."
        },
        "concept_reminder": (
            "Excess base → product is still basic (pH > 7). Leftover OH⁻ ions keep it alkaline. "
            "Perfect neutralisation needs EXACT stoichiometric ratio. "
            "(ಕ್ಷಾರ ಹೆಚ್ಚಾದರೆ ಫಲಿತಾಂಶ ಇನ್ನೂ ಕ್ಷಾರೀಯ!)"
        )
    }
]


# =============================================================================
# ANT BITE TREATMENT SIMULATION (sim8)
# ಇರುವೆ ಕಚ್ಚುವಿಕೆ ಚಿಕಿತ್ಸೆ – ದೈನಂದಿನ ಜೀವನದಲ್ಲಿ ತಟಸ್ಥೀಕರಣ
# =============================================================================
SIMULATIONS_KN["ant_bite_treatment_kn"] = {
    "title": "ಇರುವೆ ಕಚ್ಚುವಿಕೆ ಚಿಕಿತ್ಸೆ (Ant Bite Treatment)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation8_ant_bite_treatment_kn.html",
    "description": (
        "Kannada sequential simulation: students observe an ant bite inject formic acid "
        "(HCOOH) into the skin, causing redness and pain. Applying baking soda (base) "
        "neutralises the acid, eliminating pain and healing the skin. A real-world "
        "demonstration of neutralisation as first aid."
    ),
    "cannot_demonstrate": [
        "Chemical equation with actual molecular symbols in interactive form",
        "Other ant-bite remedies beyond baking soda",
        "Difference between red-ant and black-ant venom"
    ],
    "initial_params": {"initialState": "normal", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Scenario State",
            "range": "normal, bitten, treated",
            "url_key": "initialState",
            "effect": (
                "Controls the sequential treatment scenario auto-played on load.\n"
                "  'normal'  → healthy skin, no bite (default)\n"
                "  'bitten'  → ant bites, formic acid injected, skin turns red (1 click)\n"
                "  'treated' → baking soda applied, neutralisation, pain relief (2 clicks)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight and science explanation boxes."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "ಇರುವೆ ಚುಚ್ಚುವ ಆಮ್ಲ: ಫಾರ್ಮಿಕ್ ಆಮ್ಲ (HCOOH)",
            "description": (
                "Ant venom contains formic acid (HCOOH). When an ant bites, it injects "
                "this acid into the skin, causing a burning sensation, redness, "
                "and localised pain."
            ),
            "key_insight": (
                "Formic acid (HCOOH) = ant venom. Acidic substance causes inflammation. "
                "To relieve pain we need to NEUTRALISE the acid — apply a base."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "ಚಿಕಿತ್ಸೆ: ಬೇಕಿಂಗ್ ಸೋಡಾ ತಟಸ್ಥೀಕರಣ (Baking Soda Neutralises the Acid)",
            "description": (
                "Baking soda (NaHCO₃) is a base. Applied to the ant bite it reacts with "
                "formic acid and neutralises it: Formic acid + Baking soda → Salt + Water. "
                "Pain and inflammation disappear."
            ),
            "key_insight": (
                "Baking soda (base) + Formic acid → salt + water + relief. "
                "The same neutralisation formula applies: acid + base → harmless products. "
                "This is the chemistry behind a simple first aid remedy."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "ವಾಸ್ತವ ಅನ್ವಯ: ಚರ್ಮ pH ಮರಳಿ ತಟಸ್ಥ",
            "description": (
                "After treatment the skin's pH returns to normal (~7). "
                "The neutralisation converts the acidic sting into harmless salt and water, "
                "stopping the chemical damage to skin cells."
            ),
            "key_insight": (
                "Neutralisation has real medical uses. Bee stings (also acid) → baking soda. "
                "Wasp stings (alkaline) → vinegar (acid). Match the treatment to the venom type. "
                "Acid venom → base treatment; alkaline venom → acid treatment."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["ant_bite_treatment_kn"] = [
    {
        "id": "antbite_q1",
        "challenge": (
            "Show just the ANT BITE — the moment formic acid is injected into the skin "
            "causing pain and redness. Do NOT apply treatment yet.\n\n"
            "(ಇರುವೆ ಕಚ್ಚುವ ಕ್ಷಣ ತೋರಿಸಿ — ಚಿಕಿತ್ಸೆ ಇಲ್ಲದೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "bitten"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'bitten' — the simulation auto-clicks the bite button showing formic acid injection and redness.",
            "attempt_2": "Set 'initialState' to 'bitten'. The skin turns red, pain shows HIGH, pH drops to ~4 (acidic).",
            "attempt_3": "Choose 'bitten': just the bite, no treatment. This shows formic acid (HCOOH) causing the problem."
        },
        "concept_reminder": (
            "Ant venom = formic acid (HCOOH). Injection makes skin acidic (~pH 4). "
            "Pain, redness, burning = acid damage to skin cells. Treatment needed! "
            "(ಇರುವೆ ಕಚ್ಚಿದಾಗ ಫಾರ್ಮಿಕ್ ಆಮ್ಲ ಚುಚ್ಚುತ್ತದೆ — ನೋವು ಮತ್ತು ಕೆಂಪು!)"
        )
    },
    {
        "id": "antbite_q2",
        "challenge": (
            "Show the COMPLETE treatment — bite followed by baking soda application. "
            "Demonstrate how neutralisation provides relief.\n\n"
            "(ಇರುವೆ ಕಚ್ಚಿದ ನಂತರ ಬೇಕಿಂಗ್ ಸೋಡಾ ಲೇಪಿಸಿ ತಟಸ್ಥೀಕರಣ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "treated"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'treated' — both buttons are auto-clicked: bite (800ms) then treatment (1800ms later). Shows full neutralisation.",
            "attempt_2": "Set 'initialState' to 'treated'. Redness disappears, pH returns to ~7, pain becomes 'ಇಲ್ಲ ✅'.",
            "attempt_3": "Choose 'treated': complete scenario — bite → baking soda → neutralisation → relief."
        },
        "concept_reminder": (
            "Baking soda (base) + Formic acid → salt + water. Skin pH returns to 7. "
            "Neutralisation reverses the damage — pain disappears. "
            "(ಬೇಕಿಂಗ್ ಸೋಡಾ ಫಾರ್ಮಿಕ್ ಆಮ್ಲ ತಟಸ್ಥೀಕರಿಸಿ ನೋವು ದೂರ ಮಾಡುತ್ತದೆ!)"
        )
    },
    {
        "id": "antbite_q3",
        "challenge": (
            "Show the HEALTHY initial state — before any bite. "
            "This is the baseline for comparing the effect of acid injection.\n\n"
            "(ಕಚ್ಚುವ ಮೊದಲು ಆರೋಗ್ಯಕರ ಚರ್ಮದ ಪ್ರಾರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "normal"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'normal' — the default state with healthy skin and pH ~7 before any ant bite.",
            "attempt_2": "Set 'initialState' to 'normal'. This is the unaffected baseline — no acid, no pain, no treatment needed.",
            "attempt_3": "Choose 'normal': healthy skin, pH ~7. Compare this to 'bitten' (pH ~4) to see the acid's effect."
        },
        "concept_reminder": (
            "Normal skin pH is ~7 (neutral). After ant bite it drops to ~4 (acidic). "
            "After baking soda treatment it returns to ~7. "
            "This three-state comparison shows neutralisation in action. "
            "(ಸಾಮಾನ್ಯ ಚರ್ಮ pH 7 → ಕಚ್ಚಿದ ಮೇಲೆ pH 4 → ಚಿಕಿತ್ಸೆ ನಂತರ pH 7 ಮರಳಿ!)"
        )
    }
]


# =============================================================================
# SOIL TREATMENT SIMULATION (sim9)
# ಮಣ್ಣಿನ ಚಿಕಿತ್ಸೆ – ಕೃಷಿಯಲ್ಲಿ ತಟಸ್ಥೀಕರಣ
# =============================================================================
SIMULATIONS_KN["soil_treatment_kn"] = {
    "title": "ಮಣ್ಣಿನ ಚಿಕಿತ್ಸೆ (Soil Treatment — Agriculture)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter2_simulation9_soil_treatment_kn.html",
    "description": (
        "Kannada two-step soil simulation. Students select acidic soil (pH 4–5) or "
        "alkaline soil (pH 9–10), then apply the correct neutralising agent: lime (base) "
        "for acidic soil, compost (releases acids) for alkaline soil. The wilted plant "
        "recovers to show pH-7 healthy soil. Demonstrates agricultural neutralisation."
    ),
    "cannot_demonstrate": [
        "Quantitative lime dosage calculations",
        "Different types of lime or compost products",
        "Long-term soil pH management over seasons"
    ],
    "initial_params": {"initialState": "acidic", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Soil Scenario",
            "range": "acidic, basic, treated",
            "url_key": "initialState",
            "effect": (
                "Controls which soil problem is selected and whether treatment is applied.\n"
                "  'acidic'  → acidic soil selected (pH 4-5), plant wilted, lime shown\n"
                "  'basic'   → alkaline soil selected (pH 9-10), plant wilted, compost shown\n"
                "  'treated' → acidic soil selected then lime applied → pH returns to 7"
            )
        },
        "showHints": {
            "label": "Show Concept Card",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "ಆಮ್ಲೀಯ ಮಣ್ಣಿಗೆ ಚಿಕಿತ್ಸೆ: ಸುಣ್ಣ (ಕ್ಷಾರ) ಸೇರಿಸಿ",
            "description": (
                "When soil is too acidic (pH < 6) plants cannot absorb nutrients properly. "
                "Farmers add lime (calcium carbonate, a base) to neutralise excess soil acid "
                "and raise pH to the optimal neutral range."
            ),
            "key_insight": (
                "Acidic soil → add lime (base) → neutralisation → pH 7 → healthy plants. "
                "Soil acid + lime base → calcium salt + water. Same neutralisation equation."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "ಕ್ಷಾರೀಯ ಮಣ್ಣಿಗೆ ಚಿಕಿತ್ಸೆ: ಕಂಪೋಸ್ಟ್ (ಆಮ್ಲ ಬಿಡುಗಡೆ) ಸೇರಿಸಿ",
            "description": (
                "When soil is too alkaline (pH > 8) plants cannot absorb iron properly. "
                "Farmers add organic compost which releases acids as it decomposes, "
                "neutralising the excess alkali and bringing pH down to 7."
            ),
            "key_insight": (
                "Alkaline soil → add compost (acid-releasing) → neutralisation → pH 7. "
                "Compost acids + soil base → harmless salts + water. Same chemistry."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "pH 7: ಸಸ್ಯಗಳಿಗೆ ಆದರ್ಶ ಸ್ಥಿತಿ",
            "description": (
                "Plants grow best in neutral or near-neutral soil (pH 6.5–7.5). "
                "At this pH, all essential nutrients are maximally available and soluble. "
                "Too acidic or too alkaline blocks nutrient uptake mechanisms."
            ),
            "key_insight": (
                "Neutralisation → pH 7 → plant recovers from wilted to healthy. "
                "This is why farmers test soil pH and apply lime or compost every season. "
                "Chemistry knowledge directly improves agricultural yield."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["soil_treatment_kn"] = [
    {
        "id": "soil_q1",
        "challenge": (
            "Show the ACIDIC SOIL problem — select the acidic soil scenario to demonstrate "
            "why excess acid in soil prevents healthy plant growth.\n\n"
            "(ಆಮ್ಲೀಯ ಮಣ್ಣಿನ ಸಮಸ್ಯೆ ತೋರಿಸಿ — ಸಸ್ಯ ಯಾಕೆ ಮ್ಲಾನವಾಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "acidic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'acidic' — the simulation shows acidic soil (pH 4-5), wilted plant, and lime bag highlighted as the solution.",
            "attempt_2": "Set 'initialState' to 'acidic'. Acidic soil blocks nutrient absorption — the plant cannot grow.",
            "attempt_3": "Choose 'acidic': see pH 4-5 soil, wilted plant emoji 🥀, and lime bag shown as the required treatment."
        },
        "concept_reminder": (
            "Acidic soil (pH 4-5) blocks nutrient absorption → plant wilts. "
            "Solution: add lime (base) to neutralise acid → pH reaches 7 → plant recovers. "
            "(ಆಮ್ಲೀಯ ಮಣ್ಣು: pH 4-5, ಸಸ್ಯ ಮ್ಲಾನ. ಸುಣ್ಣ ಹಾಕಿ ತಟಸ್ಥ ಮಾಡಿ!)"
        )
    },
    {
        "id": "soil_q2",
        "challenge": (
            "Show the ALKALINE SOIL problem — demonstrate the opposite case where "
            "excess base in soil also harms plant growth.\n\n"
            "(ಕ್ಷಾರೀಯ ಮಣ್ಣಿನ ಸಮಸ್ಯೆ ತೋರಿಸಿ — ಅಧಿಕ ಕ್ಷಾರ ಸಸ್ಯಕ್ಕೆ ಹಾಗೂ ಹಾನಿ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "basic"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'basic' — alkaline soil (pH 9-10), plant remains wilted, compost bag highlighted.",
            "attempt_2": "Set 'initialState' to 'basic'. Alkaline soil blocks iron absorption — add compost (acid-releasing) to neutralise.",
            "attempt_3": "Choose 'basic': pH 9-10, wilted 🥀 plant, compost shown as treatment. Both extremes harm plants!"
        },
        "concept_reminder": (
            "Alkaline soil (pH 9-10) blocks iron absorption → plant wilts. "
            "Solution: add compost (releases acids) to neutralise excess alkali → pH 7. "
            "Both acidic AND alkaline soil need treatment. "
            "(ಕ್ಷಾರೀಯ ಮಣ್ಣು: pH 9-10, ಸಸ್ಯ ಮ್ಲಾನ. ಕಂಪೋಸ್ಟ್ ಹಾಕಿ ತಟಸ್ಥ ಮಾಡಿ!)"
        )
    },
    {
        "id": "soil_q3",
        "challenge": (
            "Show the COMPLETE TREATMENT — acidic soil selected AND lime applied, "
            "demonstrating full agricultural neutralisation restoring healthy plant growth.\n\n"
            "(ಸಂಪೂರ್ಣ ಚಿಕಿತ್ಸೆ ತೋರಿಸಿ — ಆಮ್ಲೀಯ ಮಣ್ಣಿಗೆ ಸುಣ್ಣ ಹಾಕಿ ಸಸ್ಯ ಚೇತರಿಸಿದ್ದು)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "treated"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'treated' — simulation auto-selects acidic soil (800ms) then applies lime treatment (1800ms). Plant changes from 🥀 to 🌿.",
            "attempt_2": "Set 'initialState' to 'treated'. Full neutralisation: soil acid + lime base → pH 7, plant recovers.",
            "attempt_3": "Choose 'treated': watch the plant go from wilted to healthy! Neutralisation is complete."
        },
        "concept_reminder": (
            "Acidic soil + Lime (base) → neutralisation → pH 7 → healthy plant 🌿. "
            "Same neutralisation equation: acid + base → salt + water. "
            "This is real agricultural chemistry — farmers do this every season! "
            "(ಸುಣ್ಣ ಹಾಕಿ ತಟಸ್ಥೀಕರಣ: ಆಮ್ಲ + ಕ್ಷಾರ → ಉಪ್ಪು + ನೀರು → ಸಸ್ಯ ಆರೋಗ್ಯ!)"
        )
    }
]


# =============================================================================
# CONDUCTORS AND INSULATORS SIMULATION (sim10 — Chapter 3)
# ವಾಹಕಗಳು ಮತ್ತು ಅವಾಹಕಗಳು – ವಿದ್ಯುತ್ ಪರೀಕ್ಷೆ
# =============================================================================
SIMULATIONS_KN["conductors_insulators_kn"] = {
    "title": "ವಾಹಕ ಮತ್ತು ಅವಾಹಕ (Conductors and Insulators)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation10_conductors_insulators_kn.html",
    "description": (
        "Kannada Chapter 3 simulation: students test 8 common materials in a virtual "
        "circuit. Metals (spoon, key, coin, foil) light the bulb — confirmed conductors. "
        "Non-metals (plastic, rubber, wood, glass) keep the bulb off — confirmed insulators. "
        "Score panel tracks conductors vs insulators found. Includes safety rules for "
        "handling electricity."
    ),
    "cannot_demonstrate": [
        "Semiconductors or partial conductors",
        "Effect of temperature on conductivity",
        "Measurement of resistance in ohms"
    ],
    "initial_params": {"initialState": "conductor", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Test Material",
            "range": "conductor, insulator",
            "url_key": "initialState",
            "effect": (
                "Auto-tests a material in the circuit on load.\n"
                "  'conductor' → tests metal spoon (🥄) — bulb lights up, circuit complete\n"
                "  'insulator' → tests plastic scale (📏) — bulb stays off, circuit broken"
            )
        },
        "showHints": {
            "label": "Show Concept Card",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "ವಾಹಕಗಳು: ಲೋಹಗಳು ವಿದ್ಯುತ್ ಹರಿಸುತ್ತವೆ (Metals Conduct Electricity)",
            "description": (
                "Conductors allow electric current to flow freely. Metals like copper, "
                "iron, and aluminium have free electrons that can move through the material "
                "carrying the current. The bulb lights up when a conductor completes the circuit."
            ),
            "key_insight": (
                "Conductors = metals = free electrons = current flows = bulb ON. "
                "Spoon, key, coin, foil all light the bulb. This is why electrical wires "
                "are made of copper inside."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "ಅವಾಹಕಗಳು: ಲೋಹೇತರ ವಸ್ತುಗಳು ವಿದ್ಯುತ್ ತಡೆಯುತ್ತವೆ",
            "description": (
                "Insulators prevent electric current from flowing. Plastic, rubber, wood, "
                "and glass hold their electrons tightly in chemical bonds — no free electrons "
                "to carry the current. The bulb stays off when an insulator is in the circuit."
            ),
            "key_insight": (
                "Insulators = non-metals = tightly-bound electrons = no current = bulb OFF. "
                "Plastic, rubber, wood, glass all keep the bulb off. This is why wires "
                "are coated with plastic insulation for safety."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "ಭದ್ರತೆ: ಮಾನವ ದೇಹ ವಾಹಕ (Human Body is a Conductor)",
            "description": (
                "The human body conducts electricity (contains ions in body fluids). "
                "Never touch live wires with bare hands, wet hands, or metallic tools. "
                "Rubber gloves and wooden handles are safe insulating materials used by electricians."
            ),
            "key_insight": (
                "Safety: body = conductor → electric shock risk. "
                "Always use insulating materials (rubber, plastic, dry wood) near electricity. "
                "Never use metallic tools near live wires."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["conductors_insulators_kn"] = [
    {
        "id": "conductor_q1",
        "challenge": (
            "Show a CONDUCTOR being tested in the circuit. Demonstrate that metals "
            "allow current to flow and light the bulb.\n\n"
            "(ವಾಹಕ ಪದಾರ್ಥ ಪರೀಕ್ಷಿಸಿ — ಬಲ್ಬ್ ಬೆಳಗುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "conductor"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'conductor' — the metal spoon is auto-tested. Circuit completes, bulb lights yellow.",
            "attempt_2": "Set 'initialState' to 'conductor'. Metal has free electrons — current flows — bulb ON.",
            "attempt_3": "Choose 'conductor': spoon (metal) tested → bulb glows → circuit complete → confirmed conductor."
        },
        "concept_reminder": (
            "Conductors (metals) have FREE electrons that carry current. "
            "Spoon, key, coin, foil → all light the bulb. Bulb ON = conductor. "
            "(ವಾಹಕ + ಸರ್ಕ್ಯೂಟ್ → ಬಲ್ಬ್ ಬೆಳಗುತ್ತದೆ! ಮುಕ್ತ ಇಲೆಕ್ಟ್ರಾನ್‌ಗಳು!)"
        )
    },
    {
        "id": "conductor_q2",
        "challenge": (
            "Show an INSULATOR being tested in the circuit. Demonstrate that non-metal "
            "materials break the circuit and the bulb stays off.\n\n"
            "(ಅವಾಹಕ ಪದಾರ್ಥ ಪರೀಕ್ಷಿಸಿ — ಬಲ್ಬ್ ಆಫ್ ಆಗಿ ಉಳಿಯುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "insulator"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'insulator' — the plastic scale is auto-tested. No current flows, bulb stays dim/off.",
            "attempt_2": "Set 'initialState' to 'insulator'. Non-metals hold electrons tightly — no current — bulb OFF.",
            "attempt_3": "Choose 'insulator': plastic scale tested → bulb stays dark → circuit broken → confirmed insulator."
        },
        "concept_reminder": (
            "Insulators (non-metals) hold electrons tightly — NO free electrons to carry current. "
            "Plastic, rubber, wood, glass → all keep the bulb off. Bulb OFF = insulator. "
            "(ಅವಾಹಕ + ಸರ್ಕ್ಯೂಟ್ → ಬಲ್ಬ್ ಆಫ್! ಇಲೆಕ್ಟ್ರಾನ್‌ಗಳು ಚಲಿಸಲಾರವು!)"
        )
    },
    {
        "id": "conductor_q3",
        "challenge": (
            "Show a conductor test again and explain — why do electrical wires have "
            "METAL INSIDE and PLASTIC OUTSIDE?\n\n"
            "(ವಿದ್ಯುತ್ ತಂತಿಯಲ್ಲಿ ಒಳಗೆ ತಾಮ್ರ, ಹೊರಗೆ ಪ್ಲಾಸ್ಟಿಕ್ ಯಾಕಿದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "conductor"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'conductor' — watch the metal carry current. Metal inside = conducts; plastic outside = insulates & protects.",
            "attempt_2": "Set 'initialState' to 'conductor'. The metal (conductor) carries the electricity; plastic (insulator) prevents accidental shocks.",
            "attempt_3": "Choose 'conductor': metal spoon lights the bulb. In a wire: copper (metal) = current pathway, plastic = safety barrier."
        },
        "concept_reminder": (
            "Wire design = conductor + insulator working together. "
            "Copper/metal inside → carries current (conductor). "
            "Plastic/rubber outside → blocks accidental current leakage (insulator). "
            "Both are essential! "
            "(ತಂತಿ = ತಾಮ್ರ (ವಾಹಕ) + ಪ್ಲಾಸ್ಟಿಕ್ ಆವರಣ (ಅವಾಹಕ) = ಸುರಕ್ಷಿತ ವಿದ್ಯುತ್!)"
        )
    }
]

# ─────────────────────────────────────────────────────────────────────
# Chapter 3 – Electricity (sim11–sim15)
# ─────────────────────────────────────────────────────────────────────

SIMULATIONS_KN["electricity_uses_kn"] = {
    "id": "electricity_uses_kn",
    "title": "ವಿದ್ಯುತ್ ಬಳಕೆಗಳು (Electricity Uses)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation1_electricity_uses_kn.html",
    "description": (
        "ವಿದ್ಯುತ್ ಉಪಕರಣಗಳನ್ನು 6 ವರ್ಗಗಳಲ್ಲಿ ವರ್ಗೀಕರಿಸಿ: ಅಡುಗೆ, ಬೆಳಕು, ತಂಪು, ಸಂವಹನ, ಮನರಂಜನೆ, ಸಾರಿಗೆ. "
        "Classify 12 electrical appliances into 6 daily-life categories to understand how electricity powers modern life."
    ),
    "cannot_demonstrate": [
        "Auto-completing the sorting game — user must manually classify each appliance"
    ],
    "initial_params": {"initialState": "cooking", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Starting Category",
            "range": "cooking, lighting, cooling, communication, entertainment, transport",
            "url_key": "initialState",
            "effect": (
                "Pre-selects the appliance category when the simulation loads.\n"
                "  'cooking'       → cooking appliances selected (kettle, microwave)\n"
                "  'lighting'      → lighting appliances selected (bulb, tube light)\n"
                "  'cooling'       → cooling/heating appliances selected (fan, AC)\n"
                "  'communication' → communication devices selected (mobile, telephone)\n"
                "  'entertainment' → entertainment devices selected (TV, computer)\n"
                "  'transport'     → transport devices selected (electric train, car)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "electricity_uses_classification",
            "title": "Classifying Electrical Appliances",
            "description": "Electrical appliances can be grouped by their primary purpose into cooking, lighting, cooling/heating, communication, entertainment, and transport categories.",
            "key_insight": "Every electrical device converts electrical energy into another useful form — heat, light, motion, or sound — for a specific human need.",
            "related_params": ["initialState"]
        },
        {
            "id": "electricity_in_daily_life",
            "title": "Electricity in Daily Life",
            "description": "Electricity powers nearly every aspect of modern daily life, from preparing food to communicating and travelling.",
            "key_insight": "Without electricity, cooking (microwave), lighting (bulb), refrigeration (AC/fan), communication (phone), entertainment (TV), and electric transport would all stop.",
            "related_params": ["initialState"]
        },
        {
            "id": "energy_conversion_purpose",
            "title": "Energy Conversion and Purpose",
            "description": "Each appliance converts electrical energy to a specific output. Understanding the purpose helps classify the device correctly.",
            "key_insight": "A kettle converts electrical energy to heat (cooking). A bulb converts it to light. A fan converts it to kinetic energy (cooling). All share electricity as input.",
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["electricity_sources_kn"] = {
    "id": "electricity_sources_kn",
    "title": "ವಿದ್ಯುತ್ ಮೂಲಗಳು (Electricity Sources)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation2_electricity_sources_kn.html",
    "description": (
        "ಜಲ, ಸೌರ, ಗಾಳಿ ಮತ್ತು ಉಷ್ಣ ವಿದ್ಯುತ್ ಉತ್ಪಾದನಾ ಮೂಲಗಳ ದೃಶ್ಯ ಅನ್ವೇಷಣೆ. "
        "Explore how hydro, solar, wind and thermal power plants generate electricity and deliver it to homes via transmission lines."
    ),
    "cannot_demonstrate": [],
    "initial_params": {"initialState": "hydro", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Power Source",
            "range": "hydro, solar, wind, thermal",
            "url_key": "initialState",
            "effect": (
                "Sets which electricity generation source is shown when the simulation loads.\n"
                "  'hydro'   → hydroelectric dam with turbine animation\n"
                "  'solar'   → solar panels with sunlight rays\n"
                "  'wind'    → wind turbine with rotating blades\n"
                "  'thermal' → coal thermal plant with smoke stack"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "electricity_generation",
            "title": "How Electricity is Generated",
            "description": "Power plants convert different forms of energy — falling water, sunlight, wind, heat — into electrical energy using generators or solar cells.",
            "key_insight": "A generator converts mechanical rotation into electrical energy. Hydro, wind, and thermal plants all spin turbines to run generators; solar directly converts light.",
            "related_params": ["initialState"]
        },
        {
            "id": "renewable_vs_nonrenewable",
            "title": "Renewable vs Non-renewable Sources",
            "description": "Hydro, solar, and wind are renewable (replenished naturally); thermal (coal/oil/gas) is non-renewable and causes pollution.",
            "key_insight": "Fossil fuels used in thermal plants will eventually run out and produce CO₂. Renewable sources like sun and wind are limitless and clean.",
            "related_params": ["initialState"]
        },
        {
            "id": "electricity_transmission",
            "title": "Electricity Transmission to Homes",
            "description": "Electricity travels long distances from power plants to homes through metal transmission wires supported by towers.",
            "key_insight": "The energy journey: Source → Generator → Transmission towers & wires → Your home. For experiments, always use CELLS not mains electricity.",
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["torch_components_kn"] = {
    "id": "torch_components_kn",
    "title": "ಟಾರ್ಚ್ ಒಳಭಾಗ (Torch Components)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation3_torch_components_kn.html",
    "description": (
        "ಟಾರ್ಚ್‌ನ ಮೂರು ಭಾಗಗಳನ್ನು (ಕೋಶ, ದೀಪ, ಸ್ವಿಚ್) ಅನ್ವೇಷಿಸಿ ಮತ್ತು ಸ್ವಿಚ್ ಆನ್/ಆಫ್ ಮಾಡಿ ಸರ್ಕ್ಯೂಟ್ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ. "
        "Explore a torch's 3 main components — cells, bulb, switch — and toggle the switch to understand open/closed circuit concepts."
    ),
    "cannot_demonstrate": [],
    "initial_params": {"initialState": "assembled", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "View Mode",
            "range": "assembled, exploded, on",
            "url_key": "initialState",
            "effect": (
                "Sets the initial view state of the torch simulation.\n"
                "  'assembled' → normal assembled torch view (default)\n"
                "  'exploded'  → inside/exploded view showing all components labelled\n"
                "  'on'        → switch toggled ON after 800ms — bulb glows, light beam visible"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "torch_as_circuit",
            "title": "Torch as a Simple Electric Circuit",
            "description": "A torch is a complete simple electric circuit: cells supply energy, the switch controls current flow, and the bulb converts electrical energy to light.",
            "key_insight": "All three components must be connected in a complete loop for the torch to light up. Missing any one breaks the circuit.",
            "related_params": ["initialState"]
        },
        {
            "id": "switch_function",
            "title": "Role of the Switch",
            "description": "A switch controls whether the circuit is complete (closed) or broken (open). Switch ON → circuit closed → current flows → bulb lights up.",
            "key_insight": "A switch is like a 'gate' for electric current. Open gate (OFF) = no current. Closed gate (ON) = current flows and bulb glows.",
            "related_params": ["initialState"]
        },
        {
            "id": "cells_as_energy_source",
            "title": "Cells as the Energy Source",
            "description": "Electric cells inside the torch supply the electrical energy needed to push current through the circuit and light the bulb.",
            "key_insight": "Cells store chemical energy and convert it to electrical energy. Two cells in a torch add their voltages together to provide more energy.",
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["electric_cell_kn"] = {
    "id": "electric_cell_kn",
    "title": "ವಿದ್ಯುತ್ ಕೋಶ (Electric Cell)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation4_electric_cell_kn.html",
    "description": (
        "ವಿದ್ಯುತ್ ಕೋಶದ ಧನ (+) ಮತ್ತು ಋಣ (−) ಟರ್ಮಿನಲ್‌ಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ಸರ್ಕ್ಯೂಟ್ ಚಿಹ್ನೆ ಕಲಿಯಿರಿ. "
        "Explore the positive (+) and negative (−) terminals of an electric cell, understand their physical identification, and learn the circuit symbol."
    ),
    "cannot_demonstrate": [],
    "initial_params": {"initialState": "positive", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Terminal View",
            "range": "positive, negative, circuit",
            "url_key": "initialState",
            "effect": (
                "Sets which terminal or view is highlighted when the simulation loads.\n"
                "  'positive' → positive (+) terminal highlighted, metal cap detail shown\n"
                "  'negative' → negative (−) terminal highlighted, flat disc detail shown\n"
                "  'circuit'  → both terminals highlighted with current flow arrow animated"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "cell_terminals",
            "title": "Cell Terminals — Positive and Negative",
            "description": "An electric cell has two terminals: the positive terminal (small metal cap/bump) and the negative terminal (flat metal disc). They are always marked + and −.",
            "key_insight": "The metal cap (bump) = positive terminal (+). The flat disc = negative terminal (−). Look for the bump to find the positive end of any cell.",
            "related_params": ["initialState"]
        },
        {
            "id": "current_direction",
            "title": "Direction of Current Flow",
            "description": "Conventional electric current flows from the positive terminal through the external circuit (bulb, wires) to the negative terminal.",
            "key_insight": "Think of the cell as a pump: current is pushed OUT of the + terminal, travels through the circuit doing work, and enters back at the − terminal.",
            "related_params": ["initialState"]
        },
        {
            "id": "circuit_symbol_cell",
            "title": "Cell Symbol in Circuit Diagrams",
            "description": "In circuit diagrams, a cell is represented by two parallel lines: a LONG line for positive (+) and a SHORT line for negative (−).",
            "key_insight": "Long line = positive (more energy side). Short line = negative. This symbol is universal — same in all circuit diagrams worldwide.",
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["battery_connection_kn"] = {
    "id": "battery_connection_kn",
    "title": "ಬ್ಯಾಟರಿ ಜೋಡಣೆ (Battery Connection)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation5_battery_connection_kn.html",
    "description": (
        "1, 2 ಮತ್ತು 3 ಕೋಶಗಳನ್ನು ಸರಣಿಯಲ್ಲಿ ಜೋಡಿಸಿ ಬ್ಯಾಟರಿ ಮಾಡಿ — ಹೆಚ್ಚು ಕೋಶ = ಹೆಚ್ಚು ವೋಲ್ಟೇಜ್ = ಹೆಚ್ಚು ಹೊಳೆಯುವ ಬಲ್ಬ್. "
        "Connect 1, 2 or 3 cells in series to form a battery — observe that voltage adds up and the bulb gets brighter with each additional cell."
    ),
    "cannot_demonstrate": [],
    "initial_params": {"initialState": "one_cell", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Number of Cells",
            "range": "one_cell, two_cells, three_cells",
            "url_key": "initialState",
            "effect": (
                "Sets how many cells are connected in series when the simulation loads.\n"
                "  'one_cell'    → 1 cell = 1.5V, dim bulb glow\n"
                "  'two_cells'   → 2 cells in series = 3.0V, brighter bulb\n"
                "  'three_cells' → 3 cells in series = 4.5V, brightest bulb"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "battery_definition",
            "title": "Battery = Multiple Cells in Series",
            "description": "A battery is formed when two or more cells are connected in series: the positive (+) terminal of one cell connected to the negative (−) terminal of the next.",
            "key_insight": "A single cell ≠ a battery. A battery must have at least 2 cells connected + to −. The AA batteries in a remote control are actually individual cells.",
            "related_params": ["initialState"]
        },
        {
            "id": "series_voltage_addition",
            "title": "Voltages Add in Series",
            "description": "When cells are connected in series (+ to −), their voltages add up: 2 cells × 1.5V = 3V; 3 cells × 1.5V = 4.5V.",
            "key_insight": "Series connection = voltage addition. Total battery voltage = number of cells × voltage per cell. More cells → more voltage → more current → brighter bulb.",
            "related_params": ["initialState"]
        },
        {
            "id": "correct_connection_polarity",
            "title": "Correct Polarity is Essential",
            "description": "Cells must be connected with correct polarity (+ to −) in series. Reversing one cell cancels its voltage and reduces total output.",
            "key_insight": "Always connect one cell's (+) to the next cell's (−). Wrong polarity = cells work against each other. This is why battery compartments show + and − markings.",
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["electricity_uses_kn"] = [
    {
        "id": "electricity_uses_q1",
        "challenge": (
            "Show the COOKING category selected in the simulation. "
            "Name two electrical appliances that convert electrical energy to heat for food preparation.\n\n"
            "(ಅಡುಗೆ ವರ್ಗ ಆಯ್ಕೆ ಮಾಡಿ — ಯಾವ ಎರಡು ಉಪಕರಣಗಳು ವಿದ್ಯುತ್ ಶಕ್ತಿಯನ್ನು ಶಾಖವಾಗಿ ಮಾರ್ಪಡಿಸಿ ಅಡುಗೆಗೆ ಬಳಸುತ್ತವೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "cooking"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'cooking' as the initialState. Look for appliances that produce heat to prepare food — think of what heats water or reheats leftovers.",
            "attempt_2": "Set 'initialState' to 'cooking'. The electric kettle (🫖) boils water; the microwave (📦) heats food — both convert electrical energy to heat.",
            "attempt_3": "Choose 'cooking': Electric kettle and microwave both use electrical energy → heat energy for food preparation. Select 'cooking' in the simulation."
        },
        "concept_reminder": (
            "Cooking appliances convert electrical energy to HEAT. "
            "Electric kettle: electrical → heat to boil water. "
            "Microwave: electrical → microwave radiation → heat inside food. "
            "(ವಿದ್ಯುತ್ → ಶಾಖ → ಅಡುಗೆ!)"
        )
    },
    {
        "id": "electricity_uses_q2",
        "challenge": (
            "Set the simulation to show COMMUNICATION devices. "
            "Explain — what energy conversion happens inside a mobile phone?\n\n"
            "(ಸಂವಹನ ವರ್ಗ ಆಯ್ಕೆ ಮಾಡಿ — ಮೊಬೈಲ್ ಫೋನ್‌ನಲ್ಲಿ ಯಾವ ಶಕ್ತಿ ಪರಿವರ್ತನೆ ಆಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "communication"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'communication' as the initialState. Think about devices that send and receive information — voice, text, internet.",
            "attempt_2": "Set 'initialState' to 'communication'. Mobile phones and telephones both convert electrical signals to sound (and vice versa for sending).",
            "attempt_3": "Choose 'communication': Mobile phone converts electrical energy → screen light + sound + radio waves. It's a multi-conversion device!"
        },
        "concept_reminder": (
            "Communication devices convert electrical energy to multiple forms: "
            "sound (speaker), light (screen), and radio waves (transmitter). "
            "Mobile phone is the most complex everyday energy converter. "
            "(ವಿದ್ಯುತ್ → ಶಬ್ದ + ಬೆಳಕು + ರೇಡಿಯೋ ತರಂಗ!)"
        )
    },
    {
        "id": "electricity_uses_q3",
        "challenge": (
            "Show TRANSPORT category. Explain one advantage of electric vehicles "
            "over petrol/diesel vehicles for cities.\n\n"
            "(ಸಾರಿಗೆ ವರ್ಗ ಆಯ್ಕೆ ಮಾಡಿ — ವಿದ್ಯುತ್ ವಾಹನಗಳ ಒಂದು ಪ್ರಮುಖ ಅನುಕೂಲತೆ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "transport"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'transport' as the initialState. Electric trains (🚃) and electric cars (🚗) use electricity instead of burning fuel.",
            "attempt_2": "Set 'initialState' to 'transport'. Electric vehicles produce ZERO exhaust emissions at the point of use — much cleaner for city air quality.",
            "attempt_3": "Choose 'transport': Electric vehicles convert electrical energy → motion (kinetic energy). No burning = no exhaust = cleaner urban air."
        },
        "concept_reminder": (
            "Electric transport: electrical energy → kinetic energy (motion). "
            "Advantage over petrol: zero exhaust emissions, quieter, lower running cost. "
            "Electric trains and cars run on stored electrical energy (from grid or battery). "
            "(ವಿದ್ಯುತ್ ವಾಹನ = ಕಡಿಮೆ ಮಾಲಿನ್ಯ + ಅಧಿಕ ಕಾರ್ಯಕ್ಷಮತೆ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["electricity_sources_kn"] = [
    {
        "id": "electricity_sources_q1",
        "challenge": (
            "Show how HYDRO power generates electricity. "
            "Describe the energy conversion chain from falling water to the light in your home.\n\n"
            "(ಜಲವಿದ್ಯುತ್ ಆಯ್ಕೆ ಮಾಡಿ — ನೀರಿನಿಂದ ನಿಮ್ಮ ಮನೆ ಬೆಳಕಿಗೆ ಶಕ್ತಿ ಪರಿವರ್ತನೆ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "hydro"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'hydro' as the initialState. Watch the dam animation — falling water spins turbines which spin generators.",
            "attempt_2": "Set 'initialState' to 'hydro'. Chain: Potential energy (water in dam) → Kinetic energy (falling water) → Mechanical energy (turbine) → Electrical energy (generator) → Light (bulb).",
            "attempt_3": "Choose 'hydro': Water PE → KE → turbine rotation → generator → electricity → transmission wires → your home's bulb. 5-step chain!"
        },
        "concept_reminder": (
            "Hydro power energy chain: Water PE → KE → Turbine (mechanical) → Generator (electrical) → Home (light/heat). "
            "Renewable: water cycle constantly replenishes the dam. "
            "India example: Bhakra Nangal Dam generates hydroelectric power. "
            "(ಅಣೆಕಟ್ಟು → ಟರ್ಬೈನ್ → ಜನರೇಟರ್ → ವಿದ್ಯುತ್!)"
        )
    },
    {
        "id": "electricity_sources_q2",
        "challenge": (
            "Show SOLAR power. Why is solar power called a 'renewable' source? "
            "What happens to solar electricity generation at night?\n\n"
            "(ಸೌರ ಶಕ್ತಿ ಆಯ್ಕೆ ಮಾಡಿ — ಅದನ್ನು 'ನವೀಕರಣೀಯ' ಎಂದೇಕೆ ಕರೆಯುತ್ತಾರೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "solar"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'solar' as the initialState. Solar panels directly convert sunlight to electricity — no moving parts, no fuel burnt.",
            "attempt_2": "Set 'initialState' to 'solar'. Renewable = source naturally replenishes. Sun rises every day → solar is always available during the day.",
            "attempt_3": "Choose 'solar': The sun shines every day (renewable). No electricity at night unless stored in batteries. No pollution — the cleanest source."
        },
        "concept_reminder": (
            "Solar = renewable because the sun naturally replenishes every day — it won't run out. "
            "Solar panels: sunlight → electricity directly (no turbine needed). "
            "Limitation: no generation at night; storage needed. "
            "Zero emissions, zero fuel cost after installation. "
            "(ಸೂರ್ಯ ಪ್ರತಿದಿನ ಉದಯಿಸುತ್ತದೆ → ನವೀಕರಣೀಯ!)"
        )
    },
    {
        "id": "electricity_sources_q3",
        "challenge": (
            "Show THERMAL power and explain why it is classified as 'non-renewable'. "
            "What is the main environmental concern with thermal power plants?\n\n"
            "(ಉಷ್ಣ ವಿದ್ಯುತ್ ಆಯ್ಕೆ ಮಾಡಿ — ಅದು ನವೀಕರಣೇತರ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "thermal"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Select 'thermal' as the initialState. Thermal plants burn coal, oil or gas — these fossil fuels are formed over millions of years and cannot be replaced quickly.",
            "attempt_2": "Set 'initialState' to 'thermal'. Non-renewable = once used, cannot be replenished in our lifetime. Coal takes millions of years to form.",
            "attempt_3": "Choose 'thermal': Burning coal → CO₂ + other pollutants → air pollution + climate change. That's the main environmental concern."
        },
        "concept_reminder": (
            "Thermal = non-renewable: coal/oil/gas take millions of years to form, can run out. "
            "Main environmental concern: burning fossil fuels releases CO₂ → greenhouse gas → climate change + air pollution. "
            "India uses thermal plants for most of its electricity — major source of pollution. "
            "(ಇಂಗಾಲ ಸುಡುವುದು → CO₂ → ವಾತಾವರಣ ಮಾಲಿನ್ಯ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["torch_components_kn"] = [
    {
        "id": "torch_q1",
        "challenge": (
            "Turn the torch ON using the switch. Explain the complete circuit — "
            "what path does the current take from cell to bulb and back?\n\n"
            "(ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ — ಕೋಶದಿಂದ ದೀಪಕ್ಕೆ ಮತ್ತು ಹಿಂದೆ ಪ್ರವಾಹ ಯಾವ ಮಾರ್ಗದಲ್ಲಿ ಹೋಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "on"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'on'. Watch the light beam appear — the circuit is now complete: cells → switch → bulb → back to cells.",
            "attempt_2": "Choose 'on': Current flows from cell (+) → wire → closed switch → wire → bulb (lights up) → wire → cell (−). One complete loop.",
            "attempt_3": "Set 'initialState=on': The switch closes the gap in the circuit. Complete loop = current flows = bulb glows. Break the loop = OFF."
        },
        "concept_reminder": (
            "A complete circuit is a continuous loop: Cell(+) → switch (closed) → bulb → Cell(−) → back inside cell. "
            "Switch ON = loop is complete = current flows = bulb on. "
            "Switch OFF = loop broken = no current = bulb off. "
            "(ಸ್ವಿಚ್ ಆನ್ → ಸರ್ಕ್ಯೂಟ್ ಪೂರ್ಣ → ದೀಪ ಬೆಳಗುತ್ತದೆ!)"
        )
    },
    {
        "id": "torch_q2",
        "challenge": (
            "Switch to EXPLODED view. Identify the three components inside a torch and state the role of each.\n\n"
            "(ಒಳ ನೋಟ ಆಯ್ಕೆ ಮಾಡಿ — ಟಾರ್ಚ್‌ನ ಮೂರು ಭಾಗಗಳು ಮತ್ತು ಅವುಗಳ ಕರ್ತವ್ಯ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "exploded"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'exploded'. The inside view shows cells, bulb, and switch labelled.",
            "attempt_2": "Choose 'exploded': (1) Cells — supply electrical energy. (2) Bulb — converts electrical to light. (3) Switch — opens/closes the circuit.",
            "attempt_3": "Set 'initialState=exploded': Cells (energy source) + Switch (controller) + Bulb (output) = complete torch circuit. All three needed!"
        },
        "concept_reminder": (
            "Torch = 3-component circuit: "
            "1. CELLS: chemical energy → electrical energy (energy source). "
            "2. SWITCH: opens or closes the circuit (controller). "
            "3. BULB: electrical energy → light energy (output device). "
            "All three must be connected in a complete loop. "
            "(ಕೋಶ + ಸ್ವಿಚ್ + ದೀಪ = ಸರ್ಕ್ಯೂಟ್!)"
        )
    },
    {
        "id": "torch_q3",
        "challenge": (
            "Show the ASSEMBLED view. What would happen if you removed the switch from the torch? "
            "Would the bulb stay ON, stay OFF, or could you control it?\n\n"
            "(ಜೋಡಿಸಿದ ನೋಟ ತೋರಿಸಿ — ಸ್ವಿಚ್ ತೆಗೆದರೆ ಏನಾಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "assembled"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'assembled'. A switch controls whether the circuit loop is complete or broken.",
            "attempt_2": "Choose 'assembled': Without a switch, either the circuit is permanently complete (bulb always ON) or permanently broken (bulb always OFF). No control possible.",
            "attempt_3": "Set 'initialState=assembled': Without a switch, you'd have to physically connect/disconnect a wire to turn the bulb on/off. Very inconvenient — switch provides easy control."
        },
        "concept_reminder": (
            "Without a switch: no control over the circuit. "
            "If wires are touching → circuit always complete → bulb always ON → battery drains fast. "
            "If wires not touching → circuit always open → bulb always OFF. "
            "Switch allows convenient ON/OFF control without physically touching live wires. "
            "(ಸ್ವಿಚ್ = ಸರ್ಕ್ಯೂಟ್ ನಿಯಂತ್ರಕ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["electric_cell_kn"] = [
    {
        "id": "cell_q1",
        "challenge": (
            "Highlight the POSITIVE terminal of the cell. "
            "Describe its physical appearance — how would you identify the positive terminal "
            "of a real battery by just looking at it?\n\n"
            "(ಧನ ಟರ್ಮಿನಲ್ ತೋರಿಸಿ — ನಿಜ ಜೀವನದ ಬ್ಯಾಟರಿಯಲ್ಲಿ ಅದನ್ನು ಹೇಗೆ ಗುರುತಿಸುತ್ತೀರಿ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "positive"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'positive'. Look at the highlighted terminal — it has a protruding metal bump/cap.",
            "attempt_2": "Choose 'positive': The positive terminal has a small metal cap (bump) sticking out, usually marked with '+' symbol.",
            "attempt_3": "Set 'initialState=positive': Physical identification: Look for the BUMP/CAP at one end = positive (+). The flat disc at the other end = negative (−)."
        },
        "concept_reminder": (
            "Positive terminal (+): Small metal cap or bump protruding from one end. Marked with + sign. "
            "In circuit symbol: LONG line represents positive. "
            "Current flows OUT of the + terminal into the external circuit. "
            "Memory tip: + has an extra line (bump sticks OUT). "
            "(ಲೋಹ ಟೋಪಿ / ಬಂಪ್ = ಧನ (+) ಟರ್ಮಿನಲ್!)"
        )
    },
    {
        "id": "cell_q2",
        "challenge": (
            "Highlight the NEGATIVE terminal. Compare it to the positive terminal — "
            "what is the key physical difference between them?\n\n"
            "(ಋಣ ಟರ್ಮಿನಲ್ ತೋರಿಸಿ — ಧನ ಮತ್ತು ಋಣ ಟರ್ಮಿನಲ್‌ಗಳ ನಡುವಿನ ವ್ಯತ್ಯಾಸ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "negative"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'negative'. The negative terminal is the flat metal disc at the other end of the cell.",
            "attempt_2": "Choose 'negative': (+) = bump/cap sticking out. (−) = flat metal plate, no protrusion. In symbol: short line = negative.",
            "attempt_3": "Set 'initialState=negative': Key difference: BUMP = positive; FLAT = negative. Current enters the cell at the − terminal after completing the external circuit."
        },
        "concept_reminder": (
            "Negative terminal (−): Flat metal disc at the base. Marked with − sign. "
            "In circuit symbol: SHORT line represents negative. "
            "Current flows INTO the − terminal from the external circuit. "
            "Key difference from +: NO bump/protrusion — completely flat. "
            "(ಚಪ್ಪಟೆ ತಟ್ಟೆ = ಋಣ (−) ಟರ್ಮಿನಲ್!)"
        )
    },
    {
        "id": "cell_q3",
        "challenge": (
            "Show the CIRCUIT view (both terminals highlighted). "
            "Draw and explain the circuit symbol of an electric cell — which line is longer and what does it represent?\n\n"
            "(ಸರ್ಕ್ಯೂಟ್ ದೃಶ್ಯ ತೋರಿಸಿ — ವಿದ್ಯುತ್ ಕೋಶದ ಸರ್ಕ್ಯೂಟ್ ಚಿಹ್ನೆ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "circuit"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'circuit'. Watch both terminals highlight and the current flow arrow appear.",
            "attempt_2": "Choose 'circuit': Cell symbol = two parallel vertical lines. LONG line = positive (+). SHORT line = negative (−). Current arrow goes from + to − externally.",
            "attempt_3": "Set 'initialState=circuit': Long line (+) pushed current out. Short line (−) receives current back. The symbol tells you both identity and current direction."
        },
        "concept_reminder": (
            "Cell circuit symbol: TWO PARALLEL LINES — long and short. "
            "LONG line = POSITIVE terminal (+) = current exits here. "
            "SHORT line = NEGATIVE terminal (−) = current returns here. "
            "The direction of the current arrow in circuit diagrams: always from + to − outside the cell. "
            "(ಉದ್ದ ರೇಖೆ = + | ಕಿರಿದಾದ ರೇಖೆ = − | ಪ್ರವಾಹ + ರಿಂದ − ಕ್ಕೆ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["battery_connection_kn"] = [
    {
        "id": "battery_q1",
        "challenge": (
            "Show a SINGLE CELL (1 cell) powering the bulb. "
            "What is the voltage and how bright is the bulb? "
            "Is a single cell called a 'battery'?\n\n"
            "(ಒಂದು ಕೋಶ ಆಯ್ಕೆ ಮಾಡಿ — ವೋಲ್ಟೇಜ್ ಎಷ್ಟು? ಒಂದು ಕೋಶವನ್ನು 'ಬ್ಯಾಟರಿ' ಎಂದು ಕರೆಯಬಹುದೇ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "one_cell"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'one_cell'. Observe the bulb brightness and voltage reading — 1 cell = 1.5V.",
            "attempt_2": "Choose 'one_cell': 1 cell × 1.5V = 1.5V. Bulb glows dimly. Technically, a single cell is NOT a battery — a battery needs 2+ cells.",
            "attempt_3": "Set 'initialState=one_cell': One cell = 1.5V, dim glow. A battery = 2 or more cells connected. Common mistake: we call AA cells 'batteries' but they are actually single cells."
        },
        "concept_reminder": (
            "Single cell = 1.5V. Bulb glows but dimly. "
            "IMPORTANT: A single cell is technically NOT a battery. "
            "Battery = 2+ cells connected in series. "
            "Common misuse: people call AA cells 'batteries' but they are individual cells. "
            "(ಒಂದು ಕೋಶ = 1.5V | ಬ್ಯಾಟರಿ = 2+ ಕೋಶಗಳು!)"
        )
    },
    {
        "id": "battery_q2",
        "challenge": (
            "Connect TWO cells in series. What is the total voltage? "
            "Compare the bulb brightness to the single-cell case.\n\n"
            "(ಎರಡು ಕೋಶ ಜೋಡಿಸಿ — ಒಟ್ಟು ವೋಲ್ಟೇಜ್ ಎಷ್ಟು? ಒಂದು ಕೋಶಕ್ಕೆ ಹೋಲಿಸಿದರೆ ದೀಪ ಹೇಗಿದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "two_cells"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'two_cells'. Watch the voltage display change and the bulb get brighter.",
            "attempt_2": "Choose 'two_cells': 2 × 1.5V = 3V. The bulb glows more brightly because higher voltage pushes more current through the circuit.",
            "attempt_3": "Set 'initialState=two_cells': Voltage doubles (3V), current increases, bulb glows twice as bright. Series connection = voltages add."
        },
        "concept_reminder": (
            "Two cells in series: 1.5V + 1.5V = 3V. "
            "Connection: Cell 1 (+) → Cell 2 (−). One end of cell 1 connects to one end of cell 2. "
            "More voltage → more current → more energy to bulb → BRIGHTER. "
            "This is why TV remotes use 2 cells — needs 3V to work. "
            "(2 ಕೋಶ = 3V | ಹೆಚ್ಚು ವೋಲ್ಟೇಜ್ = ಹೆಚ್ಚು ಹೊಳೆಯುವ ಬಲ್ಬ್!)"
        )
    },
    {
        "id": "battery_q3",
        "challenge": (
            "Connect THREE cells. What is the total voltage? "
            "Explain the rule for connecting cells in series — which terminal connects to which?\n\n"
            "(ಮೂರು ಕೋಶ ಜೋಡಿಸಿ — ಒಟ್ಟು ವೋಲ್ಟೇಜ್ ಎಷ್ಟು? ಸರಣಿ ಸಂಪರ್ಕದ ನಿಯಮ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [{"parameter": "initialState", "operator": "==", "value": "three_cells"}],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": "Set 'initialState' to 'three_cells'. Observe 3 × 1.5V = 4.5V and notice the brightest bulb.",
            "attempt_2": "Choose 'three_cells': Rule for series: each cell's + terminal connects to the NEXT cell's − terminal. Polarity must alternate. Total = 4.5V.",
            "attempt_3": "Set 'initialState=three_cells': (+)cell1(−)→(+)cell2(−)→(+)cell3(−). + of one always to − of next. Total = 4.5V. Brightest bulb!"
        },
        "concept_reminder": (
            "Three cells in series: 1.5V + 1.5V + 1.5V = 4.5V. "
            "SERIES RULE: (+) of one cell always connects to (−) of the next cell. "
            "If polarity is wrong (+ to +), cells work against each other and voltage is REDUCED. "
            "Battery compartments show + and − markings for this exact reason. "
            "(3 ಕೋಶ = 4.5V | ಧನ (+) → ಋಣ (−) → ಅಗತ್ಯ ನಿಯಮ!)"
        )
    }
]


# =============================================================================
# LAMP TYPES — Config
# =============================================================================
SIMULATIONS_KN["lamp_types_kn"] = {
    "id": "lamp_types_kn",
    "title": "ದೀಪ ಪ್ರಕಾರಗಳು (Lamp Types — Incandescent vs LED)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation6_lamp_types_kn.html",
    "description": (
        "ಇನ್ಕ್ಯಾಂಡಿಸೆಂಟ್ ಬಲ್ಬ್ ಮತ್ತು LED ಅನ್ನು ಆನ್/ಆಫ್ ಮಾಡಿ ಹೋಲಿಕೆ ಮಾಡಿ. "
        "Compare an incandescent bulb (filament-heated) and an LED (semiconductor) by toggling "
        "each lamp on and off. Observe how the incandescent filament glows orange-red while the "
        "LED emits green light without any filament. A comparison table shows efficiency, polarity "
        "requirements, and lifespan differences."
    ),
    "cannot_demonstrate": [
        "Quantitative power consumption measurement (watts)",
        "Heat generation measured in degrees",
        "Actual semiconductor physics inside an LED",
    ],
    "initial_params": {"initialState": "incandescent_off", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Lamp State",
            "range": "incandescent_off, incandescent_on, led_off, led_on",
            "url_key": "initialState",
            "effect": (
                "Sets which lamp is selected and whether it is switched on.\n"
                "  'incandescent_off' → incandescent bulb selected, switch off (default)\n"
                "  'incandescent_on'  → incandescent bulb selected, switch on (filament glows)\n"
                "  'led_off'          → LED selected, switch off\n"
                "  'led_on'           → LED selected, switch on (LED emits green light)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card inside the simulation.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view)"
            )
        }
    },
    "concepts": [
        {
            "id": "incandescent_working",
            "title": "Incandescent Bulb — Filament Heating",
            "description": (
                "An incandescent bulb contains a thin tungsten wire (filament). When electric "
                "current flows through it, the filament heats up to about 2500°C and glows white-hot, "
                "producing light."
            ),
            "key_insight": (
                "Incandescent bulbs waste ~90% of electrical energy as heat. Only ~10% becomes "
                "visible light. The filament works in ANY polarity — it doesn't matter which "
                "way current flows."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "led_working",
            "title": "LED — Semiconductor Light Emission",
            "description": (
                "An LED (Light Emitting Diode) contains a semiconductor chip. When current flows "
                "through the chip in the correct direction, it emits light directly without any "
                "filament or heat."
            ),
            "key_insight": (
                "LEDs convert ~90% of electrical energy directly to light — almost no heat waste. "
                "POLARITY MATTERS: the long leg must connect to (+) and short leg to (−). "
                "Reversed polarity = no light."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "lamp_comparison",
            "title": "Incandescent vs LED — Why LED Wins",
            "description": (
                "A side-by-side comparison of efficiency, lifespan, and polarity requirements "
                "shows why LEDs have replaced incandescent bulbs in most applications."
            ),
            "key_insight": (
                "LED lifespan (~50,000 hours) is 50× longer than incandescent (~1,000 hours). "
                "LEDs use far less electricity for the same brightness. "
                "The only trade-off is polarity sensitivity — LEDs require correct (+/−) connection."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# SIMPLE CIRCUIT — Config
# =============================================================================
SIMULATIONS_KN["simple_circuit_kn"] = {
    "id": "simple_circuit_kn",
    "title": "ಸರಳ ವಿದ್ಯುತ್ ಸರ್ಕ್ಯೂಟ್ (Simple Electric Circuit)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation7_simple_circuit_kn.html",
    "description": (
        "ಕೋಶ, ಬಲ್ಬ್, ಸ್ವಿಚ್ ಮತ್ತು ತಂತಿಗಳನ್ನು ಸರ್ಕ್ಯೂಟ್ ಪ್ರದೇಶದಲ್ಲಿ ಇರಿಸಿ ಸರ್ಕ್ಯೂಟ್ ನಿರ್ಮಿಸಿ ಮತ್ತು ಪರೀಕ್ಷಿಸಿ. "
        "Build a simple electric circuit by placing a cell, bulb, switch and wires "
        "onto the circuit board, then test the circuit to see the bulb light up and "
        "current flow animation. Teaches what components are needed for a complete circuit."
    ),
    "cannot_demonstrate": [
        "Incomplete circuit failure (short circuit vs open circuit distinction)",
        "Parallel circuit connections",
        "Quantitative voltage or current values",
    ],
    "initial_params": {"initialState": "empty", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Circuit State",
            "range": "empty, built, tested",
            "url_key": "initialState",
            "effect": (
                "Sets the pre-loaded state of the circuit builder.\n"
                "  'empty'  → blank circuit board, no components placed (default)\n"
                "  'built'  → auto-places all four components (cell, bulb, switch, wires)\n"
                "  'tested' → auto-places all components AND runs the circuit test (bulb glows)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "circuit_components",
            "title": "Four Essential Circuit Components",
            "description": (
                "A basic electric circuit requires four components: a cell (energy source), "
                "a bulb (load/output), a switch (controller), and wires (conductors that connect everything)."
            ),
            "key_insight": (
                "Remove any ONE component and the circuit is incomplete — no current flows and "
                "the bulb stays off. ALL four must be present and connected in a closed loop."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "closed_loop",
            "title": "Complete Circuit = Closed Loop",
            "description": (
                "Electric current can only flow when there is a complete, unbroken loop "
                "from the cell's positive terminal, through the bulb and switch, back to "
                "the cell's negative terminal."
            ),
            "key_insight": (
                "Think of current like water in a pipe — it needs a complete loop with no "
                "gaps. Breaking the loop anywhere (opening the switch, removing a wire) "
                "instantly stops all current flow."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "switch_function",
            "title": "Role of the Switch in a Circuit",
            "description": (
                "A switch controls the circuit by either closing the gap (completing the loop, "
                "current flows) or opening the gap (breaking the loop, no current)."
            ),
            "key_insight": (
                "Switch CLOSED = circuit complete = current flows = bulb ON. "
                "Switch OPEN = circuit broken = no current = bulb OFF. "
                "The switch gives us convenient control without touching live wires."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# ELECTRIC SWITCH — Config
# =============================================================================
SIMULATIONS_KN["electric_switch_kn"] = {
    "id": "electric_switch_kn",
    "title": "ವಿದ್ಯುತ್ ಸ್ವಿಚ್ (Electric Switch)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation8_electric_switch_kn.html",
    "description": (
        "ಸ್ವಿಚ್ ಟ್ಯಾಪ್ ಮಾಡಿ ಸರ್ಕ್ಯೂಟ್ ತೆರೆದ/ಮುಚ್ಚಿದ ಸ್ಥಿತಿಯನ್ನು ವೀಕ್ಷಿಸಿ — ಲಿವರ್, ಪುಶ್ ಮತ್ತು ಟಾಗಲ್ ಸ್ವಿಚ್ ಪ್ರಕಾರಗಳನ್ನು ಪ್ರಯೋಗಿಸಿ. "
        "Tap the switch to toggle the circuit between open (OFF) and closed (ON) states. "
        "Observe the bulb turning on/off and the current flow indicator. "
        "Explore three types of switches: lever, push-button, and toggle switch."
    ),
    "cannot_demonstrate": [
        "Quantitative current or voltage values",
        "Multi-way switching (two switches controlling one bulb)",
        "Electronic (transistor-based) switching",
    ],
    "initial_params": {"initialState": "off", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Switch State",
            "range": "off, on",
            "url_key": "initialState",
            "effect": (
                "Sets the initial state of the switch.\n"
                "  'off' → switch open, circuit broken, bulb OFF (default)\n"
                "  'on'  → switch closed, circuit complete, bulb ON (current flows)"
            )
        },
        "switchType": {
            "label": "Switch Type",
            "range": "lever, push, toggle",
            "url_key": "switchType",
            "effect": (
                "Selects which type of switch to display.\n"
                "  'lever'  → lever switch (rockers in walls) — default\n"
                "  'push'   → push-button switch (doorbells, calculators)\n"
                "  'toggle' → toggle switch (used on electronic boards)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "switch_off_state",
            "title": "Open Switch — Circuit Broken (OFF)",
            "description": (
                "When a switch is OPEN (OFF), there is a physical gap or break in the "
                "circuit. No current can flow across the gap, so the bulb stays dark."
            ),
            "key_insight": (
                "An open switch = a gap in the wire. Electrons cannot jump a gap — "
                "they need a solid conductor path. Even one tiny break in the circuit "
                "is enough to stop ALL current flow."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "switch_on_state",
            "title": "Closed Switch — Circuit Complete (ON)",
            "description": (
                "When a switch is CLOSED (ON), it creates a conducting bridge across "
                "the gap, completing the circuit loop and allowing current to flow "
                "through the bulb."
            ),
            "key_insight": (
                "A closed switch = a conducting bridge. Current can now flow the complete "
                "loop: cell (+) → wire → closed switch → wire → bulb → wire → cell (−). "
                "The bulb converts electrical energy to light and heat."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "switch_types",
            "title": "Types of Switches — Lever, Push, Toggle",
            "description": (
                "Different switch mechanisms all do the same job (open/close a circuit) "
                "but are designed for different situations: lever switches for walls, "
                "push-buttons for doorbells, toggle switches for electronics."
            ),
            "key_insight": (
                "All switches share one principle: they physically make or break an "
                "electrical connection. The mechanism differs (flip, press, slide) but "
                "the effect is the same — completing or breaking the circuit loop."
            ),
            "related_params": ["initialState", "switchType", "showHints"]
        }
    ]
}

# =============================================================================
# CIRCUIT SYMBOLS — Config
# =============================================================================
SIMULATIONS_KN["circuit_symbols_kn"] = {
    "id": "circuit_symbols_kn",
    "title": "ಸರ್ಕ್ಯೂಟ್ ಚಿಹ್ನೆಗಳು (Circuit Symbols)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter3_simulation9_circuit_symbols_kn.html",
    "description": (
        "ಸರ್ಕ್ಯೂಟ್ ಚಿತ್ರಗಳಲ್ಲಿ ಬಳಸಲಾಗುವ ಮಾನಕ ಚಿಹ್ನೆಗಳನ್ನು ಕಲಿಯಿರಿ — ಕೋಶ, ಬ್ಯಾಟರಿ, ಬಲ್ಬ್, LED, ಸ್ವಿಚ್, ತಂತಿ. "
        "Learn the standard circuit diagram symbols used in electrical engineering: "
        "cell, battery, bulb, LED, open switch, closed switch, wire, and wire crossing. "
        "Click each symbol card to see its detailed diagram representation, physical appearance, "
        "and usage explanation. Includes a built-in quiz."
    ),
    "cannot_demonstrate": [
        "Symbols for resistors, capacitors, or transistors",
        "Drawing full circuit diagrams interactively",
        "Ohm's law or quantitative circuit analysis",
    ],
    "initial_params": {"initialState": "cell", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Symbol View",
            "range": "cell, battery, bulb, led, switch_open, switch_closed, wire, wire_cross",
            "url_key": "initialState",
            "effect": (
                "Sets which circuit symbol is displayed in the detail panel on page load.\n"
                "  'cell'          → cell symbol (long + short parallel lines)\n"
                "  'battery'       → battery symbol (multiple cell pairs)\n"
                "  'bulb'          → bulb/lamp symbol (circle with X inside)\n"
                "  'led'           → LED symbol (triangle with arrow)\n"
                "  'switch_open'   → open switch symbol (gap in line)\n"
                "  'switch_closed' → closed switch symbol (complete line)\n"
                "  'wire'          → connecting wire symbol (straight line)\n"
                "  'wire_cross'    → crossing wires with no connection symbol"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show concept card (default)\n"
                "  false → hide concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "cell_battery_symbols",
            "title": "Cell and Battery Circuit Symbols",
            "description": (
                "In circuit diagrams, a CELL is drawn as one long line (positive terminal) "
                "and one short line (negative terminal). A BATTERY is multiple such pairs."
            ),
            "key_insight": (
                "Long line = positive terminal; short line = negative terminal. "
                "A single cell symbol = one long + one short line. "
                "A battery symbol = two or more repeated pairs. "
                "This notation is identical worldwide — every electrician uses it."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "switch_symbols",
            "title": "Open and Closed Switch Symbols",
            "description": (
                "An OPEN switch is drawn as a line with a visible gap or a lever raised at an "
                "angle. A CLOSED switch is drawn as a complete unbroken line or lever lying flat."
            ),
            "key_insight": (
                "The symbol tells you the state: gap in symbol = gap in circuit = OFF. "
                "Complete line in symbol = complete circuit = ON. "
                "Just by reading the diagram you know whether current is flowing."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "component_symbols_overview",
            "title": "Standardised Symbols Enable Universal Circuit Diagrams",
            "description": (
                "All circuit components have agreed international symbols. Engineers in "
                "any country can read the same circuit diagram without a language barrier."
            ),
            "key_insight": (
                "Bulb = circle with X; LED = triangle with arrow + light rays; "
                "wire = straight line; crossing wires (no connection) = lines crossing WITHOUT a dot. "
                "A DOT at a junction means wires ARE connected — no dot means they cross but don't connect."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# METALS AND NON-METALS APPLICATIONS — Config
# =============================================================================
SIMULATIONS_KN["materials_applications_kn"] = {
    "id": "materials_applications_kn",
    "title": "ಲೋಹ ಮತ್ತು ಅಲೋಹ ಬಳಕೆಗಳು (Applications of Metals & Non-metals)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation10_applications_kn.html",
    "description": (
        "ಲೋಹ, ಅಲೋಹ ಮತ್ತು ಎರಡೂ ಬಳಸುವ ವಸ್ತುಗಳ ನೈಜ-ಜೀವನ ಅನ್ವಯಗಳನ್ನು ಅನ್ವೇಷಿಸಿ. "
        "Explore real-world applications of metals, non-metals, and everyday objects that "
        "use both. Click category tabs (Metals / Non-metals / Both) to discover applications "
        "like electrical wires (copper), insulation (rubber), and tools (metal head + wooden handle). "
        "A matching quiz tests understanding. Includes the Iron Pillar of Delhi fun fact."
    ),
    "cannot_demonstrate": [
        "Atomic structure differences between metals and non-metals",
        "Chemical reactions of metals",
        "Alloy compositions",
        "Quantitative physical property measurements",
    ],
    "initial_params": {"initialState": "metals", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Category",
            "range": "metals, nonmetals, both",
            "url_key": "initialState",
            "effect": (
                "Sets the active category tab when the simulation loads.\n"
                "  'metals'    → shows metal applications (wires, cookware, bells, jewellery)\n"
                "  'nonmetals' → shows non-metal applications (insulation, oxygen, chlorine, iodine)\n"
                "  'both'      → shows everyday items combining metals and non-metals (tools, pans, plugs)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of concept card and fun-fact panel.\n"
                "  true  → show concept card and Iron Pillar fun fact (default)\n"
                "  false → hide both panels (focused view)"
            )
        }
    },
    "concepts": [
        {
            "id": "metal_properties_uses",
            "title": "Metals — Properties and Applications",
            "description": (
                "Metals are used where their key properties are needed: electrical conductivity "
                "(copper wires), heat conductivity (aluminium cookware), malleability/ductility "
                "(jewellery, bells), and strength (construction)."
            ),
            "key_insight": (
                "Match property to application: conductivity → wires; malleability → sheets; "
                "ductility → wires drawn thin; sonority → bells. Every metal application "
                "exploits one or more of these physical properties."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "nonmetal_properties_uses",
            "title": "Non-metals — Properties and Applications",
            "description": (
                "Non-metals are used for their poor conductivity (rubber/plastic insulation), "
                "essential life functions (oxygen for breathing), and chemical properties "
                "(chlorine for disinfection, iodine as antiseptic)."
            ),
            "key_insight": (
                "Non-metals protect us from electricity (rubber handle, plastic casing) "
                "and sustain life (oxygen, chlorine in water). Their low conductivity, "
                "which seems like a weakness, is actually their most useful property."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "combined_applications",
            "title": "Combining Metals and Non-metals in Everyday Objects",
            "description": (
                "Many everyday tools deliberately combine a metal component (for strength/conductivity) "
                "with a non-metal component (for insulation/grip): frying pans, electric plugs, "
                "hammers, pencils."
            ),
            "key_insight": (
                "Engineering principle: use each material where its property is an advantage. "
                "Electric plug = metal pins (conduct current) + plastic body (insulate the user). "
                "Removing either material makes the object either non-functional or dangerous."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# QUIZ QUESTIONS — LAMP TYPES
# =============================================================================
QUIZ_QUESTIONS_KN["lamp_types_kn"] = [
    {
        "id": "lamp_q1",
        "challenge": (
            "Switch the INCANDESCENT bulb ON. Describe what you observe — "
            "what part of the bulb glows and why?\n\n"
            "(ಇನ್ಕ್ಯಾಂಡಿಸೆಂಟ್ ಬಲ್ಬ್ ಆನ್ ಮಾಡಿ — ಯಾವ ಭಾಗ ಬೆಳಗುತ್ತದೆ ಮತ್ತು ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "incandescent_on"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'incandescent_on'. Watch the glass bulb turn yellow "
                "and the filament glow orange-red — the filament is heating up to ~2500°C!"
            ),
            "attempt_2": (
                "Choose 'incandescent_on': The FILAMENT (thin tungsten wire inside) heats "
                "when current flows, glowing white-hot and producing light."
            ),
            "attempt_3": (
                "Set 'initialState=incandescent_on': Current → filament heats → glows. "
                "This is the incandescent (ಫಿಲಾಮೆಂಟ್ ಜ್ವಲಿಸುವ) state."
            )
        },
        "concept_reminder": (
            "Incandescent bulb: electric current heats the filament (tungsten wire) to ~2500°C. "
            "The hot filament glows white, producing light. BUT ~90% of energy is wasted as heat. "
            "(ಫಿಲಾಮೆಂಟ್ = ತೆಳು ತಂತಿ | ಬಿಸಿ = ಬೆಳಕು!)"
        )
    },
    {
        "id": "lamp_q2",
        "challenge": (
            "Now switch to the LED and turn it ON. "
            "Compare what you see with the incandescent — does the LED have a filament? "
            "What colour does it glow?\n\n"
            "(LED ಆನ್ ಮಾಡಿ — ಅದರಲ್ಲಿ ಫಿಲಾಮೆಂಟ್ ಇದೆಯೇ? ಯಾವ ಬಣ್ಣ ಹೊಳೆಯುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "led_on"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'led_on'. Observe the LED dome turn green — "
                "no filament glows; the semiconductor chip itself emits light."
            ),
            "attempt_2": (
                "Choose 'led_on': The LED glows green from the semiconductor chip, "
                "NOT from a heated filament. No heat = much more efficient."
            ),
            "attempt_3": (
                "Set 'initialState=led_on': LED on = chip emits light directly. "
                "No orange glow, no filament. LED (ಸೆಮಿಕಂಡಕ್ಟರ್) ≠ incandescent (ಫಿಲಾಮೆಂಟ್)."
            )
        },
        "concept_reminder": (
            "LED = Light Emitting Diode. A semiconductor chip emits light when current flows "
            "in the correct direction — NO filament, NO heat. ~90% efficiency vs ~10% for incandescent. "
            "POLARITY: long leg = + (ಧನ), short leg = − (ಋಣ). Wrong polarity = no light! "
            "(LED = ಸೆಮಿಕಂಡಕ್ಟರ್ ಚಿಪ್ | ಫಿಲಾಮೆಂಟ್ ಇಲ್ಲ | ಹೆಚ್ಚು ಕಾರ್ಯಕ್ಷಮ!)"
        )
    },
    {
        "id": "lamp_q3",
        "challenge": (
            "Set the simulation to show the LED in OFF state. "
            "Explain: why does an LED need correct polarity to work, "
            "but an incandescent bulb does not?\n\n"
            "(LED ಆಫ್ ಸ್ಥಿತಿ ತೋರಿಸಿ — LED ಗೆ ಧ್ರುವತೆ ಯಾಕೆ ಅಗತ್ಯ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "led_off"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'led_off'. The LED is selected but the switch is off. "
                "Think about WHY an LED is a DIODE — it only conducts one way."
            ),
            "attempt_2": (
                "Choose 'led_off': Diode = one-way conductor. Current can only flow from "
                "long leg (+) to short leg (−). Reversed = blocked. Incandescent = resistor = works both ways."
            ),
            "attempt_3": (
                "Set 'initialState=led_off': LED is a DIODE — semiconductor with a P-N junction "
                "that only allows current in ONE direction. Incandescent filament is just a resistor — "
                "direction does not matter."
            )
        },
        "concept_reminder": (
            "LED = DIODE = one-directional conductor. The P-N junction inside only allows "
            "current when (+) connects to the P-side (long leg). Reversed = junction blocks current = no light. "
            "Incandescent filament = simple resistor = conducts in both directions = polarity irrelevant. "
            "(LED: ಉದ್ದ ಕಾಲು + ⟶ ಮಾತ್ರ | ಕಿರಿದಾದ ಕಾಲು − ⟵ ಮಾತ್ರ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — SIMPLE CIRCUIT
# =============================================================================
QUIZ_QUESTIONS_KN["simple_circuit_kn"] = [
    {
        "id": "circuit_q1",
        "challenge": (
            "Start with an EMPTY circuit board. "
            "Name all four components needed to build a working simple circuit, and "
            "state the role of each component.\n\n"
            "(ಖಾಲಿ ಸರ್ಕ್ಯೂಟ್ ಬೋರ್ಡ್ ತೋರಿಸಿ — ಸರಳ ಸರ್ಕ್ಯೂಟ್‌ನ ನಾಲ್ಕು ಭಾಗಗಳು ಯಾವುವು?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "empty"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'empty'. Read the component panel — "
                "there are four components: cell, bulb, switch, wires."
            ),
            "attempt_2": (
                "Choose 'empty': (1) Cell — energy source. (2) Bulb — output device. "
                "(3) Switch — controller. (4) Wires — conductors that connect all three."
            ),
            "attempt_3": (
                "Set 'initialState=empty': Think of a circuit as a powered loop. "
                "You need: a PUMP (cell), a LOAD (bulb), a VALVE (switch), and PIPES (wires)."
            )
        },
        "concept_reminder": (
            "Four essential circuit components: "
            "CELL (energy source, chemical → electrical), BULB (load, electrical → light), "
            "SWITCH (controller, opens/closes circuit), WIRES (conductors, connect everything in a loop). "
            "Missing any one = circuit is incomplete = no current = bulb off. "
            "(ಕೋಶ + ಬಲ್ಬ್ + ಸ್ವಿಚ್ + ತಂತಿ = ಪೂರ್ಣ ಸರ್ಕ್ಯೂಟ್!)"
        )
    },
    {
        "id": "circuit_q2",
        "challenge": (
            "Build the circuit by placing ALL four components. "
            "Before testing, predict: in which direction will the current flow "
            "around the circuit once the switch is closed?\n\n"
            "(ಎಲ್ಲ ನಾಲ್ಕು ಭಾಗಗಳನ್ನು ಇರಿಸಿ — ಪ್ರವಾಹ ಯಾವ ದಿಕ್ಕಿನಲ್ಲಿ ಹರಿಯುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "built"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'built'. Watch all four components auto-place — "
                "cell, bulb, switch, and wires all in position."
            ),
            "attempt_2": (
                "Choose 'built': Conventional current flows from cell (+) through the "
                "external circuit (bulb, switch) and returns to cell (−). It's always (+) to (−) externally."
            ),
            "attempt_3": (
                "Set 'initialState=built': Current direction: cell (+) → top wire → bulb → "
                "right wire → switch → bottom wire → cell (−). Counterclockwise in this layout."
            )
        },
        "concept_reminder": (
            "Conventional current direction: always from (+) terminal of cell, "
            "through external circuit components (bulb, switch), and back to (−) terminal. "
            "Current always flows from higher potential (+) to lower potential (−) externally. "
            "Inside the cell, current flows from − to + (the cell does work to push charges). "
            "(ಪ್ರವಾಹ: + → ಬಾಹ್ಯ ಸರ್ಕ್ಯೂಟ್ → − | ಕೋಶ ಒಳಗೆ − → +!)"
        )
    },
    {
        "id": "circuit_q3",
        "challenge": (
            "Now TEST the completed circuit. Observe what happens when the circuit "
            "is tested. What does the bulb lighting up confirm about the circuit?\n\n"
            "(ಸರ್ಕ್ಯೂಟ್ ಪರೀಕ್ಷಿಸಿ — ಬಲ್ಬ್ ಬೆಳಗಿದರೆ ಅದು ಏನನ್ನು ಖಚಿತಪಡಿಸುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "tested"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'tested'. Watch all components auto-place and "
                "the circuit test run — the bulb should glow and current arrows appear."
            ),
            "attempt_2": (
                "Choose 'tested': A glowing bulb confirms the circuit loop is COMPLETE "
                "and unbroken. Current is flowing through all components."
            ),
            "attempt_3": (
                "Set 'initialState=tested': Bulb ON = closed loop = current flowing = "
                "all connections correct. The current arrow animation shows the flow direction."
            )
        },
        "concept_reminder": (
            "A lit bulb is the proof of a complete circuit. It means: "
            "(1) All 4 components are connected correctly. "
            "(2) The circuit loop is unbroken — no gaps in any connection. "
            "(3) Current is flowing from (+) through bulb → switch → back to (−). "
            "Remove any wire or component → bulb off immediately. "
            "(ಬಲ್ಬ್ ಬೆಳಕು = ಪೂರ್ಣ ಸರ್ಕ್ಯೂಟ್ ಧೃಢೀಕರಣ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — ELECTRIC SWITCH
# =============================================================================
QUIZ_QUESTIONS_KN["electric_switch_kn"] = [
    {
        "id": "switch_q1",
        "challenge": (
            "Show the switch in the OFF state. Explain — using the circuit diagram — "
            "exactly WHY the bulb does not glow when the switch is open.\n\n"
            "(ಸ್ವಿಚ್ ಆಫ್ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಬಲ್ಬ್ ಯಾಕೆ ಬೆಳಗುವುದಿಲ್ಲ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "off"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'off'. Observe the top wire (going to the switch) — "
                "it stays grey/inactive. The current cannot reach the bulb."
            ),
            "attempt_2": (
                "Choose 'off': The open switch creates a GAP in the circuit loop. "
                "Electrons cannot jump a gap — current stops completely."
            ),
            "attempt_3": (
                "Set 'initialState=off': Open switch = broken loop = zero current. "
                "The state card shows 'ತೆರೆದ ಸರ್ಕ್ಯೂಟ್' (open circuit)."
            )
        },
        "concept_reminder": (
            "Open switch (OFF) = physical gap in the circuit. "
            "Electrons need a continuous conductor path — they CANNOT jump a gap. "
            "Result: current = 0 everywhere in the circuit, bulb is dark. "
            "Even one tiny gap stops all current in the ENTIRE loop. "
            "(ಅಂತರ = ಶೂನ್ಯ ಪ್ರವಾಹ = ಬಲ್ಬ್ ಆಫ್!)"
        )
    },
    {
        "id": "switch_q2",
        "challenge": (
            "Close the switch (turn it ON). Describe the change you see in "
            "the circuit diagram. What does 'closed circuit' mean physically?\n\n"
            "(ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ — ಸರ್ಕ್ಯೂಟ್‌ನಲ್ಲಿ ಯಾವ ಬದಲಾವಣೆ ಕಾಣುತ್ತೀರಿ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "on"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'on'. Watch the entire circuit light up green "
                "and the bulb glow — the closed switch bridged the gap."
            ),
            "attempt_2": (
                "Choose 'on': The switch lever moves to bridge the two contact points, "
                "creating a conducting path. The loop is now complete — current flows."
            ),
            "attempt_3": (
                "Set 'initialState=on': Closed switch = conducting bridge = complete loop. "
                "Current indicators appear. State card shows 'ಮುಚ್ಚಿದ ಸರ್ಕ್ಯೂಟ್' (closed circuit)."
            )
        },
        "concept_reminder": (
            "Closed switch (ON) = conducting bridge across what was a gap. "
            "The metal lever/contact physically touches both terminals, providing a "
            "continuous metal path for electrons to flow. "
            "Complete loop → current flows → bulb lights up → energy is transferred. "
            "(ಸ್ವಿಚ್ ಮುಚ್ಚಿದ = ಸೇತುವೆ = ಪ್ರವಾಹ = ಬಲ್ಬ್ ಆನ್!)"
        )
    },
    {
        "id": "switch_q3",
        "challenge": (
            "Explore the push-button switch type with the circuit ON. "
            "Give one real-world example of a push-button switch and explain "
            "why it is better than a lever switch for that application.\n\n"
            "(ಪುಶ್ ಬಟನ್ ಸ್ವಿಚ್ ಆನ್ ಸ್ಥಿತಿಯಲ್ಲಿ ತೋರಿಸಿ — ನೈಜ ಉದಾಹರಣೆ ಕೊಡಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "on"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'on' and 'switchType' to 'push'. "
                "Think of where you press and release a button — doorbell, keyboard key, calculator."
            ),
            "attempt_2": (
                "Choose 'on' + 'switchType=push': A doorbell uses a push-button "
                "because it should ring ONLY while pressed — momentary contact. "
                "A lever switch would stay ON continuously — wrong for a doorbell!"
            ),
            "attempt_3": (
                "Set 'initialState=on', 'switchType=push': Examples — doorbell (momentary press), "
                "computer keyboard (each key is a push-button switch). "
                "Push-button = momentary contact = circuit closes only while pressed."
            )
        },
        "concept_reminder": (
            "Three switch types: LEVER (stays in position — light switches), "
            "PUSH-BUTTON (momentary — springs back — doorbells, keyboards), "
            "TOGGLE (flip between positions — stays where you put it — electronics boards). "
            "All three do the same job (complete/break a circuit) by different mechanisms. "
            "The right switch for the job depends on whether you need a LATCHING or MOMENTARY action. "
            "(ಲಿವರ್ = ಸ್ಥಿರ | ಪುಶ್ = ಕ್ಷಣಿಕ | ಟಾಗಲ್ = ಹಿಡಿದ ಸ್ಥಾನ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — CIRCUIT SYMBOLS
# =============================================================================
QUIZ_QUESTIONS_KN["circuit_symbols_kn"] = [
    {
        "id": "symbols_q1",
        "challenge": (
            "Display the CELL symbol. Explain the circuit symbol for a cell — "
            "which line is longer, which is shorter, and what do they represent?\n\n"
            "(ಕೋಶ ಚಿಹ್ನೆ ತೋರಿಸಿ — ಉದ್ದ ಮತ್ತು ಕಿರಿದು ರೇಖೆ ಏನನ್ನು ಸೂಚಿಸುತ್ತವೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "cell"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'cell'. Look at the detailed symbol — "
                "two parallel vertical lines of different lengths."
            ),
            "attempt_2": (
                "Choose 'cell': LONG line = positive terminal (+). "
                "SHORT line = negative terminal (−). The longer line represents "
                "the higher-potential side where current exits."
            ),
            "attempt_3": (
                "Set 'initialState=cell': Long line = + (current exits here). "
                "Short line = − (current returns here). "
                "Memory tip: Long = positive (extra bit sticking out, like the metal cap bump)."
            )
        },
        "concept_reminder": (
            "Cell circuit symbol: two parallel lines — ONE LONG, ONE SHORT. "
            "LONG line = POSITIVE (+) terminal — current exits here. "
            "SHORT line = NEGATIVE (−) terminal — current enters here. "
            "This is a universal standard — every circuit diagram in the world uses this. "
            "(ಉದ್ದ ರೇಖೆ = + | ಕಿರಿದಾ ರೇಖೆ = − | ಜಾಗತಿಕ ಮಾನಕ!)"
        )
    },
    {
        "id": "symbols_q2",
        "challenge": (
            "Show the OPEN SWITCH symbol. If you see this symbol in a circuit diagram, "
            "what does it tell you about the state of the circuit — is current flowing?\n\n"
            "(ತೆರೆದ ಸ್ವಿಚ್ ಚಿಹ್ನೆ ತೋರಿಸಿ — ಇದು ಸರ್ಕ್ಯೂಟ್ ಬಗ್ಗೆ ಏನು ಹೇಳುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "switch_open"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'switch_open'. Observe the symbol — "
                "the lever is drawn at an angle, showing a GAP in the circuit path."
            ),
            "attempt_2": (
                "Choose 'switch_open': A raised lever = open switch = gap in circuit = "
                "NO current flowing. Any device in this circuit would be OFF."
            ),
            "attempt_3": (
                "Set 'initialState=switch_open': The gap in the switch symbol represents "
                "a physical break in the conducting path. Open switch anywhere in a series "
                "circuit stops current EVERYWHERE in that loop."
            )
        },
        "concept_reminder": (
            "Open switch symbol = lever drawn at an angle with a visible gap. "
            "Meaning: circuit is BROKEN at this point. Current = 0. Everything OFF. "
            "Closed switch symbol = lever lying flat, completing the line — current flows. "
            "Reading circuit diagrams: spot the switch symbol and its state to know if the circuit is live. "
            "(ಕೋನದ ಲಿವರ್ = ತೆರೆದ = ಆಫ್ | ಸಮ ಲಿವರ್ = ಮುಚ್ಚಿದ = ಆನ್!)"
        )
    },
    {
        "id": "symbols_q3",
        "challenge": (
            "Display the BATTERY symbol. How does the battery symbol differ from "
            "a single cell symbol, and what does that difference represent?\n\n"
            "(ಬ್ಯಾಟರಿ ಚಿಹ್ನೆ ತೋರಿಸಿ — ಇದು ಕೋಶ ಚಿಹ್ನೆಯಿಂದ ಹೇಗೆ ಭಿನ್ನ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "battery"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'battery'. Compare the symbol with the cell — "
                "a battery has MULTIPLE pairs of long-short lines."
            ),
            "attempt_2": (
                "Choose 'battery': Single cell = one long + one short line. "
                "Battery = TWO or more long-short pairs representing multiple cells in series."
            ),
            "attempt_3": (
                "Set 'initialState=battery': More line-pairs = more cells = more voltage. "
                "A 9V battery symbol has 6 pairs (6 × 1.5V = 9V). "
                "The symbol visually shows the number of cells!"
            )
        },
        "concept_reminder": (
            "Battery symbol = multiple cell symbols stacked together. "
            "Each long-short pair = one cell (1.5V). "
            "Count the pairs to find the number of cells. "
            "Battery of 4 cells = 4 pairs = 4 × 1.5V = 6V total. "
            "Key difference from cell: cell = 1 pair, battery = 2+ pairs. "
            "(ಬ್ಯಾಟರಿ = ಅನೇಕ ಕೋಶ ಚಿಹ್ನೆಗಳ ಜೋಡಣೆ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — MATERIALS APPLICATIONS
# =============================================================================
QUIZ_QUESTIONS_KN["materials_applications_kn"] = [
    {
        "id": "materials_q1",
        "challenge": (
            "Show the METALS category. Name one metal application and explain "
            "which specific property of the metal makes it suitable for that use.\n\n"
            "(ಲೋಹಗಳ ವರ್ಗ ತೋರಿಸಿ — ಒಂದು ಅನ್ವಯ ಮತ್ತು ಆ ಲೋಹದ ನಿರ್ದಿಷ್ಟ ಗುಣ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "metals"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'metals'. Look at the four metal application cards — "
                "electrical wires, cookware, bells, jewellery."
            ),
            "attempt_2": (
                "Choose 'metals': Electrical wires = copper/aluminium used because of "
                "ELECTRICAL CONDUCTIVITY. Cookware = aluminium because of HEAT CONDUCTIVITY + MALLEABILITY."
            ),
            "attempt_3": (
                "Set 'initialState=metals': Property-application pairs: "
                "Conductivity → wires; Heat conductivity → cookware; "
                "Sonority → bells; Malleability + lustre → jewellery."
            )
        },
        "concept_reminder": (
            "Metal properties and their applications: "
            "CONDUCTIVITY → electrical wires (copper/aluminium carry current). "
            "HEAT CONDUCTIVITY → cookware (aluminium/steel distribute heat evenly). "
            "MALLEABILITY → sheets (gold beaten into thin foil). "
            "DUCTILITY → wires (copper drawn into thin wire). "
            "SONORITY → bells (metal rings when struck). "
            "LUSTRE → jewellery (gold/silver shine). "
            "(ಲೋಹ ಗುಣ → ನಿರ್ದಿಷ್ಟ ಬಳಕೆ!)"
        )
    },
    {
        "id": "materials_q2",
        "challenge": (
            "Display NON-METALS applications. Why is rubber used to insulate electric "
            "cables instead of a metal? Which property makes rubber suitable?\n\n"
            "(ಅಲೋಹ ವರ್ಗ ತೋರಿಸಿ — ವಿದ್ಯುತ್ ತಂತಿ ರಕ್ಷಾಕವಚಕ್ಕೆ ರಬ್ಬರ್ ಯಾಕೆ ಬಳಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "nonmetals"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'nonmetals'. Look at the insulation card — "
                "rubber and plastic block electricity."
            ),
            "attempt_2": (
                "Choose 'nonmetals': Rubber is a POOR conductor of electricity (an insulator). "
                "It DOES NOT allow current to flow through it, protecting us from electric shock."
            ),
            "attempt_3": (
                "Set 'initialState=nonmetals': Rubber insulation property = "
                "high electrical resistance = poor conductivity. "
                "If metal was used as insulation, it would conduct current and cause a short circuit!"
            )
        },
        "concept_reminder": (
            "Non-metals like rubber and plastic are POOR electrical conductors (insulators). "
            "This property — which looks like a weakness — is exactly what makes them useful "
            "as cable insulation. They protect us from shock by blocking current from "
            "escaping the metal core wire. "
            "Other non-metal uses: oxygen (O₂) for breathing, chlorine (Cl) to disinfect water. "
            "(ಕಳಪೆ ವಾಹಕತೆ = ಉತ್ತಮ ರಕ್ಷಾಕವಚ!)"
        )
    },
    {
        "id": "materials_q3",
        "challenge": (
            "Show BOTH category. Pick one everyday object that combines metal AND "
            "non-metal parts. Explain why each material is chosen for its specific part.\n\n"
            "(ಎರಡೂ ವರ್ಗ ತೋರಿಸಿ — ಒಂದು ವಸ್ತು ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ಪ್ರತಿ ಭಾಗಕ್ಕೆ ವಸ್ತು ಯಾಕೆ ಎಂದು ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "both"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'both'. Look at the four combination cards — "
                "hammer, frying pan, electric plug, pencil."
            ),
            "attempt_2": (
                "Choose 'both': Electric plug = metal pins (conduct electricity to appliance) + "
                "plastic body (insulate the user). Each material does a DIFFERENT job."
            ),
            "attempt_3": (
                "Set 'initialState=both': Frying pan = metal body (conducts heat to food) + "
                "plastic handle (insulates cook's hand from heat). "
                "Design principle: metal where conductivity helps; non-metal where it would be dangerous."
            )
        },
        "concept_reminder": (
            "Everyday combination objects use metals and non-metals strategically: "
            "ELECTRIC PLUG: metal pins (conductivity) + plastic body (insulation). "
            "FRYING PAN: metal base (heat conductivity) + plastic handle (heat insulation). "
            "PENCIL: graphite/carbon core (marks paper — non-metal) + wooden barrel (grip). "
            "HAMMER: metal head (hardness to drive nails) + wooden handle (grip + heat insulation). "
            "Key insight: use each material exactly where ITS property gives an advantage. "
            "(ಲೋಹ ಕಾರ್ಯ ಮಾಡುವಲ್ಲಿ | ಅಲೋಹ ರಕ್ಷಿಸುವಲ್ಲಿ!)"
        )
    }
]

# =============================================================================
# MALLEABILITY — Config
# =============================================================================
SIMULATIONS_KN["malleability_kn"] = {
    "id": "malleability_kn",
    "title": "ನಮ್ಯತೆ (Malleability)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation1_malleability_kn.html",
    "description": (
        "ತಾಮ್ರ, ಅಲ್ಯೂಮಿನಿಯಂ, ಕಬ್ಬಿಣ, ಕಲ್ಲಿದ್ದಲು, ಸಲ್ಫರ್ ಮತ್ತು ಸೀಮೆಸುಣ್ಣ ಮೇಲೆ ಸುತ್ತಿಗೆ ಬಡಿದು ನಮ್ಯ ಮತ್ತು ಭಂಗುರ ವಸ್ತುಗಳ ವ್ಯತ್ಯಾಸ ಕಲಿಯಿರಿ. "
        "Hammer six materials (copper, aluminium, iron, coal, sulfur, chalk) "
        "to discover which are malleable (flatten into sheets) and which are brittle (shatter into pieces). "
        "Results are recorded in a comparison table. Teaches the key physical property that "
        "distinguishes metals (malleable) from non-metals (brittle) under mechanical force."
    ),
    "cannot_demonstrate": [
        "Quantitative force measurements",
        "Temperature effects on malleability",
        "Alloy malleability (only pure elements shown)",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Demonstration State",
            "range": "initial, metal_hammer, nonmetal_hammer",
            "url_key": "initialState",
            "effect": (
                "Sets which demonstration is auto-loaded.\n"
                "  'initial'        → blank experiment, no material selected (default)\n"
                "  'metal_hammer'   → auto-selects copper and hammers it → flattens (malleable)\n"
                "  'nonmetal_hammer'→ auto-selects coal and hammers it → shatters (brittle)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "malleability_definition",
            "title": "Malleability — Metals Flatten Under Force",
            "description": (
                "Malleability is the property of metals that allows them to be beaten or "
                "rolled into thin sheets without breaking. When a force is applied, the metal "
                "atoms (arranged in layers) slide over each other rather than snapping apart."
            ),
            "key_insight": (
                "Metal atoms sit in regular layered arrangements. Under pressure, these layers "
                "slide past each other — the metal deforms but does NOT break. "
                "This is why copper can be beaten into foil and gold into gold leaf."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "brittleness_nonmetals",
            "title": "Brittleness — Non-metals Shatter Under Force",
            "description": (
                "Non-metals like coal, sulfur, and chalk are brittle — they shatter into "
                "fragments when struck. Their atoms are rigidly bonded in fixed positions "
                "and cannot slide, so force causes fracture instead of deformation."
            ),
            "key_insight": (
                "Non-metal atoms are locked in rigid bonds — they cannot slip past each other. "
                "Instead, the material fractures along bond lines. "
                "This is why chalk snaps cleanly and sulfur crumbles when hammered."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "malleability_applications",
            "title": "Real-world Applications of Malleability",
            "description": (
                "Malleability explains many everyday uses of metals: aluminium foil in kitchens, "
                "copper pipes bent into shape, iron rolled into construction beams, "
                "gold beaten into ornamental leaf."
            ),
            "key_insight": (
                "If metals were brittle like coal, they could not be shaped into pipes, wires, "
                "or sheets. Malleability is the foundation of metalworking — every shaped "
                "metal product exploits this property."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# DUCTILITY — Config
# =============================================================================
SIMULATIONS_KN["ductility_kn"] = {
    "id": "ductility_kn",
    "title": "ಸೆಳೆತ / ಎಳೆಯಬಲ್ಲ ಗುಣ (Ductility)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation2_ductility_kn.html",
    "description": (
        "ತಾಮ್ರ, ಚಿನ್ನ, ಅಲ್ಯೂಮಿನಿಯಂ, ಕಲ್ಲಿದ್ದಲು, ಸಲ್ಫರ್ ಮತ್ತು ಮರವನ್ನು ತೆಳು ತಂತಿಯಾಗಿ ಎಳೆಯಲು ಪ್ರಯತ್ನಿಸಿ. "
        "Try drawing six materials (copper, gold, aluminium, coal, sulfur, wood) into wires. "
        "Ductile metals stretch into thin wires while non-ductile materials snap. "
        "Results build a comparative table. Teaches why copper and gold are used for electrical "
        "wiring — their ductility allows them to be drawn into long, thin conductors."
    ),
    "cannot_demonstrate": [
        "Quantitative wire diameter or tensile strength values",
        "Ductility under elevated temperatures",
        "Alloy behavior",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Demonstration State",
            "range": "initial, metal_draw, nonmetal_draw",
            "url_key": "initialState",
            "effect": (
                "Sets which demonstration is auto-loaded.\n"
                "  'initial'      → blank experiment, no material selected (default)\n"
                "  'metal_draw'   → auto-selects copper and draws it → forms a wire (ductile)\n"
                "  'nonmetal_draw'→ auto-selects coal and draws it → snaps (non-ductile)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "ductility_definition",
            "title": "Ductility — Metals Can Be Drawn Into Wires",
            "description": (
                "Ductility is the property of metals that allows them to be stretched into "
                "long, thin wires without breaking. Like malleability, it depends on metal "
                "atoms being able to slide past each other under tension."
            ),
            "key_insight": (
                "When a metal is pulled, its atomic layers stretch and re-bond in new positions. "
                "The metal becomes longer and thinner but stays intact. "
                "Copper is so ductile that 1 gram can be drawn into over 2 km of wire."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "non_ductility_nonmetals",
            "title": "Non-metals — Not Ductile, They Snap",
            "description": (
                "Non-metals like coal, sulfur, and wood cannot be drawn into wires. "
                "When pulled, their rigid atomic bonds simply fracture — the material "
                "breaks cleanly rather than stretching."
            ),
            "key_insight": (
                "Non-metal atoms are in fixed, directional bonds. Pulling force "
                "exceeds bond strength → material snaps. This is why rubber-insulated "
                "wires have a METAL core (copper/aluminium) to carry current — "
                "no non-metal could form the wire itself."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "ductility_vs_malleability",
            "title": "Ductility vs Malleability — Two Faces of the Same Property",
            "description": (
                "Both ductility (wire-drawing) and malleability (sheet-forming) come from "
                "the same atomic-level sliding mechanism in metals. "
                "Ductility = stretched under tension. Malleability = compressed under pressure."
            ),
            "key_insight": (
                "Gold is BOTH the most malleable AND most ductile metal. "
                "Ductility: gold leaf can be hammered to 100 nm thickness. "
                "Malleability: 1 gram of gold can be drawn into 3 km of wire. "
                "Same atomic sliding mechanism, different directions of force."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# SONORITY — Config
# =============================================================================
SIMULATIONS_KN["sonority_kn"] = {
    "id": "sonority_kn",
    "title": "ಧ್ವನಿವಂತ ಗುಣ (Sonority)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation3_sonority_kn.html",
    "description": (
        "ಘಂಟೆ, ಚಮಚ, ನಾಣ್ಯ, ಮರ, ಪ್ಲಾಸ್ಟಿಕ್ ಮತ್ತು ರಬ್ಬರ್ ವಸ್ತುಗಳನ್ನು ಹೊಡೆದು ಅವು ಉಂಟುಮಾಡುವ ಶಬ್ದ ಕೇಳಿ. "
        "Strike six objects (bell, spoon, coin, wood, plastic, rubber) to hear and compare "
        "their sounds. Metals ring with a clear sustained tone (sonorous); non-metals produce "
        "a dull thud. A comparison table records results. Teaches why school bells, "
        "temple bells, and musical instruments are made of metal."
    ),
    "cannot_demonstrate": [
        "Exact frequency or pitch (Hz) measurements",
        "Effect of thickness or alloy composition on sound",
        "Resonance or harmonic analysis",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Demonstration State",
            "range": "initial, metal_strike, nonmetal_strike",
            "url_key": "initialState",
            "effect": (
                "Sets which demonstration is auto-loaded.\n"
                "  'initial'        → blank experiment, no object struck (default)\n"
                "  'metal_strike'   → auto-strikes bell → clear ringing sound (sonorous)\n"
                "  'nonmetal_strike'→ auto-strikes wood → dull thud (not sonorous)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "sonority_definition",
            "title": "Sonority — Metals Produce a Ringing Sound",
            "description": (
                "Sonority is the property of metals to produce a clear, sustained ringing "
                "sound when struck. Metal atoms are arranged in a crystal lattice that "
                "efficiently transfers and sustains vibrations, creating audible ringing."
            ),
            "key_insight": (
                "When metal is struck, the force sets up vibrations that travel through "
                "the crystal lattice and persist for a long time → clear ring. "
                "The denser and more uniform the lattice, the clearer and longer the ring. "
                "This is why bells, cymbals, and xylophones are made of metal."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "non_sonority_nonmetals",
            "title": "Non-metals — Dull Thud, No Ring",
            "description": (
                "Non-metals like wood, plastic, and rubber produce a dull sound when struck "
                "because they absorb (dampen) vibrations instead of propagating them. "
                "Their disordered atomic/molecular structure causes energy to be dissipated "
                "quickly as heat rather than sustained sound waves."
            ),
            "key_insight": (
                "Non-metals are sound dampers. Wood absorbs vibrations → dull thud. "
                "Rubber is so effective at damping that it is used in anti-vibration mounts. "
                "This is why wooden mallets are used when you want to hit something without ringing."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "sonority_applications",
            "title": "Sonority in Musical Instruments and Everyday Life",
            "description": (
                "Sonority explains the choice of materials in bells, gongs, musical instruments, "
                "and alarm systems. All rely on metal's ability to sustain clear vibrations "
                "that travel as audible sound waves."
            ),
            "key_insight": (
                "School bell (iron), temple bell (bronze), xylophone (steel bars), "
                "cymbal (brass) — all exploit sonority. "
                "The specific metal and shape determine the pitch and quality of sound. "
                "Non-metal bells would produce only a dull knock — useless for signaling."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# HEAT CONDUCTION — Config
# =============================================================================
SIMULATIONS_KN["heat_conduction_kn"] = {
    "id": "heat_conduction_kn",
    "title": "ಉಷ್ಣ ವಾಹಕತೆ (Heat Conduction)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation4_heat_conduction_kn.html",
    "description": (
        "ಲೋಹ ಮತ್ತು ಮರದ ಚಮಚಗಳನ್ನು ಬಿಸಿ ನೀರಲ್ಲಿ ಇರಿಸಿ ತಾಪಮಾನ ಹೇಗೆ ಬದಲಾಗುತ್ತದೆ ಎಂದು ಗಮನಿಸಿ. "
        "Place metal and wooden spoons in hot water and observe how temperature changes "
        "over 15 seconds. The metal spoon conducts heat rapidly to its handle while "
        "the wooden spoon stays cool. Real-time temperature displays and a colour-coded "
        "heat gradient animate the conduction. Teaches why metal cookware has wooden/plastic "
        "handles and why our hands feel hot when touching a metal spoon in hot soup."
    ),
    "cannot_demonstrate": [
        "Exact thermal conductivity values (W/m·K)",
        "Comparison between different metals (only metal vs wood)",
        "Convection or radiation heat transfer modes",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Experiment State",
            "range": "initial, running",
            "url_key": "initialState",
            "effect": (
                "Sets the state of the heat conduction experiment.\n"
                "  'initial' → idle state, spoons in water, experiment not started (default)\n"
                "  'running' → auto-clicks start button and begins the 15-second experiment"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "metals_good_conductors_heat",
            "title": "Metals Are Good Conductors of Heat",
            "description": (
                "Metals contain free electrons that can move throughout the metal. "
                "These electrons carry thermal energy (heat) rapidly from hotter to cooler "
                "regions, making metals excellent heat conductors."
            ),
            "key_insight": (
                "Metal spoon handle gets hot quickly because free electrons in the metal "
                "carry thermal energy from the hot end to the cool end almost instantly. "
                "This is why metals feel cold to touch — they rapidly conduct body heat away!"
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "nonmetals_poor_conductors_heat",
            "title": "Non-metals Are Poor Conductors (Insulators) of Heat",
            "description": (
                "Wood, plastic, and rubber have no free electrons. Heat transfer must happen "
                "by vibrating atoms bumping into adjacent atoms — a much slower process. "
                "This makes non-metals poor thermal conductors (good insulators)."
            ),
            "key_insight": (
                "Wooden spoon handle stays cool because heat barely moves through wood. "
                "This is not a disadvantage — it is exactly WHY wooden/plastic handles are safe: "
                "they insulate your hand from the heat of the pan."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "heat_conduction_applications",
            "title": "Why Cookware Uses Both Metal and Non-metal Parts",
            "description": (
                "Good cookware deliberately combines metals (for efficient heat transfer to food) "
                "and non-metal handles (for safe gripping without burning hands). "
                "This is a direct application of the contrast in thermal conductivity."
            ),
            "key_insight": (
                "Metal base = conducts heat fast from stove to food. "
                "Plastic/wood handle = insulates cook's hand from heat. "
                "If the handle were metal too, it would become too hot to hold. "
                "Every kitchen pan illustrates this principle."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# ELECTRICAL CONDUCTIVITY — Config
# =============================================================================
SIMULATIONS_KN["electrical_conductivity_kn"] = {
    "id": "electrical_conductivity_kn",
    "title": "ವಿದ್ಯುತ್ ವಾಹಕತೆ (Electrical Conductivity)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation5_electrical_conductivity_kn.html",
    "description": (
        "ತಾಮ್ರ, ಕಬ್ಬಿಣ, ಅಲ್ಯೂಮಿನಿಯಂ, ರಬ್ಬರ್, ಪ್ಲಾಸ್ಟಿಕ್ ಮತ್ತು ಮರವನ್ನು ಸರ್ಕ್ಯೂಟ್‌ನಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ ಅವು ವಿದ್ಯುತ್ ವಾಹಕಗಳೇ ಅಥವಾ ಅವಾಹಕಗಳೇ ಎಂದು ತಿಳಿಯಿರಿ. "
        "Insert six materials (copper, iron, aluminium, rubber, plastic, wood) into a test "
        "circuit and observe whether the bulb lights up. Conductors complete the circuit "
        "(bulb glows, current flows); insulators block current (bulb stays dark). "
        "Results populate a comparison table. Teaches the fundamental distinction between "
        "electrical conductors and insulators and connects it to safe electrical wiring."
    ),
    "cannot_demonstrate": [
        "Quantitative resistance measurements (ohms)",
        "Semiconductors or partial conductors",
        "Effect of temperature on conductivity",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Test Material",
            "range": "initial, conductor_test, insulator_test",
            "url_key": "initialState",
            "effect": (
                "Sets which demonstration is auto-loaded.\n"
                "  'initial'        → idle circuit, no material inserted (default)\n"
                "  'conductor_test' → auto-inserts copper → bulb lights (conductor)\n"
                "  'insulator_test' → auto-inserts rubber → bulb stays off (insulator)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": "conductors_free_electrons",
            "title": "Electrical Conductors — Metals Have Free Electrons",
            "description": (
                "Metals conduct electricity because their outermost electrons are loosely bound "
                "and can move freely through the metal lattice as a 'sea of electrons'. "
                "When a voltage is applied, these free electrons flow — forming an electric current."
            ),
            "key_insight": (
                "Free electrons = electrical conductivity. When copper is placed in the circuit, "
                "its free electrons are pushed by the battery's voltage → current flows → bulb glows. "
                "The more free electrons, the better the conductor. Copper and aluminium are best "
                "for wires because they have many free electrons AND can be drawn thin (ductile)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "insulators_no_free_electrons",
            "title": "Electrical Insulators — Non-metals Block Current",
            "description": (
                "Non-metals like rubber, plastic, and wood have electrons tightly bound to their "
                "atoms. No free electrons → no current flow → they act as insulators, "
                "blocking electricity completely."
            ),
            "key_insight": (
                "When rubber is placed in the circuit, no electrons can move through it → "
                "circuit is broken → bulb stays dark. This property makes rubber the perfect "
                "cable insulation material — it prevents current from escaping the copper wire core, "
                "protecting people from electric shocks."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": "conductors_insulators_applications",
            "title": "Why Every Wire Has Both a Conductor and an Insulator",
            "description": (
                "Electric cables always have a metal core (conductor) surrounded by rubber or "
                "plastic coating (insulator). This design uses both properties intentionally: "
                "metal carries the current; insulation keeps it safely contained."
            ),
            "key_insight": (
                "Wire design: copper/aluminium core (high conductivity, free electrons) "
                "+ rubber/PVC outer layer (insulator, no free electrons, protects user). "
                "Remove the insulation → live wire → dangerous shock hazard. "
                "This is why electricians wear rubber gloves — rubber blocks current."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# QUIZ QUESTIONS — MALLEABILITY
# =============================================================================
QUIZ_QUESTIONS_KN["malleability_kn"] = [
    {
        "id": "malleability_q1",
        "challenge": (
            "Demonstrate that a METAL is malleable. "
            "Select and hammer a metal to show it flattening into a sheet.\n\n"
            "(ಲೋಹ ನಮ್ಯವಾಗಿದೆ ಎಂದು ತೋರಿಸಿ — ಒಂದು ಲೋಹ ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ಬಡಿದಾಗ ಅದು ಚಪ್ಪಟೆಯಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "metal_hammer"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'metal_hammer'. The simulation auto-selects copper "
                "and hammers it — watch it flatten into a thin sheet."
            ),
            "attempt_2": (
                "Choose 'metal_hammer': Copper is selected and hammered → flattens. "
                "The result badge shows '✅ ನಮ್ಯ'. Malleable metals squash, they do NOT break."
            ),
            "attempt_3": (
                "Set 'initialState=metal_hammer': Copper (ತಾಮ್ರ) flattens when struck because "
                "its atomic layers slide past each other. Result: thin sheet, no fracture."
            )
        },
        "concept_reminder": (
            "Malleability: metal atoms are in layered crystal structure. Under hammer force, "
            "layers SLIDE past each other → metal deforms into a sheet. "
            "Does NOT break because atomic bonds reform in new positions. "
            "Malleable metals: copper, aluminium, iron, gold. "
            "(ಬಡಿದಾಗ ಚಪ್ಪಟೆ = ನಮ್ಯ ಲೋಹ!)"
        )
    },
    {
        "id": "malleability_q2",
        "challenge": (
            "Now demonstrate a NON-METAL that is BRITTLE. "
            "Hammer a non-metal and show it shattering.\n\n"
            "(ಅಲೋಹ ಭಂಗುರವಾಗಿದೆ ಎಂದು ತೋರಿಸಿ — ಬಡಿದಾಗ ಚೂರ್ಣವಾಗುತ್ತದೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "nonmetal_hammer"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'nonmetal_hammer'. The simulation auto-selects coal "
                "and hammers it — watch it shatter into fragments."
            ),
            "attempt_2": (
                "Choose 'nonmetal_hammer': Coal (ಕಲ್ಲಿದ್ದಲು) is hammered → shatters. "
                "Result badge shows '❌ ಭಂಗುರ'. Brittle materials break — they do NOT flatten."
            ),
            "attempt_3": (
                "Set 'initialState=nonmetal_hammer': Coal shatters because its atoms are "
                "rigidly bonded and cannot slide. Force exceeds bond strength → fracture."
            )
        },
        "concept_reminder": (
            "Brittleness: non-metal atoms are in rigid, directional bonds. "
            "Under hammer force, bonds BREAK rather than slide → material shatters. "
            "Brittle non-metals: coal, sulfur, chalk, glass. "
            "CONTRAST: metals flatten (slide), non-metals shatter (break). "
            "(ಬಡಿದಾಗ ಚೂರು = ಭಂಗುರ ಅಲೋಹ!)"
        )
    },
    {
        "id": "malleability_q3",
        "challenge": (
            "Start with the INITIAL empty state. "
            "Explain: why can metals be beaten into sheets while non-metals cannot? "
            "What is different about their atomic structure?\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಲೋಹ ಮತ್ತು ಅಲೋಹ ಪರಮಾಣು ರಚನೆಯ ವ್ಯತ್ಯಾಸ ಹೇಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Read the concept card — "
                "it explains the layered atomic structure of metals."
            ),
            "attempt_2": (
                "Choose 'initial': Metals = atoms in sliding layers. Non-metals = atoms in "
                "rigid fixed bonds. Same force → different outcome."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Metal layers can slide (like cards in a deck). "
                "Non-metal bonds are directional and rigid — they fracture, not slide."
            )
        },
        "concept_reminder": (
            "Metal atomic structure: layers of atoms that can SLIDE past each other. "
            "Force applied → layers slide → metal deforms without breaking. "
            "Non-metal atomic structure: rigidly positioned atoms in fixed bonds. "
            "Force applied → bonds exceed limit → fracture. "
            "This structural difference is why ONLY metals are malleable. "
            "(ಜಾರಬಹುದಾದ ಪದರ = ನಮ್ಯ | ಗಟ್ಟಿ ಬಂಧ = ಭಂಗುರ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — DUCTILITY
# =============================================================================
QUIZ_QUESTIONS_KN["ductility_kn"] = [
    {
        "id": "ductility_q1",
        "challenge": (
            "Show that COPPER is ductile. Draw copper into a wire in the simulation.\n\n"
            "(ತಾಮ್ರ ಸೆಳೆಯಬಲ್ಲ ಗುಣ ಇದೆ ಎಂದು ತೋರಿಸಿ — ಅದನ್ನು ತಂತಿಯಾಗಿ ಎಳೆಯಿರಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "metal_draw"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'metal_draw'. The simulation auto-selects copper "
                "and draws it — watch it stretch into a long thin wire."
            ),
            "attempt_2": (
                "Choose 'metal_draw': Copper stretches into a wire (ductile result). "
                "The wire-result group appears. Copper atoms slide apart without snapping."
            ),
            "attempt_3": (
                "Set 'initialState=metal_draw': Copper (ತಾಮ್ರ) draws into a wire because "
                "its atoms reposition under tension. Perfect for electrical wires!"
            )
        },
        "concept_reminder": (
            "Ductility: metal atoms slide and reposition under tensile (pulling) force. "
            "The metal elongates and thins without breaking → wire forms. "
            "Copper is the most common wire material: good ductility + excellent conductivity. "
            "1 gram of copper can make 2+ km of thin wire. "
            "(ಎಳೆದಾಗ ತಂತಿ = ಸೆಳೆತ ಗುಣ!)"
        )
    },
    {
        "id": "ductility_q2",
        "challenge": (
            "Show that a NON-METAL cannot be drawn into a wire. "
            "Attempt to draw coal — demonstrate the 'snapping' result.\n\n"
            "(ಅಲೋಹವನ್ನು ತಂತಿಯಾಗಿ ಎಳೆಯಲಾಗದು ಎಂದು ತೋರಿಸಿ — ಕಲ್ಲಿದ್ದಲು ಮುರಿಯುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "nonmetal_draw"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'nonmetal_draw'. The simulation auto-selects coal "
                "and attempts to draw it — watch it snap."
            ),
            "attempt_2": (
                "Choose 'nonmetal_draw': Coal snaps when pulled (not-ductile result). "
                "The broken-pieces group appears. Non-metal bonds fracture under tension."
            ),
            "attempt_3": (
                "Set 'initialState=nonmetal_draw': Coal (ಕಲ್ಲಿದ್ದಲು) breaks when pulled. "
                "Rigid bonds between carbon atoms fracture → no wire possible."
            )
        },
        "concept_reminder": (
            "Non-ductile materials: their atoms are in rigid, fixed bonds. "
            "Pulling force → bonds break → material snaps. No repositioning possible. "
            "This is why electrical wire cores must be METAL — no non-metal can form a wire. "
            "Coal, sulfur, wood: all snap when pulled. "
            "(ಎಳೆದಾಗ ಮುರಿಯುತ್ತದೆ = ಸೆಳೆತ ಗುಣ ಇಲ್ಲ!)"
        )
    },
    {
        "id": "ductility_q3",
        "challenge": (
            "Show the INITIAL state. Explain why electrical wires are made of "
            "copper or aluminium and NOT of materials like coal or wood.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ವಿದ್ಯುತ್ ತಂತಿಗೆ ತಾಮ್ರ ಅಥವಾ ಅಲ್ಯೂಮಿನಿಯಂ ಯಾಕೆ ಬಳಸುತ್ತಾರೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Read the concept card — "
                "then think: what TWO properties must a wire material have?"
            ),
            "attempt_2": (
                "Choose 'initial': Wire needs TWO properties: (1) DUCTILITY to be drawn thin, "
                "(2) ELECTRICAL CONDUCTIVITY to carry current. Copper has both."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Coal cannot be drawn thin (brittle, not ductile). "
                "Wood cannot conduct electricity (insulator). Copper: ductile + conductor = ideal."
            )
        },
        "concept_reminder": (
            "Why copper wires? TWO reasons working together: "
            "1. DUCTILITY: copper can be drawn into very thin, long wires without breaking. "
            "2. ELECTRICAL CONDUCTIVITY: copper has free electrons that carry current efficiently. "
            "Coal: brittle (no ductility) → can't form a wire. "
            "Wood: not ductile + insulator → useless for wires. "
            "Aluminium also used: lighter, cheaper, but less conductive than copper. "
            "(ತಾಮ್ರ = ಸೆಳೆತ ಗುಣ + ವಿದ್ಯುತ್ ವಾಹಕ = ಆದರ್ಶ ತಂತಿ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — SONORITY
# =============================================================================
QUIZ_QUESTIONS_KN["sonority_kn"] = [
    {
        "id": "sonority_q1",
        "challenge": (
            "Strike a METAL object and demonstrate its ringing sound. "
            "Which objects in the simulation are sonorous?\n\n"
            "(ಲೋಹ ವಸ್ತು ಹೊಡೆದಾಗ ಶಬ್ದ ತೋರಿಸಿ — ಯಾವ ವಸ್ತುಗಳು ಧ್ವನಿವಂತವಾಗಿವೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "metal_strike"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'metal_strike'. The simulation auto-strikes the bell — "
                "watch the sound waves appear and hear the ringing."
            ),
            "attempt_2": (
                "Choose 'metal_strike': Bell (ಘಂಟೆ) produces a sustained ringing sound. "
                "The 'sonorous' badge appears. Metal sound waves persist."
            ),
            "attempt_3": (
                "Set 'initialState=metal_strike': Bell, spoon, and coin are all sonorous — "
                "all metals produce a clear ring. The sound waves radiate outward."
            )
        },
        "concept_reminder": (
            "Sonority: metals produce a clear, sustained ringing sound. "
            "Metal crystal lattice efficiently transmits vibrations → long-lasting sound waves. "
            "Sonorous metals: bell (iron/bronze), spoon (steel), coin (various metals). "
            "Volume persists: if you strike a metal bell, the ring lasts for seconds. "
            "(ಲೋಹ ಹೊಡೆದಾಗ ಘಂಟಾ ಧ್ವನಿ = ಧ್ವನಿವಂತ ಗುಣ!)"
        )
    },
    {
        "id": "sonority_q2",
        "challenge": (
            "Strike a NON-METAL object and show the 'dull thud' result. "
            "Why do non-metals not ring when struck?\n\n"
            "(ಅಲೋಹ ಹೊಡೆದ ಮಂಕಾದ ಶಬ್ದ ತೋರಿಸಿ — ಅಲೋಹಗಳು ಯಾಕೆ ಘಂಟಾ ಧ್ವನಿ ಮಾಡುವುದಿಲ್ಲ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "nonmetal_strike"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'nonmetal_strike'. The simulation auto-strikes wood — "
                "no ringing, just a dull thud. 'Not sonorous' result appears."
            ),
            "attempt_2": (
                "Choose 'nonmetal_strike': Wood (ಮರ) produces a dull thud. "
                "Non-metal structure absorbs vibrations instead of propagating them."
            ),
            "attempt_3": (
                "Set 'initialState=nonmetal_strike': Wood, plastic, rubber all give dull sounds. "
                "Their disordered molecular structure dampens vibrations → no sustained ring."
            )
        },
        "concept_reminder": (
            "Non-sonorous non-metals: wood, plastic, rubber produce only dull thuds. "
            "Their amorphous (disordered) molecular structure ABSORBS vibrations. "
            "Energy is quickly converted to heat rather than sustained sound. "
            "This is why drum STICKS are wood — they produce a sharp hit, not a ringing tone. "
            "(ಅಲೋಹ = ಕಂಪನ ಹೀರಿಕೊಳ್ಳುತ್ತದೆ = ಧ್ವನಿ ಇಲ್ಲ!)"
        )
    },
    {
        "id": "sonority_q3",
        "challenge": (
            "Show the INITIAL state. Give two real-world examples where "
            "sonority is the primary reason metal is chosen for that application.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಧ್ವನಿವಂತ ಗುಣ ಕಾರಣ ಲೋಹ ಬಳಸುವ ಎರಡು ಉದಾಹರಣೆ ಕೊಡಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Read the concept card and takeaway. "
                "Think about bells, musical instruments, and alarm systems."
            ),
            "attempt_2": (
                "Choose 'initial': Example 1 — school bells (iron) ring to signal breaks. "
                "Example 2 — musical triangle (steel) sustains its note in music."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Temple bell = metal (sustained devotional ring). "
                "Cymbal = brass (loud, sustained crash in music). Non-metal versions would only thud."
            )
        },
        "concept_reminder": (
            "Sonority applications where metal is chosen specifically for its ringing property: "
            "1. SCHOOL BELL: iron bell produces a loud, clear ring audible across the school. "
            "2. TEMPLE BELL: bronze bell sustains its ring (OM resonance) for several seconds. "
            "3. MUSICAL TRIANGLE: steel bar rings when struck, sustains through musical passage. "
            "4. CYMBAL: brass plate produces loud sustained crash in percussion music. "
            "In ALL cases: if replaced with wood or plastic → only a dull thud → useless. "
            "(ಧ್ವನಿ ಮುಖ್ಯ = ಲೋಹ ಆಯ್ಕೆ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — HEAT CONDUCTION
# =============================================================================
QUIZ_QUESTIONS_KN["heat_conduction_kn"] = [
    {
        "id": "heat_q1",
        "challenge": (
            "Start the heat conduction experiment. Observe how quickly "
            "the metal spoon handle heats up compared to the wooden spoon.\n\n"
            "(ಪ್ರಯೋಗ ಪ್ರಾರಂಭಿಸಿ — ಲೋಹ ಮತ್ತು ಮರದ ಚಮಚ ಉಷ್ಣತೆ ಹೇಗೆ ಬದಲಾಗುತ್ತವೆ ಎಂದು ಗಮನಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "running"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'running'. The start button auto-clicks and "
                "the 15-second experiment begins. Watch the temperature cards."
            ),
            "attempt_2": (
                "Choose 'running': Metal spoon temperature rises quickly (good conductor). "
                "Wood spoon stays near 25°C (poor conductor / insulator)."
            ),
            "attempt_3": (
                "Set 'initialState=running': The metal spoon reaches ~70°C at 15s while wood "
                "barely rises above 30°C. Metal conducts heat; wood insulates."
            )
        },
        "concept_reminder": (
            "Heat conduction experiment: both spoons start at 25°C in hot water. "
            "METAL spoon: temperature rises rapidly → handle becomes hot (good conductor). "
            "WOODEN spoon: temperature barely rises → handle stays cool (poor conductor/insulator). "
            "Reason: metal has free electrons that carry heat; wood has no free electrons. "
            "(ಲೋಹ ತ್ವರಿತ ಉಷ್ಣ ವಾಹಕ | ಮರ ಉಷ್ಣ ಅವಾಹಕ!)"
        )
    },
    {
        "id": "heat_q2",
        "challenge": (
            "Show the INITIAL idle state. Explain why metal pans have wooden or "
            "plastic handles instead of metal handles.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಅಡುಗೆ ಪಾತ್ರೆಗಳಿಗೆ ಮರದ ಅಥವಾ ಪ್ಲಾಸ್ಟಿಕ್ ಹಿಡಿ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Look at the two spoons — "
                "observe this is the resting state before the experiment."
            ),
            "attempt_2": (
                "Choose 'initial': Metal conducts heat rapidly to the handle → "
                "a metal handle would burn the cook's hand. Wood insulates → safe to grip."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Same principle as the experiment. "
                "The pan body = metal (heats food fast). Handle = wood/plastic (keeps hand safe)."
            )
        },
        "concept_reminder": (
            "Cookware design principle: "
            "METAL BASE/BODY: good heat conductor → transfers heat from flame to food efficiently. "
            "WOODEN/PLASTIC HANDLE: poor heat conductor (insulator) → stays cool → safe to grip. "
            "If the handle were also metal, it would heat up to the same temperature as the base "
            "→ impossible to pick up without getting burned. "
            "This is direct application of differential thermal conductivity. "
            "(ಲೋಹ ಅಡಿ + ಮರ ಹಿಡಿ = ಸುರಕ್ಷಿತ ಅಡುಗೆ ಪಾತ್ರೆ!)"
        )
    },
    {
        "id": "heat_q3",
        "challenge": (
            "Run the experiment. After observing results, explain: "
            "why does a metal object feel cold when you touch it at room temperature, "
            "even though it is the same temperature as a wooden object nearby?\n\n"
            "(ಪ್ರಯೋಗ ಚಾಲಿಸಿ — ಒಂದೇ ತಾಪಮಾನದಲ್ಲಿ ಇದ್ದರೂ ಲೋಹ ಏಕೆ ತಂಪಾಗಿ ಅನ್ನಿಸುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "running"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'running'. Watch the heat transfer happen. "
                "The key clue is in the direction of heat flow."
            ),
            "attempt_2": (
                "Choose 'running': Metal conducts heat AWAY from your hand rapidly → "
                "your skin loses heat fast → you feel cold. Wood barely conducts → "
                "heat stays in your skin → feels warmer."
            ),
            "attempt_3": (
                "Set 'initialState=running': Temperature sensation = rate of heat transfer. "
                "Metal removes body heat fast (feels cold). Wood keeps body heat (feels warm). "
                "Both are at 25°C — only CONDUCTIVITY differs."
            )
        },
        "concept_reminder": (
            "Why metal feels cold at room temperature: "
            "Touch metal at 25°C → metal (good conductor) rapidly draws heat FROM your hand "
            "into itself → your skin temperature drops → brain interprets as 'cold'. "
            "Touch wood at 25°C → wood (insulator) barely conducts heat away → "
            "your skin stays warm → brain interprets as 'warm or neutral'. "
            "BOTH objects are at the same temperature — sensation depends on HEAT TRANSFER RATE. "
            "(ಲೋಹ ಶೀತ ಅನ್ನಿಸಲು ಕಾರಣ = ಉಷ್ಣ ವಾಹಕ, ಶರೀರ ಉಷ್ಣ ಎಳೆಯುತ್ತದೆ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — ELECTRICAL CONDUCTIVITY
# =============================================================================
QUIZ_QUESTIONS_KN["electrical_conductivity_kn"] = [
    {
        "id": "conductivity_q1",
        "challenge": (
            "Test COPPER in the circuit. Demonstrate that it is an electrical conductor.\n\n"
            "(ಸರ್ಕ್ಯೂಟ್‌ನಲ್ಲಿ ತಾಮ್ರ ಪರೀಕ್ಷಿಸಿ — ಅದು ವಿದ್ಯುತ್ ವಾಹಕ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "conductor_test"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'conductor_test'. The simulation auto-inserts copper "
                "into the circuit and tests it — the bulb should light up."
            ),
            "attempt_2": (
                "Choose 'conductor_test': Copper completes the circuit → current flows → "
                "bulb glows. The '⚡ ವಾಹಕ' badge appears."
            ),
            "attempt_3": (
                "Set 'initialState=conductor_test': Copper has free electrons that carry "
                "current through the circuit. Bulb ON = conductor."
            )
        },
        "concept_reminder": (
            "Copper (ತಾಮ್ರ) is an excellent electrical conductor. "
            "Free electrons in copper move in response to voltage → electric current. "
            "Current flows → circuit is complete → bulb lights. "
            "Also good conductors: iron (ಕಬ್ಬಿಣ), aluminium (ಅಲ್ಯೂಮಿನಿಯಂ). "
            "(ಮುಕ್ತ ಇಲೆಕ್ಟ್ರಾನ್ = ವಿದ್ಯುತ್ ಹರಿಯುತ್ತದೆ = ಬಲ್ಬ್ ಬೆಳಗುತ್ತದೆ!)"
        )
    },
    {
        "id": "conductivity_q2",
        "challenge": (
            "Test RUBBER in the circuit. Demonstrate that it is an electrical insulator.\n\n"
            "(ಸರ್ಕ್ಯೂಟ್‌ನಲ್ಲಿ ರಬ್ಬರ್ ಪರೀಕ್ಷಿಸಿ — ಅದು ಅವಾಹಕ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "insulator_test"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'insulator_test'. Rubber is auto-inserted — "
                "the bulb stays dark. Circuit cannot be completed through rubber."
            ),
            "attempt_2": (
                "Choose 'insulator_test': Rubber (ರಬ್ಬರ್) blocks current → bulb stays off. "
                "The '🚫 ಅವಾಹಕ' badge appears. No free electrons in rubber."
            ),
            "attempt_3": (
                "Set 'initialState=insulator_test': Rubber has no free electrons → "
                "current cannot flow → circuit stays open → bulb dark."
            )
        },
        "concept_reminder": (
            "Rubber (ರಬ್ಬರ್) is an excellent electrical insulator. "
            "Its electrons are tightly bound → no free electrons → no current flow. "
            "Circuit with rubber = open circuit = no current = bulb dark. "
            "Also insulators: plastic (ಪ್ಲಾಸ್ಟಿಕ್), wood (ಮರ). "
            "This is WHY rubber is used to coat electric cables — "
            "it prevents current from escaping the metal wire core. "
            "(ಮುಕ್ತ ಇಲೆಕ್ಟ್ರಾನ್ ಇಲ್ಲ = ವಿದ್ಯುತ್ ತಡೆಯಲಾಗುತ್ತದೆ = ಅವಾಹಕ!)"
        )
    },
    {
        "id": "conductivity_q3",
        "challenge": (
            "Show the INITIAL idle state. Explain why an electric cable has "
            "a metal core surrounded by a rubber/plastic coating. "
            "What would happen if the outer coating were also metal?\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ತಂತಿಗೆ ರಬ್ಬರ್ ಹೊದಿಕೆ ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Read the concept card — "
                "note the roles of conductor and insulator in a cable."
            ),
            "attempt_2": (
                "Choose 'initial': Metal core (copper) = carries current. "
                "Rubber coating = prevents current from reaching the user's hand or nearby wires."
            ),
            "attempt_3": (
                "Set 'initialState=initial': If coating were metal → current would flow "
                "to anyone touching the outside → electric shock hazard. "
                "Rubber stops this: no free electrons → no current through coating."
            )
        },
        "concept_reminder": (
            "Electric cable design intentionally uses BOTH types: "
            "METAL CORE (copper/aluminium): free electrons carry current from source to appliance. "
            "RUBBER/PLASTIC COATING: no free electrons → insulates → current stays in core. "
            "If outer coating were metal → current could flow through it → shock anyone it touches. "
            "Rubber gloves protect electricians for the same reason: no current through rubber. "
            "Two materials, two opposite properties, working TOGETHER for safe electricity delivery. "
            "(ಲೋಹ ತಂತಿ + ರಬ್ಬರ್ ಹೊದಿಕೆ = ಸುರಕ್ಷಿತ ವಿದ್ಯುತ್!)"
        )
    }
]

# =============================================================================
# RUSTING EXPERIMENT — Config
# =============================================================================
SIMULATIONS_KN["rusting_experiment_kn"] = {
    "id": "rusting_experiment_kn",
    "title": "ತುಕ್ಕು ಪ್ರಯೋಗ (Rusting Experiment)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation6_rusting_experiment_kn.html",
    "description": (
        "ಮೂರು ಕಬ್ಬಿಣದ ಉಗುರುಗಳನ್ನು ಒಣ ಗಾಳಿ, ಕುದಿಸಿದ ನೀರು+ಎಣ್ಣೆ, ಮತ್ತು ಗಾಳಿ+ನೀರು ಸ್ಥಿತಿಗಳಲ್ಲಿ "
        "7 ದಿನ ಇಟ್ಟು ಯಾವ ಉಗುರು ತುಕ್ಕು ಹಿಡಿಯುತ್ತದೆ ಎಂದು ಗಮನಿಸಿ. "
        "Three iron nails are placed in different conditions — Tube A (dry air only), "
        "Tube B (boiled water + oil seal, no air), Tube C (air + water together) — "
        "and observed over 7 days via a time slider. "
        "Only Tube C (both air AND water present) develops rust, proving that rusting "
        "requires BOTH oxygen (from air) and water simultaneously."
    ),
    "cannot_demonstrate": [
        "Exact rust formation rate or quantitative measurement",
        "Effect of salt water vs fresh water on rusting speed",
        "Galvanisation or paint as rust prevention in action",
        "Rusting of metals other than iron",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Time State",
            "range": "initial, day3, day7",
            "url_key": "initialState",
            "effect": (
                "Controls which point in the 7-day experiment is auto-loaded.\n"
                "  'initial' → Day 0: all nails shiny, experiment just started (default)\n"
                "  'day3'    → Day 3: rust beginning to form in Tube C only\n"
                "  'day7'    → Day 7: experiment complete — Tube C heavily rusted, "
                "Tubes A and B rust-free"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the key concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Rusting Requires Both Oxygen AND Water",
            "description": (
                "Iron rusts through a chemical reaction that requires two reactants: "
                "oxygen (from air) and water (moisture). If either is absent, "
                "rusting cannot occur."
            ),
            "key_insight": (
                "Tube A has only air → no rust. Tube B has only water → no rust. "
                "Tube C has air + water → rust forms. "
                "This proves rusting needs BOTH simultaneously. "
                "Chemical equation: 4Fe + 3O₂ + 6H₂O → 2Fe₂O₃·3H₂O (iron oxide = rust)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Rust Prevention — Blocking Oxygen or Water",
            "description": (
                "Since rusting needs both oxygen and water, preventing rust means "
                "blocking one or both. Common methods: painting, oiling, galvanisation "
                "(zinc coating), and making stainless steel alloys."
            ),
            "key_insight": (
                "Paint/oil = forms a barrier that prevents oxygen and water reaching iron surface. "
                "Galvanisation = zinc layer corrodes preferentially, protecting iron underneath. "
                "Stainless steel = chromium in alloy forms protective oxide layer automatically."
            ),
            "related_params": ["initialState", "showHints"]
        },
        {
            "id": 3,
            "title": "Delhi Iron Pillar — Iron That Doesn't Rust",
            "description": (
                "The 1600+ year-old Iron Pillar of Delhi has remarkably not rusted "
                "because of its unique phosphorus-rich composition, which forms a "
                "protective passive layer."
            ),
            "key_insight": (
                "Normal iron + oxygen + water → rust in days/weeks. "
                "Delhi Pillar iron + phosphorus → stable protective FePO₄ layer → "
                "resists further oxidation for 1600+ years. "
                "This is an ancient example of alloying for corrosion resistance."
            ),
            "related_params": ["initialState"]
        }
    ]
}

# =============================================================================
# METAL OXIDE REACTION — Config
# =============================================================================
SIMULATIONS_KN["metal_oxide_reaction_kn"] = {
    "id": "metal_oxide_reaction_kn",
    "title": "ಲೋಹ ಆಕ್ಸೈಡ್ ಪ್ರತಿಕ್ರಿಯೆ (Metal Oxide Reaction)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation7_metal_oxide_reaction_kn.html",
    "description": (
        "ಮೆಗ್ನೀಸಿಯಂ ರಿಬ್ಬನ್ ಉರಿಸಿ MgO ಬೂದಿ ರಚಿಸಿ, ನೀರಲ್ಲಿ ಕರಗಿಸಿ, ಮತ್ತು ಲಿಟ್ಮಸ್ ಪರೀಕ್ಷೆ ಮಾಡಿ. "
        "Burn a magnesium ribbon in oxygen to form white MgO ash, dissolve it in water "
        "to form Mg(OH)₂, then test with litmus paper. "
        "The red litmus turns blue, proving that metal oxides are basic (alkaline) in nature. "
        "Covers the 3-step reaction chain: Mg → MgO → Mg(OH)₂."
    ),
    "cannot_demonstrate": [
        "Metal oxides that are amphoteric (e.g., Al₂O₃, ZnO)",
        "Different metals burning at different temperatures",
        "Quantitative yield from burning reaction",
        "Solubility differences of different metal oxides in water",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Experiment Step",
            "range": "initial, burned, dissolved, tested",
            "url_key": "initialState",
            "effect": (
                "Sets which experimental step is auto-demonstrated.\n"
                "  'initial'   → fresh experiment ready, Mg ribbon in tongs (default)\n"
                "  'burned'    → Mg has been burned; white MgO ash formed\n"
                "  'dissolved' → MgO dissolved in water; Mg(OH)₂ solution ready\n"
                "  'tested'    → litmus test complete; red litmus turned blue (basic)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the key concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Metal + Oxygen → Metal Oxide (Basic)",
            "description": (
                "When metals react with oxygen they form metal oxides. "
                "Metal oxides are basic (alkaline) in nature — they turn red litmus blue "
                "and have pH > 7."
            ),
            "key_insight": (
                "2Mg + O₂ → 2MgO (brilliant white light during combustion). "
                "MgO + H₂O → Mg(OH)₂ (magnesium hydroxide — a base). "
                "Red litmus → blue = proof of basic nature. "
                "This is true for most metal oxides: CaO, Na₂O, Fe₂O₃ (when dissolved) are all basic."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Metal Oxides vs Non-metal Oxides — Opposite pH",
            "description": (
                "Metal oxides are basic (pH > 7). Non-metal oxides are acidic (pH < 7). "
                "This is a key distinguishing chemical property between metals and non-metals."
            ),
            "key_insight": (
                "MgO dissolves → Mg(OH)₂ (base, pH > 7) → red litmus turns blue. "
                "SO₂ dissolves → H₂SO₃ (acid, pH < 7) → blue litmus turns red. "
                "Opposite litmus results = opposite pH = fundamental chemical difference "
                "between metal and non-metal oxides."
            ),
            "related_params": ["initialState", "showHints"]
        },
        {
            "id": 3,
            "title": "Safety: Mg Burns with Blinding White Light",
            "description": (
                "Magnesium burns with an extremely bright white light that can damage "
                "the retina. This is why photographers once used magnesium flash powder "
                "and why you should never look directly at burning magnesium."
            ),
            "key_insight": (
                "Mg combustion releases very high energy → white light emission "
                "(temperature ~3100°C). The simulation shows this with a bright-light effect. "
                "Real lab: always use tinted goggles when burning magnesium."
            ),
            "related_params": ["initialState"]
        }
    ]
}

# =============================================================================
# NON-METAL OXIDE REACTION — Config
# =============================================================================
SIMULATIONS_KN["nonmetal_oxide_reaction_kn"] = {
    "id": "nonmetal_oxide_reaction_kn",
    "title": "ಅಲೋಹ ಆಕ್ಸೈಡ್ ಪ್ರತಿಕ್ರಿಯೆ (Non-metal Oxide Reaction)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation8_nonmetal_oxide_reaction_kn.html",
    "description": (
        "ಸಲ್ಫರ್ ನೀಲಿ ಜ್ವಾಲೆಯಲ್ಲಿ ಉರಿಸಿ SO₂ ಅನಿಲ ರಚಿಸಿ, ನೀರಲ್ಲಿ ಕರಗಿಸಿ H₂SO₃ (ಸಲ್ಫ್ಯೂರಸ್ ಆಮ್ಲ) ರೂಪಿಸಿ, "
        "ಲಿಟ್ಮಸ್ ಪರೀಕ್ಷೆ ಮಾಡಿ. "
        "Burn sulfur powder in a gas jar to collect SO₂, dissolve it in water to form "
        "sulfurous acid (H₂SO₃), then test with litmus paper. "
        "The blue litmus turns red, proving non-metal oxides are acidic in nature. "
        "Directly contrasts with the metal oxide experiment."
    ),
    "cannot_demonstrate": [
        "Different non-metals burning at different temperatures",
        "SO₃ formation and H₂SO₄ (sulfuric acid) chain",
        "Acid rain formation mechanism in the atmosphere",
        "Quantitative acid concentration measurement",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Experiment Step",
            "range": "initial, burned, dissolved, tested",
            "url_key": "initialState",
            "effect": (
                "Sets which experimental step is auto-demonstrated.\n"
                "  'initial'   → fresh experiment, sulfur powder on spoon (default)\n"
                "  'burned'    → sulfur has been burned with blue flame; SO₂ collected in jar\n"
                "  'dissolved' → SO₂ dissolved in water; H₂SO₃ (sulfurous acid) formed\n"
                "  'tested'    → litmus test complete; blue litmus turned red (acidic)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the key concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Non-metal + Oxygen → Non-metal Oxide (Acidic)",
            "description": (
                "When non-metals react with oxygen they form non-metal oxides. "
                "Non-metal oxides are acidic in nature — they turn blue litmus red "
                "and have pH < 7."
            ),
            "key_insight": (
                "S + O₂ → SO₂ (characteristic blue flame, pungent choking smell). "
                "SO₂ + H₂O → H₂SO₃ (sulfurous acid — an acid). "
                "Blue litmus → red = proof of acidic nature. "
                "Similarly: C + O₂ → CO₂; CO₂ + H₂O → H₂CO₃ (carbonic acid)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Contrast: Metal Oxides Basic, Non-metal Oxides Acidic",
            "description": (
                "The single most important chemical contrast between metals and non-metals "
                "is the nature of their oxides. Metal oxides → basic. "
                "Non-metal oxides → acidic. This is a reliable rule for the exam."
            ),
            "key_insight": (
                "Litmus test summary: \n"
                "Metal oxide + water → base → RED litmus turns BLUE (ಕೆಂಪು → ನೀಲಿ). \n"
                "Non-metal oxide + water → acid → BLUE litmus turns RED (ನೀಲಿ → ಕೆಂಪು). \n"
                "Memory trick: M→B (Metal→Basic), N→A (Non-metal→Acidic)."
            ),
            "related_params": ["initialState", "showHints"]
        },
        {
            "id": 3,
            "title": "Acid Rain — SO₂ in the Atmosphere",
            "description": (
                "Industrial burning of sulfur-containing fuels produces SO₂ which "
                "dissolves in atmospheric moisture to form sulfurous acid (H₂SO₃), "
                "causing acid rain. The simulation demonstrates the same chemistry "
                "that makes acid rain harmful."
            ),
            "key_insight": (
                "Factory chimneys → SO₂ into air → dissolves in rain clouds → H₂SO₃ → "
                "acid rain falls → damages marble buildings, metal structures, forests. "
                "This is a direct real-world application of the SO₂ + H₂O → H₂SO₃ reaction."
            ),
            "related_params": ["initialState"]
        }
    ]
}

# =============================================================================
# METALS vs NON-METALS COMPARISON — Config
# =============================================================================
SIMULATIONS_KN["metals_nonmetals_compare_kn"] = {
    "id": "metals_nonmetals_compare_kn",
    "title": "ಲೋಹ ಮತ್ತು ಅಲೋಹ ಹೋಲಿಕೆ (Metals vs Non-metals Comparison)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter4_simulation9_metals_nonmetals_compare_kn.html",
    "description": (
        "8 ಭೌತಿಕ ಮತ್ತು ರಾಸಾಯನಿಕ ಗುಣಗಳನ್ನು (ದ್ಯುತಿ, ನಮ್ಯತೆ, ಸೆಳೆತ, ಧ್ವನಿ, ಉಷ್ಣ ವಾಹಕತೆ, "
        "ವಿದ್ಯುತ್ ವಾಹಕತೆ, ಕಾಠಿಣ್ಯ, ಆಕ್ಸೈಡ್ ಸ್ವಭಾವ) ಲೋಹ ಮತ್ತು ಅಲೋಹಗಳ ನಡುವೆ ಹೋಲಿಸಿ. "
        "An 8-property interactive comparison chart: tap any property button "
        "(lustre, malleability, ductility, sonority, heat conduction, electrical conduction, "
        "hardness, oxide nature) to see side-by-side metal vs non-metal cards. "
        "Includes a summary table and a built-in quiz. "
        "Serves as a chapter-end consolidation tool covering all metal/non-metal properties."
    ),
    "cannot_demonstrate": [
        "Individual element-level detail (only general metal/non-metal trends shown)",
        "Absolute quantitative values for properties",
        "Exceptions in interactive form (shown only as text reminders)",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Property to Display",
            "range": (
                "initial, malleability, ductility, sonority, "
                "heat_conduction, electrical_conduction, hardness, oxide_nature"
            ),
            "url_key": "initialState",
            "effect": (
                "Sets which property comparison is auto-displayed on load.\n"
                "  'initial'               → lustre comparison (default first view)\n"
                "  'malleability'          → malleability comparison card\n"
                "  'ductility'             → ductility comparison card\n"
                "  'sonority'              → sonority comparison card\n"
                "  'heat_conduction'       → heat conductivity comparison card\n"
                "  'electrical_conduction' → electrical conductivity comparison card\n"
                "  'hardness'              → hardness comparison card\n"
                "  'oxide_nature'          → oxide nature comparison card (basic vs acidic)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the key concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Physical Properties — Metals Are Generally Shiny, Malleable, Ductile, Sonorous",
            "description": (
                "Metals as a group share physical properties: metallic lustre (shiny surface), "
                "malleability (can be beaten into sheets), ductility (can be drawn into wires), "
                "and sonority (ring when struck). Non-metals are typically the opposite."
            ),
            "key_insight": (
                "All 4 physical properties stem from the same root: free electron sea + layered "
                "atomic structure in metals. These electrons also make metals good conductors. "
                "Non-metals lack free electrons → dull, brittle, non-ductile, non-sonorous."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Chemical Property — Oxide Nature Distinguishes Metals from Non-metals",
            "description": (
                "The single most reliable chemical test: metal oxides dissolve in water to "
                "give basic solutions (turn red litmus blue); non-metal oxides give acidic "
                "solutions (turn blue litmus red)."
            ),
            "key_insight": (
                "Metal oxide → basic. Non-metal oxide → acidic. No exceptions in NCERT Class 8. "
                "(Note: some oxides like Al₂O₃ are amphoteric but this is beyond current level.) "
                "This oxide nature rule is a guaranteed exam question."
            ),
            "related_params": ["initialState", "showHints"]
        },
        {
            "id": 3,
            "title": "Important Exceptions to Remember",
            "description": (
                "Not all metals are hard solids — sodium and potassium can be cut with a knife. "
                "Mercury is a liquid metal at room temperature. "
                "Diamond (carbon, a non-metal) is the hardest natural substance. "
                "Graphite (carbon, a non-metal) conducts electricity — unlike most non-metals."
            ),
            "key_insight": (
                "Exceptions = favourite exam questions! Na, K: soft metals (stored in oil). "
                "Hg: only liquid metal. Diamond: hardest substance. Graphite: conducting non-metal. "
                "These 4 exceptions fully cover the NCERT Class 8 exception list."
            ),
            "related_params": ["initialState"]
        }
    ]
}

# =============================================================================
# WEATHERING AND EROSION — Config
# =============================================================================
SIMULATIONS_KN["weathering_erosion_kn"] = {
    "id": "weathering_erosion_kn",
    "title": "ವಾತಾವರಣ ಮತ್ತು ಕೊರೆತ (Weathering and Erosion)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation10_weathering_erosion_kn.html",
    "description": (
        "ಪರ್ವತ, ನದಿ ಕಲ್ಲುಗಳು, ಮತ್ತು ಸಮುದ್ರ ಬಂಡೆ ದೃಶ್ಯಗಳಲ್ಲಿ ಲಕ್ಷಾಂತರ ವರ್ಷಗಳ ಕಾಲ-ಪ್ರಯಾಣ ಮಾಡಿ. "
        "Three animated landscape scenes — mountain, river rocks, sea cliff — "
        "each with a time-travel slider spanning 0 to 1 million years. "
        "See mountains erode and shed rocks, river stones become rounded smooth pebbles, "
        "and sea cliffs develop caves then sea stacks. "
        "Teaches that weathering (breaking rocks) + erosion (moving fragments to new locations) "
        "together continually reshape Earth's surface over geological time."
    ),
    "cannot_demonstrate": [
        "Exact geological timescales for specific landforms",
        "Chemical weathering reactions in detail (only physical weathering shown animated)",
        "Deposition and sedimentary rock formation process",
        "Soil formation from weathered rock",
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Scene / Time State",
            "range": (
                "initial, mountain, river, cliff, "
                "mountain_aged, river_aged, cliff_aged"
            ),
            "url_key": "initialState",
            "effect": (
                "Sets which scene and time period is auto-loaded.\n"
                "  'initial'       → mountain scene at time=0 (default)\n"
                "  'mountain'      → mountain scene at time=0 (fresh peak, snow cap)\n"
                "  'river'         → river scene at time=0 (angular rocks in river)\n"
                "  'cliff'         → sea cliff scene at time=0 (steep intact cliff face)\n"
                "  'mountain_aged' → mountain scene at time=100% (peak eroded, sediment spread)\n"
                "  'river_aged'    → river scene at time=100% (smooth rounded pebbles, sand)\n"
                "  'cliff_aged'    → sea cliff scene at time=100% (cave + sea stack formed)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the concept card.\n"
                "  true  → show the key concept explanation card (default)\n"
                "  false → hide the concept card"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Weathering — Breaking Rocks Into Smaller Pieces",
            "description": (
                "Weathering is the process by which rocks are broken into smaller "
                "fragments by physical or chemical agents. Physical weathering includes "
                "temperature changes (expansion/contraction), ice wedging, and plant roots. "
                "Chemical weathering includes dissolution, oxidation, and acid rain reactions."
            ),
            "key_insight": (
                "Rock doesn't need to move to be weathered — it breaks IN PLACE. "
                "Water enters cracks → freezes → expands 9% → cracks widen → mechanical breakage. "
                "This is called 'frost wedging' — the main weathering force in cold climates."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Erosion — Moving Fragments to New Locations",
            "description": (
                "Erosion is the transport of weathered rock fragments by water, wind, "
                "ice, or gravity to new locations. Erosion is what shapes valleys, "
                "smooths river pebbles, and retreats cliff faces."
            ),
            "key_insight": (
                "River erosion: angular rocks bounce along riverbed → edges knock off → "
                "rocks become rounded smooth pebbles (abrasion). "
                "Sea erosion: waves pound cliff base → cave forms → arch → sea stack. "
                "Wind erosion: fine particles carried away, large rocks left behind (deflation)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Geological Time — Millions of Years to Reshape Landscapes",
            "description": (
                "Weathering and erosion are extremely slow processes — imperceptibly slow "
                "on a human timescale but enormously powerful over geological time. "
                "The Grand Canyon took 5–6 million years to form. "
                "Smooth river pebbles take thousands of years to form."
            ),
            "key_insight": (
                "Rate of erosion for rivers: ~1 mm per year at riverbed. "
                "It took the Colorado River 5–6 million years to carve 1.6 km deep Grand Canyon. "
                "Yet these are IRREVERSIBLE changes — eroded mountains don't regrow! "
                "This is why understanding these processes matters for land use planning."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

# =============================================================================
# QUIZ QUESTIONS — RUSTING EXPERIMENT
# =============================================================================
QUIZ_QUESTIONS_KN["rusting_experiment_kn"] = [
    {
        "id": "rusting_q1",
        "challenge": (
            "Set the simulation to Day 7 (experiment complete) and explain: "
            "which tube showed rust and why? What does this prove about the "
            "conditions needed for rusting?\n\n"
            "(ದಿನ 7 ತೋರಿಸಿ — ಯಾವ ಟ್ಯೂಬ್‌ನಲ್ಲಿ ತುಕ್ಕು ಬಂತು, ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "day7"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'day7'. The slider auto-advances to Day 7 — "
                "the experiment is complete. Observe which nail has rusted."
            ),
            "attempt_2": (
                "Choose 'day7': Tube C (air + water) shows heavy rust. "
                "Tubes A and B remain rust-free. "
                "The conclusion: BOTH oxygen and water are needed simultaneously."
            ),
            "attempt_3": (
                "Set 'initialState=day7': Only Tube C (ಗಾಳಿ + ನೀರು) rusted. "
                "Tube A (dry air only) = no rust. Tube B (water, no air) = no rust. "
                "Proof: rusting requires O₂ AND H₂O together."
            )
        },
        "concept_reminder": (
            "Rusting needs BOTH oxygen AND water simultaneously. "
            "Tube A = air only → no rust (no water). "
            "Tube B = water only → no rust (oil seal blocked oxygen). "
            "Tube C = air + water → RUST! (both present). "
            "Chemical equation: 4Fe + 3O₂ + 6H₂O → 2Fe₂O₃·3H₂O "
            "(ತುಕ್ಕಿಗೆ ಗಾಳಿ + ನೀರು ಎರಡೂ ಅಗತ್ಯ!)"
        )
    },
    {
        "id": "rusting_q2",
        "challenge": (
            "Show the experiment at Day 3 — the mid-point where rust is just starting. "
            "Explain why Tube C shows rust first while A and B still look clean.\n\n"
            "(ದಿನ 3 ತೋರಿಸಿ — ಟ್ಯೂಬ್ C ಮಾತ್ರ ತುಕ್ಕು ಆರಂಭಿಸಲು ಏಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "day3"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'day3'. The slider moves to Day 3 — "
                "you can see rust beginning in Tube C while A and B are still clean."
            ),
            "attempt_2": (
                "Choose 'day3': Only Tube C (both O₂ and H₂O present) starts rusting. "
                "Tube A has air but no water — reaction cannot proceed without water. "
                "Tube B has water but no oxygen — sealed by oil layer."
            ),
            "attempt_3": (
                "Set 'initialState=day3': Rusting is a slow chemical process. "
                "At Day 3, Tube C shows brown spots (Fe₂O₃ forming). "
                "This is the early stage of: 4Fe + 3O₂ + 6H₂O → 2Fe₂O₃·3H₂O."
            )
        },
        "concept_reminder": (
            "Rusting is a SLOW chemical reaction — it takes several days, not hours. "
            "At Day 3, only Tube C (air + water) shows rust beginning. "
            "The oil layer in Tube B creates an effective seal against dissolved oxygen. "
            "Boiling water removes dissolved O₂ — another reason Tube B doesn't rust. "
            "(ತುಕ್ಕು ನಿಧಾನ ಪ್ರಕ್ರಿಯೆ!)"
        )
    },
    {
        "id": "rusting_q3",
        "challenge": (
            "Show the INITIAL state (Day 0). Explain: a bicycle left outside in rain rusts "
            "quickly, but an identical bicycle kept indoors in a dry room does not rust. "
            "Which tube in the experiment represents each scenario, and why?\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಸೈಕಲ್ ಠ ಮತ್ತು ಅಂದಿನ ಕೋಣೆ ಸೈಕಲ್ ಯಾವ ಟ್ಯೂಬ್‌ಗೆ ಅನುರೂಪ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. This shows Day 0 — "
                "read the tube labels and think about real-world conditions."
            ),
            "attempt_2": (
                "Choose 'initial': Outdoor bicycle = Tube C (air + water from rain). "
                "Indoor dry bicycle = Tube A (air only, no moisture). "
                "Tube A → no rust, just like the indoor bicycle."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Rain provides the water. Air provides oxygen. "
                "Both present outdoors → Tube C → rust. "
                "Dry indoor room has air but no moisture → Tube A → no rust."
            )
        },
        "concept_reminder": (
            "Applying the experiment to real life: "
            "Outdoor bicycle in rain = air (O₂) + water → Tube C → rusts. "
            "Indoor dry bicycle = air (O₂) only, no water → Tube A → no rust. "
            "Prevention: oil the chain (like Tube B's oil seal!) = blocks water. "
            "Paint the frame = blocks both water and oxygen. "
            "(ವಾಸ್ತವ ಜೀವನದ ತೊಂದರೆ, ಪ್ರಯೋಗ ಪರಿಹಾರ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — METAL OXIDE REACTION
# =============================================================================
QUIZ_QUESTIONS_KN["metal_oxide_reaction_kn"] = [
    {
        "id": "metal_oxide_q1",
        "challenge": (
            "Demonstrate the full metal oxide experiment: burn magnesium, dissolve in water, "
            "and complete the litmus test to prove the oxide is basic.\n\n"
            "(ಸಂಪೂರ್ಣ ಪ್ರಯೋಗ ಮಾಡಿ — Mg ಸುಡಿ, MgO ಕರಗಿಸಿ, ಲಿಟ್ಮಸ್ ಪರೀಕ್ಷಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "tested"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'tested'. "
                "The simulation auto-runs all 3 steps: burns Mg, dissolves MgO, tests litmus."
            ),
            "attempt_2": (
                "Choose 'tested': You see the completed experiment — red litmus has turned BLUE, "
                "confirming MgO is a basic (alkaline) oxide."
            ),
            "attempt_3": (
                "Set 'initialState=tested': The red litmus strip turns blue = pH > 7 = basic. "
                "Complete reaction chain: 2Mg+O₂→2MgO, MgO+H₂O→Mg(OH)₂."
            )
        },
        "concept_reminder": (
            "Metal oxide experiment chain: "
            "Step 1: 2Mg + O₂ → 2MgO (brilliant white light). "
            "Step 2: MgO + H₂O → Mg(OH)₂ (dissolves). "
            "Step 3: Mg(OH)₂ solution → red litmus turns blue (basic, pH > 7). "
            "CONCLUSION: Metal oxides are BASIC in nature. "
            "(ಕೆಂಪು → ನೀಲಿ = ಕ್ಷಾರೀಯ ಆಕ್ಸೈಡ್!)"
        )
    },
    {
        "id": "metal_oxide_q2",
        "challenge": (
            "Show just the burning step. Describe what you observe and explain "
            "why magnesium burns with such a bright white light.\n\n"
            "(ಉರಿಸುವ ಹಂತ ತೋರಿಸಿ — ಪ್ರಕಾಶಮಾನ ಬೆಳಕಿಗೆ ಕಾರಣ ಏನು?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "burned"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'burned'. The simulation auto-clicks the burn button "
                "and shows the blinding white light and MgO ash forming."
            ),
            "attempt_2": (
                "Choose 'burned': After burning, shiny Mg ribbon becomes white powdery ash (MgO). "
                "The reaction: 2Mg + O₂ → 2MgO releases huge energy → white light."
            ),
            "attempt_3": (
                "Set 'initialState=burned': Mg combustion temperature ~3100°C → "
                "energy emitted as brilliant white light + UV. Never look directly!"
            )
        },
        "concept_reminder": (
            "Magnesium burning observations: "
            "Bright white/silver ribbon → burns with dazzling white light → white powdery ash. "
            "Why so bright? High reaction enthalpy releases energy as visible + UV light "
            "(temperature ~3100°C). "
            "Product: MgO (magnesium oxide) — a white powder. "
            "This is an oxidation reaction (combining with oxygen). "
            "(ಪ್ರಕಾಶಮಾನ ಬೆಳಕು = ಅಪಾರ ಶಕ್ತಿ ಬಿಡುಗಡೆ!)"
        )
    },
    {
        "id": "metal_oxide_q3",
        "challenge": (
            "Show the initial state. Predict: if we did the same experiment with copper "
            "(Cu) instead of magnesium, would the resulting copper oxide solution "
            "turn red litmus blue or blue litmus red? Explain.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ತಾಮ್ರ ಆಕ್ಸೈಡ್ ಯಾವ ಲಿಟ್ಮಸ್ ಬದಲಿಸುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Think: copper is a metal. "
                "What happens when metals react with oxygen?"
            ),
            "attempt_2": (
                "Choose 'initial': The rule is — ALL metal oxides are basic. "
                "Copper is a metal → CuO is a metal oxide → basic → red litmus turns blue."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Cu + O₂ → CuO (copper oxide). "
                "CuO is a metal oxide → basic → red litmus → blue. "
                "Same conclusion as MgO. ALL metal oxides behave the same way."
            )
        },
        "concept_reminder": (
            "General rule: Metal + O₂ → Metal Oxide (basic). "
            "Applies to ALL metals: Mg, Cu, Fe, Na, Ca, Al, etc. "
            "All metal oxides are basic → turn red litmus blue → pH > 7. "
            "This is why the rule is stated as a general principle, not just for Mg. "
            "(ಎಲ್ಲಾ ಲೋಹ ಆಕ್ಸೈಡ್ = ಕ್ಷಾರೀಯ = ಕೆಂಪು ಲಿಟ್ಮಸ್ ನೀಲಿ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — NON-METAL OXIDE REACTION
# =============================================================================
QUIZ_QUESTIONS_KN["nonmetal_oxide_reaction_kn"] = [
    {
        "id": "nonmetal_oxide_q1",
        "challenge": (
            "Run the full non-metal oxide experiment: burn sulfur, dissolve in water, "
            "and complete the litmus test to prove the oxide is acidic.\n\n"
            "(ಸಂಪೂರ್ಣ ಪ್ರಯೋಗ ಮಾಡಿ — S ಸುಡಿ, SO₂ ಕರಗಿಸಿ, ಲಿಟ್ಮಸ್ ಪರೀಕ್ಷಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "tested"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'tested'. "
                "All 3 steps auto-run: burns sulfur, dissolves SO₂, tests litmus."
            ),
            "attempt_2": (
                "Choose 'tested': Blue litmus turns RED — proving the SO₂ solution is acidic. "
                "Complete chain: S+O₂→SO₂, SO₂+H₂O→H₂SO₃."
            ),
            "attempt_3": (
                "Set 'initialState=tested': Blue litmus strip → red = pH < 7 = acidic. "
                "Non-metal oxide (SO₂) forms an acid when dissolved — confirms the rule."
            )
        },
        "concept_reminder": (
            "Non-metal oxide experiment chain: "
            "Step 1: S + O₂ → SO₂ (blue flame, pungent smell). "
            "Step 2: SO₂ + H₂O → H₂SO₃ (sulfurous acid forms). "
            "Step 3: H₂SO₃ solution → blue litmus turns red (acidic, pH < 7). "
            "CONCLUSION: Non-metal oxides are ACIDIC in nature. "
            "(ನೀಲಿ → ಕೆಂಪು = ಆಮ್ಲೀಯ ಆಕ್ಸೈಡ್!)"
        )
    },
    {
        "id": "nonmetal_oxide_q2",
        "challenge": (
            "Show the sulfur burning step. Describe the color of the flame "
            "and explain how this differs from magnesium burning.\n\n"
            "(ಸಲ್ಫರ್ ಉರಿಯುವ ಹಂತ ತೋರಿಸಿ — ಜ್ವಾಲೆ ಬಣ್ಣ Mg ಜ್ವಾಲೆಯಿಂದ ಹೇಗೆ ಭಿನ್ನ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "burned"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'burned'. Watch the characteristic blue flame "
                "of sulfur combustion appear."
            ),
            "attempt_2": (
                "Choose 'burned': Sulfur burns with a BLUE flame (unlike Mg's white). "
                "SO₂ gas (colorless, pungent) collects in the gas jar."
            ),
            "attempt_3": (
                "Set 'initialState=burned': Comparison: Mg = brilliant WHITE flame (~3100°C). "
                "Sulfur = characteristic BLUE flame (~900°C). Different non-metals = different flame colors."
            )
        },
        "concept_reminder": (
            "Flame color comparison: "
            "Mg (metal): brilliant white/silver flame — very high energy combustion. "
            "Sulfur (non-metal): characteristic BLUE flame — lower temperature. "
            "Carbon (non-metal): yellow-orange flame (incomplete) or blue (complete). "
            "Natural gas (methane): blue flame when burning completely. "
            "Flame color indicates the element and combustion temperature. "
            "(ಸಲ್ಫರ್ = ನೀಲಿ ಜ್ವಾಲೆ, Mg = ಬಿಳಿ ಜ್ವಾಲೆ!)"
        )
    },
    {
        "id": "nonmetal_oxide_q3",
        "challenge": (
            "Show the initial state. Compare: if metal oxide → basic (red litmus → blue), "
            "what does non-metal oxide → acidic mean for litmus? "
            "Complete the contrast table in your answer.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಲೋಹ ಮತ್ತು ಅಲೋಹ ಆಕ್ಸೈಡ್ ಲಿಟ್ಮಸ್ ವ್ಯತ್ಯಾಸ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. Note the concept card — "
                "it shows the contrast between metal and non-metal oxide nature."
            ),
            "attempt_2": (
                "Choose 'initial': Metal oxide → basic → red litmus turns BLUE. "
                "Non-metal oxide → acidic → blue litmus turns RED. Complete opposites!"
            ),
            "attempt_3": (
                "Set 'initialState=initial': "
                "MgO (metal oxide) → base → RED→BLUE. "
                "SO₂ (non-metal oxide) → acid → BLUE→RED."
            )
        },
        "concept_reminder": (
            "The key contrast table for exams: \n"
            "Metal oxide (MgO, CaO, Na₂O) → dissolves in water → BASE → red litmus BLUE. \n"
            "Non-metal oxide (SO₂, CO₂, P₂O₅) → dissolves in water → ACID → blue litmus RED. \n"
            "Memory technique: M→B (Metal→Basic) and N→A (Non-metal→Acidic). \n"
            "Exam guaranteed: 'What happens to blue litmus when non-metal oxide dissolves?' \n"
            "Answer: Blue litmus turns RED (it becomes acidic). \n"
            "(ಲೋಹ = ಮೂಲ | ಅಲೋಹ = ಆಮ್ಲ — ವಿರುದ್ಧ!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — METALS vs NON-METALS COMPARISON
# =============================================================================
QUIZ_QUESTIONS_KN["metals_nonmetals_compare_kn"] = [
    {
        "id": "compare_q1",
        "challenge": (
            "Show the OXIDE NATURE comparison. Explain the single most important "
            "chemical difference between metal oxides and non-metal oxides.\n\n"
            "(ಆಕ್ಸೈಡ್ ಸ್ವಭಾವ ಹೋಲಿಕೆ ತೋರಿಸಿ — ಲೋಹ ಮತ್ತು ಅಲೋಹ ಆಕ್ಸೈಡ್ ಪ್ರಮುಖ ವ್ಯತ್ಯಾಸ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "oxide_nature"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'oxide_nature'. "
                "The oxide nature comparison card auto-loads."
            ),
            "attempt_2": (
                "Choose 'oxide_nature': Metal oxides form basic solutions (MgO → Mg(OH)₂). "
                "Non-metal oxides form acidic solutions (SO₂ → H₂SO₃)."
            ),
            "attempt_3": (
                "Set 'initialState=oxide_nature': "
                "The comparison shows: Metal oxide → basic (red litmus blue). "
                "Non-metal oxide → acidic (blue litmus red)."
            )
        },
        "concept_reminder": (
            "Oxide nature is the CHEMICAL property contrast between metals and non-metals: "
            "Metal oxide + H₂O → BASE (pH > 7) → red litmus turns BLUE. "
            "Non-metal oxide + H₂O → ACID (pH < 7) → blue litmus turns RED. "
            "Examples: MgO (basic), CaO (basic), SO₂ (acidic), CO₂ (acidic). "
            "(ಲೋಹ ಆಕ್ಸೈಡ್ = ಕ್ಷಾರ | ಅಲೋಹ ಆಕ್ಸೈಡ್ = ಆಮ್ಲ!)"
        )
    },
    {
        "id": "compare_q2",
        "challenge": (
            "Show the electrical conductivity comparison. Name two metals used "
            "as electrical conductors in real life and explain WHY they conduct.\n\n"
            "(ವಿದ್ಯುತ್ ವಾಹಕತೆ ಹೋಲಿಕೆ ತೋರಿಸಿ — ವಿದ್ಯುತ್ ಉದ್ಯಮದಲ್ಲಿ ಯಾವ ಲೋಹ ಬಳಸುತ್ತಾರೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "electrical_conduction"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'electrical_conduction'. "
                "The electrical conductivity comparison card auto-loads."
            ),
            "attempt_2": (
                "Choose 'electrical_conduction': Metals conduct electricity because "
                "they have free electrons. Copper and aluminium are the main wire metals."
            ),
            "attempt_3": (
                "Set 'initialState=electrical_conduction': "
                "Copper = best conductor for home wiring (high conductivity + ductility). "
                "Aluminium = used for high-tension power lines (lighter weight)."
            )
        },
        "concept_reminder": (
            "Why metals conduct electricity: free valence electrons move through the metal lattice. "
            "Voltage applied → electrons flow → electric current. "
            "Why non-metals don't: all electrons are tightly bonded → no free charge carriers. "
            "Real uses: copper (home wiring), aluminium (power transmission lines), "
            "tungsten (light bulb filament — high melting point). "
            "Exception: graphite (carbon, non-metal) conducts — used in electrodes. "
            "(ಮುಕ್ತ ಇಲೆಕ್ಟ್ರಾನ್ = ವಿದ್ಯುತ್ ವಾಹಕ!)"
        )
    },
    {
        "id": "compare_q3",
        "challenge": (
            "Show the INITIAL state (lustre). Explain why metals have a shiny lustre "
            "while non-metals appear dull. Connect this to the atomic structure.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ / ದ್ಯುತಿ ತೋರಿಸಿ — ಲೋಹ ಹೊಳೆಯಲು ಕಾರಣ ಏನು?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. "
                "The default lustre comparison card appears — read both sides."
            ),
            "attempt_2": (
                "Choose 'initial': Metals are shiny because their free electrons "
                "absorb and re-emit light efficiently. Non-metals appear dull."
            ),
            "attempt_3": (
                "Set 'initialState=initial': Free electron sea in metals reflects light "
                "at all wavelengths uniformly → silvery metallic shine. "
                "Non-metals have no free electrons → light is absorbed differently → dull appearance."
            )
        },
        "concept_reminder": (
            "Metallic lustre origin: The free electron sea in metals interacts strongly "
            "with incoming light — electrons absorb photons and immediately re-emit them. "
            "This efficient re-emission gives the characteristic silvery metallic shine. "
            "Non-metals (coal, sulfur, phosphorus) have no sea of electrons → "
            "light energy is absorbed without being re-emitted uniformly → dull. "
            "Note: freshly cut sodium is shiny too (metallic lustre) but quickly dulls "
            "as it oxidises — another reminder that metallic lustre = free electrons. "
            "(ಮುಕ್ತ ಇಲೆಕ್ಟ್ರಾನ್ ಬೆಳಕು ಹಿಂದಿರುಗಿಸುತ್ತದೆ = ಹೊಳಪು!)"
        )
    }
]

# =============================================================================
# QUIZ QUESTIONS — WEATHERING AND EROSION
# =============================================================================
QUIZ_QUESTIONS_KN["weathering_erosion_kn"] = [
    {
        "id": "weathering_q1",
        "challenge": (
            "Show the AGED MOUNTAIN scene (1 million years of erosion). "
            "Describe what has changed and explain which weathering forces caused it.\n\n"
            "(ಹಳೆಯ ಪರ್ವತ ದೃಶ್ಯ ತೋರಿಸಿ — ಯಾವ ಬದಲಾವಣೆಗಳಾದವು, ಕಾರಣ ಏನು?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "mountain_aged"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'mountain_aged'. "
                "This loads the mountain scene at maximum time — a heavily eroded landscape."
            ),
            "attempt_2": (
                "Choose 'mountain_aged': The peak has lowered, rocks have fallen, "
                "sediment has spread. Temperature changes, frost wedging, and plant roots caused this."
            ),
            "attempt_3": (
                "Set 'initialState=mountain_aged': Over 1 million years — "
                "sharp peaks become gentle hills, fallen rocks form sediment plains, "
                "snow cap disappears. Weathering + gravity erosion together."
            )
        },
        "concept_reminder": (
            "Mountain weathering over 1 million years: "
            "1. Temperature changes → rock expands/contracts → micro-cracks form. "
            "2. Water in cracks → freezes → expands 9% → cracks widen (frost wedging). "
            "3. Plant roots grow into cracks → split rocks further. "
            "4. Gravity + rain → fallen rocks roll downhill (erosion = transport). "
            "Result: sharp peaks → rounded gentle hills → flat plains (over millions of years). "
            "(ವಾತಾವರಣ + ಕೊರೆತ = ಲಕ್ಷಾಂತರ ವರ್ಷ ಭೂರೂಪ ಬದಲಾವಣೆ!)"
        )
    },
    {
        "id": "weathering_q2",
        "challenge": (
            "Show the AGED RIVER ROCKS scene. Explain the process that transformed "
            "angular rocks into smooth rounded pebbles in the riverbed.\n\n"
            "(ಹಳೆಯ ನದಿ ಕಲ್ಲುಗಳ ದೃಶ್ಯ ತೋರಿಸಿ — ಕೋನೀಯ ಕಲ್ಲು ನಯವಾಗಲು ಕಾರಣ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "river_aged"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'river_aged'. "
                "This loads the river scene at maximum time — smooth pebbles everywhere."
            ),
            "attempt_2": (
                "Choose 'river_aged': Angular rocks → smooth round pebbles through 'abrasion'. "
                "Rocks tumble in the river current → edges chip off → gradually rounded."
            ),
            "attempt_3": (
                "Set 'initialState=river_aged': Process called abrasion: "
                "rocks roll along riverbed → collide → edges break off → smooth oval pebbles. "
                "Sand accumulates from fine particles."
            )
        },
        "concept_reminder": (
            "River rock smoothing = ABRASION (a type of erosion): "
            "Angular rocks tumble along the riverbed carried by water current. "
            "Rocks knock against each other and the riverbed → edges and corners break off. "
            "Gradually: sharp angular → oval → rounded smooth pebble. "
            "Fine particles produced become sand → settles as riverbed deposit. "
            "This process takes thousands of years of constant tumbling. "
            "LINK TO REAL LIFE: Beach pebbles and riverbed pebbles are always smooth "
            "because of this same abrasion process. New quarry rocks are angular. "
            "(ಉಜ್ಜಾಟ = ಕೋನೀಯ → ನಯ!)"
        )
    },
    {
        "id": "weathering_q3",
        "challenge": (
            "Show the INITIAL state (fresh mountain at time=0). "
            "Explain the difference between weathering and erosion using the mountain scene.\n\n"
            "(ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ — ವಾತಾವರಣ ಮತ್ತು ಕೊರೆತ ವ್ಯತ್ಯಾಸ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'initial'. "
                "This shows a fresh intact mountain — the starting point before any changes."
            ),
            "attempt_2": (
                "Choose 'initial': Weathering = breaking rocks IN PLACE (no movement). "
                "Erosion = MOVING the broken fragments to a new location."
            ),
            "attempt_3": (
                "Set 'initialState=initial': "
                "On the mountain: cracks forming = weathering. "
                "Rocks rolling downhill to form sediment = erosion."
            )
        },
        "concept_reminder": (
            "KEY DISTINCTION for exams: \n"
            "WEATHERING = breaking or decomposing rocks without moving them. "
            "Agents: temperature, frost, plant roots, acid rain. IN PLACE. \n"
            "EROSION = picking up and transporting weathered material to a new place. "
            "Agents: water (rivers, rain), wind, ice (glaciers), gravity. TRANSPORT. \n"
            "They work TOGETHER: weathering produces fragments → erosion carries them away. \n"
            "Without weathering, erosion has nothing to transport. "
            "Without erosion, weathered material would pile up in place. "
            "(ವಾತಾವರಣ = ಒಡೆಯುವಿಕೆ | ಕೊರೆತ = ಸಾಗಿಸುವಿಕೆ!)"
        )
    }
]

# =============================================================================
# PHYSICAL CHANGES SIMULATION
# ಭೌತಿಕ ಬದಲಾವಣೆಗಳು – ಹೊಸ ಪದಾರ್ಥ ಇಲ್ಲ
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["physical_changes_kn"] = {
    "title": "ಭೌತಿಕ ಬದಲಾವಣೆಗಳು (Physical Changes)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation1_physical_changes_kn.html",
    "description": (
        "Kannada simulation where students select from six everyday examples "
        "(paper folding, chalk crushing, ice melting, balloon inflating, rubber stretching, "
        "spring compressing) and observe the 'before → after' transformation. "
        "Each example visually demonstrates that the appearance changes but no new "
        "substance is formed — the defining signature of a physical change. "
        "Students also see whether the change is reversible or irreversible."
    ),
    "cannot_demonstrate": [
        "Chemical changes or new substance formation",
        "Quantitative measurement of mass conservation",
        "Changes at the molecular/atomic level",
        "Temperature-induced state changes (covered in simulation 4)"
    ],
    "initial_params": {"initialState": "ice", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Example to Demonstrate",
            "range": "initial, paper, chalk, ice, balloon, rubber, spring",
            "url_key": "initialState",
            "effect": (
                "Selects an example and auto-performs the physical change:\n"
                "  'initial' → no example selected (default start)\n"
                "  'paper'   → fold paper flat sheet → boat (reversible physical change)\n"
                "  'chalk'   → crush chalk stick → powder (irreversible physical change)\n"
                "  'ice'     → melt ice cube → water (reversible state change)\n"
                "  'balloon' → inflate balloon (reversible physical change)\n"
                "  'rubber'  → stretch rubber band (reversible physical change)\n"
                "  'spring'  → compress spring (reversible physical change)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the learning panel and takeaway sections."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Physical Change Leaves the Substance Unchanged",
            "description": (
                "In a physical change, the appearance (shape, size, or state) of a "
                "substance changes but the substance itself remains the same — no new "
                "material is formed."
            ),
            "key_insight": (
                "Folded paper is still paper. Crushed chalk is still calcium carbonate. "
                "Melted ice is still H₂O. The chemical identity never changes in a "
                "physical change."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Reversible vs Irreversible Physical Changes",
            "description": (
                "Some physical changes can be undone (reversible) while others cannot "
                "(irreversible), even though both involve only a physical change."
            ),
            "key_insight": (
                "Ice → water → ice again = reversible. Chalk stick → chalk powder = "
                "irreversible (you cannot un-crush chalk). Both are physical changes "
                "because no new substance forms."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Real-World Physical Changes Are Everywhere",
            "description": (
                "Physical changes occur constantly in daily life — bending a wire, "
                "stretching a rubber band, inflating a tyre, melting butter, cutting "
                "vegetables — all involve shape or state change without new substance."
            ),
            "key_insight": (
                "The key test: ask 'Is the substance still the same?' If yes → physical "
                "change. Ask 'Can it be reversed?' to determine reversibility."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# CHEMICAL CHANGES SIMULATION
# ರಾಸಾಯನಿಕ ಬದಲಾವಣೆಗಳು – ಹೊಸ ಪದಾರ್ಥಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["chemical_changes_kn"] = {
    "title": "ರಾಸಾಯನಿಕ ಬದಲಾವಣೆಗಳು (Chemical Changes)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation2_chemical_changes_kn.html",
    "description": (
        "Kannada simulation demonstrating chemical changes through two classic experiments: "
        "(1) Vinegar + baking soda → vigorous bubbling, CO₂ gas released, new substances "
        "formed (sodium acetate, water, carbon dioxide). "
        "(2) Exhaling CO₂ into limewater → milky white precipitate (CaCO₃) forms. "
        "Students observe the hallmark signs of chemical change: bubble formation, "
        "colour change, and irreversibility."
    ),
    "cannot_demonstrate": [
        "Reversible chemical changes",
        "Exothermic/endothermic energy changes (heat or cold produced)",
        "Balanced stoichiometric calculations",
        "Other types of chemical reactions beyond acid-base and precipitation"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Experiment State",
            "range": "initial, vinegar_reacted, limewater, limewater_reacted",
            "url_key": "initialState",
            "effect": (
                "Controls which experiment and reaction state is shown:\n"
                "  'initial'          → vinegar + baking soda tab, before reaction\n"
                "  'vinegar_reacted'  → vinegar poured onto baking soda, CO₂ bubbles visible\n"
                "  'limewater'        → limewater tab selected, clear water in tube\n"
                "  'limewater_reacted'→ CO₂ blown into limewater, water turned milky white"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the learning panel, takeaway, and equation box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Chemical Change Creates New Substances",
            "description": (
                "In a chemical change, the original substances react to form entirely "
                "new substances with different properties. The change is generally permanent."
            ),
            "key_insight": (
                "Vinegar + baking soda → CO₂ gas + water + sodium acetate. "
                "You cannot get the original vinegar and baking soda back — "
                "this is the key distinction from physical change."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Observable Signs of Chemical Change",
            "description": (
                "Chemical changes produce observable evidence: gas bubble formation, "
                "colour change, precipitate formation, heat or light production, "
                "and new odours."
            ),
            "key_insight": (
                "Vigorous bubbling in the vinegar-baking soda reaction = CO₂ gas forming. "
                "Limewater turning milky = CaCO₃ precipitate forming. "
                "Both are clear evidence that a chemical change has occurred."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Testing for CO₂ with Limewater",
            "description": (
                "Limewater (calcium hydroxide solution) is a standard chemical test for "
                "the presence of carbon dioxide gas. CO₂ + Ca(OH)₂ → CaCO₃ (milky) + H₂O."
            ),
            "key_insight": (
                "If limewater turns milky, CO₂ is present. This is a real lab technique "
                "used in science experiments worldwide — a direct application of the "
                "acid-base → salt + water reaction type."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# REVERSIBLE AND IRREVERSIBLE CHANGES SIMULATION
# ಹಿಮ್ಮುಖ ಮತ್ತು ಅಹಿಮ್ಮುಖ ಬದಲಾವಣೆಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["reversible_irreversible_kn"] = {
    "title": "ಹಿಮ್ಮುಖ ಮತ್ತು ಅಹಿಮ್ಮುಖ ಬದಲಾವಣೆಗಳು (Reversible & Irreversible Changes)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation3_reversible_irreversible_kn.html",
    "description": (
        "Kannada quiz-style simulation where students classify 10 everyday changes as "
        "reversible (can be undone) or irreversible (cannot be undone). Changes include: "
        "melting ice, folding paper, burning paper, making curd, boiling water, cutting "
        "vegetables, inflating a balloon, cooking an egg, melting butter, and rusting iron. "
        "Immediate feedback explains the reasoning for each answer."
    ),
    "cannot_demonstrate": [
        "Showing the reverse process visually (only classifying is shown)",
        "Partial reversibility of changes",
        "Chemical equations for the irreversible processes"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Quiz State",
            "range": "initial, show_reversible, show_irreversible",
            "url_key": "initialState",
            "effect": (
                "Controls which quiz question state to demonstrate:\n"
                "  'initial'          → start of quiz, first question (melting ice) shown\n"
                "  'show_reversible'  → auto-answers first question (melting ice) as reversible\n"
                "  'show_irreversible'→ jumps to question 3 (burning paper) and answers irreversible"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and takeaway guide."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Reversible Changes Can Be Undone",
            "description": (
                "A reversible change is one where the original substance can be recovered. "
                "The change is not permanent — the material can return to its prior form."
            ),
            "key_insight": (
                "Melting ice → freeze it again = back to ice. "
                "Inflating a balloon → deflate it = original balloon. "
                "The substance identity and amount are preserved."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Irreversible Changes Are Permanent",
            "description": (
                "An irreversible change cannot be undone — the original substance is "
                "permanently altered or destroyed. New substances are often formed."
            ),
            "key_insight": (
                "Burning paper → ash (you cannot un-burn it). "
                "Making curd from milk → curd cannot become milk again. "
                "Cooking an egg → the protein structure is permanently changed."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Physical Changes Are Often Reversible; Chemical Often Irreversible",
            "description": (
                "There is a strong pattern: physical changes (shape, size, state) tend to "
                "be reversible, while chemical changes (new substances formed) tend to be "
                "irreversible. However, exceptions exist."
            ),
            "key_insight": (
                "Exception: Cutting vegetables is a physical change but irreversible. "
                "Most state changes (melting, boiling, freezing) are physical AND reversible. "
                "Understanding this pattern helps classify most everyday changes correctly."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# STATES OF MATTER SIMULATION
# ದ್ರವ್ಯದ ಸ್ಥಿತಿಗಳು – ನೀರಿನ ಪರಿವರ್ತನೆಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["states_of_matter_kn"] = {
    "title": "ದ್ರವ್ಯದ ಸ್ಥಿತಿಗಳು – ನೀರಿನ ಪರಿವರ್ತನೆಗಳು (States of Matter – Water)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation4_states_of_matter_kn.html",
    "description": (
        "Kannada temperature-slider simulation showing water (H₂O) existing in three "
        "states: solid (ice, below 0°C), liquid (water, 0–100°C), and gas (steam, above 100°C). "
        "A movable thermometer slider lets students set any temperature from -20°C to 120°C "
        "and observe the corresponding state change visually. "
        "Core message: the substance (H₂O) stays the same across all states — "
        "only the energy level and arrangement of molecules change."
    ),
    "cannot_demonstrate": [
        "Sublimation (solid → gas directly)",
        "Intermediate temperature ranges near transition points",
        "Molecular-level particle movement visualisation",
        "Latent heat concept (energy absorbed/released during state change)"
    ],
    "initial_params": {"initialState": "liquid", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "State of Water",
            "range": "solid, liquid, gas",
            "url_key": "initialState",
            "effect": (
                "Sets the temperature slider to show the corresponding state:\n"
                "  'solid'  → -10°C: ice cubes visible in container\n"
                "  'liquid' → 25°C: liquid water in container (default)\n"
                "  'gas'    → 110°C: steam/vapour rising from container"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the learning panel, concept card, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Same Substance, Three Different States",
            "description": (
                "Water (H₂O) is the same chemical substance whether it is ice, liquid "
                "water, or steam. The state depends only on temperature — the chemical "
                "identity never changes."
            ),
            "key_insight": (
                "Ice, water, and steam are all H₂O. State changes are physical changes — "
                "no new substance forms. This is why state changes are reversible: "
                "freeze water → ice; heat ice → water; boil water → steam."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Key Transition Temperatures for Water",
            "description": (
                "Water changes state at two key temperatures: 0°C (melting/freezing point) "
                "and 100°C (boiling/condensation point) at standard atmospheric pressure."
            ),
            "key_insight": (
                "0°C = melting point (solid ↔ liquid transition). "
                "100°C = boiling point (liquid ↔ gas transition). "
                "Between 0°C and 100°C, water stays liquid — the range comfortable for life."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "State Changes Are Physical and Reversible",
            "description": (
                "All three state transitions of water (freezing, melting, boiling, "
                "condensing) are physical changes because no new substance is formed "
                "and all are reversible by adjusting temperature."
            ),
            "key_insight": (
                "Ice → water (melting, heat absorbed). Water → steam (boiling, heat absorbed). "
                "Steam → water (condensation, heat released). Water → ice (freezing, heat released). "
                "Energy drives state changes; the substance H₂O is always conserved."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# FIRE TRIANGLE SIMULATION
# ಅಗ್ನಿ ತ್ರಿಕೋಣ – ದಹನಕ್ಕೆ ಅಗತ್ಯಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["fire_triangle_kn"] = {
    "title": "ಅಗ್ನಿ ತ್ರಿಕೋಣ (Fire Triangle – Conditions for Combustion)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation5_fire_triangle_kn.html",
    "description": (
        "Kannada fire-triangle simulation where students toggle the three conditions "
        "for combustion — fuel, oxygen (O₂), and heat — on and off. "
        "Fire appears only when ALL three are present simultaneously. "
        "Removing any one element extinguishes the fire. "
        "This teaches both the requirements for burning and the three methods of "
        "fire extinguishing (remove fuel, remove oxygen, remove heat)."
    ),
    "cannot_demonstrate": [
        "Specific chemical equations for combustion reactions",
        "Different ignition temperatures for different fuels",
        "Incomplete combustion or carbon monoxide formation",
        "Fire extinguisher working mechanisms in detail"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Fire Triangle State",
            "range": "initial, fire, no_fuel, no_oxygen, no_heat",
            "url_key": "initialState",
            "effect": (
                "Controls which elements of the fire triangle are activated:\n"
                "  'initial'   → no elements active, no fire (default)\n"
                "  'fire'      → all three active (fuel + oxygen + heat) → fire burns\n"
                "  'no_fuel'   → oxygen + heat only → no fire (fuel missing)\n"
                "  'no_oxygen' → fuel + heat only → no fire (oxygen missing)\n"
                "  'no_heat'   → fuel + oxygen only → no fire (heat missing)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the learning panel and takeaway sections."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Fire Requires All Three: Fuel, Oxygen, and Heat",
            "description": (
                "Combustion (burning) is a chemical reaction that requires three "
                "conditions simultaneously: a fuel (combustible material), oxygen "
                "(from air), and sufficient heat (ignition temperature). Removing "
                "any one stops the fire."
            ),
            "key_insight": (
                "The fire triangle summarises: FUEL + OXYGEN + HEAT = FIRE. "
                "All three must be present at the same time. This is why fire cannot "
                "burn in a vacuum (no oxygen) or on a very wet surface (no ignition heat)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Three Methods to Extinguish Fire",
            "description": (
                "Since fire needs all three elements, removing any one of them "
                "extinguishes the fire: (1) remove fuel, (2) remove oxygen, "
                "(3) cool below ignition temperature."
            ),
            "key_insight": (
                "Water cools the fuel (removes heat). Blanket smothers a fire (removes oxygen). "
                "CO₂ extinguishers displace oxygen (removes oxygen). "
                "Letting wood burn out (removes fuel). Each method targets one triangle element."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Combustion Is a Chemical Change",
            "description": (
                "Burning (combustion) is an example of a chemical change: fuel reacts "
                "with oxygen to produce heat, light, carbon dioxide, and water vapour. "
                "This is irreversible — ash and CO₂ cannot become wood again."
            ),
            "key_insight": (
                "Fuel + O₂ → CO₂ + H₂O + heat + light. "
                "New substances are formed (CO₂, water, ash), energy is released, "
                "and the reaction cannot be reversed — definitive signs of a chemical change."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# QUIZ QUESTIONS — PHYSICAL CHANGES (Kannada)
# 3 questions: demonstrate a state-change example, a shape-change example,
#              then an irreversible physical change
# =============================================================================
QUIZ_QUESTIONS_KN["physical_changes_kn"] = [

    {
        "id": "phys_kn_q1",
        "challenge": (
            "Demonstrate that melting ice is a PHYSICAL change. Set the simulation "
            "to show the ice melting into water and explain why this is a physical "
            "change and not a chemical change.\n\n"
            "(ಬರ್ಫ ಕರಗುವುದು ಭೌತಿಕ ಬದಲಾವಣೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "ice"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'ice' as the initialState. The simulation will show an ice cube "
                "melting into water. Note: the substance is still H₂O — no new substance formed!"
            ),
            "attempt_2": (
                "Set 'initialState' to 'ice'. The animation shows ice (solid) → water (liquid). "
                "This is a state change — a type of physical change. The substance H₂O remains."
            ),
            "attempt_3": (
                "Choose 'ice' from the dropdown. Ice melting is reversible — you can freeze "
                "the water to get ice back — confirming it is a physical change."
            )
        },
        "concept_reminder": (
            "Melting ice is a PHYSICAL change: the substance H₂O remains unchanged; "
            "only the state (solid → liquid) changes. No new substance is formed. "
            "It is reversible — freeze the water to get ice back. "
            "(ಬರ್ಫ ಕರಗುವುದು = ಭೌತಿಕ ಬದಲಾವಣೆ — H₂O ಅದೇ ಉಳಿಯುತ್ತದೆ!)"
        )
    },

    {
        "id": "phys_kn_q2",
        "challenge": (
            "Show the paper folding example. Explain why folding a flat sheet of "
            "paper into a paper boat is classified as a physical change.\n\n"
            "(ಕಾಗದ ಮಡಚುವುದು ಭೌತಿಕ ಬದಲಾವಣೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "paper"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Choose 'paper' as the initialState to show the paper being folded into a boat. "
                "The paper molecules remain the same — only the arrangement changes."
            ),
            "attempt_2": (
                "Set 'initialState=paper'. You will see flat paper → paper boat. "
                "The paper is still paper — unfolding restores the original sheet."
            ),
            "attempt_3": (
                "Select 'paper'. After the animation: the paper boat is still made of paper. "
                "You can unfold it to recover the flat sheet — reversible physical change."
            )
        },
        "concept_reminder": (
            "Paper folding = PHYSICAL change: the paper's shape changes but it is still paper. "
            "The paper molecules are simply rearranged, not chemically altered. "
            "This is reversible — unfolding the paper restores the original flat sheet. "
            "(ಕಾಗದ ಇನ್ನೂ ಕಾಗದ — ಭೌತಿಕ ಬದಲಾವಣೆ!)"
        )
    },

    {
        "id": "phys_kn_q3",
        "challenge": (
            "Show the chalk crushing example. Explain why crushing chalk is a "
            "physical change even though it CANNOT be easily reversed.\n\n"
            "(ಸೀಮೆಸುಣ್ಣ ಚೂರ್ಣ ಮಾಡುವುದು ಭೌತಿಕ ಬದಲಾವಣೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "chalk"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'chalk' as the initialState. The chalk stick is crushed into powder. "
                "Even as powder, it is still calcium carbonate (CaCO₃) — the substance did not change."
            ),
            "attempt_2": (
                "Set 'initialState=chalk'. Crushed chalk powder is still chalk (CaCO₃). "
                "No new substance formed → physical change, even though it's irreversible."
            ),
            "attempt_3": (
                "Choose 'chalk'. The simulation shows an irreversible physical change: "
                "the shape changed but the chemical identity (CaCO₃) remains. "
                "Physical changes do not always have to be reversible!"
            )
        },
        "concept_reminder": (
            "Crushing chalk = IRREVERSIBLE physical change: the chalk is smaller but "
            "is still calcium carbonate (CaCO₃). No new substance formed. "
            "Key insight: not all physical changes are reversible — "
            "irreversibility alone does NOT make a change chemical. "
            "(ಸೀಮೆಸುಣ್ಣ ಪುಡಿ ಇನ್ನೂ ಸೀಮೆಸುಣ್ಣ — ಅಹಿಮ್ಮುಖ ಭೌತಿಕ ಬದಲಾವಣೆ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — CHEMICAL CHANGES (Kannada)
# 3 questions: show harmless initial state → vinegar reaction → limewater test
# =============================================================================
QUIZ_QUESTIONS_KN["chemical_changes_kn"] = [

    {
        "id": "chem_kn_q1",
        "challenge": (
            "Show the vinegar and baking soda reaction. Demonstrate the chemical "
            "change by setting the simulation to show the reaction in progress with "
            "bubbles and CO₂ gas visible.\n\n"
            "(ವಿನಿಗರ್ + ಬೇಕಿಂಗ್ ಸೋಡಾ ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "vinegar_reacted"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'vinegar_reacted' as the initialState. "
                "This pours vinegar onto baking soda and shows the fizzing CO₂ reaction."
            ),
            "attempt_2": (
                "Set 'initialState=vinegar_reacted'. The simulation shows: "
                "vinegar poured → vigorous bubbling → CO₂ gas rising. "
                "New substances (CO₂, water, sodium acetate) have formed!"
            ),
            "attempt_3": (
                "Choose 'vinegar_reacted'. The bubbling proves CO₂ was created — "
                "a brand new substance. The original vinegar and baking soda are gone. "
                "This is an irreversible chemical change."
            )
        },
        "concept_reminder": (
            "NaHCO₃ + CH₃COOH → CO₂↑ + H₂O + CH₃COONa. "
            "Baking soda + vinegar creates NEW substances: CO₂ gas, water, sodium acetate. "
            "The vigorous bubbling shows gas production — a classic sign of chemical change. "
            "It is IRREVERSIBLE — you cannot recover the original reactants. "
            "(ಬುರುಡೆಗಳು = CO₂ ಅನಿಲ — ಹೊಸ ಪದಾರ್ಥ — ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ!)"
        )
    },

    {
        "id": "chem_kn_q2",
        "challenge": (
            "Switch to the limewater experiment and show the CO₂ test. Demonstrate "
            "how exhaling into limewater proves CO₂ is present by observing the "
            "colour change.\n\n"
            "(ಸುಣ್ಣದ ನೀರಿನ CO₂ ಪರೀಕ್ಷೆ ತೋರಿಸಿ — ಹಾಲಿನಂತಾಗುವಿಕೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "limewater_reacted"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'limewater_reacted' as the initialState. "
                "The simulation blows CO₂ through limewater and shows it turning milky white."
            ),
            "attempt_2": (
                "Set 'initialState=limewater_reacted'. The clear limewater turns milky — "
                "this is CaCO₃ (calcium carbonate) precipitate forming: a new substance!"
            ),
            "attempt_3": (
                "Choose 'limewater_reacted'. The milky colour proves that CO₂ reacted with "
                "Ca(OH)₂ to form CaCO₃. This chemical change also serves as the standard "
                "laboratory test for carbon dioxide."
            )
        },
        "concept_reminder": (
            "Ca(OH)₂ + CO₂ → CaCO₃↓ + H₂O. "
            "Limewater + carbon dioxide → calcium carbonate (milky precipitate) + water. "
            "The milky white colour indicates CaCO₃ has formed — a new solid substance. "
            "This is a standard lab test: if limewater turns milky, CO₂ is present. "
            "(ಸುಣ್ಣದ ನೀರು ಹಾಲಿನಂತಾದರೆ = CO₂ ಇದೆ — ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ!)"
        )
    },

    {
        "id": "chem_kn_q3",
        "challenge": (
            "Show the initial unreacted state of the vinegar + baking soda experiment. "
            "This represents the state BEFORE any chemical change has occurred — "
            "the starting point for comparison.\n\n"
            "(ಪ್ರತಿಕ್ರಿಯೆ ಮೊದಲಿನ ಆರಂಭಿಕ ಸ್ಥಿತಿ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the initialState. "
                "This shows baking soda in the beaker and vinegar in the bottle, unmixed — "
                "no reaction has occurred yet."
            ),
            "attempt_2": (
                "Set 'initialState=initial'. The beaker shows white baking soda powder "
                "and the green vinegar bottle is separate. Compare this to 'vinegar_reacted' "
                "to see what a chemical change looks like before and after."
            ),
            "attempt_3": (
                "Choose 'initial' to see the reactants before mixing. "
                "This is the baseline — no bubbling, no new substances yet. "
                "The chemical change only begins when the two are mixed."
            )
        },
        "concept_reminder": (
            "Before mixing, vinegar (CH₃COOH) and baking soda (NaHCO₃) are separate. "
            "No reaction occurs until they contact each other. "
            "This initial state is the reference point: compare it with 'vinegar_reacted' "
            "to observe clearly what a chemical change produces. "
            "(ಪ್ರತಿಕ್ರಿಯೆ ಮೊದಲು: ಎರಡೂ ಪದಾರ್ಥ ಪ್ರತ್ಯೇಕ — ಯಾವ ಬದಲಾವಣೆಯೂ ಇಲ್ಲ.)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — REVERSIBLE & IRREVERSIBLE CHANGES (Kannada)
# 3 questions: initial state → demonstrate reversible → demonstrate irreversible
# =============================================================================
QUIZ_QUESTIONS_KN["reversible_irreversible_kn"] = [

    {
        "id": "rev_kn_q1",
        "challenge": (
            "Start the reversible vs irreversible quiz at the beginning. "
            "Show the first question (melting ice) and identify which category it belongs to.\n\n"
            "(ಮೊದಲ ಪ್ರಶ್ನೆ ತೋರಿಸಿ — ಕರಗುವ ಐಸ್ ಯಾವ ಬದಲಾವಣೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the initialState to begin the quiz with the first question "
                "(melting ice). Ice melting is a reversible change — you can freeze water to get ice."
            ),
            "attempt_2": (
                "Set 'initialState=initial'. The first change shown is melting ice → water. "
                "This is reversible: cool the water back to 0°C and it becomes ice again."
            ),
            "attempt_3": (
                "Choose 'initial'. Melting ice is both a physical change AND reversible. "
                "The substance (H₂O) stays the same; only the state changes."
            )
        },
        "concept_reminder": (
            "Melting ice = REVERSIBLE change. Water and ice are both H₂O. "
            "Cooling water below 0°C reverses the change completely. "
            "Reversible changes are those where the original substance can be fully recovered. "
            "(ಕರಗುವ ಐಸ್ = ಹಿಮ್ಮುಖ ಬದಲಾವಣೆ — ನೀರನ್ನು ಘನೀಕರಿಸಿ ಬರ್ಫ ಮರಳಿ ಪಡೆಯಬಹುದು!)"
        )
    },

    {
        "id": "rev_kn_q2",
        "challenge": (
            "Demonstrate a REVERSIBLE change example by auto-answering the first "
            "question in the quiz. Show that melting ice is correctly identified as reversible.\n\n"
            "(ಹಿಮ್ಮುಖ ಬದಲಾವಣೆ ಉದಾಹರಣೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_reversible"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_reversible' as the initialState. "
                "The simulation auto-clicks the 'Reversible' answer for the ice melting question "
                "and shows why that is correct."
            ),
            "attempt_2": (
                "Set 'initialState=show_reversible'. Melting ice is classified correctly as "
                "reversible — the feedback explains that water can be frozen again to recover ice."
            ),
            "attempt_3": (
                "Choose 'show_reversible' to see the reversible answer confirmed with feedback. "
                "State changes (melting, boiling, freezing) are almost always reversible."
            )
        },
        "concept_reminder": (
            "Reversible changes: the original substance can be recovered. "
            "Examples: ice melting, butter melting, inflating a balloon, boiling water. "
            "Pattern: most state changes and shape stretching are reversible. "
            "Key question to ask: 'Can I get the original back?' "
            "(ಮೂಲ ವಾಪಸ್ ಪಡೆಯಬಹುದೇ? ಹೌದು → ಹಿಮ್ಮುಖ!)"
        )
    },

    {
        "id": "rev_kn_q3",
        "challenge": (
            "Demonstrate an IRREVERSIBLE change example. Jump to the burning paper "
            "question and show that burning is correctly identified as irreversible.\n\n"
            "(ಅಹಿಮ್ಮುಖ ಬದಲಾವಣೆ ಉದಾಹರಣೆ ತೋರಿಸಿ — ಕಾಗದ ಉರಿಯುವಿಕೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_irreversible"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_irreversible' as the initialState. "
                "The simulation jumps to the burning paper question and auto-answers 'Irreversible'."
            ),
            "attempt_2": (
                "Set 'initialState=show_irreversible'. Burning paper → ash is irreversible "
                "because you cannot un-burn the paper. The feedback confirms this."
            ),
            "attempt_3": (
                "Choose 'show_irreversible' to see the irreversible answer with explanation. "
                "Burning creates new substances (ash, CO₂, water vapour) that cannot "
                "be converted back to paper."
            )
        },
        "concept_reminder": (
            "Burning paper = IRREVERSIBLE chemical change: ash, CO₂, and water vapour form. "
            "You cannot turn ash back into paper. "
            "Irreversible changes: the original cannot be recovered. "
            "Examples: burning, cooking, rusting, making curd, growth of living things. "
            "(ಕಾಗದ ಬೂದಿ → ಕಾಗದ ಆಗಲು ಸಾಧ್ಯವಿಲ್ಲ — ಅಹಿಮ್ಮುಖ ಬದಲಾವಣೆ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — STATES OF MATTER (Kannada)
# 3 questions: solid state → gas state → liquid state
# =============================================================================
QUIZ_QUESTIONS_KN["states_of_matter_kn"] = [

    {
        "id": "states_kn_q1",
        "challenge": (
            "Show water in its SOLID state (ice). Set the simulation to a temperature "
            "below 0°C and observe the ice cubes in the container.\n\n"
            "(ನೀರನ್ನು ಘನ ಸ್ಥಿತಿ (ಬರ್ಫ) ಯಲ್ಲಿ ತೋರಿಸಿ — 0°C ಗಿಂತ ಕಡಿಮೆ ಉಷ್ಣತೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "solid"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'solid' as the initialState. The slider moves to -10°C showing ice "
                "cubes in the container. Below 0°C, H₂O is in solid state."
            ),
            "attempt_2": (
                "Set 'initialState=solid'. The thermometer shows -10°C and ice cubes appear. "
                "Below 0°C (freezing point), water molecules slow down and lock into ice crystals."
            ),
            "attempt_3": (
                "Choose 'solid'. The ice state shows H₂O below its freezing point (0°C). "
                "The substance is still H₂O — only the energy level is low enough to stay solid."
            )
        },
        "concept_reminder": (
            "At temperatures below 0°C, water exists as solid ice. "
            "Ice molecules are locked in a fixed crystalline structure with very low kinetic energy. "
            "0°C is the melting/freezing point — the transition temperature between solid and liquid. "
            "Ice, water, and steam are all still H₂O — just at different energy levels. "
            "(0°C ಗಿಂತ ಕಡಿಮೆ = ಘನ (ಬರ್ಫ) — H₂O ಸ್ಥಿರ ರಚನೆಯಲ್ಲಿ ಇರುತ್ತದೆ!)"
        )
    },

    {
        "id": "states_kn_q2",
        "challenge": (
            "Show water in its GAS state (steam). Set the simulation to a temperature "
            "above 100°C and observe the steam rising from the container.\n\n"
            "(ನೀರನ್ನು ಅನಿಲ ಸ್ಥಿತಿ (ಆವಿ) ಯಲ್ಲಿ ತೋರಿಸಿ — 100°C ಗಿಂತ ಹೆಚ್ಚು ಉಷ್ಣತೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "gas"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'gas' as the initialState. The slider moves to 110°C showing "
                "steam rising. Above 100°C, H₂O escapes as gas (water vapour)."
            ),
            "attempt_2": (
                "Set 'initialState=gas'. The thermometer shows 110°C and steam particles "
                "are visible rising. At 100°C (boiling point), liquid water converts to gas."
            ),
            "attempt_3": (
                "Choose 'gas'. Above 100°C, water molecules have enough energy to break "
                "free and spread out as steam. Compare with 'solid' and 'liquid' states."
            )
        },
        "concept_reminder": (
            "At temperatures above 100°C, water boils and becomes steam (gas/vapour). "
            "Gas molecules move freely in all directions with very high kinetic energy. "
            "100°C is the boiling/condensation point for water at atmospheric pressure. "
            "Steam is still H₂O — condensing steam back gives liquid water (reversible!). "
            "(100°C ಗಿಂತ ಹೆಚ್ಚು = ಆವಿ (ಅನಿಲ) — ಅಣುಗಳು ಸ್ವತಂತ್ರವಾಗಿ ಚಲಿಸುತ್ತವೆ!)"
        )
    },

    {
        "id": "states_kn_q3",
        "challenge": (
            "Show water in its LIQUID state. Set the simulation to room temperature "
            "and observe liquid water in the container — the form we use every day.\n\n"
            "(ನೀರನ್ನು ದ್ರವ ಸ್ಥಿತಿ ಯಲ್ಲಿ ತೋರಿಸಿ — 0°C ಮತ್ತು 100°C ನಡುವೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "liquid"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'liquid' as the initialState. The slider moves to 25°C (room temperature) "
                "showing liquid water — the state between 0°C and 100°C."
            ),
            "attempt_2": (
                "Set 'initialState=liquid'. Liquid water at 25°C is shown in the container. "
                "Molecules move freely but stay together — the familiar state we drink and use."
            ),
            "attempt_3": (
                "Choose 'liquid'. Between 0°C and 100°C, water is liquid. "
                "This is the biologically vital state for all life — liquid water as a solvent."
            )
        },
        "concept_reminder": (
            "Between 0°C and 100°C, water is in liquid state. "
            "Liquid molecules move freely but remain close enough to maintain a definite volume. "
            "This is the most biologically important state of water — it is a universal solvent. "
            "Comparison: solid (below 0°C) < liquid (0–100°C) < gas (above 100°C). "
            "(0°C−100°C = ದ್ರವ ನೀರು — ಅಣುಗಳು ಮುಕ್ತವಾಗಿ ಆದರೆ ಒಟ್ಟಿಗೆ ಚಲಿಸುತ್ತವೆ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — FIRE TRIANGLE (Kannada)
# 3 questions: all 3 elements present (fire) → no oxygen → no fuel
# =============================================================================
QUIZ_QUESTIONS_KN["fire_triangle_kn"] = [

    {
        "id": "fire_kn_q1",
        "challenge": (
            "Show fire BURNING by providing all three elements of the fire triangle. "
            "Demonstrate that fuel, oxygen, AND heat are all required simultaneously.\n\n"
            "(ಮೂರು ಅಂಶಗಳ ಸಮ್ಮೇಳನದಿಂದ ಅಗ್ನಿ ಉರಿಯುವಂತೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "fire"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'fire' as the initialState. All three buttons (fuel, oxygen, heat) "
                "will be auto-clicked and fire will appear when all three are present."
            ),
            "attempt_2": (
                "Set 'initialState=fire'. The simulation activates fuel + oxygen + heat "
                "and shows a burning flame. All three conditions of the fire triangle are met."
            ),
            "attempt_3": (
                "Choose 'fire'. The flame animation shows combustion in action — "
                "fuel providing material, oxygen supporting burning, heat providing ignition energy."
            )
        },
        "concept_reminder": (
            "Fire Triangle: FUEL + OXYGEN + HEAT = FIRE. "
            "All three must be present simultaneously for combustion to occur. "
            "This is why fire cannot burn in a vacuum (no oxygen) or with wet fuel "
            "(water absorbs heat, lowering temperature below ignition point). "
            "(ಇಂಧನ + ಆಮ್ಲಜನಕ + ಉಷ್ಣ = ಅಗ್ನಿ — ಮೂರೂ ಇಲ್ಲದೆ ಅಗ್ನಿ ಸಾಧ್ಯವಿಲ್ಲ!)"
        )
    },

    {
        "id": "fire_kn_q2",
        "challenge": (
            "Show what happens when OXYGEN is removed from the fire. Demonstrate "
            "how removing oxygen extinguishes the fire even when fuel and heat are present.\n\n"
            "(ಆಮ್ಲಜನಕ ತೆಗೆದಾಗ ಅಗ್ನಿ ಆರುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "no_oxygen"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'no_oxygen' as the initialState. Fuel and heat are present but "
                "oxygen is missing — fire does not burn. This simulates smothering a fire."
            ),
            "attempt_2": (
                "Set 'initialState=no_oxygen'. Without oxygen, combustion cannot proceed. "
                "The simulation shows fire is impossible even with fuel and heat present."
            ),
            "attempt_3": (
                "Choose 'no_oxygen' to see: fuel ✅ + heat ✅ + oxygen ❌ = NO FIRE. "
                "This is the principle behind smothering fires with blankets or CO₂ extinguishers."
            )
        },
        "concept_reminder": (
            "Removing oxygen extinguishes fire. This is the principle of SMOTHERING. "
            "Methods: blanket over a small fire, CO₂ fire extinguisher (displaces oxygen), "
            "fire-proof cover, foam extinguisher (seals oxygen supply). "
            "Oxygen is essential because combustion is oxidation — O₂ reacts with fuel molecules. "
            "(ಆಮ್ಲಜನಕ ತೆಗೆ = ಅಗ್ನಿ ಆರಿ — ಹೊದಿಕೆ ಮುಚ್ಚಿ ಅಥವಾ CO₂ ಮೂಲಕ!)"
        )
    },

    {
        "id": "fire_kn_q3",
        "challenge": (
            "Show what happens when FUEL is removed. Demonstrate how removing the "
            "combustible material stops the fire even when oxygen and heat are present.\n\n"
            "(ಇಂಧನ ತೆಗೆದಾಗ ಅಗ್ನಿ ಆರುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "no_fuel"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'no_fuel' as the initialState. Oxygen and heat are present but "
                "no fuel means nothing to burn — fire cannot start."
            ),
            "attempt_2": (
                "Set 'initialState=no_fuel'. Without combustible material, there is nothing "
                "for oxygen to react with. No fuel = no fire, even with oxygen and heat."
            ),
            "attempt_3": (
                "Choose 'no_fuel'. Oxygen ✅ + heat ✅ + fuel ❌ = NO FIRE. "
                "This is why firebreaks (cleared strips of land) stop forest fires from spreading."
            )
        },
        "concept_reminder": (
            "Removing fuel extinguishes fire. This is the principle of STARVATION. "
            "Methods: firebreaks in forest fires (remove trees in a strip), "
            "turning off a gas valve (removes gas fuel), letting a candle burn out (fuel consumed). "
            "Without fuel, there is no material for the combustion reaction to proceed. "
            "(ಇಂಧನ ತೆಗೆ = ಅಗ್ನಿ ಆರಿ — ಉರಿಯಲು ಏನೂ ಇಲ್ಲ!)"
        )
    }
]


# =============================================================================
# OXYGEN AND COMBUSTION SIMULATION
# ಉರಿಯಲು ಆಮ್ಲಜನಕ ಅಗತ್ಯ – ಮೇಣ ಮತ್ತು ಜಾರ್ ಪ್ರಯೋಗ
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["oxygen_combustion_kn"] = {
    "title": "ಉರಿಯಲು ಆಮ್ಲಜನಕ ಅಗತ್ಯ (Oxygen Required for Combustion)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation6_oxygen_combustion_kn.html",
    "description": (
        "Kannada candle-and-glass-jar experiment simulation demonstrating that oxygen "
        "is essential for combustion. Students light a candle, then cover it with a "
        "glass jar — the trapped oxygen is consumed, CO₂ and water vapour are produced, "
        "and the flame automatically extinguishes when oxygen runs out. "
        "A timer tracks the seconds, oxygen indicators fade as they are consumed, "
        "and CO₂ indicators appear. "
        "This is a classic school experiment proving the role of oxygen in sustaining fire."
    ),
    "cannot_demonstrate": [
        "Quantitative measurement of oxygen consumed",
        "Effect of different jar sizes on burn duration",
        "Incomplete combustion producing carbon monoxide",
        "The precise chemical equation for wax combustion"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Experiment State",
            "range": "initial, lit, covered_extinguished",
            "url_key": "initialState",
            "effect": (
                "Controls which stage of the candle-jar experiment is shown:\n"
                "  'initial'              → candle unlit, jar not present (default start)\n"
                "  'lit'                  → candle is burning, O₂ indicators visible\n"
                "  'covered_extinguished' → jar covers candle, oxygen depletes, flame extinguishes"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, learning panel, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Oxygen Is Essential for Combustion",
            "description": (
                "Combustion (burning) requires oxygen to proceed. When the supply of "
                "oxygen is cut off — by covering the flame — the fire extinguishes "
                "because combustion cannot continue without oxygen."
            ),
            "key_insight": (
                "The glass jar traps a fixed amount of oxygen. As the candle burns, "
                "oxygen (O₂) is consumed and replaced by CO₂. When O₂ runs out, "
                "the flame dies — proving oxygen is a non-negotiable requirement for fire."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Combustion Produces CO₂ and Water Vapour",
            "description": (
                "Candle wax (a hydrocarbon) reacts with oxygen to produce carbon dioxide "
                "and water vapour. These new substances are the products of the "
                "chemical change of combustion."
            ),
            "key_insight": (
                "Wax + O₂ → CO₂ + H₂O. This is why a glass jar placed over a burning "
                "candle fogs up (water vapour condenses on the cool glass) and CO₂ "
                "accumulates inside, displacing oxygen."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Smothering — Removing Oxygen to Extinguish Fire",
            "description": (
                "One of the three fire-extinguishing methods is smothering: cutting off "
                "the oxygen supply. Covering the candle with a jar demonstrates this "
                "principle directly."
            ),
            "key_insight": (
                "Fire can be extinguished by removing fuel, removing oxygen, or cooling. "
                "The jar experiment removes oxygen — the same principle used by blanket "
                "smothering and CO₂ fire extinguishers."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# CANDLE BURNING — PHYSICAL AND CHEMICAL CHANGES SIMULATION
# ಮೇಣ ಉರಿಯುವಿಕೆ – ಭೌತಿಕ ಮತ್ತು ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["candle_burning_kn"] = {
    "title": "ಮೇಣ ಉರಿಯುವಿಕೆ – ಭೌತಿಕ ಮತ್ತು ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ (Candle Burning)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation7_candle_burning_kn.html",
    "description": (
        "Kannada two-tab simulation showing that a burning candle involves BOTH a "
        "physical change AND a chemical change simultaneously. "
        "Physical tab: wax melts (solid → liquid) — same substance, reversible, no new material. "
        "Chemical tab: wax vapour burns with oxygen → CO₂ + H₂O — new substances, irreversible. "
        "Students toggle between the two views with a colour-coded before/after comparison "
        "and an explanation box that updates for each type of change."
    ),
    "cannot_demonstrate": [
        "The balanced chemical equation for wax combustion",
        "Intermediate partial combustion states",
        "Quantitative measurements of reactants and products",
        "Other real-world examples of dual physical-chemical changes"
    ],
    "initial_params": {"initialState": "physical", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Change Type View",
            "range": "physical, chemical",
            "url_key": "initialState",
            "effect": (
                "Controls which change-type tab is shown:\n"
                "  'physical'  → wax melting view (solid → liquid, same substance, reversible)\n"
                "  'chemical'  → wax burning view (wax + O₂ → CO₂ + H₂O, new substances, irreversible)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and explanation box."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Wax Melting Is a Physical Change",
            "description": (
                "When a candle is lit, the solid wax near the wick melts into liquid wax — "
                "a state change. The wax molecules remain the same; only the state changes. "
                "Solidifying the liquid wax restores the original solid."
            ),
            "key_insight": (
                "Wax melting is physical: same substance (wax), different state (solid → liquid). "
                "It is reversible — cooling solidifies the wax again. "
                "No new substance is formed in the melting zone."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Wax Burning Is a Chemical Change",
            "description": (
                "The liquid wax vaporises and the wax vapour reacts with oxygen in a "
                "combustion reaction, producing carbon dioxide and water vapour — "
                "entirely new substances. This is irreversible."
            ),
            "key_insight": (
                "Wax vapour + O₂ → CO₂ + H₂O. New substances form, energy (heat and light) "
                "is released, and the wax is permanently consumed. "
                "This cannot be reversed — you cannot convert CO₂ and water back to wax candle."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "One Candle — Two Changes Happening Together",
            "description": (
                "A burning candle is a real-world example where physical and chemical "
                "changes occur simultaneously in the same object — wax melts (physical) "
                "and wax vapour burns (chemical)."
            ),
            "key_insight": (
                "Key distinction: the melting wax → physical (reversible, same substance). "
                "The burning flame zone → chemical (irreversible, new substances). "
                "This dual-change phenomenon shows that a single event can contain "
                "both types of change at once."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# COMBUSTION EXAMPLES SIMULATION
# ವಿವಿಧ ಪದಾರ್ಥಗಳ ದಹನ – ಜ್ವಾಲೆಯ ಬಣ್ಣ ಮತ್ತು ಉತ್ಪನ್ನಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["combustion_examples_kn"] = {
    "title": "ವಿವಿಧ ಪದಾರ್ಥಗಳ ದಹನ (Combustion Examples)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation8_combustion_examples_kn.html",
    "description": (
        "Kannada combustion laboratory simulation where students select from six "
        "materials (magnesium, paper, wood, charcoal, sulfur, match) and observe "
        "each material burning on a lab burner. Each combustion experiment shows: "
        "the characteristic flame colour (white for Mg, yellow for paper/wood, "
        "blue for sulfur, red glow for charcoal), the chemical equation, and "
        "the products formed. Students learn that all combustion requires oxygen "
        "and produces oxides, but each material has unique properties."
    ),
    "cannot_demonstrate": [
        "Incomplete combustion producing carbon monoxide",
        "Effect of temperature and surface area on combustion rate",
        "Combustion in pure oxygen vs. air",
        "Extinguishing fires caused by different materials"
    ],
    "initial_params": {"initialState": "magnesium", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Material to Burn",
            "range": "initial, magnesium, paper, wood, charcoal, sulfur, match",
            "url_key": "initialState",
            "effect": (
                "Selects a material and auto-burns it showing the flame and products:\n"
                "  'initial'   → no material selected (default empty state)\n"
                "  'magnesium' → bright white flame, MgO (white ash): 2Mg + O₂ → 2MgO\n"
                "  'paper'     → yellow flame, CO₂ + H₂O + grey ash\n"
                "  'wood'      → orange-yellow flame, CO₂ + H₂O + smoke + ash\n"
                "  'charcoal'  → glowing red (no visible flame), CO₂: C + O₂ → CO₂\n"
                "  'sulfur'    → blue flame, SO₂ (pungent): S + O₂ → SO₂\n"
                "  'match'     → two-stage: head burns then wood ignites"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, learning panel, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Different Materials Produce Different Flame Colours",
            "description": (
                "Each combustible material burns with a characteristic flame colour "
                "that depends on the chemical elements present: magnesium → brilliant "
                "white, sulfur → blue, hydrocarbons (wood, paper) → yellow/orange, "
                "charcoal → red glow without visible flame."
            ),
            "key_insight": (
                "Flame colour is a diagnostic property of what is burning. "
                "Pyrotechnicians use this principle — magnesium for white light, "
                "sulfur for blue, potassium for violet. "
                "Charcoal's lack of visible flame shows glowing combustion differs from flaming combustion."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "All Combustion Requires Oxygen and Produces Oxides",
            "description": (
                "Despite looking different, all combustion reactions follow the same "
                "pattern: fuel + O₂ → oxide products + heat + light. "
                "Carbon → CO₂, hydrogen → H₂O, magnesium → MgO, sulfur → SO₂."
            ),
            "key_insight": (
                "The common thread: oxygen is the reactant in all cases and the "
                "products are always oxides of the elements in the fuel. "
                "This is why combustion is categorised as oxidation."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Combustion Is an Irreversible Chemical Change",
            "description": (
                "All combustion reactions produce new substances (oxides) that cannot "
                "be converted back to the original fuel. They are irreversible chemical "
                "changes releasing energy as heat and light."
            ),
            "key_insight": (
                "You cannot un-burn wood back into a log, un-burn magnesium back into "
                "a shiny ribbon, or un-burn sulfur from SO₂. The irreversible production "
                "of oxide products is the defining characteristic of combustion as a "
                "chemical change."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# DESIRABLE AND UNDESIRABLE CHANGES SIMULATION
# ಅಪೇಕ್ಷಣೀಯ ಮತ್ತು ಅನಪೇಕ್ಷಿತ ಬದಲಾವಣೆಗಳು
# Science Chapter 5 – Changes Around Us
# =============================================================================
SIMULATIONS_KN["desirable_undesirable_kn"] = {
    "title": "ಅಪೇಕ್ಷಣೀಯ ಮತ್ತು ಅನಪೇಕ್ಷಿತ ಬದಲಾವಣೆಗಳು (Desirable & Undesirable Changes)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter5_simulation9_desirable_undesirable_kn.html",
    "description": (
        "Kannada quiz simulation where students classify 10 real-world changes as "
        "desirable (beneficial/wanted) or undesirable (harmful/unwanted). "
        "Changes include: milk curdling (desirable), iron rusting (undesirable), "
        "cooking food (desirable), fruit rotting (undesirable), seed germination "
        "(desirable), air pollution (undesirable), composting (desirable), "
        "tooth decay (undesirable), bread making (desirable), and global warming (undesirable). "
        "Each answer gives detailed feedback explaining the reasoning. "
        "Students learn that the desirability of a change depends on its usefulness "
        "or harmfulness to humans and the environment."
    ),
    "cannot_demonstrate": [
        "Preventing undesirable changes (only classification shown)",
        "Partial desirability (e.g. fruit rotting is undesirable for us but useful for ecosystems)",
        "Changes that are desirable in one context but undesirable in another"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Quiz State",
            "range": "initial, show_desirable, show_undesirable",
            "url_key": "initialState",
            "effect": (
                "Controls which quiz state to demonstrate:\n"
                "  'initial'          → first question shown (milk curdling), no answer selected\n"
                "  'show_desirable'   → auto-answers first question (curdling) as desirable\n"
                "  'show_undesirable' → auto-answers first question (curdling) as undesirable"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and takeaway panels."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Desirable Changes Benefit Humans or the Environment",
            "description": (
                "A change is desirable when it produces a useful or beneficial outcome: "
                "cooking food makes it safe and nutritious; milk curdling gives us yoghurt; "
                "seed germination grows crops; composting recycles nutrients."
            ),
            "key_insight": (
                "The question to ask: 'Does this change help us or harm us?' "
                "Desirable changes are those we intentionally bring about or want to happen. "
                "Cooking, fermentation, germination — all are deliberately induced beneficial changes."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Undesirable Changes Are Harmful or Wasteful",
            "description": (
                "A change is undesirable when it causes damage, loss, or harm: rusting weakens "
                "structures, tooth decay causes pain, air pollution harms health, "
                "global warming threatens ecosystems."
            ),
            "key_insight": (
                "Undesirable changes are those we try to prevent or minimise. "
                "Iron is painted to prevent rusting; food is refrigerated to slow spoilage; "
                "emissions are regulated to reduce air pollution. Prevention is the response to undesirability."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "The Same Type of Change Can Be Desirable or Undesirable",
            "description": (
                "Biological decomposition (rotting/decay) is: desirable when composting "
                "kitchen waste → soil nutrients, but undesirable when it means "
                "fruit spoiling and going to waste. Context determines desirability."
            ),
            "key_insight": (
                "Desirability is not a property of the change itself, but of its context and impact. "
                "Fungal decomposition in compost = desirable. Same process on food = undesirable. "
                "This teaches students to evaluate changes critically rather than categorise them "
                "by type alone."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# SAY NO TO HARMFUL SUBSTANCES SIMULATION
# ಹಾನಿಕರ ವಸ್ತುಗಳಿಗೆ 'ಇಲ್ಲ' ಹೇಳಿ – ಸನ್ನಿವೇಶ ಆಧಾರಿತ ತರಬೇತಿ
# Science Chapter 6 – Knowing About Tobacco, Alcohol and Drugs
# =============================================================================
SIMULATIONS_KN["say_no_kn"] = {
    "title": "ಹಾನಿಕರ ವಸ್ತುಗಳಿಗೆ 'ಇಲ್ಲ' ಹೇಳಿ (Say No to Harmful Substances)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation10_say_no_kn.html",
    "description": (
        "Kannada scenario-based simulation (Chapter 6) where students practice "
        "saying NO to harmful substances — tobacco (cigarettes), alcohol, vaping, "
        "pills, and family social pressure. "
        "For each scenario involving peer pressure or temptation, students choose "
        "between accepting (wrong) or refusing (correct). The simulation provides "
        "immediate feedback: saying NO gives positive reinforcement explaining health "
        "reasons; saying YES shows the consequences and guides students to the correct choice. "
        "A national helpline number (14446) is displayed for real-world support. "
        "5 scenarios cover peer pressure, curiosity, online influence, exam stress, "
        "and family situations."
    ),
    "cannot_demonstrate": [
        "Physical health effects of tobacco/alcohol on body organs",
        "Chemical composition of addictive substances",
        "Long-term addiction progression",
        "Legal consequences of substance use"
    ],
    "initial_params": {"initialState": "initial", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Scenario State",
            "range": "initial, show_no, show_yes",
            "url_key": "initialState",
            "effect": (
                "Controls which response is demonstrated in the first scenario:\n"
                "  'initial'  → first scenario shown (cigarette peer pressure), no answer yet\n"
                "  'show_no'  → auto-selects 'NO' for scenario 1, showing the correct response\n"
                "  'show_yes' → auto-selects 'YES' for scenario 1, showing the wrong-choice feedback"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and takeaway (refusal strategies) panel."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Peer Pressure and Harmful Substances",
            "description": (
                "Adolescents often face peer pressure to try tobacco, alcohol, or other "
                "harmful substances. Recognising these situations and having strategies "
                "to refuse is a critical life skill for health and safety."
            ),
            "key_insight": (
                "Peer pressure scenarios include: 'everyone's doing it', 'it'll make you cool', "
                "'just try it once'. None of these are valid reasons to risk one's health. "
                "True friends respect a NO; those who don't aren't real friends."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Health Consequences of Tobacco, Alcohol and Drugs",
            "description": (
                "Tobacco contains nicotine (highly addictive), alcohol affects the developing "
                "adolescent brain, vapes contain harmful chemicals, and unprescribed pills "
                "can be addictive or fatal. All are dangerous, particularly for adolescents "
                "whose bodies and brains are still developing."
            ),
            "key_insight": (
                "The adolescent brain is more vulnerable to addiction than an adult brain. "
                "One cigarette can start nicotine dependency. Alcohol impairs judgment and "
                "brain development. Each substance has specific biological harms, "
                "making early refusal critically important."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Strategies to Refuse Harmful Substances",
            "description": (
                "Students learn practical refusal strategies: 'No thank you, I'm fine', "
                "leaving the situation, citing parents or values, offering an alternative "
                "activity, or just walking away without explanation."
            ),
            "key_insight": (
                "Saying NO is a strength, not a weakness. Having a prepared response reduces "
                "hesitation in a real pressure situation. The national helpline 14446 is "
                "toll-free and available 24/7 for anyone needing support with substance issues."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# QUIZ QUESTIONS — OXYGEN AND COMBUSTION (Kannada)
# 3 questions: show lit candle → show extinguished → explain baseline
# =============================================================================
QUIZ_QUESTIONS_KN["oxygen_combustion_kn"] = [

    {
        "id": "o2_kn_q1",
        "challenge": (
            "Show the candle burning. Light the candle to demonstrate that a flame "
            "is sustained when oxygen is freely available.\n\n"
            "(ಮೇಣ ಉರಿಯುತ್ತಿದೆ ಎಂದು ತೋರಿಸಿ — ಆಮ್ಲಜನಕ ಲಭ್ಯವಿರುವಾಗ ಜ್ವಾಲೆ ಇರುತ್ತದೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "lit"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'lit' as the initialState. "
                "The simulation lights the candle — the flame burns freely with open air "
                "providing unlimited oxygen."
            ),
            "attempt_2": (
                "Set 'initialState=lit'. The lit candle shows O₂ indicators around the flame. "
                "Oxygen is freely available → combustion continues → flame stays lit."
            ),
            "attempt_3": (
                "Choose 'lit'. The burning flame is the baseline: open air = oxygen available = "
                "fire sustained. Compare this with 'covered_extinguished' to see the difference."
            )
        },
        "concept_reminder": (
            "A candle burns freely in open air because oxygen (O₂) from the atmosphere "
            "continuously reaches the flame. Combustion: wax + O₂ → CO₂ + H₂O + heat + light. "
            "As long as O₂ is available and fuel (wax) remains, the flame continues. "
            "(ಆಮ್ಲಜನಕ + ಇಂಧನ = ಜ್ವಾಲೆ ಮುಂದುವರಿಯುತ್ತದೆ!)"
        )
    },

    {
        "id": "o2_kn_q2",
        "challenge": (
            "Cover the candle with the glass jar and show that the flame extinguishes "
            "when oxygen runs out. This proves that oxygen is essential for combustion.\n\n"
            "(ಜಾರ್‌ನಿಂದ ಮುಚ್ಚಿ ಆಮ್ಲಜನಕ ಮುಗಿದಾಗ ಜ್ವಾಲೆ ಆರುವುದನ್ನು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "covered_extinguished"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'covered_extinguished' as the initialState. "
                "The simulation lights the candle then covers it — watch the oxygen deplete and "
                "the flame extinguish."
            ),
            "attempt_2": (
                "Set 'initialState=covered_extinguished'. The jar traps a fixed oxygen supply. "
                "As wax burns, O₂ is consumed. When O₂ runs out → flame extinguishes. "
                "CO₂ indicators appear showing what was produced."
            ),
            "attempt_3": (
                "Choose 'covered_extinguished'. The timer shows how long the flame lasts "
                "with limited oxygen. Extinguishing proves: no oxygen = no combustion. "
                "This is the scientific proof that oxygen is an essential requirement for fire."
            )
        },
        "concept_reminder": (
            "When enclosed in a jar, the candle consumes all available oxygen (O₂) "
            "and produces CO₂ + H₂O. When O₂ is exhausted, combustion stops and the flame "
            "extinguishes — not because of lack of fuel (wax remains) but lack of oxygen. "
            "This classically proves O₂ is essential for burning. "
            "(ಆಮ್ಲಜನಕ ಮುಗಿದರೆ — ಜ್ವಾಲೆ ಆರಿಹೋಗುತ್ತದೆ!)"
        )
    },

    {
        "id": "o2_kn_q3",
        "challenge": (
            "Show the initial state of the experiment — candle unlit, jar absent. "
            "This is the baseline before any combustion occurs.\n\n"
            "(ಪ್ರಯೋಗ ಪ್ರಾರಂಭ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಉರಿಯದ ಮೇಣ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the initialState. "
                "The candle is unlit and no jar is present — the starting point before the experiment."
            ),
            "attempt_2": (
                "Set 'initialState=initial'. The unlit candle shows the setup before any reaction. "
                "Oxygen is present, fuel (wax) is present, but no heat/ignition → no combustion."
            ),
            "attempt_3": (
                "Choose 'initial' to show the candle before lighting. "
                "This reinforces the fire triangle: fuel (wax ✓) + oxygen (air ✓) + heat (✗) = "
                "no fire yet. All three elements of the fire triangle must be present."
            )
        },
        "concept_reminder": (
            "Before lighting, the candle has fuel (wax) and oxygen (air) but no ignition heat. "
            "This shows the fire triangle requirement: fuel + oxygen + ignition temperature = fire. "
            "Wax and air alone do not spontaneously combust — heat is the trigger. "
            "(ಇಂಧನ + ಆಮ್ಲಜನಕ ಆದರೆ ಉಷ್ಣ ಇಲ್ಲ → ಅಗ್ನಿ ಇಲ್ಲ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — CANDLE BURNING — PHYSICAL VS CHEMICAL CHANGE (Kannada)
# 3 questions: physical change → chemical change → distinguish both
# =============================================================================
QUIZ_QUESTIONS_KN["candle_burning_kn"] = [

    {
        "id": "candle_kn_q1",
        "challenge": (
            "Show the PHYSICAL change in a burning candle. "
            "Demonstrate that wax melting is a physical change — same substance, "
            "different state, reversible.\n\n"
            "(ಮೇಣ ಕರಗುವಿಕೆ ಭೌತಿಕ ಬದಲಾವಣೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "physical"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'physical' as the initialState. "
                "The simulation shows the wax melting zone — solid wax → liquid wax. "
                "The substance (wax) is the same; only the state changes."
            ),
            "attempt_2": (
                "Set 'initialState=physical'. The physical-change tab shows: solid wax melts to "
                "liquid near the wick. This is reversible — cool the liquid wax and it solidifies again."
            ),
            "attempt_3": (
                "Choose 'physical'. Wax melting: same substance (wax), different state (solid → liquid), "
                "reversible. No new substance forms. The substance identity is preserved."
            )
        },
        "concept_reminder": (
            "Wax melting = PHYSICAL change: the wax changes from solid to liquid but is still wax. "
            "The chemical composition of wax does not change. "
            "It is reversible — liquid wax solidifies when cooled. "
            "No new substance is formed in the melting zone. "
            "(ಮೇಣ ಕರಗುವಿಕೆ = ಭೌತಿಕ — ಪದಾರ್ಥ ಅದೇ!)"
        )
    },

    {
        "id": "candle_kn_q2",
        "challenge": (
            "Show the CHEMICAL change in a burning candle. "
            "Demonstrate that wax vapour burning with oxygen is a chemical change — "
            "new substances CO₂ and H₂O are formed.\n\n"
            "(ಮೇಣ ಉರಿಯುವಿಕೆ ರಾಸಾಯನಿಕ ಬದಲಾವಣೆ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "chemical"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'chemical' as the initialState. "
                "The simulation shows the combustion zone — wax vapour + O₂ → CO₂ + H₂O. "
                "New substances form, making this a chemical change."
            ),
            "attempt_2": (
                "Set 'initialState=chemical'. The chemical tab shows wax vapour reacting with oxygen. "
                "Products: CO₂ and H₂O — completely different molecules from wax. Irreversible."
            ),
            "attempt_3": (
                "Choose 'chemical'. The before/after comparison shows: wax + O₂ (before) → "
                "CO₂ + H₂O (after). Different substances = chemical change. "
                "You cannot convert CO₂ and H₂O back into wax."
            )
        },
        "concept_reminder": (
            "Wax burning = CHEMICAL change: wax vapour + O₂ → CO₂ + H₂O + heat + light. "
            "New substances (carbon dioxide and water) form — completely different from wax. "
            "It is irreversible — the wax molecules are permanently destroyed. "
            "The yellow flame is visible because of incandescent carbon particles. "
            "(ಮೇಣ ಉರಿಯುವಿಕೆ = ರಾಸಾಯನಿಕ — ಹೊಸ ಪದಾರ್ಥ CO₂ ಮತ್ತು H₂O!)"
        )
    },

    {
        "id": "candle_kn_q3",
        "challenge": (
            "Go back to the physical change view. Explain why a single burning candle "
            "demonstrates BOTH a physical change AND a chemical change at the same time.\n\n"
            "(ಮೇಣ ಕರಗುವಿಕೆಗೆ ಮರಳಿ — ಒಂದು ಮೇಣ ಎರಡೂ ಬದಲಾವಣೆ ಹೇಗೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "physical"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'physical' as the initialState. "
                "The physical tab reminds us: wax melts (physical) — then the liquid wax "
                "vaporises and the vapour burns (chemical). Same candle, two zones."
            ),
            "attempt_2": (
                "Set 'initialState=physical'. Melting zone: solid → liquid (physical, reversible). "
                "Flame zone: vapour + O₂ → CO₂ + H₂O (chemical, irreversible). "
                "Both happen simultaneously in a burning candle."
            ),
            "attempt_3": (
                "Choose 'physical'. The candle simultaneously: melts wax (physical change) in "
                "the lower zone AND burns wax vapour (chemical change) in the flame zone. "
                "This is why a burning candle is THE classic dual-change example."
            )
        },
        "concept_reminder": (
            "A burning candle = BOTH changes at once. "
            "Zone 1 (near wick): solid wax → liquid wax (PHYSICAL — same substance, reversible). "
            "Zone 2 (flame): liquid wax → vapour → CO₂ + H₂O (CHEMICAL — new substances, irreversible). "
            "This dual-change phenomenon is unique and commonly tested in exams. "
            "(ಒಂದು ಮೇಣ = ಭೌತಿಕ + ರಾಸಾಯನಿಕ ಬದಲಾವಣೆಗಳು ಒಟ್ಟಿಗೆ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — COMBUSTION EXAMPLES (Kannada)
# 3 questions: magnesium (distinctive flame) → charcoal (no visible flame) → initial
# =============================================================================
QUIZ_QUESTIONS_KN["combustion_examples_kn"] = [

    {
        "id": "comb_kn_q1",
        "challenge": (
            "Burn MAGNESIUM and observe its characteristic flame. Show why magnesium "
            "produces such a distinctive bright white flame when burned.\n\n"
            "(ಮೆಗ್ನೀಸಿಯಂ ಸುಡಿ — ಪ್ರಕಾಶಮಾನ ಬಿಳಿ ಜ್ವಾಲೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "magnesium"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'magnesium' as the initialState. "
                "The simulation shows magnesium ribbon burning with a brilliant white flame "
                "and forming white MgO powder."
            ),
            "attempt_2": (
                "Set 'initialState=magnesium'. The equation shown is: 2Mg + O₂ → 2MgO. "
                "The product is magnesium oxide (white ash). "
                "Magnesium's intense white light is used in fireworks and photography flash."
            ),
            "attempt_3": (
                "Choose 'magnesium'. The bright white flame is unique — do not look directly at it! "
                "Magnesium burns at very high temperature, which is why it produces such brilliant light. "
                "Product: white powdery ash (MgO)."
            )
        },
        "concept_reminder": (
            "Magnesium combustion: 2Mg + O₂ → 2MgO. "
            "Magnesium burns with an intensely bright white flame due to the high temperature reached. "
            "The product is magnesium oxide (white powder). "
            "Real-world use: fireworks (white light), old-style photography flash bulbs. "
            "Do not look directly at burning magnesium — it can damage your eyes! "
            "(2Mg + O₂ → 2MgO + ಪ್ರಕಾಶಮಾನ ಬಿಳಿ ಬೆಳಕು!)"
        )
    },

    {
        "id": "comb_kn_q2",
        "challenge": (
            "Burn CHARCOAL and observe that it glows red without a visible flame. "
            "Explain why charcoal burns differently from wood or paper.\n\n"
            "(ಇದ್ದಲು ಸುಡಿ — ಗೋಚರ ಜ್ವಾಲೆ ಇಲ್ಲ, ಕೆಂಪು ಜ್ವಳಿಕೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "charcoal"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'charcoal' as the initialState. "
                "The simulation shows charcoal glowing red without a visible flame — "
                "this is called glowing combustion (vs flaming combustion)."
            ),
            "attempt_2": (
                "Set 'initialState=charcoal'. Charcoal is nearly pure carbon (C). "
                "Equation: C + O₂ → CO₂. It burns hotter than wood but without a visible flame. "
                "The red glow is incandescence of hot carbon."
            ),
            "attempt_3": (
                "Choose 'charcoal'. Charcoal has no volatile compounds that produce a visible flame. "
                "It undergoes surface combustion — glowing red. "
                "This makes it ideal for cooking (uniform heat without flames)"
            )
        },
        "concept_reminder": (
            "Charcoal combustion: C + O₂ → CO₂. "
            "Charcoal is nearly pure carbon. Unlike wood, it has no hydrogen or volatile compounds "
            "to produce a visible flame — instead it glows red (surface combustion). "
            "It burns hotter and more uniformly than wood, making it ideal for cooking and barbecue. "
            "(ಇದ್ದಲು = ಶುದ್ಧ ಕಾರ್ಬನ್ — ಗೋಚರ ಜ್ವಾಲೆ ಇಲ್ಲ, ಆದರೆ ಅತಿ ಬಿಸಿ!)"
        )
    },

    {
        "id": "comb_kn_q3",
        "challenge": (
            "Burn SULFUR and observe its distinctive blue flame and pungent SO₂ gas. "
            "Show this unusual combustion reaction that produces a toxic oxide.\n\n"
            "(ಸಲ್ಫರ್ ಸುಡಿ — ನೀಲಿ ಜ್ವಾಲೆ ಮತ್ತು SO₂ ಅನಿಲ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "sulfur"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'sulfur' as the initialState. "
                "The simulation shows sulfur burning with a distinctive blue flame "
                "and producing SO₂ (sulfur dioxide) — a pungent, choking gas."
            ),
            "attempt_2": (
                "Set 'initialState=sulfur'. Equation: S + O₂ → SO₂. "
                "Sulfur dioxide is acidic and toxic. The blue flame is unique to sulfur "
                "and metal compounds."
            ),
            "attempt_3": (
                "Choose 'sulfur'. The blue flame is a diagnostic property of sulfur combustion. "
                "SO₂ formed is the cause of acid rain when sulfur-containing fuels (coal, oil) "
                "are burned in power plants."
            )
        },
        "concept_reminder": (
            "Sulfur combustion: S + O₂ → SO₂. "
            "Sulfur burns with a unique blue flame. The product SO₂ (sulfur dioxide) is acidic, "
            "pungent (rotten egg smell), and toxic. "
            "Real-world impact: burning of sulfur-containing coal and oil in power plants produces "
            "SO₂ which causes acid rain — an environmental problem. "
            "Always burn sulfur in a well-ventilated area or fume cupboard! "
            "(S + O₂ → SO₂ — ನೀಲಿ ಜ್ವಾಲೆ, ಆಮ್ಲ ಮಳೆ ಕಾರಣ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — DESIRABLE AND UNDESIRABLE CHANGES (Kannada)
# 3 questions: initial → demonstrate desirable → demonstrate undesirable
# =============================================================================
QUIZ_QUESTIONS_KN["desirable_undesirable_kn"] = [

    {
        "id": "desir_kn_q1",
        "challenge": (
            "Start the quiz at the beginning. Show the first question (milk curdling) "
            "and identify whether it is a desirable or undesirable change.\n\n"
            "(ಮೊದಲ ಪ್ರಶ್ನೆ ತೋರಿಸಿ — ಹಾಲಿನಿಂದ ಮೊಸರು ಅಪೇಕ್ಷಣೀಯವೇ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the initialState to show the first question (milk curdling). "
                "Think: is making curd from milk beneficial or harmful?"
            ),
            "attempt_2": (
                "Set 'initialState=initial'. The first question is milk curdling. "
                "Bacteria convert milk to curd — a useful food product. "
                "Is this change something we want (desirable) or something we want to prevent?"
            ),
            "attempt_3": (
                "Choose 'initial'. Milk → curd via bacterial fermentation: "
                "this produces nutritious food (yoghurt, lassi) — a deliberately induced, "
                "beneficial change that humans have used for thousands of years."
            )
        },
        "concept_reminder": (
            "Desirable changes are those that produce beneficial outcomes. "
            "Milk curdling by bacteria is desirable: it produces yoghurt and curd — "
            "nutritious, probiotic food enjoyed worldwide. "
            "It is an irreversible chemical change but a WANTED one. "
            "(ಅಪೇಕ್ಷಣೀಯ = ಲಾಭಕರ ಬದಲಾವಣೆ — ಮೊಸರು ಉಪಯುಕ್ತ!)"
        )
    },

    {
        "id": "desir_kn_q2",
        "challenge": (
            "Demonstrate a DESIRABLE change by auto-answering the first quiz question "
            "correctly as desirable. Show the feedback explaining why milk curdling "
            "is beneficial.\n\n"
            "(ಅಪೇಕ್ಷಣೀಯ ಉತ್ತರ ತೋರಿಸಿ — ಮೊಸರು ಉಪಯೋಗಿ!)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_desirable"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_desirable' as the initialState. "
                "The simulation auto-clicks the desirable button and shows positive feedback "
                "for milk curdling."
            ),
            "attempt_2": (
                "Set 'initialState=show_desirable'. The feedback confirms milk curdling is desirable: "
                "it produces nutritious curd used in yoghurt, lassi, and other dairy products "
                "— a beneficial use of bacterial fermentation."
            ),
            "attempt_3": (
                "Choose 'show_desirable'. The correct answer with feedback: curdling is a "
                "desirable chemical change that humans have used intentionally for thousands of "
                "years to preserve milk and create food products."
            )
        },
        "concept_reminder": (
            "Desirable chemical changes are those humans intentionally bring about for benefit. "
            "Examples: cooking food, curdling milk, composting waste, fermenting bread, germinating seeds. "
            "The key question: 'Is this change something we WANT to happen?' "
            "Desirable ≠ reversible. Many desirable changes are irreversible (cooking, curdling). "
            "(ಅಪೇಕ್ಷಣೀಯ = ನಾವು ಬಯಸುವ ಬದಲಾವಣೆ — ಲಾಭದಾಯಕ!)"
        )
    },

    {
        "id": "desir_kn_q3",
        "challenge": (
            "Show an UNDESIRABLE answer for the first question — demonstrate what happens "
            "when a student incorrectly classifies milk curdling as undesirable, "
            "and see the feedback explaining the correct classification.\n\n"
            "(ಅನಪೇಕ್ಷಿತ ಉತ್ತರ ತೋರಿಸಿ — ತಪ್ಪು ಆಯ್ಕೆಯ ಪ್ರತಿಕ್ರಿಯೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_undesirable"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_undesirable' as the initialState. "
                "The simulation auto-clicks 'undesirable' for milk curdling — an incorrect answer — "
                "and shows the corrective feedback."
            ),
            "attempt_2": (
                "Set 'initialState=show_undesirable'. The wrong-answer feedback explains: "
                "milk curdling is actually desirable because it produces useful food products. "
                "The simulation guides the student toward correct understanding."
            ),
            "attempt_3": (
                "Choose 'show_undesirable'. The incorrect-answer feedback reinforces: "
                "if a change produces a useful product (curd), it is desirable even though "
                "it changes the milk permanently."
            )
        },
        "concept_reminder": (
            "Contrast for exam preparation: "
            "Milk curdling (desired → produces curd food) = DESIRABLE. "
            "Milk spoiling through unwanted bacteria (making it undrinkable) = UNDESIRABLE. "
            "The same underlying process (bacterial action on milk) can be desirable or undesirable "
            "depending on whether it is controlled and produces something useful. "
            "(ಬ್ಯಾಕ್ಟೀರಿಯಾ ಕ್ರಿಯೆ: ಉದ್ದೇಶಪೂರ್ವಕ = ಅಪೇಕ್ಷಣೀಯ, ಅನಿಯಂತ್ರಿತ = ಅನಪೇಕ್ಷಿತ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — SAY NO TO HARMFUL SUBSTANCES (Kannada)
# 3 questions: show first scenario → show correct NO choice → show wrong YES choice
# =============================================================================
QUIZ_QUESTIONS_KN["say_no_kn"] = [

    {
        "id": "sayno_kn_q1",
        "challenge": (
            "Start the scenario at the beginning. Show scenario 1 (cigarette peer pressure) "
            "before any response is selected — let the student understand the situation.\n\n"
            "(ಮೊದಲ ಸನ್ನಿವೇಶ ತೋರಿಸಿ — ಸಮವಯಸ್ಕ ಒತ್ತಡ: ಸಿಗರೇಟ್ ಕೊಡುತ್ತಾರೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the initialState. "
                "Scenario 1 is shown: a friend offers a cigarette at a party saying "
                "'everyone's doing it'. No response is selected yet."
            ),
            "attempt_2": (
                "Set 'initialState=initial'. The peer pressure scenario appears. "
                "Think: what is the right response? What are the health consequences of accepting?"
            ),
            "attempt_3": (
                "Choose 'initial'. The scenario shows the starting situation before any choice. "
                "Context: cigarettes contain highly addictive nicotine and cause serious lung disease. "
                "This is the moment to assess the situation and make a decision."
            )
        },
        "concept_reminder": (
            "Peer pressure scenario: friend offers cigarette. "
            "Tobacco contains NICOTINE — highly addictive. Just one cigarette can start dependency. "
            "Long-term effects: lung cancer, heart disease, reduced lung capacity. "
            "You always have the right to say NO. Real friends respect your decision. "
            "(ಸಮವಯಸ್ಕ ಒತ್ತಡ: ನಿಮ್ಮ ಆರೋಗ್ಯ ರಕ್ಷಿಸಲು 'ಇಲ್ಲ' ಹೇಳಿ!)"
        )
    },

    {
        "id": "sayno_kn_q2",
        "challenge": (
            "Show the CORRECT response to peer pressure: demonstrate saying NO to "
            "the cigarette offer and see the positive reinforcement feedback.\n\n"
            "(ಸರಿಯಾದ ಉತ್ತರ ತೋರಿಸಿ — 'ಇಲ್ಲ' ಹೇಳುವ ಸಾಹಸ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_no"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_no' as the initialState. "
                "The simulation auto-clicks 'NO' for scenario 1 and shows the "
                "positive feedback: 'Saying NO takes courage and is the smart choice!'"
            ),
            "attempt_2": (
                "Set 'initialState=show_no'. The correct NO response is selected. "
                "Feedback explains: real friends respect your decision; nicotine is highly addictive; "
                "one cigarette can lead to addiction."
            ),
            "attempt_3": (
                "Choose 'show_no'. The positive feedback reinforces: saying NO is the brave and "
                "healthy choice. Confidence comes from self-respect, not social conformity. "
                "The helpline number 14446 is available if support is ever needed."
            )
        },
        "concept_reminder": (
            "Saying NO to cigarettes: correct and healthy choice. "
            "Nicotine is one of the most addictive substances known. "
            "Adolescent brains are more susceptible to addiction than adult brains. "
            "Strategies to say NO: 'No thank you', leave the situation, cite your values, "
            "change the subject. True friends never pressure you into harming yourself. "
            "(ಧೈರ್ಯದಿಂದ 'ಇಲ್ಲ' ಹೇಳಿ — ಇದು ಶೌರ್ಯ, ಹೇಡಿತನ ಅಲ್ಲ!)"
        )
    },

    {
        "id": "sayno_kn_q3",
        "challenge": (
            "Show the WRONG response: demonstrate selecting 'YES' to the cigarette offer "
            "to reveal the consequences and understand why this choice is harmful.\n\n"
            "(ತಪ್ಪು ಆಯ್ಕೆ ತೋರಿಸಿ — 'ಹೌದು' ಹೇಳಿದರೆ ಏನಾಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "show_yes"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'show_yes' as the initialState. "
                "The simulation auto-clicks 'YES' (wrong choice) and shows the warning feedback "
                "about health risks and addiction potential."
            ),
            "attempt_2": (
                "Set 'initialState=show_yes'. The wrong-answer feedback explains: "
                "accepting to fit in puts health at serious risk. "
                "One cigarette can create nicotine addiction. Real friends don't pressure you."
            ),
            "attempt_3": (
                "Choose 'show_yes' to reveal consequences: giving in to peer pressure → "
                "potential addiction, health damage, and compromised decision-making. "
                "The simulation uses this to teach students why the temptation must be resisted."
            )
        },
        "concept_reminder": (
            "Saying YES to harmful substances: wrong choice with serious consequences. "
            "Accepting peer-pressured cigarettes risks: nicotine addiction (within days), "
            "lung damage, reduced sports performance, and normalising harmful behaviour. "
            "If you feel pressured: walk away, call the helpline (14446 — free, 24/7), "
            "or talk to a trusted adult. Your health and future are worth protecting. "
            "(ಒತ್ತಡಕ್ಕೆ ಮಣಿಯಬೇಡಿ — ಆರೋಗ್ಯ ಬೆಲೆಕಟ್ಟಲಾಗದ ಸಂಪತ್ತು!)"
        )
    }
]


# =============================================================================
# LIFE STAGES OF HUMANS SIMULATION
# ಮಾನವ ಜೀವನದ ಹಂತಗಳು – ಶಿಶು ಅವಧಿಯಿಂದ ವೃದ್ಧಾಪ್ಯದವರೆಗೆ
# Science Chapter 6 – Growing Up
# =============================================================================
SIMULATIONS_KN["life_stages_kn"] = {
    "title": "ಮಾನವ ಜೀವನದ ಹಂತಗಳು (Human Life Stages)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation1_life_stages_kn.html",
    "description": (
        "Kannada interactive timeline simulation showing the five stages of human life: "
        "infancy (0-2 yrs), childhood (3-9 yrs), adolescence (10-19 yrs), adulthood (20-60 yrs), "
        "and old age (60+ yrs). Clicking any stage on the vertical timeline updates a detail "
        "panel with that stage's key physical, cognitive, social and emotional characteristics. "
        "The adolescence stage is specially highlighted as the central 'you are here' stage. "
        "A comparison panel draws analogies to plant growth (seed→sprout→flower→mature tree), "
        "reinforcing that growth patterns are universal across nature."
    ),
    "cannot_demonstrate": [
        "Individual variation in onset of life stages",
        "Numerical comparisons of developmental milestones",
        "Neurological or biological details of each stage",
        "Interactive progression from one stage to the next"
    ],
    "initial_params": {"initialState": "adolescence", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Life Stage",
            "range": "infant, childhood, adolescence, adulthood, old_age",
            "url_key": "initialState",
            "effect": (
                "Selects and highlights the specified life stage on the timeline:\n"
                "  'infant'      → Infancy (0-2 yrs): rapid growth, learning to walk & speak\n"
                "  'childhood'   → Childhood (3-9 yrs): learning, play, social skills\n"
                "  'adolescence' → Adolescence (10-19 yrs): puberty, identity, transition (default)\n"
                "  'adulthood'   → Adulthood (20-60 yrs): independence, career, family\n"
                "  'old_age'     → Old Age (60+ yrs): wisdom, experience, guidance"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, nature comparison box, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Human Life Progresses Through Five Distinct Stages",
            "description": (
                "Human life is divided into five sequential stages, each characterised by "
                "unique patterns of physical, cognitive, social and emotional development. "
                "Understanding these stages helps us appreciate changes happening in our own bodies."
            ),
            "key_insight": (
                "The five stages — infancy → childhood → adolescence → adulthood → old age — "
                "are universal to all humans, though the exact timing varies between individuals. "
                "Each stage builds on the previous one, preparing the person for the next."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Adolescence Is the Critical Transitional Stage",
            "description": (
                "Adolescence (10-19 years) is the bridge between childhood and adulthood. "
                "It is marked by rapid physical growth, emotional changes, identity formation, "
                "and the beginning of reproductive maturity (puberty)."
            ),
            "key_insight": (
                "Adolescence is specially highlighted in the simulation because it is the period "
                "students are currently living through. The rapid changes — physical, emotional, "
                "social — are all normal and expected parts of development. "
                "Recognising adolescence as a stage helps students understand their own experience."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Growth Patterns Are Universal Across Nature",
            "description": (
                "Just as humans pass through predictable life stages, plants also grow through "
                "sequential phases: seed → sprout → flowering → mature tree. "
                "This pattern of staged development is a universal biological principle."
            ),
            "key_insight": (
                "The plant analogy (seed = infancy, sprout = childhood, flowering = adolescence, "
                "mature tree = adulthood) helps students see that staged growth is not unique to "
                "humans — it is a fundamental feature of all living organisms. "
                "Each organism grows to reach its reproductive potential."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# GROWTH CHART DURING ADOLESCENCE SIMULATION
# ಕೌಮಾರದಲ್ಲಿ ಬೆಳವಣಿಗೆ – ಎತ್ತರ ಮತ್ತು ತೂಕ ಬದಲಾವಣೆ
# Science Chapter 6 – Growing Up
# =============================================================================
SIMULATIONS_KN["growth_chart_kn"] = {
    "title": "ಕೌಮಾರದಲ್ಲಿ ಬೆಳವಣಿಗೆ ಚಾರ್ಟ್ (Growth Chart During Adolescence)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation2_growth_chart_kn.html",
    "description": (
        "Kannada interactive growth chart simulation using an age slider (5-20 years) "
        "to visualise how height and weight change across childhood and adolescence. "
        "Dragging the slider updates: an animated person figure (height), displayed stats "
        "(average height in cm, average weight in kg), annual growth rate indicators "
        "(showing the growth spurt with a 'rocket' icon when annual gain ≥ 6 cm), "
        "and a descriptive info panel explaining what is happening at each age. "
        "The adolescent period (10-18) is highlighted in orange, showing the growth spurt. "
        "Facts about gender differences in growth timing are also displayed."
    ),
    "cannot_demonstrate": [
        "Individual variation — these are population averages only",
        "Exact genetic contribution to final height",
        "Weight-for-height (BMI) calculations",
        "Nutrition or sleep effects on growth rate"
    ],
    "initial_params": {"initialState": "age_12", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Age to Display",
            "range": "age_8, age_10, age_12, age_13, age_14, age_15, age_16, age_18, age_20",
            "url_key": "initialState",
            "effect": (
                "Sets the age slider to the given age value and updates all growth stats:\n"
                "  'age_8'  → pre-puberty (128 cm, 26 kg, steady growth)\n"
                "  'age_10' → pre-adolescence (138 cm, 32 kg, puberty approaching)\n"
                "  'age_12' → early adolescence (149 cm, 40 kg, growth spurt beginning) [default]\n"
                "  'age_13' → puberty peak (156 cm, 45 kg, rocket icon growth)\n"
                "  'age_14' → continued rapid growth (162 cm, 50 kg)\n"
                "  'age_15' → mid-adolescence (167 cm, 55 kg, growth slowing)\n"
                "  'age_16' → nearing adult height (170 cm, 58 kg)\n"
                "  'age_18' → near-adult (173 cm, 62 kg, final stages)\n"
                "  'age_20' → adult height reached (175 cm, 65 kg)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, puberty highlight fact box, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "The Growth Spurt: Rapid Height and Weight Increase in Adolescence",
            "description": (
                "During adolescence, the body experiences a dramatic increase in growth "
                "rate called the 'growth spurt'. Adolescents can grow 8-12 cm in a single year, "
                "compared to the steady 5-6 cm/year in childhood."
            ),
            "key_insight": (
                "The growth spurt is driven by a surge in growth hormones (GH) and sex hormones "
                "(testosterone in boys, oestrogen in girls). "
                "The simulation shows this visually: the height gain per year jumps dramatically "
                "at ages 12-15, with the rocket icon appearing when annual gain ≥ 6 cm."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Girls and Boys Experience Growth Spurts at Different Ages",
            "description": (
                "Girls typically reach their growth spurt earlier (ages 10-14) than boys (ages 12-16). "
                "This is why girls are often taller than boys in early adolescence, "
                "but boys eventually become taller as adults on average."
            ),
            "key_insight": (
                "The simulation shows average data (combined), but the fact box explains gender "
                "differences in timing. Girls' earlier growth spurt is linked to earlier puberty: "
                "female sex hormones (oestrogen) are released sooner than male (testosterone). "
                "By age 16-17, most boys have caught up and typically exceed girls in height."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Every Person Grows at Their Own Pace — All Variation Is Normal",
            "description": (
                "The growth data shown represents population averages. Individual adolescents "
                "may reach their growth spurt earlier or later, and reach different final heights, "
                "all of which is completely normal and determined mainly by genetics."
            ),
            "key_insight": (
                "Good nutrition (especially calcium, protein), adequate sleep (8-9 hours when growth "
                "hormone is primarily released), and regular exercise all support reaching one's "
                "genetic height potential. Not maturing at the exact 'average' age is not a "
                "medical concern."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# PHYSICAL CHANGES DURING PUBERTY SIMULATION
# ಯೌವನದಲ್ಲಿ ಭೌತಿಕ ಬದಲಾವಣೆಗಳು – ಸಾಮಾನ್ಯ, ಹುಡುಗರು, ಹುಡುಗಿಯರು
# Science Chapter 6 – Growing Up
# =============================================================================
SIMULATIONS_KN["puberty_physical_changes_kn"] = {
    "title": "ಯೌವನದಲ್ಲಿ ಭೌತಿಕ ಬದಲಾವಣೆಗಳು (Physical Changes in Puberty)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation3_physical_changes_kn.html",
    "description": (
        "Kannada three-tab simulation cataloguing physical changes during puberty, "
        "organised into three categories: "
        "Common Changes (all genders): growth spurt, body hair, increased sweating, skin/acne. "
        "Boys-specific: voice deepening, broader shoulders, facial hair. "
        "Girls-specific: wider hips, breast development, onset of menstruation. "
        "Tapping any item in the list opens a detailed explanation panel showing what causes the "
        "change, what it looks/feels like, and a green badge confirming it is completely normal. "
        "A secondary information panel explains the term 'secondary sexual characteristics'."
    ),
    "cannot_demonstrate": [
        "Exact hormonal mechanisms causing each change",
        "Timeline or sequencing of changes in a single individual",
        "Emotional and psychological changes (covered in the life stages sim)",
        "Gender-diverse or intersex puberty experiences"
    ],
    "initial_params": {"initialState": "common", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Change Category",
            "range": "common, boys, girls",
            "url_key": "initialState",
            "effect": (
                "Selects which category of puberty changes to display:\n"
                "  'common' → changes in all genders: growth spurt, body hair, sweat, acne [default]\n"
                "  'boys'   → boys-specific changes: voice deepening, broad shoulders, facial hair\n"
                "  'girls'  → girls-specific changes: wider hips, breast development, menstruation"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, secondary sexual characteristics panel, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "All Puberty Changes Are Normal and Hormone-Driven",
            "description": (
                "Every physical change during puberty — from acne to body hair to growth spurts "
                "— is caused by hormones released by the body. These changes are universal, "
                "completely normal, and happen to everyone."
            ),
            "key_insight": (
                "The green 'normal' badge in the simulation reinforces that no puberty change is "
                "a cause for shame or concern. Hormones (testosterone, oestrogen, growth hormone) "
                "trigger all these changes as the body prepares for adulthood and reproduction."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Secondary Sexual Characteristics Differentiate Male and Female Bodies",
            "description": (
                "Puberty-specific changes that differ between males and females are called "
                "'secondary sexual characteristics'. These include voice depth, body fat distribution, "
                "facial hair, and breast development — distinguishing adult male and female bodies."
            ),
            "key_insight": (
                "Secondary sexual characteristics are features caused by sex hormones that appear "
                "during puberty but are not the primary reproductive organs themselves. "
                "They are 'secondary' because they appear after primary sexual characteristics "
                "(genitalia) which are present from birth."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Some Changes Are Shared, Some Are Gender-Specific",
            "description": (
                "While some puberty changes occur in all adolescents (growth spurt, body hair, "
                "acne), others are specific to one sex (voice cracking in boys, breast development "
                "in girls). This is because the hormones driving these changes differ."
            ),
            "key_insight": (
                "Boys' testes produce testosterone → deeper voice, facial hair, broader shoulders. "
                "Girls' ovaries produce oestrogen/progesterone → breast development, wider hips, "
                "start of menstrual cycle. Common changes are driven by adrenal androgens "
                "present in all genders."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# VOICE CHANGES DURING PUBERTY SIMULATION
# ಯೌವನದಲ್ಲಿ ಧ್ವನಿ ಬದಲಾವಣೆಗಳು – ಸ್ವರಪೆಟ್ಟಿಗೆ ಬೆಳವಣಿಗೆ
# Science Chapter 6 – Growing Up
# =============================================================================
SIMULATIONS_KN["voice_changes_kn"] = {
    "title": "ಯೌವನದಲ್ಲಿ ಧ್ವನಿ ಬದಲಾವಣೆಗಳು (Voice Changes in Puberty)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation4_voice_changes_kn.html",
    "description": (
        "Kannada interactive simulation using an SVG diagram of the larynx (voice box) "
        "to show how the larynx grows during puberty, causing voice changes. "
        "Two gender tabs (boys/girls) × three stage buttons (before/during/after puberty) "
        "give 6 explorable states. Each state updates: the SVG larynx diagram size, vocal cord "
        "positions, presence of the Adam's apple, animated sound-wave bars visualising pitch, "
        "and a text panel explaining the biological change. "
        "A comparison panel shows boys' voices deepen ~1 octave while girls' change only ~3 semitones. "
        "The voice-cracking phenomenon is explained as muscles adapting to the rapidly growing larynx."
    ),
    "cannot_demonstrate": [
        "Actual audio demonstration of voice pitch",
        "Detailed vocal cord anatomy beyond simplified SVG",
        "Hormonal dosage driving larynx growth",
        "Non-binary or intersex voice change patterns"
    ],
    "initial_params": {"initialState": "boys_before", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Gender × Puberty Stage",
            "range": "boys_before, boys_during, boys_after, girls_before, girls_during, girls_after",
            "url_key": "initialState",
            "effect": (
                "Selects gender AND puberty stage to show the larynx and voice state:\n"
                "  'boys_before'  → boys, pre-puberty: small larynx, high pitch (default)\n"
                "  'boys_during'  → boys, mid-puberty: larynx growing, voice cracking\n"
                "  'boys_after'   → boys, post-puberty: large larynx, deep adult voice, Adam's apple\n"
                "  'girls_before' → girls, pre-puberty: small larynx, high pitch\n"
                "  'girls_during' → girls, mid-puberty: slight larynx growth, subtle change\n"
                "  'girls_after'  → girls, post-puberty: modest change, mature female voice"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and fun facts takeaway panel."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "The Larynx Grows During Puberty, Changing the Voice",
            "description": (
                "The larynx (voice box) contains vocal cords that vibrate to produce sound. "
                "During puberty, sex hormones cause the larynx to grow larger. "
                "Longer, thicker vocal cords vibrate more slowly, producing a lower-pitched sound."
            ),
            "key_insight": (
                "Before puberty: small larynx → short vocal cords → fast vibration → high pitch. "
                "After puberty in boys: larynx grows ~60% larger → long thick cords → slow vibration "
                "→ deep voice (~1 octave drop). The Adam's apple is simply the larger larynx "
                "visible through the skin of the neck."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Voice Cracking Is Temporary — Muscles Adjusting to Rapid Larynx Growth",
            "description": (
                "During peak growth, the larynx enlarges so rapidly that the muscles controlling "
                "the vocal cords temporarily lose their coordination, causing the voice to "
                "crack or squeak unpredictably. This is completely normal and temporary."
            ),
            "key_insight": (
                "Voice cracking only occurs because the muscles cannot immediately adjust to the "
                "rapidly growing larynx. Once growth stabilises, the muscles re-coordinate and "
                "the voice settles into its new deeper range, typically by age 16-17 in boys."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Voice Change Is Much Greater in Boys Than in Girls",
            "description": (
                "Boys' voices deepen by approximately one full octave during puberty, "
                "while girls' voices deepen by only ~3 semitones. "
                "This is because testosterone drives much greater larynx growth than oestrogen."
            ),
            "key_insight": (
                "The difference in voice change magnitude directly reflects the difference in "
                "sex hormone effects: testosterone in boys drives ~60% larynx growth; "
                "oestrogen in girls drives only ~30% growth. "
                "This is why adult male voices are typically much deeper than adult female voices, "
                "even though children of both sexes have similar voice pitches."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# MENSTRUAL CYCLE SIMULATION
# ಋತುಚಕ್ರ ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು – ನಾಲ್ಕು ಹಂತಗಳ ಚಕ್ರ
# Science Chapter 6 – Growing Up
# =============================================================================
SIMULATIONS_KN["menstrual_cycle_kn"] = {
    "title": "ಋತುಚಕ್ರ ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು (Understanding the Menstrual Cycle)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation5_menstrual_cycle_kn.html",
    "description": (
        "Kannada interactive simulation with a circular 28-day cycle diagram and a day slider "
        "to explore the four phases of the menstrual cycle: "
        "Menstruation (days 1-5): uterine lining shedding. "
        "Follicular phase (days 6-13): uterine lining rebuilding, body preparing. "
        "Ovulation (day 14): egg released from ovary. "
        "Luteal phase (days 15-28): body waiting for potential fertilisation; if none, cycle restarts. "
        "Dragging the slider or clicking legend items jumps to each phase, updating the ring diagram "
        "center, phase title, and educational description. "
        "A myth-buster panel challenges common misconceptions (periods are not impure; exercise is safe). "
        "The takeaway covers cycle length variation, menopause, and when to talk to a doctor."
    ),
    "cannot_demonstrate": [
        "Hormonal levels (FSH, LH, oestrogen, progesterone) across the cycle",
        "What happens if fertilisation occurs",
        "Pregnancy or foetal development",
        "Contraception or reproductive health beyond cycle education",
        "Cycle irregularity causes or medical conditions"
    ],
    "initial_params": {"initialState": "menstruation", "showHints": True},
    "parameter_info": {
        "initialState": {
            "label": "Cycle Phase",
            "range": "menstruation, follicular, ovulation, luteal",
            "url_key": "initialState",
            "effect": (
                "Jumps the cycle diagram to the specified phase:\n"
                "  'menstruation' → days 1-5: uterine lining sheds, pink/red phase [default]\n"
                "  'follicular'   → days 6-13: lining rebuilds, orange phase\n"
                "  'ovulation'    → day 14: egg released, green phase\n"
                "  'luteal'       → days 15-28: waiting period, blue phase"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, myth-buster panel, and takeaway."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "The Menstrual Cycle Is a Natural Monthly Biological Process",
            "description": (
                "The menstrual cycle is the monthly cycle by which the uterine lining builds up "
                "to prepare for a possible pregnancy, and then sheds if no fertilisation occurs. "
                "It begins during puberty (typically ages 10-15) and is a sign of reproductive health."
            ),
            "key_insight": (
                "The cycle is driven by hormones (FSH, LH, oestrogen, progesterone) in a carefully "
                "co-ordinated sequence. The average cycle is 28 days but 21-35 days is normal. "
                "The menstrual cycle is not a disease or a weakness — it is a sign that the "
                "reproductive system is functioning correctly."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "The Four Phases and What Happens in Each",
            "description": (
                "Phase 1 — Menstruation (d.1-5): uterine lining sheds → bleeding. "
                "Phase 2 — Follicular (d.6-13): lining regrows, egg matures in ovary. "
                "Phase 3 — Ovulation (d.14): mature egg released from ovary. "
                "Phase 4 — Luteal (d.15-28): body prepares for implantation; if no fertilisation, "
                "hormone levels drop → cycle restarts."
            ),
            "key_insight": (
                "The four phases form a continuous, repeating cycle. "
                "Ovulation (day 14) is the pivotal event — when pregnancy can occur. "
                "If no pregnancy: progesterone drops → uterine lining sheds → day 1 of next cycle. "
                "This continuous preparation-and-shed cycle repeats monthly from puberty to menopause."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Menstruation Is Normal — Myths Must Be Challenged",
            "description": (
                "Many harmful cultural myths surround menstruation — that menstruating girls are "
                "impure, should be isolated, or should not exercise. All of these are false. "
                "Menstruation is a completely natural biological process with no spiritual or "
                "hygiene implications beyond normal sanitary management."
            ),
            "key_insight": (
                "The myth-buster panel in the simulation directly addresses two common myths: "
                "(1) isolation/impurity myths — false; menstruation is biologically normal. "
                "(2) exercise restriction — false; light exercise can actually reduce cramps and "
                "improve mood by releasing endorphins. Education is the tool to dismantle these myths."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# QUIZ QUESTIONS — LIFE STAGES OF HUMANS (Kannada)
# 3 questions: adolescence (key stage) → contrast childhood vs old_age → infant
# =============================================================================
QUIZ_QUESTIONS_KN["life_stages_kn"] = [

    {
        "id": "life_kn_q1",
        "challenge": (
            "Show the ADOLESCENCE stage on the life-stages timeline. "
            "Demonstrate why adolescence is the central and most significant stage "
            "in terms of biological transformation.\n\n"
            "(ಕೌಮಾರ ಹಂತ ತೋರಿಸಿ — ಏಕೆ ಇದು ಅತ್ಯಂತ ಮಹತ್ವದ ಹಂತ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "adolescence"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'adolescence' as the initialState. "
                "The timeline will highlight the ⭐ adolescence stage (10-19 years) with "
                "its orange emphasis, showing it as the transitional stage between childhood and adulthood."
            ),
            "attempt_2": (
                "Set 'initialState=adolescence'. The detail panel will show: rapid physical growth, "
                "puberty changes, emotional development, identity formation, and cognitive growth. "
                "Adolescence is highlighted because students are currently in this stage."
            ),
            "attempt_3": (
                "Choose 'adolescence'. The stage is specially marked with a ⭐ symbol because "
                "it is the bridge stage: childhood (dependent, learning) → adolescence (changing, "
                "growing reproductive capability) → adulthood (independent, responsible)."
            )
        },
        "concept_reminder": (
            "Adolescence (10-19 years) is the transitional stage between childhood and adulthood. "
            "Key changes: rapid physical growth, puberty, emotional changes, identity formation. "
            "It is highlighted specially because all students studying this topic are currently "
            "experiencing this stage. The orange colour in the simulation marks it as the 'current' stage. "
            "(ಕೌಮಾರ = ಬಾಲ್ಯ ಮತ್ತು ಪ್ರೌಢಾವಸ್ಥೆಯ ನಡುವಿನ ಪರಿವರ್ತನಾ ಹಂತ!)"
        )
    },

    {
        "id": "life_kn_q2",
        "challenge": (
            "Show the INFANT stage. Compare infancy with adolescence — "
            "what makes infancy the stage of maximum physical growth rate "
            "even faster than the adolescent growth spurt?\n\n"
            "(ಶಿಶು ಅವಧಿ ತೋರಿಸಿ — ಬೆಳವಣಿಗೆ ದರ ಹೋಲಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "infant"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'infant' as the initialState. "
                "The timeline will show infancy (0-2 years): the stage of the fastest physical "
                "growth in human life, when birth weight triples and the first words are spoken."
            ),
            "attempt_2": (
                "Set 'initialState=infant'. The detail panel explains: rapid physical growth, "
                "learning to walk, first words, complete dependence on parents. "
                "Height growth in the first year is faster than in the adolescent growth spurt."
            ),
            "attempt_3": (
                "Choose 'infant'. The 👶 stage (0-2 years) shows sensory-motor learning: "
                "infants learn about the world through their senses (touching, tasting, seeing). "
                "Weight triples in year 1. This is actually the highest absolute growth rate "
                "per year in the entire human lifespan."
            )
        },
        "concept_reminder": (
            "Infancy (0-2 years): the 👶 stage. Key features: "
            "birth weight triples in year 1 (fastest physical growth in life), "
            "motor skills develop (rolling → sitting → standing → walking), "
            "first words spoken, complete parental dependence. "
            "Though adolescence has a notable growth spurt, a baby's first-year growth "
            "rate is actually faster in absolute terms. "
            "(ಶಿಶು ಅವಧಿ = ಜೀವನದ ಅತ್ಯಂತ ವೇಗದ ಬೆಳವಣಿಗೆ ಹಂತ!)"
        )
    },

    {
        "id": "life_kn_q3",
        "challenge": (
            "Show the OLD AGE stage. What makes old age valuable despite the "
            "physical slowing of the body?\n\n"
            "(ವೃದ್ಧಾವಸ್ಥೆ ತೋರಿಸಿ — ಭೌತಿಕ ನಿಧಾನ, ಆದರೆ ಜ್ಞಾನ ಅಮೂಲ್ಯ!)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "old_age"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'old_age' as the initialState. "
                "The timeline shows old age (60+ years): physical slowing but accumulation of "
                "wisdom and life experience."
            ),
            "attempt_2": (
                "Set 'initialState=old_age'. The detail panel shows: gradual physical slowing, "
                "mental wisdom and knowledge from life experience, grandparent role as mentor to "
                "younger generations, sharing of knowledge and stories."
            ),
            "attempt_3": (
                "Choose 'old_age'. The 👴 stage: body slows but knowledge and experience grow. "
                "Elders serve as guides and mentors (grandparents, teachers). "
                "They are a 'treasure of experience and wisdom' as the simulation states."
            )
        },
        "concept_reminder": (
            "Old age (60+ years): the 👴 stage. Key features: "
            "gradual physical slowing (reduced speed and strength), "
            "accumulated wisdom and life experience, "
            "social role as guide/mentor/grandparent, "
            "continued learning and reflection. "
            "Each life stage has its own unique value — old age contributes wisdom and intergenerational knowledge. "
            "(ವೃದ್ಧಾವಸ್ಥೆ = ಜ್ಞಾನ ಮತ್ತು ಅನುಭವದ ನಿಧಿ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — GROWTH CHART DURING ADOLESCENCE (Kannada)
# 3 questions: peak growth spurt age → pre-puberty → adult
# =============================================================================
QUIZ_QUESTIONS_KN["growth_chart_kn"] = [

    {
        "id": "growth_kn_q1",
        "challenge": (
            "Show the AGE 13 growth data — the peak of the adolescent growth spurt. "
            "Demonstrate that this is when the rocket-icon appears, indicating the fastest "
            "growth rate in the adolescent period.\n\n"
            "(ವಯಸ್ಸು 13 ತೋರಿಸಿ — ಬೆಳವಣಿಗೆ ಉಲ್ಬಣದ ಉತ್ಕರ್ಷ!)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "age_13"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'age_13' as the initialState. "
                "The slider jumps to age 13 (156 cm, 45 kg) and displays the 🚀 growth-spurt icon "
                "showing +7 cm gained in this year — the fastest annual growth in the simulation."
            ),
            "attempt_2": (
                "Set 'initialState=age_13'. At 13, the growth rate indicator shows maximum growth "
                "(7 cm/year), the orange 'adolescence' highlight is active, and the info panel "
                "shows 'Many people's peak growth. Body is changing rapidly.'"
            ),
            "attempt_3": (
                "Choose 'age_13'. The visual figure shows a rapidly growing person, the height "
                "stat shows +7 cm/year (the rocket icon), and the weight increased by +5 kg. "
                "This confirms age 13 as the growth-spurt peak in the simulation data."
            )
        },
        "concept_reminder": (
            "The adolescent growth spurt typically peaks around age 12-14. "
            "At age 13 in the simulation: height = 156 cm (up 7 cm from age 12), weight = 45 kg "
            "(up 5 kg). This 7 cm/year rate triggers the 🚀 icon — faster than typical childhood "
            "growth of ~5 cm/year. Growth hormone and sex hormones drive this rapid acceleration. "
            "(ಬೆಳವಣಿಗೆ ಉಲ್ಬಣ: ವರ್ಷಕ್ಕೆ 8-12 ಸೆ.ಮೀ ಬೆಳೆಯಬಹುದು!)"
        )
    },

    {
        "id": "growth_kn_q2",
        "challenge": (
            "Show AGE 8 — the pre-puberty baseline. Compare this steady childhood "
            "growth with the adolescent growth spurt you just saw.\n\n"
            "(ವಯಸ್ಸು 8 ತೋರಿಸಿ — ಯೌವನ ಪೂರ್ವ ಸ್ಥಿರ ಬೆಳವಣಿಗೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "age_8"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'age_8' as the initialState. "
                "The slider shows age 8 (128 cm, 26 kg) with a '📊 ಸ್ಥಿರ ಬೆಳವಣಿಗೆ' (steady growth) "
                "indicator — no growth spurt icon, just calm, consistent growth."
            ),
            "attempt_2": (
                "Set 'initialState=age_8'. The growth rate indicator shows +6 cm from age 7 — "
                "steady but not spectacular. The info panel says 'Consistent steady growth, "
                "physical ability developing.' The purple/teal highlight is absent (not yet adolescence)."
            ),
            "attempt_3": (
                "Choose 'age_8'. At 8 years, growth is regular and predictable — about 5-6 cm/year. "
                "Compare with age 13 (+7 cm/year): the spurt is visually obvious. "
                "This contrast shows why adolescence is recognised as a special growth period."
            )
        },
        "concept_reminder": (
            "Pre-puberty growth (age 5-10): steady at approximately 5-6 cm per year. "
            "At age 8: 128 cm, 26 kg. Growth is consistent but not dramatically fast. "
            "This steady childhood pattern contrasts sharply with the adolescent growth spurt "
            "(8-12 cm/year at peak). The difference in growth rate is what defines the 'spurt'. "
            "(ಬಾಲ್ಯ ಬೆಳವಣಿಗೆ: ಸ್ಥಿರ ಮತ್ತು ಮಿತ — ಕೌಮಾರ ಏರಿಕೆಗಿಂತ ನಿಧಾನ!)"
        )
    },

    {
        "id": "growth_kn_q3",
        "challenge": (
            "Show AGE 20 — the point where adult height is essentially reached. "
            "Demonstrate that growth slows dramatically after the adolescent spurt.\n\n"
            "(ವಯಸ್ಸು 20 ತೋರಿಸಿ — ಪ್ರೌಢ ಎತ್ತರ ತಲುಪಿದಾಗ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "age_20"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'age_20' as the initialState. "
                "The slider shows age 20 (175 cm, 65 kg), with growth slowing to only +1 cm "
                "from age 19. The info panel says 'Generally adult height reached'."
            ),
            "attempt_2": (
                "Set 'initialState=age_20'. At 20, only +1 cm gained from age 19 — near zero growth. "
                "Compare with age 13 (+7 cm/year): the growth rate has dropped dramatically after "
                "the spurt. Growth plates (epiphyseal plates) close at the end of adolescence."
            ),
            "attempt_3": (
                "Choose 'age_20'. The 175 cm final height contrasts with 128 cm at age 8 — a "
                "47 cm total gain over 12 years, mostly in the adolescent spurt between ages 10-17. "
                "After the growth plates close, no more height gain is possible."
            )
        },
        "concept_reminder": (
            "Adult height is typically reached by age 17-20. "
            "At age 20: 175 cm (average), +1 cm from age 19 — near-zero growth rate. "
            "Growth stops because sex hormones cause the growth plates (epiphyseal plates at "
            "the ends of long bones) to close. Once closed, the bones cannot lengthen further. "
            "This is why proper nutrition during the growth spurt (ages 10-17) is critical. "
            "(ಬೆಳವಣಿಗೆ ಫಲಕಗಳು ಮುಚ್ಚಿದ ನಂತರ ಎತ್ತರ ಹೆಚ್ಚಾಗುವುದಿಲ್ಲ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — PHYSICAL CHANGES IN PUBERTY (Kannada)
# 3 questions: common changes → boys-specific → girls-specific
# =============================================================================
QUIZ_QUESTIONS_KN["puberty_physical_changes_kn"] = [

    {
        "id": "phys_kn_q1",
        "challenge": (
            "Show the COMMON changes tab — physical changes that occur in ALL adolescents "
            "regardless of gender. Identify what causes these changes.\n\n"
            "(ಎಲ್ಲರಲ್ಲೂ ಕಾಣುವ ಸಾಮಾನ್ಯ ಬದಲಾವಣೆಗಳು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "common"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'common' as the initialState. "
                "The '🔄 ಸಾಮಾನ್ಯ ಬದಲಾವಣೆಗಳು' tab is selected, showing changes that happen "
                "in both boys and girls: growth spurt, body hair, increased sweating, acne."
            ),
            "attempt_2": (
                "Set 'initialState=common'. Four changes are listed: 📏 growth spurt, "
                "🌿 body hair (underarms, pubic area), 😓 increased sweat/body odour, "
                "🔴 skin changes (acne). All are caused by adrenal androgens present in all genders."
            ),
            "attempt_3": (
                "Choose 'common'. These changes happen in all adolescents because adrenal glands "
                "(present in everyone) release androgens during puberty. Tap any item to see "
                "detailed explanation — all items have a green 'completely normal' badge."
            )
        },
        "concept_reminder": (
            "Common puberty changes (all genders): "
            "1. Growth spurt (8-12 cm/year peak) — growth hormone surge. "
            "2. Body hair in underarms and pubic area — adrenal androgens. "
            "3. Increased sweating and body odour — sweat gland activation. "
            "4. Acne — sebaceous glands produce more oil under hormone influence. "
            "All are 100% normal and happen to everyone. Good hygiene (bathing, deodorant) "
            "helps manage sweating and acne. "
            "(ಎಲ್ಲಾ ಬದಲಾವಣೆಗಳು ಸಾಮಾನ್ಯ — ಭಯ ಬೇಡ!)"
        )
    },

    {
        "id": "phys_kn_q2",
        "challenge": (
            "Show the BOYS-specific changes tab. What physical changes are unique to "
            "boys during puberty and what hormone drives them?\n\n"
            "(ಹುಡುಗರಲ್ಲಿ ಮಾತ್ರ ಕಾಣುವ ಬದಲಾವಣೆಗಳು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "boys"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'boys' as the initialState. "
                "The '👦 ಹುಡುಗರಲ್ಲಿ' tab appears with boys-specific changes: "
                "🎤 voice deepening, 💪 broader shoulders, 🧔 facial hair."
            ),
            "attempt_2": (
                "Set 'initialState=boys'. The three boys-specific changes show: "
                "voice cracking then deepening (larynx growth), broader chest and shoulders "
                "(testosterone effects on muscle and bone), "
                "upper lip/chin/cheek hair appearing."
            ),
            "attempt_3": (
                "Choose 'boys'. The key driver is testosterone — produced by the testes from "
                "puberty onset. Testosterone causes all three: larynx growth (voice), "
                "muscle/bone broadening (shoulders), and hair follicle stimulation (facial hair). "
                "Tap 'ಸ್ವರ ಆಳ' to see the voice change detail at the simulation level."
            )
        },
        "concept_reminder": (
            "Boys-specific puberty changes driven by testosterone: "
            "1. 🎤 Voice deepening: larynx (voice box) grows larger → vocal cords lengthen → voice drops ~1 octave. "
            "Temporary voice 'cracking' occurs as muscles adjust to the rapid larynx growth. "
            "2. 💪 Broader shoulders: testosterone stimulates bone and muscle growth, widening the chest. "
            "3. 🧔 Facial hair: testosterone activates facial hair follicles; appears first on upper lip. "
            "All driven by testosterone from the testes. "
            "(ಟೆಸ್ಟೋಸ್ಟೆರಾನ್ = ಹುಡುಗರ ಬದಲಾವಣೆಗಳ ಮೂಲ ಕಾರಣ!)"
        )
    },

    {
        "id": "phys_kn_q3",
        "challenge": (
            "Show the GIRLS-specific changes tab. What physical changes are unique to "
            "girls during puberty and which change is the first sign of puberty in girls?\n\n"
            "(ಹುಡುಗಿಯರಲ್ಲಿ ಮಾತ್ರ ಕಾಣುವ ಬದಲಾವಣೆಗಳು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "girls"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'girls' as the initialState. "
                "The '👧 ಹುಡುಗಿಯರಲ್ಲಿ' tab shows girls-specific changes: "
                "📐 wider hips, 🌸 breast development, 🔄 onset of menstruation."
            ),
            "attempt_2": (
                "Set 'initialState=girls'. Three changes appear: "
                "wider hips (body preparing for potential future childbirth), "
                "breast development (usually the FIRST sign of puberty in girls), "
                "and menstrual cycle beginning 2-3 years after breast development starts."
            ),
            "attempt_3": (
                "Choose 'girls'. Tap '🌸 ಸ್ತನ ವಿಕಾಸ' — the detail shows this is the FIRST sign "
                "of puberty in girls. Menstruation (🔄) starts 2-3 years later. "
                "All driven by oestrogen and progesterone from the ovaries."
            )
        },
        "concept_reminder": (
            "Girls-specific puberty changes driven by oestrogen/progesterone: "
            "1. 🌸 Breast development: the FIRST sign of puberty in girls, starts as 'breast buds'. "
            "2. 📐 Wider hips: pelvis broadens under oestrogen influence. "
            "3. 🔄 Menstruation begins: typically 2-3 years after breast development; "
            "the uterine lining begins its monthly cycle. "
            "First menstruation (menarche) usually occurs between ages 11-14. "
            "(ಸ್ತನ ವಿಕಾಸ = ಹುಡುಗಿಯರ ಯೌವನದ ಮೊದಲ ಸಂಕೇತ!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — VOICE CHANGES IN PUBERTY (Kannada)
# 3 questions: boys_after (dramatic change) → boys_during (voice cracking) → girls_after
# =============================================================================
QUIZ_QUESTIONS_KN["voice_changes_kn"] = [

    {
        "id": "voice_kn_q1",
        "challenge": (
            "Show BOYS AFTER PUBERTY — demonstrate the fully developed adult male voice "
            "and larynx. Show how much the larynx has grown and why the Adam's apple is now visible.\n\n"
            "(ಯೌವನದ ನಂತರ ಹುಡುಗರ ಸ್ವರ ತೋರಿಸಿ — ಆಡಮ್‌ಸ್ ಆಪಲ್ ಮತ್ತು ಆಳ ಸ್ವರ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "boys_after"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'boys_after' as the initialState. "
                "The SVG shows the largest larynx size with long vocal cords, the Adam's apple "
                "is visible, and the voice wave bars are taller (deeper frequency)."
            ),
            "attempt_2": (
                "Set 'initialState=boys_after'. The voice pitch shows 'Deep' (adult male). "
                "The info panel explains: larynx has grown about 60% larger, vocal cords are "
                "longer and thicker, producing a deep voice about one octave below the childhood pitch."
            ),
            "attempt_3": (
                "Choose 'boys_after'. The SVG larynx box is now 90×70 (vs 60×50 before puberty). "
                "The Adam's apple triangle is visible. Wave bars are at maximum height (deep bass). "
                "This confirms: bigger larynx → longer cords → slower vibration → deeper voice."
            )
        },
        "concept_reminder": (
            "After puberty (boys): larynx grows ~60% larger (from 60 to 90 units wide). "
            "Vocal cords: longer and thicker → vibrate more slowly → lower frequency → deep voice. "
            "Adam's apple: the enlarged larynx angled forward, visible through the neck skin. "
            "Voice drops approximately one full octave (e.g., from C5 to C4). "
            "Voice change is complete by approximately age 16-17. "
            "(ಆಡಮ್‌ಸ್ ಆಪಲ್ = ಚರ್ಮದ ಮೂಲಕ ಕಾಣುವ ದೊಡ್ಡ ಸ್ವರಪೆಟ್ಟಿಗೆ!)"
        )
    },

    {
        "id": "voice_kn_q2",
        "challenge": (
            "Show BOYS DURING PUBERTY — demonstrate voice cracking. "
            "Explain why the voice unpredictably cracks or squeaks at this stage.\n\n"
            "(ಯೌವನದ ಸಮಯದಲ್ಲಿ ಹುಡುಗರ ಸ್ವರ ಒಡೆಯುವಿಕೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "boys_during"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'boys_during' as the initialState. "
                "The SVG shows an intermediate larynx size with the Adam's apple just appearing. "
                "The voice pitch shows 'Changing' with the description 'Voice may crack!'"
            ),
            "attempt_2": (
                "Set 'initialState=boys_during'. The wave bars are uneven (irregular heights), "
                "representing the unpredictable voice cracking. "
                "The info panel explains: larynx growing so rapidly that muscles haven't adjusted yet."
            ),
            "attempt_3": (
                "Choose 'boys_during'. The intermediate larynx (75×60) is between childhood (60×50) "
                "and adult (90×70). Voice cracking happens because vocal cord muscles haven't "
                "learned to coordinate with the rapidly changing larynx size. This is temporary."
            )
        },
        "concept_reminder": (
            "Voice cracking during puberty: a temporary phenomenon. "
            "Cause: the larynx grows so rapidly that the muscles controlling the vocal cords "
            "temporarily lose their coordination — sometimes the cords vibrate too loosely "
            "(squeak) or too tightly (crack). "
            "This is 100% normal and temporary — muscles gradually adjust over 6-18 months. "
            "By age 16-17, the voice settles into its new deeper range. "
            "(ಸ್ವರ ಒಡೆಯುವಿಕೆ ತಾತ್ಕಾಲಿಕ — ನಿಲ್ಲುತ್ತದೆ!)"
        )
    },

    {
        "id": "voice_kn_q3",
        "challenge": (
            "Show GIRLS AFTER PUBERTY — compare the girls' voice change with boys'. "
            "Why is the voice change so much less dramatic in girls?\n\n"
            "(ಯೌವನದ ನಂತರ ಹುಡುಗಿಯರ ಸ್ವರ ತೋರಿಸಿ — ಹುಡುಗರ ಬದಲಾವಣೆಯೊಂದಿಗೆ ಹೋಲಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "girls_after"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'girls_after' as the initialState. "
                "The SVG shows a modestly larger larynx (70×55 vs 60×50 before) with no Adam's apple. "
                "Voice pitch shows 'Mature' — a subtle, adult female voice."
            ),
            "attempt_2": (
                "Set 'initialState=girls_after'. The info panel explains: girls' larynx grows ~30% "
                "(vs boys' 60%), so the voice deepens only ~3 semitones (vs boys' ~12 semitones = 1 octave). "
                "The change is gradual and usually not very noticeable."
            ),
            "attempt_3": (
                "Choose 'girls_after'. Compare the wave bars with boys_after: girls' bars are shorter "
                "(higher pitch). The larynx box is smaller: 70×55 for girls vs 90×70 for boys. "
                "The difference in larynx growth is directly caused by the difference in hormones: "
                "oestrogen vs testosterone."
            )
        },
        "concept_reminder": (
            "Girls' voice change after puberty: subtle and gradual. "
            "Girls' larynx grows ~30% (oestrogen effect) vs boys' ~60% (testosterone effect). "
            "Result: girls' voice deepens by only ~3 semitones (~a minor third) vs boys' ~12 semitones (1 octave). "
            "No Adam's apple appears in girls (the larynx doesn't tilt forward enough to show). "
            "Adult female voices are typically higher than adult male voices for this anatomical reason. "
            "(ಹೆಣ್ಣಿನ ಸ್ವರ ಬದಲಾವಣೆ ಕಡಿಮೆ — ಟೆಸ್ಟೋಸ್ಟೆರಾನ್ ಇಲ್ಲ, ಸ್ವರಪೆಟ್ಟಿಗೆ ಚಿಕ್ಕದು!)"
        )
    }
]


# =============================================================================
# QUIZ QUESTIONS — MENSTRUAL CYCLE (Kannada)
# 3 questions: menstruation (start) → ovulation (pivotal event) → luteal (completion)
# =============================================================================
QUIZ_QUESTIONS_KN["menstrual_cycle_kn"] = [

    {
        "id": "menses_kn_q1",
        "challenge": (
            "Show the MENSTRUATION phase (days 1-5). "
            "Explain what happens in the uterus during this phase and why it is the START "
            "of a new cycle, not the end.\n\n"
            "(ಋತುಚಕ್ರ ಹಂತ ತೋರಿಸಿ — ಇದು ಮುಕ್ತಾಯ ಅಲ್ಲ, ಹೊಸ ಆರಂಭ!)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "menstruation"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'menstruation' as the initialState. "
                "The cycle diagram jumps to days 1-5 (pink ring segment), the center shows 'Day 1 / ಋತುಚಕ್ರ', "
                "and the phase info explains uterine lining shedding."
            ),
            "attempt_2": (
                "Set 'initialState=menstruation'. Days 1-5 are highlighted in the ring. "
                "The phase text explains: uterine lining sheds because no pregnancy occurred "
                "in the previous cycle. Sanitary products are used for comfort and hygiene."
            ),
            "attempt_3": (
                "Choose 'menstruation'. The ring diagram shows menstruation as the pink/red quadrant "
                "at the 'top' of the circular diagram — day 1 of the cycle. "
                "It is designated 'Day 1' because it is the most visible, trackable event "
                "that marks where the cycle is counted from."
            )
        },
        "concept_reminder": (
            "Menstruation phase (days 1-5): uterine lining (endometrium) sheds → bleeding lasting 3-7 days. "
            "Why day 1? Because it is the most visible event, used to count the cycle start. "
            "The shedding occurs because progesterone dropped (no pregnancy from previous cycle), "
            "triggering the uterine lining to release. "
            "Sanitary pads, tampons or cups manage the flow hygienically. "
            "Menstruation is not impure — it is a biological resetting process. "
            "(ಋತುಚಕ್ರ = ಹೊಸ ಚಕ್ರದ ಆರಂಭ, ಶುದ್ಧ ಜೈವಿಕ ಪ್ರಕ್ರಿಯೆ!)"
        )
    },

    {
        "id": "menses_kn_q2",
        "challenge": (
            "Show the OVULATION phase (day 14). "
            "Explain why this is the most pivotal event in the entire menstrual cycle.\n\n"
            "(ಅಂಡೋತ್ಸರ್ಜನ ಹಂತ ತೋರಿಸಿ — ಇದೇ ಚಕ್ರದ ಅತಿ ಮುಖ್ಯ ಘಟನೆ!)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "ovulation"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'ovulation' as the initialState. "
                "The cycle diagram jumps to day 14 (green segment), the center shows 'Day 14 / Ovulation', "
                "and the phase text explains egg release from the ovary."
            ),
            "attempt_2": (
                "Set 'initialState=ovulation'. Day 14 is the single most significant day. "
                "The phase explains: a mature egg is released from the ovary. "
                "This is when pregnancy can occur if the egg is fertilised. The egg survives ~24 hours."
            ),
            "attempt_3": (
                "Choose 'ovulation'. The green dot in the legend and the ring confirm day 14 "
                "as the pivotal event. The phase info notes: some may feel mild discomfort "
                "(Mittelschmerz). The entire follicular phase (days 6-13) was building toward "
                "this event — egg maturation in the ovary."
            )
        },
        "concept_reminder": (
            "Ovulation (day 14): LH surge triggers release of a mature egg from the ovary. "
            "The egg travels down the fallopian tube. It is viable for approximately 24 hours. "
            "This is the ONLY time in the cycle that fertilisation can occur. "
            "The entire cycle revolves around this event: "
            "before it (days 1-13): preparation; after it (days 15-28): waiting for fertilisation. "
            "At the school level, the key fact is: ovulation = egg released = potential start of pregnancy. "
            "(ಅಂಡೋತ್ಪತ್ತಿ = ಚಕ್ರದ ಕೇಂದ್ರ ಘಟನೆ!)"
        )
    },

    {
        "id": "menses_kn_q3",
        "challenge": (
            "Show the LUTEAL phase (days 15-28). "
            "Explain what happens at the end of the luteal phase that causes the "
            "next menstruation to begin, restarting the whole cycle.\n\n"
            "(ಲ್ಯೂಟಿಯಲ್ ಹಂತ ತೋರಿಸಿ — ಚಕ್ರ ಮರಳಿ ಶುರುವಾಗಲು ಏನು ಆಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "luteal"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'luteal' as the initialState. "
                "The diagram shows days 15-28 (blue segment), and the phase info explains: "
                "the body prepares for potential pregnancy; if none, hormones drop."
            ),
            "attempt_2": (
                "Set 'initialState=luteal'. The phase text explains: if no fertilisation, "
                "progesterone and oestrogen levels fall at the end of day 28 — this hormone drop "
                "triggers the uterine lining to shed, starting day 1 of the next cycle."
            ),
            "attempt_3": (
                "Choose 'luteal'. All 14 days (15-28) are the largest phase of the cycle. "
                "PMS symptoms may occur in the last few days (days 25-28) as hormones drop. "
                "The key mechanism: progesterone drop → endometrium shedding → day 1 of new cycle. "
                "This makes the luteal phase the 'closing bracket' of every cycle."
            )
        },
        "concept_reminder": (
            "Luteal phase (days 15-28): after ovulation, the empty follicle becomes the corpus luteum, "
            "producing progesterone to prepare the uterine lining for implantation. "
            "If NO fertilisation: corpus luteum degenerates → progesterone and oestrogen drop → "
            "uterine lining sheds → day 1 of next cycle (menstruation restart). "
            "If a fertilised egg implants: corpus luteum continues producing progesterone → "
            "no menstruation (first sign of pregnancy). "
            "The cycle: menstruation → follicular → ovulation → luteal → menstruation... repeats monthly. "
            "(ಲ್ಯೂಟಿಯಲ್ ಕೊನೆ = ಗರ್ಭಧಾರಣೆ ಇಲ್ಲದಿದ್ದರೆ, ಮತ್ತೆ ಋತುಚಕ್ರ!)"
        )
    }
]



# =============================================================================
# EMOTIONAL CHANGES IN ADOLESCENCE SIMULATION
# ಕೌಮಾರದಲ್ಲಿ ಭಾವನಾತ್ಮಕ ಬದಲಾವಣೆಗಳು
# Science Chapter 6 – Growing Up (ಬೆಳೆಯುವಿಕೆ)
# =============================================================================
SIMULATIONS_KN["emotional_changes_kn"] = {
    "title": "ಕೌಮಾರದಲ್ಲಿ ಭಾವನಾತ್ಮಕ ಬದಲಾವಣೆಗಳು (Emotional Changes in Adolescence)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation6_emotional_changes_kn.html",
    "description": """
An interactive Kannada-language simulation exploring emotional changes during
adolescence through five real-life scenario-based exercises.

Students are presented with common adolescent situations (friend drift, exam
failure, puberty changes, parental rules, being teased) and asked to choose
the emotion they would feel, receiving validating feedback for every answer.

The simulation teaches:
- All emotions felt during adolescence are valid and normal
- Hormonal changes during puberty cause rapid mood swings
- Healthy coping strategies for difficult emotions (music, journaling, talking)
- Emotional intelligence: identifying and naming one's feelings
- When to seek help from trusted adults

The simulation UI, labels, and narrative are entirely in Kannada. State is
exposed via URL query string so the teaching agent can set the scenario directly.
""",
    "cannot_demonstrate": [
        "Specific neurological mechanisms behind hormonal mood changes",
        "Quantitative measurement of hormone levels",
        "Diagnosis or treatment of clinical mental health conditions",
        "Gender-specific emotional differences in detail"
    ],
    "initial_params": {
        "initialState": "scenario1",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Scenario State",
            "range": "scenario1, scenario2, scenario3, scenario4, scenario5, completed",
            "url_key": "initialState",
            "effect": (
                "Sets which scenario the simulation auto-loads into on page open.\n"
                "  'scenario1' → friend drifting away (default starting scenario)\n"
                "  'scenario2' → exam failure despite studying hard\n"
                "  'scenario3' → body changing faster/slower than peers\n"
                "  'scenario4' → parents' rules seem unfair vs friends\n"
                "  'scenario5' → being teased about appearance\n"
                "  'completed' → all scenarios explored, completion screen"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept explanation card (default)\n"
                "  false → hide the concept card (cleaner view for focused observation)"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Emotional Turbulence Is Normal in Adolescence",
            "description": (
                "Understanding why adolescents experience intense and rapidly changing "
                "emotions, and why these feelings are a normal part of growing up."
            ),
            "key_insight": (
                "Hormones released during puberty (especially oestrogen and testosterone) "
                "directly affect the brain's emotional centres. Feeling happy, sad, excited, "
                "or confused all within a single day is completely normal and temporary. "
                "These mood swings do not mean something is wrong with you."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Coping Strategies for Difficult Emotions",
            "description": (
                "Learning healthy, constructive ways to manage strong emotions such as "
                "sadness, anger, jealousy, and anxiety during adolescence."
            ),
            "key_insight": (
                "Healthy coping strategies include physical activity (sports, dance), "
                "creative outlets (music, art, journaling), deep breathing, and talking "
                "to a trusted person. Unhealthy responses like acting out or isolating "
                "worsen emotional wellbeing. Channelling energy positively builds resilience."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Recognising When to Seek Help",
            "description": (
                "Understanding the difference between normal emotional fluctuation and "
                "situations where adult support from parents, teachers, or counsellors is needed."
            ),
            "key_insight": (
                "While mood swings are normal, persistent sadness lasting weeks, inability "
                "to function, or feeling overwhelmed without relief are signals to reach out "
                "to a trusted adult. Asking for help is a sign of strength, not weakness. "
                "Parents, teachers, school counsellors, and doctors are appropriate sources of support."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# NUTRITION FOR ADOLESCENTS SIMULATION
# ಕೌಮಾರ ವಯಸ್ಕರಿಗೆ ಪೋಷಣೆ
# Science Chapter 6 – Growing Up (ಬೆಳೆಯುವಿಕೆ)
# =============================================================================
SIMULATIONS_KN["nutrition_adolescence_kn"] = {
    "title": "ಕೌಮಾರ ವಯಸ್ಕರಿಗೆ ಪೋಷಣೆ (Nutrition for Adolescents)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation7_nutrition_kn.html",
    "description": """
An interactive Kannada-language simulation teaching the four major nutrient
groups through a visual plate model: carbohydrates, proteins, vitamins &
minerals, and healthy fats.

Students tap plate sections or nutrient tabs to explore:
- Carbohydrates: the primary energy source; complex carbs preferred over simple sugars
- Proteins: muscle and tissue building blocks; extra demand during adolescent growth spurts
- Vitamins & Minerals: body regulators; iron (especially for girls post-menstruation),
  calcium for bone density, vitamin C for immunity
- Healthy Fats: brain development and long-term energy

A special panel highlights girls' additional nutritional needs (iron, B12, calcium).

The simulation UI is in Kannada. States are exposed via URL query strings
so the teaching agent can highlight specific nutrient groups.
""",
    "cannot_demonstrate": [
        "Caloric calculations or quantitative dietary planning",
        "Effects of malnutrition diseases in detail",
        "Specific food allergy or intolerance management",
        "Cooking methods and their effect on nutrient content"
    ],
    "initial_params": {
        "initialState": "carbs",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Nutrient Group",
            "range": "carbs, protein, veggies, fats",
            "url_key": "initialState",
            "effect": (
                "Selects which nutrient group is highlighted in the plate and info panel.\n"
                "  'carbs'   → carbohydrates highlighted (default) — energy source\n"
                "  'protein' → proteins highlighted — muscle and body building\n"
                "  'veggies' → vitamins & minerals highlighted — body regulators\n"
                "  'fats'    → healthy fats highlighted — brain development and energy"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Carbohydrates and Proteins: Energy and Growth",
            "description": (
                "Understanding how carbohydrates provide the primary fuel for adolescent "
                "activity and study, while proteins provide building blocks for the rapid "
                "muscle and organ growth that occurs during puberty."
            ),
            "key_insight": (
                "Carbohydrates are rapidly converted to glucose — the brain's only fuel. "
                "Complex carbs (whole grains, millets like ragi) release energy slowly, "
                "sustaining both physical activity and concentration. Proteins supply the "
                "amino acids needed to build and repair muscles and organs; adolescents "
                "need significantly more protein than children due to their growth spurt."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Vitamins, Minerals, and Special Adolescent Needs",
            "description": (
                "Exploring the role of micronutrients in adolescent health, with particular "
                "focus on iron (for girls), calcium (for bone strength), and vitamins."
            ),
            "key_insight": (
                "Iron is critical for haemoglobin production; girls lose iron through "
                "menstruation and must replenish it with spinach, dates, jaggery. "
                "Calcium builds peak bone density in the teenage years — a window that "
                "closes by age 20. Vitamin C from colourful vegetables enhances iron "
                "absorption. Each colour of vegetable/fruit provides different nutrients."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Healthy Fats and Balanced Diet Principles",
            "description": (
                "Understanding that fats are essential for brain development and vitamin "
                "absorption, and applying the principle of a balanced diet across all food groups."
            ),
            "key_insight": (
                "Healthy fats (nuts, seeds, fish, olive oil) supply essential fatty acids "
                "like omega-3 that are critical for brain development during adolescence. "
                "Fat-soluble vitamins (A, D, E, K) can only be absorbed in the presence of "
                "dietary fat. A balanced diet includes ALL four groups; skipping any group "
                "(e.g., eliminating carbs) creates deficiencies during this high-demand growth phase."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# PERSONAL HYGIENE IN ADOLESCENCE SIMULATION
# ಕೌಮಾರದಲ್ಲಿ ವೈಯಕ್ತಿಕ ಶುಚಿತ್ವ
# Science Chapter 6 – Growing Up (ಬೆಳೆಯುವಿಕೆ)
# =============================================================================
SIMULATIONS_KN["personal_hygiene_kn"] = {
    "title": "ಕೌಮಾರದಲ್ಲಿ ವೈಯಕ್ತಿಕ ಶುಚಿತ್ವ (Personal Hygiene in Adolescence)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation8_hygiene_kn.html",
    "description": """
An interactive Kannada-language simulation presenting a daily hygiene checklist
of 7 essential practices for adolescents, with educational tips for each item.

Students tap/check each hygiene item (daily bath, twice-daily brushing, clean
clothing, deodorant, face washing, handwashing, nail trimming) to mark it done.
Each check reveals a specific tip explaining WHY the practice matters.

A menstrual hygiene panel (for girls) explains sanitary product options:
disposable pads, reusable pads, and biodegradable options.

The simulation teaches:
- Why adolescents produce more sweat and oil than children (hormonal changes)
- Which hygiene habits prevent body odour, acne, and infection
- Correct techniques for each hygiene practice
- Menstrual hygiene management and available product choices
- That hygiene habits formed now persist throughout life

State is exposed via URL so the agent can demonstrate different completion levels.
""",
    "cannot_demonstrate": [
        "Specific dermatological treatment for severe acne",
        "Medical menstrual disorders (dysmenorrhoea, PCOS)",
        "Brand-specific product recommendations",
        "Detailed technique animation for brushing or bathing"
    ],
    "initial_params": {
        "initialState": "initial",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Checklist State",
            "range": "initial, all_complete",
            "url_key": "initialState",
            "effect": (
                "Sets the state of the hygiene checklist on page load.\n"
                "  'initial'      → empty checklist, 0/7 items done (default)\n"
                "  'all_complete' → all 7 items auto-checked with staggered animation, "
                "badge shows 'All Done!', final tip displayed"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Why Adolescents Need Increased Hygiene",
            "description": (
                "Understanding the biological reason why puberty dramatically increases "
                "the need for daily hygiene practices compared to childhood."
            ),
            "key_insight": (
                "Puberty hormones (androgens) dramatically increase the activity of sweat "
                "glands and sebaceous (oil) glands. More sweat + skin bacteria = body odour; "
                "more sebum = blocked pores = acne. These are not signs of uncleanliness — "
                "they are normal physiological changes. Daily bathing and face washing "
                "remove the bacterial substrate that causes odour and skin problems."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Daily Hygiene Checklist and Correct Practices",
            "description": (
                "Learning which hygiene habits are essential daily and understanding "
                "the specific purpose and correct method for each practice."
            ),
            "key_insight": (
                "The 7 core daily practices — bathing, brushing twice, clean clothes, "
                "deodorant, face washing, handwashing, and nail trimming — together prevent "
                "the three main hygiene-related problems of adolescence: body odour, acne, "
                "and infectious disease spread. Handwashing alone prevents more disease "
                "transmission than any other single hygiene measure."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Menstrual Hygiene Management",
            "description": (
                "Understanding the specific additional hygiene requirements during "
                "menstruation and the available product options for management."
            ),
            "key_insight": (
                "During menstruation, sanitary products must be changed every 4-6 hours "
                "to prevent bacterial growth and infection. Three types are available: "
                "disposable pads (most common, convenient), reusable cloth pads "
                "(eco-friendly, washable), and biodegradable pads (environmentally safe "
                "disposal). Government schemes provide free sanitary products in many schools. "
                "Each change should include washing the area with clean water."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# HEALTHY HABITS FOR ADOLESCENTS SIMULATION
# ಕೌಮಾರ ವಯಸ್ಕರಿಗೆ ಆರೋಗ್ಯಕರ ಅಭ್ಯಾಸಗಳು
# Science Chapter 6 – Growing Up (ಬೆಳೆಯುವಿಕೆ)
# =============================================================================
SIMULATIONS_KN["healthy_habits_kn"] = {
    "title": "ಕೌಮಾರ ವಯಸ್ಕರಿಗೆ ಆರೋಗ್ಯಕರ ಅಭ್ಯಾಸಗಳು (Healthy Habits for Adolescents)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter6_simulation9_healthy_habits_kn.html",
    "description": """
An interactive Kannada-language simulation presenting four essential healthy
habit categories for adolescents through a tabbed interface: physical activity,
sleep, social connections, and mental wellness.

Each tab shows a large animated icon, a science-based explanation, and a
four-point list of specific benefits of that habit during adolescence.

An online safety panel teaches responsible internet use: keeping personal
information private, avoiding strangers, respectful communication, and
reporting cyberbullying.

The simulation teaches:
- Physical activity: 60 minutes/day strengthens bones, improves mood, boosts focus
- Sleep: 8-10 hours/night supports growth hormone release and memory consolidation
- Social wellbeing: positive relationships build communication skills and emotional support
- Mental wellness: mindfulness, stress management, and knowing when to seek help
- Safe online behaviour as a component of holistic adolescent health

State is exposed via URL so the agent can demonstrate any of the four habit areas.
""",
    "cannot_demonstrate": [
        "Clinical treatment for anxiety or depression disorders",
        "Specific exercise or sleep schedules for individual students",
        "Detailed cyberbullying reporting procedures for specific platforms",
        "Quantitative measurement of mental health improvement"
    ],
    "initial_params": {
        "initialState": "exercise",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Habit Category",
            "range": "exercise, sleep, social, mental",
            "url_key": "initialState",
            "effect": (
                "Selects which healthy habit category is displayed in the info panel.\n"
                "  'exercise' → physical activity tab (default) — 60 min/day, builds strength\n"
                "  'sleep'    → quality sleep tab — 8-10 hrs/night, growth hormone release\n"
                "  'social'   → social connections tab — family and friend relationships\n"
                "  'mental'   → mental wellness tab — mindfulness and stress management"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Physical Activity and Sleep: The Foundation of Adolescent Health",
            "description": (
                "Understanding why regular exercise (minimum 60 min/day) and adequate "
                "sleep (8-10 hrs/night) are non-negotiable requirements for healthy "
                "adolescent development — not optional extras."
            ),
            "key_insight": (
                "Exercise during adolescence increases peak bone density (a lifetime asset), "
                "releases endorphins that reduce stress hormones, and improves concentration "
                "by increasing blood flow to the prefrontal cortex. "
                "Sleep is when the pituitary gland releases 70% of growth hormone; "
                "chronic sleep deprivation directly stunts physical growth and impairs "
                "memory consolidation — making late-night study counterproductive."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Social Connections and Communication Skills",
            "description": (
                "Exploring how positive social relationships with family and peers "
                "contribute to emotional wellbeing, and how communication skills "
                "developed during adolescence shape adult relationships."
            ),
            "key_insight": (
                "The adolescent brain is in a critical period for social learning. "
                "Positive peer interactions develop empathy, conflict resolution, and "
                "cooperation — skills that predict adult success more reliably than "
                "academic grades. Family connections provide the emotional safety net "
                "that allows adolescents to explore independence without anxiety. "
                "Quality over quantity: a few trusted relationships matter more than "
                "large social networks."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Mental Wellness and Safe Online Behaviour",
            "description": (
                "Understanding mental wellness practices that build resilience, and "
                "how responsible online behaviour protects adolescent mental health "
                "in the digital environment."
            ),
            "key_insight": (
                "Mental health is as important as physical health. Simple practices "
                "(5-minute mindful breathing, journaling, gratitude) measurably reduce "
                "cortisol (stress hormone) levels. Online safety is directly connected "
                "to mental health: cyberbullying, social comparison, and excessive "
                "screen time all elevate adolescent anxiety. Balanced screen time with "
                "outdoor activity and face-to-face interaction protects mental wellbeing."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# WATER CONSERVATION SIMULATION
# ಜಲ ಸಂರಕ್ಷಣೆ
# Science Chapter 7 – Water: Our Lifeline (ನೀರು: ನಮ್ಮ ಜೀವನಾಡಿ)
# =============================================================================
SIMULATIONS_KN["water_conservation_kn"] = {
    "title": "ಜಲ ಸಂರಕ್ಷಣೆ (Water Conservation)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation10_water_conservation_kn.html",
    "description": """
An interactive Kannada-language simulation demonstrating three water conservation
methods through animated visual models:

1. Rainwater Harvesting (ವರ್ಷಾಧಾರ ಸಂಗ್ರಹಣೆ): Rooftop collection system animation
   showing rain → gutters → pipes → storage tank, reducing dependence on groundwater.

2. Recharge Pit (ರಿಚಾರ್ಜ್ ಗುಂಡಿ): Cross-sectional view of a gravel-and-sand pit
   showing rainwater percolating downward through filter layers into the aquifer,
   replenishing groundwater that concrete surfaces would otherwise block.

3. Ice Stupa (ಐಸ್ ಸ್ತೂಪ): Ladakh's ingenious winter water storage — water sprayed
   at night freezes into a cone-shaped artificial glacier that slowly melts in
   summer, providing irrigation water precisely when needed.

The simulation teaches:
- Why groundwater is depleting (excess extraction, concrete blocking percolation)
- How each conservation method addresses a different aspect of the water crisis
- The connection between vegetation loss and reduced water retention
- Traditional and modern solutions that communities and households can implement

State is exposed via URL so the agent can demonstrate each conservation method.
""",
    "cannot_demonstrate": [
        "Quantitative calculation of water saved per system",
        "Detailed construction specifications for any system",
        "Groundwater flow dynamics and aquifer recharge rates",
        "Policy and legal frameworks for water conservation"
    ],
    "initial_params": {
        "initialState": "rwh",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Conservation Method",
            "range": "rwh, pit, stupa",
            "url_key": "initialState",
            "effect": (
                "Selects which water conservation method is displayed.\n"
                "  'rwh'   → rainwater harvesting animation (default) — roof → tank\n"
                "  'pit'   → recharge pit cross-section — water seeping into aquifer\n"
                "  'stupa' → ice stupa at night in Ladakh — artificial glacier formation"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Groundwater Depletion: The Problem",
            "description": (
                "Understanding why groundwater levels are falling across India and "
                "what human activities prevent natural aquifer recharge."
            ),
            "key_insight": (
                "Groundwater (stored in underground aquifers) is depleted by two forces: "
                "over-extraction (pumps removing water faster than rainfall can replace it) "
                "and blocked recharge (concrete, roads, and buildings prevent rainwater "
                "from percolating into the ground). Deforestation removes tree roots that "
                "previously held water in soil. The result: water tables falling 1-3 metres "
                "per year in many Indian cities, threatening agriculture and drinking water supply."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Rainwater Harvesting and Recharge Pits",
            "description": (
                "How collecting and redirecting rainwater at roof level (harvesting) "
                "and creating percolation pits (recharge) together address both supply "
                "and aquifer replenishment."
            ),
            "key_insight": (
                "Rainwater harvesting captures roof runoff before it flows away, "
                "storing it for direct use (gardening, washing) or filtered drinking water. "
                "A 100 m² roof in a region with 600 mm annual rainfall can collect ~60,000 litres/year. "
                "Recharge pits bypass impermeable concrete by channelling water through "
                "gravel and sand filters directly into the aquifer — the same mechanism "
                "that vegetation and open soil provide naturally."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Ice Stupas: Traditional Innovation for Water Security",
            "description": (
                "Exploring how Ladakh's ice stupa technique exemplifies traditional "
                "ecological knowledge solving a modern water scarcity problem."
            ),
            "key_insight": (
                "Ice stupas are artificial glaciers built in winter by spraying water "
                "upward at night — the spray freezes in the cold air and accumulates "
                "into a cone shape (like a Buddhist stupa) that can hold millions of litres. "
                "The conical shape minimises the surface-area-to-volume ratio, slowing melt. "
                "They release meltwater in spring and summer — exactly when farmers need "
                "water for sowing — months after natural glaciers would normally melt. "
                "This is traditional engineering adapted to modern climate challenges."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}


# =============================================================================
# EMOTIONAL CHANGES — QUIZ QUESTIONS
# 3 questions: explore scenario → understand emotional response → coping strategy
# =============================================================================
QUIZ_QUESTIONS_KN["emotional_changes_kn"] = [

    {
        "id": "emotions_kn_q1",
        "challenge": (
            "Show the first scenario where a friend starts spending time with "
            "others. Set the simulation to demonstrate the opening emotional "
            "situation that students most commonly face in adolescence.\n\n"
            "(ಮೊದಲ ಸನ್ನಿವೇಶ ತೋರಿಸಿ: ಸ್ನೇಹಿತ ದೂರವಾಗುತ್ತಾರೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "scenario1"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'scenario1' as the initialState. This loads the first scenario: "
                "your best friend starts spending more time with others. Explore how "
                "different emotions (sad, angry, jealous, confused) can arise in this situation."
            ),
            "attempt_2": (
                "Set 'initialState' to 'scenario1'. The simulation shows a common adolescent "
                "experience — friendship changes. Notice that every emotion selected receives "
                "a validating, non-judgmental response."
            ),
            "attempt_3": (
                "Choose 'scenario1' from the Simulation State dropdown. "
                "This is the foundational scenario demonstrating that emotional responses "
                "to social change are completely normal during adolescence."
            )
        },
        "concept_reminder": (
            "Adolescence brings rapid changes in social relationships as friends develop "
            "new interests. Feelings of sadness, jealousy, or confusion when friendships "
            "shift are completely normal. Hormonal fluctuations mean emotions can feel "
            "more intense than before puberty — this is biology, not a personal failing. "
            "(ಎಲ್ಲ ಭಾವನೆಗಳು ಸಹಜ — ಕೌಮಾರ್ಯದಲ್ಲಿ ಮನಸ್ಥಿತಿ ಬದಲಾವಣೆ ಸಾಮಾನ್ಯ!)"
        )
    },

    {
        "id": "emotions_kn_q2",
        "challenge": (
            "Now navigate to the scenario about body changes during puberty. "
            "Set the simulation to show the scenario where students compare "
            "their physical development with their peers.\n\n"
            "(ದೇಹ ಬದಲಾವಣೆ ಸನ್ನಿವೇಶ ತೋರಿಸಿ — ಸಹಪಾಠಿಗಳ ಜೊತೆ ಹೋಲಿಕೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "scenario3"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'scenario3' as the initialState. This is the scenario about body "
                "changes happening faster or slower than friends. It directly relates to "
                "the physical changes studied in the puberty topic."
            ),
            "attempt_2": (
                "Set 'initialState=scenario3'. The scenario: 'Your body is changing faster "
                "(or slower) than your friends.' Each emotion selected reveals the key message: "
                "everyone develops at their own pace — this is completely normal."
            ),
            "attempt_3": (
                "Choose 'scenario3'. This scenario teaches a critical message: puberty timing "
                "varies by 4-6 years between individuals, and no timeline is 'wrong'. "
                "Comparing oneself to peers' development pace often causes unnecessary anxiety."
            )
        },
        "concept_reminder": (
            "Puberty onset ranges from age 8 to 13 in girls and 9 to 14 in boys — a spread "
            "of 4-6 years. Someone who develops 'early' or 'late' compared to classmates is "
            "simply following their own genetic timeline. Every body has its own schedule. "
            "Anxiety about being different from peers is one of the most common emotional "
            "challenges of adolescence, but medically there is a very wide range of 'normal'. "
            "(ಪ್ರತಿಯೊಬ್ಬರ ದೇಹ ತನ್ನದೇ ಸಮಯದಲ್ಲಿ ಬದಲಾಗುತ್ತದೆ — ಇದು ಸಹಜ!)"
        )
    },

    {
        "id": "emotions_kn_q3",
        "challenge": (
            "Navigate to the scenario about being teased or bullied. Set the "
            "simulation to demonstrate how social humiliation affects adolescent "
            "emotions and what the healthy response is.\n\n"
            "(ಅಪಹಾಸ್ಯ ಸನ್ನಿವೇಶ ತೋರಿಸಿ — ಅನಾರೋಗ್ಯಕರ ಸಾಮಾಜಿಕ ಒತ್ತಡ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "scenario5"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'scenario5' as the initialState. This loads the scenario about "
                "being teased or made fun of. It teaches that a teaser's behaviour "
                "reflects their own insecurities, and that talking to a trusted adult "
                "is the appropriate response."
            ),
            "attempt_2": (
                "Set 'initialState=scenario5'. The scenario: 'Someone makes fun of how "
                "you look or something you did.' Notice that anger, anxiety, and sadness "
                "are all validated — but the advice consistently points to seeking support "
                "from a trusted person."
            ),
            "attempt_3": (
                "Choose 'scenario5'. This is the scenario that connects emotional health "
                "to the concept of seeking adult help when needed. The simulation's "
                "guidance: the teaser's behaviour is about their own problems, not your "
                "worth. Always tell a trusted adult if teasing becomes persistent."
            )
        },
        "concept_reminder": (
            "Teasing and bullying trigger real emotional pain — sadness, anger, anxiety, "
            "and confusion are all valid responses. Research shows that bullies often target "
            "perceived differences related to puberty (height, weight, development). "
            "The healthy response: walk away from the situation, tell a trusted adult, "
            "and remember that what others say does not define your worth. "
            "Persistent bullying that is not addressed can impact mental health long-term "
            "and should always be reported to a teacher, parent, or counsellor. "
            "(ಅಪಹಾಸ್ಯ ಸಹಿಸಬೇಡಿ — ಯಾರಾದರೂ ವಿಶ್ವಾಸಿ ವ್ಯಕ್ತಿಗೆ ಹೇಳಿ!)"
        )
    }
]


# =============================================================================
# NUTRITION FOR ADOLESCENTS — QUIZ QUESTIONS
# 3 questions: energy from carbs → growth from protein → micronutrients
# =============================================================================
QUIZ_QUESTIONS_KN["nutrition_adolescence_kn"] = [

    {
        "id": "nutrition_kn_q1",
        "challenge": (
            "Show the primary energy-giving nutrient group. Set the simulation "
            "to highlight the carbohydrate section of the balanced plate and "
            "demonstrate why energy foods are essential for adolescents.\n\n"
            "(ಶಕ್ತಿ ಕೊಡುವ ಪೋಷಕಾಂಶ ತೋರಿಸಿ: ಕಾರ್ಬೋಹೈಡ್ರೇಟ್)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "carbs"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'carbs' as the Nutrient Group. This highlights carbohydrates on "
                "the plate and shows the info panel explaining rice, roti, millets, and "
                "other complex carbs as the body's primary fuel source."
            ),
            "attempt_2": (
                "Set 'initialState=carbs'. Carbohydrates supply glucose — the only fuel "
                "your brain can directly use. Adolescents doing sports, studying, and "
                "growing need more carbohydrate energy than younger children or adults."
            ),
            "attempt_3": (
                "Choose 'carbs' from the Nutrient Group dropdown. Note the emphasis on "
                "COMPLEX carbohydrates (whole grains, millets like ragi) over simple sugars. "
                "Complex carbs release energy slowly for sustained concentration and activity."
            )
        },
        "concept_reminder": (
            "Carbohydrates are the body's preferred and fastest energy source. "
            "Glucose (broken down from carbs) is the sole fuel for the brain and the "
            "primary fuel for muscles during exercise. Adolescents experiencing rapid "
            "growth, active school days, and sports need substantially more carbohydrate "
            "relative to body weight than adults. Complex carbs (whole grains, millets, "
            "legumes) are vastly superior to refined sugars — they release energy slowly, "
            "preventing blood sugar spikes that cause fatigue and poor concentration. "
            "(ಕಾರ್ಬೋಹೈಡ್ರೇಟ್ = ದೇಹ ಮತ್ತು ಮೆದುಳಿಗೆ ಶಕ್ತಿ!)"
        )
    },

    {
        "id": "nutrition_kn_q2",
        "challenge": (
            "Demonstrate the body-building nutrient group. Set the simulation to "
            "highlight proteins and explain why adolescents need extra protein "
            "during their growth spurt.\n\n"
            "(ದೇಹ ನಿರ್ಮಾಣ ಪೋಷಕಾಂಶ ತೋರಿಸಿ: ಪ್ರೊಟೀನ್)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "protein"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'protein' as the Nutrient Group. This activates the protein section "
                "of the plate and shows the info panel about muscle building, tissue repair, "
                "and hormone synthesis using amino acids from protein."
            ),
            "attempt_2": (
                "Set 'initialState=protein'. During the adolescent growth spurt, the body "
                "is literally manufacturing new muscle fibres, bone matrix proteins, and "
                "organ tissue at a much higher rate than at any other time of life except infancy."
            ),
            "attempt_3": (
                "Choose 'protein'. Note the range of protein sources: chicken and fish "
                "(complete proteins), eggs and dairy (casein and whey), and plant sources "
                "like dal, legumes, nuts, and soya. Vegetarians can meet all protein "
                "requirements by combining different plant proteins."
            )
        },
        "concept_reminder": (
            "Proteins are made of amino acids — the actual building blocks of every cell. "
            "During the adolescent growth spurt (peak: ~13 years), the body adds more "
            "muscle and bone mass per year than at any later point in life. "
            "Protein requirements jump from ~0.9 g/kg body weight in childhood to "
            "~1.2-1.5 g/kg during the growth spurt. Protein also forms hormones like "
            "insulin and growth hormone, and enzymes for digestion and metabolism. "
            "A dal+rice combination provides all essential amino acids for vegetarians. "
            "(ಪ್ರೊಟೀನ್ = ಬೆಳವಣಿಗೆಯ ಸಮಯ ಹೆಚ್ಚು ಅಗತ್ಯ!)"
        )
    },

    {
        "id": "nutrition_kn_q3",
        "challenge": (
            "Highlight the vitamins and minerals section to demonstrate why "
            "micronutrients are especially critical for girls during adolescence, "
            "particularly iron and calcium.\n\n"
            "(ಹುಡುಗಿಯರ ವಿಶೇಷ ಪೋಷಕಾಂಶ ಅಗತ್ಯ ತೋರಿಸಿ: ಜೀವಸತ್ವ ಮತ್ತು ಖನಿಜ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "veggies"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'veggies' as the Nutrient Group. This activates the vitamins & "
                "minerals section showing colourful vegetables and their specific nutrients: "
                "spinach for iron, orange vegetables for vitamin A, citrus for vitamin C."
            ),
            "attempt_2": (
                "Set 'initialState=veggies'. The info panel explains that each vegetable "
                "colour provides different protective nutrients. The special needs panel "
                "below explains iron (for girls post-menstruation), B12, and calcium needs."
            ),
            "attempt_3": (
                "Choose 'veggies'. Look at both the info panel AND the special needs section "
                "below the sim card. Iron from spinach, dates, and jaggery is critical for "
                "girls once menstruation begins. Calcium from milk and green vegetables "
                "builds bone density during the critical teenage window."
            )
        },
        "concept_reminder": (
            "Micronutrients regulate every body process despite being needed in tiny amounts. "
            "Girls specifically need: "
            "(1) Iron — lost during menstruation, needed for haemoglobin; deficiency causes anaemia "
            "(fatigue, poor concentration). Sources: spinach, jaggery, dates, fortified cereals. "
            "(2) Calcium — peak bone density is built by age 20; the teenage years are a "
            "critical window. Sources: milk, yoghurt, paneer, green leafy vegetables. "
            "(3) Vitamin B12 — essential for nerve function and red blood cells; at risk in "
            "strict vegetarians. Sources: dairy, eggs, fortified foods. "
            "Colourful vegetables (eat the rainbow!) provide different vitamins — no single "
            "food supplies all micronutrients. "
            "(ಕಬ್ಬಿಣ ಮತ್ತು ಕ್ಯಾಲ್ಸಿಯಂ ಹುಡುಗಿಯರಿಗೆ ಅತ್ಯಂತ ಮುಖ್ಯ!)"
        )
    }
]


# =============================================================================
# PERSONAL HYGIENE — QUIZ QUESTIONS
# 3 questions: reason for hygiene → daily practices → menstrual hygiene
# =============================================================================
QUIZ_QUESTIONS_KN["personal_hygiene_kn"] = [

    {
        "id": "hygiene_kn_q1",
        "challenge": (
            "Show the default empty hygiene checklist to demonstrate the "
            "starting point — what a student's hygiene routine looks like "
            "before any habits have been established.\n\n"
            "(ಖಾಲಿ ಶುಚಿತ್ವ ಪಟ್ಟಿ ತೋರಿಸಿ — ಅಭ್ಯಾಸ ಇಲ್ಲದ ಆರಂಭಿಕ ಸ್ಥಿತಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "initial"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' as the Checklist State. This shows the empty checklist "
                "(0/7 done) — all 7 hygiene items are unchecked, representing a student "
                "who has not yet established these daily habits."
            ),
            "attempt_2": (
                "Set 'initialState=initial'. Notice the 7 hygiene practices listed: daily bath, "
                "brushing twice, clean clothes, deodorant, face wash, handwashing, nail trimming. "
                "All are unchecked in this starting state."
            ),
            "attempt_3": (
                "Choose 'initial'. This state sets up the contrast — compare it with "
                "'all_complete' to see the full difference between having no hygiene habits "
                "and following the complete daily routine."
            )
        },
        "concept_reminder": (
            "During childhood, body odour and skin oil production are minimal. "
            "Puberty changes this: androgens (hormones) dramatically activate sweat glands "
            "(apocrine glands under arms and groin) and sebaceous oil glands in skin. "
            "Without daily hygiene practices, bacteria break down sweat molecules into "
            "odorous compounds, and excess sebum blocks pores causing acne. "
            "These are not signs of being 'dirty' — they are unavoidable physiological changes "
            "that require a new, more active daily hygiene routine. "
            "(ಕೌಮಾರ್ಯದಲ್ಲಿ ಹೆಚ್ಚು ಬೆವರು ಮತ್ತು ತೈಲ — ದೈನಂದಿನ ಶುಚಿತ್ವ ಅಗತ್ಯ!)"
        )
    },

    {
        "id": "hygiene_kn_q2",
        "challenge": (
            "Demonstrate the complete daily hygiene routine by setting the simulation "
            "to show all 7 hygiene items checked off. This represents the ideal daily "
            "practice that prevents adolescent health problems.\n\n"
            "(ಎಲ್ಲ 7 ಶುಚಿತ್ವ ಅಭ್ಯಾಸ ಪೂರ್ಣ ತೋರಿಸಿ — ಸಂಪೂರ್ಣ ದೈನಂದಿನ ರೊಟೀನ್)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "all_complete"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'all_complete' as the Checklist State. This auto-checks all 7 "
                "hygiene items with a staggered animation, showing the badge '🎉 All Done!' "
                "and the final tip about nail hygiene."
            ),
            "attempt_2": (
                "Set 'initialState=all_complete'. Watch all 7 items get checked in sequence: "
                "bath → brushing → clean clothes → deodorant → face wash → handwashing → nails. "
                "Each check represents a habit that prevents a specific adolescent health problem."
            ),
            "attempt_3": (
                "Choose 'all_complete'. The 7 habits prevent: body odour, tooth decay and bad "
                "breath, bacterial skin infections, sustained body odour protection, acne, "
                "disease transmission, and nail-harboured dirt/bacteria respectively."
            )
        },
        "concept_reminder": (
            "Each of the 7 daily hygiene habits targets a specific problem: "
            "(1) Daily bath: removes apocrine sweat bacteria → prevents body odour "
            "(2) Brush ×2/day: removes plaque/bacteria → prevents cavities and bad breath "
            "(3) Clean clothes: bacteria in fabric = persistent odour → fresh clothes break cycle "
            "(4) Deodorant: neutralises odour compounds in underarm area "
            "(5) Face wash ×2-3: removes excess sebum + dead skin → prevents blocked pores/acne "
            "(6) Handwashing: single most effective disease-prevention measure known to medicine "
            "(7) Short nails: removes the main reservoir for dirt and pathogenic bacteria. "
            "Habits formed consistently in adolescence typically persist into adulthood. "
            "(ದೈನಂದಿನ 7 ಅಭ್ಯಾಸ = ಆರೋಗ್ಯ, ಆತ್ಮವಿಶ್ವಾಸ ಮತ್ತು ಸ್ವಚ್ಛತೆ!)"
        )
    },

    {
        "id": "hygiene_kn_q3",
        "challenge": (
            "Reset to the initial state and focus on the menstrual hygiene panel "
            "below the sim card. Set the simulation so that the menstrual hygiene "
            "content is visible for discussion.\n\n"
            "(ಋತುಕಾಲ ಶುಚಿತ್ವ ಮಾಹಿತಿ ತೋರಿಸಲು ಆರಂಭಿಕ ಸ್ಥಿತಿ ಹೊಂದಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "initial"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState=initial'. In this state, the full page is visible including "
                "the 'Menstrual Hygiene' panel below the checklist. This panel shows product "
                "options: disposable pads, reusable pads, and biodegradable options."
            ),
            "attempt_2": (
                "Choose 'initial'. The menstrual hygiene section is always visible; the "
                "checklist state controls only the top interactive section. The panel below "
                "covers changing frequency (every 4-6 hours), proper disposal, and spare "
                "products when going out."
            ),
            "attempt_3": (
                "Select 'initial' to view the complete page including the menstrual hygiene "
                "panel. The key rules: change products every 4-6 hours, wash with clean water "
                "at each change, wrap and dispose safely, carry extras when away from home."
            )
        },
        "concept_reminder": (
            "Menstrual hygiene management is an important component of adolescent health. "
            "Key practices: "
            "(1) Change sanitary products every 4-6 hours — longer intervals allow bacteria "
            "to multiply causing infections (bacterial vaginosis, UTIs). "
            "(2) Clean water wash at each change — reduces bacterial load. "
            "(3) Safe disposal — wrap in paper/plastic to prevent spread of bloodborne pathogens. "
            "(4) Three product types are available: disposable pads (most common), "
            "reusable cloth pads (environmental benefit, washable), and biodegradable pads. "
            "Government schemes provide free sanitary products in many Karnataka schools. "
            "Girls should never feel ashamed to ask school management for sanitary supplies. "
            "(ಋತುಕಾಲ ಶುಚಿತ್ವ — ಪ್ರತಿ 4-6 ಗಂಟೆಗೆ ಬದಲಾಯಿಸಿ!)"
        )
    }
]


# =============================================================================
# HEALTHY HABITS — QUIZ QUESTIONS
# 3 questions: physical activity → sleep → mental wellness/online safety
# =============================================================================
QUIZ_QUESTIONS_KN["healthy_habits_kn"] = [

    {
        "id": "habits_kn_q1",
        "challenge": (
            "Show the physical activity section to demonstrate why exercise is "
            "foundational for adolescent health and academic performance.\n\n"
            "(ಶಾರೀರಿಕ ಚಟುವಟಿಕೆ ತೋರಿಸಿ — ಕ್ರೀಡೆ ಮತ್ತು ವ್ಯಾಯಾಮದ ಪ್ರಾಮುಖ್ಯತೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "exercise"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'exercise' as the Habit Category. This shows the physical activity "
                "section with the pulsing football icon and 4 benefits: strengthens muscles "
                "and bones, improves mood and reduces stress, improves concentration and "
                "memory, increases energy levels."
            ),
            "attempt_2": (
                "Set 'initialState=exercise'. The WHO recommends 60 minutes of moderate-to-vigorous "
                "physical activity daily for adolescents. This can include sports, cycling, "
                "walking, dancing — anything that raises heart rate and breathing."
            ),
            "attempt_3": (
                "Choose 'exercise'. Notice the connection between exercise and academics: "
                "exercise increases blood flow to the prefrontal cortex (planning/concentration "
                "centre) and triggers BDNF release — a protein that literally grows new brain "
                "connections, improving learning capacity."
            )
        },
        "concept_reminder": (
            "Physical activity at 60 min/day during adolescence delivers multiple health benefits: "
            "(1) Bone density: weight-bearing exercise (running, jumping) stimulates osteoblasts "
            "to deposit calcium — building peak bone mass that protects against fractures/osteoporosis later. "
            "(2) Mood regulation: exercise releases endorphins and reduces cortisol — the same "
            "effect as antidepressant medication, without side effects. "
            "(3) Academic performance: 20 minutes of aerobic exercise has been shown to improve "
            "attention, working memory, and problem-solving for 2-3 hours afterward. "
            "(4) Sleep quality: physically tired adolescents fall asleep faster and sleep more deeply. "
            "(ದಿನಕ್ಕೆ 60 ನಿಮಿಷ ವ್ಯಾಯಾಮ — ದೇಹ, ಮನಸ್ಸು ಮತ್ತು ಓದಿಗೆ ಸಹಾಯ!)"
        )
    },

    {
        "id": "habits_kn_q2",
        "challenge": (
            "Set the simulation to show the sleep section. Demonstrate why "
            "adolescents need 8-10 hours of sleep and what happens when they "
            "consistently sleep less.\n\n"
            "(ನಿದ್ರೆ ವಿಭಾಗ ತೋರಿಸಿ — ಕೌಮಾರ್ಯದಲ್ಲಿ ಸಾಕಷ್ಟು ನಿದ್ರೆ ಏಕೆ ಅಗತ್ಯ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "sleep"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'sleep' as the Habit Category. This shows the sleep section with "
                "4 benefits: supports growth hormone release, improves learning and memory, "
                "strengthens immune system, and provides better emotional control."
            ),
            "attempt_2": (
                "Set 'initialState=sleep'. The recommended 8-10 hours for adolescents is "
                "significantly more than the 7-8 hours adults need. The adolescent brain is "
                "undergoing active structural remodelling that requires deep sleep to complete."
            ),
            "attempt_3": (
                "Choose 'sleep'. The key scientific insight is that 70% of growth hormone "
                "is released during the first hours of deep sleep. Consistently sleeping "
                "6 hours instead of 8 effectively reduces growth hormone production — "
                "directly impacting height and physical development."
            )
        },
        "concept_reminder": (
            "Adolescents need 8-10 hours of sleep — more than adults — for three critical reasons: "
            "(1) Growth hormone: the pituitary gland releases ~70% of daily growth hormone "
            "during the first 3 hours of deep sleep. Chronic sleep deprivation literally "
            "stunts height and muscle development. "
            "(2) Memory consolidation: during sleep, the hippocampus transfers learning from "
            "short-term to long-term memory storage. Students who sleep 8 hours after studying "
            "retain 30-40% more than those who stay up late. "
            "(3) Emotional regulation: the prefrontal cortex (emotional control centre) resets "
            "during sleep. Chronically sleep-deprived adolescents show increased aggression, "
            "anxiety, and impulsive decision-making. "
            "(8-10 ಗಂಟೆ ನಿದ್ರೆ = ಬೆಳವಣಿಗೆ + ಕಲಿಕೆ + ಭಾವನಾ ನಿಯಂತ್ರಣ!)"
        )
    },

    {
        "id": "habits_kn_q3",
        "challenge": (
            "Show the mental wellness section to demonstrate mindfulness practices "
            "and connect mental health habits to better academic and social outcomes.\n\n"
            "(ಮಾನಸಿಕ ಆರೋಗ್ಯ ವಿಭಾಗ ತೋರಿಸಿ — ಒತ್ತಡ ನಿರ್ವಹಣೆ ಮತ್ತು ಯೋಗಕ್ಷೇಮ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "mental"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'mental' as the Habit Category. This shows the mental wellness "
                "section with benefits including stress/anxiety reduction, improved focus, "
                "increased self-confidence, and better decision-making."
            ),
            "attempt_2": (
                "Set 'initialState=mental'. Mental wellness practices include mindfulness, "
                "gratitude journalling, deep breathing, and setting achievable daily goals. "
                "These practices work by lowering cortisol (stress hormone) levels."
            ),
            "attempt_3": (
                "Choose 'mental'. Look also at the online safety tips panel (below the "
                "habit-info panel) — cyberbullying, social comparison on social media, and "
                "excessive screen time are the main digital threats to adolescent mental health."
            )
        },
        "concept_reminder": (
            "Mental health is physical health — the brain is an organ that needs care. "
            "Evidence-based mental wellness practices for adolescents: "
            "(1) Mindful breathing (5 min/day): activates the parasympathetic nervous system, "
            "measurably lowering heart rate and cortisol within minutes. "
            "(2) Gratitude journalling: trains the brain to notice positive events, "
            "counteracting the adolescent brain's natural negativity bias. "
            "(3) Digital balance: social media use >3 hrs/day is linked to increased anxiety, "
            "depression, and body image issues in adolescents. Setting screen time limits "
            "and taking regular offline breaks protects mental wellbeing. "
            "(4) Knowing when to seek help: persistent low mood, withdrawal from friends, "
            "loss of interest in activities, or inability to concentrate for >2 weeks "
            "are signs to talk to a trusted adult. "
            "(ಮಾನಸಿಕ ಆರೋಗ್ಯ = ಶಾರೀರಿಕ ಆರೋಗ್ಯದಷ್ಟೇ ಮುಖ್ಯ!)"
        )
    }
]


# =============================================================================
# WATER CONSERVATION — QUIZ QUESTIONS
# 3 questions: problem (depletion) → solution 1 (RWH) → solution 2 (recharge pit)
# =============================================================================
QUIZ_QUESTIONS_KN["water_conservation_kn"] = [

    {
        "id": "water_kn_q1",
        "challenge": (
            "Show the rainwater harvesting animation to demonstrate how rooftop "
            "collection systems capture and store rain that would otherwise be lost "
            "as surface runoff.\n\n"
            "(ಮಳೆನೀರು ಸಂಗ್ರಹಣೆ ತೋರಿಸಿ — ಛಾವಣಿ ಮೇಲಿನ ನೀರು ಸಂಗ್ರಹ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "rwh"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'rwh' as the Conservation Method. This shows the animated rainwater "
                "harvesting system: rain falling on the roof, gutters collecting it, a pipe "
                "directing it to a storage tank filling up. The info panel explains reducing "
                "groundwater dependence."
            ),
            "attempt_2": (
                "Set 'initialState=rwh'. The animation shows the complete sequence: "
                "🌧️ rain → roof collection → gutter → downpipe → storage tank (ಭಂಡಾರ ಟ್ಯಾಂಕ್). "
                "This water can be used for gardens, cleaning, or treated for drinking."
            ),
            "attempt_3": (
                "Choose 'rwh'. The info panel mentions that harvested water reduces dependence "
                "on groundwater. A 100 m² roof in a region receiving 600mm annual rainfall "
                "can collect approximately 60,000 litres — enough for a family's non-drinking "
                "needs for months."
            )
        },
        "concept_reminder": (
            "Rainwater harvesting (RWH) intercepts rain before it runs off as surface water. "
            "The system components: roof (collection surface) → gutters (channelling) → "
            "first-flush diverter (discards first dirty rain) → filter → storage tank. "
            "Benefits: reduces groundwater extraction, lowers water bills, provides water "
            "security during droughts, and reduces urban flooding by slowing runoff. "
            "In India, many states (including Karnataka) now legally mandate RWH systems "
            "in new buildings above a certain size. "
            "The water can directly replace groundwater for irrigation, toilet flushing, "
            "and washing — or be further treated for drinking. "
            "(ಮಳೆನೀರು ಸಂಗ್ರಹಣೆ = ಭೂಜಲ ಉಳಿಸುವ ಮೊದಲ ಹೆಜ್ಜೆ!)"
        )
    },

    {
        "id": "water_kn_q2",
        "challenge": (
            "Demonstrate the recharge pit method to show how water is directed "
            "back into the ground to replenish the aquifer — addressing groundwater "
            "depletion at its source.\n\n"
            "(ರಿಚಾರ್ಜ್ ಗುಂಡಿ ತೋರಿಸಿ — ಭೂಜಲ ಮರು ತುಂಬಿಸುವ ವಿಧಾನ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "pit"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'pit' as the Conservation Method. This shows the recharge pit "
                "cross-section: rain from above, water entering the pit, percolating through "
                "gravel and sand layers, seeping into the ground. Arrows show the downward "
                "direction of water movement."
            ),
            "attempt_2": (
                "Set 'initialState=pit'. The recharge pit cross-section shows three filtering "
                "layers: water → gravel (coarse filter) → sand (fine filter) → aquifer. "
                "The info panel explains that this bypasses impermeable concrete surfaces "
                "that prevent natural percolation."
            ),
            "attempt_3": (
                "Choose 'pit'. The key distinction from rainwater harvesting: RWH captures "
                "water for use, while recharge pits return water TO the aquifer — addressing "
                "the depletion problem directly by artificially replacing natural percolation "
                "that concrete and buildings have blocked."
            )
        },
        "concept_reminder": (
            "A recharge pit solves the percolation problem created by urbanisation. "
            "Normally, rain soaks into open soil and slowly percolates down to the water table. "
            "When soil is covered by concrete (buildings, roads, pavements), this path is blocked — "
            "rain becomes surface runoff into drains and eventually the sea, never reaching the aquifer. "
            "A recharge pit creates an artificial pathway: a deep hole filled with alternating layers "
            "of gravel (coarse: removes large particles) and sand (fine: removes smaller impurities) "
            "acts as a biological plus mechanical filter. "
            "Water percolating through emerges clean enough to enter the aquifer without contaminating "
            "the groundwater table. This is the most direct method for replenishing depleted aquifers. "
            "(ರಿಚಾರ್ಜ್ ಗುಂಡಿ = ಭೂಜಲ ಮರು ತುಂಬಿಸುವ ನೇರ ಮಾರ್ಗ!)"
        )
    },

    {
        "id": "water_kn_q3",
        "challenge": (
            "Show the ice stupa method to demonstrate the innovative traditional "
            "solution used in Ladakh for water storage — an example of engineering "
            "using natural processes without any machinery.\n\n"
            "(ಐಸ್ ಸ್ತೂಪ ತೋರಿಸಿ — ಲಡಾಕ್‌ನ ಸಾಂಪ್ರದಾಯಿಕ ಜಲ ಸಂರಕ್ಷಣೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "stupa"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'stupa' as the Conservation Method. This shows the ice stupa scene: "
                "a night sky (moon), a mountain backdrop, the conical ice formation, and a "
                "spray of water at the base. The label reads '❄️ ಐಸ್ ಸ್ತೂಪ - Ladakh'."
            ),
            "attempt_2": (
                "Set 'initialState=stupa'. The info panel explains: water is sprayed upward "
                "at night in winter, freezing in the cold air to build a cone-shaped "
                "artificial glacier. This slowly melts in summer to provide irrigation "
                "water when farmers need it most."
            ),
            "attempt_3": (
                "Choose 'stupa'. The genius of the cone shape: a cone has the lowest possible "
                "surface-area-to-volume ratio among simple 3D shapes. Less exposed surface "
                "means slower melting in sunlight — preserving the water store for longer. "
                "This is traditional geometry applied to water conservation."
            )
        },
        "concept_reminder": (
            "Ice stupas are artificial glaciers — a traditional innovation adapted to modern "
            "climate change challenges in Ladakh, developed by engineer Sonam Wangchuk. "
            "Process: in winter, pipes carry glacial meltwater to lower altitudes; "
            "a sprinkler sprays water upward at night; the spray freezes in sub-zero temperatures "
            "and accumulates into a conical shape (stupa = Buddhist dome structure). "
            "The cone shape (minimal surface area / volume ratio) slows solar melting. "
            "A single ice stupa can hold 5-10 million litres, melting gradually through spring "
            "and summer — providing water for sowing crops in April-June, months before "
            "natural glacier melt water would normally be available. "
            "This demonstrates that traditional ecological knowledge often contains elegant "
            "engineering solutions that modern technology is now rediscovering. "
            "(ಐಸ್ ಸ್ತೂಪ = ಸಾಂಪ್ರದಾಯಿಕ ವಿಜ್ಞಾನ × ಆಧುನಿಕ ಅಗತ್ಯ!)"
        )
    }
]


SIMULATIONS_KN["heat_sources_kn"] = {
    "title": "ಉಷ್ಣದ ಮೂಲಗಳು (Heat Sources – Regional Differences)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation1_heat_sources_kn.html",
    "description": """
An interactive Kannada-language simulation exploring how the Sun as Earth's primary
heat source creates different temperature conditions across India's regions:

1. Kerala (ಕೇರಳ): Tropical coastal region near the equator — hot and humid year-round
   with temperatures 25–32°C; short direct sunlight path, high sea moisture.

2. Delhi (ದೆಹಲಿ): Continental interior region — extreme temperature variation 5–45°C;
   far from moderating sea influence, clear dry air for rapid heating/cooling.

3. Sikkim (ಸಿಕ್ಕಿಂ): High Himalayan altitude region — cool temperatures 5–20°C;
   elevation reduces atmospheric heating, lower oxygen density.

The simulation teaches:
- Sun is the ultimate source of all heat energy on Earth
- Distance from equator (latitude) affects solar angle and heating intensity
- Altitude: every 1000m rise reduces temperature by ~6°C (lapse rate)
- Proximity to sea: moderates temperature extremes (high specific heat of water)

State is exposed via URL so the agent can demonstrate each region.
""",
    "cannot_demonstrate": [
        "Precise meteorological calculations or seasonal forecast data",
        "Historical climate data or temperature records",
        "Atmospheric pressure differences between regions",
        "Ocean current effects on coastal temperatures"
    ],
    "initial_params": {
        "initialState": "kerala",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Region / ಪ್ರದೇಶ",
            "range": "kerala, delhi, sikkim",
            "url_key": "initialState",
            "effect": (
                "Selects which Indian region's temperature profile is shown.\n"
                "  'kerala' → tropical coastal (25-32°C, near equator, high humidity) [default]\n"
                "  'delhi'  → continental interior (5-45°C, extreme variation, dry)\n"
                "  'sikkim' → high altitude Himalayan (5-20°C, cold mountain climate)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Sun as Earth's Primary Heat Source",
            "description": (
                "Understanding that solar radiation is the ultimate driver of all "
                "temperature differences observed on Earth's surface."
            ),
            "key_insight": (
                "The Sun radiates energy as electromagnetic waves (light and infrared). "
                "Earth's surface absorbs this and re-radiates as heat. The amount absorbed "
                "depends on: (1) angle of sunlight — perpendicular rays carry more energy "
                "per unit area; (2) duration of daylight; (3) surface type (land vs water). "
                "Kerala near the equator receives nearly perpendicular sun rays year-round, "
                "making it consistently hot. Sikkim's high altitude means the atmosphere is "
                "thinner, absorbing less heat even though it receives similar solar radiation."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Latitude, Altitude and Coastal Proximity",
            "description": (
                "How three geographic factors — latitude, altitude, and distance from "
                "the sea — explain India's extreme regional temperature differences."
            ),
            "key_insight": (
                "Latitude (distance from equator): Near the equator, Sun is overhead → "
                "heating is intense and direct. Farther north/south, Sun's rays hit at "
                "an angle → same energy spread over larger area → less intense heating. "
                "Altitude: Atmosphere is thinner at height → less air to trap heat → "
                "temperature drops ~6°C per 1000m rise (environmental lapse rate). "
                "Coastal proximity: Water has high specific heat capacity — it heats and "
                "cools slowly. Coastal areas like Kerala have moderate temperatures; "
                "continental interiors like Delhi have extreme hot summers and cold winters."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Delhi's Extreme Temperature Variation",
            "description": (
                "Why landlocked continental interiors experience extreme seasonal "
                "temperature swings compared to coastal or high-altitude regions."
            ),
            "key_insight": (
                "Delhi's temperature extremes (5°C in winter, 45°C in summer) result from "
                "its continental location: no nearby ocean to moderate temperatures, "
                "dry air heats and cools rapidly, clear skies allow maximum solar gain "
                "in summer and maximum heat loss at night in winter. "
                "Compare: Mumbai (coastal, near Delhi's latitude) has 19-33°C year-round. "
                "The same latitude, but the Arabian Sea moderates Mumbai's temperature. "
                "This shows coastal proximity is as important as latitude for daily "
                "and seasonal temperature patterns."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["conduction_experiment_kn"] = {
    "title": "ಉಷ್ಣ ವಾಹಕತೆ ಪ್ರಯೋಗ (Heat Conduction Experiment)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation2_conduction_kn.html",
    "description": """
An interactive Kannada-language simulation demonstrating heat conduction through
a metal strip with wax-pinned pins at measured distances from a flame:

The experiment shows 4 pins held by wax at increasing distances (3, 6, 9, 12 cm)
from a heat source. As heat travels along the metal strip by conduction, pins
closer to the flame drop first, recording their fall times.

Three heat intensity levels are available:
- Low flame: pins drop slowly over 4–10 seconds
- Medium flame: pins drop at moderate rate over 2–6.5 seconds (default)
- High flame: pins drop rapidly over 1–4 seconds

A particle view shows molecular vibration: hot particles vibrate faster and
transfer energy to neighboring cooler particles without moving themselves.

The simulation teaches:
- Conduction transfers heat through solids from hot to cold end
- Rate of conduction increases with higher temperature difference
- Particles vibrate in place (do not move) — only energy is transferred
- Closer pins fall first — demonstrating the direction of heat flow

State is exposed via URL so the agent can demonstrate different heat intensities.
""",
    "cannot_demonstrate": [
        "Specific thermal conductivity values (k) for different materials",
        "Fourier's law calculations or quantitative heat transfer",
        "Effects of cross-sectional area on conduction rate",
        "Conduction through non-metal materials (wood, plastic comparison)"
    ],
    "initial_params": {
        "initialState": "medium",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Flame Intensity / ಜ್ವಾಲೆ ತೀವ್ರತೆ",
            "range": "low, medium, high",
            "url_key": "initialState",
            "effect": (
                "Sets the flame intensity before auto-starting the experiment.\n"
                "  'low'    → slow heat (pins drop at 4, 6, 8, 10 seconds)\n"
                "  'medium' → moderate heat (pins drop at 2, 3.5, 5, 6.5 seconds) [default]\n"
                "  'high'   → intense heat (pins drop at 1, 2, 3, 4 seconds)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Conduction: Energy Transfer Through Particle Vibration",
            "description": (
                "Understanding the molecular mechanism of heat conduction in solids "
                "and why particles vibrate but do not migrate during this process."
            ),
            "key_insight": (
                "In conduction, heat energy is transferred through a solid by particle "
                "vibration. When the metal strip's atoms near the flame receive heat energy, "
                "they vibrate faster (higher kinetic energy). These vibrating atoms collide "
                "with adjacent atoms, transferring kinetic energy to them. Those atoms then "
                "vibrate faster and transfer energy to their neighbors. "
                "Crucially: the atoms themselves do NOT move — only energy passes along. "
                "This is why metals are good conductors (tightly packed, strongly bonded "
                "atoms) while gases are poor conductors (atoms too far apart to collide often). "
                "This is also why a metal spoon in hot tea burns your hand quickly!"
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Direction of Heat Flow: Hot to Cold",
            "description": (
                "Why heat always spontaneously flows from higher to lower temperature "
                "regions, and how the pin drop sequence demonstrates this."
            ),
            "key_insight": (
                "Heat always flows from high temperature to low temperature — never the "
                "reverse (second law of thermodynamics). In the experiment, pin 1 (3 cm "
                "from flame) drops first because it reaches the wax melting temperature "
                "before pins further away. Pin 4 (12 cm) drops last because heat must "
                "travel the greatest distance. The time difference between pin drops "
                "shows that heat conduction takes time — it is not instantaneous. "
                "Higher flame intensity (higher temperature difference) means faster "
                "heat flow — demonstrating that temperature gradient drives conduction rate."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Effect of Temperature on Conduction Rate",
            "description": (
                "How increasing the temperature difference between heat source and "
                "material affects the speed of heat conduction."
            ),
            "key_insight": (
                "Compare pin drop times at low vs high flame: High flame makes ALL pins "
                "fall faster, showing that greater temperature difference (ΔT) drives "
                "faster conduction. This is Fourier's Law in action: heat flow rate is "
                "proportional to the temperature gradient. "
                "Real-world application: cooking on high heat vs low heat, industrial "
                "heat treatment of metals, why insulation reduces heat flow (reduces ΔT "
                "across the insulating material). "
                "The metal strip in this experiment simulates materials like metal cooking "
                "utensils, radiators, and heat sinks in electronics."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["thermal_conductors_kn"] = {
    "title": "ಉಷ್ಣ ವಾಹಕಗಳು ಮತ್ತು ಅವಾಹಕಗಳು (Thermal Conductors and Insulators)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation3_conductors_insulators_kn.html",
    "description": """
An interactive Kannada-language simulation comparing heat conduction rates across
four materials using a visual race where heat progresses as a coloured bar:

Materials in the race:
- Metal (ಲೋಹ): Very fast conductor, speed factor 5x — wins every race
- Wood (ಮರ): Poor conductor, speed 0.8x — slow heat transfer
- Glass (ಗಾಜು): Poor conductor, speed 1.0x — slightly better than wood
- Plastic (ಪ್ಲಾಸ್ಟಿಕ್): Very poor conductor, speed 0.6x — slowest of all

Two modes available:
- Race Mode: All four materials race simultaneously; badges awarded 1st–4th
- Compare Mode: Side-by-side comparison view for analysis

Each material can be tapped/clicked to see an explanation of why it conducts
well or poorly (free electrons in metals vs air pockets in wood/plastic).

The simulation teaches:
- Metals are excellent thermal conductors (free electrons transfer energy)
- Non-metals (wood, plastic, glass) are thermal insulators
- This is why cooking pots are metal but handles are plastic or wood
- Insulators slow heat flow — used in building insulation, clothing, thermos flasks

State is exposed via URL so the agent can demonstrate race vs compare mode.
""",
    "cannot_demonstrate": [
        "Precise thermal conductivity values (W/m·K) for materials",
        "Fourier's law quantitative calculations",
        "Effect of material thickness on insulation",
        "Comparison of different metals (copper vs iron vs aluminium)"
    ],
    "initial_params": {
        "initialState": "race",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Mode / ಮೋಡ್",
            "range": "race, compare",
            "url_key": "initialState",
            "effect": (
                "Selects the display mode for the conductors/insulators comparison.\n"
                "  'race'    → race mode — all materials compete simultaneously [default]\n"
                "  'compare' → compare mode — side-by-side analysis view"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Why Metals are Good Thermal Conductors",
            "description": (
                "Understanding the atomic structure of metals that makes them "
                "exceptional heat conductors compared to non-metals."
            ),
            "key_insight": (
                "Metals have a unique atomic structure: their outermost electrons are "
                "loosely bound and can move freely throughout the metal (called 'free electrons' "
                "or 'sea of electrons'). When one end of a metal is heated, these free electrons "
                "gain kinetic energy and move rapidly through the metal, transferring their "
                "energy to cold regions almost instantly. Metal atoms also vibrate and pass "
                "energy, but the free electron mechanism makes metals far superior conductors "
                "than non-metals. This explains why copper, aluminium, and iron heat up quickly "
                "and why metal handles on cooking pots become dangerously hot."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Why Wood, Glass and Plastic are Insulators",
            "description": (
                "How the molecular structure of non-metals traps air and blocks "
                "the electron-flow mechanisms that make metals good conductors."
            ),
            "key_insight": (
                "Non-metals lack free electrons — their electrons are tightly bound to "
                "individual atoms. Heat can only transfer through atomic vibration, which "
                "is slow. Wood is especially poor because it has microscopic air pockets "
                "in its cellular structure (air is among the worst conductors — it has "
                "no free electrons and molecules are too far apart for efficient vibration "
                "transfer). Plastic polymers have long hydrocarbon chains that vibrate "
                "slowly. Glass conducts slightly better than wood but still far slower "
                "than any metal. This is why: cooking pot bodies = metal (conducts heat "
                "to food); handles = plastic/wood (insulates hand from heat)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Real-World Applications of Conductors and Insulators",
            "description": (
                "Applying knowledge of thermal conductors and insulators to understand "
                "everyday objects and engineering designs."
            ),
            "key_insight": (
                "Engineers choose materials based on whether they WANT heat to flow or not. "
                "WANT heat flow: cooking pots (metal for even heating), car engine blocks "
                "(metal for heat dissipation), heat sinks in electronics (metal fins). "
                "WANT to block heat: building insulation (glass wool, hollow bricks with "
                "trapped air), thermos flask (vacuum — no medium for conduction), oven mitts "
                "(thick cotton/silicone with air pockets), winter clothing (wool traps air). "
                "The race shows metal wins by a huge margin — important for cooking and "
                "electronics, but we also need insulators to control where heat goes."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["convection_kn"] = {
    "title": "ಸಂವಹನ ಪ್ರವಾಹಗಳು (Convection Currents)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation4_convection_kn.html",
    "description": """
An interactive Kannada-language simulation demonstrating convection currents in
both water (liquid) and air (gas) modes:

Water Mode (💧 ನೀರು):
- A beaker with 6 colored particles showing rising (hot) and falling (cool) movement
- Flame heats the bottom; particles near heat turn red/orange and rise
- Cool blue particles at top sink to replace them
- Current arrows show the circular convection loop
- Temperature slider animates heating from 0-100°C

Air Mode (💨 ಗಾಳಿ):
- Room with heater showing warm air rising, cool air filling in from sides
- Air particles animate in rising/falling paths

Interactive features:
- Toggle heat on/off to start/stop convection
- Tap individual particles to track their path and state
- Show/hide circulation arrows
- Switch between water and air modes

The simulation teaches:
- Convection occurs in fluids (liquids and gases) — NOT in solids
- Hot fluid expands → becomes less dense → rises
- Cool fluid is denser → sinks to replace rising hot fluid
- Creates continuous circular convection currents

State is exposed via URL so the agent can demonstrate water vs air convection.
""",
    "cannot_demonstrate": [
        "Quantitative convection coefficient calculations",
        "Turbulent vs laminar flow distinctions",
        "Natural vs forced convection differences",
        "Convection in space (microgravity — why it does not occur)"
    ],
    "initial_params": {
        "initialState": "water",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Medium / ಮಾಧ್ಯಮ",
            "range": "water, air",
            "url_key": "initialState",
            "effect": (
                "Selects which fluid medium demonstrates convection.\n"
                "  'water' → water beaker with particle animation, flame heating base [default]\n"
                "  'air'   → room with heater, warm air rising and cool air circulating"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Convection: Heat Transfer Through Fluid Movement",
            "description": (
                "Understanding how convection differs from conduction by involving "
                "actual movement of the heated matter itself."
            ),
            "key_insight": (
                "Convection transfers heat through the physical movement of a fluid (liquid "
                "or gas). Unlike conduction (where particles vibrate in place), in convection "
                "the heated particles themselves move, carrying their kinetic energy with them. "
                "When water at the bottom of the beaker is heated: molecules gain energy → "
                "move faster → spread apart → become less dense → buoyancy force pushes them "
                "upward. The cooler, denser water above sinks to replace them. This creates a "
                "continuous circular current called a convection current. "
                "Key difference from conduction: in conduction, energy moves through stationary "
                "matter; in convection, the matter itself moves and carries energy."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Density Change Drives Convection",
            "description": (
                "How temperature-induced density changes create the buoyancy forces "
                "that drive convection currents in fluids."
            ),
            "key_insight": (
                "The driving force of convection is density difference caused by temperature. "
                "Density = mass / volume. When you heat a fluid: mass stays the same, but "
                "volume increases (thermal expansion) → density decreases. "
                "Less dense (hot) fluid floats on denser (cool) fluid — the same principle "
                "as why oil floats on water or hot air balloons rise. "
                "As hot fluid rises, it moves away from heat source and cools → becomes denser "
                "→ sinks. This creates the convection loop seen in the simulation. "
                "Important: Convection requires gravity to separate denser and less dense fluid. "
                "In space (weightlessness), convection does not occur — astronauts cannot use "
                "convection ovens and food heats unevenly."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Convection in Air: Room Heating and Weather",
            "description": (
                "Applying convection principles to explain how room heaters work "
                "and how large-scale atmospheric convection drives weather patterns."
            ),
            "key_insight": (
                "Room heater: heater warms nearby air → warm air rises (lighter) → "
                "spreads across ceiling → cools → sinks along opposite wall → flows "
                "back to heater along floor → heated again. This convection loop gradually "
                "warms the entire room. Placing the heater at floor level maximises this "
                "circulation (if placed at ceiling, hot air just stays at top). "
                "Atmospheric scale: the Sun heats equatorial air more than polar air. "
                "Warm equatorial air rises → flows toward poles → cools → descends → "
                "flows back along surface toward equator. These giant atmospheric convection "
                "cells (Hadley cells) create Earth's major wind belts, monsoons, and weather "
                "patterns — convection drives our entire climate system."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

SIMULATIONS_KN["land_sea_breeze_kn"] = {
    "title": "ಭೂ ಮತ್ತು ಸಮುದ್ರ ಗಾಳಿ (Land and Sea Breeze)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter7_simulation5_land_sea_breeze_kn.html",
    "description": """
An interactive Kannada-language simulation demonstrating the day-night cycle of
coastal wind patterns driven by differential heating of land and sea:

Day Mode (☀️ ಹಗಲು — Sea Breeze / ಸಮುದ್ರ ಗಾಳಿ):
- Sun visible, bright blue sky
- Land heats faster than sea (lower specific heat capacity)
- Hot air over land rises → low pressure over land
- Cool sea air flows inland to fill the gap → sea breeze (→)
- Temperature indicators: Land = 🔥 (hot), Sea = 🌊 (cool)

Night Mode (🌙 ರಾತ್ರಿ — Land Breeze / ಭೂ ಗಾಳಿ):
- Moon visible, dark starry sky
- Land cools faster than sea → sea is now relatively warmer
- Warm air over sea rises → low pressure over sea
- Cool land air flows toward sea → land breeze (←)
- Temperature indicators: Sea = 🔥 (warm), Land = ❄️ (cool)

The simulation teaches:
- Land has lower specific heat capacity than water → heats/cools faster
- Temperature difference between land and sea creates pressure gradient
- Air flows from high pressure to low pressure (from cool to warm area)
- This reversal pattern repeats daily at coastal areas

State is exposed via URL so the agent can demonstrate day vs night breezes.
""",
    "cannot_demonstrate": [
        "Quantitative specific heat capacity values for land and water",
        "Wind speed measurements or Beaufort scale",
        "Seasonal monsoon patterns (larger scale than daily breezes)",
        "Three-dimensional wind circulation at multiple altitudes"
    ],
    "initial_params": {
        "initialState": "day",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Time of Day / ಸಮಯ",
            "range": "day, night",
            "url_key": "initialState",
            "effect": (
                "Selects which breeze pattern is displayed.\n"
                "  'day'   → daytime sea breeze (→): land hot, sea cool, wind blows sea→land [default]\n"
                "  'night' → night-time land breeze (←): sea warm, land cool, wind blows land→sea"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the key concept card at the top.\n"
                "  true  → show the 'ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆ' concept card (default)\n"
                "  false → hide the concept card for a cleaner view"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Specific Heat Capacity: Why Land Heats Faster than Sea",
            "description": (
                "Understanding the physical property that explains why land and water "
                "respond differently to the same amount of solar heating."
            ),
            "key_insight": (
                "Specific heat capacity is the amount of heat energy needed to raise 1 kg "
                "of a material by 1°C. Water's specific heat capacity (~4200 J/kg°C) is "
                "about 5× higher than dry land (~840 J/kg°C). "
                "This means: for the same amount of solar energy absorbed, land heats up "
                "5× more than the same mass of water. Land also loses heat 5× faster at "
                "night. So during the day, land quickly becomes much hotter than the sea; "
                "at night, land quickly becomes much cooler. "
                "This daily temperature swing (large for land, small for sea) is the "
                "engine that drives sea and land breezes."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Sea Breeze: Daytime Coastal Wind Pattern",
            "description": (
                "How differential daytime heating creates a low-pressure zone over "
                "land that draws cool sea air inland as the sea breeze."
            ),
            "key_insight": (
                "Daytime sequence: Sun heats land strongly → hot air over land rises "
                "(convection) → surface air pressure over land drops (fewer air molecules "
                "at surface level) → creates pressure gradient between cool sea (high "
                "pressure) and hot land (low pressure) → air flows from high to low "
                "pressure → cool sea air blows inland = sea breeze. "
                "Effect: coastal areas receive refreshing cool sea breeze in the afternoon, "
                "making coastal cities like Mumbai, Chennai, and Kochi more bearable in "
                "summer afternoons despite high temperatures. The sea breeze can extend "
                "20-50 km inland and reach speeds of 15-25 km/h."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Land Breeze: Night-Time Reversal",
            "description": (
                "How the temperature differential reverses at night, creating the "
                "opposite wind pattern blowing from land toward sea."
            ),
            "key_insight": (
                "At night, land cools rapidly (low specific heat capacity releases "
                "heat quickly) while the sea retains its warmth (high specific heat "
                "capacity). Now the sea is relatively warmer than land. "
                "Night sequence: Sea surface is warmer → warm air over sea rises → "
                "pressure drops over sea → pressure is now higher over cool land → "
                "cool land air flows toward sea = land breeze (opposite of daytime). "
                "This reversal happens predictably each day at coastal areas. "
                "Fishermen have traditionally used this pattern: go to sea at night "
                "on the land breeze, return in the afternoon on the sea breeze — "
                "free wind power aligned with their fishing schedule!"
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["heat_sources_kn"] = [

    {
        "id": "heat_sources_kn_q1",
        "challenge": (
            "Show the Kerala region to explain why coastal tropical areas near the "
            "equator remain consistently hot and humid throughout the year.\n\n"
            "(ಕೇರಳ ಪ್ರದೇಶ ತೋರಿಸಿ — ಉಷ್ಣವಲಯ ಕರಾವಳಿ ಹವಾಮಾನ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "kerala"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'kerala' as the Region. This shows Kerala's temperature profile: "
                "25-32°C year-round, near the equator, high humidity. The panel explains "
                "why sunlight hits almost perpendicularly here, maximizing heating."
            ),
            "attempt_2": (
                "Set 'initialState=kerala'. Kerala sits close to the equator (8-12°N latitude), "
                "so the Sun is nearly overhead most of the year — rays strike at 90° or close "
                "to it, concentrating solar energy per unit area. The Arabian Sea and Bay of "
                "Bengal provide moisture, making it hot AND humid."
            ),
            "attempt_3": (
                "Choose 'kerala'. The key factors: (1) low latitude = perpendicular sun rays = "
                "intense heating, (2) coastal location = sea moisture = high humidity, "
                "(3) no extreme seasonal variation because equatorial sun angle changes little "
                "across the year. Compare this with Delhi and Sikkim to see the contrast."
            )
        },
        "concept_reminder": (
            "Kerala's climate (hot and humid year-round) results from two factors: "
            "1. LATITUDE: Kerala lies between 8-12°N — close to the equator. At low latitudes, "
            "the Sun is nearly overhead throughout the year. Perpendicular sun rays concentrate "
            "maximum solar energy per unit area of ground (same energy over smallest area). "
            "Farther from equator, rays hit at an angle, spreading energy over a larger area "
            "and providing less heating per square metre. "
            "2. COASTAL POSITION: Water has high specific heat — the surrounding seas moderate "
            "temperature extremes and contribute moisture to the air. "
            "Result: consistently high temperatures (25-32°C) with little seasonal variation. "
            "(ಸೂರ್ಯ = ಭೂಮಿಯ ಉಷ್ಣ ಮೂಲ; ಅಕ್ಷಾಂಶ = ತಾಪಮಾನ ಮೊದಲ ನಿರ್ಣಾಯಕ!)"
        )
    },

    {
        "id": "heat_sources_kn_q2",
        "challenge": (
            "Show the Delhi region to demonstrate why continental interior regions "
            "far from the sea experience extreme temperature variation between seasons.\n\n"
            "(ದೆಹಲಿ ಪ್ರದೇಶ ತೋರಿಸಿ — ಭೂಖಂಡ ಹಿಂಭಾಗ ಹವಾಮಾನ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "delhi"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'delhi' as the Region. This shows Delhi's extreme temperature range: "
                "5°C in winter to 45°C in summer. The panel explains the continental location "
                "with no sea to moderate temperatures."
            ),
            "attempt_2": (
                "Set 'initialState=delhi'. Delhi is at ~28°N latitude, similar to some "
                "coastal Mediterranean cities with mild climates. But landlocked Delhi has "
                "no ocean nearby to moderate its temperatures — it heats intensely in summer "
                "and loses heat rapidly in winter."
            ),
            "attempt_3": (
                "Choose 'delhi'. Compare Delhi with Mumbai (also around 19°N but coastal): "
                "Mumbai range is 19-33°C; Delhi is 5-45°C. The huge difference shows how "
                "coastal proximity moderates temperatures while continental interiors experience "
                "extremes. Water's high specific heat absorbs and releases heat slowly."
            )
        },
        "concept_reminder": (
            "Delhi's extreme temperature variation (5°C winter to 45°C summer) results from "
            "its continental interior location: no large water body nearby to moderate temperatures. "
            "LAND heats up and cools down rapidly (low specific heat capacity: ~840 J/kg°C). "
            "WATER heats up and cools down slowly (high specific heat capacity: ~4200 J/kg°C). "
            "So coastal cities experience moderate temperatures year-round because nearby oceans "
            "absorb summer heat and release stored warmth in winter. "
            "Continental interiors like Delhi have no such moderating influence: "
            "Dry air heats rapidly in summer (intense solar radiation, low humidity). "
            "Clear skies allow rapid radiative cooling in winter nights. "
            "Result: 40°C temperature swing between summer and winter — five times more than "
            "coastal cities at similar latitudes! "
            "(ಸಮುದ್ರ = ತಾಪಮಾನ ನಿಯಂತ್ರಕ; ದೆಹಲಿ = ಭೂಖಂಡ ತೀವ್ರತೆ!)"
        )
    },

    {
        "id": "heat_sources_kn_q3",
        "challenge": (
            "Show the Sikkim region to explain why high-altitude Himalayan areas "
            "remain cold even though they receive the same solar radiation as plains.\n\n"
            "(ಸಿಕ್ಕಿಂ ಪ್ರದೇಶ ತೋರಿಸಿ — ಎತ್ತರದ ಪರ್ವತ ಹವಾಮಾನ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "sikkim"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'sikkim' as the Region. This shows Sikkim's cool temperature profile: "
                "5-20°C despite receiving similar solar radiation to the plains. The panel "
                "explains the altitude effect on temperature."
            ),
            "attempt_2": (
                "Set 'initialState=sikkim'. Sikkim sits at altitudes of 300-8600m (most "
                "inhabited areas 1500-4000m). At high altitudes, the atmosphere is thinner — "
                "less air to absorb and retain heat from the Sun. Temperature drops "
                "approximately 6°C for every 1000m rise in altitude."
            ),
            "attempt_3": (
                "Choose 'sikkim'. Gangtok (capital of Sikkim) at ~1650m altitude averages "
                "12-22°C. At the same latitude but near sea level (like Kolkata), temperatures "
                "are 20-36°C. The 1650m altitude accounts for ~10°C cooler temperatures. "
                "This is the environmental lapse rate: atmosphere thins with altitude, "
                "retaining less heat."
            )
        },
        "concept_reminder": (
            "Sikkim is cold because of ALTITUDE despite its latitude (27°N, similar to Delhi). "
            "The environmental lapse rate: temperature decreases by ~6°C per 1000m of altitude. "
            "WHY? Atmosphere is thinner at high altitude: "
            "1. Fewer air molecules to absorb solar radiation and retain heat. "
            "2. Lower atmospheric pressure → air expands → expansion causes cooling "
            "   (adiabatic cooling — same principle as aerosol cans feeling cold when emptied). "
            "3. Distance from the warm ground surface (which absorbs most solar radiation). "
            "The Sun reaches high altitudes just as intensely (UV radiation is actually "
            "MORE intense at altitude), but the thin air cannot hold the heat. "
            "Comparing all three: Kerala (hot, low latitude, coastal), Delhi (extreme, "
            "low altitude, continental), Sikkim (cold, high altitude) — all show "
            "different faces of HOW the Sun's heat reaches and affects Earth's surface. "
            "(ಎತ್ತರ ಹೆಚ್ಚಿದಂತೆ = ತಾಪಮಾನ ಕಡಿಮೆ; ಪ್ರತಿ 1000 ಮೀ = 6°C ಕಡಿಮೆ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["conduction_experiment_kn"] = [

    {
        "id": "conduction_exp_kn_q1",
        "challenge": (
            "Set the flame to medium intensity and run the conduction experiment to "
            "show how heat travels along a metal strip, dropping closer pins first.\n\n"
            "(ಮಧ್ಯಮ ಜ್ವಾಲೆ ಹೊಂದಿಸಿ ಉಷ್ಣ ವಾಹಕತೆ ಪ್ರಯೋಗ ನಡೆಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "medium"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'medium' as the Flame Intensity. The simulation auto-starts "
                "with medium heat (🔥🔥), showing pins 1-4 dropping in sequence at "
                "approximately 2.0s, 3.5s, 5.0s, 6.5s from closest to furthest."
            ),
            "attempt_2": (
                "Set 'initialState=medium'. Watch the heat gradient bar extend along "
                "the metal strip from left to right, and the particle view shows "
                "particles changing from cold (grey) → warm (orange) → hot (red) "
                "as heat conducts from pin 1 to pin 4."
            ),
            "attempt_3": (
                "Choose 'medium'. The result panel shows pin drop times for all 4 pins. "
                "Pin 1 (3 cm from flame) falls first, Pin 4 (12 cm) falls last — "
                "demonstrating that heat travels from the heat source outward, and "
                "conduction takes time proportional to distance."
            )
        },
        "concept_reminder": (
            "Heat conduction in solids: heat energy travels from the hot end to the cold end "
            "through particle vibration. The metal strip's atoms near the flame vibrate faster "
            "(higher temperature = higher kinetic energy). These fast-vibrating atoms collide "
            "with adjacent slower-vibrating atoms, gradually transferring kinetic energy along "
            "the strip. Critical point: atoms VIBRATE in place — they do NOT move from their "
            "positions. Only energy is transferred, not matter itself. "
            "This is why: "
            "- Pin 1 (closest, 3 cm) drops first — heat arrives there soonest. "
            "- Pin 4 (furthest, 12 cm) drops last — heat must travel 12 cm. "
            "- Higher flame = faster conduction (greater temperature difference = faster transfer). "
            "The wax on each pin melts at ~40-50°C. When heat traveling along the strip "
            "reaches a pin location, it melts the wax → pin falls. This is the classic "
            "school experiment to PROVE that conduction travels from one end to the other. "
            "(ಉಷ್ಣ ಹರಿವು = ಬಿಸಿ ಪ್ರದೇಶ → ತಂಪು ಪ್ರದೇಶ; ಕಣಗಳು ಕಂಪಿಸುತ್ತವೆ, ಚಲಿಸುವುದಿಲ್ಲ!)"
        )
    },

    {
        "id": "conduction_exp_kn_q2",
        "challenge": (
            "Set the flame to high intensity to show how increased heat accelerates "
            "conduction, dropping all pins much faster than medium flame.\n\n"
            "(ಅಧಿಕ ಜ್ವಾಲೆ ಹೊಂದಿಸಿ — ಹೆಚ್ಚು ಉಷ್ಣ = ವೇಗವಾಗಿ ವಾಹಕತೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "high"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'high' as the Flame Intensity. The simulation auto-starts with "
                "maximum heat (🔥🔥🔥), dropping all 4 pins within 4 seconds — "
                "compare with medium (6.5s for pin 4) to see the 40% speed increase."
            ),
            "attempt_2": (
                "Set 'initialState=high'. The high flame creates a larger temperature "
                "difference between the flame end and each pin. Greater ΔT (temperature "
                "gradient) drives faster conduction — this is Fourier's Law."
            ),
            "attempt_3": (
                "Choose 'high'. Pin drop times with high flame: ~1s, ~2s, ~3s, ~4s. "
                "Compare with medium: ~2s, ~3.5s, ~5s, ~6.5s. High flame is roughly "
                "1.5-2× faster, showing that temperature difference directly drives "
                "the rate of heat transfer."
            )
        },
        "concept_reminder": (
            "Fourier's Law of Heat Conduction: heat flow rate (Q/t) is proportional to "
            "the temperature gradient (ΔT/L) and the material's thermal conductivity (k). "
            "Formula: Q/t = k × A × ΔT/L "
            "where A = cross-sectional area, L = length of conductor. "
            "When flame intensity increases: "
            "- Temperature at hot end increases → ΔT (temperature difference) increases "
            "- Larger ΔT → stronger driving force → faster conduction → pins drop sooner. "
            "This is why: cooking on high heat is faster, iron heating elements get hotter "
            "faster when powered more, industrial furnaces use intense heat. "
            "The relationship is LINEAR: doubling the temperature difference roughly "
            "doubles the rate of heat transfer through the same material. "
            "This simulation demonstrates this by showing high flame pins fall roughly "
            "twice as fast as low flame pins. "
            "(ΔT ಹೆಚ್ಚು = ವಾಹಕತೆ ವೇಗ ಹೆಚ್ಚು — ಫ್ಯೂರಿಯರ್ ನಿಯಮ!)"
        )
    },

    {
        "id": "conduction_exp_kn_q3",
        "challenge": (
            "Set the flame to low intensity to show that reduced heat slows conduction "
            "significantly, demonstrating that temperature gradient controls the rate.\n\n"
            "(ಕಡಿಮೆ ಜ್ವಾಲೆ ಹೊಂದಿಸಿ — ಕಡಿಮೆ ಉಷ್ಣ = ನಿಧಾನ ವಾಹಕತೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "low"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'low' as the Flame Intensity. The simulation auto-starts with "
                "the weakest flame (🔥), dropping pins at ~4s, ~6s, ~8s, ~10s — "
                "the last pin takes 10 seconds with low heat vs 4 seconds with high heat."
            ),
            "attempt_2": (
                "Set 'initialState=low'. Low flame = small temperature difference between "
                "flame and metal. The smaller the driving force (ΔT), the slower the "
                "conduction. Particles near the flame gain energy slowly and "
                "transfer it slowly to their neighbors."
            ),
            "attempt_3": (
                "Choose 'low'. The particle view shows particles changing color more slowly "
                "from cold grey to hot red. Pin 4 takes 10 seconds — 2.5× longer than "
                "with high flame (4 seconds). This comparison across all three flame levels "
                "demonstrates the proportional relationship between ΔT and conduction rate."
            )
        },
        "concept_reminder": (
            "At low flame intensity, the temperature at the hot end is lower, shrinking "
            "the temperature difference (ΔT) across the metal strip. Per Fourier's Law, "
            "smaller ΔT → slower heat flow → pins take longer to drop. "
            "Real-world implications: "
            "- Insulation works by reducing ΔT across a barrier — walls, clothing, and "
            "  thermos flasks create a temperature gradient spread over thick material, "
            "  reducing heat flow per unit time. "
            "- This is why a metal utensil on a very low flame barely heats the handle "
            "  (small ΔT, slow conduction), while on full heat the handle quickly becomes "
            "  dangerously hot (large ΔT, fast conduction). "
            "- Body temperature regulation: the body maintains core temperature of 37°C; "
            "  skin may be 32°C; a slight ΔT ensures steady (not rapid) heat loss to air. "
            "The experiment across three flame levels proves that temperature gradient "
            "is the key variable controlling conduction rate in a given material. "
            "(ಕಡಿಮೆ ΔT = ನಿಧಾನ ವಾಹಕತೆ; ಅವಾಹಕ = ΔT ಕಡಿಮೆ ಮಾಡುವ ಸಾಧನ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["thermal_conductors_kn"] = [

    {
        "id": "thermal_conductors_kn_q1",
        "challenge": (
            "Run the heat race in race mode to visually demonstrate that metal is "
            "a far superior thermal conductor compared to wood, glass, and plastic.\n\n"
            "(ಉಷ್ಣ ಓಟ ನಡೆಸಿ — ಲೋಹ ಉತ್ತಮ ವಾಹಕ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "race"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'race' as the Mode. The simulation auto-starts the race, "
                "showing heat progressing along 4 material tracks simultaneously. "
                "Metal finishes first (🥇), followed by glass (🥈), wood (🥉), plastic (4th)."
            ),
            "attempt_2": (
                "Set 'initialState=race'. The race mode shows heat bars extending from "
                "left to right for each material at different speeds. Metal's bar extends "
                "5× faster than wood's, demonstrating the huge difference between "
                "metallic and non-metallic conductors."
            ),
            "attempt_3": (
                "Choose 'race'. The results panel shows finish times: metal finishes "
                "in about 1-2 seconds while plastic may take 15-20 seconds. "
                "This visual comparison makes the relative conductivity differences "
                "immediately obvious — metals are dramatically better conductors."
            )
        },
        "concept_reminder": (
            "Why metals win every thermal race: "
            "Metals have FREE ELECTRONS — valence electrons loosely bound to atoms that "
            "move freely throughout the metal lattice (the 'sea of electrons model'). "
            "When heat is applied: free electrons gain kinetic energy → zip through the "
            "metal rapidly → transfer energy to cooler regions → very fast conduction. "
            "Non-metals (wood, glass, plastic): NO free electrons. Heat can only "
            "transfer through slow atomic vibration chains. Air pockets in wood further "
            "slow conduction. Result: 5-10× slower than metal. "
            "Conductivity ranking (W/m·K): Copper ~400, Aluminium ~237, Iron ~80, "
            "Glass ~1.0, Wood ~0.1-0.3, Plastic ~0.1-0.5. "
            "Ratio: copper is 1000-4000× better conductor than wood! "
            "Practical design: frying pan = iron/steel (conducts heat to food); "
            "handle = bakelite/plastic (insulates hand). Both properties needed together. "
            "(ಲೋಹ = ಉತ್ತಮ ವಾಹಕ; ಮರ/ಪ್ಲಾಸ್ಟಿಕ್ = ಉತ್ತಮ ಅವಾಹಕ!)"
        )
    },

    {
        "id": "thermal_conductors_kn_q2",
        "challenge": (
            "Switch to compare mode to examine each material's properties individually "
            "and explain why metals and non-metals differ so dramatically in heat conduction.\n\n"
            "(ಹೋಲಿಕೆ ಮೋಡ್ ತೋರಿಸಿ — ವ್ಯತ್ಯಾಸ ವಿಶ್ಲೇಷಣೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "compare"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'compare' as the Mode. This switches to compare mode where each "
                "material is displayed separately for individual analysis. "
                "Tap on each material track to see detailed information about why "
                "it conducts or insulates."
            ),
            "attempt_2": (
                "Set 'initialState=compare'. The compare mode is useful when you want "
                "to focus on one material at a time and explain the atomic-level reason "
                "for its thermal behaviour — free electrons in metals, air pockets in wood."
            ),
            "attempt_3": (
                "Choose 'compare'. In compare mode, clicking the metal track shows: "
                "'ಲೋಹ ಉತ್ತಮ ವಾಹಕ! ಉಷ್ಣ ಅದರ ಮೂಲಕ ಬಹು ವೇಗವಾಗಿ ಹರಿಯುತ್ತದೆ.' "
                "Clicking wood shows: 'ಮರ ಅವಾಹಕ. ಗಾಳಿ ಜಾಗಗಳು ಉಷ್ಣ ವರ್ಗಾವಣೆ ನಿಧಾನಗೊಳಿಸುತ್ತವೆ.'"
            )
        },
        "concept_reminder": (
            "Why materials differ in thermal conductivity: "
            "METALS (ಲೋಹಗಳು): 'Sea of electrons' model — outer electrons not bound to any "
            "single atom but free to roam. Heat → free electrons gain KE → move fast → "
            "instantly carry energy to cooler end + atom vibration also contributes. "
            "WOOD (ಮರ): Organic polymer (cellulose, lignin). No free electrons. Tightly "
            "bound electrons. Cellular structure has many microscopic air spaces — air "
            "is an excellent insulator (molecules too far apart, no free electrons). "
            "GLASS (ಗಾಜು): Amorphous silica network — no free electrons, but denser than "
            "wood so slightly better conduction through atomic vibration. "
            "PLASTIC (ಪ್ಲಾಸ್ಟಿಕ್): Long hydrocarbon polymer chains. No free electrons. "
            "Flexible chains absorb rather than transmit vibration energy. Excellent insulator. "
            "ENGINEERING USE: Products designed using BOTH — body = metal (fast conduction "
            "for intended function), contact surface = insulator (protection from burns). "
            "(ಮುಕ್ತ ಎಲೆಕ್ಟ್ರಾನ್ = ಉಷ್ಣ ವಾಹಕ; ಮುಕ್ತ ಎಲೆಕ್ಟ್ರಾನ್ ಇಲ್ಲ = ಅವಾಹಕ!)"
        )
    },

    {
        "id": "thermal_conductors_kn_q3",
        "challenge": (
            "Return to race mode and observe which material finishes last to identify "
            "the best thermal insulator and explain where it is used in daily life.\n\n"
            "(ಓಟ ಮೋಡ್‌ಗೆ ಹಿಂತಿರುಗಿ — ಅತ್ಯುತ್ತಮ ಅವಾಹಕ ಗುರುತಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "race"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'race' as the Mode again. Watch the race to its end — the last "
                "material to finish (receive 4th badge) is plastic, the worst thermal "
                "conductor and therefore the best insulator in this set of materials."
            ),
            "attempt_2": (
                "Set 'initialState=race'. Plastic (speed 0.6x) finishes last — even "
                "behind wood (0.8x) and glass (1.0x). Plastic polymer chains are "
                "extremely poor heat conductors. This makes plastic the material of "
                "choice for kitchen handles, electrical insulation, and packaging."
            ),
            "attempt_3": (
                "Choose 'race'. Compare finish times: metal finishes ~3-4× faster than "
                "plastic. This huge gap explains why: kitchen utensil handles are "
                "plastic/teflon-coated (not metal), electrical wires are plastic-insulated, "
                "styrofoam (expanded plastic) keeps coffee hot and ice cream cold."
            )
        },
        "concept_reminder": (
            "Best insulator in the race: PLASTIC (last to finish). "
            "Thermal insulators are as important as conductors in engineering: "
            "1. KITCHEN SAFETY: Plastic and rubber handles on pots, pans, and appliances "
            "   prevent burns. The metal pot conducts heat to food; the plastic handle "
            "   conducts almost no heat to your hand. "
            "2. BUILDING INSULATION: Fiberglass, mineral wool, expanded polystyrene (EPS) "
            "   in walls and roofs reduce heat loss in winter and heat gain in summer "
            "   → saves energy, reduces heating/cooling costs. "
            "3. THERMOS FLASK: Vacuum (no material at all) is the ultimate insulator "
            "   between inner and outer walls. The glass/plastic walls add extra insulation. "
            "4. ELECTRICAL SAFETY: Copper wire (conductor) surrounded by PVC plastic "
            "   (insulator) — conducts electricity where needed, prevents leakage elsewhere. "
            "5. WINTER CLOTHING: Wool and down feathers trap air pockets in their fiber "
            "   structure — air is extremely poor conductor (0.025 W/m·K vs iron 80 W/m·K). "
            "The race's 'loser' (plastic) wins in real-life insulation applications! "
            "(ಅವಾಹಕ = ಉಷ್ಣ ತಡೆಯುವ ವಸ್ತು; ಪ್ಲಾಸ್ಟಿಕ್ = ನಿಜ ಜೀವನದ ವಿಜೇತ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["convection_kn"] = [

    {
        "id": "convection_kn_q1",
        "challenge": (
            "Show water convection with heat turned on to demonstrate circular "
            "convection currents where hot particles rise and cool particles sink.\n\n"
            "(ನೀರಿನ ಸಂವಹನ ತೋರಿಸಿ — ಬಿಸಿ ನೀರು ಏರುತ್ತದೆ, ತಂಪು ಇಳಿಯುತ್ತದೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "water"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'water' as the Medium. The simulation auto-activates heat, "
                "showing the beaker with 6 numbered particles. Bottom particles turn "
                "red/orange (hot) and rise; top particles remain blue/cool and sink. "
                "The circular convection current forms."
            ),
            "attempt_2": (
                "Set 'initialState=water'. Watch particle 1, 2, 3 near the flame — "
                "they gain the 'hot' (red) class and animate along the 'rise-path'. "
                "Particles 4, 5, 6 near the top stay cool (blue) and animate along "
                "the 'fall-path'. Together they form the convection loop."
            ),
            "attempt_3": (
                "Choose 'water'. The explanation panel states: hot water near the "
                "bottom expands (becomes less dense) → rises. Cool water at top "
                "sinks to replace it → creates continuous circular flow (convection "
                "current). You can click individual particles to track their path."
            )
        },
        "concept_reminder": (
            "Convection in liquids: heat transfers through actual movement of the fluid. "
            "MECHANISM: "
            "1. Flame heats water at the bottom of beaker. "
            "2. Hot water molecules gain KE → move faster → volume increases (expansion). "
            "3. Density = mass/volume. Same mass, more volume → LESS DENSE. "
            "4. Less dense hot water is buoyed upward (Archimedes' principle — less dense "
            "   fluid rises in denser surroundings). "
            "5. Hot water rises to top → moves sideways → loses heat to surroundings → "
            "   becomes denser → sinks back toward heat source. "
            "6. Complete loop = CONVECTION CURRENT. "
            "KEY CONTRAST with conduction: in conduction, particles VIBRATE in place; "
            "in convection, particles PHYSICALLY MOVE, carrying their heat energy along. "
            "This is why convection is faster and more efficient for heat distribution "
            "in fluids than conduction. "
            "(ಸಂವಹನ = ದ್ರವ ಚಲನೆ; ಬಿಸಿ ದ್ರವ ಏರುತ್ತದೆ, ತಂಪು ದ್ರವ ಇಳಿಯುತ್ತದೆ!)"
        )
    },

    {
        "id": "convection_kn_q2",
        "challenge": (
            "Switch to air mode to show how convection in air (gas) works in a room "
            "with a heater — explaining how the entire room eventually warms up.\n\n"
            "(ಗಾಳಿ ಮೋಡ್ ತೋರಿಸಿ — ಕೋಣೆಯ ಉಷ್ಣ ಸಂವಹನ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "air"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'air' as the Medium. The simulation switches to air mode showing "
                "a room with a heater (🔥) at bottom left. Air particles near the heater "
                "animate upward (air-rising), while other particles animate downward "
                "(air-falling) in the circular convection pattern."
            ),
            "attempt_2": (
                "Set 'initialState=air'. The explanation panel for air mode reads: "
                "'ಕೋಣೆಯ ಹೀಟರ್ ಹತ್ತಿರದ ಗಾಳಿಯನ್ನು ಬಿಸಿ ಮಾಡುತ್ತದೆ. ಬಿಸಿ ಗಾಳಿ ಮೇಲಕ್ಕೆ ಏರುತ್ತದೆ' — "
                "showing the same convection principle as water but in air (a gas)."
            ),
            "attempt_3": (
                "Choose 'air'. The room convection loop: heater (bottom left) → warm air "
                "rises → spreads across ceiling → cools → sinks along opposite wall → "
                "flows back along floor → reheated at heater. This gradual circulation "
                "warms the entire room, not just the area near the heater."
            )
        },
        "concept_reminder": (
            "Convection in air (gas) works by the same density-difference mechanism as water: "
            "Room heater heats nearby air → hot air expands → less dense → rises to ceiling → "
            "spreads across → cools at ceiling and walls → becomes denser → sinks down → "
            "flows across floor back to heater → heated again → loops continuously. "
            "This convection loop gradually transfers heat throughout the entire room. "
            "PLACEMENT MATTERS: Heater at floor level → most effective (hot air naturally "
            "rises from floor, circulating whole room). Heater at ceiling → inefficient "
            "(hot air stays near ceiling, floor remains cold — wrong direction). "
            "Air conditioners are placed HIGH on the wall — cold air is denser and sinks "
            "naturally, cooling the whole room from top down. "
            "This is the same circulation principle on much larger scales: "
            "Sun heats equatorial air → rises → flows toward poles → cools → descends → "
            "flows back = atmospheric circulation cells (Hadley cells) driving global weather. "
            "(ಕೋಣೆ ಹೀಟರ್ = ಸಣ್ಣ ಪ್ರಮಾಣದ ಸಂವಹನ; ವಾತಾವರಣ ಪರಿಚಲನೆ = ದೊಡ್ಡ ಪ್ರಮಾಣ!)"
        )
    },

    {
        "id": "convection_kn_q3",
        "challenge": (
            "Show water convection mode to explain why convection only occurs in "
            "fluids (liquids and gases) but NOT in solids.\n\n"
            "(ನೀರಿನ ಸಂವಹನ ತೋರಿಸಿ — ಸಂವಹನ ಏಕೆ ಘನದಲ್ಲಿ ಸಂಭವಿಸುವುದಿಲ್ಲ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "water"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'water' as the Medium. The simulation shows convection as "
                "particles physically moving in circular paths. This physical movement "
                "is only possible in fluids — in solids, particles are locked in fixed "
                "positions by strong bonds and cannot move to create currents."
            ),
            "attempt_2": (
                "Set 'initialState=water'. The key observation: particles move along "
                "paths (rise-path and fall-path animations). In a solid, particles can "
                "only VIBRATE around fixed positions — they cannot flow or change relative "
                "positions. No flow = no convection current possible."
            ),
            "attempt_3": (
                "Choose 'water'. The informational text says: 'ಸಂವಹನ ದ್ರವಗಳಲ್ಲಿ "
                "ಸಂಭವಿಸುತ್ತದೆ (ದ್ರವಗಳು ಮತ್ತು ಅನಿಲಗಳು)' — confirming convection occurs "
                "in fluids (liquids and gases). Solids can only conduct heat; "
                "they cannot convect because their particles cannot migrate."
            )
        },
        "concept_reminder": (
            "Why convection is IMPOSSIBLE in solids: "
            "Convection requires physical movement of matter from hot to cool regions. "
            "In solids, particles (atoms or molecules) are held in fixed positions by "
            "strong intermolecular bonds in a crystal lattice or rigid structure. "
            "They can only VIBRATE around fixed positions — they CANNOT move from one "
            "place to another. Without particle migration, there can be no bulk flow, "
            "and without flow, there is no convection. "
            "Solids can only transfer heat by CONDUCTION (vibration energy passed "
            "from particle to particle). "
            "Summary of heat transfer modes and where they occur: "
            "• CONDUCTION: solids (and liquids/gases, but poorly) — NO particle movement "
            "• CONVECTION: fluids only (liquids + gases) — requires particle movement "
            "• RADIATION: anywhere including vacuum — no medium needed at all "
            "A metal rod conducts (can't convect). Water in a beaker can do both "
            "(conduct a little, convect a lot). Sun heats Earth through radiation "
            "across the vacuum of space. "
            "(ಘನ = ಕೇವಲ ವಾಹಕತೆ; ದ್ರವ = ವಾಹಕತೆ + ಸಂವಹನ; ವಿಕಿರಣ = ಮಾಧ್ಯಮ ಬೇಡ!)"
        )
    }
]

QUIZ_QUESTIONS_KN["land_sea_breeze_kn"] = [

    {
        "id": "land_sea_breeze_kn_q1",
        "challenge": (
            "Show the daytime sea breeze to explain why coastal areas receive cool "
            "wind from the sea during hot afternoons.\n\n"
            "(ಹಗಲಿನ ಸಮುದ್ರ ಗಾಳಿ ತೋರಿಸಿ — ಸಮುದ್ರ ತೀರದಲ್ಲಿ ತಂಪು ಮಧ್ಯಾಹ್ನ ಗಾಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "day"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'day' as the Time of Day. The simulation shows: bright sky, "
                "sun visible, land glowing hot (🔥) and sea cool (🌊). Wind arrows "
                "point right (sea → land). The breeze name shows '🌬️ ಸಮುದ್ರ ಗಾಳಿ'."
            ),
            "attempt_2": (
                "Set 'initialState=day'. The explanation reads: 'ಹಗಲು, ಭೂಮಿ ಸಮುದ್ರಕ್ಕಿಂತ "
                "ಬೇಗ ಬಿಸಿಯಾಗುತ್ತದೆ. ಭೂಮಿ ಮೇಲಿನ ಬಿಸಿ ಗಾಳಿ ಏರುತ್ತದೆ. ಸಮುದ್ರದಿಂದ ತಂಪು ಗಾಳಿ "
                "ಅದರ ಸ್ಥಾನ ತುಂಬಲು ಒಳನುಗ್ಗುತ್ತದೆ. ಸಮುದ್ರದಿಂದ ಭೂಮಿಗೆ ಈ ತಂಪು ಗಾಳಿಯೇ ಸಮುದ್ರ ಗಾಳಿ.'"
            ),
            "attempt_3": (
                "Choose 'day'. The mechanism: Sun heats land → hot air rises over land "
                "(convection) → low pressure over land → high pressure over sea "
                "(relatively cooler) → air flows from high to low pressure → "
                "cool sea breeze blows inland. This is why coastal cities in India "
                "(Mumbai, Chennai, Kochi) feel refreshed in afternoon sea breezes."
            )
        },
        "concept_reminder": (
            "Sea breeze (ಸಮುದ್ರ ಗಾಳಿ) — the daytime coastal wind: "
            "ROOT CAUSE: Land has LOWER specific heat capacity (~840 J/kg°C) than water "
            "(~4200 J/kg°C). So for the same solar energy received: land heats up 5× faster. "
            "MECHANISM (convection-driven): "
            "1. Morning: land and sea start at similar temperatures. "
            "2. As Sun rises: land heats rapidly → hot air above land rises (low density) → "
            "   low air pressure zone forms over land. "
            "3. Sea heats slowly → stays cool → relatively high pressure over sea. "
            "4. Air flows from high pressure (sea) to low pressure (land) = SEA BREEZE. "
            "5. Sea breeze is typically strongest in early afternoon (peak land heating). "
            "EFFECT: Coastal areas receive refreshing cool, moist air from the sea during "
            "the hottest part of the day. Sea breeze can penetrate 20-50 km inland and "
            "reach speeds of 15-25 km/h. "
            "This is why coastal cities like Mumbai and Kochi are more bearable in summer "
            "than inland cities at similar latitudes. "
            "(ಹಗಲು = ಭೂಮಿ ಬಿಸಿ → ಗಾಳಿ ಏರುತ್ತದೆ → ಸಮುದ್ರ ಗಾಳಿ ಒಳನುಗ್ಗುತ್ತದೆ!)"
        )
    },

    {
        "id": "land_sea_breeze_kn_q2",
        "challenge": (
            "Show the night-time land breeze to demonstrate how the wind pattern "
            "reverses at night when land cools faster than the sea.\n\n"
            "(ರಾತ್ರಿ ಭೂ ಗಾಳಿ ತೋರಿಸಿ — ರಾತ್ರಿ ವಿರುದ್ಧ ದಿಕ್ಕಿನಲ್ಲಿ ಗಾಳಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "night"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'night' as the Time of Day. The simulation switches to: dark sky "
                "with moon and stars, sea indicators show 🔥 (warm), land shows ❄️ (cool). "
                "Wind arrows now point LEFT (land → sea). The breeze name shows '🌬️ ಭೂ ಗಾಳಿ'."
            ),
            "attempt_2": (
                "Set 'initialState=night'. The explanation: 'ರಾತ್ರಿಯಲ್ಲಿ, ಭೂಮಿ ಸಮುದ್ರಕ್ಕಿಂತ "
                "ವೇಗವಾಗಿ ತಂಪಾಗುತ್ತದೆ. ಸಮುದ್ರ ತುಲನಾತ್ಮಕವಾಗಿ ಬೆಚ್ಚನೆಯಾಗಿ ಉಳಿಯುತ್ತದೆ.' "
                "The situation is now reversed: sea is relatively warmer, creating rising "
                "air over sea and flow from land toward sea."
            ),
            "attempt_3": (
                "Choose 'night'. Notice the complete reversal: arrows go LEFT instead "
                "of right, temperature indicators swap (land cold, sea warm). "
                "At night, land loses heat rapidly; sea retains warmth from the day. "
                "This reversal happens predictably every 24 hours at coastal areas."
            )
        },
        "concept_reminder": (
            "Land breeze (ಭೂ ಗಾಳಿ) — the night-time coastal wind: "
            "After sunset, the heat reversal begins: "
            "- Land (low specific heat): rapidly radiates stored heat back to sky → cools fast. "
            "- Sea (high specific heat): releases stored heat slowly → stays warm for hours. "
            "MECHANISM: "
            "1. By evening/night: land has cooled below sea surface temperature. "
            "2. Sea is now relatively warmer → warm moist air rises over sea → "
            "   low pressure over sea. "
            "3. Cool dense land air moves toward sea (high pressure to low pressure) = LAND BREEZE. "
            "4. Land breeze is typically weaker than sea breeze (smaller temperature difference). "
            "TRADITIONAL USE: Fishermen in Kerala, Tamil Nadu, and other coastal states have "
            "used this pattern for centuries — sail OUT to sea at midnight on the land breeze, "
            "fish till dawn, return to shore in afternoon on the sea breeze. "
            "No engine needed — just knowledge of this daily wind reversal! "
            "This perfectly illustrates how traditional communities observed and applied "
            "natural weather patterns before formal scientific understanding. "
            "(ರಾತ್ರಿ = ಭೂಮಿ ತಂಪು → ಗಾಳಿ ಸಮುದ್ರದ ಕಡೆ → ಭೂ ಗಾಳಿ!)"
        )
    },

    {
        "id": "land_sea_breeze_kn_q3",
        "challenge": (
            "Show the daytime sea breeze again and explain the connection between "
            "land-sea breezes and the large-scale monsoon winds affecting all of India.\n\n"
            "(ಸಮುದ್ರ ಗಾಳಿ ತೋರಿಸಿ — ಮಾನ್ಸೂನ್ ಮತ್ತು ಸಮುದ್ರ ಗಾಳಿ ಸಂಬಂಧ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "initialState",
                    "operator": "==",
                    "value": "day"
                }
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'day' to show the sea breeze mechanism. The sea breeze is "
                "essentially a small-scale, local version of the same process that "
                "drives the Indian summer monsoon — land heating faster than sea, "
                "creating a pressure gradient that draws in moist ocean air."
            ),
            "attempt_2": (
                "Set 'initialState=day'. The sea breeze operates on a daily cycle "
                "(hours). The monsoon operates on a seasonal cycle (months). "
                "Both involve: land heats more than ocean → hot air rises over land → "
                "low pressure draws in moist ocean air. Same physics, different scales."
            ),
            "attempt_3": (
                "Choose 'day'. The key connection: India's summer monsoon (June-September) "
                "happens because the Indian subcontinent heats intensely in summer, "
                "creating low pressure that draws in moist southwest winds from the "
                "Indian Ocean — a giant, season-long 'sea breeze' for all of India."
            )
        },
        "concept_reminder": (
            "Sea breeze and monsoon — same physics, different scales: "
            "DAILY SEA BREEZE (12-24 hour cycle): "
            "- Affects coastal strip ~50 km inland "
            "- Triggered by daytime land heating, reversed at night "
            "- Wind speed: 15-25 km/h "
            "- Carries moist sea air a short distance inland "
            "INDIAN SUMMER MONSOON (3-4 month seasonal reverse): "
            "Same mechanism, continental scale: "
            "- April-May: whole Indian subcontinent heats intensely under summer sun "
            "  (large land mass, low specific heat) → enormous low pressure zone forms. "
            "- Indian Ocean stays cooler (high specific heat) → high pressure over ocean. "
            "- Giant 'sea breeze' draws moisture-laden southwest winds across the ocean "
            "  from the Arabian Sea and Bay of Bengal onto the Indian subcontinent. "
            "- These winds carry enormous moisture → condense as they hit Western Ghats "
            "  and Himalayan foothills → torrential monsoon rain (June-September). "
            "- After monsoon: land cools faster than ocean in October → winds reverse → "
            "  northeast monsoon (weaker, drier) in Tamil Nadu and Sri Lanka. "
            "The simulation's little arrows (→ during day) scale up to the monsoon's "
            "massive southwest winds that bring 80% of India's annual rainfall! "
            "(ಸಮುದ್ರ ಗಾಳಿ = ದೈನಂದಿನ ಮಾನ್ಸೂನ್; ದೊಡ್ಡ ಮಾನ್ಸೂನ್ = ಋತುಮಾನ ಸಮುದ್ರ ಗಾಳಿ!)"
        )
    }
]

# =============================================================================
# RADIATION SIMULATION (Chapter 7, sim6)
# ವಿಕಿರಣ – ಮಾಧ್ಯಮವಿಲ್ಲದ ಉಷ್ಣ ವರ್ಗಾವಣೆ
# =============================================================================
SIMULATIONS_KN["radiation_kn"] = {
    "title": "ವಿಕಿರಣ (Radiation — Heat Without a Medium)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter7_simulation6_radiation_kn.html",

    "description": (
        "Interactive Kannada radiation simulation. Students select a heat source "
        "(fire / sun / hot pan) then use the distance slider to observe how radiated "
        "heat intensity varies with distance (inverse-square-law concept). A colour "
        "experiment shows that dark surfaces absorb more radiation than light ones."
    ),

    "cannot_demonstrate": [
        "Infrared wavelength or electromagnetic spectrum details",
        "Quantitative Stefan-Boltzmann calculations",
        "Simultaneous side-by-side comparison of multiple sources",
    ],

    "initial_params": {"initialState": "fire", "distance": 5, "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Heat Source",
            "range": "fire, sun, pan",
            "url_key": "initialState",
            "effect": (
                "Selects the radiating heat source shown on load.\n"
                "  'fire' → campfire / bonfire (default)\n"
                "  'sun'  → the Sun radiating to Earth\n"
                "  'pan'  → hot cooking pan radiating to a nearby hand"
            )
        },
        "distance": {
            "label": "Distance from Source",
            "range": "1–10 (integer)",
            "url_key": "distance",
            "effect": (
                "Sets the slider position (receiver distance).\n"
                "  1 → very close (intensity ~100%, HOT!)\n"
                "  5 → medium distance (warm, default)\n"
                " 10 → far from source (cool, ~10% intensity)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card, colour experiment, and takeaway box."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Radiation: Heat Transfer Without Any Medium",
            "description": (
                "Radiation transmits heat energy through empty space as electromagnetic "
                "waves. No medium (no air, no water, no solid) is needed — the Sun heats "
                "Earth across the vacuum of space entirely by radiation."
            ),
            "key_insight": (
                "No medium needed = radiation. The Sun is 150 million km away in vacuum, "
                "yet its radiation warms every surface it touches. "
                "This distinguishes radiation from conduction (needs solid) and "
                "convection (needs fluid)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Intensity Decreases With Distance",
            "description": (
                "The intensity of radiated heat decreases as the receiver moves farther "
                "from the source. Moving the slider from 1 to 10 shows the receiver "
                "cooling from HOT! to Cool as intensity drops."
            ),
            "key_insight": (
                "Radiation intensity follows an inverse-square law: double the distance "
                "→ quarter the intensity. This is why standing close to a fire is much "
                "hotter than standing far away, even though the same energy is emitted."
            ),
            "related_params": ["initialState", "distance"]
        },
        {
            "id": 3,
            "title": "Dark Colours Absorb More Radiation Than Light Colours",
            "description": (
                "Dark / black surfaces absorb radiation energy and become hotter. "
                "Light / shiny surfaces reflect radiation and stay cooler. "
                "This explains why dark clothes feel hot in sunlight."
            ),
            "key_insight": (
                "Black absorbs → hotter. White reflects → cooler. "
                "In summer, wear light colours (reflect sun) to stay cool. "
                "In winter, wear dark colours (absorb sun) to stay warm. "
                "Same radiation source, different material response."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["radiation_kn"] = [
    {
        "id": "radiation_kn_q1",
        "challenge": (
            "Show heat radiation from the SUN source. Demonstrate how the Sun "
            "transfers heat to Earth through the vacuum of space with no medium.\n\n"
            "(ಸೂರ್ಯ ವಿಕಿರಣ ಮೂಲ ಆಯ್ಕೆ ಮಾಡಿ — ಮಾಧ್ಯಮ ಇಲ್ಲದೆ ಉಷ್ಣ ಭೂಮಿ ತಲುಪುವ ಪ್ರಕ್ರಿಯೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "sun"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'sun' as the Simulation State. Radiation waves appear between "
                "the Sun and Earth — no medium at all in the vacuum of space!"
            ),
            "attempt_2": (
                "Set 'initialState' to 'sun'. The Sun–Earth example is the most dramatic "
                "proof that radiation needs no medium (space is a near-perfect vacuum)."
            ),
            "attempt_3": (
                "Choose 'sun': solar radiation travels 150 million km through vacuum to "
                "warm the Earth. Neither conduction nor convection can bridge a vacuum."
            )
        },
        "concept_reminder": (
            "Radiation is the ONLY heat-transfer mode that works across a vacuum. "
            "Sun → Earth: 150 million km of empty space, yet solar radiation keeps Earth warm. "
            "Neither conduction (needs solid) nor convection (needs fluid) can do this. "
            "(ವಿಕಿರಣಕ್ಕೆ ಮಾಧ್ಯಮ ಬೇಡ — ಖಾಲಿ ಜಾಗದಲ್ಲೂ ಹರಡುತ್ತದೆ!)"
        )
    },
    {
        "id": "radiation_kn_q2",
        "challenge": (
            "Show radiation from a HOT PAN (cooking pan). This demonstrates radiation "
            "from an everyday kitchen object. Observe the receiver (hand) positioned nearby.\n\n"
            "(ಬಿಸಿ ಪಾತ್ರೆ ವಿಕಿರಣ ಮೂಲ ಆಯ್ಕೆ ಮಾಡಿ — ಅಡುಗೆ ಅಟ್ಟಿ ಬಳಿ ಉಷ್ಣ ಅನುಭವ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "pan"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'pan' as the Simulation State. The hot pan radiates heat to a "
                "nearby hand — the same warmth felt standing near a hot stove without touching it."
            ),
            "attempt_2": (
                "Set 'initialState' to 'pan'. Even a cooking pan below boiling "
                "radiates heat to nearby objects without direct contact."
            ),
            "attempt_3": (
                "Choose 'pan': hot pan radiates to the hand. Conduction would require "
                "touching the pan; radiation reaches without any contact."
            )
        },
        "concept_reminder": (
            "A hot pan radiates heat to nearby hands/faces WITHOUT direct contact. "
            "This is radiation — not conduction (no touch) and not convection "
            "(the hand is not in the hot air stream). "
            "Standing near a stove = feeling radiant heat. "
            "(ಬಿಸಿ ಪಾತ್ರೆ → ಸ್ಪರ್ಶ ಇಲ್ಲದೆ ಕೈಗೆ ಉಷ್ಣ = ವಿಕಿರಣ!)"
        )
    },
    {
        "id": "radiation_kn_q3",
        "challenge": (
            "Show a FIRE source. Explain how distance affects radiant heat intensity "
            "— what happens to the intensity as you move further from the fire?\n\n"
            "(ಅಗ್ನಿಕುಂಡ ತೋರಿಸಿ — ದೂರ ಹೆಚ್ಚಾದಂತೆ ವಿಕಿರಣ ತೀವ್ರತೆ ಹೇಗೆ ಬದಲಾಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "fire"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'fire'. Then move the distance slider from 1 (HOT!) to 10 "
                "(Cool) to see how intensity drops rapidly with distance."
            ),
            "attempt_2": (
                "Set 'initialState' to 'fire'. Distance = 1 shows intensity near 100%; "
                "distance = 10 shows ~10%. Radiation spreads outward in all directions."
            ),
            "attempt_3": (
                "Choose 'fire': campfire radiates intensely at close range; intensity "
                "drops because the same energy now covers a larger spherical area."
            )
        },
        "concept_reminder": (
            "Radiation intensity decreases with distance from the source. "
            "Close to fire → high intensity (HOT!). Far from fire → low intensity (Cool). "
            "Radiated energy spreads outward in all directions — the same energy covers "
            "a larger area at greater distance → less energy per unit area. "
            "(ದೂರ ಹೆಚ್ಚಾದಂತೆ ತೀವ್ರತೆ ಕಡಿಮೆ: ವಿಕಿರಣ ಎಲ್ಲ ದಿಕ್ಕಿನಲ್ಲಿ ಹರಡುತ್ತದೆ!)"
        )
    }
]


# =============================================================================
# COMBINED HEAT TRANSFER SIMULATION (Chapter 7, sim7)
# ಸಂಯೋಜಿತ ಉಷ್ಣ ವರ್ಗಾವಣೆ – ಮೂರು ವಿಧಾನಗಳು ಒಟ್ಟಿಗೆ
# =============================================================================
SIMULATIONS_KN["combined_heat_transfer_kn"] = {
    "title": "ಸಂಯೋಜಿತ ಉಷ್ಣ ವರ್ಗಾವಣೆ (Combined Heat Transfer)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter7_simulation7_combined_heat_transfer_kn.html",

    "description": (
        "Kannada simulation showing all three heat-transfer modes (conduction, "
        "convection, radiation) occurring simultaneously in one cooking scenario. "
        "A pot of water on a stove illustrates: conduction (flame → metal pan), "
        "convection (hot water rises, cool water falls), radiation (heat felt by a "
        "person standing nearby). Students tap the three highlight tabs for a "
        "detailed explanation of each mode."
    ),

    "cannot_demonstrate": [
        "Quantitative comparison of the relative amounts of each transfer mode",
        "Heat transfer in a single-mode isolated system",
        "Effect of pan material on conduction rate"
    ],

    "initial_params": {"initialState": "conduction", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Heat Transfer Mode",
            "range": "conduction, convection, radiation",
            "url_key": "initialState",
            "effect": (
                "Sets which explanation tab is active when the simulation loads.\n"
                "  'conduction' → shows conduction: flame → pan → water bottom (default)\n"
                "  'convection' → shows convection: hot water rises, cool water sinks\n"
                "  'radiation'  → shows radiation: heat felt by person standing nearby"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Conduction: Flame → Metal Pan → Water at the Bottom",
            "description": (
                "Heat from the flame passes to the metal pan by conduction: metal "
                "atoms in the pan vibrate faster when heated and pass vibration "
                "energy to neighbouring atoms, conducting heat through the pan base."
            ),
            "key_insight": (
                "Conduction = particle-to-particle energy transfer in solids. "
                "Flame contacts pan → metal atoms vibrate → adjacent atoms vibrate "
                "→ heat spreads. Metals are good conductors because free electrons "
                "also carry thermal energy rapidly."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Convection: Hot Water Rises, Cool Water Falls — Circular Currents",
            "description": (
                "Inside the pan, convection drives uniform heating of all the water. "
                "The heated bottom water becomes less dense and rises; cooler surface "
                "water, being denser, sinks. This creates continuous circular convection "
                "currents visible as rising bubbles."
            ),
            "key_insight": (
                "Convection = fluid movement transfers heat. Hot fluid (less dense) "
                "rises; cool fluid (more dense) sinks. Circular current ensures ALL "
                "the water heats uniformly — without convection only the bottom would heat."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Radiation: Feeling Heat Near the Stove Without Touching It",
            "description": (
                "The hot pan and flame radiate infrared waves outward in all directions. "
                "A person standing to the side feels warmth without touching the pan or "
                "being in the rising hot-air stream — that is radiation in action."
            ),
            "key_insight": (
                "Radiation needs no medium. Hot stove radiates to your face even if you "
                "stand to the side, away from rising air. All three modes work "
                "SIMULTANEOUSLY in one cooking scene. Real life never uses only one mode!"
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["combined_heat_transfer_kn"] = [
    {
        "id": "combined_ht_kn_q1",
        "challenge": (
            "Select the CONDUCTION tab. In the pan-on-stove scenario, which part of "
            "the heat flow is caused by conduction and why?\n\n"
            "(ವಾಹಕತೆ ಟ್ಯಾಬ್ ಆಯ್ಕೆ ಮಾಡಿ — ಈ ದೃಶ್ಯದಲ್ಲಿ ವಾಹಕತೆ ಎಲ್ಲಿ ಸಂಭವಿಸುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "conduction"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'conduction'. The label 'ವಾಹಕತೆ: ಜ್ವಾಲೆ → ಪಾತ್ರೆ' "
                "shows where conduction occurs — direct flame-to-metal contact."
            ),
            "attempt_2": (
                "Choose 'conduction': direct contact between flame and metal pan → "
                "metal atoms vibrate → vibration travels through solid metal → pan heats up."
            ),
            "attempt_3": (
                "Set 'initialState=conduction': Conduction = particle vibration in solids. "
                "Flame touching pan base → metal gets hot. "
                "Metals are used for pans precisely because of their conductivity."
            )
        },
        "concept_reminder": (
            "Conduction in cooking: Heat flows FLAME → PAN → WATER BOTTOM. "
            "Mechanism: flame heats pan atoms → they vibrate → pass vibration to neighbours. "
            "Metals are good conductors because their FREE electrons carry thermal energy rapidly. "
            "This is why metal pans efficiently transfer heat from stove to food. "
            "(ನೇರ ಸಂಪರ್ಕ + ಕಣ ಕಂಪನ = ವಾಹಕತೆ!)"
        )
    },
    {
        "id": "combined_ht_kn_q2",
        "challenge": (
            "Show the CONVECTION tab. Explain the circular water movement inside the "
            "pan and why it is essential for heating all the water, not just the bottom.\n\n"
            "(ಸಂವಹನ ಟ್ಯಾಬ್ ಆಯ್ಕೆ ಮಾಡಿ — ನೀರು ಪಾತ್ರೆಯೊಳಗೆ ಯಾಕೆ ಸುತ್ತುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "convection"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'convection'. Watch the bubbles rise — hot water "
                "at the bottom is less dense, so it rises; cool water from the top sinks."
            ),
            "attempt_2": (
                "Choose 'convection': density difference drives the cycle. Hot water "
                "(bottom) → low density → rises. Cool water (top) → high density → sinks. "
                "Circular current forms!"
            ),
            "attempt_3": (
                "Set 'initialState=convection': without convection only the bottom layer "
                "heats. Convection mixes water, ensuring even heating throughout the pot."
            )
        },
        "concept_reminder": (
            "Convection in the pan: HOT water at bottom → low density → RISES. "
            "COOL water at top → high density → SINKS. "
            "Circular current → mixes water → UNIFORM heating. "
            "Convection only works in FLUIDS (liquids and gases) — not in solids! "
            "Rising bubbles you see = evidence of convection currents in action. "
            "(ಬಿಸಿ ನೀರು ಏರುತ್ತದೆ, ತಂಪು ಇಳಿಯುತ್ತದೆ = ಸಂವಹನ ಪ್ರವಾಹ!)"
        )
    },
    {
        "id": "combined_ht_kn_q3",
        "challenge": (
            "Show the RADIATION tab. Which part of the heat transfer in the scene is "
            "radiation and how does it differ from conduction and convection?\n\n"
            "(ವಿಕಿರಣ ಟ್ಯಾಬ್ ಆಯ್ಕೆ ಮಾಡಿ — ಈ ದೃಶ್ಯದಲ್ಲಿ ವಿಕಿರಣ ಎಲ್ಲಿ ಆಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "radiation"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'initialState' to 'radiation'. The person on the right feels warm "
                "without touching anything and without being in the rising hot-air stream. "
                "That warmth is radiation."
            ),
            "attempt_2": (
                "Choose 'radiation': orange waves from the pan show heat radiating outward. "
                "The person absorbs these infrared waves without any medium."
            ),
            "attempt_3": (
                "Set 'initialState=radiation': KEY difference — radiation travels through "
                "AIR and even vacuum. Conduction needs solid contact; convection needs fluid."
            )
        },
        "concept_reminder": (
            "Radiation in cooking: hot pan and flame radiate heat outward in all directions. "
            "Person nearby (not touching, not in direct hot-air stream) feels warm = RADIATION. "
            "COMPARISON: Conduction = solid contact needed. Convection = fluid medium needed. "
            "Radiation = NO medium needed — goes through air and even vacuum. "
            "All three happen simultaneously in one cooking scenario! "
            "(ಮಾಧ್ಯಮ ಇಲ್ಲದೆ ಉಷ್ಣ ತರಂಗ = ವಿಕಿರಣ!)"
        )
    }
]


# =============================================================================
# WATER CYCLE SIMULATION (Chapter 7, sim8)
# ಜಲ ಚಕ್ರ – ಸೂರ್ಯ ಚಾಲಿತ ನೀರಿನ ಚಕ್ರ
# =============================================================================
SIMULATIONS_KN["water_cycle_kn"] = {
    "title": "ಜಲ ಚಕ್ರ (Water Cycle)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter7_simulation8_water_cycle_kn.html",

    "description": (
        "Interactive Kannada water cycle simulation. Students tap stage labels "
        "(evaporation, condensation, precipitation, runoff, collection) or use "
        "Play / Step-by-Step buttons to explore each phase. The Sun drives the "
        "entire cycle; the simulation animates each stage with visual cues and "
        "a pop-up explanation for every stage."
    ),

    "cannot_demonstrate": [
        "Transpiration separately from evaporation",
        "Glaciers and polar ice as part of the cycle",
        "Quantitative water volume or flow rates"
    ],

    "initial_params": {"initialState": "initial", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Cycle Stage",
            "range": "initial, playing, evaporation, condensation, precipitation, runoff, collection",
            "url_key": "initialState",
            "effect": (
                "Sets which stage is shown and highlighted on load.\n"
                "  'initial'       → default view with instruction overlay (no stage)\n"
                "  'playing'       → auto-clicks Play All — all animations run continuously\n"
                "  'evaporation'   → highlights sun + evaporation arrows, shows info popup\n"
                "  'condensation'  → highlights clouds, shows condensation info popup\n"
                "  'precipitation' → activates rain cloud and raindrops, shows info popup\n"
                "  'runoff'        → activates runoff arrow, shows info popup\n"
                "  'collection'    → highlights ocean label, shows info popup"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "The Sun Drives the Water Cycle via Evaporation",
            "description": (
                "The Sun's heat converts liquid water from oceans, rivers, and lakes into "
                "invisible water vapour (evaporation). Without the Sun's energy input, "
                "evaporation stops and the entire water cycle ceases."
            ),
            "key_insight": (
                "Sun = the engine of the water cycle. Solar energy converts liquid water "
                "to gas (evaporation). Remove the sun → no evaporation → no clouds → "
                "no rain → all water stays on the ground. "
                "Plants also contribute water vapour via transpiration."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Condensation Forms Clouds; Precipitation Returns Water to Earth",
            "description": (
                "Rising water vapour cools at altitude. Cool air cannot hold as much "
                "vapour → vapour condenses into tiny water droplets → clouds form. "
                "When droplets grow heavy enough, they fall as precipitation "
                "(rain, snow, or hail depending on temperature)."
            ),
            "key_insight": (
                "Condensation = vapour → liquid droplets (clouds). "
                "Precipitation = cloud droplets too heavy → fall to Earth. "
                "Rain is the water the Sun evaporated, returned to Earth. "
                "Temperature determines form: above 0°C = rain; below = snow."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Runoff, Collection, and the Perpetual Cycle",
            "description": (
                "Fallen water runs off land into rivers (runoff) or seeps into the ground "
                "(infiltration). All water eventually collects in oceans, lakes, and rivers "
                "— ready to evaporate again. The cycle repeats without end."
            ),
            "key_insight": (
                "The water cycle never stops because the Sun continuously supplies energy. "
                "The same water molecules cycle repeatedly — the water you drink today "
                "may have been ocean water, vapour, rain, and river water across millions of years."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["water_cycle_kn"] = [
    {
        "id": "water_cycle_kn_q1",
        "challenge": (
            "Show the EVAPORATION stage of the water cycle. Explain why evaporation "
            "is called the first step and what energy source drives it.\n\n"
            "(ಆವಿಯಾಗುವಿಕೆ ಹಂತ ತೋರಿಸಿ — ಇದನ್ನು ಮೊದಲ ಹಂತ ಯಾಕೆ ಕರೆಯಲಾಗುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "evaporation"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'evaporation'. The sun glows actively and orange upward-arrows "
                "rise from the ocean toward the clouds."
            ),
            "attempt_2": (
                "Set 'initialState' to 'evaporation'. Evaporation starts the cycle — "
                "Sun's heat converts ocean/river water into invisible water vapour."
            ),
            "attempt_3": (
                "Choose 'evaporation': Sun energy → liquid water → water vapour (invisible gas) "
                "rising. This first step determines how much rain will eventually fall."
            )
        },
        "concept_reminder": (
            "Evaporation = liquid water → water vapour, driven by SUN's heat energy. "
            "Sources: oceans (70%), rivers, lakes, wet soil. Plants also release vapour (transpiration). "
            "Water vapour is INVISIBLE — clouds form only when it condenses into droplets. "
            "Without evaporation, there is no precipitation — the cycle starts here. "
            "(ಸೂರ್ಯ + ಸಮುದ್ರ → ಆವಿ → ಮೇಲೇರುತ್ತದೆ = ಆವಿಯಾಗುವಿಕೆ!)"
        )
    },
    {
        "id": "water_cycle_kn_q2",
        "challenge": (
            "Demonstrate the PRECIPITATION stage. Show how water falls from clouds "
            "and explain what determines whether it is rain, snow, or hail.\n\n"
            "(ಅವಕ್ಷೇಪಣ ಹಂತ ತೋರಿಸಿ — ಮಳೆ ಅಥವಾ ಹಿಮ ಎಂಬ ರೂಪ ಯಾವುದು ನಿರ್ಧರಿಸುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "precipitation"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'precipitation'. The dark rain cloud activates and "
                "raindrops fall from it. The 🌧️ label pulses to show the active stage."
            ),
            "attempt_2": (
                "Set 'initialState' to 'precipitation'. When cloud droplets grow too "
                "heavy, gravity pulls them down as precipitation."
            ),
            "attempt_3": (
                "Choose 'precipitation': cloud droplets coalesce → too heavy → fall. "
                "TEMPERATURE determines form: above 0°C = rain; near 0°C = sleet; below = snow."
            )
        },
        "concept_reminder": (
            "Precipitation = condensed cloud droplets coalesce until too heavy → FALL. "
            "Forms: RAIN (above 0°C all the way down), SNOW (below 0°C), HAIL (frozen in updrafts). "
            "India receives most rainfall June–September as southwest monsoon precipitation. "
            "The water cycle exists to move water from oceans back to land as precipitation. "
            "(ಮೋಡ ತುಂಬಿ ಭಾರವಾದಾಗ → ಮಳೆ/ಹಿಮ/ಆಲಿಕಲ್ಲಾಗಿ ಬೀಳುತ್ತದೆ = ಅವಕ್ಷೇಪಣ!)"
        )
    },
    {
        "id": "water_cycle_kn_q3",
        "challenge": (
            "Show the COLLECTION stage. Where does rain water eventually go before "
            "evaporation can restart the cycle?\n\n"
            "(ಸಂಗ್ರಹ ಹಂತ ತೋರಿಸಿ — ಮಳೆ ನೀರು ಕೊನೆಯಲ್ಲಿ ಎಲ್ಲಿ ಸೇರುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "collection"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'collection'. The ocean label activates — water from precipitation "
                "and runoff collects in oceans, lakes, rivers, and groundwater."
            ),
            "attempt_2": (
                "Set 'initialState' to 'collection'. After runoff and infiltration, "
                "water reaches the ocean → ready to evaporate again."
            ),
            "attempt_3": (
                "Choose 'collection': the ocean (covering 70% of Earth) is the main collector. "
                "From here the sun evaporates water again → cycle restarts."
            )
        },
        "concept_reminder": (
            "Collection = final stage where water gathers in: "
            "OCEANS (primary reservoir, ~97%), rivers, lakes, glaciers, groundwater (aquifers). "
            "From the ocean, Sun's heat triggers evaporation → cycle restarts. "
            "The same water molecules have been cycling for billions of years! "
            "Conservation of water: Earth's total water amount stays roughly constant. "
            "(ಸಮುದ್ರ + ನದಿ + ಸರೋವರ = ಸಂಗ್ರಹ → ಚಕ್ರ ಮತ್ತೆ ಪ್ರಾರಂಭ!)"
        )
    }
]


# =============================================================================
# INFILTRATION SIMULATION (Chapter 7, sim9)
# ಅಂತರ್ಸೇಚನ ಓಟ – ಯಾವ ಮಣ್ಣು ನೀರನ್ನು ವೇಗವಾಗಿ ಹೀರಿಕೊಳ್ಳುತ್ತದೆ?
# =============================================================================
SIMULATIONS_KN["infiltration_kn"] = {
    "title": "ಅಂತರ್ಸೇಚನ ಓಟ (Infiltration Race — Soil Types)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter7_simulation9_infiltration_kn.html",

    "description": (
        "Kannada infiltration race simulation. Three soil columns (gravel, sand, clay) "
        "race to show which allows water to seep through fastest. Students start the "
        "race by clicking 'Make It Rain'. Gravel wins (largest particles, biggest gaps); "
        "clay finishes last (tiny particles, almost no gaps). A results table shows all "
        "three finish times. Teaches how particle size determines infiltration rate and "
        "why clay soils and concrete surfaces cause flooding."
    ),

    "cannot_demonstrate": [
        "Mixed soil compositions such as loam",
        "Runoff vs infiltration split on impermeable hard surfaces",
        "Effect of soil compaction on infiltration rate"
    ],

    "initial_params": {"initialState": "initial", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Race State",
            "range": "initial, raining",
            "url_key": "initialState",
            "effect": (
                "Controls whether the infiltration race has been started.\n"
                "  'initial' → waiting state, soil columns visible, race not started (default)\n"
                "  'raining' → auto-clicks 'Make It Rain' after 800 ms to start the race"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept summary card at the top."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Infiltration Rate Depends on Particle Size (Gravel > Sand > Clay)",
            "description": (
                "Gravel particles are large, leaving large gaps — water passes quickly. "
                "Sand has medium particles with moderate gaps — medium speed. "
                "Clay particles are tiny and pack tightly — almost no gaps, very slow infiltration."
            ),
            "key_insight": (
                "Large particles → large gaps → fast infiltration (gravel wins). "
                "Tiny particles → tiny gaps → slow infiltration (clay loses). "
                "This relationship defines a soil's permeability."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Sandy / Gravelly Soil: Good Drainage and Groundwater Recharge",
            "description": (
                "Sandy and gravelly soils allow rain to infiltrate rapidly, reducing "
                "surface flooding and recharging underground aquifers (groundwater). "
                "Gravel is used in drainage systems precisely for this reason."
            ),
            "key_insight": (
                "Fast infiltration (gravel/sand): less flood risk, more groundwater recharge. "
                "Gardens and sports fields use sandy / gravelly material to avoid waterlogging. "
                "Gravel-lined drains exploit fast infiltration to clear water quickly."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Clay Soil and Concrete: Flood Risk and Groundwater Depletion",
            "description": (
                "Clay soils and impermeable surfaces like concrete prevent infiltration. "
                "Rain on clay or concrete cannot enter the ground and flows as surface "
                "runoff — increasing flood risk and depleting groundwater reserves."
            ),
            "key_insight": (
                "Clay + concrete cities = near-zero infiltration = all rain becomes runoff "
                "= floods AND groundwater not recharged = future water shortage. "
                "This is why urban planners now build permeable pavements and parks."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["infiltration_kn"] = [
    {
        "id": "infiltration_kn_q1",
        "challenge": (
            "Start the infiltration race (RAINING state). Observe which soil allows "
            "water to pass through fastest and explain why.\n\n"
            "(ಮಳೆ ಪ್ರಾರಂಭ ಮಾಡಿ — ಯಾವ ಮಣ್ಣು ನೀರನ್ನು ವೇಗವಾಗಿ ಒಳಕ್ಕೆ ಬಿಡುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "raining"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'raining'. Rain animation starts and water drops appear in all "
                "three columns. Watch which one reaches the aquifer first."
            ),
            "attempt_2": (
                "Set 'initialState' to 'raining'. Race result: gravel (⚡ FAST!), "
                "sand (💧 Medium), clay (🐢 Slow)."
            ),
            "attempt_3": (
                "Choose 'raining': gravel wins because large particles leave large gaps "
                "for water to flow through quickly."
            )
        },
        "concept_reminder": (
            "Infiltration race result: GRAVEL (1st) → SAND (2nd) → CLAY (3rd). "
            "Gravel wins: large particles = large pores = fast water flow path. "
            "Same physics as wide pipe vs narrow pipe — bigger opening = faster flow. "
            "Clay loses: tiny particles pack together → almost no pores → water barely seeps. "
            "(ದೊಡ್ಡ ಕಣ = ದೊಡ್ಡ ಅಂತರ = ನೀರು ವೇಗ → ಜಲ್ಲಿ ಗೆಲ್ಲುತ್ತದೆ!)"
        )
    },
    {
        "id": "infiltration_kn_q2",
        "challenge": (
            "Show the INITIAL state (before rain). Just by looking at the three soil "
            "columns, predict which will be fastest and explain your reasoning.\n\n"
            "(ಮಳೆ ಮೊದಲಿನ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಮೂರು ಮಣ್ಣಿನ ಸ್ತಂಭ ನೋಡಿ ಮುಂಚಿತವಾಗಿ ಊಹಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "initial"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'initial' to see the soil columns before rain. Observe particle "
                "sizes — gravel has large visible stones; sand has tiny dots; clay is very fine."
            ),
            "attempt_2": (
                "Set 'initialState' to 'initial'. Bigger particles = bigger gaps between them "
                "= more space for water to flow. Gravel should win (prediction)."
            ),
            "attempt_3": (
                "Choose 'initial': the initial view lets you predict from visual reasoning. "
                "This is scientific method — predict then observe to confirm."
            )
        },
        "concept_reminder": (
            "Before the race, use visual reasoning: "
            "Gravel column → large round stones with clear visible gaps → FAST. "
            "Sand column → many tiny grains, moderate gaps → MEDIUM. "
            "Clay column → so many fine particles that gaps are almost invisible → SLOW. "
            "PREDICTION → OBSERVATION → CONFIRMATION = the scientific method in action. "
            "(ಕಣ ಗಾತ್ರ ನೋಡಿ ಊಹಿಸು, ಮಳೆ ಅಳಿದ ಮೇಲೆ ದೃಢೀಕರಿಸು!)"
        )
    },
    {
        "id": "infiltration_kn_q3",
        "challenge": (
            "Run the infiltration race (RAINING state). Explain the real-world "
            "consequence: why do clay soils cause flooding while gravel reduces it?\n\n"
            "(ಮಳೆ ಓಟ ತೋರಿಸಿ — ಮಣ್ಣಿನ ಅಂತರ್ಸೇಚನ ದರ ಪ್ರಾಕೃತಿಕ ಮತ್ತು ನಗರ ಪ್ರಭಾವ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "raining"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'raining'. Watch clay — water barely infiltrates. When rain falls "
                "faster than clay can absorb it, the excess flows on the surface = flooding."
            ),
            "attempt_2": (
                "Set 'initialState=raining'. Clay near-zero infiltration → runoff → floods. "
                "Gravel → rain soaks in immediately → no runoff → no flood."
            ),
            "attempt_3": (
                "Choose 'raining': the takeaway section explains real impacts. "
                "Gravel-lined drains = fast drainage. Concrete cities = clay-like = flood-prone."
            )
        },
        "concept_reminder": (
            "Real-world infiltration impact: "
            "HIGH infiltration (gravel/sand): rain soaks into ground → no surface runoff "
            "→ no flood → groundwater recharged → long-term water availability. "
            "LOW infiltration (clay/concrete): rain stays on surface → runoff → FLOODS "
            "→ groundwater NOT recharged → water shortage later. "
            "City solution: permeable pavements, parks, and gravel paths allow infiltration. "
            "(ಹೆಚ್ಚು ಅಂತರ್ಸೇಚನ = ಪ್ರವಾಹ ಕಡಿಮೆ + ಭೂಜಲ ಹೆಚ್ಚು!)"
        )
    }
]


# =============================================================================
# SPEEDOMETER SIMULATION (Chapter 8, sim10)
# ಸ್ಪೀಡೋಮೀಟರ್ ಮತ್ತು ಓಡೋಮೀಟರ್ – ತ್ವರಿತ ವೇಗ vs ಒಟ್ಟು ಅಂತರ
# =============================================================================
SIMULATIONS_KN["speedometer_kn"] = {
    "title": "ಸ್ಪೀಡೋಮೀಟರ್ ಮತ್ತು ಓಡೋಮೀಟರ್ (Speedometer and Odometer)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation10_speedometer_kn.html",

    "description": (
        "Interactive Kannada vehicle dashboard simulation. Students press and hold "
        "the gas pedal to accelerate (0–240 km/h) and brake to decelerate. The "
        "speedometer needle rotates, the digital speed display changes colour by zone "
        "(green / yellow / red), and the odometer accumulates total distance. A trip "
        "meter can be reset. Teaches the difference between instantaneous speed "
        "(speedometer) and total distance (odometer)."
    ),

    "cannot_demonstrate": [
        "Calculating travel time from speed and distance",
        "Average speed vs instantaneous speed distinction quantitatively",
        "Velocity (direction + magnitude) vs speed (magnitude only)"
    ],

    "initial_params": {"initialState": "stopped", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Speed State",
            "range": "stopped, slow, medium, fast",
            "url_key": "initialState",
            "effect": (
                "Sets the initial speed shown on the speedometer on load.\n"
                "  'stopped' → 0 km/h, needle at far left (default)\n"
                "  'slow'    → 40 km/h, needle in green safe zone\n"
                "  'medium'  → 100 km/h, needle at yellow zone (highway speed)\n"
                "  'fast'    → 200 km/h, needle at red danger zone"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and fun-fact panel."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Speedometer Shows Instantaneous Speed",
            "description": (
                "The speedometer displays how fast the vehicle is moving at THIS EXACT "
                "MOMENT — the instantaneous speed in km/h. It changes continuously as "
                "the driver accelerates or brakes."
            ),
            "key_insight": (
                "Speedometer = INSTANTANEOUS SPEED. Push gas → needle rises immediately. "
                "Press brake → needle falls immediately. Speed limits on road signs are "
                "checked against the speedometer — not average speed."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Odometer Records Total Distance Travelled",
            "description": (
                "The odometer is a cumulative counter that adds up ALL the distance the "
                "vehicle has ever travelled. It never decreases unless manually reset. "
                "The trip meter (sub-odometer) can be reset for individual journeys."
            ),
            "key_insight": (
                "Odometer = TOTAL DISTANCE (accumulated). Speedometer = speed right now. "
                "Buying a second-hand car: check odometer to know total usage. "
                "Service is due every 5,000 km — tracked by odometer, not calendar."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Speed and Distance: Speed = Distance ÷ Time",
            "description": (
                "Speedometer and odometer together let us apply: Speed = Distance ÷ Time. "
                "If you travel 100 km (odometer) in 2 hours, your average speed was 50 km/h. "
                "The two instruments measure different but mathematically linked quantities."
            ),
            "key_insight": (
                "v = d / t. Speedometer gives instantaneous v; odometer gives cumulative d. "
                "Average speed = total distance (odometer) ÷ total travel time. "
                "Display colour zones give safety feedback: green (safe) → yellow (caution) → red (danger)."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["speedometer_kn"] = [
    {
        "id": "speedometer_kn_q1",
        "challenge": (
            "Set the simulation to SLOW speed (40 km/h). Explain what the speedometer "
            "reading tells us and why speed is described as 'instantaneous'.\n\n"
            "(ನಿಧಾನ ವೇಗ ತೋರಿಸಿ — ಸ್ಪೀಡೋಮೀಟರ್ ಏನು ಅಳೆಯುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "slow"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'slow'. The needle points to ~40 km/h in the green safe zone. "
                "This is typical city driving speed."
            ),
            "attempt_2": (
                "Set 'initialState' to 'slow'. 40 km/h = instantaneous speed: the vehicle "
                "covers 40 km if it maintains this speed for one hour."
            ),
            "attempt_3": (
                "Choose 'slow': the speedometer updates continuously as speed changes — "
                "it always shows 'right now' speed. Press gas → needle jumps immediately."
            )
        },
        "concept_reminder": (
            "Speedometer shows INSTANTANEOUS speed = your speed at this exact second. "
            "40 km/h means: if you maintained this speed for 1 hour, you would cover 40 km. "
            "Speed is NOT constant during a journey — it rises and falls. "
            "That is why speedometer reading and average speed are DIFFERENT concepts. "
            "Speed limit signs are checked against the speedometer reading. "
            "(ಸ್ಪೀಡೋಮೀಟರ್ = ಈ ಕ್ಷಣದ ತ್ವರಿತ ವೇಗ!)"
        )
    },
    {
        "id": "speedometer_kn_q2",
        "challenge": (
            "Set the simulation to FAST speed (200 km/h). What happens to the display "
            "colour and what is the real-world safety implication of such speed?\n\n"
            "(ತೀವ್ರ ವೇಗ ತೋರಿಸಿ — ಸೂಚಕ ಬಣ್ಣ ಏನಾಗುತ್ತದೆ, ಸುರಕ್ಷತೆ ಬಗ್ಗೆ ಏನು?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "fast"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'fast'. The needle swings far right to 200 km/h and the "
                "digital display turns RED. This is the danger zone."
            ),
            "attempt_2": (
                "Set 'initialState' to 'fast'. At 200 km/h the display goes red — "
                "alerting that this speed far exceeds safe road limits."
            ),
            "attempt_3": (
                "Choose 'fast': at 200 km/h braking distance is around 4× longer "
                "than at 100 km/h, dramatically increasing crash severity."
            )
        },
        "concept_reminder": (
            "At 200 km/h: digital display turns RED = danger zone. "
            "Why dangerous: braking distance at 200 km/h is ~4× longer than at 100 km/h. "
            "High speed also magnifies the effect of driver errors. "
            "India highway speed limit: 120 km/h; city: 50 km/h. "
            "Colour zones: green (safe) → yellow (highway caution) → RED (dangerous, slow down). "
            "(200 km/h = ಅಪಾಯ ವಲಯ = ಕೆಂಪು ಬಣ್ಣ = ವೇಗ ಕಡಿಮೆ ಮಾಡಿ!)"
        )
    },
    {
        "id": "speedometer_kn_q3",
        "challenge": (
            "Show the STOPPED state (0 km/h). The odometer still shows accumulated "
            "distance. Explain the key difference between the speedometer (zero) and "
            "the odometer (non-zero) readings.\n\n"
            "(ನಿಂತ ಸ್ಥಿತಿ ತೋರಿಸಿ — ಸ್ಪೀಡೋಮೀಟರ್ ಶೂನ್ಯ ಆದರೆ ಓಡೋಮೀಟರ್ ಶೂನ್ಯ ಅಲ್ಲ — ಯಾಕೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "stopped"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'stopped'. Needle at 0, but odometer shows total accumulated "
                "distance from previous travel. Speed can be 0 while past distance persists."
            ),
            "attempt_2": (
                "Set 'initialState' to 'stopped'. Speedometer = current instantaneous "
                "speed (now 0). Odometer = TOTAL distance ever driven — never auto-resets."
            ),
            "attempt_3": (
                "Choose 'stopped': the car is not moving (speed = 0) but it previously "
                "covered some distance (odometer > 0). These are two different measurements."
            )
        },
        "concept_reminder": (
            "KEY DISTINCTION: "
            "SPEEDOMETER = current instantaneous speed. Zero = not moving right now. "
            "ODOMETER = total accumulated distance (all past journeys added). "
            "Odometer never goes to 0 automatically — only manual reset. "
            "Analogy: speedometer = your running speed THIS second. "
            "Odometer = total steps you have ever walked in your life. "
            "(ಸ್ಪೀಡೋಮೀಟರ್ = ಈಗಿನ ವೇಗ | ಓಡೋಮೀಟರ್ = ಒಟ್ಟು ಅಂತರ = ಎರಡು ಭಿನ್ನ ಅಳತೆಗಳು!)"
        )
    }
]


# =============================================================================
# HISTORICAL CLOCKS SIMULATION (Chapter 8, sim1)
# ಸಮಯ ಮಾಪನದ ಇತಿಹಾಸ – ಸೂರ್ಯ ಘಡಿಯಾರದಿಂದ ಅಣು ಗಡಿಯಾರದವರೆಗೆ
# =============================================================================
SIMULATIONS_KN["historical_clocks_kn"] = {
    "title": "ಸಮಯ ಮಾಪನದ ಇತಿಹಾಸ (Historical Clocks — Evolution of Timekeeping)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation1_historical_clocks_kn.html",

    "description": (
        "Kannada interactive timeline of six timekeeping devices: sundial, water clock "
        "(clepsydra / ghatika-yantra), hourglass, candle clock, pendulum clock, and "
        "quartz clock. Students tap each timeline item to see a live animation of that "
        "device in action and read how it works. A precision chart shows the accuracy "
        "improvement from ~30 minutes (sundial) to sub-microsecond (atomic clock)."
    ),

    "cannot_demonstrate": [
        "Atomic clock / caesium standard in detail",
        "Quantitative calculation of precision improvement",
        "How different latitudes affect sundial accuracy",
    ],

    "initial_params": {"initialState": "sundial", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Clock Type",
            "range": "sundial, water, hourglass, candle, pendulum, quartz",
            "url_key": "initialState",
            "effect": (
                "Selects which historical clock is active on the timeline on load.\n"
                "  'sundial'   → shadow-based solar clock (~3500 BCE Egypt, default)\n"
                "  'water'     → clepsydra / ghatika-yantra (~1500 BCE India)\n"
                "  'hourglass' → sand glass (~8th century)\n"
                "  'candle'    → marked candle clock (~9th century)\n"
                "  'pendulum'  → Huygens pendulum clock (1656 CE)\n"
                "  'quartz'    → crystal-oscillation clock (1927 CE)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and precision-evolution takeaway box."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "All Clocks Rely on a Regular, Repeating Process",
            "description": (
                "Every clock — from the sundial to the quartz watch — works by counting "
                "the number of completed repetitions of some periodic process: "
                "the shadow arc of the Sun, water drips, sand grains falling, "
                "candle burning, pendulum swings, or crystal vibrations."
            ),
            "key_insight": (
                "The key requirement for any clock: a REGULAR repeating event. "
                "Fast + regular = accurate. Sundial period = 24 hours (too slow for minutes). "
                "Quartz crystal = 32,768 oscillations per second (very regular = very accurate)."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Pendulum Clock: Isochronism Gives the First Minute-Accurate Clock",
            "description": (
                "Galileo discovered that a pendulum of fixed length always takes the "
                "same time for one swing — regardless of how wide the swing is "
                "(isochronism). Huygens (1656) built the first pendulum clock, accurate "
                "to about 15 seconds per day — 100× better than any previous clock."
            ),
            "key_insight": (
                "Isochronism = equal time for each swing = reliable clock. "
                "T = 2π√(L/g) — only length matters. "
                "A 1-metre pendulum swings exactly once per second → called a 'seconds pendulum'. "
                "This is WHY grandfather clocks have long pendulums."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Quartz Crystal: 32,768 Vibrations per Second for Mass-Market Accuracy",
            "description": (
                "Quartz crystals vibrate at exactly 32,768 Hz when an electric current "
                "is applied (piezoelectric effect). Digital circuits count these vibrations. "
                "Quartz watches are accurate to ~1 second per day and cost very little "
                "to manufacture — replacing mechanical clocks globally after ~1969."
            ),
            "key_insight": (
                "32,768 = 2^15 vibrations/second → dividing by 2 fifteen times gives exactly 1 Hz "
                "(1 tick per second). Binary division is easy in digital circuits. "
                "Modern atomic clocks go further: error of 1 second in 300 million years."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["historical_clocks_kn"] = [
    {
        "id": "hist_clocks_kn_q1",
        "challenge": (
            "Select the PENDULUM CLOCK on the timeline. Explain the key property of a "
            "pendulum that makes it suitable for accurate timekeeping.\n\n"
            "(ಊಸರವಳಿ ಗಡಿಯಾರ ಆಯ್ಕೆ ಮಾಡಿ — ಯಾವ ಗುಣ ಆಧಾರದಲ್ಲಿ ಇದು ನಿಖರ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "pendulum"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'pendulum' from the clock timeline. The animation shows a clock "
                "with a swinging pendulum. The key word is 'isochronism'."
            ),
            "attempt_2": (
                "Set 'initialState' to 'pendulum'. Isochronism = every swing takes the "
                "same time regardless of swing width. T = 2π√(L/g)."
            ),
            "attempt_3": (
                "Choose 'pendulum': Huygens 1656 — accuracy jumped from ±30 min/day "
                "(sundial) to ±15 sec/day using isochronism of the pendulum."
            )
        },
        "concept_reminder": (
            "Pendulum clock key property: ISOCHRONISM — every swing takes equal time. "
            "T = 2π√(L/g): period depends only on length and gravity, not swing width. "
            "1 metre pendulum → 1 second per swing = 'seconds pendulum' → grandfather clocks. "
            "Huygens 1656: accuracy 15 sec/day (100× better than water/hour-glass clocks). "
            "(ಊಸರವಳಿ: ಎಲ್ಲ ತೂಗಾಡುವಿಕೆ ಸಮಾನ ಸಮಯ = ಸಮಗಾಮಿತ್ವ!)"
        )
    },
    {
        "id": "hist_clocks_kn_q2",
        "challenge": (
            "Select the QUARTZ CLOCK. How does a quartz crystal measure time and "
            "why is the number 32,768 significant?\n\n"
            "(ಕ್ವಾರ್ಟ್ಜ್ ಗಡಿಯಾರ ಆಯ್ಕೆ ಮಾಡಿ — 32,768 ಸಂಖ್ಯೆ ಮಹತ್ವ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "quartz"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'quartz'. The label says '32,768 Hz'. "
                "This number is a power of 2 — important for digital circuits."
            ),
            "attempt_2": (
                "Set 'initialState' to 'quartz'. The crystal vibrates 32,768 times/sec. "
                "32,768 = 2^15. Divide by 2 fifteen times → 1 Hz = 1 tick per second."
            ),
            "attempt_3": (
                "Choose 'quartz': piezoelectric crystal vibrates at constant 32,768 Hz "
                "when current applied. Binary counter chip counts these vibrations."
            )
        },
        "concept_reminder": (
            "Quartz clock: crystal vibrates at 32,768 Hz (32,768 = 2^15 — binary power). "
            "Circuit counts vibrations and divides by 2 fifteen times → 1 tick/second. "
            "Accuracy: ~1 second/day — far better than pendulum (15 sec/day). "
            "Piezoelectric effect: mechanical stress produces electric voltage and vice versa. "
            "Result: cheap, accurate clocks available to everyone after ~1969. "
            "(32,768 Hz = 2^15 → 15 ಬಾರಿ 2 ರಿಂದ ಭಾಗಿಸಿ = 1 Hz = 1 ಟಿಕ್!)"
        )
    },
    {
        "id": "hist_clocks_kn_q3",
        "challenge": (
            "Select the WATER CLOCK (Clepsydra). This was an important timekeeping device "
            "in ancient India (ಘಟಿಕಾ-ಯಂತ್ರ). How does it measure time?\n\n"
            "(ನೀರು ಗಡಿಯಾರ ಆಯ್ಕೆ ಮಾಡಿ — ಭಾರತದ ಘಟಿಕಾ-ಯಂತ್ರ ಹೇಗೆ ಕೆಲ್ಸ ಮಾಡುತ್ತದೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "water"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'water' to see the clepsydra animation. The water level drops "
                "at a steady rate — marks on the side indicate how much time has passed."
            ),
            "attempt_2": (
                "Set 'initialState' to 'water'. "
                "The ghatika-yantra (Indian version ~1500 BCE) used a small vessel with "
                "a hole — it sinks in water after a fixed time interval."
            ),
            "attempt_3": (
                "Choose 'water': water flows out at a constant rate from a small hole. "
                "When the vessel is empty, one 'ghatika' (24 minutes) has passed."
            )
        },
        "concept_reminder": (
            "Water clock (Clepsydra): water drips out at a CONSTANT RATE from a small hole. "
            "The falling water level (or time until full vessel sinks) measures elapsed time. "
            "Indian ghatika-yantra (~1500 BCE): small copper vessel with hole sinks in 24 min = 1 ghatika. "
            "Advantage over sundial: works at NIGHT and on cloudy days. "
            "Limitation: water flow rate changes with temperature; vessel not perfectly cylindrical. "
            "(ಸ್ಥಿರ ನೀರು ಹರಿವು → ಮಟ್ಟ ಇಳಿತ → ಸಮಯ ಮಾಪನ = ನೀರು ಗಡಿಯಾರ!)"
        )
    }
]


# =============================================================================
# SUNDIAL SIMULATION (Chapter 8, sim2)
# ಸಂವಾದಾತ್ಮಕ ಸೂರ್ಯ ಘಡಿಯಾರ – ಸೂರ್ಯ ಆಕಾಶದಲ್ಲಿ ಚಲಿಸಿದಂತೆ
# =============================================================================
SIMULATIONS_KN["sundial_kn"] = {
    "title": "ಸಂವಾದಾತ್ಮಕ ಸೂರ್ಯ ಘಡಿಯಾರ (Interactive Sundial — Shadow & Rotation)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation2_sundial_kn.html",

    "description": (
        "Interactive Kannada sundial simulation. Students drag a slider to move the "
        "Sun across the sky arc from 6 AM to 6 PM. The gnomon shadow rotates in real "
        "time, pointing to the corresponding hour mark on the dial face. The displayed "
        "clock time updates continuously. Teaches Earth's rotation, shadow direction, "
        "and the limitations of sundials (night, clouds, latitude correction)."
    ),

    "cannot_demonstrate": [
        "Sundial accuracy variation by latitude",
        "Equation of time (difference between solar and clock time)",
        "Night-time timekeeping",
    ],

    "initial_params": {"hour": 12, "showHints": True},

    "parameter_info": {
        "hour": {
            "label": "Time of Day",
            "range": "6–18 (float, e.g. 6.0 = 6:00 AM, 13.5 = 1:30 PM)",
            "url_key": "hour",
            "effect": (
                "Sets the Sun position on the arc and updates the shadow angle.\n"
                "  6.0  → sunrise, shadow points hard right\n"
                " 12.0  → noon, shadow points straight down (Sun overhead, default)\n"
                " 18.0  → sunset, shadow points hard left"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and limitations panel."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Earth Rotates 15° per Hour — Causing the Sun's Apparent Movement",
            "description": (
                "The Sun appears to move from east to west across the sky because Earth "
                "rotates eastward at 15° per hour (360° / 24 hours). The gnomon (vertical "
                "rod) casts a shadow that sweeps the dial face by 15° every hour."
            ),
            "key_insight": (
                "Earth rotates 360° in 24 hours = 15°/hour. "
                "Shadow sweeps 15°/hour on the dial = one hour mark per 15°. "
                "The Sun does NOT move — Earth moves. Shadow = Earth's rotation made visible."
            ),
            "related_params": ["hour"]
        },
        {
            "id": 2,
            "title": "Gnomon Shadow Points Opposite to the Sun",
            "description": (
                "When the Sun is in the east (morning), the shadow points west. "
                "At noon, the Sun is (nearly) due south in the Northern Hemisphere, "
                "so the shadow is at its shortest, pointing north. "
                "In the evening, the shadow points east."
            ),
            "key_insight": (
                "Shadow always points AWAY from the Sun. "
                "Noon = shortest shadow (Sun highest). "
                "Morning = long shadow pointing west. Evening = long shadow pointing east. "
                "Longer shadow = lower Sun = greater angle from vertical."
            ),
            "related_params": ["hour"]
        },
        {
            "id": 3,
            "title": "Sundial Limitations: Night, Clouds, and Latitude",
            "description": (
                "Sundials fail completely at night (no Sun), fail on cloudy days "
                "(shadow blocked), and must be recalibrated for different latitudes "
                "because the Sun's arc across the sky changes with location. "
                "Accuracy is only ~15–30 minutes."
            ),
            "key_insight": (
                "Limits of sundial → need for other methods (water clock, candle, pendulum). "
                "Each limitation drove a new invention. "
                "No universal time until pendulum clock (1656) and later atomic clocks."
            ),
            "related_params": ["hour", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["sundial_kn"] = [
    {
        "id": "sundial_kn_q1",
        "challenge": (
            "Set the sundial to NOON (12:00 PM). Observe the shadow length and direction. "
            "Why is the shadow at its shortest at noon?\n\n"
            "(ಮಧ್ಯಾಹ್ನ 12 ಗಂಟೆಗೆ ಸ್ಲೈಡರ್ ಹೊಂದಿಸಿ — ನೆರಳು ಚಿಕ್ಕದಾಗಿರಲು ಕಾರಣ ಹೇಳಿ)"
        ),
        "target_parameters": ["hour"],
        "success_rule": {
            "conditions": [
                {"parameter": "hour", "operator": "==", "value": "12"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set the 'hour' slider to 12. The Sun is at its highest point in the sky. "
                "The shadow is shortest and points almost straight down."
            ),
            "attempt_2": (
                "Set 'hour = 12'. At noon the Sun is due south (highest elevation). "
                "The higher the Sun, the more vertical the rays, the shorter the shadow."
            ),
            "attempt_3": (
                "Choose hour = 12: Sun highest → rays near vertical → gnomon shadow falls "
                "straight down and is shortest. Sundial reads 12."
            )
        },
        "concept_reminder": (
            "At noon (12:00 PM): Sun is at its HIGHEST point in the sky. "
            "High Sun = nearly vertical rays = SHORT shadow. "
            "Short shadow points toward north (in Northern Hemisphere). "
            "As Sun rises higher → shadow gets shorter; as Sun sets lower → shadow lengthens. "
            "Longest shadows: early morning and late evening (Sun low on horizon). "
            "(ಮಧ್ಯಾಹ್ನ = ಸೂರ್ಯ ಅತಿ ಮೇಲೆ = ನೆರಳು ಅತಿ ಚಿಕ್ಕದು!)"
        )
    },
    {
        "id": "sundial_kn_q2",
        "challenge": (
            "Move the slider to early morning (6:00 AM / hour = 6). Describe the shadow "
            "direction and explain why it points the way it does.\n\n"
            "(ಬೆಳಿಗ್ಗೆ 6 ಗಂಟೆಗೆ ಹೊಂದಿಸಿ — ನೆರಳು ಯಾವ ದಿಕ್ಕಿನಲ್ಲಿ ಇರುತ್ತದೆ ಮತ್ತು ಯಾಕೆ?)"
        ),
        "target_parameters": ["hour"],
        "success_rule": {
            "conditions": [
                {"parameter": "hour", "operator": "==", "value": "6"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set the slider to hour = 6 (sunrise). Sun is on the eastern horizon. "
                "Shadow points in the OPPOSITE direction — toward the west."
            ),
            "attempt_2": (
                "hour = 6: Sun rises in the east → shadow cast toward the west. "
                "Long shadow because Sun barely above horizon → nearly horizontal rays."
            ),
            "attempt_3": (
                "Choose hour = 6: shadow angle is about +75° (far right on dial = pointing west). "
                "Dial reads '6' because it is 6 AM."
            )
        },
        "concept_reminder": (
            "At sunrise (6 AM): Sun is on the eastern horizon. "
            "Shadow always points OPPOSITE to the Sun. "
            "Sun in east → shadow points WEST (long shadow, nearly horizontal). "
            "Earth rotates eastward → Sun appears to rise in east. "
            "Shadow sweeps 15° per hour across the dial as Earth rotates. "
            "(ಸೂರ್ಯ ಪೂರ್ವದಲ್ಲಿ → ನೆರಳು ಪಶ್ಚಿಮಕ್ಕೆ — ಮತ್ತೆ ನೇರ ವಿರುದ್ಧ!)"
        )
    },
    {
        "id": "sundial_kn_q3",
        "challenge": (
            "Move the slider to evening (hour = 17 / 5:00 PM). Observe the shadow. "
            "Now compare morning and evening shadows — what is the key difference?\n\n"
            "(ಸಂಜೆ 5 ಗಂಟೆಗೆ ಹೊಂದಿಸಿ — ಬೆಳಿಗ್ಗೆ ಮತ್ತು ಸಂಜೆ ನೆರಳಿನ ವ್ಯತ್ಯಾಸ ಏನು?)"
        ),
        "target_parameters": ["hour"],
        "success_rule": {
            "conditions": [
                {"parameter": "hour", "operator": "==", "value": "17"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set hour = 17. Evening sun is in the west → shadow now points east. "
                "Compare with morning (hour = 6) where shadow pointed west."
            ),
            "attempt_2": (
                "hour = 17: Sun has travelled from east (morning) to west (evening). "
                "Shadow has swept from +75° (west) through 0° (noon) to -75° (east)."
            ),
            "attempt_3": (
                "Morning shadow = points west; Evening shadow = points east. "
                "Both are long (low Sun) but in OPPOSITE directions."
            )
        },
        "concept_reminder": (
            "Shadow direction comparison: "
            "MORNING (6 AM): Sun in EAST → shadow points WEST (long). "
            "NOON (12 PM): Sun overhead → shadow points straight down (shortest). "
            "EVENING (5-6 PM): Sun in WEST → shadow points EAST (long). "
            "Pattern: shadow sweeps from west → north → east across the dial as the day passes. "
            "Earth rotates 360° / 24 hours = 15° per hour → shadow moves 15°/hour on dial. "
            "(ಸೂರ್ಯ ಪೂರ್ವ→ಪಶ್ಚಿಮ, ನೆರಳು ಪಶ್ಚಿಮ→ಪೂರ್ವ!)"
        )
    }
]


# =============================================================================
# SIMPLE PENDULUM SIMULATION (Chapter 8, sim3)
# ಸರಳ ಲೋಲಕ – ಉದ್ದ ಮತ್ತು ದ್ರವ್ಯರಾಶಿ ಪ್ರಯೋಗ
# =============================================================================
SIMULATIONS_KN["pendulum_kn"] = {
    "title": "ಸರಳ ಲೋಲಕ (Simple Pendulum — Length, Mass, and Period)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation3_pendulum_kn.html",

    "description": (
        "Interactive Kannada pendulum simulation with two independent sliders: "
        "string length (50–200 cm) and bob mass (50–200 g). Students can start the "
        "pendulum swinging and watch it count complete oscillations. The formula "
        "T = 2π√(L/g) is displayed and updates live with the measurements panel "
        "showing calculated period and frequency. Mass changes make the bob visually "
        "larger/heavier but do NOT change the period."
    ),

    "cannot_demonstrate": [
        "Effect of amplitude on period (small-angle approximation used)",
        "Pendulum on different planets (fixed g = 9.8 m/s²)",
        "Damping due to air resistance in detail",
    ],

    "initial_params": {"initialState": "stopped", "length": 100, "mass": 100, "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Swing State",
            "range": "stopped, swinging",
            "url_key": "initialState",
            "effect": (
                "Controls whether the pendulum starts swinging on load.\n"
                "  'stopped'  → pendulum at rest at centre (default)\n"
                "  'swinging' → auto-starts pendulum after 800 ms"
            )
        },
        "length": {
            "label": "String Length (cm)",
            "range": "50–200 (integer, cm)",
            "url_key": "length",
            "effect": (
                "Sets the pendulum string length slider.\n"
                "  50  → short string → fast swing (~1.4 s period)\n"
                " 100  → default length (~2.0 s period)\n"
                " 200  → long string → slow swing (~2.8 s period)"
            )
        },
        "mass": {
            "label": "Bob Mass (g)",
            "range": "50–200 (integer, grams)",
            "url_key": "mass",
            "effect": (
                "Sets the bob mass slider. Large mass → visually heavier bob. "
                "However, changing mass does NOT change the oscillation period "
                "(demonstrates mass independence)."
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides concept card, formula box, and takeaway."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Pendulum Period Depends ONLY on String Length",
            "description": (
                "T = 2π√(L/g). The period (T) of a pendulum depends on string length (L) "
                "and gravitational acceleration (g). It does NOT depend on the bob's mass "
                "or the amplitude of swing (for small angles). This is Galileo's discovery."
            ),
            "key_insight": (
                "Length makes a pendulum slower (longer string = longer period). "
                "Double the length → period increases by √2 = 1.41× (not double). "
                "Mass is completely irrelevant to period — change it and T stays the same."
            ),
            "related_params": ["length", "initialState"]
        },
        {
            "id": 2,
            "title": "Mass Independence: Heavy and Light Bobs Swing at the Same Rate",
            "description": (
                "Students often expect a heavier bob to swing slower. In reality, "
                "the restoring force (gravity component) and the inertia both scale "
                "with mass, so they cancel out. A 50 g bob and a 200 g bob on the "
                "same string complete each swing in identical time."
            ),
            "key_insight": (
                "Mass independence is counterintuitive but experimentally verifiable. "
                "This is related to the equivalence of gravitational and inertial mass "
                "— the same principle that makes all objects fall at the same rate."
            ),
            "related_params": ["mass", "initialState"]
        },
        {
            "id": 3,
            "title": "The Pendulum as a Clock: Why Clocks Use Long Pendulums",
            "description": (
                "A 1-metre pendulum has a period of almost exactly 2 seconds (1 s each way). "
                "Pendulum clocks exploit this to count seconds reliably. Grandfather clocks "
                "use a 1-metre pendulum; the 'tick' and 'tock' are the two half-swings."
            ),
            "key_insight": (
                "L = 1 m → T = 2π√(1/9.8) ≈ 2 s. "
                "Each half-swing = 1 second = 1 tick on the clock mechanism. "
                "Longer pendulum → ticks slower → clock runs slow. "
                "This is how grandma would adjust her clock: shorten pendulum to speed up."
            ),
            "related_params": ["length", "initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["pendulum_kn"] = [
    {
        "id": "pendulum_kn_q1",
        "challenge": (
            "Set the pendulum to its MAXIMUM length (200 cm) and start it swinging. "
            "Observe the period and explain how a longer pendulum relates to clock design.\n\n"
            "(ಅತ್ಯಧಿಕ ಉದ್ದ 200 ಸೆಂ ಹೊಂದಿಸಿ, ಊಸರವಳಿ ಪ್ರಾರಂಭಿಸಿ — ಅವಧಿ ಮತ್ತು ಗಡಿಯಾರ ಸಂಬಂಧ)"
        ),
        "target_parameters": ["length", "initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": "==", "value": "200"},
                {"parameter": "initialState", "operator": "==", "value": "swinging"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'length' to 200 and 'initialState' to 'swinging'. "
                "Watch the slow swing — period > 2.8 seconds at 200 cm."
            ),
            "attempt_2": (
                "length = 200, initialState = swinging: T = 2π√(2/9.8) ≈ 2.84 s. "
                "Grandfather clocks use ~1 m pendulum for ~2 s period (1 tick = 1 s)."
            ),
            "attempt_3": (
                "Long pendulum → long period → slow clock. "
                "To speed a clock up: shorten the pendulum. To slow it down: lengthen it."
            )
        },
        "concept_reminder": (
            "T = 2π√(L/g). At L = 200 cm = 2 m: T = 2π√(2/9.8) ≈ 2.84 s. "
            "Longer pendulum → longer period → clock ticks SLOWER. "
            "1 m pendulum → T ≈ 2 s → 1 tick per second (grandfather clock standard). "
            "Clock adjustment: lengthen pendulum → slower ticks → clock runs slow. "
            "Shorten pendulum → faster ticks → clock speeds up. "
            "(ಉದ್ದ ಊಸರವಳಿ = ನಿಧಾನ ಊಘಾಟ = ನಿಧಾನ ಗಡಿಯಾರ!)"
        )
    },
    {
        "id": "pendulum_kn_q2",
        "challenge": (
            "Set length to 100 cm and change the MASS from minimum (50 g) to maximum "
            "(200 g) without starting the swing. Predict: will the period change?\n\n"
            "(ಉದ್ದ 100 ಸೆಂ ಇಟ್ಟು ದ್ರವ್ಯರಾಶಿ 50 ರಿಂದ 200 ಗ್ರಾಂ ಬದಲಾಯಿಸಿ — ಅವಧಿ ಬದಲಾಗುತ್ತದೆಯೇ?)"
        ),
        "target_parameters": ["mass"],
        "success_rule": {
            "conditions": [
                {"parameter": "mass", "operator": "==", "value": "200"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'mass' to 200. Notice the bob becomes larger and darker (Heavy). "
                "But check the calculated period display — it stays the same as mass 50!"
            ),
            "attempt_2": (
                "mass = 200: formula T = 2π√(L/g) — no 'm' in the formula. "
                "Mass cancels out because gravitational force and inertia both scale with mass."
            ),
            "attempt_3": (
                "Choose mass = 200: the displayed period at 100 cm is 2.01 s regardless "
                "of whether mass=50 or mass=200. Mass independence confirmed."
            )
        },
        "concept_reminder": (
            "Mass independence of pendulum: T = 2π√(L/g) contains NO mass term. "
            "Reason: gravitational pull ∝ mass (more pull) AND inertia ∝ mass (harder to accelerate). "
            "These two effects CANCEL → mass disappears from the formula. "
            "Same principle as Galileo's falling bodies: heavy and light objects fall at same rate. "
            "Proves: period is determined by LENGTH only, not by what the bob is made of. "
            "(ದ್ರವ್ಯರಾಶಿ ಅವಧಿ ಮೇಲೆ ಪರಿಣಾಮ ಬೀರುವುದಿಲ್ಲ — ಕೇವಲ ಉದ್ದ ಮಾತ್ರ!)"
        )
    },
    {
        "id": "pendulum_kn_q3",
        "challenge": (
            "Set length to 50 cm (shortest) and start SWINGING. Compare the fast "
            "oscillations to what you see at length 200 cm — what is the connection "
            "to the T = 2π√(L/g) formula?\n\n"
            "(ಅತ್ಯಲ್ಪ ಉದ್ದ 50 ಸೆಂ + ಊಘಾಟ ಪ್ರಾರಂಭ — T = 2π√(L/g) ಸೂತ್ರ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["length", "initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "length", "operator": "==", "value": "50"},
                {"parameter": "initialState", "operator": "==", "value": "swinging"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'length' to 50 and 'initialState' to 'swinging'. "
                "Short 50 cm string → fast swings; period ≈ 1.42 s."
            ),
            "attempt_2": (
                "length = 50, swinging: T = 2π√(0.5/9.8) ≈ 1.42 s vs 200 cm → 2.84 s. "
                "Ratio: 1.42 : 2.84 ≈ 1 : 2 = √(50:200) = √4 = 2. Formula verified!"
            ),
            "attempt_3": (
                "Short pendulum → high frequency (fast counting). "
                "Long pendulum → low frequency. Clock-makers choose length to match desired tick rate."
            )
        },
        "concept_reminder": (
            "Short pendulum test: L = 50 cm → T = 2π√(0.5/9.8) ≈ 1.42 s. "
            "Long pendulum test: L = 200 cm → T = 2π√(2.0/9.8) ≈ 2.84 s. "
            "Ratio of periods: 2.84/1.42 ≈ 2.0. Ratio of lengths: 200/50 = 4. √4 = 2. ✓ "
            "T ∝ √L: doubling length → period × √2 (not × 2). "
            "Verifying formulas by experiment = the spirit of science. "
            "(T ∝ √L: ಉದ್ದ 4 ಪಟ್ಟು → ಅವಧಿ 2 ಪಟ್ಟು. ಸೂತ್ರ ದೃಢೀಕರಿಸಿ!)"
        )
    }
]


# =============================================================================
# PENDULUM TIMING EXPERIMENT (Chapter 8, sim4)
# ಲೋಲಕ ಕಾಲಾವಧಿ ಪ್ರಯೋಗ – ಮೂರು ಉದ್ದಗಳ ಹೋಲಿಕೆ
# =============================================================================
SIMULATIONS_KN["pendulum_timing_kn"] = {
    "title": "ಲೋಲಕ ಕಾಲಾವಧಿ ಪ್ರಯೋಗ (Pendulum Timing Experiment — Three Lengths)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation4_pendulum_timing_kn.html",

    "description": (
        "Kannada experiment simulation that times three pendulums of lengths 50 cm "
        "(short / red), 100 cm (medium / green), and 150 cm (long / blue) through "
        "10 complete oscillations. Students select a pendulum, start the stopwatch, "
        "and the simulation auto-completes after the calculated time. Results are "
        "shown in a comparison table displaying time-for-10 oscillations and the "
        "individual period (T). Once all three are done, a conclusion panel "
        "confirms: longer pendulum = longer period."
    ),

    "cannot_demonstrate": [
        "Effect of bob mass on timing (fixed equal masses used)",
        "Timing by hand with a real stopwatch",
        "Effect of amplitude on period",
    ],

    "initial_params": {"initialState": "short", "showHints": True},

    "parameter_info": {
        "initialState": {
            "label": "Pendulum to Select",
            "range": "short, medium, long",
            "url_key": "initialState",
            "effect": (
                "Pre-selects which pendulum length is highlighted for the experiment.\n"
                "  'short'  → 50 cm / red bob selected (default, T ≈ 1.42 s)\n"
                "  'medium' → 100 cm / green bob selected (T ≈ 2.01 s)\n"
                "  'long'   → 150 cm / blue bob selected (T ≈ 2.46 s)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the concept card and the takeaway observation box."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "Experimental Method: Measuring Period by Timing 10 Oscillations",
            "description": (
                "One oscillation is very short to time accurately. Scientists measure "
                "10 (or 20) oscillations and divide — this reduces the percentage error "
                "in timing. The table shows 'Time for 10' and T = (time for 10) / 10."
            ),
            "key_insight": (
                "Timing error stays roughly constant regardless of how many oscillations. "
                "Timing 10 oscillations and dividing by 10 gives period 10× more accurately "
                "than timing a single oscillation. This is standard experimental practice."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Longer Pendulum = Longer Period — Experimental Confirmation",
            "description": (
                "The experiment data confirms: short (50 cm) ≈ 1.42 s, medium (100 cm) "
                "≈ 2.01 s, long (150 cm) ≈ 2.46 s. Increasing length by 3× (50→150 cm) "
                "increases period by √3 ≈ 1.73× (not 3×)."
            ),
            "key_insight": (
                "T ∝ √L. If L → 4L, then T → 2T. "
                "Experimentally: T₁₅₀/T₅₀ = 2.46/1.42 ≈ 1.73 = √3. ✓ "
                "Data matches the formula. Experiment confirms theory."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Why Grandfather Clocks Have Long Pendulums",
            "description": (
                "The results table shows that longer pendulums swing slower. "
                "A 1-metre pendulum ticks every 2 seconds (half-swing = 1 second). "
                "Clock designers choose pendulum length to achieve a specific tick rate. "
                "Short pendulums tick too fast; long ones are more visible and adjustable."
            ),
            "key_insight": (
                "Long pendulum → slow tick → easier to count mechanically. "
                "Grandfather clock pendulum ≈ 1 m → T ≈ 2 s → 1 tick per second. "
                "To speed clock: adjust (lower) the bob to effectively shorten pendulum. "
                "To slow clock: raise the bob to lengthen pendulum."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["pendulum_timing_kn"] = [
    {
        "id": "pend_timing_kn_q1",
        "challenge": (
            "Select the LONG pendulum (150 cm / blue) for the experiment. "
            "Before running it, predict its period using T = 2π√(L/g) and "
            "explain how you would verify the formula.\n\n"
            "(ಉದ್ದ ಲೋಲಕ (150 ಸೆಂ) ಆಯ್ಕೆ ಮಾಡಿ — ಪ್ರಾಯೋಗಿಕ ಮೌಲ್ಯ ಊಹಿಸಿ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "long"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'long' → blue bob is highlighted. "
                "Predicted T = 2π√(1.5/9.8) = 2π × 0.391 ≈ 2.46 s."
            ),
            "attempt_2": (
                "Set 'initialState' to 'long'. Then run the experiment — "
                "the result should be very close to 2.46 s ± small variation."
            ),
            "attempt_3": (
                "Choose 'long': 10 oscillations take about 24.6 s → T = 24.6/10 = 2.46 s. "
                "Compare this result from the formula. Do they match?"
            )
        },
        "concept_reminder": (
            "Prediction for long pendulum (L = 150 cm = 1.5 m): "
            "T = 2π√(L/g) = 2π√(1.5/9.8) = 2π × 0.391 = 2.46 s. "
            "Experiment verification: time 10 oscillations → divide by 10. "
            "If result ≈ 2.46 s, the formula is confirmed! "
            "Scientific method: PREDICT → EXPERIMENT → COMPARE → CONCLUDE. "
            "(ಸೂತ್ರ ಭವಿಷ್ಯ + ಪ್ರಯೋಗ ಫಲಿತ = ವಿಜ್ಞಾನ ವಿಧಾನ!)"
        )
    },
    {
        "id": "pend_timing_kn_q2",
        "challenge": (
            "Select the SHORT pendulum (50 cm / red). Run it and record the period. "
            "How does it compare to the long pendulum? Express the ratio.\n\n"
            "(ಚಿಕ್ಕ ಲೋಲಕ (50 ಸೆಂ) ಆಯ್ಕೆ ಮಾಡಿ — ಉದ್ದ ಮತ್ತು ಚಿಕ್ಕ ಲೋಲಕ ಅವಧಿ ಹೋಲಿಕೆ)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "short"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'short' → red bob is highlighted. Period ≈ 1.42 s. "
                "Long pendulum period ≈ 2.46 s. Ratio ≈ 2.46/1.42 ≈ 1.73 ≈ √3."
            ),
            "attempt_2": (
                "Set 'initialState' to 'short'. L ratio = 150/50 = 3. "
                "T ratio = √3 ≈ 1.73. Confirms T ∝ √L."
            ),
            "attempt_3": (
                "Choose 'short': short red pendulum completes 10 oscillations fastest "
                "(≈ 14.2 s). Long blue takes ≈ 24.6 s for 10. Both confirm T ∝ √L."
            )
        },
        "concept_reminder": (
            "Short (50 cm) vs Long (150 cm) comparison: "
            "T_short = 2π√(0.5/9.8) ≈ 1.42 s. T_long = 2π√(1.5/9.8) ≈ 2.46 s. "
            "Ratio T_long/T_short = 2.46/1.42 ≈ 1.73. "
            "√(L_long/L_short) = √(150/50) = √3 ≈ 1.73. MATCH! ✓ "
            "T ∝ √L confirmed experimentally. Triple the length → period × √3, not × 3. "
            "(ಉದ್ದ 3 ಪಟ್ಟು → ಅವಧಿ √3 ≈ 1.73 ಪಟ್ಟು ‑ ಸೂತ್ರ ದೃಢ!)"
        )
    },
    {
        "id": "pend_timing_kn_q3",
        "challenge": (
            "Select the MEDIUM pendulum (100 cm). Why do scientists time 10 oscillations "
            "instead of just 1? How does this reduce measurement error?\n\n"
            "(ಮಧ್ಯಮ ಲೋಲಕ (100 ಸೆಂ) ಆಯ್ಕೆ ಮಾಡಿ — 10 ಆಂದೋಲನ ಏಕೆ ಅಳೆಯುತ್ತಾರೆ?)"
        ),
        "target_parameters": ["initialState"],
        "success_rule": {
            "conditions": [
                {"parameter": "initialState", "operator": "==", "value": "medium"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Select 'medium'. The experiment times 10 oscillations (≈ 20 s). "
                "If you timed just 1 swing (≈ 2 s), a 0.2 s error = 10% error."
            ),
            "attempt_2": (
                "Set 'initialState' to 'medium'. Timing 10 oscillations: "
                "a 0.2 s error on 20 s = only 1% error. Divide by 10 → T accurate to 0.1%."
            ),
            "attempt_3": (
                "Choose 'medium': timing error is roughly constant regardless of count. "
                "More oscillations timed → smaller % error in each period."
            )
        },
        "concept_reminder": (
            "Why time 10 oscillations? Reducing percentage error in timing. "
            "Timing 1 oscillation (≈ 2 s): human reaction time error ≈ ±0.2 s = 10% error. "
            "Timing 10 oscillations (≈ 20 s): same ±0.2 s error = only 1% error. "
            "Dividing by 10: period error = 0.02 s = much more accurate. "
            "General rule: more repetitions timed → better accuracy in each measurement. "
            "(10 ಆಂದೋಲನ ಅಳತೆ → ± ದೋಷ 10 ಪಟ್ಟು ಕಡಿಮೆ!)"
        )
    }
]


# =============================================================================
# TIME UNITS SIMULATION (Chapter 8, sim5)
# ಸಮಯ ಘಟಕ ಪರಿವರ್ತಕ – ಸೆಕೆಂಡ್ SI ಘಟಕ
# =============================================================================
SIMULATIONS_KN["time_units_kn"] = {
    "title": "ಸಮಯ ಘಟಕ ಪರಿವರ್ತಕ (Time Unit Converter — Second as SI Unit)",

    "language": "kannada",

    "file": "simulations_kannada/science_chapter8_simulation5_time_units_kn.html",

    "description": (
        "Kannada interactive time-unit converter. Students type any number and select "
        "a unit (hours, minutes, seconds, milliseconds). The tool instantly shows the "
        "equivalent values in all four units, with the selected unit highlighted. "
        "A reference table shows key conversion factors. Additional panels explain "
        "why milliseconds matter (sports, medicine, computers) and display the correct "
        "SI notation (s, min, h, ms) vs common wrong forms (sec, hr, msec)."
    ),

    "cannot_demonstrate": [
        "Microseconds, nanoseconds, or sub-millisecond units",
        "Time calculations with start/end timestamps",
        "Calendar time (days, weeks, months, years)",
    ],

    "initial_params": {"value": 1, "unit": "s", "showHints": True},

    "parameter_info": {
        "value": {
            "label": "Time Value",
            "range": "any positive number",
            "url_key": "value",
            "effect": (
                "Sets the numeric input field. Combined with 'unit' to compute equivalents.\n"
                "  Examples: value=1&unit=h → 1 hour\n"
                "            value=90&unit=min → 90 minutes\n"
                "            value=3600&unit=s → 3600 seconds (= 1 hour)"
            )
        },
        "unit": {
            "label": "Input Unit",
            "range": "h, min, s, ms",
            "url_key": "unit",
            "effect": (
                "Sets the unit dropdown on load, then triggers conversion.\n"
                "  'h'   → hours\n"
                "  'min' → minutes\n"
                "  's'   → seconds (default, SI base unit)\n"
                "  'ms'  → milliseconds"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides concept card, conversion factors, small-units, and notation panels."
        }
    },

    "concepts": [
        {
            "id": 1,
            "title": "The Second (s) is the SI Base Unit of Time",
            "description": (
                "The International System of Units (SI) defines the second as the base "
                "unit of time. All other time units are defined relative to it: "
                "1 minute = 60 s; 1 hour = 3600 s; 1 ms = 0.001 s. "
                "In scientific writing, the symbol 's' must be used (not 'sec')."
            ),
            "key_insight": (
                "SI base unit for time = SECOND (symbol: s, not sec). "
                "Why 60 seconds in a minute? Ancient Babylonian base-60 (sexagesimal) counting. "
                "Why 24 hours per day? Ancient Egyptians divided night/day into 12 hours each."
            ),
            "related_params": ["unit", "value"]
        },
        {
            "id": 2,
            "title": "Key Conversion Factors: 60 and 3600",
            "description": (
                "1 h = 60 min = 3600 s. 1 min = 60 s = 60,000 ms. "
                "1 s = 1000 ms = 1,000,000 μs. "
                "Students often confuse hours with minutes in calculations. "
                "Converting to seconds first always prevents errors."
            ),
            "key_insight": (
                "Memory trick: 1 hour = 60 min = 3600 s. "
                "Converting to seconds first → then do arithmetic → convert back. "
                "Example: 1.5 hours = 1.5 × 3600 = 5400 seconds."
            ),
            "related_params": ["value", "unit"]
        },
        {
            "id": 3,
            "title": "Correct SI Notation: s, min, h, ms (Not sec, secs, hr, hrs)",
            "description": (
                "SI notation for time uses: s (second), min (minute), h (hour), "
                "ms (millisecond). Common incorrect forms — sec, secs, hr, hrs, msec — "
                "should not be used in scientific work. SI symbols are always singular "
                "and never have a period except at the end of a sentence."
            ),
            "key_insight": (
                "Correct: '5 s', '2 min', '1 h', '500 ms'. "
                "Incorrect: '5 sec', '2 mins', '1 hr', '500 msec'. "
                "SI symbols are case-sensitive: 'ms' = millisecond; 'MS' means something else. "
                "This matters in competitive exams and professional communication."
            ),
            "related_params": ["unit", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["time_units_kn"] = [
    {
        "id": "time_units_kn_q1",
        "challenge": (
            "Set the unit to HOURS (h). Enter value = 1 (1 hour). "
            "What is 1 hour in seconds? Show the conversion step-by-step.\n\n"
            "(ಘಟಕ = ಗಂಟೆ (h), ಮೌಲ್ಯ = 1 ಹೊಂದಿಸಿ — 1 ಗಂಟೆ = ಎಷ್ಟು ಸೆಕೆಂಡ್?)"
        ),
        "target_parameters": ["unit"],
        "success_rule": {
            "conditions": [
                {"parameter": "unit", "operator": "==", "value": "h"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'unit' to 'h' and value = 1. The results show: "
                "1 h = 60 min = 3600 s = 3,600,000 ms."
            ),
            "attempt_2": (
                "unit = h: 1 hour → 60 minutes → 60 × 60 = 3600 seconds. "
                "Multiply by 1000 → 3,600,000 milliseconds."
            ),
            "attempt_3": (
                "Choose unit = 'h': the key conversion is 1 h = 3600 s. "
                "Memorise: 60 sec/min × 60 min/h = 3600 s/h."
            )
        },
        "concept_reminder": (
            "Time unit conversions starting from 1 HOUR: "
            "1 h = 60 min (because 60 minutes in 1 hour). "
            "1 h = 60 × 60 = 3,600 s (because 60 seconds in 1 minute). "
            "1 h = 3,600 × 1,000 = 3,600,000 ms (because 1000 ms in 1 second). "
            "Memory: h × 60 = min; min × 60 = s; s × 1000 = ms. "
            "Going backward: ÷60 ÷60 ÷1000. "
            "(1 ಗಂಟೆ = 60 ನಿಮಿ = 3600 ಸೆ = 36,00,000 ms!)"
        )
    },
    {
        "id": "time_units_kn_q2",
        "challenge": (
            "Set the unit to MILLISECONDS (ms) and value = 1000. "
            "What is 1000 ms? Why are milliseconds important in sports and medicine?\n\n"
            "(ಘಟಕ = ಮಿಲಿಸೆಕೆಂಡ್ (ms), ಮೌಲ್ಯ = 1000 — ms ಮಹತ್ವ ವಿವರಿಸಿ)"
        ),
        "target_parameters": ["unit"],
        "success_rule": {
            "conditions": [
                {"parameter": "unit", "operator": "==", "value": "ms"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'unit' to 'ms' and value = 1000. Result: 1000 ms = 1 s exactly. "
                "1 ms = 0.001 s → small but significant in speed events."
            ),
            "attempt_2": (
                "unit = ms, value = 1000: 1000 ms = 1 s. "
                "Olympic 100 m sprints are won/lost by 10–100 ms = hundredths of seconds."
            ),
            "attempt_3": (
                "Choose unit = 'ms': 1 ms = 0.001 s. "
                "ECG measures heartbeat timing to 1 ms accuracy; laptops process in nanoseconds."
            )
        },
        "concept_reminder": (
            "Milliseconds importance: 1 ms = 0.001 s = 1/1000 of a second. "
            "SPORTS: Olympic results decided by 10–100 ms (photo-finish cameras). "
            "MEDICINE: ECG/EEG tracks heart/brain signals to ±1 ms precision. "
            "COMPUTERS: processors work in nanoseconds (1 ns = 0.000001 ms). "
            "1000 ms = 1 s exactly. SI symbol: ms (NOT msec). "
            "(1000 ms = 1 ಸೆ | ಕ್ರೀಡೆ, ಔಷಧ, ಕಂಪ್ಯೂಟರ್‌ನಲ್ಲಿ ms ಮುಖ್ಯ!)"
        )
    },
    {
        "id": "time_units_kn_q3",
        "challenge": (
            "Set the unit to MINUTES (min) and value = 90. What is 90 minutes "
            "expressed in hours AND in seconds? Show both conversions.\n\n"
            "(ಘಟಕ = ನಿಮಿಷ (min), ಮೌಲ್ಯ = 90 — 90 ನಿಮಿ ಗಂಟೆ ಮತ್ತು ಸೆಕೆಂಡ್‌ನಲ್ಲಿ?)"
        ),
        "target_parameters": ["unit"],
        "success_rule": {
            "conditions": [
                {"parameter": "unit", "operator": "==", "value": "min"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set 'unit' to 'min' and value = 90. Results: "
                "90 min = 1.5 h AND 90 × 60 = 5400 s."
            ),
            "attempt_2": (
                "unit = min, value = 90: "
                "90 min ÷ 60 = 1.5 h (one and a half hours). "
                "90 min × 60 = 5400 s."
            ),
            "attempt_3": (
                "Choose unit = 'min': the converter shows all equivalents simultaneously. "
                "A school exam is often 90 min = 1 h 30 min = 5400 s."
            )
        },
        "concept_reminder": (
            "90 minutes in all units: "
            "90 min ÷ 60 = 1.5 hours. "
            "90 min × 60 = 5,400 seconds. "
            "5,400 × 1000 = 5,400,000 milliseconds. "
            "Common applications: 90-minute football match = 1.5 h = 5400 s. "
            "SI notation reminder: min (NOT mins), h (NOT hr/hrs), s (NOT sec). "
            "(90 ನಿಮಿ = 1.5 ಗಂ = 5400 ಸೆ — ಸರಿಯಾದ SI ಸಂಕೇತ ಬಳಸಿ!)"
        )
    }
]



# =============================================================================
# SPEED CALCULATOR SIMULATION (Kannada)
# ವೇಗ ಕ್ಯಾಲ್ಕುಲೇಟರ್ – ವೇಗ, ದೂರ ಮತ್ತು ಸಮಯ ಲೆಕ್ಕ ಹಾಕಿ
# Science Chapter 8 – Motion and Time
# =============================================================================
SIMULATIONS_KN["speed_calculator_kn"] = {
    "title": "ವೇಗ ಕ್ಯಾಲ್ಕುಲೇಟರ್ (Speed Calculator)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter8_simulation6_speed_calculator_kn.html",
    "description": (
        "An interactive Kannada-language calculator that teaches the three forms of the "
        "speed–distance–time triangle. Students switch between three modes: finding speed "
        "(ವೇಗ = ದೂರ ÷ ಸಮಯ), finding distance (ದೂರ = ವೇಗ × ಸಮಯ), and finding time "
        "(ಸಮಯ = ದೂರ ÷ ವೇಗ). Real-world speed examples (walker, cyclist, car, train, "
        "aeroplane) anchor the formula to daily experience. Unit conversion between "
        "km/h and m/s is also demonstrated."
    ),
    "cannot_demonstrate": [
        "Relative speed or motion of two objects simultaneously",
        "Average speed over a journey with different speeds",
        "Acceleration or change in speed over time",
        "Graphical representation of distance-time relationship",
        "Velocity (direction of motion)"
    ],
    "initial_params": {
        "initialState": "speed",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Calculator Mode",
            "range": "speed, distance, time",
            "url_key": "initialState",
            "effect": (
                "'speed'    → Find Speed mode (ವೇಗ = ದೂರ ÷ ಸಮಯ) — default\n"
                "'distance' → Find Distance mode (ದೂರ = ವೇಗ × ಸಮಯ)\n"
                "'time'     → Find Time mode (ಸಮಯ = ದೂರ ÷ ವೇಗ)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight explanation box (if present)."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Speed Formula: Speed = Distance ÷ Time",
            "description": (
                "Speed measures how fast an object moves — the distance covered per unit time. "
                "When distance and time are known, speed is calculated as ವೇಗ = ದೂರ ÷ ಸಮಯ."
            ),
            "key_insight": (
                "A car travelling 100 km in 2 hours has speed = 100 ÷ 2 = 50 km/h. "
                "Doubling the distance at the same speed doubles the travel time. "
                "Speed unit km/h means 'kilometres per hour'."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Distance Formula: Distance = Speed × Time",
            "description": (
                "When speed and time are known, the distance covered can be calculated as "
                "ದೂರ = ವೇಗ × ಸಮಯ. This rearranges the speed triangle."
            ),
            "key_insight": (
                "A train moving at 100 km/h for 3 hours covers 100 × 3 = 300 km. "
                "Higher speed means greater distance in the same time."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Time Formula and Unit Conversion (km/h ↔ m/s)",
            "description": (
                "Time = Distance ÷ Speed completes the triangle. Additionally, speed in "
                "km/h converts to m/s by dividing by 3.6, and m/s converts to km/h by "
                "multiplying by 3.6."
            ),
            "key_insight": (
                "36 km/h = 36 ÷ 3.6 = 10 m/s. The SI unit of speed is m/s. "
                "km/h is used for road vehicles; m/s in scientific contexts."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["speed_calculator_kn"] = [

    # Q1: Use the speed-finding mode (core formula)
    {
        "id": "speed_calc_kn_q1",
        "question": (
            "A train travels 200 km in 4 hours. Set the calculator to FIND SPEED mode "
            "and calculate its speed. (ರೈಲು 4 ಗಂಟೆಯಲ್ಲಿ 200 km ಓಡಿದೆ — ವೇಗ ಕಂಡুಹಿಡಿ)"
        ),
        "action_required": "Set 'initialState' to 'speed' to activate Find Speed mode.",
        "hint": "Select 'speed' mode — the calculator shows ವೇಗ = ದೂರ ÷ ಸಮಯ. Enter 200 km and 4 h.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "speed"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! Speed = 200 ÷ 4 = 50 km/h. "
            "The speed mode directly applies ವೇಗ = ದೂರ ÷ ಸಮಯ."
        ),
        "failure_message": (
            "Select 'speed' from the Calculator Mode dropdown to activate the "
            "Find Speed mode (ವೇಗ ಕಂಡುಹಿಡಿ)."
        )
    },

    # Q2: Use the distance-finding mode
    {
        "id": "speed_calc_kn_q2",
        "question": (
            "A cyclist rides at 20 km/h for 3 hours. Set the calculator to FIND DISTANCE "
            "mode. (ಸೈಕ್ಲಿಸ್ಟ್ 20 km/h ವೇಗದಲ್ಲಿ 3 ಗಂಟೆ ಸವಾರಿ ಮಾಡಿದ — ದೂರ ಕಂಡухиди)"
        ),
        "action_required": "Set 'initialState' to 'distance' to activate Find Distance mode.",
        "hint": "Select 'distance' mode — the calculator shows ದೂರ = ವೇಗ × ಸಮಯ. Enter 20 km/h and 3 h.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "distance"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! Distance = 20 × 3 = 60 km. "
            "ದೂರ = ವೇಗ × ಸಮಯ — the distance formula is the reverse of the speed formula."
        ),
        "failure_message": (
            "Select 'distance' from the Calculator Mode dropdown to activate Find Distance mode."
        )
    },

    # Q3: Use the time-finding mode
    {
        "id": "speed_calc_kn_q3",
        "question": (
            "A car needs to travel 150 km at 50 km/h. Set the calculator to FIND TIME "
            "mode to calculate how long the journey takes. "
            "(ಕಾರು 150 km, 50 km/h ವೇಗ — ಸಮಯ ಎಷ್ಟಾಗುತ್ತದೆ?)"
        ),
        "action_required": "Set 'initialState' to 'time' to activate Find Time mode.",
        "hint": "Select 'time' mode — the calculator shows ಸಮಯ = ದೂರ ÷ ವೇಗ. Enter 150 km and 50 km/h.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "time"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! Time = 150 ÷ 50 = 3 hours. "
            "ಸಮಯ = ದೂರ ÷ ವೇಗ — completing the speed-distance-time triangle."
        ),
        "failure_message": (
            "Select 'time' from the Calculator Mode dropdown to activate Find Time mode."
        )
    }
]


# =============================================================================
# SPEED RACE SIMULATION (Kannada)
# ವೇಗ ಓಟ – 1 ಕಿಮೀ ಸ್ಪರ್ಧೆ
# Science Chapter 8 – Motion and Time
# =============================================================================
SIMULATIONS_KN["speed_race_kn"] = {
    "title": "ವೇಗ ಓಟ (Speed Race)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter8_simulation7_speed_race_kn.html",
    "description": (
        "An animated 1-km race in Kannada that pits a walker (5 km/h), cyclist (20 km/h), "
        "car (60 km/h), and train (100 km/h) against each other on the same track. "
        "Students observe that higher speed means shorter time to cover the same distance. "
        "After the race, the simulation shows the calculated finish times using "
        "Time = Distance ÷ Speed, reinforcing the inverse relationship between speed and time."
    ),
    "cannot_demonstrate": [
        "Different distances for each racer",
        "Acceleration or deceleration during the race",
        "Average speed across multiple segments",
        "Relative speed between two moving objects",
        "Direction of motion or vector quantities"
    ],
    "initial_params": {
        "initialState": "setup",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Race State",
            "range": "setup, racing",
            "url_key": "initialState",
            "effect": (
                "'setup'  → show the race setup screen before starting — default\n"
                "'racing' → auto-click 'Start Race' button (800 ms delay), animation begins"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight explanation box (if present)."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Higher Speed → Less Time for Same Distance",
            "description": (
                "When multiple objects travel the same distance, the faster object finishes first. "
                "Time = Distance ÷ Speed, so doubling speed halves travel time."
            ),
            "key_insight": (
                "Walker at 5 km/h takes 720 s for 1 km. Train at 100 km/h takes only 36 s. "
                "The train is 20× faster and finishes 20× sooner — a direct inverse relationship."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Calculating Finish Time: Time = Distance ÷ Speed",
            "description": (
                "After the race, the simulation shows the finish time for each racer "
                "computed as Time = 1 km ÷ speed. This connects the visual race to "
                "the mathematical formula."
            ),
            "key_insight": (
                "Car at 60 km/h: 1 km ÷ 60 km/h = 1/60 h = 60 s. "
                "Cyclist at 20 km/h: 1 km ÷ 20 km/h = 3 min. "
                "Same distance, different speeds → very different times."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Comparing Real-Life Speeds",
            "description": (
                "The four racers represent real-world modes of transport. Comparing their "
                "speeds builds number sense about how fast different vehicles actually move."
            ),
            "key_insight": (
                "Speeds in daily life: walking ~5 km/h, cycling ~20 km/h, "
                "car in city ~60 km/h, express train ~100–160 km/h. "
                "These benchmarks help estimate travel time for familiar journeys."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["speed_race_kn"] = [

    # Q1: Observe the setup (default state — identify speeds)
    {
        "id": "speed_race_kn_q1",
        "question": (
            "Look at the race setup. Which racer has the LOWEST speed, and which has the "
            "HIGHEST? Set the simulation to its default SETUP state to examine the starting "
            "speeds. (ಯಾರಿಗೆ ಅತಿ ಕಡಿಮೆ ವೇಗ? ಯಾರಿಗೆ ಅತಿ ಹೆಚ್ಚು?)"
        ),
        "action_required": "Set 'initialState' to 'setup' to show the race configuration.",
        "hint": "Select 'setup' state — observe the speed inputs: walker=5 km/h, train=100 km/h.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "setup"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! In setup mode you can see all four speeds. "
            "Walker (5 km/h) is slowest; Train (100 km/h) is fastest. "
            "The train is 20× faster than the walker."
        ),
        "failure_message": (
            "Select 'setup' from the Race State dropdown to display the starting configuration."
        )
    },

    # Q2: Start the race (racing state)
    {
        "id": "speed_race_kn_q2",
        "question": (
            "Now START the race to see who reaches the 1 km finish line first. "
            "Set the simulation to RACING state. "
            "(1 km ಓಟ ಪ್ರಾರಂಭಿಸಿ — ಯಾರು ಮೊದಲು ಗೆಲ್ಲುತ್ತಾರೆ?)"
        ),
        "action_required": "Set 'initialState' to 'racing' to auto-start the race.",
        "hint": "Select 'racing' state — the Start Race button is automatically clicked and the animation begins.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "racing"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Race started! The train wins, followed by the car, cyclist, and walker. "
            "Finish times: Train ~36 s, Car ~60 s, Cyclist ~180 s, Walker ~720 s."
        ),
        "failure_message": (
            "Select 'racing' from the Race State dropdown to auto-start the race animation."
        )
    },

    # Q3: Back to setup to verify calculations
    {
        "id": "speed_race_kn_q3",
        "question": (
            "After watching the race, return to SETUP mode. Using Time = Distance ÷ Speed, "
            "calculate how many SECONDS the walker takes to finish 1 km at 5 km/h. "
            "(ನಡೆದಾಡುವವನು 1 km ಮುಗಿಸಲು ಎಷ್ಟು ಸೆಕೆಂಡ್ ತೆಗೆದುಕೊಳ್ಳುತ್ತಾನೆ?)"
        ),
        "action_required": "Set 'initialState' to 'setup' and verify walker finish time manually.",
        "hint": (
            "Select 'setup' state. Then calculate: Time = 1 km ÷ 5 km/h = 0.2 h = "
            "0.2 × 3600 = 720 seconds."
        ),
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "setup"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! 1 km ÷ 5 km/h = 0.2 h = 720 s (12 minutes). "
            "The race result panel confirms this when you run the simulation."
        ),
        "failure_message": (
            "Return to 'setup' state to review the racer speeds before calculating."
        )
    }
]


# =============================================================================
# UNIFORM LINEAR MOTION SIMULATION (Kannada)
# ಏಕರೂಪ ರೇಖೀಯ ಚಲನೆ – ಸ್ಥಿರ ವೇಗ, ನೇರ ರೇಖೆ
# Science Chapter 8 – Motion and Time
# =============================================================================
SIMULATIONS_KN["uniform_motion_kn"] = {
    "title": "ಏಕರೂಪ ರೇಖೀಯ ಚಲನೆ (Uniform Linear Motion)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter8_simulation8_uniform_motion_kn.html",
    "description": (
        "An animated Kannada simulation of a train moving along a 10 km track at a "
        "student-chosen constant speed (10–100 km/h). The simulation fills a distance–time "
        "data table and draws the distance-time graph in real time, showing that uniform "
        "motion produces a straight-line graph with the slope equal to speed. "
        "Students observe that equal distances are covered in equal time intervals."
    ),
    "cannot_demonstrate": [
        "Non-uniform (accelerating or decelerating) motion",
        "Two-dimensional or curved-path motion",
        "Average speed vs instantaneous speed distinction",
        "Velocity (direction) vs speed",
        "Forces causing the motion"
    ],
    "initial_params": {
        "initialState": "setup",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Motion State",
            "range": "setup, slow_run, fast_run",
            "url_key": "initialState",
            "effect": (
                "'setup'    → slider at 50 km/h, no animation — default view\n"
                "'slow_run' → set slider to 20 km/h, auto-start animation\n"
                "'fast_run' → set slider to 80 km/h, auto-start animation"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight explanation box (if present)."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Uniform Motion: Equal Distance in Equal Time",
            "description": (
                "In uniform linear motion, an object moves in a straight line at constant speed, "
                "covering equal distances in equal time intervals."
            ),
            "key_insight": (
                "At 50 km/h, the train covers exactly 13.9 m every second. "
                "The distance column increases by the same amount each second — "
                "this uniformity is what 'uniform motion' means."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Distance-Time Graph is a Straight Line",
            "description": (
                "The distance-time graph for uniform motion is a straight line (not a curve). "
                "The steeper the line, the higher the speed."
            ),
            "key_insight": (
                "At 80 km/h the graph line is steeper than at 20 km/h. "
                "Slope = rise/run = distance/time = speed. "
                "A straight line confirms constant (uniform) speed."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "Faster Speed → Steeper Graph Slope",
            "description": (
                "Comparing slow (20 km/h) and fast (80 km/h) runs on the same graph "
                "shows that speed equals the slope of the distance-time graph."
            ),
            "key_insight": (
                "Slow run (20 km/h): low slope. Fast run (80 km/h): steep slope. "
                "Double the speed → doubled slope → doubled distance per second. "
                "This visual comparison makes the speed-slope relationship concrete."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["uniform_motion_kn"] = [

    # Q1: Observe the setup (default state)
    {
        "id": "uniform_motion_kn_q1",
        "question": (
            "Open the simulation in SETUP state. Observe the slider and the empty graph. "
            "What type of graph line do you predict for uniform motion? "
            "(ಏಕರೂಪ ಚಲನೆಗೆ ದೂರ-ಸಮಯ ಗ್ರಾಫ್ ಹೇಗಿರುತ್ತದೆ?)"
        ),
        "action_required": "Set 'initialState' to 'setup' to view the initial configuration.",
        "hint": "Select 'setup' — the graph axes are visible. Recall that uniform motion = constant speed = straight line graph.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "setup"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! In setup mode the empty graph shows the axes. "
            "Uniform motion produces a STRAIGHT LINE because speed (slope) is constant."
        ),
        "failure_message": (
            "Select 'setup' from the Motion State dropdown to open the default configuration view."
        )
    },

    # Q2: Slow run to observe equal-distance intervals
    {
        "id": "uniform_motion_kn_q2",
        "question": (
            "Set the simulation to SLOW RUN (20 km/h) and observe the distance-time table. "
            "Are the distances in each second interval equal? "
            "(ಮಂದ ಓಟ 20 km/h — ಪ್ರತಿ ಸೆಕೆಂಡ್ ದೂರ ಸಮಾನವಾಗಿದೆಯೇ?)"
        ),
        "action_required": "Set 'initialState' to 'slow_run' to start a 20 km/h animation.",
        "hint": "Select 'slow_run' — the slider moves to 20 km/h and animation starts. Watch the data table fill with equal values.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "slow_run"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! At 20 km/h = 5.6 m/s, each second shows ~5.6 m added. "
            "Equal distance per second confirms this is uniform motion."
        ),
        "failure_message": (
            "Select 'slow_run' from the Motion State dropdown to run the animation at 20 km/h."
        )
    },

    # Q3: Fast run to compare slope
    {
        "id": "uniform_motion_kn_q3",
        "question": (
            "Now set the simulation to FAST RUN (80 km/h). Compare the graph slope with "
            "the slow run. What does a steeper slope indicate? "
            "(ತ್ವರಿತ ಓಟ 80 km/h — ಗ್ರಾಫ್ ಇಳಿಜಾರು ಹೆಚ್ಚಾಗಿದೆ ಎಂದರೇನು?)"
        ),
        "action_required": "Set 'initialState' to 'fast_run' to start an 80 km/h animation.",
        "hint": "Select 'fast_run' — slider moves to 80 km/h. The graph line is steeper because slope = speed.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "fast_run"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! At 80 km/h the slope is 4× steeper than at 20 km/h. "
            "Steeper slope = higher speed. Slope of distance-time graph = speed."
        ),
        "failure_message": (
            "Select 'fast_run' from the Motion State dropdown to run the animation at 80 km/h."
        )
    }
]


# =============================================================================
# NON-UNIFORM MOTION SIMULATION (Kannada)
# ಅಸಮ ಚಲನೆ – ವೇಗ ಬದಲಾಗುತ್ತಿದೆ
# Science Chapter 8 – Motion and Time
# =============================================================================
SIMULATIONS_KN["nonuniform_motion_kn"] = {
    "title": "ಅಸಮ ಚಲನೆ (Non-Uniform Motion)",
    "language": "kannada",
    "file": "simulations_kannada/science_chapter8_simulation9_nonuniform_motion_kn.html",
    "description": (
        "A Kannada simulation of a car undergoing non-uniform motion in three scenarios: "
        "accelerating (speed increases linearly), decelerating/braking (speed decreases), "
        "and city traffic (stop-go pattern with acceleration and cruising phases). "
        "An onscreen speedometer shows the changing speed; a distance–time graph is drawn "
        "in real time as a CURVED line — contrasted with a dashed straight-line reference "
        "for uniform motion. A data table shows unequal distances in successive seconds, "
        "defining non-uniform motion."
    ),
    "cannot_demonstrate": [
        "Uniform motion (shown only as a reference dashed line)",
        "Two-dimensional or projectile motion",
        "Forces causing acceleration (Newton's laws)",
        "Quantitative calculation of acceleration",
        "Motion with friction effects modelled explicitly"
    ],
    "initial_params": {
        "initialState": "accelerate",
        "showHints": True
    },
    "parameter_info": {
        "initialState": {
            "label": "Motion Mode",
            "range": "accelerate, decelerate, traffic",
            "url_key": "initialState",
            "effect": (
                "'accelerate' → car speeds up (0 → 100 km/h) — default, auto-starts\n"
                "'decelerate' → car slows down (100 → 0 km/h / braking) — auto-starts\n"
                "'traffic'    → city stop-go pattern — auto-starts"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true/false",
            "url_key": "showHints",
            "effect": "Shows or hides the insight explanation box (if present)."
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Non-Uniform Motion: Unequal Distances in Equal Time",
            "description": (
                "In non-uniform motion, the speed changes over time, so unequal distances "
                "are covered in equal successive time intervals."
            ),
            "key_insight": (
                "An accelerating car covers 0 m in the first second and many more metres "
                "in the fifth second. The unequal distances in the data table are the "
                "defining signature of non-uniform motion."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 2,
            "title": "Curved Distance-Time Graph vs Straight-Line (Uniform)",
            "description": (
                "Non-uniform motion produces a CURVED distance-time graph. "
                "A dashed straight line shows what uniform motion would look like for comparison."
            ),
            "key_insight": (
                "Acceleration → graph curves upward (increasing slope = increasing speed). "
                "Deceleration → graph curves and flattens (decreasing slope = decreasing speed). "
                "The curve shape reveals whether the object is speeding up or slowing down."
            ),
            "related_params": ["initialState"]
        },
        {
            "id": 3,
            "title": "City Traffic: The Most Common Non-Uniform Pattern",
            "description": (
                "Real-world city driving is a classic example of non-uniform motion — "
                "the car repeatedly stops, accelerates, cruises, and brakes."
            ),
            "key_insight": (
                "In the traffic mode, the speed cycles: 0 (stopped at signal) → "
                "accelerating → 60 km/h (cruising) → decelerating → 0 again. "
                "This irregular pattern means the distance-time graph is neither straight "
                "nor smoothly curved."
            ),
            "related_params": ["initialState", "showHints"]
        }
    ]
}

QUIZ_QUESTIONS_KN["nonuniform_motion_kn"] = [

    # Q1: Show accelerating motion (the canonical non-uniform demonstration)
    {
        "id": "nonuniform_motion_kn_q1",
        "question": (
            "Show ACCELERATING non-uniform motion — a car that speeds up from rest. "
            "Observe the data table: are the distances in successive seconds equal or unequal? "
            "(ವೇಗ ಹೆಚ್ಚಾಗುವ ಅಸಮ ಚಲನೆ ತೋರಿಸಿ — ಪ್ರತಿ ಸೆಕೆಂಡ್ ದೂರ ಸಮಾನವೇ?)"
        ),
        "action_required": "Set 'initialState' to 'accelerate' to show accelerating motion.",
        "hint": "Select 'accelerate' mode — the car speeds up from 0 to 100 km/h. The graph curves upward and distances in the table increase each second.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "accelerate"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! Accelerating motion shows UNEQUAL distances in successive seconds "
            "(e.g., the car covers more distance in second 5 than in second 1). "
            "This is the definition of non-uniform motion."
        ),
        "failure_message": (
            "Select 'accelerate' from the Motion Mode dropdown to show the accelerating car."
        )
    },

    # Q2: Show decelerating / braking motion
    {
        "id": "nonuniform_motion_kn_q2",
        "question": (
            "Now show DECELERATING motion — a car applying brakes and slowing to a stop. "
            "How does the graph shape differ from accelerating motion? "
            "(ಬ್ರೇಕ್ ಹಾಕಿ ನಿಲ್ಲುವ ಚಲನೆ ತೋರಿಸಿ — ಗ್ರಾಫ್ ಎಂತಿರುತ್ತದೆ?)"
        ),
        "action_required": "Set 'initialState' to 'decelerate' to show braking motion.",
        "hint": "Select 'decelerate' mode — the car slows from 100 km/h to 0. The graph slope decreases (flattens) as speed drops.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "decelerate"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! Braking produces a FLATTENING curve — distances per second shrink "
            "as speed decreases toward zero. Compare: acceleration curves up, "
            "deceleration curves and flattens."
        ),
        "failure_message": (
            "Select 'decelerate' from the Motion Mode dropdown to show braking motion."
        )
    },

    # Q3: Show city traffic (most complex non-uniform pattern)
    {
        "id": "nonuniform_motion_kn_q3",
        "question": (
            "Show CITY TRAFFIC mode — the most realistic example of non-uniform motion with "
            "repeated stop-and-go cycles. Observe how the graph shape differs from both "
            "accelerate and decelerate modes. "
            "(ನಗರ ಸಂಚಾರ ಮೋಡ್ ತೋರಿಸಿ — ಗ್ರಾಫ್ ಹೇಗಿದೆ?)"
        ),
        "action_required": "Set 'initialState' to 'traffic' to show city stop-go motion.",
        "hint": "Select 'traffic' mode — the car cycles through stopped, accelerating, cruising, and braking phases. The distance-time graph is irregular.",
        "conditions": [
            {"parameter": "initialState", "operator": "==", "value": "traffic"}
        ],
        "scoring": {"perfect": 1.0, "acceptable": 0.5, "wrong": 0.0},
        "success_message": (
            "Correct! City traffic is the most common real-world non-uniform motion. "
            "The graph shows flat sections (stopped), upward curves (accelerating), "
            "and nearly straight sections (cruising) — all within one journey."
        ),
        "failure_message": (
            "Select 'traffic' from the Motion Mode dropdown to show the stop-go city traffic pattern."
        )
    }
]


# ═══════════════════════════════════════════════════════════════════════
# HELPER: list of Kannada simulation IDs for sidebar grouping
# ═══════════════════════════════════════════════════════════════════════

KN_SIMULATION_IDS = list(SIMULATIONS_KN.keys())
