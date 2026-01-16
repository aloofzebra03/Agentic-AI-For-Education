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

from simulation_to_concept.config import (
    GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, CANNOT_DEMONSTRATE, 
    PARAMETER_INFO, TOPIC_TITLE, TOPIC_DESCRIPTION
)
from simulation_to_concept.state import add_message_to_history


def get_llm():
    """Get configured LLM instance."""
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=TEMPERATURE
    )


def is_gemma_model() -> bool:
    """Check if using a Gemma model (doesn't support system messages)."""
    return "gemma" in GEMINI_MODEL.lower()


def invoke_llm_with_prompts(llm, system_prompt: str, user_prompt: str):
    """
    Invoke LLM with model-aware message handling.
    
    Gemma models don't support SystemMessage, so we combine prompts.
    Gemini models support SystemMessage for better results.
    """
    if is_gemma_model():
        # Combine system and user prompt for Gemma
        combined_prompt = f"{system_prompt}\n\n---\n\nNow respond to this:\n\n{user_prompt}"
        return llm.invoke([HumanMessage(content=combined_prompt)])
    else:
        # Use proper system message for Gemini
        return llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])


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


def teacher_node(state: Dict[str, Any]) -> Dict[str, Any]:
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
    
    print(f"   Concept: {current_concept['title']}")
    print(f"   Strategy: {strategy}")
    print(f"   Mode: {teacher_mode}")
    print(f"   Understanding: {understanding}")
    print(f"   Exchange #: {exchange_count}")
    if student_asked_question:
        print(f"   ❓ Student asked: {question_asked}")
    if student_requested_param:
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
    
    # Build the teaching prompt
    system_prompt = f"""You are a warm, engaging science teacher named Alex. You're teaching a student about {TOPIC_TITLE} through an interactive simulation.

TOPIC DETAILS:
{TOPIC_DESCRIPTION}

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
            # Very first concept - just introduce it
            user_prompt = f"""
CONCEPT TO TEACH:
Title: {current_concept['title']}
Description: {current_concept['description']}
Key Insight: {current_concept['key_insight']}
Relevant Parameters: {current_concept['related_params']}

This is the START of the lesson. The student hasn't said anything yet.

Generate an engaging introduction that:
1. Introduces what we'll explore
2. Connects to something relatable if possible
3. Ends with a thought-provoking question OR asks for a prediction with options

⚠️ RESPOND WITH ONLY THIS JSON FORMAT (no other text):
```json
{{
    "teacher_message": "Your warm, engaging introduction...",
    "suggests_param_change": false,
    "param_to_change": null,
    "new_value": null,
    "prediction_question": null
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
        
        user_prompt = f"""{wrong_answer_alert}
CONCEPT BEING TAUGHT:
Title: {current_concept['title']}
Key Insight: {current_concept['key_insight']}

STUDENT'S UNDERSTANDING LEVEL: {understanding}
EXCHANGE NUMBER: {exchange_count}
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

    llm = get_llm()
    
    # Use model-aware invocation (handles both Gemma and Gemini)
    response = invoke_llm_with_prompts(llm, system_prompt, user_prompt)
    
    try:
        result = parse_json_safe(response.content)
    except Exception as e:
        print(f"   ⚠️ JSON parse failed, using raw response")
        result = {
            "teacher_message": response.content,
            "suggests_param_change": False
        }
    
    teacher_message = result.get("teacher_message", response.content)
    
    # Handle parameter change suggestion
    updates = {
        "last_teacher_message": teacher_message,
        "waiting_for_input": True,
        "exchange_count": exchange_count + 1,
        "needs_deeper": False  # Reset after handling
    }
    
    # Add message to history
    new_message = add_message_to_history(state, "teacher", teacher_message)
    updates["conversation_history"] = state.get("conversation_history", []) + [new_message]
    
    # Handle parameter change
    if result.get("suggests_param_change") and result.get("param_to_change"):
        param = result["param_to_change"]
        new_val = result.get("new_value")
        
        if param and new_val is not None:
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
                "was_effective": False
            }
            
            # Update params
            new_params = current_params.copy()
            new_params[param] = new_val
            
            updates["current_params"] = new_params
            updates["parameter_history"] = state.get("parameter_history", []) + [change_record]
            
            print(f"\n   📊 Parameter Change: {param} = {change_record['old_value']} → {new_val}")
    
    # Print the teacher's message
    print(f"\n🎓 Teacher says:")
    print(f"   {teacher_message}")
    
    return updates
