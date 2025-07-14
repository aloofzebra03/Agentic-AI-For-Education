# nodes.py
import os, re
from typing_extensions import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from agent.config import concept_pkg

import dotenv
dotenv.load_dotenv(dotenv_path=".env",override=True)

AgentState = dict

def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Please set GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.5
    )

def start_node(state: AgentState) -> AgentState:
    # Always just greet once and move on
    tpl = ChatPromptTemplate.from_template(
        "Prompt the user that you are redy to teach the user about {title}.\n\n"
    )
    msg = tpl.format_messages(title=concept_pkg.title)
    resp = get_llm().invoke(msg)
    state["agent_output"] = resp.content
    state["current_state"] = "APK"
    # Reset last_user_msg so APK doesn’t accidentally see your START-reply
    state["last_user_msg"] = ""
    return state

def apk_node(state: AgentState) -> AgentState:
    # 1 Ask the swing question once
    if not state.get("_asked_apk", False):
        state["_asked_apk"] = True
        state["agent_output"] = concept_pkg.hook_question
        return state

    # Learner replied—check for “oscillatory”
    reply = state["last_user_msg"].lower()
    if "oscillatory" in reply:
        state["agent_output"] = (
            "Exactly! That’s called oscillatory motion. "
            "Great—let’s move on to the definition."
        )
        state["current_state"] = "CI"
    else:
        state["agent_output"] = (
            "Not quite—remember, a swing is doing oscillatory motion. "
            "What would you call that kind of motion?"
        )
        # stay in APK
    return state

def ci_node(state: AgentState) -> AgentState:
    # Ask for definition
    if not state.get("_asked_ci", False):
        tpl = ChatPromptTemplate.from_template(
            "Definition: {one_line_definition}\n\nHow would you restate this in your own words?"
        )
        msg = tpl.format_messages(one_line_definition=concept_pkg.one_line_definition)
        state["agent_output"] = msg[0].content
        state["_asked_ci"] = True
        return state

    # Learner restated → echo back via LLM
    resp = get_llm().invoke([
        {"role": "user", "content": state["last_user_msg"]},
        {"role": "system", "content":
            f"Here’s a corrected version of that definition:\n\n{concept_pkg.one_line_definition}"
        }
    ])
    state["agent_output"] = resp.content
    state["definition_echoed"] = True
    state["current_state"] = "GE"
    return state

def ge_node(state: AgentState) -> AgentState:
    # Ask the mechanism question
    if not state.get("_asked_ge", False):
        state["agent_output"] = concept_pkg.mechanism_question
        state["_asked_ge"] = True
        return state

    # Check for misconceptions
    reply = state["last_user_msg"].lower()
    if any(m.lower() in reply for m in concept_pkg.common_misconceptions):
        state["agent_output"] = concept_pkg.misconception_correction
        state["misconception_detected"] = True
        state["current_state"] = "MH"
    else:
        state["agent_output"] = concept_pkg.real_life_fact
        state["misconception_detected"] = False
        state["current_state"] = "AR"
    return state

def mh_node(state: AgentState) -> AgentState:
    # If a misconception was detected, this runs automatically
    if state["misconception_detected"] and not state.get("_asked_mh", False):
        state["agent_output"] = (
            "Let me unpack that misconception:\n\n" +
            concept_pkg.misconception_correction
        )
        state["_asked_mh"] = True
        return state

    # After correction, move to active recall
    state["current_state"] = "AR"
    return state

def ar_node(state: AgentState) -> AgentState:
    # Ask a retrieval practice question
    if not state.get("_asked_ar", False):
        tpl = ChatPromptTemplate.from_template(
            "Please generate a short quiz question on **{title}** and prompt the learner to answer."
        )
        msg = tpl.format_messages(title=concept_pkg.title)
        resp = get_llm().invoke(msg)
        state["agent_output"] = resp.content
        state["_asked_ar"] = True
        return state

    # Score their answer (yes/no or free-text)
    # Here we do a quick LLM “grade”:  
    grade = get_llm().invoke([
        {"role": "user", "content": state["last_user_msg"]},
        {"role": "system", "content":
            "On a scale of 0–1, how correct is the above answer?"
        }
    ])
    try:
        score = float(re.search(r"[0-1]\.\d+", grade.content).group())
    except:
        score = 0.0
    state["retrieval_score"] = score

    # Branch on performance
    if score < 0.5:
        state["agent_output"] = "Let’s review that again."
        state["current_state"] = "CI"
    else:
        state["agent_output"] = "Nice work! Time for a transfer question."
        state["current_state"] = "TC"
    return state

def tc_node(state: AgentState) -> AgentState:
    # 1️⃣ Ask transfer question
    if not state.get("_asked_tc", False):
        state["agent_output"] = concept_pkg.transfer_question
        state["_asked_tc"] = True
        return state

    # 2️⃣ Check their transfer answer with LLM
    resp = get_llm().invoke([
        {"role": "user", "content": state["last_user_msg"]},
        {"role": "system", "content":
            "Does this answer correctly apply the concept? Yes or No."
        }
    ])
    if "yes" in resp.content.lower():
        state["transfer_success"] = True
        state["agent_output"] = "Excellent application! You’ve mastered this concept."
    else:
        state["transfer_success"] = False
        state["agent_output"] = "That’s not quite right—let’s revisit the definition."
        state["current_state"] = "CI"
        return state

    # 3️⃣ Move on to creative task
    state["current_state"] = "RLC"
    return state

def rlc_node(state: AgentState) -> AgentState:
    # 1️⃣ Ask if they’ve seen a real-life case
    if not state.get("_asked_rlc", False):
        state["agent_output"] = "Have you seen this in real life? (Yes/No)"
        state["_asked_rlc"] = True
        return state

    # 2️⃣ Branch on their reply
    if state["last_user_msg"].lower().startswith("y"):
        state["agent_output"] = "Great—let’s do a creative task now."
        state["current_state"] = "RCT"
    else:
        state["agent_output"] = (
            "No worries—I’ll give you a quick real-life example:\n" +
            concept_pkg.real_life_fact
        )
        state["current_state"] = "RCT"
    return state

def rct_node(state: AgentState) -> AgentState:
    # Creative task → then end
    state["agent_output"] = (
        "As a creative task, try drawing the pendulum path and share insights!"
    )
    state["current_state"] = "END"
    return state

def end_node(state: AgentState) -> AgentState:
    state["agent_output"] = "Great work today! Here's a quick recap…"
    state["session_summary"] = {
        "prior_knowledge": state.get("prior_knowledge"),
        "quiz_score": state.get("retrieval_score"),
        "transfer": state.get("transfer_success")
    }
    return state
