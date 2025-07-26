import os
from dotenv import load_dotenv
import streamlit as st
import json
import subprocess
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
# Ensure this path is correct for your system if ffmpeg is still needed by onnx_asr or for other audio ops
# ffmpeg_path = r'C:\micromamba\envs\langchain\Library\bin\ffmpeg.exe'

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
        f.write(audio_bytes)

    mono_wav_path = "temp_recorded_mono.wav"
    transcript = None
    try:
        convert_to_mono_wav(tmp_path, mono_wav_path)
        transcript = asr_model.recognize(mono_wav_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        # Corrected: ensure the mono_wav_path variable is used for cleanup
        if os.path.exists(mono_wav_path):
            os.remove(mono_wav_path)
    return transcript

# ── Text-to-Speech Function using HTML5 Audio (Improved Version) ─────
def play_text_as_audio_autoplay(text, audio_placeholder_container):
    """
    Converts text to speech using gTTS and plays it automatically
    by embedding an HTML5 audio tag into the given placeholder
    and programmatically playing it with JavaScript.
    """
    if text and text.strip(): # Only generate audio if there's actual text to speak
        try:
            tts = gTTS(text=text, lang='en', slow=False)

            # Use tempfile to create and manage temporary files securely
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.write_to_fp(tmp)
                temp_audio_file_path = tmp.name

            # Read the audio bytes and base64 encode them
            with open(temp_audio_file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            # Generate a unique ID for the audio element
            audio_id = f"audio_player_{int(time.time() * 1000000)}"  # More unique timestamp
            
            # Check if user has interacted to enable more aggressive autoplay
            autoplay_enabled = st.session_state.get("audio_interaction_done", False)
            
            # Create the HTML audio tag with aggressive autoplay bypassing techniques
            audio_html = f"""
            <div style="margin: 10px 0; padding: 10px; background: #f0f2f6; border-radius: 8px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 14px;">🔊 Agent Response Audio:</span>
                    <button id="play_btn_{audio_id}" onclick="forcePlayAudio_{audio_id}()" 
                            style="background: #ff4b4b; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                        ▶️ Play Audio
                    </button>
                    <button id="enable_autoplay_{audio_id}" onclick="enableAutoplayForSession_{audio_id}()" 
                            style="background: #28a745; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                        🔓 Enable Autoplay
                    </button>
                </div>
                <audio id="{audio_id}" controls preload="auto" style="width: 100%; margin-top: 10px;" autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                <script>
                    // Global autoplay permission flag
                    window.autoplayPermissionGranted = window.autoplayPermissionGranted || {str(autoplay_enabled).lower()};
                    
                    function enableAutoplayForSession_{audio_id}() {{
                        // Play a silent audio to get user gesture
                        var audio = document.getElementById("{audio_id}");
                        var btn = document.getElementById("enable_autoplay_{audio_id}");
                        
                        if (audio) {{
                            audio.muted = true;
                            audio.play().then(function() {{
                                // Immediately unmute and set proper volume
                                audio.muted = false;
                                audio.volume = 0.9;
                                window.autoplayPermissionGranted = true;
                                btn.innerHTML = "✅ Autoplay Enabled";
                                btn.disabled = true;
                                btn.style.background = "#6c757d";
                                
                                // Store permission in sessionStorage
                                sessionStorage.setItem('audioAutoplayEnabled', 'true');
                                
                                // Immediately try to play current audio unmuted
                                setTimeout(function() {{
                                    forcePlayAudio_{audio_id}();
                                }}, 100);
                            }}).catch(function(error) {{
                                console.log('Could not enable autoplay:', error);
                                btn.innerHTML = "❌ Failed";
                            }});
                        }}
                    }}
                    
                    function forcePlayAudio_{audio_id}() {{
                        var audio = document.getElementById("{audio_id}");
                        var btn = document.getElementById("play_btn_{audio_id}");
                        if (audio) {{
                            audio.muted = false;
                            audio.volume = 0.9;
                            audio.play().then(function() {{
                                btn.innerHTML = "🔊 Playing...";
                                btn.disabled = true;
                                window.autoplayPermissionGranted = true;
                                sessionStorage.setItem('audioAutoplayEnabled', 'true');
                            }}).catch(function(error) {{
                                console.log('Manual play failed:', error);
                                btn.innerHTML = "❌ Play Failed";
                            }});
                        }}
                    }}
                    
                    function unmutedAutoplay_{audio_id}() {{
                        var audio = document.getElementById("{audio_id}");
                        var btn = document.getElementById("play_btn_{audio_id}");
                        var enableBtn = document.getElementById("enable_autoplay_{audio_id}");
                        
                        // Check if we have permission from previous interactions
                        var hasPermission = window.autoplayPermissionGranted || 
                                          sessionStorage.getItem('audioAutoplayEnabled') === 'true';
                        
                        if (hasPermission && audio) {{
                            // Try unmuted autoplay first
                            audio.muted = false;
                            audio.volume = 0.9;
                            var playPromise = audio.play();
                            if (playPromise !== undefined) {{
                                playPromise.then(function() {{
                                    console.log('Unmuted autoplay successful');
                                    btn.innerHTML = "🔊 Playing...";
                                    btn.disabled = true;
                                    enableBtn.style.display = "none"; // Hide enable button
                                }}).catch(function(error) {{
                                    console.log('Unmuted autoplay blocked, trying muted fallback:', error);
                                    // Fallback to muted play
                                    audio.muted = true;
                                    audio.play().then(function() {{
                                        btn.innerHTML = "🔇 Playing Muted - Click to Unmute";
                                        btn.onclick = function() {{
                                            audio.muted = false;
                                            btn.innerHTML = "� Playing...";
                                            btn.disabled = true;
                                        }};
                                        enableBtn.innerHTML = "🔊 Unmute";
                                        enableBtn.onclick = function() {{
                                            audio.muted = false;
                                            btn.innerHTML = "🔊 Playing...";
                                            enableBtn.style.display = "none";
                                        }};
                                    }}).catch(function(mutedError) {{
                                        console.log('Even muted autoplay failed:', mutedError);
                                        btn.innerHTML = "▶️ Click to Play";
                                        btn.style.background = "#28a745";
                                    }});
                                }});
                            }}
                        }} else {{
                            btn.innerHTML = "▶️ Click to Play";
                            btn.style.background = "#28a745";
                            enableBtn.innerHTML = "🔓 Enable Autoplay";
                        }}
                    }}
                    
                    (function() {{
                        var audio = document.getElementById("{audio_id}");
                        var btn = document.getElementById("play_btn_{audio_id}");
                        var enableBtn = document.getElementById("enable_autoplay_{audio_id}");
                        var autoplayEnabled = {str(autoplay_enabled).lower()};
                        
                        if (audio) {{
                            // Set volume to ensure it's audible
                            audio.volume = 0.9;
                            
                            // Check for existing permission
                            var hasStoredPermission = sessionStorage.getItem('audioAutoplayEnabled') === 'true';
                            if (hasStoredPermission) {{
                                window.autoplayPermissionGranted = true;
                                autoplayEnabled = true;
                            }}
                            
                            // Multiple autoplay bypass strategies
                            function attemptAutoplay(strategy) {{
                                console.log('Attempting autoplay strategy:', strategy);
                                
                                switch(strategy) {{
                                    case 'immediate':
                                        audio.muted = false;
                                        audio.volume = 0.9;
                                        return audio.play();
                                    
                                    case 'muted-then-unmuted':
                                        audio.muted = true;
                                        return audio.play().then(function() {{
                                            console.log('Muted play started, unmuting in 500ms...');
                                            setTimeout(function() {{
                                                audio.muted = false;
                                                audio.volume = 0.9;
                                                console.log('Audio unmuted');
                                            }}, 500);
                                        }});
                                    
                                    case 'interaction-triggered':
                                        // Wait for any click on the page
                                        document.addEventListener('click', function triggerPlay() {{
                                            audio.muted = false;
                                            audio.volume = 0.9;
                                            audio.play().then(function() {{
                                                btn.innerHTML = "🔊 Playing...";
                                                btn.disabled = true;
                                            }});
                                            document.removeEventListener('click', triggerPlay);
                                        }}, {{ once: true }});
                                        break;
                                }}
                            }}
                            
                    (function() {{
                        var audio = document.getElementById("{audio_id}");
                        var btn = document.getElementById("play_btn_{audio_id}");
                        var enableBtn = document.getElementById("enable_autoplay_{audio_id}");
                        var autoplayEnabled = {str(autoplay_enabled).lower()};
                        
                        if (audio) {{
                            // Set volume to ensure it's audible
                            audio.volume = 0.9;
                            
                            // Check for existing permission
                            var hasStoredPermission = sessionStorage.getItem('audioAutoplayEnabled') === 'true';
                            if (hasStoredPermission) {{
                                window.autoplayPermissionGranted = true;
                                autoplayEnabled = true;
                            }}
                            
                            // Multiple autoplay bypass strategies
                            function attemptAutoplay(strategy) {{
                                console.log('Attempting autoplay strategy:', strategy);
                                
                                switch(strategy) {{
                                    case 'immediate':
                                        audio.muted = false;
                                        audio.volume = 0.9;
                                        return audio.play();
                                    
                                    case 'muted-then-unmuted':
                                        audio.muted = true;
                                        return audio.play().then(function() {{
                                            console.log('Muted play started, unmuting in 500ms...');
                                            setTimeout(function() {{
                                                audio.muted = false;
                                                audio.volume = 0.9;
                                                console.log('Audio unmuted');
                                            }}, 500);
                                        }});
                                    
                                    case 'interaction-triggered':
                                        // Wait for any click on the page
                                        document.addEventListener('click', function triggerPlay() {{
                                            audio.muted = false;
                                            audio.volume = 0.9;
                                            audio.play().then(function() {{
                                                btn.innerHTML = "🔊 Playing...";
                                                btn.disabled = true;
                                            }});
                                            document.removeEventListener('click', triggerPlay);
                                        }}, {{ once: true }});
                                        break;
                                }}
                            }}
                            
                            // Trigger autoplay when audio can play
                            audio.addEventListener('canplay', function() {{
                                console.log('Audio can play, checking autoplay permissions');
                                if (autoplayEnabled || window.autoplayPermissionGranted) {{
                                    console.log('Autoplay enabled, attempting immediate play');
                                    attemptAutoplay('immediate').then(function() {{
                                        console.log('Immediate autoplay successful');
                                        btn.innerHTML = "🔊 Playing...";
                                        btn.disabled = true;
                                        enableBtn.style.display = "none";
                                    }}).catch(function(error) {{
                                        console.log('Immediate autoplay failed, trying muted strategy');
                                        attemptAutoplay('muted-then-unmuted').then(function() {{
                                            btn.innerHTML = "🔇➡️🔊 Playing";
                                            btn.disabled = true;
                                            enableBtn.innerHTML = "🔊 Unmute";
                                        }}).catch(function(error2) {{
                                            console.log('Muted autoplay failed, waiting for interaction');
                                            attemptAutoplay('interaction-triggered');
                                            btn.innerHTML = "👆 Click anywhere to play";
                                            btn.style.background = "#ffc107";
                                        }});
                                    }});
                                }} else {{
                                    console.log('Autoplay not enabled, showing manual controls');
                                    btn.innerHTML = "▶️ Click to Play";
                                    btn.style.background = "#28a745";
                                }}
                            }});
                            
                            // Also listen for loadeddata event for earlier trigger
                            audio.addEventListener('loadeddata', function() {{
                                console.log('Audio data loaded, checking for autoplay');
                                if (autoplayEnabled || window.autoplayPermissionGranted) {{
                                    if (!audio.paused) return; // Already playing
                                    console.log('Attempting autoplay on loadeddata');
                                    attemptAutoplay('immediate').then(function() {{
                                        console.log('Loadeddata autoplay successful');
                                        btn.innerHTML = "🔊 Playing...";
                                        btn.disabled = true;
                                        enableBtn.style.display = "none";
                                    }}).catch(function(error) {{
                                        console.log('Loadeddata autoplay failed');
                                    }});
                                }}
                            }});
                            
                            // Listen for play event from HTML autoplay attribute
                            audio.addEventListener('play', function() {{
                                console.log('Audio started playing');
                                btn.innerHTML = "🔊 Playing...";
                                btn.disabled = true;
                                enableBtn.style.display = "none";
                            }});
                            
                            audio.addEventListener('pause', function() {{
                                console.log('Audio paused');
                                if (!audio.ended) {{
                                    btn.innerHTML = "▶️ Resume";
                                    btn.disabled = false;
                                    btn.style.background = "#28a745";
                                }}
                            }});
                            
                            // Also try immediate autoplay for cases where audio is already loaded
                            if (autoplayEnabled || window.autoplayPermissionGranted) {{
                                setTimeout(function() {{
                                    if (audio.readyState >= 3) {{ // HAVE_FUTURE_DATA or better
                                        console.log('Audio already loaded, attempting immediate autoplay');
                                        attemptAutoplay('immediate').then(function() {{
                                            console.log('Immediate autoplay successful');
                                            btn.innerHTML = "🔊 Playing...";
                                            btn.disabled = true;
                                            enableBtn.style.display = "none";
                                        }}).catch(function(error) {{
                                            console.log('Immediate autoplay failed');
                                            btn.innerHTML = "▶️ Click to Play";
                                            btn.style.background = "#28a745";
                                        }});
                                    }}
                                }}, 100);
                            }}
                            
                            // Reset button when audio ends
                            audio.addEventListener('ended', function() {{
                                btn.innerHTML = "🔄 Replay";
                                btn.disabled = false;
                                btn.style.background = "#6c757d";
                            }});
                            
                            audio.addEventListener('error', function(e) {{
                                console.error('Audio error:', e);
                                btn.innerHTML = "❌ Error";
                            }});
                        }}
                    }})();
                </script>
            </div>
            """
            
            # Use the passed placeholder to render the audio HTML
            with audio_placeholder_container:
                st.markdown(audio_html, unsafe_allow_html=True)

            # Clean up the temporary file
            os.remove(temp_audio_file_path)

        except Exception as e:
            st.error(f"Could not generate audio for: '{text[:50]}...'. Error: {e}")
            st.info("Please check your internet connection (required for text-to-speech) and browser audio settings.")


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

# ── Initial Interaction / Welcome Screen ───────────────────────────────────
# This block ensures an initial user click to enable autoplay
if "first_interaction_done" not in st.session_state:
    st.title("🧑‍🎓 Interactive Tutor")
    st.info("Welcome to the Interactive Tutor! To enable voice communication and begin the session, please click the button below.")
    
    # Add audio test button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Learning"):
            st.session_state.first_interaction_done = True
            st.session_state.audio_interaction_done = True  # Enable autoplay
            # IMPORTANT: Do NOT st.rerun() here. Let the script proceed naturally.
            # This allows the initial audio to play as a direct result of the click.
    
    with col2:
        if st.button("🔊 Test Audio"):
            st.success("Testing audio... You should hear a test message.")
            test_placeholder = st.empty()
            play_text_as_audio_autoplay("This is a test of the audio system. If you can hear this, audio is working correctly.", test_placeholder)
            # Enable autoplay for the session after successful user interaction
            st.session_state.audio_interaction_done = True
    
    # Add instructions for enabling autoplay
    st.info("""
    **🎵 For the best experience with automatic audio:**
    1. Click '🚀 Start Learning' or '🔊 Test Audio' above
    2. After starting, click '🔓 Enable Auto-Audio for All Responses' 
    3. If audio still doesn't auto-play, check your browser settings:
       - **Chrome**: Click the 🔒 icon in address bar → Site settings → Sound → Allow
       - **Firefox**: Click the 🛡️ icon → Permissions → Autoplay → Allow Audio and Video
       - **Safari**: Safari → Settings → Websites → Auto-Play → Allow All Auto-Play
    """)
    
    with st.expander("🔧 Browser Autoplay Settings (Click to expand)"):
        st.markdown("""
        **If autoplay doesn't work, manually allow it:**
        
        **Google Chrome:**
        1. Click the lock/info icon left of the URL
        2. Select "Site settings"  
        3. Find "Sound" and set to "Allow"
        4. Refresh the page
        
        **Firefox:**
        1. Click the shield icon in address bar
        2. Click "Permissions"
        3. Set "Autoplay" to "Allow Audio and Video"
        
        **Safari:**
        1. Safari menu → Settings → Websites
        2. Select "Auto-Play" 
        3. Set to "Allow All Auto-Play" for this site
        
        **Microsoft Edge:**
        1. Click the lock icon in address bar
        2. Select "Permissions for this site"
        3. Set "Media autoplay" to "Allow"
        """)
    
    if not st.session_state.get("first_interaction_done", False):
        # If the start button hasn't been clicked yet, stop the script here.
        st.stop()

# ── Main Application Logic (runs only after initial interaction or on subsequent reruns) ──────────

# Initialize session state for the agent if not already done
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
    st.session_state.audio_recorder_key_counter = 0 # This counter is still useful for unique keys

    # Process the initial START node
    init_state = start_node(st.session_state.state)
    intro_message = init_state["agent_output"]
    st.session_state.state = init_state

    # Add intro message to chat history
    st.session_state.messages.append(("assistant", intro_message))
    st.session_state.state["history"].append({
        "role":    "assistant",
        "node":    "START",
        "content": intro_message
    })

    # Play the initial intro message automatically.
    # This call now happens in the same script run where the "Start Learning" button was clicked,
    # ensuring it's seen as a direct user gesture.
    # The audio will be displayed when the chat history is rendered above


st.title("🧑‍🎓 Interactive Tutor")

# Add a global autoplay enabler
if st.session_state.get("first_interaction_done", False):
    st.markdown("""
    <div style="background: #e8f4fd; padding: 10px; border-radius: 8px; margin: 10px 0;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span>🔊 <strong>Audio Status:</strong></span>
            <button onclick="enableGlobalAutoplay()" id="global-autoplay-btn" 
                    style="background: #28a745; color: white; border: none; padding: 5px 15px; border-radius: 4px; cursor: pointer;">
                🔓 Enable Auto-Audio for All Responses
            </button>
            <span id="autoplay-status" style="font-size: 12px; color: #666;">Click to enable seamless audio playback</span>
        </div>
    </div>
    <script>
        function enableGlobalAutoplay() {
            // Create a silent audio element to get user permission
            var silentAudio = document.createElement('audio');
            silentAudio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+Hvw2odBDx+0fPTfS4GL3fA7+WXRAoglaLe8KlnHg'; // Very short silent audio
            
            var btn = document.getElementById('global-autoplay-btn');
            var status = document.getElementById('autoplay-status');
            
            silentAudio.play().then(function() {
                // Success - store permission
                sessionStorage.setItem('audioAutoplayEnabled', 'true');
                window.autoplayPermissionGranted = true;
                
                btn.innerHTML = '✅ Auto-Audio Enabled';
                btn.disabled = true;
                btn.style.background = '#6c757d';
                status.innerHTML = 'All audio will now play automatically!';
                status.style.color = '#28a745';
                
                // Enable autoplay for current session
                window.dispatchEvent(new CustomEvent('autoplayEnabled'));
                
            }).catch(function(error) {
                btn.innerHTML = '❌ Permission Denied';
                btn.style.background = '#dc3545';
                status.innerHTML = 'Browser blocked autoplay. Use individual play buttons.';
                status.style.color = '#dc3545';
            });
        }
        
        // Check if permission already exists
        if (sessionStorage.getItem('audioAutoplayEnabled') === 'true') {
            var btn = document.getElementById('global-autoplay-btn');
            var status = document.getElementById('autoplay-status');
            if (btn && status) {
                btn.innerHTML = '✅ Auto-Audio Enabled';
                btn.disabled = true;
                btn.style.background = '#6c757d';
                status.innerHTML = 'Auto-audio is active for this session';
                status.style.color = '#28a745';
                window.autoplayPermissionGranted = true;
            }
        }
    </script>
    """, unsafe_allow_html=True)

# Display chat history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)
        # Add audio player for each assistant message
        if role == "assistant":
            audio_container = st.empty()
            play_text_as_audio_autoplay(msg, audio_container)


# ── User Turn: only show input options if the agent is not in the END state ──
if st.session_state.state["current_state"] != "END":
    user_msg = None
    input_source = None

    st.markdown("### Respond with Audio or Text")

    # --- Direct Microphone Icon for Recording ---
    current_audio_recorder_key = f"audio_recorder_{st.session_state.audio_recorder_key_counter}"

    recorded_audio_bytes = audio_recorder(
        text="Click mic to record, click again to stop.", # Clear instruction for the user
        key=current_audio_recorder_key,
        icon_size="3x",
        auto_start=False, # Explicitly set to False for manual control
    )

    if recorded_audio_bytes:
        with st.spinner("Transcribing recorded audio..."):
            try:
                user_msg = transcribe_recorded_audio_bytes(recorded_audio_bytes)
                st.success(f"Transcribed Text: {user_msg}")
                input_source = "audio_recording"
                # Increment the key counter to ensure a fresh audio_recorder component
                # is rendered on the next turn, ready for a new recording.
                st.session_state.audio_recorder_key_counter += 1
            except Exception as e:
                st.error(f"Recorded audio transcription failed: {e}")
                pass # The cleanup is now handled robustly inside the transcribe function

    # Text input (always display now)
    if not user_msg:
        user_msg = st.chat_input("Or type your response...")
        if user_msg:
            input_source = "chat_input"
            # If text input is used, increment the audio_recorder key to reset it
            # so it's ready for recording on the next turn.
            st.session_state.audio_recorder_key_counter += 1


    # If user responded (via any mode)
    if user_msg:
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

        # This st.rerun() will redisplay the chat history with the new message and its audio
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