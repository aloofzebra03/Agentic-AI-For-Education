import os
import streamlit as st
import json
import onnx_asr
from scipy.io import wavfile
import numpy as np
import tempfile
import base64
import time

# Import the audio_recorder component
from audio_recorder_streamlit import audio_recorder

# Import gTTS for text-to-speech
from gtts import gTTS

# This is a placeholder for your agent logic.
try:
    from agent.nodes4 import (
        start_node, apk_node, ci_node, ge_node,
        mh_node, ar_node, tc_node, rlc_node, end_node,
        AgentState
    )
except ImportError:
    st.error("Could not import agent nodes. Running with placeholder logic.")
    def placeholder_node(state):
        next_states = {"START": "APK", "END": "END"}
        current_node = state["current_state"]
        state["current_state"] = next_states.get(current_node, "END")
        state["agent_output"] = f"Placeholder response from '{current_node}'. You said: '{state['last_user_msg']}'"
        if state["current_state"] == "END":
            state["agent_output"] = "End of placeholder session."
            state["session_summary"] = {"summary": "This is a placeholder summary."}
        return state
    start_node, apk_node, ci_node, ge_node, mh_node, ar_node, tc_node, rlc_node, end_node = (placeholder_node,) * 9
    class AgentState(dict): pass

# ── ASR & TTS Functions ──────────────────────────────────────────────────
@st.cache_resource
def load_asr_model():
    return onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v2")

asr_model = load_asr_model()

def convert_to_mono_wav(input_path, output_path):
    try:
        sr, data = wavfile.read(input_path)
        if len(data.shape) == 2:
            data = np.mean(data, axis=1).astype(data.dtype)
        wavfile.write(output_path, sr, data)
    except Exception as e:
        st.error(f"Error converting WAV to mono: {e}")

def transcribe_recorded_audio_bytes(audio_bytes):
    tmp_path = f"temp_recorded_{time.time()}.wav"
    mono_wav_path = f"temp_mono_{time.time()}.wav"
    try:
        with open(tmp_path, 'wb') as f: f.write(audio_bytes)
        convert_to_mono_wav(tmp_path, mono_wav_path)
        return asr_model.recognize(mono_wav_path)
    finally:
        if os.path.exists(tmp_path): os.remove(tmp_path)
        if os.path.exists(mono_wav_path): os.remove(mono_wav_path)

def play_text_as_audio(text, container):
    """
    This function is now only called for the latest message, so it always includes autoplay.
    """
    if not text or not text.strip(): return
    
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.write_to_fp(tmp)
            temp_audio_file_path = tmp.name
        
        with open(temp_audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        os.remove(temp_audio_file_path)

        audio_html = f"""
        <audio controls autoplay style="width: 100%; margin-top: 5px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        container.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"TTS Error: {e}")

# ── Streamlit Page Configuration ───────────────────────────────────────────
st.set_page_config(page_title="Interactive Tutor", page_icon="🤖")

NODE_MAP = {
    "START": start_node, "APK": apk_node, "CI": ci_node, "GE": ge_node,
    "MH": mh_node, "AR": ar_node, "TC": tc_node, "RLC": rlc_node, "END": end_node,
}

# ── Welcome Screen & Session State Initialization ───────────────────────
if "session_started" not in st.session_state:
    st.title("🧑‍🎓 Interactive Tutor")
    st.info("Welcome! Please click the 'Start Learning' button to begin the session.")
    if st.button("🚀 Start Learning", type="primary"):
        st.session_state.session_started = True
        st.session_state.state = AgentState({
            "current_state": "START", "last_user_msg": "", "history": [], "session_summary": {},
        })
        st.session_state.messages = []
        st.session_state.audio_recorder_key_counter = 0

        # This runs only once after the first click
        init_state = start_node(st.session_state.state)
        intro_message = init_state.get("agent_output", "Hello! Let's begin.")
        st.session_state.state = init_state
        st.session_state.messages.append(("assistant", intro_message))
        st.session_state.state["history"].append({"role": "assistant", "node": "START", "content": intro_message})
        st.rerun()
    st.stop()

# ── Main Application Logic ───────────────────────────────────────────────

st.title("🧑‍🎓 Interactive Tutor")

# Display chat history
for i, (role, msg) in enumerate(st.session_state.messages):
    with st.chat_message(role):
        st.write(msg)
        # **THE CRITICAL FIX**: Only render an audio player for the single, most recent assistant message.
        if role == "assistant" and (i == len(st.session_state.messages) - 1):
            audio_container = st.container()
            play_text_as_audio(msg, audio_container)

# User Input Logic
if st.session_state.state["current_state"] != "END":
    user_msg = None
    recorded_audio_bytes = audio_recorder(
        text="Click the mic to speak",
        key=f"audio_recorder_{st.session_state.audio_recorder_key_counter}",
        icon_size="2x",
    )
    if recorded_audio_bytes:
        with st.spinner("Transcribing..."):
            user_msg = transcribe_recorded_audio_bytes(recorded_audio_bytes)

    text_input = st.chat_input("Or type your response here...")
    if text_input:
        user_msg = text_input

    if user_msg:
        st.session_state.audio_recorder_key_counter += 1
        st.session_state.messages.append(("user", user_msg))
        st.session_state.state["last_user_msg"] = user_msg
        st.session_state.state["history"].append({"role": "user", "content": user_msg})

        with st.spinner("Thinking..."):
            current_node_key = st.session_state.state["current_state"]
            node_function = NODE_MAP.get(current_node_key, end_node)
            new_state = node_function(st.session_state.state)
            agent_reply = new_state.get("agent_output", "I'm not sure how to respond.")
            st.session_state.state = new_state
            st.session_state.messages.append(("assistant", agent_reply))
            st.session_state.state["history"].append({
                "role": "assistant",
                "node": new_state["current_state"],
                "content": agent_reply
            })
        st.rerun()

# Session End Summary
if st.session_state.state["current_state"] == "END":
    st.markdown("---")
    st.success("🎉 Session Complete!")
    st.subheader("Session Summary")
    summary_data = st.session_state.state.get("session_summary", {"message": "No summary."})
    st.json(summary_data)
    if summary_data:
        summary_json = json.dumps(summary_data, indent=2)
        st.download_button(
            label="📥 Download Session Summary",
            data=summary_json,
            file_name="tutor_session_summary.json",
            mime="application/json",
        )