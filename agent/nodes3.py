# agent/nodes2.py
import os
import json
from typing_extensions import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.config import concept_pkg

AgentState = dict

import dotenv
dotenv.load_dotenv(dotenv_path=".env", override=True)

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
        if msg["role"] == "user":
            messages.append(("human", msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(("assistant", msg["content"]))
    messages.append(("human", system_content))
    return get_llm().invoke(messages)

def start_node(state: AgentState) -> AgentState:
    system_content = (
        f'''You are an educational agent helping a learner understand the concept of {concept_pkg.title} for a student of class 7.\n This is the first interaction.\n\n with the student.
        Greet the learner and ask then whether they are ready to start learning about {concept_pkg.title}.\n\n'''
    )
    resp = llm_with_history(state, system_content)
    state["agent_output"]  = resp.content
    state["current_state"] = "APK"
    return state

def apk_node(state: AgentState) -> AgentState:
    if not state.get("_asked_apk", False):
        state["_asked_apk"] = True
        prompt = (
            f"Generate a thought-provoking hook question to activate prior knowledge "
            f"for the concept '{concept_pkg.title}'.Ensure you don't generate any other useless markers commas etc.\n"
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    reply = state["last_user_msg"]
    prompt = (
        f"Student reply: \"{reply}\"\n"
        f"Evaluate whether this reply correctly identifies the concept '{concept_pkg.title}'.\n"
        "Respond ONLY with a JSON object:\n"
        "{\n"
        "  \"feedback\": <short response to student>,\n"
        "  \"next_state\": \"CI\" or \"APK\"\n"
        "}"
        "Ensure you start directly with the given schema and do not generate anything other than the pure json object because I will be parsing it later.\n" \
        "Do not start with '''json or ```json or any other markers.\n" \
    )
    resp = llm_with_history(state, prompt)
    # Parse the response as JSON
    resp_content = resp.content.strip()
    if resp_content.startswith("```json"):
        resp_content = resp_content.removeprefix("```json").strip()
    if resp_content.endswith("```"):
        resp_content = resp_content.removesuffix("```").strip()
    try:
        result = json.loads(resp_content)
        state["agent_output"]  = result["feedback"]
        state["current_state"] = result["next_state"]
    except:
        # fallback: assume correct
        state["agent_output"]  = resp.content
        state["current_state"] = "CI"
    return state

def ci_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ci", False):
        state["_asked_ci"] = True
        prompt = (
            f"Provide a concise definition (≤30 words) of '{concept_pkg.title}', "
            "then ask the learner to restate it in their own words."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    reply = state["last_user_msg"]
    prompt = (
        f"Student restatement: \"{reply}\"\n"
        f"Evaluate whether this restatement accurately captures the definition of "
        f"'{concept_pkg.title}'.\n"
        "Respond ONLY with a JSON object:\n"
        "{\n"
        "  \"feedback\": <brief feedback>,\n"
        "  \"next_state\": \"GE\" or \"CI\"\n"
        "}"
    )
    resp = llm_with_history(state, prompt)
    try:
        result = json.loads(resp.content)
        state["agent_output"]  = result["feedback"]
        state["current_state"] = result["next_state"]
    except:
        state["agent_output"]  = resp.content
        state["current_state"] = "GE"
    return state

def ge_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ge", False):
        state["_asked_ge"] = True
        prompt = (
            f"Generate a 'why' or 'how' question to help the learner explore the "
            f"mechanism behind '{concept_pkg.title}'. Only output the question."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    reply = state["last_user_msg"]
    prompt = (
        f"Student response: \"{reply}\"\n"
        f"Analyze for misconceptions or correct reasoning about '{concept_pkg.title}'.\n"
        "Respond ONLY with a JSON object:\n"
        "{\n"
        "  \"feedback\": <gentle hint or affirmation>,\n"
        "  \"next_state\": \"MH\" or \"AR\",\n"
        "  \"correction\": <if MH, brief correction; otherwise omit>\n"
        "}"
    )
    resp = llm_with_history(state, prompt)
    try:
        result = json.loads(resp.content)
        state["agent_output"]  = result["feedback"]
        state["current_state"] = result["next_state"]
        if result.get("correction"):
            state["last_correction"] = result["correction"]
    except:
        state["agent_output"]  = resp.content
        state["current_state"] = "AR"
    return state

def mh_node(state: AgentState) -> AgentState:
    if state.get("current_state") == "MH" and not state.get("_asked_mh", False):
        state["_asked_mh"] = True
        corr = state.get("last_correction", "")
        state["agent_output"] = f"Good thinking! Actually, {corr}"
        return state
    state["current_state"] = "AR"
    return state

def ar_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ar", False):
        state["_asked_ar"] = True
        prompt = (
            f"Please generate a short quiz question (T/F, MCQ, or short answer) "
            f"on '{concept_pkg.title}' and prompt the learner."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    reply = state["last_user_msg"]
    prompt = (
        f"Student answer: \"{reply}\"\n"
        "Grade this answer on a scale from 0 to 1 for accuracy. Respond ONLY with JSON:\n"
        "{\n"
        "  \"score\": <float 0–1>,\n"
        "  \"feedback\": <brief feedback>\n"
        "}"
    )
    resp = llm_with_history(state, prompt)
    try:
        result = json.loads(resp.content)
        score    = result["score"]
        feedback = result["feedback"]
    except:
        score, feedback = 0.0, resp.content

    state["retrieval_score"] = score
    if score < 0.5:
        state["agent_output"]  = feedback
        state["current_state"] = "CI"
    else:
        state["agent_output"]  = feedback + "\nNice work! Time for a transfer question."
        state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_tc", False):
        state["_asked_tc"] = True
        prompt = (
            f"Generate a 'what-if' or transfer question to test applying "
            f"'{concept_pkg.title}' in a new context."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    reply = state["last_user_msg"]
    prompt = (
        f"Student answer: \"{reply}\"\n"
        "Evaluate if this applies the concept correctly. Respond ONLY with JSON:\n"
        "{\n"
        "  \"correct\": true or false,\n"
        "  \"feedback\": <brief feedback>\n"
        "}"
    )
    resp = llm_with_history(state, prompt)
    try:
        result = json.loads(resp.content)
        correct  = result["correct"]
        feedback = result["feedback"]
    except:
        correct, feedback = False, resp.content

    state["transfer_success"] = correct
    if correct:
        state["agent_output"]  = feedback + "\nExcellent application! You've mastered this concept."
        state["current_state"] = "RLC"
    else:
        state["agent_output"]  = feedback + "\nThat’s not quite right—let’s revisit the definition."
        state["current_state"] = "CI"
    return state

def rlc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_rlc", False):
        state["_asked_rlc"] = True
        prompt = (
            f"Provide a real-life application or context for '{concept_pkg.title}', "
            "then ask the learner if they've seen or used it themselves."
        )
        resp = llm_with_history(state, prompt)
        state["agent_output"] = resp.content
        return state

    state["agent_output"]     = (
        "Great! As a quick creative task, try drawing or explaining this idea "
        "to a friend and share what you notice."
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
