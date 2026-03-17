"""
Understanding Evaluator Node
============================
Analyzes student responses to determine their understanding level.

This node uses the LLM to:
1. FIRST: Classify the response type (answer, question, param_request)
2. THEN: If answer, evaluate understanding level
3. Extract relevant info (questions asked, params requested)

The evaluation is nuanced - it's not just right/wrong, but a spectrum.
"""

import json
import re
from typing import Dict, Any
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from simulation_to_concept.config import (
    GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, INITIAL_PARAMS,
    TOPIC_TITLE, TOPIC_DESCRIPTION, PARAMETER_INFO, USE_API_TRACKER,
    get_best_api_key_for_model, track_model_call
)
from api_tracker_utils.error import MinuteLimitExhaustedError, DayLimitExhaustedError
from simulation_to_concept.state import add_message_to_history


def get_llm():
    """Get configured LLM instance and the exact API key used."""
    if USE_API_TRACKER:
        try:
            # Get best API key for this model from tracker
            api_key = get_best_api_key_for_model(GEMINI_MODEL)
            print(f"[EVALUATOR] Using tracked API key ...{api_key[-6:]} for {GEMINI_MODEL}")
        except (MinuteLimitExhaustedError, DayLimitExhaustedError):
            raise  # Propagate rate-limit errors up to the API server
        except Exception as e:
            print(f"[EVALUATOR] Tracker error: {e}, falling back to GOOGLE_API_KEY")
            api_key = GOOGLE_API_KEY
    else:
        api_key = GOOGLE_API_KEY
    
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=0.3  # Lower temperature for more consistent evaluation
    )
    return llm, api_key


def parse_json_safe(text: str) -> dict:
    """Extract JSON from LLM response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    code_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    return {"response_type": "answer", "level": "partial", "reasoning": "Could not parse evaluation"}


def understanding_evaluator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify and evaluate the student's response.
    
    STEP 1: Classify response type
        - answer: Student is answering the teacher's question
        - question: Student is asking a question
        - param_request: Student wants to change simulation parameters
        
    STEP 2: Based on type, extract relevant info
        - answer → evaluate understanding level
        - question → extract the question for teacher to answer
        - param_request → extract parameter and value
    """
    print("\n" + "="*60)
    print("🔍 EVALUATOR NODE: Classifying & Assessing")
    print("="*60)
    
    student_response = state.get("student_response", "")
    
    if not student_response:
        print("   ⚠️ No student response to evaluate")
        return {
            "understanding_level": "none",
            "understanding_reasoning": "Student hasn't responded yet",
            "response_type": "answer"
        }
    
    # Get current concept
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    current_params = state.get("current_params", INITIAL_PARAMS)
    
    if current_idx >= len(concepts):
        return {
            "understanding_level": "complete",
            "understanding_reasoning": "All concepts completed",
            "response_type": "answer"
        }
    
    current_concept = concepts[current_idx]
    last_teacher_msg = state.get("last_teacher_message", "")
    session_language = state.get("language", "english")
    language_instruction = "English" if session_language.lower() == "english" else session_language.capitalize()
    
    print(f"   Student said: \"{student_response[:100]}...\"" if len(student_response) > 100 else f"   Student said: \"{student_response}\"")
    
    # Get parameter history for context - CRITICAL for evaluating correctness
    param_history = state.get("parameter_history", [])
    last_param_change = param_history[-1] if param_history else None
    
    # Build parameter change context using teacher's message (more reliable than param_history)
    # Teacher's question contains the comparison baseline
    
    # Build parameter list dynamically from PARAMETER_INFO
    param_list = "\n".join([f"- {key} = {current_params.get(key, '?')}" for key in PARAMETER_INFO.keys()])
    
    param_change_context = f"""
⚠️ CRITICAL - DETERMINING CORRECTNESS:

CURRENT SIMULATION STATE:
{param_list}

TEACHER'S LAST MESSAGE (contains the comparison context):
"{last_teacher_msg}"

HOW TO EVALUATE:
1. Look at teacher's question - it asks student to compare current state to a previous value
   Example: "faster or slower compared to when [parameter] was [value]?"
   
2. Extract the comparison baseline from teacher's question
3. Compare to CURRENT value
4. Apply the physics/scientific rules from the concept being taught
5. If student's answer contradicts the rules → is_factually_wrong = true, level = "none"
"""
    
    # Build concept-specific physics rules dynamically
    physics_rules = f"""
CONCEPT BEING TAUGHT:
Title: {current_concept['title']}
Description: {current_concept['description']}
Key Insight: {current_concept['key_insight']}

SIMULATION INFORMATION:
Topic: {TOPIC_TITLE}
{TOPIC_DESCRIPTION}

PARAMETER EFFECTS (use these to judge correctness):
"""
    for param_name, param_info in PARAMETER_INFO.items():
        physics_rules += f"\n{param_info['label']} ({param_info['range']}): {param_info['effect']}"
    
    # Build the combined classification + evaluation prompt
    eval_prompt = f"""⚠️ LANGUAGE REQUIREMENT: All free-text fields in your JSON response (understanding_reasoning, question_asked, correction_explanation) MUST be written in {language_instruction} only. Do not use any other language, even if the simulation topic contains text in another language.

You are analyzing a student's response in a science teaching session.

═══════════════════════════════════════════════════════════════
{physics_rules}
═══════════════════════════════════════════════════════════════

{param_change_context}

CURRENT SIMULATION PARAMETERS:
{param_list}

TEACHER'S LAST MESSAGE:
"{last_teacher_msg}"

STUDENT'S RESPONSE:
"{student_response}"

═══════════════════════════════════════════════════════════════
STEP 1: CLASSIFY THE RESPONSE TYPE
═══════════════════════════════════════════════════════════════

First, determine what TYPE of response this is:

1. "answer" - Student is answering/responding to the teacher's question
   Examples: "slower", "I think it takes longer", "don't know", "faster"

2. "question" - Student is ASKING a question or requesting explanation
   Examples: "What's the formula?", "Can you explain again?", "Why does that happen?", "What is time period?"

3. "param_request" - Student wants to CHANGE simulation parameters OR see the simulation
   Examples: 
   - "Change length to 3", "Set it to 5 units", "Make it shorter", "Try with 20 oscillations"
   - "Can you show the simulation?", "Show me", "Let me see it", "Display the simulation", "Show simulation as well"
   NOTE: Student may request MULTIPLE params at once
   ⚠️ IMPORTANT: If student asks to "show", "see", or "display" the simulation, treat as param_request with "show_simulation": true

═══════════════════════════════════════════════════════════════
STEP 2: BASED ON TYPE, FILL RELEVANT FIELDS
═══════════════════════════════════════════════════════════════

IF response_type == "answer":
- Evaluate understanding level (none/partial/mostly/complete)
- Check if factually wrong

IF response_type == "question":
- Extract the question being asked
- Set level to current understanding (don't change it)

IF response_type == "param_request":
- Extract which parameter (length or number_of_oscillations)
- Extract the requested value
- Validate it's in range
- Set level to current understanding (don't change it)
- **SPECIAL CASE**: If student asks to "show"/"see"/"display" simulation (without specifying values), set "show_simulation": true

═══════════════════════════════════════════════════════════════
UNDERSTANDING LEVELS (only for "answer" type):
═══════════════════════════════════════════════════════════════

- "complete": Correct answer WITH explanation of WHY
- "mostly": Correct answer but NO reasoning (observation only)
- "partial": Vague, unclear, or just acknowledgment ("okay", "sure")
- "none": "I don't know", off-topic, OR **FACTUALLY WRONG**

⚠️ CRITICAL: WRONG ANSWERS = NONE
If student states something factually incorrect (opposite of the concept), level = "none"

═══════════════════════════════════════════════════════════════
RESPOND WITH ONLY THIS JSON:
═══════════════════════════════════════════════════════════════
```json
{{
    "response_type": "answer" or "question" or "param_request",
    
    // For ALL types:
    "level": "none/partial/mostly/complete",
    "reasoning": "Brief explanation of classification and evaluation",
    
    // For "answer" type:
    "is_factually_wrong": true/false,
    "needs_deeper": true/false,
    "what_they_got_right": "what was correct, empty if wrong",
    
    // For "question" type:
    "question_asked": "The question the student is asking",
    
    // For "param_request" type (can have BOTH if student requested multiple):
    "param_requested": "length" or "number_of_oscillations" or "both" or null,
    "param_value": number or null,
    "param_valid": true/false,
    "length_value": number or null (if length was requested),
    "oscillations_value": number or null (if oscillations was requested),
    "show_simulation": true/false (true if student asked to see/show/display simulation without specific values)
}}
```
"""

    # DEBUG: Print parameter context being used
    print(f"   🔎 DEBUG - param_history length: {len(param_history)}")
    if last_param_change:
        print(f"   🔎 DEBUG - Last change: {last_param_change.get('parameter')} {last_param_change.get('old_value')} → {last_param_change.get('new_value')}")
    else:
        print(f"   🔎 DEBUG - No param_history available!")
    
    llm, used_api_key = get_llm()

    # Track BEFORE invocation for accurate quota accounting
    if USE_API_TRACKER and used_api_key:
        try:
            track_model_call(used_api_key, GEMINI_MODEL)
            print(f"[EVALUATOR] Tracked API call: ...{used_api_key[-6:]} + {GEMINI_MODEL}")
        except Exception as e:
            print(f"[EVALUATOR] Warning: Failed to track API call: {e}")

    response = llm.invoke([HumanMessage(content=eval_prompt)])
    
    result = parse_json_safe(response.content)
    
    # Extract response type (default to "answer")
    response_type = result.get("response_type", "answer")
    valid_types = ["answer", "question", "param_request"]
    if response_type not in valid_types:
        response_type = "answer"
    
    print(f"\n   📋 Response Type: {response_type.upper()}")
    
    # Handle based on response type
    level = result.get("level", "partial")
    reasoning = result.get("reasoning", "Evaluation uncertain")
    needs_deeper = result.get("needs_deeper", False)
    is_factually_wrong = result.get("is_factually_wrong", False)
    
    # Validate level
    valid_levels = ["none", "partial", "mostly", "complete"]
    if level not in valid_levels:
        level = "partial"
    
    # Initialize output
    output = {
        "response_type": response_type,
        "understanding_level": level,
        "understanding_reasoning": reasoning,
    }
    
    if response_type == "answer":
        # Normal answer evaluation
        print(f"   📊 Understanding Level: {level.upper()}")
        print(f"   📝 Reasoning: {reasoning}")
        
        if is_factually_wrong:
            print(f"   ❌ Factually Wrong: Student stated something incorrect")
        if needs_deeper:
            print(f"   🔄 Needs Deeper: Yes (correct observation, asking for WHY)")
        
        output["is_factually_wrong"] = is_factually_wrong
        output["needs_deeper"] = needs_deeper
        output["_eval_details"] = {
            "what_they_got_right": result.get("what_they_got_right", ""),
            "what_needs_work": result.get("what_needs_work", ""),
            "misconception": result.get("detected_misconception")
        }
        
        # Update trajectory for answers
        old_trajectory = state.get("understanding_trajectory", [])
        output["understanding_trajectory"] = old_trajectory + [level]
        
    elif response_type == "question":
        # Student asked a question
        question_asked = result.get("question_asked", student_response)
        print(f"   ❓ Question Asked: {question_asked}")
        
        output["student_asked_question"] = True
        output["question_asked"] = question_asked
        # Don't update trajectory for questions
        output["understanding_trajectory"] = state.get("understanding_trajectory", [])
        
    elif response_type == "param_request":
        # Student requested parameter change
        param =result.get("param_requested")
        value = result.get("param_value")
        is_valid = result.get("param_valid", False)
        show_simulation = result.get("show_simulation", False)
        
        # Handle "both" - multiple params requested
        length_val = result.get("length_value")
        osc_val = result.get("oscillations_value")
        
        if show_simulation:
            print(f"   🖥️ Student requested to SEE/SHOW simulation")
            output["student_wants_to_see_simulation"] = True
            output["student_requested_param"] = True  # Treat this as a param request
            output["requested_param"] = "show"  # Special marker
            output["requested_value"] = None
            output["param_request_valid"] = True
        elif param == "both":
            print(f"   🎛️ Multiple Parameters Requested:")
            print(f"      - length = {length_val}")
            print(f"      - oscillations = {osc_val}")
        else:
            print(f"   🎛️ Parameter Request: {param} = {value}")
            print(f"   ✓ Valid: {is_valid}")
        
        if not show_simulation:
            output["student_requested_param"] = True
            output["requested_param"] = param
            output["requested_value"] = value
            output["param_request_valid"] = is_valid
        
        # If valid, update the params (only for actual value changes, not show requests)
        if not show_simulation:
            new_params = current_params.copy()
            if param == "both":
                # Handle both parameters
                if length_val is not None:
                    new_params["length"] = length_val
                    print(f"   ✅ Updating length → {length_val}")
                if osc_val is not None:
                    new_params["number_of_oscillations"] = osc_val
                    print(f"   ✅ Updating oscillations → {osc_val}")
                if length_val is not None or osc_val is not None:
                    output["current_params"] = new_params
            elif is_valid and param and value is not None:
                new_params[param] = value
                output["current_params"] = new_params
                print(f"   ✅ Updating params: {param} → {value}")
        
        # Don't update trajectory for param requests
        output["understanding_trajectory"] = state.get("understanding_trajectory", [])
    
    # Add student message to history (for all types)
    student_message = add_message_to_history(state, "student", student_response)
    output["conversation_history"] = state.get("conversation_history", []) + [student_message]
    
    # Update parameter history if exists (for answers)
    if response_type == "answer":
        param_history = state.get("parameter_history", [])
        if param_history:
            param_history[-1]["student_reaction"] = student_response[:200]
            param_history[-1]["understanding_after"] = level
            
            before = param_history[-1].get("understanding_before", "none")
            level_order = {"none": 0, "partial": 1, "mostly": 2, "complete": 3}
            if level_order.get(level, 0) > level_order.get(before, 0):
                param_history[-1]["was_effective"] = True
        output["parameter_history"] = param_history
    
    return output
