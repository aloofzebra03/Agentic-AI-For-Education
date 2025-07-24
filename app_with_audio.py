import os
from dotenv import load_dotenv
import streamlit as st
import json
import subprocess
import onnx_asr
from scipy.io import wavfile
import numpy as np

# Import the audio_recorder component
from audio_recorder_streamlit import audio_recorder

# Load environment variables if you have a .env file
# load_dotenv()

# This is a placeholder for your agent logic.
# Ensure the 'agent' directory and 'nodes4.py' file exist and are correctly defined.
try:
    from agent.nodes4 import (
        start_node, apk_node, ci_node, ge_node,
        mh_node, ar_node, tc_node, rlc_node, end_node,
        AgentState
    )
except ImportError:
    st.error("Could not import agent nodes. Please ensure 'agent/nodes4.py' is in the correct path.")
    # Create dummy functions and state to allow the app to run for layout testing
    def placeholder_node(state):
        next_states = {"START": "APK", "END": "END"}
        state["current_state"] = next_states.get(state["current_state"], "END")
        state["agent_output"] = f"Placeholder response from {state['current_state']}. User said: '{state['last_user_msg']}'"
        if state["current_state"] == "END":
            state["session_summary"] = {"summary": "This is a placeholder summary."}
        return state
    start_node, apk_node, ci_node, ge_node, mh_node, ar_node, tc_node, rlc_node, end_node = (placeholder_node,) * 9
    class AgentState(dict): pass


# ── Load ASR model ─────────────────────────────────────────────────────────
@st.cache_resource
def load_asr_model():
    """Caches the ASR model to avoid reloading on each script run."""
    return onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v2")

asr_model = load_asr_model()
ffmpeg_path = r'C:\micromamba\envs\langchain\Library\bin\ffmpeg.exe' # Ensure this path is correct for your system

# Removed: convert_m4a_to_wav_mono function as M4A upload is gone
# Removed: transcribe_audio function as file upload is gone

def convert_to_mono_wav(input_path, output_path):
    """Converts a stereo WAV to mono. Handles potential issues with file reading."""
    try:
        sr, data = wavfile.read(input_path)
        if len(data.shape) == 2:
            data = np.mean(data, axis=1).astype(data.dtype)
        wavfile.write(output_path, sr, data)
    except Exception as e:
        st.error(f"Error converting WAV to mono: {e}")
        raise

def transcribe_recorded_audio_bytes(audio_bytes):
    """Transcribes recorded audio bytes (from audio_recorder)."""
    tmp_path = "temp_recorded.wav" # audio_recorder outputs WAV
    with open(tmp_path, 'wb') as f:
        f.write(audio_bytes) # audio_bytes is already bytes, no .read()

    mono_wav_path = "temp_recorded_mono.wav"
    transcript = None
    try:
        convert_to_mono_wav(tmp_path, mono_wav_path)
        transcript = asr_model.recognize(mono_wav_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(mono_wav_path):
            os.remove(mono_wav_path)
    return transcript


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

# ── Initialize session state ────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = AgentState({
        "current_state":        "START",
        "last_user_msg":        "",
        "history":              [],
        "definition_echoed":    False,
        "misconception_detected": False,
        "retrieval_score":      0.0,
        "transfer_success":     False,
        "session_summary":      {},
    })
    st.session_state.messages = []
    st.session_state.audio_recorder_key_counter = 0

    init_state = start_node(st.session_state.state)
    intro_message = init_state["agent_output"]
    st.session_state.state = init_state
    st.session_state.messages.append(("assistant", intro_message))
    st.session_state.state["history"].append({
        "role":    "assistant",
        "node":    "START",
        "content": intro_message
    })


st.title("🧑‍🎓 Interactive Tutor")

# Display chat history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)


# ── User Turn: only show input options if the agent is not in the END state ──
if st.session_state.state["current_state"] != "END":
    user_msg = None
    input_source = None

    st.markdown("### Respond with Audio or Text") # Simplified header

    # Use audio_recorder for primary voice input
    current_audio_recorder_key = f"audio_recorder_{st.session_state.audio_recorder_key_counter}"

    recorded_audio_bytes = audio_recorder(
        # Updated text for clarity
        text="Click to stop recording (stops automatically after 5s of inactivity)",
        auto_start=True, # Automatically starts recording when component is rendered
        pause_threshold=5.0, # Stops recording after 5 seconds of silence
        energy_threshold=(0.1, 0.4), # Tune these for better VAD. (start_threshold, end_threshold)
        key=current_audio_recorder_key,
        icon_size = "3x", # Larger icon for better visibility
    )

    if recorded_audio_bytes:
        with st.spinner("Transcribing recorded audio..."):
            try:
                user_msg = transcribe_recorded_audio_bytes(recorded_audio_bytes)
                st.success(f"Transcribed Text: {user_msg}")
                input_source = "audio_recording"
            except Exception as e:
                st.error(f"Recorded audio transcription failed: {e}")
                if os.path.exists("temp_recorded.wav"): os.remove("temp_recorded.wav")
                if os.path.exists("temp_recorded_mono.wav"): os.remove("temp_recorded_mono.wav")

    # Removed: Audio file uploader section completely

    # Text input (always display now)
    if not user_msg: # Only show text input if audio was not just provided
        user_msg = st.chat_input("Or type your response...")
        if user_msg:
            input_source = "chat_input"

    # If user responded (via any mode)
    if user_msg:
        # Increment the audio recorder key counter to force a reset on the next rerun
        st.session_state.audio_recorder_key_counter += 1
        
        # Removed: Clear specific session state keys for audio_file as it's gone
        
        # Add user message to chat and history
        st.session_state.messages.append(("user", user_msg))
        st.session_state.state["last_user_msg"] = user_msg
        st.session_state.state["history"].append({"role": "user", "content": user_msg})

        # Process user message through the agent graph
        current_node_key = st.session_state.state["current_state"]
        node_function = NODE_MAP[current_node_key]
        
        # Add a placeholder for processing to improve UX
        with st.spinner("Thinking..."):
            new_state = node_function(st.session_state.state)
            agent_reply = new_state["agent_output"]

        # Update state and add agent reply to history
        st.session_state.state = new_state
        st.session_state.messages.append(("assistant", agent_reply))
        st.session_state.state["history"].append({
            "role":    "assistant",
            "node":    new_state["current_state"],
            "content": agent_reply
        })

        st.rerun()

# If the conversation has ended, display the summary
if st.session_state.state["current_state"] == "END":
    st.markdown("---")
    st.subheader("Session Summary")
    st.json(st.session_state.state.get("session_summary", {"message": "No summary was generated."}))

    # Provide a download button for the summary
    summary_data = st.session_state.state.get("session_summary", {})
    if summary_data:
        summary_json = json.dumps(summary_data, indent=2)
        st.download_button(
            label="📥 Download Session Summary",
            data=summary_json,
            file_name="session_summary.json",
            mime="application/json",
        )
    
    # st.stop()