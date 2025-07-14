# agent/nodes.py
import os
import re
from typing_extensions import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.config import concept_pkg

AgentState = dict

import dotenv
dotenv.load_dotenv(dotenv_path=".env",override=True)

def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Please set GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.5
    )

def llm_with_history(state: AgentState, system_content: str):
    prior = state.setdefault("history", []).copy()

    message_list = []
    for msg in prior:
        if msg["role"] == "user":
            message_list.append(("human", msg["content"]))
        elif msg["role"] == "assistant":
            message_list.append(("assistant", msg["content"]))
        # ignore any system messages

    # Append the new prompt as a human message
    message_list.append(("human", system_content))

    # Invoke Gemini with the tuple list
    return get_llm().invoke(message_list)


def start_node(state: AgentState) -> AgentState:
    system_content = (
        f'''You are an educational agent helping a learner understand the concept of {concept_pkg.title}.\n This is the first interaction.\n\n with the student.
        Greet the learner and ask then whether they are ready to start learning about {concept_pkg.title}.\n\n'''
    )
    resp = llm_with_history(state, system_content)
    state["agent_output"]   = resp.content
    state["current_state"]  = "APK"
    state["last_user_msg"]  = ""
    return state

def apk_node(state: AgentState) -> AgentState:
    if not state.get("_asked_apk", False):
        state["_asked_apk"]    = True
        state["agent_output"]  = concept_pkg.hook_question
        return state

    reply = state["last_user_msg"].lower()
    if "oscillatory" in reply:
        state["agent_output"]  = (
            "Exactly—that’s oscillatory motion! Now let’s look at a crisp definition."
        )
        state["current_state"] = "CI"
    else:
        state["agent_output"]  = (
            "Not quite—remember, a swing moves back and forth. "
            "What would you call that motion?"
        )
    return state

def ci_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ci", False):
        state["_asked_ci"]    = True
        system_content        = (
            f"Definition: {concept_pkg.one_line_definition}\n\n"
            "How would you restate that in your own words?"
        )
        resp                  = llm_with_history(state, system_content)
        state["agent_output"] = resp.content
        return state

    system_content        = (
        f"Here’s a corrected version of that definition:\n\n"
        f"{concept_pkg.one_line_definition}"
    )
    resp                  = llm_with_history(state, system_content)
    state["agent_output"] = resp.content
    state["definition_echoed"] = True
    state["current_state"]    = "GE"
    return state

def ge_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ge", False):
        state["_asked_ge"]    = True
        state["agent_output"] = concept_pkg.mechanism_question
        return state

    reply = state["last_user_msg"].lower()
    if any(m.lower() in reply for m in concept_pkg.common_misconceptions):
        state["agent_output"]        = concept_pkg.misconception_correction
        state["misconception_detected"] = True
        state["current_state"]       = "MH"
    else:
        state["agent_output"]        = concept_pkg.real_life_fact
        state["misconception_detected"] = False
        state["current_state"]       = "AR"
    return state

def mh_node(state: AgentState) -> AgentState:
    if state.get("misconception_detected", False) and not state.get("_asked_mh", False):
        state["_asked_mh"]    = True
        state["agent_output"] = (
            "Good thinking! Actually, here’s the correction:\n\n"
            + concept_pkg.misconception_correction
        )
        return state

    state["current_state"] = "AR"
    return state

def ar_node(state: AgentState) -> AgentState:
    if not state.get("_asked_ar", False):
        state["_asked_ar"]   = True
        system_content       = (
            f"Please generate a short quiz question on **{concept_pkg.title}** "
            "and prompt the learner to answer."
        )
        resp                 = llm_with_history(state, system_content)
        state["agent_output"]= resp.content
        return state

    system_content = "On a scale of 0–1, how correct is the above answer?"
    grade          = llm_with_history(state, system_content)
    try:
        score = float(re.search(r"[0-1]\.\d+", grade.content).group())
    except:
        score = 0.0
    state["retrieval_score"] = score

    if score < 0.5:
        state["agent_output"]  = "Let’s review that again."
        state["current_state"] = "CI"
    else:
        state["agent_output"]  = "Nice work! Time for a transfer question."
        state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_tc", False):
        state["_asked_tc"]    = True
        state["agent_output"] = concept_pkg.transfer_question
        return state

    system_content = "Does this answer correctly apply the concept? Yes or No."
    resp           = llm_with_history(state, system_content)
    if "yes" in resp.content.lower():
        state["transfer_success"] = True
        state["agent_output"]     = "Excellent application! You’ve mastered this concept."
    else:
        state["transfer_success"] = False
        state["agent_output"]     = "That’s not quite right—let’s revisit the definition."
        state["current_state"]    = "CI"
        return state

    state["current_state"] = "RLC"
    return state

def rlc_node(state: AgentState) -> AgentState:
    if not state.get("_asked_rlc", False):
        state["_asked_rlc"]    = True
        state["agent_output"]  = (
            f"{concept_pkg.real_life_fact}\n\n"
            "Have you ever noticed or used this yourself?"
        )
        return state

    state["agent_output"]  = (
        "Great! As a creative task, try drawing or explaining this idea "
        "to a friend and share what you notice."
    )
    state["current_state"] = "END"
    return state

def end_node(state: AgentState) -> AgentState:
    recap = (
        f"• {concept_pkg.one_line_definition}\n"
        f"• {concept_pkg.mechanism_question} answered\n"
        f"• Your quiz score: {state.get('retrieval_score')}"
    )
    state["agent_output"] = recap
    state["session_summary"] = {
        "quiz_score":      state.get("retrieval_score"),
        "transfer_success": state.get("transfer_success"),
    }
    return state
