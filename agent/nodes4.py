# agent/nodes2.py

import os
import json
from typing import Literal, Optional, Dict
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from agent.config import concept_pkg
import dotenv

dotenv.load_dotenv(dotenv_path=".env", override=True)

AgentState = dict

def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Please set GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.5,
    )

def llm_with_history(state: AgentState, system_content: str):
    prior = state.setdefault("history", []).copy()
    messages = []
    for msg in prior:
        role = "human" if msg["role"] == "user" else "assistant"
        messages.append((role, msg["content"]))
    messages.append(("human", system_content))
    return get_llm().invoke(messages)

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

class ArResponse(BaseModel):
    score: float
    feedback: str

class TcResponse(BaseModel):
    correct: bool
    feedback: str

# ─── Parsers ───────────────────────────────────────────────────────────────────

apk_parser = PydanticOutputParser(pydantic_object=ApkResponse)
ci_parser  = PydanticOutputParser(pydantic_object=CiResponse)
ge_parser  = PydanticOutputParser(pydantic_object=GeResponse)
ar_parser  = PydanticOutputParser(pydantic_object=ArResponse)
tc_parser  = PydanticOutputParser(pydantic_object=TcResponse)

# ─── Pedagogical‐move context ───────────────────────────────────────────────────

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

# ─── Node definitions ───────────────────────────────────────────────────────────

def start_node(state: AgentState) -> AgentState:
    prompt = (
        f"You are an educational agent helping a learner understand '{concept_pkg.title}'. The learner is a student of class 7.\n"
        "Greet the learner and ask if they are ready to begin."
    )
    resp = llm_with_history(state, prompt)
    state["agent_output"]  = resp.content
    state["current_state"] = "APK"
    return state

def apk_node(state: AgentState) -> AgentState:
    if not state.get("_asked_apk", False):
        state["_asked_apk"] = True
        prompt = (
            f"Generate one hook question that activates prior knowledge for '{concept_pkg.title}'."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    instructions = apk_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["APK"], indent=2)
    decision_prompt = f"""{instructions}

Current node: APK (Activate Prior Knowledge)
Possible next_state values:
- "CI": when the student's reply shows they correctly identified '{concept_pkg.title}'.
- "APK": when the student's reply does not clearly identify '{concept_pkg.title}'.

Pedagogical context:
{context}

Student reply: "{state['last_user_msg']}"
Task: Evaluate whether the student identified the concept correctly. Respond ONLY with JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    try:
        parsed: ApkResponse = apk_parser.parse(raw)
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception:
        state["agent_output"]  = "Oops, I got confused. Let's try defining it.\n" + raw
        state["current_state"] = "CI"
    return state

def ci_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ci", False):
        state["_asked_ci"] = True
        prompt = (
            f"Provide a concise definition (≤30 words) of '{concept_pkg.title}', "
            "then ask the learner to restate it."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    instructions = ci_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["CI"], indent=2)
    decision_prompt = f"""{instructions}

Current node: CI (Concept Introduction)
Possible next_state values:
- "GE": when the student's paraphrase accurately captures the definition.
- "CI": when the paraphrase is inaccurate or incomplete.

Pedagogical context:
{context}

Student restatement: "{state['last_user_msg']}"
Task: Determine if the restatement is accurate. Respond ONLY with JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    try:
        parsed: CiResponse = ci_parser.parse(raw)
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception:
        state["agent_output"]  = "Hmm, let's move on.\n" + raw
        state["current_state"] = "GE"
    return state

def ge_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ge", False):
        state["_asked_ge"] = True
        prompt = (
            f"Generate one 'why' or 'how' question to explore the mechanism of '{concept_pkg.title}'."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    instructions = ge_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["GE"], indent=2)
    decision_prompt = f"""{instructions}

Current node: GE (Guided Exploration)
Possible next_state values:
- "MH": if you detect a misconception in the student's reasoning (must include a non-empty "correction" ≤2 sentences).
- "AR": if the reasoning is correct or there’s no misconception.

Pedagogical context:
{context}

Student response: "{state['last_user_msg']}"
Task: Detect misconception or correct reasoning. RESPOND ONLY WITH JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    try:
        parsed: GeResponse = ge_parser.parse(raw)
        if parsed.next_state == "MH":
            state["last_correction"] = parsed.correction or "Let me clarify that for you."
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception:
        state["agent_output"]  = "Sorry, I couldn’t interpret that—let’s move on."
        state["current_state"] = "AR"
    return state

def mh_node(state: AgentState) -> AgentState:
    if state.get("current_state") == "MH" and not state.get("_asked_mh", False):
        state["_asked_mh"] = True
        corr = state.get("last_correction", "Let me clarify that for you.")
        state["agent_output"]  = f"Good thinking! Actually, {corr}"
        state["current_state"] = "AR"
        return state
    state["current_state"] = "AR"
    return state

def ar_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ar", False):
        state["_asked_ar"] = True
        prompt = (
            f"Generate a short quiz question (T/F, MCQ, or short answer) on '{concept_pkg.title}' and prompt the learner."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    instructions = ar_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["AR"], indent=2)
    decision_prompt = f"""{instructions}

Current node: AR (Application & Retrieval)
Possible next_state values (handled by agent code):
- "CI": when the quiz score is less than 0.5.
- "TC": when the quiz score is 0.5 or greater.

Pedagogical context:
{context}

Student answer: "{state['last_user_msg']}"
Task: Grade this answer on a scale from 0 to 1. Respond ONLY with JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    try:
        parsed: ArResponse = ar_parser.parse(raw)
        score, feedback = parsed.score, parsed.feedback
    except Exception:
        score, feedback = 0.0, raw

    state["retrieval_score"] = score
    if score < 0.5:
        state["agent_output"]  = feedback
        state["current_state"] = "CI"
        state["_asked_ci"]     = False
    else:
        state["agent_output"]  = feedback + "\nNice work! Time for a transfer question."
        state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_tc", False):
        state["_asked_tc"] = True
        prompt = (
            f"Generate a 'what-if' or transfer question to apply '{concept_pkg.title}' in a new context."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    instructions = tc_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["TC"], indent=2)
    decision_prompt = f"""{instructions}

Current node: TC (Transfer & Critical Thinking)
Possible next_state values (handled by agent code):
- "RLC": when correct=true.
- "CI": when correct=false.

Pedagogical context:
{context}

Student answer: "{state['last_user_msg']}"
Task: Evaluate whether the application is correct. Respond ONLY with JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    try:
        parsed: TcResponse = tc_parser.parse(raw)
        correct, feedback = parsed.correct, parsed.feedback
    except Exception:
        correct, feedback = False, raw

    state["transfer_success"] = correct
    if correct:
        state["agent_output"]  = feedback + "\nExcellent application! You've mastered this concept."
        state["current_state"] = "RLC"
    else:
        state["agent_output"]   = feedback + "\nThat’s not quite right—let’s revisit the definition."
        state["current_state"]  = "CI"
        state["_asked_ci"]      = False
    return state

def rlc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_rlc", False):
        state["_asked_rlc"] = True
        prompt = (
            f"Provide a real-life application for '{concept_pkg.title}', then ask if the learner has seen or used it."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    state["agent_output"] = (
        "Great! As a quick creative task, try drawing or explaining this idea to a friend and share what you notice."
    )
    state["current_state"] = "END"
    return state

def end_node(state: AgentState) -> AgentState:
    recap = (
        f"Quick recap:\n"
        f"• Definition of '{concept_pkg.title}'.\n"
        f"• Quiz score: {state.get('retrieval_score')}\n"
        f"• Transfer success: {state.get('transfer_success')}"
    )
    state["agent_output"]     = recap
    state["session_summary"] = {
        "quiz_score":       state.get("retrieval_score"),
        "transfer_success": state.get("transfer_success")
    }
    return state
