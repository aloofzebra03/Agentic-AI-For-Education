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
    sr, data = wavfile.read(input_path)
    if len(data.shape) == 2:
        data = np.mean(data, axis=1).astype(data.dtype)
    wavfile.write(output_path, sr, data)

def transcribe_recorded_audio_bytes(audio_bytes):
    tmp_path = f"temp_recorded_{time.time()}.wav"
    mono_wav_path = f"temp_mono_{time.time()}.wav"
    try:
        with open(tmp_path, 'wb') as f:
            f.write(audio_bytes)
        convert_to_mono_wav(tmp_path, mono_wav_path)
        return asr_model.recognize(mono_wav_path)
    finally:
        if os.path.exists(tmp_path): os.remove(tmp_path)
        if os.path.exists(mono_wav_path): os.remove(mono_wav_path)

def play_text_as_audio_autoplay(text, audio_placeholder_container):
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

        audio_id = f"audio_player_{int(time.time() * 1000)}"
        audio_html = f"""
        <audio id="{audio_id}" controls autoplay style="width: 100%; margin-top: 5px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        audio_placeholder_container.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"TTS Error: {e}")

# ── Streamlit Page Configuration ───────────────────────────────────────────
st.set_page_config(page_title="Interactive Tutor", page_icon="🤖")

NODE_MAP = {
    "START": start_node, "APK": apk_node, "CI": ci_node, "GE": ge_node,
    "MH": mh_node, "AR": ar_node, "TC": tc_node, "RLC": rlc_node, "END": end_node,
}

# ── Session State Initialization ───────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = AgentState({
        "current_state": "START", "last_user_msg": "", "history": [],
        "definition_echoed": False, "misconception_detected": False,
        "retrieval_score": 0.0, "transfer_success": False, "session_summary": {},
    })
    st.session_state.messages = []
    st.session_state.audio_recorder_key_counter = 0
    st.session_state.processing_audio = False # New flag for two-phase render

    init_state = start_node(st.session_state.state)
    intro_message = init_state.get("agent_output", "Hello! Let's begin.")
    st.session_state.state = init_state
    st.session_state.messages.append(("assistant", intro_message))
    st.session_state.state["history"].append({
        "role": "assistant", "node": "START", "content": intro_message
    })

# ── PHASE 2: Process the request after the "Silence" render has occurred ──
if st.session_state.processing_audio:
    with st.spinner("Thinking..."):
        # This code now runs on the second rerun, while the user sees a silent page
        current_node_key = st.session_state.state["current_state"]
        node_function = NODE_MAP.get(current_node_key, end_node)
        
        # Perform slow agent and TTS generation
        new_state = node_function(st.session_state.state)
        agent_reply = new_state.get("agent_output", "I'm not sure how to respond.")

        # Update state and history
        st.session_state.state = new_state
        st.session_state.messages.append(("assistant", agent_reply))
        st.session_state.state["history"].append({
            "role": "assistant",
            "node": new_state["current_state"],
            "content": agent_reply
        })

        # CRUCIAL: Reset the flag and trigger the final "Reveal" render
        st.session_state.processing_audio = False
        st.rerun()

# ── Main Page Rendering Logic ───────────────────────────────────────────────
st.title("🧑‍🎓 Interactive Tutor")

# Display chat history
for i, (role, msg) in enumerate(st.session_state.messages):
    with st.chat_message(role):
        st.write(msg)
        # Only render audio for the last message AND if we are NOT in the processing phase
        if role == "assistant" and not st.session_state.processing_audio and (i == len(st.session_state.messages) - 1):
            audio_container = st.empty()
            play_text_as_audio_autoplay(msg, audio_container)

# ── User Input Logic ───────────────────────────────────────────────────────
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
            st.info(f"You said: {user_msg}")

    text_input = st.chat_input("Or type your response here...")
    if text_input:
        user_msg = text_input

    # ── PHASE 1: Acknowledge input and trigger the "Silence" render ───────
    if user_msg:
        st.session_state.audio_recorder_key_counter += 1
        
        # Add user message to history immediately
        st.session_state.messages.append(("user", user_msg))
        st.session_state.state["last_user_msg"] = user_msg
        st.session_state.state["history"].append({"role": "user", "content": user_msg})

        # CRUCIAL: Set the flag and trigger the "Silence" rerun.
        # This will redraw the page without the old audio player before we do any slow work.
        st.session_state.processing_audio = True
        st.rerun()

# ── Session End Summary ────────────────────────────────────────────────────
if st.session_state.state["current_state"] == "END" and not st.session_state.processing_audio:
    st.markdown("---")
    st.success("🎉 Session Complete!")
    st.subheader("Session Summary")
    
    summary_data = st.session_state.state.get("session_summary", {"message": "No summary was generated."})
    st.json(summary_data)

    if summary_data:
        summary_json = json.dumps(summary_data, indent=2)
        st.download_button(
            label="📥 Download Session Summary",
            data=summary_json,
            file_name="tutor_session_summary.json",
            mime="application/json",
        )