# agent/nodes2.py

import json
from typing import Literal, Optional, Dict

from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from educational_agent.config_rag import concept_pkg
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import shared utilities
from educational_agent.shared_utils import (
    AgentState,
    extract_json_block,
    get_llm,
    add_ai_message_to_conversation,
    llm_with_history,
    build_conversation_history,
    build_prompt_from_template,
    get_ground_truth,
)

PEDAGOGICAL_MOVES: Dict[str, Dict[str, str]] = {
    "APK": {
        "goal": "Activate prior knowledge; pose a hook linking the concept to everyday intuition.",
        "constraints": "Do not reveal definitions or answers; question must be common-sense answerable."
    },  
    "CI": {
        "goal": "Provide a concise definition (≤30 words); ask learner to restate it.",
        "constraints": "Keep definition crisp; hint why it matters in ≤1 phrase."
    },
    "GE": {
        "goal": "Ask a why/how question to explore the mechanism; respond with hint or affirmation.",
        "constraints": "Provide only one nudge if learner struggles; do not lecture."
    },
    "MH": {
        "goal": "Detect and correct misconceptions gently.",
        "constraints": "Start positive; keep correction ≤2 sentences."
    },
    "AR": {
        "goal": "Generate a short quiz (T/F, MCQ, or short answer) and prompt learner.",
        "constraints": "Give immediate feedback after each question."
    },
    "TC": {
        "goal": "Pose a hypothetical transfer question applying the concept in a new context.",
        "constraints": "Scenario plausible but unfamiliar; ≤2 sentences."
    },
    "RLC": {
        "goal": "Provide a real-life application/context; ask if learner has seen or used it themselves.",
        "constraints": "Story ≤3 sentences; open-ended question."
    },
    "END": {
        "goal": "Summarize 2–3 bullet takeaways; offer next actions.",
        "constraints": "Bullet format; no new content."
    },
}


# ─── Pydantic response models ─────────────────────────────────────────────────

class ApkResponse(BaseModel):
    feedback: str
    next_state: Literal["CI", "APK"]

class CiResponse(BaseModel):
    feedback: str
    next_state: Literal["GE", "CI"]

class GeResponse(BaseModel):
    feedback: str
    next_state: Literal["MH", "AR"]
    correction: Optional[str] = None

class MhResponse(BaseModel):
    feedback: str
    next_state: Literal["MH", "AR"]

class ArResponse(BaseModel):
    score: float
    feedback: str

class TcResponse(BaseModel):
    correct: bool
    feedback: str

class RlcResponse(BaseModel):
    feedback: str
    next_state: Literal["RLC", "END"]

# ─── Parsers ───────────────────────────────────────────────────────────────────

apk_parser = PydanticOutputParser(pydantic_object=ApkResponse)
ci_parser  = PydanticOutputParser(pydantic_object=CiResponse)
ge_parser  = PydanticOutputParser(pydantic_object=GeResponse)
mh_parser  = PydanticOutputParser(pydantic_object=MhResponse)
ar_parser  = PydanticOutputParser(pydantic_object=ArResponse)
tc_parser  = PydanticOutputParser(pydantic_object=TcResponse)
rlc_parser = PydanticOutputParser(pydantic_object=RlcResponse)



# ─── Node definitions ───────────────────────────────────────────────────────────

def start_node(state: AgentState) -> AgentState:
    system_prompt = (
        f"You are an educational agent helping a learner understand '{concept_pkg.title}'. The learner is a student of class 7. Remember that you are interacting directly with the learner.\n"
        "Greet the learner and ask if they are ready to begin."
        # "Also Remember that the student is of Kannada origin and understands olny kannada.So speak to the student in kannada.The script has to be kannada and not english.\n"
    )
    
    # Build final prompt using template
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False
    )
    
    print("IN START NODE")
    resp = llm_with_history(state, final_prompt)
    # Apply JSON extraction in case LLM wraps response in markdown
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Add AI message to conversation after successful processing
    add_ai_message_to_conversation(state, content)
    
    # 🔍 START NODE - CONTENT PROCESSING 🔍
    print("=" * 80)
    print("🎯 START NODE - CONTENT OUTPUT 🎯")
    print("=" * 80)
    print(f"📄 CONTENT: {content}")
    print(f"📏 CONTENT_LENGTH: {len(content)} characters")
    print(f"📊 CONTENT_TYPE: {type(content).__name__}")
    print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
    print("=" * 80)
    
    state["agent_output"]  = content
    state["current_state"] = "APK"
    return state

def apk_node(state: AgentState) -> AgentState:
    if not state.get("_asked_apk", False):
        state["_asked_apk"] = True
        state["_apk_tries"] = 0
        # Include ground truth for Concept Definition
        gt = get_ground_truth(concept_pkg.title, "Concept Definition")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Concept Definition):\n{gt}\nGenerate one hook question that activates prior knowledge for '{concept_pkg.title}'.",
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        # Add AI message to conversation after successful processing
        add_ai_message_to_conversation(state, content)
        
        # 🔍 APK NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 APK NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    # Handle student's response after hook question
    state["_apk_tries"] = state.get("_apk_tries", 0) + 1
    
    # Check if we've reached max tries (2) - provide answer and move to CI
    if state["_apk_tries"] >= 2:
        gt = get_ground_truth(concept_pkg.title, "Concept Definition")
        final_system_prompt = f"""Current node: APK (Activate Prior Knowledge) - FINAL ATTEMPT
This is the final attempt to help the student identify the concept.

The student has had 2 attempts to identify '{concept_pkg.title}' but hasn't gotten it right.

Ground truth (Concept Definition): {gt}

Task: Provide the correct identification of '{concept_pkg.title}' in a supportive way that:
1. Acknowledges their effort
2. Gives the correct answer clearly
3. Briefly explains why this is the concept
4. Transitions positively to learning more about it

Respond ONLY with a clear, encouraging message (not JSON - just the message text)."""

        # Build final prompt for revealing the concept
        final_prompt = build_prompt_from_template(
            system_prompt=final_system_prompt,
            state=state,
            include_last_message=True,
            include_instructions=False,
            parser=None
        )
        
        final_response = llm_with_history(state, final_prompt).content.strip()
        
        # Add AI message to conversation
        add_ai_message_to_conversation(state, final_response)
        
        # 🔍 APK NODE - MAX TRIES REACHED 🔍
        print("=" * 80)
        print("🎯 APK NODE - MAX TRIES REACHED, PROVIDING ANSWER 🎯")
        print("=" * 80)
        print(f"🔢 APK_TRIES: {state['_apk_tries']}")
        print(f"💬 LLM_FINAL_MESSAGE: {final_response}")
        print("=" * 80)
        
        state["agent_output"] = final_response
        state["current_state"] = "CI"
        return state

    context = json.dumps(PEDAGOGICAL_MOVES["APK"], indent=2)
    system_prompt = f"""Current node: APK (Activate Prior Knowledge)
Possible next_state values:
- "CI": when the student's reply shows they correctly identified '{concept_pkg.title}'.
- "APK": when the student's reply does not clearly identify '{concept_pkg.title}'.

Pedagogical context:
{context}

This is attempt {state["_apk_tries"]} of 2 for prior knowledge activation.

Task: Evaluate whether the student identified the concept correctly. Respond ONLY with JSON matching the schema above. If not, help the student to do so."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=apk_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: ApkResponse = apk_parser.parse(json_text)
        
        # Add AI message to conversation after successful parsing
        add_ai_message_to_conversation(state, parsed.feedback)
        
        # 🔍 APK PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 APK NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"🚀 NEXT_STATE: {parsed.next_state}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception as e:
        print(f"Error parsing APK response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise
    return state

def ci_node(state: AgentState) -> AgentState:
    # print("REACHED HERE")
    if not state.get("_asked_ci", False):
        state["_asked_ci"] = True
        state["_ci_tries"] = 0  # Initialize attempt counter
        # Include ground truth for Explanation (with analogies)
        gt = get_ground_truth(concept_pkg.title, "Explanation (with analogies)")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Explanation):\n{gt}\nProvide a concise definition (≤30 words) of '{concept_pkg.title}', "
            "then ask the learner to restate it."
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        # Add AI message to conversation after successful processing
        add_ai_message_to_conversation(state, content)
        
        # 🔍 CI NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 CI NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    # Increment attempt counter
    state["_ci_tries"] = state.get("_ci_tries", 0) + 1
    
    # Check if we've reached 2 attempts - if so, provide definition and move on
    if state["_ci_tries"] >= 2:
        # gt = get_ground_truth(concept_pkg.title, "Explanation (with analogies)")
        system_prompt = (
            f"The student has struggled with restating the definition. Provide the correct definition of '{concept_pkg.title}' "
            f"clearly and encourage them that it's okay to struggle with new concepts. "
            "Then say 'Now let's explore this concept deeper with a question.'"
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        # Add AI message to conversation after successful processing
        add_ai_message_to_conversation(state, content)
        
        # 🔍 CI NODE - AUTO-PROGRESS CONTENT 🔍
        print("=" * 80)
        print("🎯 CI NODE - AUTO-PROGRESS AFTER 2 TRIES 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔢 CI_TRIES: {state['_ci_tries']}")
        print("=" * 80)
        
        state["agent_output"] = content
        state["current_state"] = "GE"
        return state

    context = json.dumps(PEDAGOGICAL_MOVES["CI"], indent=2)
    system_prompt = f"""Current node: CI (Concept Introduction)
Possible next_state values:
- "GE": when the student's paraphrase accurately captures the definition.
- "CI": when the paraphrase is inaccurate or incomplete.

Pedagogical context:
{context}

This is attempt {state["_ci_tries"]} for the student. If they get it wrong this time, we'll provide the correct definition and move on.

Task: Determine if the restatement is accurate. Respond ONLY with JSON matching the schema above. If not, help the student to do so."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=ci_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: CiResponse = ci_parser.parse(json_text)
        
        # Add AI message to conversation after successful parsing
        add_ai_message_to_conversation(state, parsed.feedback)
        
        # 🔍 CI PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 CI NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"🚀 NEXT_STATE: {parsed.next_state}")
        print(f"🔢 CI_TRIES: {state['_ci_tries']}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception as e:
        print(f"Error parsing CI response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise
    return state

def ge_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ge", False):
        state["_asked_ge"] = True
        # Include ground truth for Details (facts, sub-concepts)
        gt = get_ground_truth(concept_pkg.title, "Details (facts, sub-concepts)")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Details):\n{gt}\nGenerate one 'why' or 'how' question to explore the mechanism of '{concept_pkg.title}'.",
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        # Add AI message to conversation after successful processing
        add_ai_message_to_conversation(state, content)
        
        # 🔍 GE NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 GE NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    context = json.dumps(PEDAGOGICAL_MOVES["GE"], indent=2)
    system_prompt = f"""Current node: GE (Guided Exploration)
Possible next_state values:
- "MH": if you detect a misconception in the student's reasoning (must include a non-empty "correction" ≤2 sentences).
- "AR": if the reasoning is correct or there's no misconception.
Choose ONLY from these options

Pedagogical context:
{context}

If the student's response indicates they don't know or are stuck after two attempts, provide the correct explanation in a concise manner and move on to the next state.

Task: Detect misconception or correct reasoning. RESPOND ONLY WITH JSON matching the schema above."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=ge_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: GeResponse = ge_parser.parse(json_text)
        
        # Add AI message to conversation after successful parsing
        add_ai_message_to_conversation(state, parsed.feedback)
        
        # 🔍 GE PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 GE NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"🚀 NEXT_STATE: {parsed.next_state}")
        print(f"🔧 CORRECTION: {parsed.correction}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        if parsed.next_state == "MH":
            state["last_correction"] = parsed.correction or "Let me clarify that for you."
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception as e:
        print(f"Error parsing GE response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise
    return state

def mh_node(state: AgentState) -> AgentState:
    """Misconception Handling node - addresses student misconceptions and handles follow-up questions"""
    
    # First time entering MH: provide the correction from GE node
    if not state.get("_asked_mh", False):
        state["_asked_mh"] = True
        state["_mh_tries"] = 0
        
        # Get the correction from GE node
        correction = state.get("last_correction", "Let me clarify that for you.")
        
        # Provide the correction to the student
        correction_message = f"I understand your thinking, but let me clarify: {correction}"
        
        # Add AI message to conversation
        add_ai_message_to_conversation(state, correction_message)
        
        # 🔍 MH NODE - FIRST PASS CORRECTION 🔍
        print("=" * 80)
        print("🎯 MH NODE - INITIAL CORRECTION PROVIDED 🎯")
        print("=" * 80)
        print(f"📝 CORRECTION: {correction}")
        print(f"💬 MESSAGE: {correction_message}")
        print("=" * 80)
        
        state["agent_output"] = correction_message
        return state
    
    # Handle student's response after correction
    state["_mh_tries"] = state.get("_mh_tries", 0) + 1
    
    # Check if we've reached max tries - use LLM for final conclusion
    if state["_mh_tries"] >= 2:
        context = json.dumps(PEDAGOGICAL_MOVES["MH"], indent=2)
        correction = state.get("last_correction", "the previous correction")
        
        final_system_prompt = f"""Current node: MH (Misconception Handling) - FINAL ATTEMPT
This is the final attempt to address the student's misconception.

Pedagogical context:
{context}

Original correction provided: {correction}

The student has had 2 attempts to understand the misconception correction, but may still be confused.

Task: Provide a FINAL, CLEAR explanation that:
1. Acknowledges their confusion/persistence 
2. Gives the correct concept one more time in the simplest terms
3. Concludes the misconception handling positively
4. Transitions to moving forward with assessment

Be encouraging but definitive. This is the final clarification before moving to assessment.
Respond ONLY with a clear, conclusive message (not JSON - just the message text)."""

        # Build final prompt for concluding misconception
        final_prompt = build_prompt_from_template(
            system_prompt=final_system_prompt,
            state=state,
            include_last_message=True,
            include_instructions=False,
            parser=None
        )
        
        final_response = llm_with_history(state, final_prompt).content.strip()
        
        # Add AI message to conversation
        add_ai_message_to_conversation(state, final_response)
        
        # 🔍 MH NODE - MAX TRIES REACHED 🔍
        print("=" * 80)
        print("🎯 MH NODE - MAX TRIES REACHED, LLM CONCLUSION 🎯")
        print("=" * 80)
        print(f"🔢 MH_TRIES: {state['_mh_tries']}")
        print(f"💬 LLM_FINAL_MESSAGE: {final_response}")
        print("=" * 80)
        
        state["agent_output"] = final_response
        state["current_state"] = "AR"
        return state
    
    # Normal MH processing: evaluate student's response and decide next action
    context = json.dumps(PEDAGOGICAL_MOVES["MH"], indent=2)
    correction = state.get("last_correction", "the previous correction")
    
    system_prompt = f"""Current node: MH (Misconception Handling)
Possible next_state values:
- "MH": if the student still has doubts, questions, or shows continued misconception (max 2 tries total).
- "AR": if the student shows understanding or acceptance of the correction.

Pedagogical context:
{context}

Previous correction provided: {correction}

This is attempt {state["_mh_tries"]} of 2 for misconception handling.

The student has received a correction for their misconception. Now they have responded. 
Analyze their response:
- If they seem to understand and accept the correction, move to AR
- If they have more questions, doubts, or still show misconception, provide additional clarification and stay in MH
- Be encouraging and supportive while addressing their concerns

Task: Evaluate the student's response after receiving misconception correction. Respond ONLY with JSON matching the schema above."""

    # Build final prompt using template with instructions
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=mh_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: MhResponse = mh_parser.parse(json_text)
        
        # Add AI message to conversation after successful parsing
        add_ai_message_to_conversation(state, parsed.feedback)
        
        # 🔍 MH PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 MH NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"🚀 NEXT_STATE: {parsed.next_state}")
        print(f"🔢 MH_TRIES: {state['_mh_tries']}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        state["agent_output"] = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception as e:
        print(f"Error parsing MH response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise
    
    return state

def ar_node(state: AgentState) -> AgentState:
    # First pass: generate the quiz
    if not state.get("_asked_ar", False):
        state["_asked_ar"] = True
        # Include ground truth for MCQs
        gt = get_ground_truth(concept_pkg.title, "MCQs")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (MCQs):\n{gt}\nGenerate a short quiz question (T/F, MCQ, or short answer) on '{concept_pkg.title}' and prompt the learner."
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        add_ai_message_to_conversation(state, content)

        # 🔍 AR NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 AR NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    # Second pass: grade & either explain or advance
    context = json.dumps(PEDAGOGICAL_MOVES["AR"], indent=2)
    system_prompt = f"""Current node: AR (Application & Retrieval)
Possible next_state values (handled by agent code):
- "TC": always move forward after feedback/explanation

Pedagogical context:
{context}

Task: Grade this answer on a scale from 0 to 1. Respond ONLY with JSON matching the schema above.DO NOT start with any additional text.Direct reply in requested format so I can parse directly."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=ar_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        print("#############JSON TEXT HERE",json_text)
        parsed: ArResponse = ar_parser.parse(json_text)
        
        # 🔍 AR PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 AR NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"📊 SCORE: {parsed.score}")
        print(f"🎯 SCORE_TYPE: {type(parsed.score).__name__}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        score, feedback = parsed.score, parsed.feedback
        
        # Store the quiz score in the state for metrics
        state["quiz_score"] = score * 100  # Convert 0-1 score to 0-100 percentage
    except Exception as e:
        print(f"Error parsing AR response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise

    if score < 0.5:
        # Student struggled: give correct answer + explanation, then introduce transfer
        explain_system_prompt = (
            "Provide the correct answer to the quiz question, explain why it is correct in 2–3 sentences, "
            "and then say, Nice work! Time for a transfer question."
        )
        
        # Build final prompt using template
        explain_final_prompt = build_prompt_from_template(
            system_prompt=explain_system_prompt,
            state=state,
            include_last_message=True,
            include_instructions=False
        )
            
        resp = llm_with_history(state, explain_final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content

        # 🔍 AR NODE - EXPLANATION CONTENT 🔍
        print("=" * 80)
        print("🎯 AR NODE - EXPLANATION CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
    else:
        state["agent_output"] = feedback + "\nNice work! Time for a transfer question."

    add_ai_message_to_conversation(state, state["agent_output"])

    state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    # First pass: generate the transfer question
    if not state.get("_asked_tc", False):
        state["_asked_tc"] = True
        # Include ground truth for What-if Scenarios
        gt = get_ground_truth(concept_pkg.title, "What-if Scenarios")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (What-if Scenarios):\n{gt}\nGenerate a 'what-if' or transfer question to apply '{concept_pkg.title}' in a new context."
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content

        add_ai_message_to_conversation(state, content)

        # 🔍 TC NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 TC NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    # Second pass: evaluate & either affirm or explain
    context = json.dumps(PEDAGOGICAL_MOVES["TC"], indent=2)
    system_prompt = f"""Current node: TC (Transfer & Critical Thinking)
Possible next_state values (handled by agent code):
- "RLC": always move forward after feedback/explanation

Pedagogical context:
{context}

Task: Evaluate whether the application is correct. Respond ONLY with JSON matching the schema above."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=tc_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: TcResponse = tc_parser.parse(json_text)
        
        # 🔍 TC PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 TC NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"✅ CORRECT: {parsed.correct}")
        print(f"🎯 CORRECT_TYPE: {type(parsed.correct).__name__}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        correct, feedback = parsed.correct, parsed.feedback
    except Exception as e:
        print(f"Error parsing TC response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise

    if correct:
        state["agent_output"] = feedback + "\nExcellent application! You've mastered this concept."
        add_ai_message_to_conversation(state, state["agent_output"])
    else:
        # Student struggled: give correct transfer answer + explanation
        explain_system_prompt = (
            "Provide the correct answer to the transfer question, explain why it is correct in 2–3 sentences, "
            "and then say we are proceeding to see a real-life application."
        )
        
        # Build final prompt using template
        explain_final_prompt = build_prompt_from_template(
            system_prompt=explain_system_prompt,
            state=state,
            include_last_message=True,
            include_instructions=False
        )
            
        resp = llm_with_history(state, explain_final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        add_ai_message_to_conversation(state, content)

        # 🔍 TC NODE - EXPLANATION CONTENT 🔍
        print("=" * 80)
        print("🎯 TC NODE - EXPLANATION CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content

    state["current_state"] = "RLC"
    return state

def rlc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_rlc", False):
        state["_asked_rlc"] = True
        state["_rlc_tries"] = 0  # Initialize attempt counter
        # Include ground truth for Real-Life Application
        gt = get_ground_truth(concept_pkg.title, "Real-Life Application")
        system_prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Real-Life Application):\n{gt}\nProvide a real-life application for '{concept_pkg.title}', then ask if the learner has seen or used it themselves."
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        add_ai_message_to_conversation(state, content)

        # 🔍 RLC NODE - FIRST PASS CONTENT 🔍
        print("=" * 80)
        print("🎯 RLC NODE - FIRST PASS CONTENT OUTPUT 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔧 USED_JSON_EXTRACTION: {resp.content.strip().startswith('```')}")
        print("=" * 80)
        
        state["agent_output"] = content
        return state

    # Increment attempt counter
    state["_rlc_tries"] = state.get("_rlc_tries", 0) + 1
    
    # Check if we've reached 2 attempts - if so, answer final doubts and move to END
    if state["_rlc_tries"] >= 2:
        # Include ground truth for Real-Life Application to help answer any final questions
        # gt = get_ground_truth(concept_pkg.title, "Real-Life Application")
        system_prompt = (
            f"The student has been discussing real-life applications of '{concept_pkg.title}' and this is their final interaction in this section. "
            f"Answer any remaining questions or doubts they might have about the real-life application thoroughly and helpfully. "
            "After addressing their question/doubt, conclude by saying: "
            "'Great! As a quick creative task, try drawing or explaining this idea to a friend and share what you notice. You've learned a lot today!'"
        )
        
        # Build final prompt using template
        final_prompt = build_prompt_from_template(
            system_prompt=system_prompt,
            state=state,
            include_last_message=True,
            include_instructions=False
        )
            
        resp = llm_with_history(state, final_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content

        add_ai_message_to_conversation(state, content)
        
        # 🔍 RLC NODE - FINAL ANSWER AND CONCLUSION 🔍
        print("=" * 80)
        print("🎯 RLC NODE - FINAL ANSWER AND CONCLUSION 🎯")
        print("=" * 80)
        print(f"📄 CONTENT: {content}")
        print(f"📏 CONTENT_LENGTH: {len(content)} characters")
        print(f"🔢 RLC_TRIES: {state['_rlc_tries']}")
        print("=" * 80)
        
        state["agent_output"] = content
        state["current_state"] = "END"
        return state

    context = json.dumps(PEDAGOGICAL_MOVES["RLC"], indent=2)
    system_prompt = f"""Current node: RLC (Real-Life Context)
Possible next_state values:
- "RLC": when the student is asking relevant questions about the real-life application and you want to continue the discussion.
- "END": when the student seems satisfied or has no more questions about the real-life application.

Pedagogical context:
{context}

This is attempt {state["_rlc_tries"]} for the student in the RLC node. You can stay in this node for up to 2 attempts to answer questions about the real-life application before moving to END.

Task: Evaluate whether the student has more questions about the real-life application. If they're asking relevant questions, stay in RLC. If they seem satisfied or ready to move on, go to END. Respond ONLY with JSON matching the schema above."""

    # Build final prompt using template with instructions at the end
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=rlc_parser
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: RlcResponse = rlc_parser.parse(json_text)
        
        # Add AI message to conversation after successful parsing
        add_ai_message_to_conversation(state, parsed.feedback)
        
        # 🔍 RLC PARSING OUTPUT - MAIN CONTENT 🔍
        print("=" * 80)
        print("🎯 RLC NODE - PARSED OUTPUT CONTENTS 🎯")
        print("=" * 80)
        print(f"📝 FEEDBACK: {parsed.feedback}")
        print(f"🚀 NEXT_STATE: {parsed.next_state}")
        print(f"🔢 RLC_TRIES: {state['_rlc_tries']}")
        print(f"📊 PARSED_TYPE: {type(parsed).__name__}")
        print("=" * 80)
        
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception as e:
        print(f"Error parsing RLC response: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON text: {json_text}")
        raise
    return state

def end_node(state: AgentState) -> AgentState:
    # build debug-rich summary
    state["session_summary"] = {
        "quiz_score":             state.get("retrieval_score"),
        "transfer_success":       state.get("transfer_success"),
        "definition_echoed":      state.get("definition_echoed"),
        "misconception_detected": state.get("misconception_detected"),
        "last_user_msg":          state.get("last_user_msg"),
        "history":                state.get("history"),
    }

    # 🔍 END NODE - SESSION SUMMARY 🔍
    print("=" * 80)
    print("🎯 END NODE - SESSION SUMMARY CONTENTS 🎯")
    print("=" * 80)
    print(f"📊 QUIZ_SCORE: {state['session_summary']['quiz_score']}")
    print(f"🎯 TRANSFER_SUCCESS: {state['session_summary']['transfer_success']}")
    print(f"📝 DEFINITION_ECHOED: {state['session_summary']['definition_echoed']}")
    print(f"🔍 MISCONCEPTION_DETECTED: {state['session_summary']['misconception_detected']}")
    print(f"💬 LAST_USER_MSG: {state['session_summary']['last_user_msg']}")
    print(f"📚 HISTORY_LENGTH: {len(str(state['session_summary']['history'])) if state['session_summary']['history'] else 0} characters")
    print("=" * 80)

    # final output
    state["agent_output"] = (
        "Great work today! Here's your session summary:\n"
        f"- Quiz score: {state['session_summary']['quiz_score']}\n"
        f"- Transfer success: {state['session_summary']['transfer_success']}\n"
        f"- Definition echoed: {state['session_summary']['definition_echoed']}\n"
        f"- Misconception detected: {state['session_summary']['misconception_detected']}\n"
        f"- Last user message: {state['session_summary']['last_user_msg']}"
    )
    return state
