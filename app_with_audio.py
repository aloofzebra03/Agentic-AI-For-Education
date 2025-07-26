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
# The app will run with placeholder logic if agent/nodes4.py is not found.
try:
    from agent.nodes4 import (
        start_node, apk_node, ci_node, ge_node,
        mh_node, ar_node, tc_node, rlc_node, end_node,
        AgentState
    )
except ImportError:
    st.error("Could not import agent nodes. Please ensure 'agent/nodes4.py' is in the correct path. Running with placeholder logic.")
    # Create dummy functions and state to allow the app to run
    def placeholder_node(state):
        next_states = {"START": "APK", "END": "END"}
        current_node = state["current_state"]
        state["current_state"] = next_states.get(current_node, "END")
        state["agent_output"] = f"This is a placeholder response from the '{current_node}' node. You said: '{state['last_user_msg']}'"
        if state["current_state"] == "END":
            state["agent_output"] = "This is the end of the placeholder session."
            state["session_summary"] = {"summary": "This is a placeholder summary from the placeholder agent."}
        return state
    start_node, apk_node, ci_node, ge_node, mh_node, ar_node, tc_node, rlc_node, end_node = (placeholder_node,) * 9
    class AgentState(dict): pass


# ── Load ASR model ─────────────────────────────────────────────────────────
@st.cache_resource
def load_asr_model():
    """Caches the ASR model to avoid reloading on each script run."""
    return onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v2")

asr_model = load_asr_model()

def convert_to_mono_wav(input_path, output_path):
    """Converts a stereo WAV to mono."""
    try:
        sr, data = wavfile.read(input_path)
        if len(data.shape) == 2:
            data = np.mean(data, axis=1).astype(data.dtype)
        wavfile.write(output_path, sr, data)
    except Exception as e:
        st.error(f"Error converting WAV to mono: {e}")
        raise

def transcribe_recorded_audio_bytes(audio_bytes):
    """Transcribes recorded audio bytes from audio_recorder."""
    tmp_path = f"temp_recorded_{time.time()}.wav"
    with open(tmp_path, 'wb') as f:
        f.write(audio_bytes)

    mono_wav_path = f"temp_mono_{time.time()}.wav"
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

# ── Text-to-Speech Function (Corrected Version) ──────────────────────────
def play_text_as_audio_autoplay(text, audio_placeholder_container, autoplay=False):
    """
    Converts text to speech and creates an HTML5 audio player.
    Autoplays ONLY if the flag is True and browser permission is granted.
    """
    if not text or not text.strip():
        return

    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.write_to_fp(tmp)
            temp_audio_file_path = tmp.name

        with open(temp_audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        os.remove(temp_audio_file_path)

        autoplay_attribute = "autoplay" if autoplay else ""
        audio_id = f"audio_player_{int(time.time() * 1000)}_{hash(text)}"

        audio_html = f"""
        <audio id="{audio_id}" controls {autoplay_attribute} style="width: 100%; margin-top: 5px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <script>
            (function() {{
                var audio = document.getElementById("{audio_id}");
                var hasPermission = sessionStorage.getItem('audioAutoplayEnabled') === 'true';
                var shouldAutoplay = {str(autoplay).lower()};

                if (audio && shouldAutoplay && hasPermission) {{
                    var playPromise = audio.play();
                    if (playPromise !== undefined) {{
                        playPromise.catch(error => {{
                            console.error("Autoplay was prevented: ", error);
                        }});
                    }}
                }}
            }})();
        </script>
        """
        audio_placeholder_container.markdown(audio_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"TTS Error: Could not generate audio. {e}")

# ── Streamlit Page Configuration ───────────────────────────────────────────
st.set_page_config(page_title="Interactive Tutor", page_icon="🤖")

NODE_MAP = {
    "START": start_node, "APK": apk_node, "CI": ci_node, "GE": ge_node,
    "MH": mh_node, "AR": ar_node, "TC": tc_node, "RLC": rlc_node, "END": end_node,
}

# ── Initial Interaction / Welcome Screen ───────────────────────────────────
if "first_interaction_done" not in st.session_state:
    st.title("🧑‍🎓 Interactive Tutor")
    st.info("Welcome! To enable voice communication, please click the button below to start the session.")

    if st.button("🚀 Start Learning", type="primary"):
        st.session_state.first_interaction_done = True
        st.rerun()

    st.stop()

# ── Main Application Logic ───────────────────────────────────────────────

# Initialize session state for the agent if not already done
if "state" not in st.session_state:
    st.session_state.state = AgentState({
        "current_state": "START", "last_user_msg": "", "history": [],
        "definition_echoed": False, "misconception_detected": False,
        "retrieval_score": 0.0, "transfer_success": False, "session_summary": {},
    })
    st.session_state.messages = []
    st.session_state.audio_recorder_key_counter = 0

    with st.spinner("Initializing tutor..."):
        init_state = start_node(st.session_state.state)
        intro_message = init_state.get("agent_output", "Hello! Let's begin.")
        st.session_state.state = init_state
        st.session_state.messages.append(("assistant", intro_message))
        st.session_state.state["history"].append({
            "role": "assistant", "node": "START", "content": intro_message
        })

st.title("🧑‍🎓 Interactive Tutor")

# Global autoplay enabler button
st.markdown("""
<div style="background: #e8f4fd; padding: 10px; border-radius: 8px; margin-bottom: 1rem;">
    <span>🔊 <b>Audio Control:</b></span>
    <button onclick="enableGlobalAutoplay()" id="global-autoplay-btn"
            style="background: #28a745; color: white; border: none; padding: 5px 15px; border-radius: 4px; cursor: pointer;">
        🔓 Enable Auto-Audio
    </button>
    <span id="autoplay-status" style="font-size: 12px; color: #666; margin-left: 10px;">Click to allow automatic audio playback.</span>
</div>
<script>
    function enableGlobalAutoplay() {
        var btn = document.getElementById('global-autoplay-btn');
        var status = document.getElementById('autoplay-status');
        var silentAudio = new Audio('data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAVFYAAFRWAAABAAgAZGF0YQAAAAA='); // Short silent audio
        
        silentAudio.play().then(() => {
            sessionStorage.setItem('audioAutoplayEnabled', 'true');
            btn.innerHTML = '✅ Auto-Audio Enabled';
            btn.disabled = true;
            btn.style.background = '#6c757d';
            status.innerHTML = 'All new responses will now play automatically!';
            status.style.color = '#28a745';
        }).catch(error => {
            btn.innerHTML = '❌ Permission Denied';
            btn.style.background = '#dc3545';
            status.innerHTML = 'Browser blocked autoplay. Please check site settings.';
            status.style.color = '#dc3545';
        });
    }
    if (sessionStorage.getItem('audioAutoplayEnabled') === 'true') {
        enableGlobalAutoplay();
    }
</script>
""", unsafe_allow_html=True)

# Display chat history (with corrected audio player logic)
for i, (role, msg) in enumerate(st.session_state.messages):
    with st.chat_message(role):
        st.write(msg)
        # ONLY create an audio player for the MOST RECENT assistant message.
        if role == "assistant" and (i == len(st.session_state.messages) - 1):
            audio_container = st.empty()
            play_text_as_audio_autoplay(
                text=msg,
                audio_placeholder_container=audio_container,
                autoplay=True
            )

# ── User Input Logic ──────────────────────────────────────────────────────
if st.session_state.state["current_state"] != "END":
    user_msg = None

    recorded_audio_bytes = audio_recorder(
        text="Click the mic to speak",
        key=f"audio_recorder_{st.session_state.audio_recorder_key_counter}",
        icon_size="2x",
    )

    if recorded_audio_bytes:
        with st.spinner("Transcribing your audio..."):
            try:
                user_msg = transcribe_recorded_audio_bytes(recorded_audio_bytes)
                st.info(f"You said: {user_msg}")
            except Exception as e:
                st.error(f"Audio transcription failed: {e}")

    text_input = st.chat_input("Or type your response here...")
    if text_input:
        user_msg = text_input

    if user_msg:
        # **FIX FOR TIMING ISSUE**: Immediately pause any currently playing audio.
        st.markdown("<script>document.querySelectorAll('audio').forEach(a => a.pause());</script>", unsafe_allow_html=True)
        
        st.session_state.audio_recorder_key_counter += 1

        st.session_state.messages.append(("user", user_msg))
        st.session_state.state["last_user_msg"] = user_msg
        st.session_state.state["history"].append({"role": "user", "content": user_msg})

        with st.spinner("Thinking..."):
            current_node_key = st.session_state.state["current_state"]
            node_function = NODE_MAP.get(current_node_key, end_node)
            new_state = node_function(st.session_state.state)
            agent_reply = new_state.get("agent_output", "I'm not sure how to respond to that.")

            st.session_state.state = new_state
            st.session_state.messages.append(("assistant", agent_reply))
            st.session_state.state["history"].append({
                "role": "assistant",
                "node": new_state["current_state"],
                "content": agent_reply
            })

        st.rerun()

# ── Session End Summary ────────────────────────────────────────────────────
if st.session_state.state["current_state"] == "END":
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