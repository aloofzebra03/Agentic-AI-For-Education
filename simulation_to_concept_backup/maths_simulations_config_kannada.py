"""
Maths Simulations Configuration - Kannada (ಕನ್ನಡ)
===================================================
Contains metadata, parameters, concepts, and quiz questions for
Kannada-medium MATHS simulations designed for native-language learners.

These simulations have their UI, labels, and instructions written in Kannada.
The agent pipeline continues to operate in English for consistent evaluation;
the translation layer handles student-facing communication in Kannada.

Each entry follows the EXACT same structure as simulations_config.py so that
all existing helper functions (get_simulation, get_quiz_questions, etc.) work
transparently after this file is merged at runtime.

This file is imported and merged into simulations_config.py at the bottom of
that file via:
    from maths_simulations_config_kannada import SIMULATIONS_MATHS_KN, QUIZ_QUESTIONS_MATHS_KN
    SIMULATIONS.update(SIMULATIONS_MATHS_KN)
    QUIZ_QUESTIONS.update(QUIZ_QUESTIONS_MATHS_KN)
"""

# ═══════════════════════════════════════════════════════════════════════
# KANNADA MATHS SIMULATION DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

SIMULATIONS_MATHS_KN = {}


# =============================================================================
# PLACE VALUE CALCULATOR SIMULATION
# ಸ್ಥಾನ ಬೆಲೆ ಕ್ಯಾಲ್ಕುಲೇಟರ್ – ಸ್ಥಾನ ಬೆಲೆ ಬಟನ್‌ಗಳಿಂದ ಸಂಖ್ಯೆ ನಿರ್ಮಾಣ
# Maths Chapter 1 – Knowing Our Numbers (Place Value)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["place_value_calculator_kn"] = {
    "title": "ಸ್ಥಾನ ಬೆಲೆ ಕ್ಯಾಲ್ಕುಲೇಟರ್ (Place Value Calculator)",

    # Mark as Kannada so the sidebar can group it in the Kannada-Maths section
    "language": "kannada_maths",

    # Relative path from the project root — matches the folder structure
    "file": "maths_simulations_kannada/math_chapter1_simulation1_place_value_calculator_kn.html",

    "description": """
An interactive Kannada-language maths simulation where students build numbers
by pressing coloured place-value buttons (+1, +10, +100, +1K, +10K, +1L, +10L).
A live bar chart updates to show how many of each place value have been used,
and the number is displayed in Indian number format (using commas for lakhs/thousands).

Two modes are available:
- Challenge Mode: a target number is given; students must build it using as few
  clicks as possible, discovering that the minimum clicks equals the digit-sum.
- Free Explore Mode: students build any number freely and observe patterns.

The simulation teaches:
- Place value: ones, tens, hundreds, thousands, ten-thousands, lakhs, ten-lakhs
- Indian place value notation (commas at thousands and lakhs, not just thousands)
- The digit-sum property: minimum clicks to build a number = sum of its digits
- Efficient number decomposition (each digit tells how many times to press that button)

The simulation UI, labels, and narrative are entirely in Kannada for native
language learners. Driving parameters are exposed via URL query strings so
the teaching agent can set the demonstration state directly.
""",

    "cannot_demonstrate": [
        "International (Western) place value notation (millions/billions)",
        "Subtraction or decomposition of numbers",
        "Decimals or fractional place values",
        "Place value beyond ten-lakhs (crores and above)",
        "Negative numbers",
        "Arithmetic operations beyond building a number by addition"
    ],

    # ── Agent-controllable parameters ──────────────────────────────────────
    # mode         : string  – 'challenge' or 'free' — selects the activity mode
    # targetIndex  : int     – 0..9 — selects which target number to show in challenge mode
    # restrict     : string  – 'all', '1000', '100', '10' — limits which buttons are active
    "initial_params": {
        "mode": "challenge",
        "targetIndex": 0,
        "restrict": "all"
    },

    "parameter_info": {
        "mode": {
            "label": "Simulation Mode",
            "range": "challenge, free",
            "url_key": "mode",
            "effect": (
                "Controls which activity mode the simulation opens in.\n"
                "  'challenge' → a target number is displayed; student must build it\n"
                "                using as few clicks as possible (default)\n"
                "  'free'      → free exploration; student can build any number with\n"
                "                no target — good for open-ended discovery"
            )
        },
        "targetIndex": {
            "label": "Target Number Index",
            "range": "0-9 (integer)",
            "url_key": "targetIndex",
            "effect": (
                "In Challenge mode, selects which of the 10 preset target numbers is shown.\n"
                "  0 → 5,072     (4-digit, digit-sum 14 — textbook example)\n"
                "  1 → 8,300     (zero in tens place — tests understanding of zeros)\n"
                "  2 → 40,629    (5-digit number)\n"
                "  3 → 56,354    (5-digit, balanced digits)\n"
                "  4 → 66,666    (all same digit — interesting pattern)\n"
                "  5 → 3,67,813  (6-digit, uses lakh place)\n"
                "  6 → 997       (3-digit, digit-sum 25 — minimum clicks challenge)\n"
                "  7 → 1,00,000  (exactly one lakh — landmark number)\n"
                "  8 → 75,000    (round number in thousands)\n"
                "  9 → 321       (simple 3-digit starter)"
            )
        },
        "restrict": {
            "label": "Button Restriction",
            "range": "all, 1000, 100, 10",
            "url_key": "restrict",
            "effect": (
                "Restricts which place-value buttons the student can press.\n"
                "  'all'  → all buttons available (default — normal play)\n"
                "  '1000' → only +1K button active; student must press it repeatedly;\n"
                "           teaches how many thousands are in large numbers\n"
                "  '100'  → only +100 button active; explores hundreds decomposition\n"
                "  '10'   → only +10 button active; explores tens decomposition"
            )
        }
    },

    # ── Teaching concepts ────────────────────────────────────────────────────
    # 3 concepts in progression: foundation → pattern discovery → application
    "concepts": [
        {
            "id": 1,
            "title": "Place Value: Every Digit Has a Position and a Value",
            "description": (
                "Understanding that the position of a digit in a number determines its value. "
                "In 5,072: the digit 5 means five thousands, 0 means no hundreds, "
                "7 means seven tens, 2 means two ones."
            ),
            "key_insight": (
                "Each place-value button (+1, +10, +100, +1K, etc.) adds exactly that value. "
                "The bar chart shows how many of each place value makes up the number. "
                "5,072 needs 5 presses of +1K, 0 of +100, 7 of +10, and 2 of +1."
            ),
            "related_params": ["mode", "targetIndex"]
        },
        {
            "id": 2,
            "title": "The Digit-Sum Property: Minimum Clicks = Sum of Digits",
            "description": (
                "The minimum number of button-presses needed to build any number is always "
                "equal to the sum of its digits. This reveals why place value notation is "
                "the most efficient way to represent numbers."
            ),
            "key_insight": (
                "For 5,072: digit sum = 5+0+7+2 = 14. You need exactly 14 presses. "
                "This works for ALL numbers — the digit sum tells you the minimum presses. "
                "This IS Indian place value: each digit tells how many times to press that button."
            ),
            "related_params": ["mode", "targetIndex"]
        },
        {
            "id": 3,
            "title": "Indian Place Value System: Ones, Thousands, Lakhs",
            "description": (
                "The Indian place value system groups digits as ones (1-999), "
                "thousands (1,000-99,999), lakhs (1,00,000-99,99,999), and crores. "
                "Commas are placed after every 2 digits from the right (except the first group of 3)."
            ),
            "key_insight": (
                "Indian format: 3,67,813 (not 367,813 as in Western format). "
                "After the first comma (thousands), subsequent commas come every 2 digits: "
                "3 | 67 | 813. The simulation uses Indian notation throughout — "
                "lakhs and ten-lakhs are explicitly shown as separate place values."
            ),
            "related_params": ["mode", "targetIndex", "restrict"]
        }
    ]
}


# =============================================================================
# NUMBER SYSTEMS SIMULATION
# ಭಾರತೀಯ vs ಅಂತರರಾಷ್ಟ್ರೀಯ ಸಂಖ್ಯಾ ವ್ಯವಸ್ಥೆ – Indian vs International Number Systems
# Maths Chapter 1 – Knowing Our Numbers (Number Systems)
# =============================================================================
SIMULATIONS_MATHS_KN["number_systems_kn"] = {
    "title": "ಭಾರತೀಯ vs ಅಂತರರಾಷ್ಟ್ರೀಯ ಸಂಖ್ಯಾ ವ್ಯವಸ್ಥೆ (Number Systems)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter1_simulation2_number_systems_kn.html",
    "description": """
An interactive Kannada-language simulation comparing the Indian and International number
systems side by side. Students explore a number displayed simultaneously in both notations
(Indian: 3-2-2 grouping with commas; International: 3-3-3 grouping) and convert between
systems using a labelled digit strip.

Two modes are available:
- Explore Mode: adjust a slider to choose any number up to 9,99,99,999 and see it in both
  systems instantly, with the full word-name in each system.
- Quiz Mode: comparison questions (e.g., 'Is 30 Thousand < 3 Lakhs?') test understanding of
  relative magnitudes across both systems.

The simulation teaches:
- Indian place value: ones, thousands, ten-thousands, lakhs, ten-lakhs, crores
- International place value: ones, thousands, millions, billions
- Comma-grouping rules for each system (3-2 vs 3-3)
- Cross-system conversion: 1 Crore = 10 Million, 1 Lakh = 100 Thousand
""",
    "cannot_demonstrate": [
        "Decimals or fractions in either number system",
        "Numbers larger than 99,99,99,999 (ten crore / one billion)",
        "Arithmetic operations across number systems",
        "Roman numerals or other historical number systems",
        "Negative numbers"
    ],
    "initial_params": {
        "mode": "explore",
        "number": 4050678
    },
    "parameter_info": {
        "mode": {
            "label": "Simulation Mode",
            "range": "explore, quiz",
            "url_key": "mode",
            "effect": (
                "Controls which activity mode the simulation opens in.\n"
                "  'explore' → slider lets student adjust the number and see both systems side by side\n"
                "  'quiz'    → presents comparison questions (< > =) between Indian and International magnitudes"
            )
        },
        "number": {
            "label": "Starting Number",
            "range": "1 – 999,999,999 (integer)",
            "url_key": "number",
            "effect": (
                "Sets the initial number displayed in explore mode.\n"
                "The digit strip and word-names update instantly to show it in both systems."
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Indian vs International Comma Grouping",
            "description": (
                "The Indian system groups digits as 3 from the right, then 2-2-2 (right to left): "
                "e.g., 40,50,678. The International system groups as 3-3-3: 4,050,678."
            ),
            "key_insight": (
                "The same number looks different in each system because of the comma positions. "
                "40,50,678 (Indian) = 4,050,678 (International). Both represent 'forty lakh fifty thousand six hundred seventy-eight'."
            ),
            "related_params": ["mode", "number"]
        },
        {
            "id": 2,
            "title": "Cross-System Conversion: Lakhs, Crores, Millions",
            "description": (
                "Key conversion facts: 1 Lakh = 1,00,000 = 100 Thousand; "
                "1 Crore = 1,00,00,000 = 10 Million; 100 Crore = 1 Billion."
            ),
            "key_insight": (
                "When comparing across systems, use anchor conversions. "
                "The quiz mode tests these: '500 Lakhs vs 5 Million' — knowing 1 Lakh = 100 Thousand "
                "quickly shows 500 Lakhs = 5,00,00,000 while 5 Million = 50,00,000, so 500 Lakhs > 5 Million."
            ),
            "related_params": ["mode"]
        },
        {
            "id": 3,
            "title": "Reading Large Numbers in Both Systems",
            "description": (
                "Practise reading numbers aloud using both systems: "
                "Indian word-names use 'lakh' and 'crore'; International names use 'million' and 'billion'."
            ),
            "key_insight": (
                "The digit strip shows exactly which comma goes where in each system. "
                "Indian: ...| crore | ten-lakh | lakh | ten-thousand | thousand | hundred | ten | one. "
                "International: ...| billion | hundred-million | ten-million | million | hundred-thousand | ten-thousand | thousand | hundred | ten | one."
            ),
            "related_params": ["mode", "number"]
        }
    ]
}


# =============================================================================
# SENSE OF SCALE SIMULATION
# ಸ್ಕೇಲ್ ಅರಿವು – Large Number Visualisation
# Maths Chapter 1 – Knowing Our Numbers (Large Numbers)
# =============================================================================
SIMULATIONS_MATHS_KN["sense_of_scale_kn"] = {
    "title": "ಸ್ಕೇಲ್ ಅರಿವು — ದೊಡ್ಡ ಸಂಖ್ಯೆ ದೃಶ್ಯೀಕರಣ (Sense of Scale)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter1_simulation3_sense_of_scale_kn.html",
    "description": """
A real-world Kannada-language simulation that makes large numbers tangible by embedding them
in concrete, relatable scenarios. Students adjust sliders and see progress bars scale against
familiar reference quantities.

Five scenario tabs are available:
- Journey (ಪ್ರಯಾಣ): driving at a chosen speed for a chosen number of years — comparing distance
  to the Moon, the Sun, and the Trans-Siberian railway.
- Buses (ಬಸ್‌ಗಳು): filling buses with passengers to try to match city populations (Chintamani,
  Jaipur, Mumbai).
- Weight (ತೂಕ): stacking small items to compare their combined weight against a child, adult,
  or weightlifter.
- Counting (ಎಣಿಕೆ): counting items at a chosen rate — does it fit within an hour, a day, a year?
- Facts (ತಥ್ಯಗಳು): probability-based facts (e.g., chance of getting a specific 10-digit phone number).

The simulation teaches:
- Real-world meaning of numbers in the lakh and crore range
- Relative comparisons using progress bars (are we there yet?)
- Multiplicative reasoning with large factor products
""",
    "cannot_demonstrate": [
        "Exact arithmetic computations step-by-step",
        "Numbers in the billions range",
        "Probability theory beyond intuitive comparison",
        "Geographic or scientific facts beyond the stated scenarios"
    ],
    "initial_params": {
        "scenario": 0
    },
    "parameter_info": {
        "scenario": {
            "label": "Scenario Tab",
            "range": "0-4 (integer)",
            "url_key": "scenario",
            "effect": (
                "Selects which real-world scenario tab the simulation opens on.\n"
                "  0 → Journey (🚀 — driving speed × years vs astronomical distances)\n"
                "  1 → Buses (🚌 — passengers × buses vs city populations)\n"
                "  2 → Weight (⚖️ — item weight × count vs human weights)\n"
                "  3 → Counting (⏱️ — items at rate vs time durations)\n"
                "  4 → Facts (🔢 — probability-based number facts)"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Large Numbers Need Real-World Anchors",
            "description": (
                "Abstract numbers like 1,00,00,000 are hard to sense. "
                "Anchoring them to physical journeys, populations, or time makes them concrete."
            ),
            "key_insight": (
                "Driving 100 km/day for 10 years covers 3,65,000 km — just short of Earth-Moon distance (3,84,400 km). "
                "Suddenly '3.6 lakh' feels like a real and almost reachable scale."
            ),
            "related_params": ["scenario"]
        },
        {
            "id": 2,
            "title": "Multiplicative Scaling with Progress Bars",
            "description": (
                "Progress bars show what fraction of a reference quantity a student's chosen value reaches. "
                "Filling a bar requires multiplying two controllable quantities."
            ),
            "key_insight": (
                "In the Buses scenario: 50 passengers × 2,00,000 buses = 1,00,00,000 (one crore) people — "
                "enough to fill Jaipur nearly three times. This reveals how multiplying modest numbers "
                "quickly reaches crore-scale quantities."
            ),
            "related_params": ["scenario"]
        },
        {
            "id": 3,
            "title": "Comparing Magnitudes: Which Is Bigger?",
            "description": (
                "Comparing two large quantities (e.g., 50 lakh vs Mumbai's 1.24 crore) requires "
                "understanding both numbers in Indian notation and knowing their relative sizes."
            ),
            "key_insight": (
                "Use the progress bar percentage: if the bar shows 40%, the student's number is "
                "less than half the reference. This makes > / < comparisons intuitive without needing "
                "to line up digits."
            ),
            "related_params": ["scenario"]
        }
    ]
}


# =============================================================================
# ROUNDING & ESTIMATION SIMULATION
# ಪೂರ್ಣಾಂಕನ ಮತ್ತು ಅಂದಾಜು – Rounding and Estimation
# Maths Chapter 1 – Knowing Our Numbers (Rounding)
# =============================================================================
SIMULATIONS_MATHS_KN["rounding_estimation_kn"] = {
    "title": "ಪೂರ್ಣಾಂಕನ ಮತ್ತು ಅಂದಾಜು (Rounding and Estimation)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter1_simulation4_rounding_estimation_kn.html",
    "description": """
An interactive Kannada-language simulation that teaches rounding large numbers to the nearest
thousand, ten-thousand, lakh, ten-lakh, and crore using animated number-line visualisations.

Two modes are available:
- Explore Mode: a slider lets the student choose any number; five number lines (one per rounding
  place) update simultaneously, showing the red marker (actual position) and blue snap marker
  (rounded value). The rounded value for each place is displayed alongside the number line.
- Quiz Mode: estimation questions based on real Indian census data and textbook examples test
  whether students can round correctly and compare sums/differences.

The simulation teaches:
- The rounding rule: if the digit in the next smaller place is ≥ 5, round up; else round down
- Visual intuition: where does the number lie on the number line between two multiples?
- Estimation in context: approximating sums of large populations to the nearest lakh/crore
""",
    "cannot_demonstrate": [
        "Rounding to the nearest ten or hundred (the slider minimum is in tens of thousands)",
        "Decimal rounding",
        "Negative number rounding",
        "Numbers larger than 9,99,99,999 (ten crore)"
    ],
    "initial_params": {
        "mode": "explore",
        "number": 38769957
    },
    "parameter_info": {
        "mode": {
            "label": "Simulation Mode",
            "range": "explore, quiz",
            "url_key": "mode",
            "effect": (
                "Controls which activity mode the simulation opens in.\n"
                "  'explore' → number lines show all five rounding places at once for the chosen number\n"
                "  'quiz'    → estimation questions using real census data and textbook numbers"
            )
        },
        "number": {
            "label": "Starting Number",
            "range": "1 – 99,999,999 (integer)",
            "url_key": "number",
            "effect": (
                "Sets the initial number shown by the number lines in explore mode. "
                "All five number lines (nearest thousand up to nearest crore) update to reflect it."
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "The Rounding Rule: ≥ 5 Round Up, < 5 Round Down",
            "description": (
                "To round to a given place, look at the digit immediately to the right. "
                "If it is 5 or more, add 1 to the rounding digit; if less than 5, keep the rounding digit."
            ),
            "key_insight": (
                "For 3,87,69,957 rounded to the nearest crore: the ten-lakh digit is 8 (≥ 5) so round up → 4,00,00,000. "
                "The number lines make this visible: the red marker is closer to the upper end of the interval."
            ),
            "related_params": ["mode", "number"]
        },
        {
            "id": 2,
            "title": "Visual Number Lines for Every Rounding Place",
            "description": (
                "Each number line spans from the lower multiple to the upper multiple of one rounding unit. "
                "The red marker shows the number's exact position; the blue snap shows where it rounds to."
            ),
            "key_insight": (
                "If the red marker is past the midpoint (50%), the blue snap jumps to the right end (round up). "
                "If the red marker is before the midpoint, the blue snap stays at the left end (round down). "
                "Five number lines at once show that a number can round up in some places and down in others."
            ),
            "related_params": ["mode", "number"]
        },
        {
            "id": 3,
            "title": "Estimation Using Rounded Numbers",
            "description": (
                "Adding or comparing city populations is easier when rounded to the nearest lakh. "
                "Estimation is not imprecision — it is deliberate, useful approximation."
            ),
            "key_insight": (
                "4,63,128 + 4,19,682 ≈ 5 lakh + 4 lakh = 9 lakh (both round up). "
                "Exact answer 8,82,810 confirms the estimate is close. "
                "This shows why rounding is a TOOL: it lets you verify a calculation quickly."
            ),
            "related_params": ["mode"]
        }
    ]
}


# =============================================================================
# MULTIPLICATION PATTERNS SIMULATION
# ಗುಣಾಕಾರ ಭಾವನೆ ಮತ್ತು ಅಂಕಿ ಎಣಿಕೆ – Multiplication Patterns and Digit Counting
# Maths Chapter 1 – Knowing Our Numbers (Multiplication)
# =============================================================================
SIMULATIONS_MATHS_KN["multiplication_patterns_kn"] = {
    "title": "ಗುಣಾಕಾರ ಭಾವನೆ ಮತ್ತು ಅಂಕಿ ಎಣಿಕೆ (Multiplication Patterns)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter1_simulation5_multiplication_patterns_kn.html",
    "description": """
An interactive Kannada-language simulation that explores the number of digits in a product
when two numbers are multiplied, and reveals shortcuts for multiplying by 10, 100, 1000, etc.

Four tabs are available:
- Multiply (ಗುಣಿಸಿ): two sliders (A and B) let students set any two numbers; the product is
  displayed instantly along with a 'digit range rule' badge: digits(A) + digits(B) - 1 ≤ digits(product) ≤ digits(A) + digits(B).
- Patterns (ಭಾವನೆ): preset multiplication tables showing how digit counts behave when identical
  numbers are multiplied (e.g., 111×111, 1111×1111).
- Shortcuts (ಶಾರ್ಟ್‌ಕಟ್): rules for multiplying by 10 (append zero), 100 (append two zeros), etc.
- Digit Grid (ಅಂಕಿ ಗ್ರಿಡ್): a 5×5 grid showing digit-count ranges for all combinations of 1-5 digit numbers.

The simulation teaches:
- The digit-count rule for products: product has da + db − 1 or da + db digits
- Why multiplying by 10 appends a zero (place-value shift)
- Estimation of product magnitude without computing it
""",
    "cannot_demonstrate": [
        "Decimal multiplication",
        "Division or factorisation",
        "Numbers beyond 5 digits in the digit grid",
        "Negative number multiplication",
        "Exact products beyond the slider range"
    ],
    "initial_params": {
        "mode": "multiply",
        "numA": 111,
        "numB": 111
    },
    "parameter_info": {
        "mode": {
            "label": "Simulation Tab",
            "range": "multiply, patterns, shortcuts, digitGrid",
            "url_key": "mode",
            "effect": (
                "Controls which activity tab the simulation opens on.\n"
                "  'multiply'  → live sliders show product and digit-count rule badge\n"
                "  'patterns'  → preset multiplication tables showing digit-count patterns\n"
                "  'shortcuts' → rules for ×10, ×100, ×1000 with examples\n"
                "  'digitGrid' → 5×5 grid of digit-count ranges for all A×B combinations"
            )
        },
        "numA": {
            "label": "Number A",
            "range": "1 – 99,999 (integer)",
            "url_key": "numA",
            "effect": (
                "Sets the initial value of slider A in multiplication mode. "
                "The digit count of A is highlighted in the digit grid."
            )
        },
        "numB": {
            "label": "Number B",
            "range": "1 – 99,999 (integer)",
            "url_key": "numB",
            "effect": (
                "Sets the initial value of slider B in multiplication mode. "
                "Both slider values together determine starting product and grid highlight."
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Digit-Count Rule for Products",
            "description": (
                "When multiplying a d_a-digit number by a d_b-digit number, the product always has "
                "either d_a + d_b − 1 or d_a + d_b digits. This lets you estimate the magnitude "
                "of a product before computing it."
            ),
            "key_insight": (
                "111 (3 digits) × 111 (3 digits) = 12,321 (5 digits = 3+3−1). "
                "999 × 999 = 998,001 (6 digits = 3+3). "
                "So 3-digit × 3-digit will always give a 5- or 6-digit product."
            ),
            "related_params": ["mode", "numA", "numB"]
        },
        {
            "id": 2,
            "title": "Multiplication Shortcuts: Appending Zeros",
            "description": (
                "Multiplying any number by 10 shifts every digit one place to the left, "
                "equivalent to appending one zero. Multiplying by 100 appends two zeros, etc."
            ),
            "key_insight": (
                "234 × 10 = 2,340. The digits don't change — each moves one place-value position up. "
                "Place value makes this automatic: ones become tens, tens become hundreds, etc."
            ),
            "related_params": ["mode"]
        },
        {
            "id": 3,
            "title": "Pattern Recognition in Multiplication Tables",
            "description": (
                "Special multiplication tables (e.g., 11×11=121, 111×111=12321, 1111×1111=1234321) "
                "reveal palindrome patterns that arise from the digit-count rule."
            ),
            "key_insight": (
                "111×111 = 12,321 — the product's digits go 1,2,3,2,1. "
                "1111×1111 = 1,234,321 — the pattern extends. "
                "These patterns are not magic; they follow directly from the distributive property "
                "and the place-value structure of the number system."
            ),
            "related_params": ["mode"]
        }
    ]
}


# =============================================================================
# EXPRESSION EVALUATOR SIMULATION
# ಸಮೀಕರಣ ಮೌಲ್ಯಮಾಪನ – Expression Evaluator
# Maths Chapter 2 – Whole Numbers (Algebraic Expressions)
# =============================================================================
SIMULATIONS_MATHS_KN["expression_evaluator_kn"] = {
    "title": "ಸಮೀಕರಣ ಮೌಲ್ಯಮಾಪನ (Expression Evaluator)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter2_simulation1_expression_evaluator_kn.html",
    "description": """
An interactive Kannada-language simulation that teaches students to identify terms in an
algebraic expression and evaluate each term step-by-step before summing them to find the
final value.

The simulation displays a mathematical expression (e.g., '39 − 2×6 + 11') in coloured term
boxes — each distinct term (separated by + or −) gets its own colour. Step-by-step cards then
show:
  Step 1: Identify the terms and count them.
  Step 2: Evaluate each term individually (respecting multiplication/division before addition).
  Step 3: Add all term values to get the final result.

A preset panel lets students select from 12 built-in expressions of increasing complexity.
The 'problem' URL param lets the agent load any specific expression by index.

The simulation teaches:
- Defining a 'term' in an expression (a quantity separated by + or −)
- Evaluating each term independently before combining
- Why BODMAS/PEMDAS matters: multiplication inside a term must be done first
- Reading expressions that mix subtraction (as negative terms) with addition
""",
    "cannot_demonstrate": [
        "Expressions with variables (only numeric expressions)",
        "Expressions with brackets requiring bracket expansion",
        "Expressions longer than 4 terms",
        "Division resulting in non-integer quotients",
        "Floating-point arithmetic"
    ],
    "initial_params": {
        "problem": 0
    },
    "parameter_info": {
        "problem": {
            "label": "Expression Index",
            "range": "0 – 11 (integer)",
            "url_key": "problem",
            "effect": (
                "Selects which of the 12 preset expressions is displayed.\n"
                "  0  → 28 − 7 + 8        (result: 29 — simple mix of add and subtract)\n"
                "  1  → 39 − 2×6 + 11     (result: 38 — introduces multiplication in a term)\n"
                "  2  → 40 − 10 + 10 + 10 (result: 50 — four terms)\n"
                "  3  → 48 − 10×2 + 16÷2  (result: 36 — both multiplication and division)\n"
                "  4  → 6×3 − 4×8×5       (result: −142 — large negative term)\n"
                "  5  → 30 + 5×4           (result: 50 — classic BODMAS starter)\n"
                "  6  → 4×23 + 5           (result: 97)\n"
                "  7  → 6×5 + 3            (result: 33)\n"
                "  8  → 89 + 21 − 10       (result: 100 — landmark answer)\n"
                "  9  → 5×12 − 6           (result: 54)\n"
                "  10 → 4×9 + 2×6          (result: 48 — two multiplication terms)\n"
                "  11 → 13 − 2 + 6         (result: 17)"
            )
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "What Is a Term? Separating an Expression",
            "description": (
                "A term is a quantity in an expression that is separated from others by + or −. "
                "The sign before it is part of the term: '39 − 2×6 + 11' has three terms: 39, −2×6, and 11."
            ),
            "key_insight": (
                "Colour-coded boxes make terms visually distinct. "
                "Counting terms correctly is the first step: '48 − 10×2 + 16÷2' has 3 terms, not 5 — "
                "because 10×2 is one term (multiplication within the term, not a separator)."
            ),
            "related_params": ["problem"]
        },
        {
            "id": 2,
            "title": "Evaluate Each Term First (BODMAS Within a Term)",
            "description": (
                "Before adding terms together, each term must be fully evaluated — "
                "multiplication and division within a term must be computed before any addition or subtraction."
            ),
            "key_insight": (
                "In '39 − 2×6 + 11': evaluate 2×6 = 12 first (not 39−2=37 then ×6). "
                "So the terms are 39, −12, and 11, giving 39 − 12 + 11 = 38. "
                "The step-by-step cards guide this exact sequence."
            ),
            "related_params": ["problem"]
        },
        {
            "id": 3,
            "title": "Summing Signed Terms to Get the Final Value",
            "description": (
                "Once all terms are evaluated, add them algebraically — "
                "treating negative terms as subtraction from the running sum."
            ),
            "key_insight": (
                "For problem 4 ('6×3 − 4×8×5'): term 1 = 18, term 2 = −160. Sum = 18 + (−160) = −142. "
                "The result can be negative! Term evaluation prevents the common error of computing "
                "left-to-right without respecting multiplication priority."
            ),
            "related_params": ["problem"]
        }
    ]
}


# =============================================================================
# BRACKETS & SIGN RULES SIMULATION
# ಆವರಣ ಮತ್ತು ಚಿಹ್ನೆ ನಿಯಮ – Brackets and Sign Rules
# Maths Chapter 2 – Whole Numbers (Brackets)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["brackets_signs_kn"] = {
    "title": "ಆವರಣ ಮತ್ತು ಚಿಹ್ನೆ ನಿಯಮ (Brackets & Sign Rules)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter2_simulation2_brackets_signs_kn.html",
    "description": """
An interactive Kannada-language simulation that teaches the two sign rules when removing
brackets from arithmetic expressions.

Two modes are available:
- Learn Mode: shows 10 stepped examples, each with 'with brackets' → 'without brackets'
  forms side by side, a colour-coded rule badge (flip / keep), three derivation steps,
  and the final value for both forms. A slider and preset buttons let the agent load any
  of the 10 examples directly.
- Quiz Mode: presents an expression with brackets; students pick the correctly expanded
  bracket-free form from 4 options. 10 questions cover a range of minus-before and
  plus-before bracket scenarios, including negative numbers inside brackets.

The simulation teaches:
- MINUS before brackets → every sign inside FLIPS (+ becomes −, − becomes +)
- PLUS before brackets → signs inside stay the same; only brackets are removed
- Why: subtracting a sum a−(b+c) = a−b−c; subtracting a difference a−(b−c) = a−b+c
""",
    "cannot_demonstrate": [
        "Nested brackets (more than one bracket level)",
        "Algebraic expressions with variables",
        "Multiplication outside brackets (only + and − outside)",
        "Expressions with more than two terms inside brackets",
        "Brackets in the middle of multi-step calculations",
    ],
    "initial_params": {
        "mode": "learn",
        "problemIndex": 0,
        "showHints": "true",
    },
    "parameter_info": {
        "mode": {
            "label": "Simulation Mode",
            "range": "learn, quiz",
            "url_key": "mode",
            "effect": (
                "Selects the active tab on load.\n"
                "  'learn' → step-by-step examples of bracket removal (default)\n"
                "  'quiz'  → 10 multiple-choice questions on bracket expansion"
            )
        },
        "problemIndex": {
            "label": "Example Problem Index",
            "range": "0-9 (integer)",
            "url_key": "problemIndex",
            "effect": (
                "In learn mode, selects which of the 10 preset examples is shown.\n"
                "  0 → 200 − (40 + 3)   = 200 − 40 − 3  = 157  (minus, flip)\n"
                "  1 → 500 − (250 − 100) = 500 − 250 + 100 = 350 (minus, flip −100→+100)\n"
                "  2 → 100 − (15 + 56)   = 100 − 15 − 56  = 29  (minus, flip)\n"
                "  3 → 28 + (35 − 10)    = 28 + 35 − 10   = 53  (plus, keep)\n"
                "  4 → 24 + (6 − 4)      = 24 + 6 − 4     = 26  (plus, keep)\n"
                "  5 → 24 − (6 + 4)      = 24 − 6 − 4     = 14  (minus, flip)\n"
                "  6 → 27 − (8 + 3)      = 27 − 8 − 3     = 16  (minus, flip)\n"
                "  7 → 27 − (8 − 3)      = 27 − 8 + 3     = 22  (minus, flip −3→+3)\n"
                "  8 → 14 − (12 − 10)    = 14 − 12 + 10   = 12  (minus, flip)\n"
                "  9 → 14 − (−12 − 10)   = 14 + 12 + 10   = 36  (minus, flip both negative)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true, false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the sign-rule insight box at the bottom of the page.\n"
                "  'true'  → insight box visible (default)\n"
                "  'false' → insight box hidden (for unguided discovery)"
            )
        },
    },
    "concepts": [
        {
            "id": 1,
            "title": "Minus Before Brackets: Every Sign Inside Flips",
            "description": (
                "When a minus sign immediately precedes a bracket, removing the bracket "
                "reverses every sign inside: + becomes − and − becomes +. "
                "Example: 500 − (250 − 100) → 500 − 250 + 100 = 350."
            ),
            "key_insight": (
                "Think of the minus as distributing to each term inside: "
                "−(250 − 100) = (−1)×250 + (−1)×(−100) = −250 + 100. "
                "The rule is a direct consequence of the distributive property with multiplier −1."
            ),
            "related_params": ["mode", "problemIndex"]
        },
        {
            "id": 2,
            "title": "Plus Before Brackets: Signs Stay the Same",
            "description": (
                "When a plus sign immediately precedes a bracket, removing the bracket "
                "leaves all signs inside unchanged. "
                "Example: 28 + (35 − 10) → 28 + 35 − 10 = 53."
            ),
            "key_insight": (
                "A plus outside means +(35 − 10) = (+1)×35 + (+1)×(−10) = 35 − 10. "
                "Nothing flips. Students often correctly flip for minus but wrongly flip for plus — "
                "the simulation's colour badge (green for keep, yellow for flip) reinforces the contrast."
            ),
            "related_params": ["mode", "problemIndex"]
        },
        {
            "id": 3,
            "title": "Why the Rule Works: Subtracting a Difference",
            "description": (
                "Subtracting a difference, a − (b − c), gives a − b + c because you are "
                "subtracting too much (b) and must add back what was over-subtracted (c). "
                "This is a classic NCERT textbook insight."
            ),
            "key_insight": (
                "14 − (12 − 10) = 14 − 12 + 10 = 12. "
                "Without the rule: naively 14 − 12 − 10 = −8 (wrong!). "
                "The expression 14 − (12 − 10) = 14 − 2 = 12. "
                "When we 'subtract a difference', we must add back the subtracted part."
            ),
            "related_params": ["mode", "problemIndex"]
        }
    ]
}


# =============================================================================
# DISTRIBUTIVE PROPERTY SIMULATION
# ವಿಭಾಜಕ ಗುಣ ದೃಶ್ಯ ಅನ್ವೇಷಕ – Distributive Property Visual Explorer
# Maths Chapter 2 – Whole Numbers (Distributive Property)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["distributive_kn"] = {
    "title": "ವಿಭಾಜಕ ಗುಣ ದೃಶ್ಯ ಅನ್ವೇಷಕ (Distributive Property Explorer)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter2_simulation3_distributive_kn.html",
    "description": """
An interactive Kannada-language simulation that visualises the distributive property
a × (b + c) = a × b + a × c through four complementary representations.

Four tabs are available:
- Dot Array (ಚುಕ್ಕೆ ಜಾಲ): a grid of a rows with b blue columns and c green columns.
  Blue and green groups correspond to a×b and a×c respectively; separating and
  combining them shows that both sides equal the same total.
- Area Model (ವಿಸ್ತೀರ್ಣ ಮಾದರಿ): a rectangle of width (b+c) and height a, divided
  by a dashed line. Grid lines make each unit square countable; the areas of the
  two parts (blue = a×b, green = a×c) sum to the whole.
- Mental Math (ಮಾನಸಿಕ ಗಣಿತ): 5 real-world examples (97×25, 95×8, 104×15, 49×50,
  998×7) where re-expressing one factor as a sum or difference of a round number
  makes multiplication easy using the distributive property.
- Quiz (ರಸಪ್ರಶ್ನೆ): 10 fill-in-the-blank questions testing whether students can
  identify the correct operator (+/−), the correct multiplier, or the correct
  decomposition in a distributive equation.

The simulation teaches:
- The distributive property: a×(b+c) = a×b + a×c
- Equivalent visual representations (dots, area) of the same algebraic fact
- Multiplication shortcuts via decomposition (97 = 100 − 3 → 97×25 = 2500 − 75)
""",
    "cannot_demonstrate": [
        "Division distribution (a÷(b+c) ≠ a÷b + a÷c)",
        "Distributive property with more than two addends",
        "Algebraic variables (only numerical examples)",
        "Negative multipliers outside brackets",
        "Decimal or fractional values of a, b, or c"
    ],
    "initial_params": {
        "mode": "dots",
        "a": 3,
        "b": 4,
        "c": 6,
        "mentalMathIndex": 0,
        "showHints": "true",
    },
    "parameter_info": {
        "mode": {
            "label": "Visualisation Tab",
            "range": "dots, area, mental, quiz",
            "url_key": "mode",
            "effect": (
                "Selects the active visualisation tab on load.\n"
                "  'dots'   → dot-array grid (default)\n"
                "  'area'   → area model rectangle\n"
                "  'mental' → mental-math shortcut examples\n"
                "  'quiz'   → 10 fill-in-the-blank practice questions"
            )
        },
        "a": {
            "label": "Rows / Multiplier (a)",
            "range": "1-8 (integer)",
            "url_key": "a",
            "effect": (
                "Sets the number of rows in the dot array and the height of the area rectangle.\n"
                "Represents the multiplier outside the bracket in a×(b+c)."
            )
        },
        "b": {
            "label": "Blue Columns / First Addend (b)",
            "range": "1-10 (integer)",
            "url_key": "b",
            "effect": (
                "Sets the number of blue columns in the dot array and the width of the blue rectangle.\n"
                "Represents the first addend inside the bracket."
            )
        },
        "c": {
            "label": "Green Columns / Second Addend (c)",
            "range": "1-10 (integer)",
            "url_key": "c",
            "effect": (
                "Sets the number of green columns in the dot array and the width of the green rectangle.\n"
                "Represents the second addend inside the bracket."
            )
        },
        "mentalMathIndex": {
            "label": "Mental Math Example Index",
            "range": "0-4 (integer)",
            "url_key": "mentalMathIndex",
            "effect": (
                "In mental-math tab, selects which preset mental-math example is shown.\n"
                "  0 → 97 × 25  = (100−3)×25 = 2500 − 75   = 2425\n"
                "  1 → 95 × 8   = (100−5)×8  = 800  − 40   = 760\n"
                "  2 → 104 × 15 = (100+4)×15 = 1500 + 60   = 1560\n"
                "  3 → 49 × 50  = (50−1)×50  = 2500 − 50   = 2450\n"
                "  4 → 998 × 7  = (1000−2)×7 = 7000 − 14   = 6986"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true, false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the distributive-property insight box at the bottom.\n"
                "  'true'  → insight box visible (default)\n"
                "  'false' → insight box hidden"
            )
        },
    },
    "concepts": [
        {
            "id": 1,
            "title": "The Distributive Property: a × (b + c) = a × b + a × c",
            "description": (
                "Multiplying a number by a sum gives the same result as "
                "multiplying that number by each addend separately and then adding. "
                "This is the core distributive law for multiplication over addition."
            ),
            "key_insight": (
                "3 × (4 + 6) = 3 × 10 = 30. Also, 3×4 + 3×6 = 12 + 18 = 30. "
                "The dot array makes this visible: 3 rows of 10 can be split into "
                "3 rows of 4 (blue) + 3 rows of 6 (green), yet the total count is the same."
            ),
            "related_params": ["mode", "a", "b", "c"]
        },
        {
            "id": 2,
            "title": "Area Model: Rectangle Split by a Dashed Line",
            "description": (
                "An a×(b+c) rectangle can be divided into two smaller rectangles: "
                "a×b (blue) and a×c (green). The total area is the same whether "
                "counted as one rectangle or as the sum of two parts."
            ),
            "key_insight": (
                "The area model (dots or rectangles) is a geometric proof of the distributive property. "
                "It shows that the property is not a rule to memorise but a visual fact: "
                "splitting a rectangle vertically doesn't change its total area."
            ),
            "related_params": ["mode", "a", "b", "c"]
        },
        {
            "id": 3,
            "title": "Mental Math Shortcut: Decompose to a Round Number",
            "description": (
                "Hard multiplications like 97×25 become easy when one factor is "
                "decomposed as a round number ± a small correction: "
                "97 = 100 − 3, so 97×25 = 100×25 − 3×25 = 2500 − 75 = 2425."
            ),
            "key_insight": (
                "The mental math tab shows that the distributive property is not just abstract algebra — "
                "it is the engine behind every multiplication shortcut. "
                "Students who learn to 'see' a hard number as a round number ± correction "
                "can multiply any two-digit number mentally."
            ),
            "related_params": ["mode", "mentalMathIndex"]
        }
    ]
}


# =============================================================================
# EXPRESSION COMPARISON SIMULATION
# ಸಮೀಕರಣ ಹೋಲಿಕೆ – Expression Comparison (Compare Without Computing)
# Maths Chapter 2 – Whole Numbers (Expressions and Comparisons)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["expression_compare_kn"] = {
    "title": "ಸಮೀಕರಣ ಹೋಲಿಕೆ (Expression Comparison)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter2_simulation4_expression_compare_kn.html",
    "description": """
An interactive Kannada-language quiz simulation that trains students to compare two
arithmetic expressions without computing both sides in full. Students see two expressions
side by side with a '?' in the middle, then press <, =, or > as their answer.

15 questions span four reasoning strategies:
- Addition/subtraction change: 1023+125 vs 1022+128 → compare the net change
- Cancellation: 273−145 vs 272−144 → identical change on both sides → equal
- BODMAS order-of-operations: 15+9×18 vs (15+9)×18 → brackets vs no brackets
- Distributive equality: (34−28)×42 vs 34×42−28×42 → both equal 6×42 = 252

The questions are shuffled randomly on each page load. The agent can set questionIndex
to start the student at a specific position in the shuffled deck, giving variety across
quiz sessions. After each answer, a full explanation is shown.

The simulation teaches:
- Reasoning about relative size without full computation
- Applying the distributive property to identify equalities
- Understanding how BODMAS changes the value of an expression
""",
    "cannot_demonstrate": [
        "Expressions with variables or unknowns",
        "Inequality chains (a < b < c)",
        "Comparison of more than two expressions",
        "Fractional or decimal expressions",
        "Ordering more than two values"
    ],
    "initial_params": {
        "questionIndex": 0,
        "showHints": "true",
    },
    "parameter_info": {
        "questionIndex": {
            "label": "Starting Question Index",
            "range": "0-14 (integer)",
            "url_key": "questionIndex",
            "effect": (
                "Sets the starting position in the shuffled question deck.\n"
                "Since questions are randomly shuffled on each page load, this parameter "
                "does not deterministically select a specific question, but allows the agent "
                "to start the student at different points in the deck across sessions.\n"
                "  0  → start from position 0 in shuffled deck (default)\n"
                "  7  → start from position 7 (encounters BODMAS/bracket questions)\n"
                "  9  → start from position 9 (encounters distributive equality questions)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true, false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the comparison-strategy insight box at the bottom.\n"
                "  'true'  → insight box visible (default)\n"
                "  'false' → insight box hidden (tests unguided reasoning)"
            )
        },
    },
    "concepts": [
        {
            "id": 1,
            "title": "Compare by Spotting What Changed",
            "description": (
                "Instead of computing both sides, look at what is different between the two expressions. "
                "If one side gains more than it loses relative to the other, it is larger."
            ),
            "key_insight": (
                "1023+125 vs 1022+128: left side decreases by 1 (1023→1022), right side increases by 3 (125→128). "
                "Net: right side gains 2 more → left < right. "
                "Never computed the totals directly!"
            ),
            "related_params": ["questionIndex"]
        },
        {
            "id": 2,
            "title": "Distributive Property Reveals Hidden Equality",
            "description": (
                "When (a−b)×c appears next to a×c − b×c, recognising the distributive law "
                "shows both sides are equal without any calculation."
            ),
            "key_insight": (
                "(34−28)×42 vs 34×42 − 28×42. Right side expands the left side by distribution: "
                "(34−28)×42 = 34×42 − 28×42 (distributive law). Both = 6×42 = 252. "
                "Recognising the pattern avoids all multiplication."
            ),
            "related_params": ["questionIndex"]
        },
        {
            "id": 3,
            "title": "BODMAS: Brackets Change the Computation Order",
            "description": (
                "Adding brackets around an addition before a multiplication "
                "forces the addition to happen first, dramatically changing the result."
            ),
            "key_insight": (
                "15 + 9×18 vs (15+9)×18: without brackets, only 9 is multiplied by 18 → 15 + 162 = 177. "
                "With brackets, the whole sum (24) is multiplied by 18 → 432. "
                "The bracketed form is more than twice as large."
            ),
            "related_params": ["questionIndex"]
        }
    ]
}


# =============================================================================
# EXPRESSION ENGINEER SIMULATION
# ಸಮೀಕರಣ ಎಂಜಿನಿಯರ್ – Expression Engineer (Build Target Values)
# Maths Chapter 2 – Whole Numbers (Expressions and Brackets)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["expression_engineer_kn"] = {
    "title": "ಸಮೀಕರಣ ಎಂಜಿನಿಯರ್ (Expression Engineer)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter2_simulation5_expression_engineer_kn.html",
    "description": """
An interactive Kannada-language puzzle simulation where students build arithmetic
expressions from a fixed set of digits to match target values — exploring how
operator choice and bracket placement change the result radically.

Four challenges are available:
- Three 3s (ಮೂರು 3ಗಳು): use exactly three 3s with +, −, ×, ÷ and brackets to make
  each value in {0,1,2,3,...,12}.
- Four 4s (ನಾಲ್ಕು 4ಗಳು): use exactly four 4s to make every integer from 1 to 20
  (a famous NCERT textbook puzzle on page 45).
- Use 2, 3, 5 (2, 3, 5 ಬಳಸಿ): use each of 2, 3, 5 exactly once to make
  {−6, −4, 0, 1, 4, 6, 10}.
- Pay ₹432 (₹432 ಪಾವತಿ): express ₹432 as a sum of products of currency denominations
  (₹1, ₹5, ₹10, ₹20, ₹50, ₹100).

A progress grid shows found / not-found / current target cells. Solutions are recorded
for the current session. Hints are available for hard targets.

The simulation teaches:
- Operator precedence (BODMAS): multiplying before adding, brackets override all
- How brackets change an expression's value radically
- Flexible arithmetic thinking: multiple valid expressions per target
- Real-world application: currency decomposition as a distributive product
""",
    "cannot_demonstrate": [
        "Expressions requiring fractions (except where integer division is exact)",
        "Using more or fewer digits than specified for each challenge",
        "Building numbers outside each challenge's defined target set",
        "Exponentiation or factorial operations",
        "Multi-variable algebraic expressions"
    ],
    "initial_params": {
        "challenge": "three3s",
        "showHints": "true",
    },
    "parameter_info": {
        "challenge": {
            "label": "Challenge Type",
            "range": "three3s, four4s, use235, pay432",
            "url_key": "challenge",
            "effect": (
                "Selects which digit challenge opens on load.\n"
                "  'three3s' → use exactly three 3s to make 0–12 (default)\n"
                "  'four4s'  → use exactly four 4s to make 1–20 (NCERT pg 45 puzzle)\n"
                "  'use235'  → use 2, 3, 5 each exactly once to make {−6,−4,0,1,4,6,10}\n"
                "  'pay432'  → express ₹432 using currency denominations"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true, false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the insight box at the bottom.\n"
                "  'true'  → insight box visible (default)\n"
                "  'false' → insight box hidden"
            )
        },
    },
    "concepts": [
        {
            "id": 1,
            "title": "Same Digits, Different Operators → Different Results",
            "description": (
                "Changing the operators between the same set of digits can produce completely "
                "different results. The expression 3+3−3, 3×3+3, 3×3−3, and (3+3)/3 "
                "all use three 3s but give 3, 12, 6, and 2 respectively."
            ),
            "key_insight": (
                "In the Three 3s challenge: try making 0 = (3−3)×3, then 6 = 3×3−3, then 12 = 3×3+3. "
                "Each successive target requires a different operator combination with identical digits. "
                "This shows that the OPERATOR, not just the digits, determines the value."
            ),
            "related_params": ["challenge"]
        },
        {
            "id": 2,
            "title": "Brackets Change Everything: BODMAS in Action",
            "description": (
                "Placing brackets around part of an expression forces that sub-expression "
                "to be evaluated first, overriding the usual multiplication-before-addition order."
            ),
            "key_insight": (
                "Four 4s: 4+4÷4+4 = 4+1+4 = 9 (without brackets, ÷ first). "
                "(4+4)÷(4+4) = 8÷8 = 1 (with brackets, additions happen inside first). "
                "Same digits, same operators, different bracket positions → completely different values. "
                "This is the most direct demonstration of BODMAS rule."
            ),
            "related_params": ["challenge"]
        },
        {
            "id": 3,
            "title": "Currency as Sums of Products",
            "description": (
                "₹432 can be expressed as 4×100 + 1×20 + 1×10 + 2×1 or "
                "as 8×50 + 1×10 + 4×5 + 2×1 — both are sums of denomination×count products. "
                "This is the real-world meaning of the distributive property."
            ),
            "key_insight": (
                "The ₹432 challenge mirrors how we physically make change: "
                "choose how many of each denomination so the sum equals the target. "
                "Mathematically, this is: amount = Σ (count × denomination), "
                "a direct application of multiplication and addition."
            ),
            "related_params": ["challenge"]
        }
    ]
}


# =============================================================================
# DECIMAL NUMBER LINE SIMULATION
# ದಶಮಾಂಶ ಸಂಖ್ಯಾರೇಖೆ – Decimal Number Line (Zoom and Explore)
# Maths Chapter 3 – Playing with Numbers (Decimals)
# Student level: medium
# =============================================================================
SIMULATIONS_MATHS_KN["decimal_number_line_kn"] = {
    "title": "ದಶಮಾಂಶ ಸಂಖ್ಯಾರೇಖೆ (Decimal Number Line)",
    "language": "kannada_maths",
    "file": "maths_simulations_kannada/math_chapter3_simulation1_decimal_number_line_kn.html",
    "description": """
An interactive Kannada-language simulation that helps students locate decimal numbers
on a number line through progressive zoom, discover patterns in decimal sequences,
and answer quiz questions about decimal place value.

Three tabs are available:
- Explore (ಅನ್ವೇಷಿಸಿ): a slider selects any decimal from 0.000 to 9.999. Three stacked
  number lines (zoom levels 1, 2, 3) show the number's position between consecutive
  whole numbers, between consecutive tenths, and between consecutive hundredths.
  Pre-set buttons load notable examples (4.185, 0.274, 9.876, 0.407, 1.5, 0.05).
- Sequence (ಅನುಕ್ರಮ): 7 preset arithmetic sequences with decimal step, each showing
  known terms (white) and predicted next 3 terms (yellow). Students discover the
  step size and verify their predictions.
- Quiz (ರಸಪ್ರಶ್ನೆ): 10 multiple-choice questions covering position on number line,
  comparing decimals, trailing zeros (0.2 = 0.20 ≠ 0.02), and converting tenths/hundredths.

The simulation teaches:
- Each decimal place divides the previous unit into 10 equal parts
- Successive zoom reveals increasing precision: tenths → hundredths → thousandths
- Trailing zeros (0.20) do not change value; position zeros (0.02) do
- Comparing decimals column by column from the decimal point
""",
    "cannot_demonstrate": [
        "Negative decimal numbers",
        "Decimal arithmetic (addition/subtraction with carrying)",
        "Decimals beyond the thousandths place",
        "Converting fractions to decimals algorithmically",
        "Irrational or recurring decimals"
    ],
    "initial_params": {
        "mode": "explore",
        "num": 4.185,
        "seqIndex": 0,
        "quizIndex": 0,
        "showHints": "true",
    },
    "parameter_info": {
        "mode": {
            "label": "Simulation Tab",
            "range": "explore, sequence, quiz",
            "url_key": "mode",
            "effect": (
                "Selects the active tab on load.\n"
                "  'explore'  → three zoom-level number lines (default)\n"
                "  'sequence' → decimal arithmetic-sequence patterns\n"
                "  'quiz'     → 10 multiple-choice decimal questions"
            )
        },
        "num": {
            "label": "Decimal Number",
            "range": "0.001 – 9.999 (float, 3 decimal places)",
            "url_key": "num",
            "effect": (
                "In explore mode, sets the decimal value shown on all three zoom-level number lines.\n"
                "The purple marker moves to the exact position; the description below the display "
                "lists the units, tenths, hundredths, and thousandths components."
            )
        },
        "seqIndex": {
            "label": "Sequence Preset Index",
            "range": "0-6 (integer)",
            "url_key": "seqIndex",
            "effect": (
                "In sequence tab, selects which preset arithmetic sequence is shown.\n"
                "  0 → 4.4, 4.8, 5.2, 5.6  (step +0.4)  — gentle intro to decimal sequences\n"
                "  1 → 4.4, 4.45, 4.5       (step +0.05) — hundredths-step pattern\n"
                "  2 → 25.75, 26.25, 26.75  (step +0.5)  — half-step pattern\n"
                "  3 → 10.56, 10.67, 10.78  (step +0.11) — hundredths step\n"
                "  4 → 8.5, 9.4, 10.3       (step +0.9)  — tenths close to whole units\n"
                "  5 → 5, 4.95, 4.90        (step −0.05) — decreasing hundredths\n"
                "  6 → 12.45, 11.95, 11.45  (step −0.5)  — decreasing by 0.5"
            )
        },
        "quizIndex": {
            "label": "Starting Quiz Question",
            "range": "0-9 (integer)",
            "url_key": "quizIndex",
            "effect": (
                "In quiz tab, sets the starting question index.\n"
                "  0 → 'Where is 1.4 on the number line?' (position)\n"
                "  1 → 'Which is greater: 1.23 or 1.32?' (comparison)\n"
                "  3 → 'Are 0.2 and 0.20 equal?' (trailing zeros)\n"
                "  4 → 'Are 0.2 and 0.02 equal?' (position zeros)\n"
                "  5 → 'Which is closest to 1: 0.9, 1.01, 1.1?' (proximity)\n"
                "  8 → 'What is 234 tenths in decimal?' (conversion)"
            )
        },
        "showHints": {
            "label": "Show Hints",
            "range": "true, false",
            "url_key": "showHints",
            "effect": (
                "Controls visibility of the zoom-explanation insight box at the bottom.\n"
                "  'true'  → insight box visible (default)\n"
                "  'false' → insight box hidden"
            )
        },
    },
    "concepts": [
        {
            "id": 1,
            "title": "Each Decimal Place is 10× More Precise",
            "description": (
                "The tenths place divides each whole unit into 10 equal parts. "
                "The hundredths place divides each tenth into 10 equal parts (giving 100 per whole unit). "
                "The thousandths place divides each hundredth into 10 (1000 per whole unit)."
            ),
            "key_insight": (
                "Set num=4.185 in explore mode. Zoom level 1: marker between 4 and 5. "
                "Zoom level 2: marker between 4.1 and 4.2. "
                "Zoom level 3: marker between 4.18 and 4.19. "
                "Each zoom level 'magnifies' one interval by 10×, showing increasing precision."
            ),
            "related_params": ["mode", "num"]
        },
        {
            "id": 2,
            "title": "Comparing Decimals: Column by Column From the Decimal Point",
            "description": (
                "To compare 1.23 and 1.32: both have 1 whole unit; "
                "compare tenths (2 vs 3) — since 3 > 2, we know 1.32 > 1.23 "
                "without looking at hundredths."
            ),
            "key_insight": (
                "1.009 vs 1.090: same whole (1), same tenths (0 in both), "
                "compare hundredths: 0 vs 9 → 1.090 > 1.009. "
                "A digit in a higher place (hundredths) dominates digits in lower places. "
                "The quiz question at index 2 tests this."
            ),
            "related_params": ["mode", "quizIndex"]
        },
        {
            "id": 3,
            "title": "Trailing Zeros vs Position Zeros",
            "description": (
                "0.2 = 0.20 = 0.200 (trailing zeros after the last non-zero digit do not change value). "
                "But 0.2 ≠ 0.02 ≠ 0.002 (leading zeros after the decimal point DO change value — "
                "these are 'position zeros' that shift the significant digit to a smaller place)."
            ),
            "key_insight": (
                "0.2 = 2 tenths. 0.20 = 20 hundredths = 2 tenths. Same position, same value. "
                "0.02 = 2 hundredths — the 2 is in a different (smaller) place! "
                "Number line: 0.2 is far right; 0.02 is 10× closer to 0."
            ),
            "related_params": ["mode", "num", "quizIndex"]
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════
# QUIZ QUESTIONS — KANNADA MATHS SIMULATIONS
# ═══════════════════════════════════════════════════════════════════════

QUIZ_QUESTIONS_MATHS_KN = {}


# =============================================================================
# PLACE VALUE CALCULATOR — QUIZ QUESTIONS
# 3 questions: understand place value → discover digit-sum property → apply lakh notation
#
# Quiz parameters:
#   mode        (string): 'challenge' | 'free'
#   targetIndex (int):    0..9
#   restrict    (string): 'all' | '1000' | '100' | '10'
#   The student selects from dropdowns/number inputs in the Streamlit quiz UI.
#   The simulation iframe reflects the chosen values via URL params:
#     ?mode=challenge&targetIndex=0&restrict=all
#   Evaluation uses string/numeric equality (handled by quiz_rules.py fallback).
# =============================================================================

QUIZ_QUESTIONS_MATHS_KN["place_value_calculator_kn"] = [

    # ── Q1: Understand place value with the textbook 5,072 example ─────────
    {
        "id": "place_value_kn_q1",
        "challenge": (
            "Set the simulation to Challenge mode and select the textbook number 5,072 "
            "(index 0) as the target. This is the classic example used in the NCERT textbook "
            "for Class 6 place value. Observe how many of each place-value button you need "
            "to press to reach 5,072 using the minimum clicks.\n\n"
            "(ಪಠ್ಯಪುಸ್ತಕದ ಉದಾಹರಣೆ 5,072 ಗುರಿಯಾಗಿ ಇಟ್ಟು ಸವಾಲು ಮೋಡ್ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["mode", "targetIndex"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "mode",
                    "operator": "==",
                    "value": "challenge"
                },
                {
                    "parameter": "targetIndex",
                    "operator": "==",
                    "value": 0
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
                "Set Mode to 'challenge' and Target Number Index to 0. "
                "Index 0 loads the textbook example 5,072. "
                "Then observe: you need 5 presses of +1K, 0 of +100, 7 of +10, 2 of +1 — "
                "that is exactly 14 minimum clicks (= 5+0+7+2, the digit sum)."
            ),
            "attempt_2": (
                "Choose mode='challenge' and targetIndex=0. "
                "The target 5,072 will appear. Notice the bar chart: bar for 'ಸಾವಿರ' (+1K) "
                "must reach height 5, 'ಹತ್ತು' (+10) must reach 7, 'ಒಂದು' (+1) must reach 2, "
                "and 'ನೂರು' (+100) stays at 0."
            ),
            "attempt_3": (
                "Select mode='challenge' and targetIndex=0 to load 5,072. "
                "The minimum clicks = digit sum of 5,072 = 5+0+7+2 = 14. "
                "This is the key insight: place value tells you HOW MANY times to press each button."
            )
        },
        "concept_reminder": (
            "Place value: 5,072 = 5×1000 + 0×100 + 7×10 + 2×1. "
            "Each digit tells how many of that place value the number contains. "
            "The digit in the thousands place (5) means five thousands; "
            "the digit in the tens place (7) means seven tens. "
            "(ಪ್ರತಿ ಅಂಕಿ ಪ್ರತಿ ಸ್ಥಾನ ಬೆಲೆಯಲ್ಲಿ ಎಷ್ಟಿದೆ ಎಂದು ತಿಳಿಸುತ್ತದೆ!)"
        )
    },

    # ── Q2: Discover the digit-sum property with a lakh-scale number ───────
    {
        "id": "place_value_kn_q2",
        "challenge": (
            "Now select the 6-digit number 3,67,813 (targetIndex 5) in Challenge mode. "
            "This number uses the lakh place value. Before clicking, calculate its digit sum "
            "(3+6+7+8+1+3 = 28). This should be the minimum number of button presses. "
            "Set the simulation to show this target.\n\n"
            "(6 ಅಂಕಿಯ ಸಂಖ್ಯೆ 3,67,813 ಗುರಿಯಾಗಿ ಇಟ್ಟು ಲಕ್ಷ ಸ್ಥಾನ ಬೆಲೆ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["mode", "targetIndex"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "mode",
                    "operator": "==",
                    "value": "challenge"
                },
                {
                    "parameter": "targetIndex",
                    "operator": "==",
                    "value": 5
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
                "Set mode='challenge' and targetIndex=5. "
                "Index 5 loads 3,67,813 — a six-digit number with a lakh digit. "
                "Digit sum = 3+6+7+8+1+3 = 28. You need 28 minimum clicks — "
                "including 3 presses of the +1L (lakh) button."
            ),
            "attempt_2": (
                "Choose mode='challenge' and targetIndex=5 to load 3,67,813. "
                "The bar for 'ಲಕ್ಷ' (+1L) should show 3, 'ಹ.ಸಾವಿರ' (+10K) shows 6, "
                "'ಸಾವಿರ' (+1K) shows 7, 'ನೂರು' (+100) shows 8, 'ಹತ್ತು' (+10) shows 1, "
                "'ಒಂದು' (+1) shows 3."
            ),
            "attempt_3": (
                "Set mode='challenge', targetIndex=5 for 3,67,813. "
                "This demonstrates Indian lakh notation: 3,67,813 is 'three lakh sixty-seven "
                "thousand eight hundred thirteen'. The lakh place is the 6th digit from the right."
            )
        },
        "concept_reminder": (
            "3,67,813 = 3×1,00,000 + 6×10,000 + 7×1,000 + 8×100 + 1×10 + 3×1. "
            "In the Indian system, one lakh = 1,00,000 (not 100,000 written as in the West). "
            "Digit sum = 3+6+7+8+1+3 = 28 = minimum clicks to build this number. "
            "(ಡಿಜಿಟ್ ಮೊತ್ತ = ಕನಿಷ್ಠ ಕ್ಲಿಕ್‌ಗಳು — ಸ್ಥಾನ ಬೆಲೆ ವ್ಯವಸ್ಥೆಯ ಸೊಬಗು!)"
        )
    },

    # ── Q3: Explore zeros in place value with restrict mode ─────────────────
    {
        "id": "place_value_kn_q3",
        "challenge": (
            "Set the simulation to Challenge mode with target number 1,00,000 "
            "(one lakh, targetIndex 7), AND restrict the buttons to '+1K only' "
            "(restrict='1000'). Count how many presses of +1K it takes to reach one lakh. "
            "This shows how many thousands are in one lakh.\n\n"
            "(ಒಂದು ಲಕ್ಷ ತಲುಪಲು +1K ಮಾತ್ರ ಬಳಸಿ — ಎಷ್ಟು ಬಾರಿ ಒತ್ತಬೇಕು?)"
        ),
        "target_parameters": ["mode", "targetIndex", "restrict"],
        "success_rule": {
            "conditions": [
                {
                    "parameter": "mode",
                    "operator": "==",
                    "value": "challenge"
                },
                {
                    "parameter": "targetIndex",
                    "operator": "==",
                    "value": 7
                },
                {
                    "parameter": "restrict",
                    "operator": "==",
                    "value": "1000"
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
                "Set mode='challenge', targetIndex=7 (for 1,00,000), and restrict='1000'. "
                "With only +1K available, you must press it 100 times to reach one lakh. "
                "This concretely shows: 1 lakh = 100 thousands."
            ),
            "attempt_2": (
                "Choose mode='challenge', targetIndex=7, restrict='1000'. "
                "1,00,000 ÷ 1,000 = 100 presses required. "
                "The bar chart will show the 'ಸಾವಿರ' bar reaching count 100 "
                "before the 'ಲಕ್ಷ' bar activates — revealing the place-value relationship."
            ),
            "attempt_3": (
                "Set targetIndex=7 (1,00,000) and restrict='1000'. "
                "You need exactly 100 presses of +1K to reach one lakh. "
                "Answer to 'how many thousands in one lakh?' is 100. "
                "This is the key relationship: 1 lakh = 100 thousand = 1,000 × 100."
            )
        },
        "concept_reminder": (
            "1,00,000 (one lakh) = 100 × 1,000 (one thousand). "
            "The zero digits in 1,00,000 are significant: they show that there are "
            "no hundreds, no tens, and no ones — ONLY the lakh place has a value. "
            "Zeros as place-holders are essential: without them, the number would read '1' not '1,00,000'. "
            "(ಸೊನ್ನೆ ಸ್ಥಾನ ಭರ್ತಿ ಮಾಡುತ್ತದೆ — ಇಲ್ಲದಿದ್ದರೆ 1,00,000 ಬರೀ 1 ಆಗಿಬಿಡುತ್ತಿತ್ತು!)"
        )
    }
]


# =============================================================================
# NUMBER SYSTEMS — QUIZ QUESTIONS
# 3 questions: explore Indian notation → learn cross-system conversion → quiz mode
# =============================================================================
QUIZ_QUESTIONS_MATHS_KN["number_systems_kn"] = [

    {
        "id": "number_systems_kn_q1",
        "challenge": (
            "Set the simulation to Explore mode and enter the number 40,50,678 (four crore "
            "fifty lakh six hundred seventy-eight). Observe how the same number is shown in "
            "the Indian system (40,50,678) and the International system (4,050,678) side by side.\n\n"
            "(ಸಂಖ್ಯೆ 4050678 ಅನ್ನು ಭಾರತೀಯ ಮತ್ತು ಅಂತರರಾಷ್ಟ್ರೀಯ ವ್ಯವಸ್ಥೆಗಳಲ್ಲಿ ತೋರಿಸಿ)"
        ),
        "target_parameters": ["mode", "number"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "explore"},
                {"parameter": "number", "operator": "==", "value": 4050678}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='explore' and number=4050678. "
                "Indian: 40,50,678 (comma after every 2 digits from right, first group of 3). "
                "International: 4,050,678 (comma after every 3 digits from right)."
            ),
            "attempt_2": (
                "Choose mode='explore' and number=4050678. "
                "The digit strip shows both comma placements simultaneously — "
                "red commas for the Indian system, blue commas for International."
            ),
            "attempt_3": (
                "Set mode='explore', number=4050678. "
                "Word name (Indian): 'Forty Lakh Fifty Thousand Six Hundred Seventy-Eight'. "
                "Word name (International): 'Four Million Fifty Thousand Six Hundred Seventy-Eight'."
            )
        },
        "concept_reminder": (
            "40,50,678 (Indian) = 4,050,678 (International). "
            "Indian groups: 3 from right, then 2-2. International groups: 3-3-3 from right. "
            "The numbers are identical — only the comma placement rules differ."
        )
    },

    {
        "id": "number_systems_kn_q2",
        "challenge": (
            "Use the simulation in Quiz mode. Answer the comparison question: "
            "'500 Lakhs ___ 5 Million' (is it <, >, or =?). "
            "Use the explore mode to check: enter 50000000 (5 crore) to see 500 Lakhs, "
            "then check what 5 Million equals in Indian notation.\n\n"
            "(ರಸಪ್ರಶ್ನೆ ಮೋಡ್‌ನಲ್ಲಿ 500 Lakhs vs 5 Million ಹೋಲಿಸಿ)"
        ),
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "quiz"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='quiz'. "
                "500 Lakhs = 500 × 1,00,000 = 5,00,00,000 (five crore). "
                "5 Million = 50,00,000 (fifty lakh). "
                "So 500 Lakhs > 5 Million."
            ),
            "attempt_2": (
                "Use mode='quiz'. "
                "Key anchor: 1 Lakh = 100 Thousand = 0.1 Million. "
                "Therefore 500 Lakhs = 50 Million, NOT 5 Million. "
                "500 Lakhs is 10× larger than 5 Million."
            ),
            "attempt_3": (
                "Select mode='quiz'. "
                "To compare: 1 Million = 10 Lakh. So 5 Million = 50 Lakh. "
                "500 Lakh > 50 Lakh → 500 Lakhs > 5 Million. Answer: >."
            )
        },
        "concept_reminder": (
            "Conversion anchors: 1 Million = 10 Lakh; 1 Billion = 100 Crore. "
            "500 Lakhs = 50 Million (not 5 Million). "
            "Always convert both numbers to the same system before comparing."
        )
    },

    {
        "id": "number_systems_kn_q3",
        "challenge": (
            "Set the simulation to explore mode and enter 1,00,00,000 (one crore = 10 million). "
            "This is the key conversion anchor between the two systems. "
            "Observe both the Indian word name (One Crore) and the International word name (Ten Million).\n\n"
            "(1 ಕೋಟಿ = 10 ಮಿಲಿಯನ್ ಎಂದು ತೋರಿಸಿ)"
        ),
        "target_parameters": ["mode", "number"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "explore"},
                {"parameter": "number", "operator": "==", "value": 10000000}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='explore' and number=10000000 (one crore). "
                "Indian: 1,00,00,000. International: 10,000,000. "
                "Indian name: 'One Crore'. International name: 'Ten Million'."
            ),
            "attempt_2": (
                "Choose mode='explore', number=10000000. "
                "This shows the key anchor: 1 Crore = 10 Million = 10,000 Thousand."
            ),
            "attempt_3": (
                "mode='explore', number=10000000. "
                "1 Crore has 8 digits (1 followed by 7 zeros). "
                "In International it is 10 Million — the digit strip clearly shows both comma styles."
            )
        },
        "concept_reminder": (
            "1 Crore (Indian) = 10 Million (International). "
            "1,00,00,000 (Indian notation) = 10,000,000 (International notation). "
            "This is the most important cross-system anchor for Class 6 students."
        )
    }
]


# =============================================================================
# SENSE OF SCALE — QUIZ QUESTIONS
# 3 questions: journey scenario → buses scenario → counting scenario
# =============================================================================
QUIZ_QUESTIONS_MATHS_KN["sense_of_scale_kn"] = [

    {
        "id": "sense_of_scale_kn_q1",
        "challenge": (
            "Open the Journey scenario (scenario 0). Set the speed to 100 km/day and the "
            "duration to 10 years. Observe what fraction of the Earth-Moon distance "
            "(3,84,400 km) you can cover. "
            "How many kilometres does 100 km/day for 10 years give?\n\n"
            "(ಪ್ರಯಾಣ ಸನ್ನಿವೇಶ: 100 km/day × 10 years ಎಷ್ಟು km?)"
        ),
        "target_parameters": ["scenario"],
        "success_rule": {
            "conditions": [
                {"parameter": "scenario", "operator": "==", "value": 0}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set scenario=0 (Journey). Use speed=100 km/day, years=10. "
                "Distance = 100 × 365 × 10 = 3,65,000 km. "
                "Earth-Moon distance = 3,84,400 km. We reach about 94.9%!"
            ),
            "attempt_2": (
                "Select scenario=0. "
                "3,65,000 km is just short of the Moon. "
                "This shows '3.65 lakh' is a real, tangible scale — almost Moon distance."
            ),
            "attempt_3": (
                "Choose scenario=0 to open the Journey tab. "
                "100 km/day × 365 days × 10 years = 3,65,000 km = 3 lakh 65 thousand km. "
                "This gives intuitive meaning to a 6-digit number."
            )
        },
        "concept_reminder": (
            "3,65,000 km ≈ 3.65 lakh km. The Moon is 3,84,400 km away. "
            "Driving 100 km/day for 10 years gets you 95% of the way to the Moon. "
            "This makes '3 lakh' a viscerally understandable quantity."
        )
    },

    {
        "id": "sense_of_scale_kn_q2",
        "challenge": (
            "Open the Buses scenario (scenario 1). Set capacity to 50 passengers per bus "
            "and count to 2,00,000 buses. Compare the total passenger count to the population "
            "of Mumbai (1,24,42,373). Does the bus fleet carry more or fewer people than Mumbai?\n\n"
            "(ಬಸ್ ಸನ್ನಿವೇಶ: 50 × 2,00,000 = ? — ಮುಂಬೈ ಜನಸಂಖ್ಯೆಗಿಂತ ಹೆಚ್ಚೇ?)"
        ),
        "target_parameters": ["scenario"],
        "success_rule": {
            "conditions": [
                {"parameter": "scenario", "operator": "==", "value": 1}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set scenario=1 (Buses). 50 passengers × 2,00,000 buses = 1,00,00,000 people (1 crore). "
                "Mumbai's population = 1,24,42,373 (about 1.24 crore). "
                "Our fleet carries slightly less than Mumbai's population."
            ),
            "attempt_2": (
                "Use scenario=1. "
                "50 × 2,00,000 = 1,00,00,000. Mumbai = 1,24,42,373. "
                "The progress bar for Mumbai shows ~80% — we don't quite reach Mumbai's size."
            ),
            "attempt_3": (
                "Select scenario=1. "
                "To exceed Mumbai (1.24 crore) with 50-passenger buses, you need 50 × 2,49,000 ≈ 1.24 crore. "
                "This shows that '1 crore' and 'Mumbai's population' are in the same magnitude range."
            )
        },
        "concept_reminder": (
            "50 × 2,00,000 = 1,00,00,000 = 1 crore. "
            "Mumbai's population ≈ 1.24 crore. "
            "Multiplying two relatively small numbers (50 and 2 lakh) gives a crore-scale result — "
            "demonstrating why multiplication is a powerful tool for working with large numbers."
        )
    },

    {
        "id": "sense_of_scale_kn_q3",
        "challenge": (
            "Open the Counting scenario (scenario 3). Set the target to 10,00,000 (ten lakh) "
            "items and the counting rate to 1 item per second. How long does it take to count "
            "ten lakh items — is it within one day, one year, or more?\n\n"
            "(ಎಣಿಕೆ ಸನ್ನಿವೇಶ: 10 ಲಕ್ಷ ವಸ್ತುಗಳನ್ನು 1/ಸೆಕೆಂಡ್ ವೇಗದಲ್ಲಿ ಎಣಿಸಲು ಎಷ್ಟು ಸಮಯ?)"
        ),
        "target_parameters": ["scenario"],
        "success_rule": {
            "conditions": [
                {"parameter": "scenario", "operator": "==", "value": 3}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set scenario=3 (Counting). target=1000000, rate=1 item/second. "
                "10,00,000 seconds ÷ 86,400 seconds/day ≈ 11.6 days. "
                "More than one day, less than one month."
            ),
            "attempt_2": (
                "Use scenario=3. "
                "1,00,000 seconds = about 1.16 days. "
                "10,00,000 seconds = about 11.6 days. "
                "The progress bar for '1 day' shows > 100%, meaning counting takes longer than a day."
            ),
            "attempt_3": (
                "Select scenario=3. "
                "10 lakh ÷ (1 per second × 86,400 seconds/day) = 11.57 days. "
                "This shows that 'lakh' is a human-scale number — countable within a lifetime!"
            )
        },
        "concept_reminder": (
            "10,00,000 seconds ≈ 11.6 days at 1 per second. "
            "1 crore seconds ≈ 115 days. "
            "These anchors make lakh and crore viscerally understandable — "
            "they are large but not infinitely large."
        )
    }
]


# =============================================================================
# ROUNDING & ESTIMATION — QUIZ QUESTIONS
# 3 questions: visualise rounding → apply rounding rule → estimation in context
# =============================================================================
QUIZ_QUESTIONS_MATHS_KN["rounding_estimation_kn"] = [

    {
        "id": "rounding_estimation_kn_q1",
        "challenge": (
            "Set the simulation to Explore mode and enter 38,769,957 (3,87,69,957). "
            "Look at all five number lines. For which rounding places does the number round UP, "
            "and for which does it round DOWN?\n\n"
            "(3,87,69,957 ಅನ್ನು ತೋರಿಸಿ ಮತ್ತು ಎಲ್ಲಾ 5 ಪೂರ್ಣಾಂಕನ ಸ್ಥಾನಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ)"
        ),
        "target_parameters": ["mode", "number"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "explore"},
                {"parameter": "number", "operator": "==", "value": 38769957}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='explore' and number=38769957. "
                "Nearest 1000: 957 > 500 → round UP → 3,87,70,000. "
                "Nearest 10000: 9957 > 5000 → round UP → 3,87,70,000 (same here). "
                "Nearest 1 lakh: 69,957 > 50,000 → round UP → 3,88,00,000. "
                "Nearest 10 lakh: 7,69,957 > 5,00,000 → round UP → 3,90,00,000. "
                "Nearest crore (1,00,00,000): 87,69,957 > 50,00,000 → round UP → 4,00,00,000."
            ),
            "attempt_2": (
                "Choose mode='explore', number=38769957. "
                "The red marker on every number line is past the midpoint — so ALL five places round UP for this number."
            ),
            "attempt_3": (
                "Set mode='explore', number=38769957. "
                "All blue snap markers are at the right end of their number lines (100%), confirming all places round up."
            )
        },
        "concept_reminder": (
            "3,87,69,957 rounds UP at every place because: "
            "957 > 500, 9957 > 5000, 69957 > 50000, 769957 > 500000, 8769957 > 5000000. "
            "Rounded to nearest crore = 4,00,00,000 (four crore)."
        )
    },

    {
        "id": "rounding_estimation_kn_q2",
        "challenge": (
            "Switch to Quiz mode. Answer the question: "
            "'What is the nearest crore of 29,05,32,481?' "
            "(Is it 29,00,00,000 or 30,00,00,000?)\n\n"
            "(ರಸಪ್ರಶ್ನೆ ಮೋಡ್: 29,05,32,481 ನ ಹತ್ತಿರದ ಕೋಟಿ ಯಾವುದು?)"
        ),
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "quiz"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='quiz'. "
                "29,05,32,481 rounded to nearest crore: look at the ten-lakh digit = 0. "
                "0 < 5 → round DOWN → 29,00,00,000."
            ),
            "attempt_2": (
                "Use mode='quiz'. "
                "29,05,32,481 = 29 crore 5,32,481. "
                "The sub-crore part is 5,32,481 which is less than 50,00,000 (half a crore) → round down. "
                "Nearest crore = 29,00,00,000."
            ),
            "attempt_3": (
                "Select mode='quiz'. "
                "Rule: look at the crore-remainder = 5,32,481. "
                "5,32,481 < 50,00,000 → stay at 29 crore. Answer: 29,00,00,000."
            )
        },
        "concept_reminder": (
            "29,05,32,481 → nearest crore: check if the sub-crore part (5,32,481) ≥ 50,00,000. "
            "5,32,481 < 50,00,000 → round DOWN → 29,00,00,000. "
            "Always compare the remainder to half the rounding unit."
        )
    },

    {
        "id": "rounding_estimation_kn_q3",
        "challenge": (
            "Set explore mode and enter 4631280 (46,31,280) — Bengaluru's 2001 census population. "
            "Observe it rounded to the nearest lakh. Now mentally check: "
            "Bengaluru's 2011 population was 84,43,675. Rounded to the nearest lakh, "
            "did the city roughly double?\n\n"
            "(ಬೆಂಗಳೂರು ಜನಸಂಖ್ಯೆ 2001: 46,31,280 — ಹತ್ತಿರದ ಲಕ್ಷಕ್ಕೆ ಪೂರ್ಣಾಂಕ ಮಾಡಿ)"
        ),
        "target_parameters": ["mode", "number"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "explore"},
                {"parameter": "number", "operator": "==", "value": 4631280}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='explore', number=4631280 (46,31,280). "
                "Nearest lakh: 31,280 < 50,000 → round DOWN → 46,00,000 (46 lakh). "
                "2011 population 84,43,675 → nearest lakh: 43,675 < 50,000 → 84,00,000 (84 lakh). "
                "84 ÷ 46 ≈ 1.83 — almost doubled!"
            ),
            "attempt_2": (
                "Use mode='explore', number=4631280. "
                "46,31,280 rounds to 46 lakh (down, because 31,280 < 50,000). "
                "84,43,675 rounds to 84 lakh (down, because 43,675 < 50,000). "
                "46 × 2 = 92 lakh; actual is 84 lakh — so not quite doubled but very close."
            ),
            "attempt_3": (
                "Set mode='explore', number=4631280 → 46 lakh. "
                "84 lakh ÷ 46 lakh ≈ 1.83. Bengaluru grew by 83% — close to doubling. "
                "Rounding to the nearest lakh is enough precision to answer 'roughly doubled'."
            )
        },
        "concept_reminder": (
            "46,31,280 → nearest lakh = 46,00,000 (31,280 < 50,000 → round down). "
            "84,43,675 → nearest lakh = 84,00,000 (43,675 < 50,000 → round down). "
            "Estimation answer: 84 ÷ 46 ≈ 1.83 — city nearly doubled in one decade."
        )
    }
]


# =============================================================================
# MULTIPLICATION PATTERNS — QUIZ QUESTIONS
# 3 questions: digit-count rule → shortcuts → digit grid
# =============================================================================
QUIZ_QUESTIONS_MATHS_KN["multiplication_patterns_kn"] = [

    {
        "id": "multiplication_patterns_kn_q1",
        "challenge": (
            "Set the simulation to Multiply mode with numA=999 and numB=999. "
            "Before looking at the product, predict: will the result have 5 or 6 digits? "
            "(Use the digit-count rule: 3-digit × 3-digit gives 3+3−1=5 or 3+3=6 digits.) "
            "Then verify by checking the product displayed.\n\n"
            "(ಗುಣಾಕಾರ ಮೋಡ್: 999 × 999 — ಉತ್ಪನ್ನದಲ್ಲಿ ಎಷ್ಟು ಅಂಕಿ?)"
        ),
        "target_parameters": ["mode", "numA", "numB"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "multiply"},
                {"parameter": "numA", "operator": "==", "value": 999},
                {"parameter": "numB", "operator": "==", "value": 999}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='multiply', numA=999, numB=999. "
                "999 × 999 = 998,001 → 6 digits. "
                "Digit-count rule: 3+3=6 (the maximum). "
                "When both numbers have 9 as the leading digit, the product hits the maximum digit count."
            ),
            "attempt_2": (
                "Use mode='multiply', numA=999, numB=999. "
                "Rule: d_a=3, d_b=3 → product has 3+3−1=5 or 3+3=6 digits. "
                "999×999=998,001 is a 6-digit number (maximum). "
                "Compare: 100×100=10,000 (5 digits, minimum). The badge confirms which applies."
            ),
            "attempt_3": (
                "Set mode='multiply', numA=999, numB=999. "
                "The PASS badge shows '3+3−1 ≤ digits(product) ≤ 3+3', i.e., 5 ≤ 6 ≤ 6. "
                "998,001 has exactly 6 digits — the maximum allowed by the rule."
            )
        },
        "concept_reminder": (
            "d_a-digit × d_b-digit → product has d_a+d_b−1 or d_a+d_b digits. "
            "999 (3-digit) × 999 (3-digit) → 5 or 6 digits. Answer: 998,001 has 6 digits. "
            "Minimum case: 100×100=10,000 (5 digits, the minimum). Maximum case: 999×999=998,001 (6 digits)."
        )
    },

    {
        "id": "multiplication_patterns_kn_q2",
        "challenge": (
            "Switch to Shortcuts mode. Study the rule for multiplying by 10 and 100. "
            "Then answer: what is 4,367 × 1,000? "
            "Explain why the answer has three extra zeros compared to 4,367.\n\n"
            "(ಶಾರ್ಟ್‌ಕಟ್ ಮೋಡ್: 4,367 × 1,000 = ? — ಮೂರು ಸೊನ್ನೆ ಸೇರಿಸಲು ಕಾರಣ ಏನು?)"
        ),
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "shortcuts"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='shortcuts'. "
                "Rule: multiplying by 10 appends one zero (each digit shifts one place left). "
                "×100 appends two zeros, ×1000 appends three zeros. "
                "4,367 × 1,000 = 43,67,000 (append three zeros → seven digits)."
            ),
            "attempt_2": (
                "Use mode='shortcuts'. "
                "Place-value explanation: 4,367 × 1,000 shifts every digit three places left: "
                "ones become thousands, tens become ten-thousands, etc. "
                "The three vacated places become zeros."
            ),
            "attempt_3": (
                "Select mode='shortcuts'. "
                "4,367 × 1,000 = 4,367,000 = 43,67,000 (Indian notation). "
                "The rule: count the zeros in the multiplier → append that many zeros to the other number."
            )
        },
        "concept_reminder": (
            "Multiplying by 10^n appends n zeros. "
            "4,367 × 1,000 = 43,67,000 (three extra zeros). "
            "This is a direct consequence of place value: each ×10 shifts all digits one position left."
        )
    },

    {
        "id": "multiplication_patterns_kn_q3",
        "challenge": (
            "Open the Digit Grid (digitGrid mode). Find the cell for 4-digit × 4-digit. "
            "What is the range of digit counts possible for such a product? "
            "Verify by checking: 1000 × 1000 (minimum) and 9999 × 9999 (maximum).\n\n"
            "(ಅಂಕಿ ಗ್ರಿಡ್ ಮೋಡ್: 4 ಅಂಕಿ × 4 ಅಂಕಿ ಉತ್ಪನ್ನದಲ್ಲಿ ಎಷ್ಟು ಅಂಕಿ ಇರಬಹುದು?)"
        ),
        "target_parameters": ["mode"],
        "success_rule": {
            "conditions": [
                {"parameter": "mode", "operator": "==", "value": "digitGrid"}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set mode='digitGrid'. "
                "Cell (4d, 4d): range = 4+4−1 to 4+4 = 7 to 8 digits. "
                "Check: 1000×1000=1,000,000 (7 digits ✓). 9999×9999=99,980,001 (8 digits ✓)."
            ),
            "attempt_2": (
                "Use mode='digitGrid'. "
                "The 4d×4d cell shows '7-8'. "
                "Minimum: 10^3 × 10^3 = 10^6 (7 digits). Maximum: (10^4−1)^2 ≈ 10^8 (8 digits)."
            ),
            "attempt_3": (
                "Select mode='digitGrid'. "
                "4-digit × 4-digit always gives either 7 or 8 digit answer. "
                "The grid shows this pattern for all combinations from 1d×1d up to 5d×5d."
            )
        },
        "concept_reminder": (
            "4-digit × 4-digit product has 7 or 8 digits (4+4−1=7 to 4+4=8). "
            "1,000 × 1,000 = 10,00,000 (7 digits, minimum). "
            "9,999 × 9,999 = 9,99,80,001 (8 digits, maximum). "
            "The digit-count rule holds for ALL integer multiplication."
        )
    }
]


# =============================================================================
# EXPRESSION EVALUATOR — QUIZ QUESTIONS
# 3 questions: identify terms → evaluate BODMAS → sum signed terms
# =============================================================================
QUIZ_QUESTIONS_MATHS_KN["expression_evaluator_kn"] = [

    {
        "id": "expression_evaluator_kn_q1",
        "challenge": (
            "Load expression index 1: '39 − 2×6 + 11'. "
            "Before stepping through, count the number of terms. "
            "Hint: terms are separated by + or −. How many terms does this expression have?\n\n"
            "(ಸಮೀಕರಣ index 1 ತೋರಿಸಿ: 39 − 2×6 + 11 ರಲ್ಲಿ ಎಷ್ಟು ಪದಗಳಿವೆ?)"
        ),
        "target_parameters": ["problem"],
        "success_rule": {
            "conditions": [
                {"parameter": "problem", "operator": "==", "value": 1}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set problem=1 to load '39 − 2×6 + 11'. "
                "Terms separated by + or −: term 1 = 39, term 2 = −2×6, term 3 = 11. "
                "Three terms, not five (the × is NOT a term separator — it stays within term 2)."
            ),
            "attempt_2": (
                "Use problem=1. "
                "The three colour-coded boxes show: '39', '−2×6', '11'. "
                "Common mistake: thinking 2 and 6 are separate terms because of ×. "
                "Only + and − between terms separate them."
            ),
            "attempt_3": (
                "Select problem=1. "
                "'39 − 2×6 + 11': the separators are '−' (before 2×6) and '+' (before 11). "
                "So 3 terms: 39, −2×6, +11. Each gets its own coloured term box."
            )
        },
        "concept_reminder": (
            "'39 − 2×6 + 11' has 3 terms: 39, −2×6, and 11. "
            "The × inside '2×6' does NOT create a new term — it is an operation within term 2. "
            "Terms are separated ONLY by + or − between separate parts of the expression."
        )
    },

    {
        "id": "expression_evaluator_kn_q2",
        "challenge": (
            "Load expression index 3: '48 − 10×2 + 16÷2'. "
            "Step through the evaluation cards and compute the final value. "
            "The three terms are: 48, −10×2, and 16÷2. Evaluate each term first, then add.\n\n"
            "(index 3 ತೋರಿಸಿ: 48 − 10×2 + 16÷2 ಮೌಲ್ಯಮಾಪನ ಮಾಡಿ)"
        ),
        "target_parameters": ["problem"],
        "success_rule": {
            "conditions": [
                {"parameter": "problem", "operator": "==", "value": 3}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set problem=3 for '48 − 10×2 + 16÷2'. "
                "Term 1 = 48. Term 2 = −10×2 = −20. Term 3 = 16÷2 = 8. "
                "Sum: 48 + (−20) + 8 = 36."
            ),
            "attempt_2": (
                "Use problem=3. "
                "Step 2: evaluate each term: 48→48, −10×2→−20, 16÷2→8. "
                "Step 3: add all: 48 − 20 + 8 = 36. Final value = 36."
            ),
            "attempt_3": (
                "Select problem=3. "
                "Do NOT compute 48−10 first! Evaluate 10×2=20 inside term 2 before subtracting. "
                "Then: 48 − 20 + 8 = 36."
            )
        },
        "concept_reminder": (
            "'48 − 10×2 + 16÷2': evaluate each term independently first. "
            "Term 2: 10×2=20 → the term is −20. Term 3: 16÷2=8. "
            "Final: 48 − 20 + 8 = 36. BODMAS within each term, then addition of all terms."
        )
    },

    {
        "id": "expression_evaluator_kn_q3",
        "challenge": (
            "Load expression index 4: '6×3 − 4×8×5'. "
            "This expression has a large negative term. Evaluate it step by step: "
            "what is the value of each term, and what is the final sum?\n\n"
            "(index 4: 6×3 − 4×8×5 — ಋಣ ಪದ ಸಹಿತ ಮೌಲ್ಯಮಾಪನ)"
        ),
        "target_parameters": ["problem"],
        "success_rule": {
            "conditions": [
                {"parameter": "problem", "operator": "==", "value": 4}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.5, "wrong": 0.2}
        },
        "hints": {
            "attempt_1": (
                "Set problem=4 for '6×3 − 4×8×5'. "
                "Term 1 = 6×3 = 18. Term 2 = −4×8×5 = −160. "
                "Sum: 18 + (−160) = −142. The result is NEGATIVE."
            ),
            "attempt_2": (
                "Use problem=4. "
                "4×8×5 = 4×40 = 160. The term is negative: −160. "
                "18 − 160 = −142. The negative term dominates completely."
            ),
            "attempt_3": (
                "Select problem=4. "
                "Step 1: two terms (6×3 and −4×8×5). "
                "Step 2: 6×3=18; 4×8×5=160 so second term = −160. "
                "Step 3: 18 + (−160) = −142."
            )
        },
        "concept_reminder": (
            "'6×3 − 4×8×5' evaluates to −142. "
            "Term 1 = 6×3 = 18 (positive). Term 2 = 4×8×5 = 160 (negative because of the '−'). "
            "Sum = 18 − 160 = −142. "
            "Expressions CAN have negative final values when a large negative term dominates."
        )
    }
]


# ─────────────────────────────────────────────────────────────────────
# brackets_signs_kn
# ─────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS_MATHS_KN["brackets_signs_kn_q1"] = {
    "simulation": "brackets_signs_kn",
    "question": (
        "ಈ ಕೆಳಗಿನ ಸಮೀಕರಣವನ್ನು ನೋಡಿ: 200 − (40 + 3). "
        "ಆವರಣ ತೆಗೆದ ನಂತರ ಚಿಹ್ನೆಗಳು ಹೇಗೆ ಬದಲಾಗುತ್ತವೆ? "
        "Simulation ನಲ್ಲಿ Problem 0 ಅನ್ನು Learn ಮೋಡ್‌ನಲ್ಲಿ ತೆರೆದು ಪ್ರತಿ ಹಂತ ಗಮನಿಸಿ."
    ),
    "target_params": {"mode": "learn", "problemIndex": 0, "showHints": "true"},
    "concept_tag": "Minus before brackets flips all signs",
    "expected_insight": (
        "200 − (40 + 3) = 200 − 40 − 3 = 157. "
        "ಮೈನಸ್ ಚಿಹ್ನೆ ಆವರಣದ ಮುಂದೆ ಇದ್ದಾಗ, ಒಳಗಿನ ಪ್ರತಿ ಚಿಹ್ನೆ ಬದಲಾಯಿಸಿ: + ಆಗುತ್ತದೆ −."
    ),
    "success_rule": "mode == 'learn' and problemIndex == 0",
    "question_kannada": (
        "200 − (40 + 3) ಎಂಬ ಸಮೀಕರಣದಲ್ಲಿ ಆವರಣ ತೆಗೆದ ನಂತರ "
        "40 ಮತ್ತು 3 ಎರಡರ ಮುಂದೆ ಯಾವ ಚಿಹ್ನೆ ಬರುತ್ತದೆ?"
    ),
}

QUIZ_QUESTIONS_MATHS_KN["brackets_signs_kn_q2"] = {
    "simulation": "brackets_signs_kn",
    "question": (
        "ಸಮೀಕರಣ 500 − (250 − 100) ಅನ್ನು ನೋಡಿ. "
        "ಇಲ್ಲಿ ಆವರಣದ ಮುಂದೆ ಮೈನಸ್ ಇದ್ದಾಗ, −100 ಆವರಣ ತೆಗೆದ ನಂತರ +100 ಆಗಬೇಕು ಏಕೆ? "
        "Simulation ನಲ್ಲಿ Problem 1 ಅನ್ನು ತೆರೆದು ಮೂರು ಹಂತಗಳ ವಿವರಣೆ ಗಮನಿಸಿ."
    ),
    "target_params": {"mode": "learn", "problemIndex": 1, "showHints": "true"},
    "concept_tag": "Minus before brackets flips minus-sign inside to plus",
    "expected_insight": (
        "500 − (250 − 100) = 500 − 250 + 100 = 350. "
        "ಮೈನಸ್ ಚಿಹ್ನೆ ಒಳಗಿನ −100 ಅನ್ನು +100 ಮಾಡುತ್ತದೆ. "
        "ಕಾರಣ: ನಾವು 'ಒಂದು ವ್ಯತ್ಯಾಸ'ವನ್ನು ಕಳೆಯುತ್ತೇವೆ, ಆಗ ಹೆಚ್ಚು ಕಳೆದದ್ದನ್ನು ಮರಳಿ ಕೂಡಿಸಬೇಕು."
    ),
    "success_rule": "mode == 'learn' and problemIndex == 1",
    "question_kannada": (
        "500 − (250 − 100) ರಲ್ಲಿ, ಆವರಣ ತೆಗೆದ ನಂತರ −100, +100 ಆಗುವುದು ಏಕೆ ಎಂದು ವಿವರಿಸಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["brackets_signs_kn_q3"] = {
    "simulation": "brackets_signs_kn",
    "question": (
        "Quiz ಮೋಡ್‌ಗೆ ಹೋಗಿ. ಸಿಮ್ಯುಲೇಷನ್ ನೀಡುವ ಮೊದಲ ಪ್ರಶ್ನೆಯಲ್ಲಿ ಆವರಣ ಸರಿಯಾಗಿ ಬಿಡಿ ಮಾಡಿದ "
        "ಉತ್ತರ ಆಯ್ಕೆ ಮಾಡಿ. ಮೈನಸ್ ಚಿಹ್ನೆ ಇದ್ದರೆ ಅಥವಾ ಪ್ಲಸ್ ಚಿಹ್ನೆ ಇದ್ದರೆ ಎರಡೂ ನಿಯಮ ನೆನಪಿಸಿಕೊಳ್ಳಿ."
    ),
    "target_params": {"mode": "quiz", "quizIndex": 0, "showHints": "true"},
    "concept_tag": "Apply both sign rules in quiz context",
    "expected_insight": (
        "ಸಿಮ್ಯುಲೇಷನ್‌ನ Quiz ನಲ್ಲಿ: ಪ್ರತಿ ಆಯ್ಕೆ ನೋಡಿ ಯಾವ ಚಿಹ್ನೆ ಸರಿಯಾಗಿ ಬದಲಾಗಿದೆ / ಉಳಿದಿದೆ ಎಂದು ಪರಿಶೀಲಿಸಿ. "
        "ಮೈನಸ್ → ಎಲ್ಲ ಚಿಹ್ನೆ ಬದಲು; ಪ್ಲಸ್ → ಎಲ್ಲ ಚಿಹ್ನೆ ಹಾಗೆಯೇ."
    ),
    "success_rule": "mode == 'quiz' and quizIndex == 0",
    "question_kannada": (
        "Quiz ಮೋಡ್‌ನಲ್ಲಿ, ಆವರಣ ತೆಗೆದ ನಂತರ ಸರಿಯಾದ ರೂಪ ಯಾವುದು ಎಂದು ಆಯ್ಕೆ ಮಾಡಿ."
    ),
}

# ─────────────────────────────────────────────────────────────────────
# distributive_kn
# ─────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS_MATHS_KN["distributive_kn_q1"] = {
    "simulation": "distributive_kn",
    "question": (
        "Simulation ನಲ್ಲಿ Dot Array ಮೋಡ್ ತೆರೆಯಿರಿ, a=2, b=3, c=5 ಇಟ್ಟು ನೋಡಿ. "
        "ನೀಲಿ ಮತ್ತು ಹಸಿರು ಚುಕ್ಕೆಗಳ ಸಂಖ್ಯೆ ಎಣಿಸಿ. "
        "2 × (3+5) = 2×3 + 2×5 ಎಂಬ ಸಂಬಂಧ ನಿಜ ಎಂದು ತೋರಿಸಿ."
    ),
    "target_params": {"mode": "dots", "a": 2, "b": 3, "c": 5, "showHints": "true"},
    "concept_tag": "Distributive property visual dot array",
    "expected_insight": (
        "2 × (3+5) = 2 × 8 = 16. "
        "ನೀಲಿ: 2×3 = 6 ಚುಕ್ಕೆಗಳು; ಹಸಿರು: 2×5 = 10 ಚುಕ್ಕೆಗಳು; ಒಟ್ಟು 6+10 = 16. "
        "ಎರಡೂ ಕಡೆ ಒಂದೇ ಉತ್ತರ — ವಿಭಾಜಕ ಗುಣ ದೃಶ್ಯವಾಗಿ ನಿಜ."
    ),
    "success_rule": "mode == 'dots' and a == 2 and b == 3 and c == 5",
    "question_kannada": (
        "2 × (3 + 5) = 2×3 + 2×5 ಎಂದು Dot Array ಮಾದರಿ ಉಪಯೋಗಿಸಿ ತೋರಿಸಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["distributive_kn_q2"] = {
    "simulation": "distributive_kn",
    "question": (
        "Area Model ಮೋಡ್ ತೆರೆಯಿರಿ, a=4, b=3, c=5 ಇಟ್ಟು ನೋಡಿ. "
        "ನೀಲಿ ಆಯತ ಮತ್ತು ಹಸಿರು ಆಯತದ ವಿಸ್ತೀರ್ಣ ಲೆಕ್ಕ ಹಾಕಿ. "
        "ಒಟ್ಟು ಆಯತದ ವಿಸ್ತೀರ್ಣ 4×(3+5) = 4×8 = 32 ಎಂದು ಖಚಿತಪಡಿಸಿ."
    ),
    "target_params": {"mode": "area", "a": 4, "b": 3, "c": 5, "showHints": "true"},
    "concept_tag": "Distributive property area model visual proof",
    "expected_insight": (
        "ನೀಲಿ ಭಾಗ: 4×3 = 12 ಚೌಕ ಘಟಕಗಳು (ಶ್ರೇಣಿಗಳ ಮೂಲಕ ಎಣಿಸಬಹುದು). "
        "ಹಸಿರು ಭಾಗ: 4×5 = 20 ಚೌಕ ಘಟಕಗಳು. ಒಟ್ಟು = 32 = 4×8. "
        "ಒಂದೇ ಆಯತ ಎರಡು ಭಾಗಗಳಾಗಿ ವಿಭಜಿಸಿದರೂ ಒಟ್ಟು ವಿಸ್ತೀರ್ಣ ಬದಲಾಗುವುದಿಲ್ಲ."
    ),
    "success_rule": "mode == 'area' and a == 4 and b == 3 and c == 5",
    "question_kannada": (
        "Area Model ಉಪಯೋಗಿಸಿ 4×(3+5) = 4×3 + 4×5 ಎಂದು ದೃಶ್ಯಪ್ರಮಾಣ ನೀಡಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["distributive_kn_q3"] = {
    "simulation": "distributive_kn",
    "question": (
        "Mental Math ಮೋಡ್ ತೆರೆಯಿರಿ, Example 0 (97 × 25) ನೋಡಿ. "
        "97 ಅನ್ನು (100 − 3) ಎಂದು ಬದಲಾಯಿಸಿ, ನಂತರ ವಿಭಾಜಕ ಗುಣ ಉಪಯೋಗಿಸಿ "
        "97×25 ಎಷ್ಟು ಎಂದು ಮಾನಸಿಕ ಲೆಕ್ಕ ಹಾಕಿ."
    ),
    "target_params": {"mode": "mental", "mentalMathIndex": 0, "showHints": "true"},
    "concept_tag": "Mental math via distributive property decomposition",
    "expected_insight": (
        "97 × 25 = (100 − 3) × 25 = 100×25 − 3×25 = 2500 − 75 = 2425. "
        "ಕಷ್ಟದ ಗುಣಾಕಾರ ಸುಲಭ ಗೋಲ ಸಂಖ್ಯೆ ± ಸಣ್ಣ ತಿದ್ದುಪಡಿ ಮೂಲಕ ಬಗೆಹರಿಸಲಾಗುತ್ತದೆ."
    ),
    "success_rule": "mode == 'mental' and mentalMathIndex == 0",
    "question_kannada": (
        "97 × 25 ಅನ್ನು (100 − 3) × 25 ಎಂದು ಬಿಡಿ ಮಾಡಿ ಮಾನಸಿಕ ಲೆಕ್ಕ ಹಾಕಿ."
    ),
}

# ─────────────────────────────────────────────────────────────────────
# expression_compare_kn
# ─────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS_MATHS_KN["expression_compare_kn_q1"] = {
    "simulation": "expression_compare_kn",
    "question": (
        "Simulation ತೆರೆಯಿರಿ. ಮೊದಲ ಪ್ರಶ್ನೆಯಿಂದ ಆರಂಭಿಸಿ. "
        "ಎರಡೂ ಸಮೀಕರಣಗಳಿಗಿಂತ ಯಾವ ಭಾಗ ಬದಲಾಗಿದೆ — ಅದನ್ನು ನೋಡಿ < / = / > ನಿರ್ಧರಿಸಿ. "
        "ಉತ್ತರ ಒತ್ತಿ ವಿವರಣೆ ಓದಿ."
    ),
    "target_params": {"questionIndex": 0, "showHints": "true"},
    "concept_tag": "Compare by spotting what changed",
    "expected_insight": (
        "1023+125 vs 1022+128: ಎಡಕ್ಕೆ −1, ಬಲಕ್ಕೆ +3 → ಬಲ ಕಡೆ 2 ಹೆಚ್ಚಾಗಿದೆ → ಎಡ < ಬಲ. "
        "ಎಲ್ಲ ಗಣನೆ ಮಾಡದೆ, ಬದಲಾದ ಭಾಗ ಮಾತ್ರ ನೋಡಿ ಉತ್ತರ ಕಂಡುಕೊಳ್ಳಬಹುದು."
    ),
    "success_rule": "questionIndex == 0",
    "question_kannada": (
        "1023+125 ಮತ್ತು 1022+128 ಹೋಲಿಸಿ. ಎರಡೂ ಲೆಕ್ಕ ಮಾಡದೆ ಉತ್ತರ ಹೇಳಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["expression_compare_kn_q2"] = {
    "simulation": "expression_compare_kn",
    "question": (
        "Simulation ನಲ್ಲಿ questionIndex=9 ಇಟ್ಟು ತೆರೆಯಿರಿ. "
        "(34−28)×42 ಮತ್ತು 34×42 − 28×42 ಹೋಲಿಸಿ. "
        "ವಿಭಾಜಕ ಗುಣ ನೆನಪು ಮಾಡಿಕೊಂಡು ಉತ್ತರ ಆಯ್ಕೆ ಮಾಡಿ."
    ),
    "target_params": {"questionIndex": 9, "showHints": "true"},
    "concept_tag": "Distributive property reveals equality",
    "expected_insight": (
        "(34−28)×42 = 6×42 = 252. 34×42 − 28×42 = 42×(34−28) = 42×6 = 252. "
        "ವಿಭಾಜಕ ಗುಣದಿಂದ ಎರಡೂ ಒಂದೇ. =."
    ),
    "success_rule": "questionIndex == 9",
    "question_kannada": (
        "(34−28)×42 ಮತ್ತು 34×42 − 28×42 ಇವುಗಳ ಸಂಬಂಧ ಹೇಳಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["expression_compare_kn_q3"] = {
    "simulation": "expression_compare_kn",
    "question": (
        "questionIndex=7 ಇಟ್ಟು Simulation ತೆರೆಯಿರಿ. "
        "15+9×18 ಮತ್ತು (15+9)×18 ಹೋಲಿಸಿ. "
        "BODMAS ನಿಯಮ ಉಪಯೋಗಿಸಿ ಯಾವ ಕಡೆ ಮೌಲ್ಯ ಹೆಚ್ಚು ಎಂದು ನಿರ್ಧರಿಸಿ."
    ),
    "target_params": {"questionIndex": 7, "showHints": "true"},
    "concept_tag": "BODMAS: brackets change computation order",
    "expected_insight": (
        "ಆವರಣ ಇಲ್ಲದೆ: 15 + 9×18 = 15 + 162 = 177. "
        "ಆವರಣ ಇದ್ದರೆ: (15+9)×18 = 24×18 = 432. "
        "ಬಲ ಕಡೆ ಎರಡಕ್ಕಿಂತ ಹೆಚ್ಚು. ಆವರಣ ಇರಿಸಿದ ಸ್ಥಳ ಮೌಲ್ಯ ಮೇಲೆ ಬಹು ಪ್ರಭಾವ ಬೀರುತ್ತದೆ."
    ),
    "success_rule": "questionIndex == 7",
    "question_kannada": (
        "15+9×18 ಮತ್ತು (15+9)×18 ಹೋಲಿಸಿ. BODMAS ಉಪಯೋಗಿಸಿ."
    ),
}

# ─────────────────────────────────────────────────────────────────────
# expression_engineer_kn
# ─────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS_MATHS_KN["expression_engineer_kn_q1"] = {
    "simulation": "expression_engineer_kn",
    "question": (
        "ಮೂರು 3ಗಳ (three3s) challenge ತೆರೆಯಿರಿ. "
        "ಗುರಿ ಸಂಖ್ಯೆ 0 ಮಾಡಲು 3, 3, 3 ಮತ್ತು +, −, ×, ÷, () ಬಳಕೆ ಮಾಡಿ ಒಂದು ಸಮೀಕರಣ ಬರೆಯಿರಿ. "
        "ನಂತರ ಗುರಿ 6 ಮತ್ತು 12 ಕೂಡ ಮಾಡಲು ಪ್ರಯತ್ನಿಸಿ."
    ),
    "target_params": {"challenge": "three3s", "showHints": "true"},
    "concept_tag": "Same digits different operators different results",
    "expected_insight": (
        "0 = (3−3)×3 ಅಥವಾ 3−3−0×3 ಸಾಧ್ಯ. "
        "6 = 3×3−3. 12 = 3×3+3. "
        "ಒಂದೇ ಮೂರು 3ಗಳಿಂದ ವಿವಿಧ ಮೌಲ್ಯಗಳಿಗೆ ತಲುಪಬಹುದು — ಕಾರ್ಯಾಚರಣೆ ಬದಲಾದಾಗ ಫಲಿತಾಂಶ ಬದಲಾಗುತ್ತದೆ."
    ),
    "success_rule": "challenge == 'three3s'",
    "question_kannada": (
        "ಮೂರು 3ಗಳಿಂದ 0, 6, 12 ಮಾಡಬಲ್ಲ ಸಮೀಕರಣ ಬರೆಯಿರಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["expression_engineer_kn_q2"] = {
    "simulation": "expression_engineer_kn",
    "question": (
        "ನಾಲ್ಕು 4ಗಳ (four4s) challenge ತೆರೆಯಿರಿ. "
        "ಗುರಿ 1 ಮಾಡಲು ನಾಲ್ಕು 4ಗಳಿಂದ ಸಮೀಕರಣ ಬರೆಯಿರಿ. "
        "ನಂತರ ಗುರಿ 4 ಮತ್ತು 8 ಕೂಡ ಸಾಧಿಸಿ."
    ),
    "target_params": {"challenge": "four4s", "showHints": "true"},
    "concept_tag": "Brackets change expression value dramatically",
    "expected_insight": (
        "1 = (4+4)÷(4+4) ಅಥವಾ 44÷44. "
        "4 = 4×(4−4)+4 ಅಥವಾ 4+4×(4−4). "
        "8 = 4+4+4−4. "
        "ಆವರಣ ಇರಿಸುವ ಸ್ಥಳ ಬದಲಾಯಿಸಿದಾಗ ಫಲಿತಾಂಶ ಬಹಳ ಬದಲಾಗುತ್ತದೆ."
    ),
    "success_rule": "challenge == 'four4s'",
    "question_kannada": (
        "ನಾಲ್ಕು 4ಗಳಿಂದ 1, 4, 8 ಮಾಡಬಲ್ಲ ಸಮೀಕರಣ ಬರೆಯಿರಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["expression_engineer_kn_q3"] = {
    "simulation": "expression_engineer_kn",
    "question": (
        "₹432 ಪಾವತಿ (pay432) challenge ತೆರೆಯಿರಿ. "
        "₹100, ₹50, ₹20, ₹10, ₹5 ಮತ್ತು ₹1 ನೋಟುಗಳ ಸಂಖ್ಯೆ ಆಯ್ಕೆ ಮಾಡಿ "
        "ಮೊತ್ತ ₹432 ಬರುವಂತೆ ಮಾಡಿ."
    ),
    "target_params": {"challenge": "pay432", "showHints": "true"},
    "concept_tag": "Currency amount as sum of products",
    "expected_insight": (
        "ಒಂದು ಉತ್ತರ: 4×100 + 1×20 + 1×10 + 2×1 = 400 + 20 + 10 + 2 = 432. "
        "ಇದು ವಿಭಾಜಕ ಗುಣದ ನೈಜ ಜೀವನ ಅನ್ವಯ — "
        "ಮೊತ್ತ = Σ (ಎಣಿಕೆ × ಮೌಲ್ಯ)."
    ),
    "success_rule": "challenge == 'pay432'",
    "question_kannada": (
        "₹432 ಅನ್ನು ನೋಟು/ನಾಣ್ಯ ಸಂಯೋಜನೆ ಮೂಲಕ ಮಾಡಿ."
    ),
}

# ─────────────────────────────────────────────────────────────────────
# decimal_number_line_kn
# ─────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS_MATHS_KN["decimal_number_line_kn_q1"] = {
    "simulation": "decimal_number_line_kn",
    "question": (
        "Explore ಮೋಡ್ ತೆರೆಯಿರಿ, num=4.185 ಇಟ್ಟು ನೋಡಿ. "
        "Zoom 1, Zoom 2, Zoom 3 ಮೂರೂ ಸಂಖ್ಯಾರೇಖೆ ನೋಡಿ ಈ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರ ಹೇಳಿ: "
        "4.185 ಇರುವ ಸ್ಥಾನ Zoom 1 ರಲ್ಲಿ, Zoom 2 ರಲ್ಲಿ, Zoom 3 ರಲ್ಲಿ ಯಾವ ಎರಡು ಮೌಲ್ಯಗಳ ನಡುವೆ ಇದೆ?"
    ),
    "target_params": {"mode": "explore", "num": 4.185, "showHints": "true"},
    "concept_tag": "Each decimal place 10x more precise zoom reveals position",
    "expected_insight": (
        "Zoom 1: 4 ಮತ್ತು 5 ನಡುವೆ. "
        "Zoom 2: 4.1 ಮತ್ತು 4.2 ನಡುವೆ. "
        "Zoom 3: 4.18 ಮತ್ತು 4.19 ನಡುವೆ. "
        "ಪ್ರತಿ ಝೂಮ್ ಮಟ್ಟ 10× ಹೆಚ್ಚು ನಿಖರ."
    ),
    "success_rule": "mode == 'explore' and abs(num - 4.185) < 0.001",
    "question_kannada": (
        "4.185 ಅನ್ನು ಮೂರು ಝೂಮ್ ಮಟ್ಟಗಳಲ್ಲಿ ಗುರುತಿಸಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["decimal_number_line_kn_q2"] = {
    "simulation": "decimal_number_line_kn",
    "question": (
        "Sequence ಮೋಡ್ ತೆರೆಯಿರಿ, seqIndex=1 ಇಟ್ಟು ನೋಡಿ. "
        "4.4, 4.45, 4.5 ಅನುಕ್ರಮ ನೋಡಿ: ಅಡ್ಡಹೆಜ್ಜೆ (step) ಎಷ್ಟು? "
        "ಮುಂದಿನ ಮೂರು ಮೌಲ್ಯಗಳು ಎಷ್ಟು ಎಂದು ಊಹಿಸಿ, ನಂತರ ಖಚಿತಪಡಿಸಿ."
    ),
    "target_params": {"mode": "sequence", "seqIndex": 1, "showHints": "true"},
    "concept_tag": "Decimal arithmetic sequences hundredths step",
    "expected_insight": (
        "Step = 4.45 − 4.4 = 0.05. "
        "ಮುಂದಿನ ಮೌಲ್ಯಗಳು: 4.55, 4.60, 4.65. "
        "ಪ್ರತಿ ಹಂತ 5 ಶತಮಾನ (hundredths) ಹೆಚ್ಚಾಗುತ್ತದೆ."
    ),
    "success_rule": "mode == 'sequence' and seqIndex == 1",
    "question_kannada": (
        "4.4, 4.45, 4.5 ಅನುಕ್ರಮದ step ಮತ್ತು ಮುಂದಿನ 3 ಮೌಲ್ಯ ಹೇಳಿ."
    ),
}

QUIZ_QUESTIONS_MATHS_KN["decimal_number_line_kn_q3"] = {
    "simulation": "decimal_number_line_kn",
    "question": (
        "Quiz ಮೋಡ್ ತೆರೆಯಿರಿ, quizIndex=3 ಇಟ್ಟು ತೆರೆಯಿರಿ. "
        "0.2 ಮತ್ತು 0.20 ಒಂದೇ ಎ? 0.2 ಮತ್ತು 0.02 ಒಂದೇ ಎ? "
        "ಎರಡೂ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರ ಕೊಡಿ ಮತ್ತು ಕಾರಣ ವಿವರಿಸಿ."
    ),
    "target_params": {"mode": "quiz", "quizIndex": 3, "showHints": "true"},
    "concept_tag": "Trailing zeros vs position zeros in decimals",
    "expected_insight": (
        "0.2 = 0.20: ಹೌದು, ಒಂದೇ. ಕೊನೆ ಶೂನ್ಯ ಮೌಲ್ಯ ಬದಲಿಸುವುದಿಲ್ಲ (trailing zero). "
        "0.2 ≠ 0.02: ಇಲ್ಲ, ಬೇರೆ. 0.02 = 2 ಶತಮಾನ = 0.2 ÷ 10 (position zero). "
        "ಲೇಖನ ಶೂನ್ಯ (trailing) vs ಸ್ಥಾನ ಶೂನ್ಯ (position) ವ್ಯತ್ಯಾಸ ತಿಳಿಯಿರಿ."
    ),
    "success_rule": "mode == 'quiz' and quizIndex == 3",
    "question_kannada": (
        "0.2 ಮತ್ತು 0.20 ಒಂದೇ ಏಕೆ? 0.2 ಮತ್ತು 0.02 ಬೇರೆ ಏಕೆ ?"
    ),
}


# ═══════════════════════════════════════════════════════════════════════
# HELPER: list of Kannada-Maths simulation IDs for sidebar grouping
# ═══════════════════════════════════════════════════════════════════════

MATHS_KN_SIMULATION_IDS = list(SIMULATIONS_MATHS_KN.keys())
