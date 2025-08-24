# agent/nodes2.py

import os
import json
from typing import Literal, Optional, Dict
import re

from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from educational_agent.config_rag import concept_pkg
from educational_agent.Creating_Section_Text.retriever import retrieve_docs
from educational_agent.Filtering_GT.filter_utils import filter_relevant_section
from educational_agent.Creating_Section_Text.schema import NextSectionChoice  # Use real schema for section_name
import dotenv
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage


dotenv.load_dotenv(dotenv_path=".env", override=True)

AgentState = dict

def extract_json_block(text: str) -> str:
    s = text.strip()

    # 1) Try to find a fenced code block containing JSON (language tag optional)
    m = re.search(r"```(?:json)?\s*({.*?})\s*```", s, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # 2) Try to find the first balanced JSON object in the text
    start = s.find("{")
    if start != -1:
        depth = 0
        in_str = False
        esc = False
        for i, ch in enumerate(s[start:], start=start):
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return s[start:i+1].strip()

    # 3) Nothing found — return original (let parser raise)
    return s


# def extract_json_block(text: str) -> str:
#     """```
#     If text starts with ```json and ends with ```, extract the JSON block.
#     Otherwise, return text unchanged.
#     """
#     pattern = r"^```json\s*(.*?)\s*```$"
#     match = re.match(pattern, text.strip(), re.DOTALL)
#     if match:
#         return match.group(1).strip()
#     return text

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
     # Build request: system instruction first, then entire past conversation
    sys_msg = SystemMessage(content=system_content)
    conversation = state.get("messages", [])

    request_msgs = [sys_msg] + conversation

    resp = get_llm().invoke(request_msgs)
    # response = llm.invoke(prompt, config={"callbacks": get_callbacks()})

    # Append model reply to persistent conversation
    state["messages"].append(AIMessage(content=resp.content))
    return resp


def get_ground_truth(concept: str, section_name: str) -> str:
    """
    Fetch relevant sections from vector store and filter by section name.
    """
    try:
        # Build a minimal NextSectionChoice object; other fields are dummy since retriever only uses section_name
        params = NextSectionChoice(
            section_name=section_name,
            difficulty=1,
            board_exam_importance=1,
            olympiad_importance=1,
            avg_study_time_min=1,
            interest_evoking=1,
            curiosity_evoking=1,
            critical_reasoning_needed=1,
            inquiry_learning_scope=1,
            example_availability=1,
        )
        docs = retrieve_docs(concept, params)
        combined = [f"# Page: {d.metadata['page_label']}\n{d.page_content}" for d in docs]
        full_doc = "\n---\n".join(combined)
        return filter_relevant_section(concept, section_name, full_doc)
    except Exception as e:
        print(f"Error retrieving ground truth for {concept} - {section_name}: {e}")
        return ""

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
        f"You are an educational agent helping a learner understand '{concept_pkg.title}'. The learner is a student of class 7. Remember that you are interacting directly with the learner.\n"
        "Greet the learner and ask if they are ready to begin."
        # "Also Remember that the student is of Kannada origin and understands olny kannada.So speak to the student in kannada.The script has to be kannada and not english.\n"
    )
    print("IN START NODE")
    resp = llm_with_history(state, prompt)
    # Apply JSON extraction in case LLM wraps response in markdown
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    state["agent_output"]  = content
    state["current_state"] = "APK"
    return state

def apk_node(state: AgentState) -> AgentState:
    if not state.get("_asked_apk", False):
        state["_asked_apk"] = True
        # Include ground truth for Concept Definition
        gt = get_ground_truth(concept_pkg.title, "Concept Definition")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Concept Definition):\n{gt}\nGenerate one hook question that activates prior knowledge for '{concept_pkg.title}'.",
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
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

If the student's reply indicates they don't know or they are stuck after two attempts, provide the correct identification and move on to the next state.

Student reply: "{state['last_user_msg']}"
Task: Evaluate whether the student identified the concept correctly. Respond ONLY with JSON matching the schema above. If not, help the student to do so.
"""
    raw = llm_with_history(state, decision_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: ApkResponse = apk_parser.parse(json_text)
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception:
        state["agent_output"]  = "Oops, I got confused. Let's try defining it.\n" + extract_json_block(raw)
        state["current_state"] = "CI"
    return state

def ci_node(state: AgentState) -> AgentState:
    # print("REACHED HERE")
    if not state.get("_asked_ci", False):
        state["_asked_ci"] = True
        # Include ground truth for Explanation (with analogies)
        gt = get_ground_truth(concept_pkg.title, "Explanation (with analogies)")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Explanation):\n{gt}\nProvide a concise definition (≤30 words) of '{concept_pkg.title}', "
            "then ask the learner to restate it."
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
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

If the student's restatement indicates they don't know or they are stuck after two attempts, provide the correct definition and move on.

Student restatement: "{state['last_user_msg']}"
Task: Determine if the restatement is accurate. Respond ONLY with JSON matching the schema above. If not, help the student to do so.
"""
    raw = llm_with_history(state, decision_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: CiResponse = ci_parser.parse(json_text)
        state["agent_output"]  = parsed.feedback
        state["current_state"] = parsed.next_state
    except Exception:
        state["agent_output"]  = "Hmm, let's move on.\n" + extract_json_block(raw)
        state["current_state"] = "GE"
    return state

def ge_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ge", False):
        state["_asked_ge"] = True
        # Include ground truth for Details (facts, sub-concepts)
        gt = get_ground_truth(concept_pkg.title, "Details (facts, sub-concepts)")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Details):\n{gt}\nGenerate one 'why' or 'how' question to explore the mechanism of '{concept_pkg.title}'.",
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
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

If the student's response indicates they don't know or are stuck after two attempts, provide the correct explanation in a concise manner and move on to the next state.

Student response: "{state['last_user_msg']}"
Task: Detect misconception or correct reasoning. RESPOND ONLY WITH JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: GeResponse = ge_parser.parse(json_text)
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
    # First pass: generate the quiz
    if not state.get("_asked_ar", False):
        state["_asked_ar"] = True
        # Include ground truth for MCQs
        gt = get_ground_truth(concept_pkg.title, "MCQs")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (MCQs):\n{gt}\nGenerate a short quiz question (T/F, MCQ, or short answer) on '{concept_pkg.title}' and prompt the learner."
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
        return state

    # Second pass: grade & either explain or advance
    instructions = ar_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["AR"], indent=2)
    decision_prompt = f"""{instructions}

Current node: AR (Application & Retrieval)
Possible next_state values (handled by agent code):
- "TC": always move forward after feedback/explanation

Pedagogical context:
{context}

Student answer: "{state['last_user_msg']}"
Task: Grade this answer on a scale from 0 to 1. Respond ONLY with JSON matching the schema above.DO NOT start with any additional text.Direct reply in requested format so I can parse directly.
"""
    raw = llm_with_history(state, decision_prompt).content
    json_text = extract_json_block(raw)
    try:
        print("#############JSON TEXT HERE",json_text)
        parsed: ArResponse = ar_parser.parse(json_text)
        score, feedback = parsed.score, parsed.feedback
    except Exception as e:
        print(e)
        score, feedback = 0.0, extract_json_block(raw)

    if score < 0.5:
        # Student struggled: give correct answer + explanation, then introduce transfer
        explain_prompt = (
            f"Student's answer: {state['last_user_msg']}\n"
            "Provide the correct answer to the quiz question, explain why it is correct in 2–3 sentences, "
            "and then say, Nice work! Time for a transfer question."
        )
        resp = llm_with_history(state, explain_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
    else:
        state["agent_output"] = feedback + "\nNice work! Time for a transfer question."

    state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    # First pass: generate the transfer question
    if not state.get("_asked_tc", False):
        state["_asked_tc"] = True
        # Include ground truth for What-if Scenarios
        gt = get_ground_truth(concept_pkg.title, "What-if Scenarios")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (What-if Scenarios):\n{gt}\nGenerate a 'what-if' or transfer question to apply '{concept_pkg.title}' in a new context."
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
        return state

    # Second pass: evaluate & either affirm or explain
    instructions = tc_parser.get_format_instructions()
    context = json.dumps(PEDAGOGICAL_MOVES["TC"], indent=2)
    decision_prompt = f"""{instructions}

Current node: TC (Transfer & Critical Thinking)
Possible next_state values (handled by agent code):
- "RLC": always move forward after feedback/explanation

Pedagogical context:
{context}

Student answer: "{state['last_user_msg']}"
Task: Evaluate whether the application is correct. Respond ONLY with JSON matching the schema above.
"""
    raw = llm_with_history(state, decision_prompt).content
    json_text = extract_json_block(raw)
    try:
        parsed: TcResponse = tc_parser.parse(json_text)
        correct, feedback = parsed.correct, parsed.feedback
    except Exception:
        correct, feedback = False, extract_json_block(raw)

    if correct:
        state["agent_output"] = feedback + "\nExcellent application! You've mastered this concept."
    else:
        # Student struggled: give correct transfer answer + explanation
        explain_prompt = (
            f"Student's answer: {state['last_user_msg']}\n"
            "Provide the correct answer to the transfer question, explain why it is correct in 2–3 sentences, "
            "and then say we are proceeding to see a real-life application."
        )
        resp = llm_with_history(state, explain_prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content

    state["current_state"] = "RLC"
    return state

def rlc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_rlc", False):
        state["_asked_rlc"] = True
        # Include ground truth for Real-Life Application
        gt = get_ground_truth(concept_pkg.title, "Real-Life Application")
        prompt = (
            f"Please use the following ground truth as a baseline and build upon it, but do not deviate too much.\n"
            f"Ground truth (Real-Life Application):\n{gt}\nProvide a real-life application for '{concept_pkg.title}', then ask if the learner has seen or used it themselves."
        )
        resp = llm_with_history(state, prompt)
        # Apply JSON extraction in case LLM wraps response in markdown
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        state["agent_output"] = content
        return state

    state["agent_output"] = (
        "Great! As a quick creative task, try drawing or explaining this idea to a friend and share what you notice."
    )
    state["current_state"] = "END"
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

    # final output
    state["agent_output"] = (
        "Great work today! Here’s your session summary:\n"
        f"- Quiz score: {state['session_summary']['quiz_score']}\n"
        f"- Transfer success: {state['session_summary']['transfer_success']}\n"
        f"- Definition echoed: {state['session_summary']['definition_echoed']}\n"
        f"- Misconception detected: {state['session_summary']['misconception_detected']}\n"
        f"- Last user message: {state['session_summary']['last_user_msg']}"
    )
    return state
