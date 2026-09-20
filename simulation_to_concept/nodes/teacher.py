"""
Teacher Node
============
The heart of the teaching agent - generates natural, adaptive responses.

This node creates teacher responses that are:
- Natural and conversational (like a real teacher)
- Adaptive to student's understanding level
- Informed by parameter history (what worked/didn't work)
- Varied in style based on teacher_mode

The teacher can:
1. Explain concepts with analogies
2. Ask Socratic questions
3. Request predictions before parameter changes
4. Provide encouragement and feedback
5. Simplify or challenge based on mode
"""

import json
import re
from typing import Dict, Any
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from simulation_to_concept.config import (
    GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, USE_API_TRACKER,
    get_best_api_key_for_model, track_model_call
)
from api_tracker_utils.error import MinuteLimitExhaustedError, DayLimitExhaustedError
from simulation_to_concept.state import add_message_to_history
from simulation_to_concept.simulations_config import get_simulation
from api_servers.request_timing import measure, timed


def get_llm_with_key():
    """Get configured LLM instance and the selected API key.

    MinuteLimitExhaustedError / DayLimitExhaustedError propagate naturally
    to the caller — never caught here.
    """
    if USE_API_TRACKER:
        # Limit errors propagate to the caller — do NOT wrap in try/except
        api_key = get_best_api_key_for_model(GEMINI_MODEL)
        print(f"[TEACHER] Using tracked API key ...{api_key[-6:]} for {GEMINI_MODEL}")
    else:
        api_key = GOOGLE_API_KEY

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=TEMPERATURE
    )
    return llm, api_key


def is_gemma_model() -> bool:
    """Check if using a Gemma model (doesn't support system messages)."""
    return "gemma" in GEMINI_MODEL.lower()


def invoke_llm_with_prompts(llm, system_prompt: str, user_prompt: str, api_key: str = None, metadata: dict = None, parent_config: dict = None):
    """
    Invoke LLM with model-aware message handling, API tracking, and LangSmith metadata.
    
    Gemma models don't support SystemMessage, so we combine prompts.
    Gemini models support SystemMessage for better results.
    
    Args:
        parent_config: The RunnableConfig from LangGraph node. Must be passed to preserve
                       tracing callbacks so LangSmith can capture metadata.
    """
    import langsmith
    
    # Build messages based on model type
    if is_gemma_model():
        combined_prompt = f"{system_prompt}\n\n---\n\nNow respond to this:\n\n{user_prompt}"
        messages = [HumanMessage(content=combined_prompt)]
    else:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
    
    # Use langsmith.trace() to create a visible span with our custom metadata.
    # This ensures metadata (simulation_url, etc.) appears in LangSmith UI
    # as a child span under the node, with all metadata fields visible.
    trace_metadata = metadata or {}

    # Track BEFORE invoking — counts attempts, not just successes (per usage guide Section 5)
    if USE_API_TRACKER and api_key:
        track_model_call(api_key, GEMINI_MODEL)
        print(f"[TEACHER] Tracked API call: ...{api_key[-6:]} + {GEMINI_MODEL}")

    with langsmith.trace(
        name="teacher_llm_call",
        run_type="llm",
        metadata=trace_metadata,
        inputs={"system_prompt_length": len(system_prompt), "user_prompt_length": len(user_prompt)},
    ) as rt:
        # Also pass parent config to llm.invoke for callback chain continuity
        config = parent_config or {}
        response = llm.invoke(messages, config=config)
        rt.outputs = {"response_length": len(extract_text_content(response.content)) if response.content else 0}

    return response


def extract_text_content(content) -> str:
    """
    Normalise response.content to a plain string.
    Multimodal models (e.g. Gemma 4) return content as a list of parts
    such as [{'type': 'text', 'text': '...'}] or [AIMessageChunk(...)],
    while text-only models return a plain string.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                parts.append(part.get("text", ""))
            elif hasattr(part, "text"):
                parts.append(part.text)
            else:
                parts.append(str(part))
        return "".join(parts)
    return str(content)


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
    
    raise ValueError(f"Could not parse JSON from response")


def clean_teacher_message(text: str) -> str:
    """
    Strip any accidentally-leaked JSON from a teacher message string.

    The LLM is instructed to return *only* JSON, but it occasionally prepends
    the human-readable reply as plain text and appends the JSON block without
    proper code-fence markers (or with a malformed one that the regex misses).
    In that situation parse_json_safe falls back to using the entire
    response.content as teacher_message, which causes the raw JSON to be
    rendered in the UI alongside the actual message.

    This function removes any trailing JSON-like block so only the readable
    part of the message reaches the student.
    """
    if not text:
        return text

    # Remove ```json ... ``` or ``` ... ``` fenced blocks at the end
    cleaned = re.sub(r'\s*```(?:json)?\s*\{[\s\S]*?\}\s*```\s*$', '', text).strip()
    if cleaned != text:
        return cleaned

    # Remove a bare JSON object that contains known structural keys
    cleaned = re.sub(
        r'\s*\{[\s\S]*?"teacher_message"[\s\S]*?\}\s*$',
        '',
        text
    ).strip()
    if cleaned != text:
        return cleaned

    # Catch any trailing { ... } block that looks like JSON output
    cleaned = re.sub(
        r'\s*\{[\s\S]*?"suggests_param_change"[\s\S]*?\}\s*$',
        '',
        text
    ).strip()
    return cleaned if cleaned else text


def format_parameter_history(history: list) -> str:
    """Format parameter history for the prompt."""
    if not history:
        return "No parameter changes yet."
    
    formatted = []
    for i, change in enumerate(history, 1):
        effectiveness = "✓ Helped" if change.get("was_effective") else "✗ Didn't help"
        formatted.append(
            f"{i}. Changed {change['parameter']}: {change['old_value']} → {change['new_value']}\n"
            f"   Reason: {change['reason']}\n"
            f"   Student reaction: {change.get('student_reaction', 'N/A')}\n"
            f"   Result: {effectiveness}"
        )
    return "\n".join(formatted)


def format_conversation_history(history: list, last_n: int = 6) -> str:
    """Format recent conversation for context."""
    if not history:
        return "No conversation yet - this is the start."
    
    recent = history[-last_n:] if len(history) > last_n else history
    formatted = []
    for msg in recent:
        role = "🎓 Teacher" if msg["role"] == "teacher" else "👩‍🎓 Student"
        formatted.append(f"{role}: {msg['content']}")
    return "\n".join(formatted)


@timed("simulation_teacher_node")
def teacher_node(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """
    Generate a natural, adaptive teacher response.
    
    Input State:
        - concepts: List of concepts to teach
        - current_concept_index: Which concept we're on
        - conversation_history: Past messages
        - understanding_level: Current student understanding
        - parameter_history: What param changes we've tried
        - current_params: Current simulation state
        - strategy: What teaching strategy to use
        - teacher_mode: encouraging/challenging/simplifying
        - exchange_count: How many exchanges for this concept
    
    Args:
        config: RunnableConfig from LangGraph with tracing callbacks for LangSmith.
        
    Output State:
        - last_teacher_message: The generated response
        - conversation_history: Updated with new message
        - current_params: Potentially updated
        - parameter_history: Updated if param change suggested
        - waiting_for_input: True (pauses for student)
    """
    print("\n" + "="*60)
    print("🎓 TEACHER NODE: Generating response")
    print("="*60)
    
    # Load simulation config dynamically from state (NOT from cached module imports!)
    simulation_id = state.get("simulation_id", "simple_pendulum")
    sim_config = get_simulation(simulation_id)
    if not sim_config:
        raise ValueError(f"Unknown simulation: {simulation_id}")
    
    TOPIC_TITLE = sim_config["title"]
    TOPIC_DESCRIPTION = sim_config["description"]
    CANNOT_DEMONSTRATE = sim_config["cannot_demonstrate"]
    PARAMETER_INFO = sim_config["parameter_info"]
    
    print(f"   🎮 Loaded config for: {TOPIC_TITLE} ({simulation_id})")
    
    # Get current concept
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    
    if current_idx >= len(concepts):
        # All concepts complete
        return {
            "last_teacher_message": f"Excellent work! We've covered all the key concepts. You've done a wonderful job exploring {TOPIC_TITLE}! 🎉",
            "session_complete": True,
            "waiting_for_input": False
        }
    
    current_concept = concepts[current_idx]
    
    # Gather context
    strategy = state.get("strategy", "continue")
    teacher_mode = state.get("teacher_mode", "encouraging")
    understanding = state.get("understanding_level", "none")
    exchange_count = state.get("exchange_count", 0)
    param_history = state.get("parameter_history", [])
    current_params = state.get("current_params", {})
    conversation = state.get("conversation_history", [])
    student_response = state.get("student_response", "")
    needs_clarification = state.get("needs_clarification", False)
    is_factually_wrong = state.get("is_factually_wrong", False)
    
    # New: Check if student asked a question or requested param change
    student_asked_question = state.get("student_asked_question", False)
    question_asked = state.get("question_asked", "")
    student_requested_param = state.get("student_requested_param", False)
    requested_param = state.get("requested_param", "")
    requested_value = state.get("requested_value", None)
    student_wants_to_see_simulation = state.get("student_wants_to_see_simulation", False)

    # NEW: Student-driven simulation parameter changes
    student_changed_params_this_turn = state.get("student_changed_params_this_turn", False)
    student_changed_params = state.get("student_changed_params", {})

    # Language this session is running in — controls what language the LLM must respond in.
    # This is critical for Kannada simulations: their titles/descriptions are in Kannada,
    # which would otherwise cause the LLM to infer and respond in Kannada even for English sessions.
    session_language = state.get("language", "english")
    language_instruction = "English" if session_language.lower() == "english" else session_language.capitalize()

    # The first simulation message does not need adaptive reasoning. Avoid an
    # LLM call while preserving the same history, counters, simulation display,
    # and interrupt-before-evaluator behavior used by later turns.
    is_first_session_message = (
        current_idx == 0
        and exchange_count == 0
        and not conversation
        and not student_response
    )
    if is_first_session_message:
        with measure("simulation_initial_template"):
            teacher_message = (
                f"Hello! Let's explore {TOPIC_TITLE} with this interactive simulation. "
                f"We'll begin with {current_concept['title']}. Observe the simulation: "
                "what do you notice?"
            )
            first_param = next(
                iter(current_concept.get("related_params", [])),
                next(iter(PARAMETER_INFO), None),
            )
            new_message = add_message_to_history(state, "teacher", teacher_message)
            updates = {
                "last_teacher_message": teacher_message,
                "waiting_for_input": True,
                "exchange_count": 1,
                "needs_deeper": False,
                "conversation_history": state.get("conversation_history", []) + [new_message],
                "current_params": current_params.copy(),
                "last_displayed_params": current_params.copy(),
                "show_simulation": True,
                "student_changed_params_this_turn": False,
                "student_changed_params": {},
            }

            if first_param is not None:
                current_value = current_params.get(first_param)
                updates["parameter_history"] = state.get("parameter_history", []) + [{
                    "parameter": first_param,
                    "old_value": current_value,
                    "new_value": current_value,
                    "reason": "Display initial simulation state",
                    "prediction_asked": "What do you notice?",
                    "student_reaction": "",
                    "understanding_before": understanding,
                    "understanding_after": "",
                    "was_effective": False,
                    "initiated_by": "agent",
                }]

            print("[TEACHER] Using deterministic initial simulation message")
            return updates

    print(f"   Concept: {current_concept['title']}")
    print(f"   Strategy: {strategy}")
    print(f"   Mode: {teacher_mode}")
    print(f"   Understanding: {understanding}")
    print(f"   Exchange #: {exchange_count}")
    if student_asked_question:
        print(f"   ❓ Student asked: {question_asked}")
    if student_requested_param:
        if student_wants_to_see_simulation:
            print(f"   🖥️ Student wants to SEE the simulation")
        else:
            print(f"   🎛️ Student requested: {requested_param} = {requested_value}")
    if is_factually_wrong:
        print(f"   ❌ Student gave WRONG answer - needs correction")
    if needs_clarification:
        print(f"   🔄 Clarification requested")
    
    # Build dynamic simulation info from config
    current_params_str = ", ".join([
        f"{info['label']}={current_params.get(key, '?')}"
        for key, info in PARAMETER_INFO.items()
    ])
    
    available_params_str = "\n".join([
        f"- {key}: {info['range']} ({info['effect']})"
        for key, info in PARAMETER_INFO.items()
    ])
    
    cannot_demonstrate_str = "\n".join([f"- {item}" for item in CANNOT_DEMONSTRATE])
    
    # Add problem examples if available (for simulations with multiple examples)
    problem_examples_str = ""
    if "problem_examples" in sim_config:
        examples = sim_config["problem_examples"]
        problem_examples_str = "\n\nAVAILABLE EXAMPLES (problemIndex):\n"
        for ex in examples:
            rule_emoji = "➖" if ex["rule"] == "minus" else "➕"
            problem_examples_str += f"{rule_emoji} {ex['index']}: {ex['expression']} = {ex['result'].split('=')[0].strip()} ({ex['rule'].upper()} before bracket)\n"
        problem_examples_str += "\n⚠️ CRITICAL: Always check this list to know which problemIndex shows which rule!"
    
    # Build the teaching prompt
    system_prompt = f"""⚠️ LANGUAGE REQUIREMENT: You MUST write your ENTIRE response in {language_instruction} only. This is mandatory. Do not use any other language, even if the topic title or description below contains text in another language.

You are a warm, engaging science teacher named Alex. You're teaching a student about {TOPIC_TITLE} through an interactive simulation.

TOPIC DETAILS:
{TOPIC_DESCRIPTION}
{problem_examples_str}

⚠️ CRITICAL: You MUST respond with ONLY a valid JSON object. No extra text before or after.
Your response must start with {{ and end with }}.

YOUR PERSONALITY:
- Warm, patient, and genuinely interested in helping students learn
- Uses analogies and real-world examples
- Celebrates small wins and acknowledges effort
- Never makes students feel bad for wrong answers
- Asks thought-provoking questions rather than just telling

YOUR TEACHING MODE: {teacher_mode.upper()}
{"- Be extra supportive and break things down simply" if teacher_mode == "simplifying" else ""}
{"- Gently push the student to think deeper" if teacher_mode == "challenging" else ""}
{"- Celebrate progress and build confidence" if teacher_mode == "encouraging" else ""}

CURRENT TEACHING STRATEGY: {strategy}
{"- Continue with your current approach, it's working" if strategy == "continue" else ""}
{"- Try a different explanation style or analogy" if strategy == "try_different" else ""}
{"- Break this down into smaller, simpler parts" if strategy == "scaffold" else ""}
{"- Give a more direct hint to guide them" if strategy == "give_hint" else ""}
{"- Summarize the key point and prepare to move on" if strategy == "summarize_advance" else ""}

SIMULATION INFO:
Current parameters: {current_params_str}

Available parameters:
{available_params_str}

⚠️ IMPORTANT - DO NOT MENTION THESE (not in this simulation):
{cannot_demonstrate_str}

CRITICAL RULES FOR ASKING QUESTIONS:
1. **ALWAYS end with ONE specific, answerable question**
2. **Give options when asking for predictions**: e.g., "Will it be bigger or smaller?", "More or less?"
3. **Be explicit about what you want**: Ask about specific observable effects
4. **Avoid vague prompts** like "what do you think?" without context
5. Keep responses concise (2-3 sentences + 1 clear question)
6. When suggesting a parameter change, ask for prediction with options FIRST
7. Use "friend" occasionally for warmth

EXAMPLES OF BAD VAGUE QUESTIONS (AVOID):
- "What do you think about that?"
- "Interesting, isn't it?"
- "What comes to mind?"
- "Let's think about this..."

RULE: ALWAYS SHOW SIMULATION WHEN YOU REFERENCE IT:
Whenever your teacher_message asks the student to "OBSERVE:", "watch", "look at", "see", or "notice"
the simulation in any way, you MUST set "suggests_param_change": true in your JSON response.
This triggers the simulation to actually appear on the student's screen.
Even if you are NOT changing values, use the current parameters with suggests_param_change=true
so the student can actually see what you are asking them to observe.
"""

    # Build user prompt based on context
    if exchange_count == 0:
        # First interaction for this concept
        # Check if we're coming from a previous concept (need to summarize it first)
        previous_concept = None
        if current_idx > 0:
            previous_concept = concepts[current_idx - 1]
        
        if previous_concept:
            # We just completed a concept - summarize it and introduce the new one
            # Check if new concept has different related params - if so, we should change one
            new_params = current_concept.get('related_params', [])
            should_change = len(new_params) > 0
            suggested_param = new_params[0] if new_params else None
            
            user_prompt = f"""
PREVIOUS CONCEPT (just completed):
Title: {previous_concept['title']}
Key Insight: {previous_concept['key_insight']}

NEW CONCEPT TO INTRODUCE:
Title: {current_concept['title']}
Key Insight: {current_concept['key_insight']}
Relevant Parameters: {current_concept['related_params']}

The student just demonstrated understanding of the previous concept. Your job is to:
1. FIRST: Celebrate and SUMMARIZE what they just learned (1-2 sentences confirming the key insight)
2. THEN: Smoothly transition to the new concept
3. **IMPORTANT**: Change a parameter to set up the new concept (e.g., change "{suggested_param}" to demonstrate the new concept)
4. End with a question or prediction about the new concept

Example structure:
"Great job! You've discovered that [key insight from previous concept]. 
Now let's explore [new concept]. I'm going to change [parameter] to [value].
PREDICT: What do you think will happen?"

⚠️ RESPOND WITH ONLY THIS JSON FORMAT (no other text):
```json
{{
    "teacher_message": "Your message that summarizes previous + introduces new with a parameter change...",
    "suggests_param_change": {str(should_change).lower()},
    "param_to_change": "{suggested_param}",
    "new_value": <pick a good value from the parameter's range>,
    "change_reason": "To demonstrate the new concept",
    "prediction_question": "What do you think will happen?"
}}
```
"""
        else:
            # Very first concept - just introduce it AND SHOW the simulation
            suggested_param = current_concept.get('related_params', [None])[0]
            user_prompt = f"""
CONCEPT TO TEACH:
Title: {current_concept['title']}
Description: {current_concept['description']}
Key Insight: {current_concept['key_insight']}
Relevant Parameters: {current_concept['related_params']}

This is the START of the lesson. The student hasn't said anything yet.

Generate an engaging introduction that:
1. Introduces what we'll explore
2. Mentions the current visualization (with parameters: {current_params_str})
3. Connects to something relatable if possible
4. Ends with a thought-provoking question OR asks for a prediction with options

⚠️ IMPORTANT: Set suggests_param_change to TRUE so the simulation is VISIBLE from the start!
You can use the current parameters or make a small adjustment to make it show.

⚠️ RESPOND WITH ONLY THIS JSON FORMAT (no other text):
```json
{{
    "teacher_message": "Your warm intro that mentions the visual/simulation...",
    "suggests_param_change": true,
    "param_to_change": "{suggested_param}",
    "new_value": {current_params.get(suggested_param, 0) if suggested_param else 0},
    "change_reason": "Display initial simulation state",
    "prediction_question": "What do you notice/expect?"
}}
```
"""
    else:
        # Continuing conversation
        needs_deeper = state.get("needs_deeper", False)
        is_factually_wrong = state.get("is_factually_wrong", False)
        
        # Build instruction for student's QUESTION
        question_instruction = ""
        if student_asked_question and question_asked:
            question_instruction = f"""
❓❓❓ MANDATORY: STUDENT ASKED A QUESTION - YOU MUST ANSWER IT ❓❓❓
The student asked: "{question_asked}"

⚠️ YOU MUST ANSWER THIS QUESTION DIRECTLY. DO NOT deflect or delay!
⚠️ DO NOT say "before we dive into that..." or "let's see first..."
⚠️ ANSWER FIRST, then continue teaching

Use the topic description and parameter info provided to answer accurately.

YOUR RESPONSE FORMAT:
1. FIRST: Answer the question directly (2-3 sentences)
2. THEN: Optionally connect to what we're learning
3. FINALLY: Ask a follow-up question to continue teaching
"""

        # Build instruction for student's PARAMETER REQUEST
        param_request_instruction = ""
        if student_requested_param and requested_param:
            if student_wants_to_see_simulation:
                # Student asked to see/show/display the simulation
                param_request_instruction =f"""
🖥️🖥️🖥️ MANDATORY: STUDENT WANTS TO SEE THE SIMULATION 🖥️🖥️🖥️
The student asked to see, show, or display the simulation.

⚠️ CRITICAL: YOU MUST make this visible to them!

YOU MUST:
1. ACKNOWLEDGE positively: "Of course!" or "Sure, let me show you!" or "Absolutely!"
2. DESCRIBE the current simulation state using the CURRENT parameters:
   {current_params_str}
3. GUIDE their attention: "Look at..." or "Notice how..." or "Can you see..."
4. ASK an observation question about what they see

IMPORTANT:
- Set "suggests_param_change": true (this triggers the visual display)
- You can choose ANY parameter to "refresh" or use a related param from the concept
- This makes the simulation visible on their screen!

Example Response:
{{
    "teacher_message": "Of course, friend! Right now you're looking at [describe current state with {current_params_str}]. Can you see [ask about a visual element]?",
    "suggests_param_change": true,
    "param_to_change": "{list(PARAMETER_INFO.keys())[0] if PARAMETER_INFO else 'parameter'}",
    "new_value": {current_params.get(list(PARAMETER_INFO.keys())[0] if PARAMETER_INFO else '', 0)},
    "change_reason": "Display current simulation state",
    "prediction_question": "What do you observe?"
}}
"""
            else:
                # Normal parameter change request
                param_request_instruction = f"""
🎛️🎛️🎛️ MANDATORY: STUDENT REQUESTED PARAMETER CHANGE 🎛️🎛️🎛️
The student wants to change: {requested_param}

⚠️ CRITICAL RULES:
1. DO NOT say "Not quite" or correct them - they made a REQUEST, not an answer!
2. DO NOT override their request with different values
3. DO NOT say "but let's do something else instead"
4. RESPECT their curiosity and desire to experiment!

YOU MUST:
1. ACKNOWLEDGE positively: "Sure!" or "Great idea!" or "Let's try that!"
2. CONFIRM you're making their requested change (not a different one)
3. GUIDE observation: "OBSERVE: What do you notice now?"

DO NOT DO THIS (wrong):
❌ "Not quite, friend. Actually..." - This is for WRONG ANSWERS, not requests!
❌ "Let me change it to something else instead..." - Respect their choice!
❌ "But first let's..." - Don't delay or redirect!
"""

        # Build instruction for correction if student gave WRONG answer
        correction_instruction = ""
        if is_factually_wrong and not student_asked_question and not student_requested_param:
            correction_instruction = """
⚠️⚠️⚠️ STUDENT GAVE A FACTUALLY WRONG ANSWER - MUST CORRECT ⚠️⚠️⚠️
The student stated something that is INCORRECT. You MUST:
1. POLITELY but CLEARLY tell them they are wrong: "Not quite, friend." or "Actually, that's not correct."
2. STATE the correct fact based on the topic and parameter effects
3. OFFER to demonstrate: "Let me show you with the simulation..."

DO NOT:
❌ Say "Good thinking!" or "You're on the right track!" - they are NOT
❌ Say "Almost!" or "Close!" - they got it WRONG
❌ Validate their incorrect answer in ANY way

DO:
✅ Be kind but honest: "Not quite, friend."
✅ Correct clearly: "Actually, [correct fact]"
✅ Help them see: "Let me demonstrate..."
"""
        
        # Build instruction for asking WHY if they gave observation without reasoning
        deeper_instruction = ""
        if needs_deeper and not is_factually_wrong and not student_asked_question and not student_requested_param:
            deeper_instruction = """
⚠️ STUDENT GAVE CORRECT OBSERVATION BUT NO REASONING:
They said WHAT happens correctly, but didn't explain WHY. Your job is to:
1. CELEBRATE their correct observation ("Exactly right!" or "Great observation!")
2. ASK them WHY they think that happens
3. Give a hint if helpful based on the concept's key insight
This is NOT a correction - they're on the right track! Just need them to think deeper.
"""
        
        # Build the correction flag at the very top of prompt
        wrong_answer_alert = ""
        if is_factually_wrong and not student_asked_question and not student_requested_param:
            wrong_answer_alert = """
🚨🚨🚨 CRITICAL: STUDENT GAVE WRONG ANSWER - MUST CORRECT! 🚨🚨🚨
DO NOT PRAISE! DO NOT SAY "EXACTLY RIGHT" OR "GREAT OBSERVATION"!
The student's answer is FACTUALLY INCORRECT. You MUST start with:
"Not quite, friend..." or "Actually, that's not correct..."
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
"""
        
        # Build instruction for student INDEPENDENTLY CHANGED params (new feature)
        student_exploration_instruction = ""
        if student_changed_params_this_turn and student_changed_params:
            changed_lines = []
            for param_key, new_val in student_changed_params.items():
                info = PARAMETER_INFO.get(param_key, {})
                label = info.get("label", param_key)
                effect = info.get("effect", "")
                old_val = current_params.get(param_key, "?")
                changed_lines.append(f"  - {label}: {old_val} → {new_val}  (Effect: {effect})")
            
            student_text = student_response.strip()
            if student_text:
                student_context_note = f'The student also said: "{student_text}"'
            else:
                student_context_note = "(The student did not type anything — they only changed the simulation parameter.)" 

            student_exploration_instruction = f"""
🎛️🎛️🎛️ STUDENT INDEPENDENTLY CHANGED SIMULATION PARAMETERS 🎛️🎛️🎛️
Parameters changed this turn:
{chr(10).join(changed_lines)}
{student_context_note}

This is an EXPLORATORY action — the student is experimenting on their own!
⚠️ YOUR RESPONSE MUST:
1. Acknowledge what they changed with genuine excitement: "Oh, I see you changed [X] to [Y]..."
2. Ask what they OBSERVED or NOTICED: "What did you notice happen to the simulation?"
3. Connect their exploration to the concept we are teaching
4. Set suggests_param_change=true so the simulation updates to their chosen values

⚠️ DO NOT:
- Correct them or redirect them to different values (they chose these!)
- Evaluate their response as right or wrong (they made a change, not an answer)
- Ask for a prediction (they already changed it — ask for an OBSERVATION instead)
🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️🎛️
"""

        user_prompt = f"""{wrong_answer_alert}
CONCEPT BEING TAUGHT:
Title: {current_concept['title']}
Key Insight: {current_concept['key_insight']}

STUDENT'S UNDERSTANDING LEVEL: {understanding}
EXCHANGE NUMBER: {exchange_count}
{student_exploration_instruction}
{question_instruction}
{param_request_instruction}
{correction_instruction}
{deeper_instruction}

PARAMETER CHANGE HISTORY:
{format_parameter_history(param_history)}

RECENT CONVERSATION:
{format_conversation_history(conversation)}

STUDENT'S LATEST RESPONSE: "{student_response}"

═══════════════════════════════════════════════════════════════
⚠️ CRITICAL RULES - READ CAREFULLY
═══════════════════════════════════════════════════════════════

RULE 1 - HONEST FEEDBACK (NO FALSE PRAISE OR VALIDATION):
⚠️ CRITICAL: Never validate or praise WRONG answers!

IF understanding is "none" AND student gave a WRONG answer (not just "I don't know"):
- Do NOT say: "Good thinking!", "Right direction!", "That's a reasonable thought!"
- Do NOT say: "You're onto something!", "Close!", "Almost!"
- DO say: "Not quite, friend." or "Actually, that's not correct."
- THEN explain the correct answer based on the concept being taught
- Be KIND but HONEST - false praise confuses students!

IF student said "I don't know":
- Say: "That's okay! Let me help you figure this out..."
- This is DIFFERENT from being wrong - they haven't made a mistake, they just need help

IF student is CORRECT:
- Praise appropriately: "Exactly right!" or "Great observation!"

EXAMPLES:
❌ WRONG (don't do this): "Good thinking! But actually the opposite happens..."
✅ RIGHT: "Not quite, friend. [Correct fact]. Let me show you why..."

❌ WRONG: "You're on the right track! Though the answer is actually the opposite..."
✅ RIGHT: "Actually, that's the opposite of what happens. Let me demonstrate..."

RULE 2 - ALWAYS BE SPECIFIC ABOUT WHAT YOU WANT:
Every response MUST end with a CLEAR ACTION for the student. Use these formats:

For PREDICTIONS (before changing parameter):
"I'm going to change [parameter]. PREDICT: What do you think will happen?"

For OBSERVATIONS (after changing parameter):
"Watch the simulation now. OBSERVE: What do you notice?"

For EXPLANATIONS:
"EXPLAIN: Why do you think that happens?"

RULE 3 - ONE CLEAR QUESTION:
- End with exactly ONE question
- Make it specific with options when possible
- Label it clearly: PREDICT/OBSERVE/EXPLAIN

{"⚠️ They gave correct observation! Celebrate it, then ask them to EXPLAIN why." if needs_deeper else ""}
{"🎉 They understand well - acknowledge success and move forward!" if understanding == 'complete' and not needs_deeper else ""}
{"They don't know yet - that's okay! Help them by changing a parameter and asking them to OBSERVE or PREDICT." if understanding == 'none' and not needs_deeper else ""}
{"They're trying but not quite right - guide them with a clearer question." if understanding == 'partial' and not needs_deeper else ""}

═══════════════════════════════════════════════════════════════
🔧 RULE 4 - USE PARAMETER CHANGES TO TEACH (MANDATORY!)
═══════════════════════════════════════════════════════════════
The simulation is your BEST teaching tool! When student is stuck:

**IF exchange >= 2 OR understanding is "none":**
You MUST change a parameter to help them SEE the concept!

Example flow:
1. "Let me show you! I'm changing [parameter] to [value]."
2. "OBSERVE: Watch the simulation now. What do you notice?"

**Choose the right parameter for the concept using the related_params list.**

**Current concept: {current_concept['title']}**
**Related parameters: {current_concept['related_params']}**

⚠️ IMPORTANT: If exchange_count >= 2 and understanding is "none" or "partial":
   SET suggests_param_change = true
   PICK a relevant parameter from the concept's related_params
   GIVE a reasonable new value

⚠️ RESPOND WITH ONLY THIS JSON FORMAT (no other text):
```json
{{
    "teacher_message": "Your response ending with a clear PREDICT/OBSERVE/EXPLAIN question...",
    "suggests_param_change": {"true" if understanding in ['none', 'partial'] and exchange_count >= 2 else "true or false"},
    "param_to_change": "length or number_of_oscillations or null",
    "new_value": "number or null",
    "change_reason": "Why this change helps learning",
    "prediction_question": "What do you think will happen if...? (if suggesting change)"
}}
```

REMEMBER: Output ONLY the JSON object. Start your response with {{ and end with }}.
"""

    # Single selection — key flows through to tracking and LLM construction
    llm, used_api_key = get_llm_with_key()

    # Build simulation URL for LangSmith metadata
    # Use the simulation_id from state (already loaded at top of function)
    # sim_config should already be available from the function scope
    import os
    
    # Build URL with current parameters
    base_url = sim_config.get("file", "")
    github_pages_base = os.environ.get("GITHUB_PAGES_BASE_URL", "")
    if github_pages_base:
        # Keep the full path including simulations/ directory
        simulation_url = f"{github_pages_base}/{base_url}"
    else:
        simulation_url = base_url
    
    # Add parameters to URL
    param_parts = []
    for key, value in current_params.items():
        if value is not None:
            param_parts.append(f"{key}={value}")
    
    if param_parts:
        simulation_url += "?" + "&".join(param_parts)
    
    # Prepare LangSmith metadata
    langsmith_metadata = {
        "simulation_url": simulation_url,
        "simulation_id": simulation_id,
        "concept": current_concept['title'],
        "understanding_level": understanding,
        "strategy": strategy,
        "teacher_mode": teacher_mode,
        "exchange_count": exchange_count,
        "parameters": json.dumps(current_params)
    }
    
    print(f"[TEACHER] 📊 LangSmith metadata: simulation_url={simulation_url}")
    print(f"[TEACHER] 📊 LangSmith metadata: simulation_id={simulation_id}")
    
    # Also try to update the current node run's metadata directly
    try:
        from langsmith import get_current_run_tree
        rt = get_current_run_tree()
        if rt:
            rt.metadata = {**(rt.metadata or {}), **langsmith_metadata}
            print(f"[TEACHER] ✅ Updated current run tree metadata")
        else:
            print(f"[TEACHER] ℹ️ No current run tree (metadata will be on child span)")
    except Exception as e:
        print(f"[TEACHER] ⚠️ Run tree update: {e}")
    
    # Use model-aware invocation (handles both Gemma and Gemini)
    response = invoke_llm_with_prompts(llm, system_prompt, user_prompt, api_key=used_api_key, metadata=langsmith_metadata, parent_config=config)
    
    try:
        result = parse_json_safe(extract_text_content(response.content))
    except Exception as e:
        print(f"   ⚠️ JSON parse failed, using raw response")
        # Attempt to salvage the human-readable portion by stripping any
        # leaked JSON block that the model appended to its plain-text reply.
        salvaged = clean_teacher_message(extract_text_content(response.content))
        result = {
            "teacher_message": salvaged,
            "suggests_param_change": False
        }
    
    teacher_message = clean_teacher_message(result.get("teacher_message", extract_text_content(response.content)))
    
    # ─── Post-process: force simulation display when teacher references it ───
    # If the teacher message contains observation/watch keywords but the LLM
    # forgot to set suggests_param_change=true, we enforce it here so the
    # student can actually see what is being referenced.
    _msg_lower = teacher_message.lower()
    _observe_keywords = [
        "observe:", "observe the", "observe our", "observe your",
        "watch the simulation", "watch now", "watch it",
        "see the simulation", "see it", "see our",
        "look at the simulation", "look at it",
        "take a moment to observe", "take a look",
        "notice how", "notice the",
        "show you the simulation", "showing you", "let me show",
        "here's the simulation", "here is the simulation",
    ]
    if not result.get("suggests_param_change") and any(kw in _msg_lower for kw in _observe_keywords):
        _first_param = list(PARAMETER_INFO.keys())[0] if PARAMETER_INFO else None
        if _first_param:
            result["suggests_param_change"] = True
            if not result.get("param_to_change"):
                result["param_to_change"] = _first_param
            if result.get("new_value") is None:
                result["new_value"] = current_params.get(_first_param, 0)
            if not result.get("change_reason"):
                result["change_reason"] = "Display simulation as referenced in teacher message"
            print(f"   🔄 POST-PROCESS: Forced suggests_param_change=True (teacher said 'observe/watch/see')")
    # ─────────────────────────────────────────────────────────────────────────

    # Handle parameter change suggestion
    # If this was a pure exploration turn, do not charge them an exchange count
    next_exchange_count = exchange_count if student_changed_params_this_turn else exchange_count + 1
    
    updates = {
        "last_teacher_message": teacher_message,
        "waiting_for_input": True,
        "exchange_count": next_exchange_count,
        "needs_deeper": False  # Reset after handling
    }
    
    # Add message to history
    new_message = add_message_to_history(state, "teacher", teacher_message)
    updates["conversation_history"] = state.get("conversation_history", []) + [new_message]
    
    # ── Simulation display logic ──────────────────────────────────────────────
    # Tracks two things:
    #   1. show_simulation (Feature 1): explicit per-turn flag so the API can
    #      tell the frontend "display now" vs stale param_change from the past.
    #   2. last_displayed_params (Feature 2): suppress consecutive renders of
    #      the exact same parameter set unless the student explicitly asked.
    last_displayed_params = state.get("last_displayed_params", {})
    student_wants_to_see = state.get("student_wants_to_see_simulation", False)
    show_simulation = False

    if result.get("suggests_param_change") and result.get("param_to_change"):
        param = result["param_to_change"]
        new_val = result.get("new_value")
        
        if param and new_val is not None:
            # Build the candidate params if this change is applied
            new_params = current_params.copy()
            new_params[param] = new_val

            # Feature 2: suppress repeat if params are unchanged from last display
            # UNLESS the student explicitly asked to see the simulation
            if new_params == last_displayed_params and not student_wants_to_see:
                print(f"\n   ⏭️ SKIP: Params unchanged from last display — suppressing repeat simulation")
                # show_simulation stays False; no history entry added
            else:
                # Record the parameter change
                change_record = {
                    "parameter": param,
                    "old_value": current_params.get(param, 0),
                    "new_value": new_val,
                    "reason": result.get("change_reason", "To illustrate the concept"),
                    "prediction_asked": result.get("prediction_question", ""),
                    "student_reaction": "",
                    "understanding_before": understanding,
                    "understanding_after": "",
                    "was_effective": False,
                    "initiated_by": "agent"
                }
                
                updates["current_params"] = new_params
                updates["parameter_history"] = state.get("parameter_history", []) + [change_record]
                updates["last_displayed_params"] = new_params
                show_simulation = True  # Feature 1: mark display for this turn
                print(f"\n   📊 Parameter Change: {param} = {change_record['old_value']} → {new_val}")
    
    # Feature 1: always write the flag so API response is accurate this turn
    updates["show_simulation"] = show_simulation
    # ─────────────────────────────────────────────────────────────────────────

    # ── NEW: Merge student-changed params into current_params ─────────────────
    # When the student dragged sliders this turn, we need to:
    # 1. Apply their chosen values to current_params (so the next simulation URL is correct)
    # 2. Add a history entry tagged as student-initiated
    # 3. Reset the flag so it doesn't fire again next turn
    if student_changed_params_this_turn and student_changed_params:
        # Start from whatever current_params already are (possibly updated by agent above)
        merged_params = dict(updates.get("current_params", current_params))
        student_history_entries = list(updates.get("parameter_history", state.get("parameter_history", [])))

        for param_key, new_val in student_changed_params.items():
            old_val = current_params.get(param_key)
            merged_params[param_key] = new_val
            student_history_entries.append({
                "parameter": param_key,
                "old_value": old_val,
                "new_value": new_val,
                "reason": "Student changed independently",
                "prediction_asked": "",
                "student_reaction": student_response,
                "understanding_before": understanding,
                "understanding_after": "",
                "was_effective": None,          # Unknown until next evaluation
                "initiated_by": "student"       # Tag as student-driven
            })
            print(f"   🎛️ Applied student param: {param_key} {old_val} → {new_val}")

        updates["current_params"] = merged_params
        updates["parameter_history"] = student_history_entries
        updates["last_displayed_params"] = merged_params
        updates["show_simulation"] = True  # Always show when student changed params

        print(f"   ✅ Student-driven params merged into current_params: {merged_params}")

    # Always reset student params flag so it doesn't persist into next turn
    updates["student_changed_params_this_turn"] = False
    updates["student_changed_params"] = {}
    # ─────────────────────────────────────────────────────────────────────────

    # Print the teacher's message
    print(f"\n🎓 Teacher says:")
    print(f"   {teacher_message}")
    
    return updates
