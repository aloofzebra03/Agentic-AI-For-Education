import os
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

from agent.nodes4 import start_node, apk_node, ci_node, ge_node, \
                         mh_node, ar_node, tc_node, rlc_node, end_node, AgentState

st.set_page_config(page_title="Interactive Tutor", page_icon="🤖")

NODE_MAP = {
    "START": start_node,
    "APK":   apk_node,
    "CI":    ci_node,
    "GE":    ge_node,
    "MH":    mh_node,
    "AR":    ar_node,
    "TC":    tc_node,
    "RLC":   rlc_node,
    "END":   end_node,
}

# ── initialize session state ────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = AgentState({
        "current_state":          "START",
        "last_user_msg":          "",
        "history":                [],
        "definition_echoed":      False,
        "misconception_detected": False,
        "retrieval_score":        0.0,
        "transfer_success":       False,
        "session_summary":        {},
    })
    st.session_state.messages = []

    # immediately invoke start_node for the intro
    initial_state = start_node(st.session_state.state)
    intro = initial_state["agent_output"]
    st.session_state.state = initial_state
    st.session_state.messages.append(("assistant", intro))
    st.session_state.state["history"].append({
        "role": "assistant",
        "node": "START",
        "content": intro
    })

# ── render chat UI ─────────────────────────────────────────────────────────
st.title("🧑‍🎓 Interactive Tutor")
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# ── handle user input ───────────────────────────────────────────────────────
if user_msg := st.chat_input("Your turn…"):
    # record user
    st.session_state.messages.append(("user", user_msg))
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.state["last_user_msg"] = user_msg
    st.session_state.state["history"].append({
        "role":    "user",
        "content": user_msg
    })

    # get bot reply
    fn = NODE_MAP[st.session_state.state["current_state"]]
    new_state = fn(st.session_state.state)
    reply = new_state["agent_output"]

    # record assistant
    st.session_state.state = new_state
    st.session_state.messages.append(("assistant", reply))
    st.session_state.state["history"].append({
        "role":    "assistant",
        "node":    new_state["current_state"],
        "content": reply
    })
    with st.chat_message("assistant"):
        st.write(reply)

    # if session ended, show summary + download
    if new_state["current_state"] == "END":
        st.markdown("---")
        st.subheader("Session Summary")
        st.json(new_state["session_summary"])

        # prepare JSON for download
        summary_json = json.dumps(new_state["session_summary"], indent=2)
        st.download_button(
            label="📥 Download Session Summary",
            data=summary_json,
            file_name="session_summary.json",
            mime="application/json"
        )
