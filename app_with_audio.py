import os
from dotenv import load_dotenv
import streamlit as st
import json
import subprocess
import onnx_asr
from scipy.io import wavfile
import numpy as np

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

def convert_m4a_to_wav_mono(input_path, output_path):
    """Converts M4A to mono WAV using ffmpeg."""
    subprocess.run([
        ffmpeg_path,
        '-i', input_path,
        '-ac', '1',    # Set audio channels to 1 (mono)
        '-y',          # Overwrite output file if it exists
        output_path
    ], check=True, capture_output=True, text=True)

def convert_to_mono_wav(input_path, output_path):
    """Converts a stereo WAV to mono."""
    sr, data = wavfile.read(input_path)
    if len(data.shape) == 2:
        data = np.mean(data, axis=1).astype(data.dtype)
    wavfile.write(output_path, sr, data)

def transcribe_audio(audio_file):
    """Transcribes an uploaded audio file (M4A or WAV)."""
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    tmp_path = f"temp_upload{file_extension}"
    with open(tmp_path, 'wb') as f:
        f.write(audio_file.read())

    mono_wav_path = "temp_audio_mono.wav"
    try:
        if file_extension == ".m4a":
            convert_m4a_to_wav_mono(tmp_path, mono_wav_path)
        elif file_extension == ".wav":
            convert_to_mono_wav(tmp_path, mono_wav_path)
        else:
            raise ValueError("Unsupported file format. Upload .m4a or .wav files.")

        transcript = asr_model.recognize(mono_wav_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(mono_wav_path):
            os.remove(mono_wav_path)
    return transcript

def transcribe_recorded_audio(audio_bytes):
    """Transcribes recorded audio bytes."""
    tmp_path = "temp_recorded.wav"
    with open(tmp_path, 'wb') as f:
        f.write(audio_bytes.read())

    mono_wav_path = "temp_recorded_mono.wav"
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
    st.markdown("### Respond with Audio (Upload/Record) or Text")

    user_msg = None
    input_source = None # To track which widget provided the input

    # Audio file uploader
    audio_file = st.file_uploader("Upload an Audio file (.m4a or .wav)", type=["m4a", "wav"], key="audio_file")
    if audio_file:
        with st.spinner("Transcribing uploaded audio..."):
            try:
                user_msg = transcribe_audio(audio_file)
                st.success(f"Transcribed Text: {user_msg}")
                input_source = "audio_file"
            except Exception as e:
                st.error(f"Audio file transcription failed: {e}")

    # Audio recording
    audio_bytes = st.audio_input("Record your voice", key="audio_recording")
    if audio_bytes:
        with st.spinner("Transcribing recorded audio..."):
            try:
                user_msg = transcribe_recorded_audio(audio_bytes)
                st.success(f"Transcribed Text: {user_msg}")
                input_source = "audio_recording"
            except Exception as e:
                st.error(f"Recorded audio transcription failed: {e}")

    # Text input
    if not user_msg:
        user_msg = st.chat_input("Type your response...")
        if user_msg:
            input_source = "chat_input"

    # If user responded (via any mode)
    if user_msg:
        # **THE FIX**: Delete the key from session state. This is the correct
        # way to reset a widget's value for the next script run.
        if input_source == "audio_file" and "audio_file" in st.session_state:
            del st.session_state.audio_file
        if input_source == "audio_recording" and "audio_recording" in st.session_state:
            del st.session_state.audio_recording
        
        # Add user message to chat and history
        st.session_state.messages.append(("user", user_msg))
        st.session_state.state["last_user_msg"] = user_msg
        st.session_state.state["history"].append({"role": "user", "content": user_msg})

        # Process user message through the agent graph
        current_node_key = st.session_state.state["current_state"]
        node_function = NODE_MAP[current_node_key]
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

        # Rerun to update the display and wait for the next input.
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
    
    st.stop()