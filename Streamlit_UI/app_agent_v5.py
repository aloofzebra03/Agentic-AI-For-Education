"""
Streamlit UI for Educational Agent V5 (Simulation + Autosuggestion)

Features:
- Text-only chat interface
- Concept selection
- Static autosuggestions display
- Last 5 messages history shown in sidebar
- Session state management with thread ID
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Import the v5 educational agent graph
try:
    from educational_agent_optimized_langsmith_v5.graph import graph, AgentState
    from langchain_core.messages import HumanMessage
    from langgraph.types import Command
    from utils.shared_utils import get_all_available_concepts
except ImportError as e:
    st.error(f"Could not import educational agent v5: {e}")
    st.info("Make sure you're running this from the project root directory.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Educational Agent V5", 
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better visibility
st.markdown("""
<style>
    /* Increase font size for chat messages */
    .stChatMessage {
        font-size: 1.1rem !important;
    }
    
    .stChatMessage p {
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Autosuggestion box styling */
    .autosuggestion-box {
        background: #f0f6ff;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .positive-suggestion {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        color: #000000;
    }
    
    .negative-suggestion {
        background: #fff3e0;
        border-left: 4px solid #FF9800;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        color: #000000;
    }
    
    .dynamic-suggestion {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_available_concepts():
    """
    Get list of available concepts (chapter/topics) from science_jsons.
    Uses the shared_utils function to dynamically load concepts from JSON files.
    """
    # Get all concepts from science_jsons folder
    concepts = get_all_available_concepts()
    
    # Convert to title case for better display (the function returns them properly formatted)
    return concepts


def initialize_session_state():
    """Initialize all session state variables."""
    if "session_started" not in st.session_state:
        st.session_state.session_started = False
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    
    if "selected_concept" not in st.session_state:
        st.session_state.selected_concept = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    
    if "autosuggestions" not in st.session_state:
        st.session_state.autosuggestions = {
            "positive": "",
            "negative": "",
            "dynamic": ""
        }


def reset_session():
    """Reset session state to start a new session."""
    st.session_state.session_started = False
    st.session_state.session_id = None
    st.session_state.selected_concept = None
    st.session_state.messages = []
    st.session_state.processing = False
    st.session_state.last_result = None
    st.session_state.autosuggestions = {
        "positive": "",
        "negative": "",
        "dynamic": ""
    }


def extract_autosuggestions(result: Dict[str, Any]) -> Dict[str, str]:
    """Extract autosuggestions from agent result."""
    return {
        "positive": result.get("positive_autosuggestion", ""),
        "negative": result.get("negative_autosuggestion", ""),
        "dynamic": result.get("dynamic_autosuggestion", "")
    }


def display_autosuggestions():
    """Display static autosuggestions in a nice format."""
    suggestions = st.session_state.autosuggestions
    
    # Only display if at least one suggestion exists
    if any(suggestions.values()):
        st.markdown("### 💡 Suggested Responses")
        st.caption("⚠️ Note: Autosuggestions are static and shown from the last agent response")
        
        if suggestions["positive"]:
            st.markdown(f"""
            <div class="positive-suggestion">
                <strong>✅ Positive:</strong> {suggestions["positive"]}
            </div>
            """, unsafe_allow_html=True)
        
        if suggestions["negative"]:
            st.markdown(f"""
            <div class="negative-suggestion">
                <strong>⚠️ Negative:</strong> {suggestions["negative"]}
            </div>
            """, unsafe_allow_html=True)
        
        if suggestions["dynamic"]:
            st.markdown(f"""
            <div class="dynamic-suggestion">
                <strong>🔄 Dynamic:</strong> {suggestions["dynamic"]}
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main Streamlit application."""
    
    initialize_session_state()
    
    # Get available concepts
    all_concepts = get_available_concepts()
    concepts_title_case = [' '.join(word.capitalize() for word in concept.split()) for concept in all_concepts]
    # ========================================================================
    # Start Screen (Concept Selection)
    # ========================================================================
    
    if not st.session_state.session_started:
        st.title("🎓 Educational Agent V5")
        st.caption("Interactive learning with simulation and autosuggestions")
        st.markdown("---")
        
        st.subheader("Select a Topic to Begin")
        
        # Concept selection dropdown
        selected_concept = st.selectbox(
            "Choose a topic:",
            options=concepts_title_case,
            index=0
        )
        
        # Start button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Learning Session", type="primary", use_container_width=True):
                # Generate session ID
                st.session_state.session_id = f"edu_v5_{selected_concept.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.selected_concept = selected_concept
                st.session_state.session_started = True
                st.session_state.processing = True
                st.rerun()
        
        # Info about the agent
        st.markdown("---")
        st.markdown("### About This Agent")
        st.info("""
        This educational agent features:
        - **Simulation-based learning**: Interactive pendulum simulations
        - **Static Autosuggestions**: Get suggested responses to guide your learning (shown from last response)
        - **Adaptive teaching**: Personalized based on your responses
        - **Conversation memory**: Agent uses last 4 messages for decision making (shown in sidebar)
        """)
        
        st.stop()
    
    # ========================================================================
    # Active Session Interface
    # ========================================================================
    
    # Sidebar with session info and last 5 messages
    with st.sidebar:
        st.header("📚 Learning Session")
        
        # Current concept display
        if st.session_state.selected_concept:
            st.info(f"**Topic:** {st.session_state.selected_concept}")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 New Topic", use_container_width=True):
            reset_session()
            st.rerun()
        
        st.markdown("---")
        
        # Session Info
        st.markdown("### Session Info")
        
        if st.session_state.last_result:
            result = st.session_state.last_result
            
            st.metric("Current State", result.get("current_state", "Unknown"))
            
            # Concept tracking
            if result.get("concept_title"):
                st.write(f"**Concept:** {result['concept_title']}")
            
            # Mode tracking
            if result.get("mode"):
                st.write(f"**Mode:** {result['mode']}")
        else:
            st.caption("Starting session...")
        
        st.markdown("---")
        
        # Last 4 Messages History
        st.markdown("### 📜 Recent Messages (Last 4)")
        
        if st.session_state.messages:
            # Get last 4 messages
            recent_messages = st.session_state.messages[-4:]
            
            for i, (role, content) in enumerate(recent_messages):
                # Truncate long messages
                display_content = content[:100] + "..." if len(content) > 100 else content
                
                if role == "user":
                    st.caption(f"**You:** {display_content}")
                else:
                    st.caption(f"**Agent:** {display_content}")
        else:
            st.caption("No messages yet...")
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("- Use suggested responses")
        st.markdown("- Ask questions freely")
        st.markdown("- Engage with simulations")
    
    # ========================================================================
    # Processing Phase (Two-Phase Rerun Pattern)
    # ========================================================================
    
    if st.session_state.processing:
        st.session_state.processing = False
        
        config = {
            "configurable": {
                "thread_id": st.session_state.session_id
            }
        }
        
        print(f"\n🔑 Streamlit: Using session_id: {st.session_state.session_id}")
        print(f"📊 Streamlit: Messages count: {len(st.session_state.messages)}")
        
        with st.spinner("🤔 Thinking..."):
            try:
                # Check if this is the initial call or continuation
                if len(st.session_state.messages) == 0:
                    # Initial call - start the session
                    print("\n📍 Streamlit: Initial graph invoke")
                    user_message = HumanMessage(content="start")
                    initial_state = {
                        "concept_title": st.session_state.selected_concept,
                        "messages": [user_message]
                    }
                    result = graph.invoke(initial_state, config)
                    
                    # Extract AI response from initial greeting
                    ai_response = result.get("agent_output", "No response from agent")
                    print(f"✅ Session started successfully")
                    
                    # Append assistant message
                    st.session_state.messages.append(("assistant", ai_response))
                    
                    # Extract autosuggestions
                    st.session_state.autosuggestions = extract_autosuggestions(result)
                    
                else:
                    # Continuation - get last user message content only
                    last_user_msg = None
                    for role, msg in reversed(st.session_state.messages):
                        if role == "user":
                            last_user_msg = msg
                            break
                    
                    if last_user_msg:
                        print(f"\n📍 Streamlit: Continuing graph with user message: {last_user_msg[:50]}...")
                        
                        # Create user message
                        user_message = HumanMessage(content=last_user_msg)
                        
                        # Use Command with resume=True to continue from interrupted state
                        cmd = Command(
                            resume=True,
                            update={
                                "messages": [user_message],
                            },
                        )
                        
                        print(f"🔄 About to invoke graph with Command...")
                        print(f"   - resume: True")
                        print(f"   - thread_id: {st.session_state.session_id}")
                        
                        try:
                            # Continue the graph from where it was interrupted
                            result = graph.invoke(cmd, config)
                            print(f"✅ Graph invoke returned successfully")
                        except Exception as invoke_error:
                            print(f"❌ ERROR during graph.invoke: {invoke_error}")
                            import traceback
                            traceback.print_exc()
                            raise
                        
                        print(f"\n✅ Graph invoke completed")
                        print(f"🎯 Current state: {result.get('current_state', 'N/A')}")
                        
                        # Extract AI response
                        ai_response = result.get("agent_output", "No response from agent")
                        
                        # Append assistant message
                        st.session_state.messages.append(("assistant", ai_response))
                        
                        # Extract autosuggestions
                        st.session_state.autosuggestions = extract_autosuggestions(result)
                        
                    else:
                        st.error("No user message found to process")
                        st.stop()
                
                # Store result for debugging
                st.session_state.last_result = result
                
                print(f"📍 Streamlit: Graph completed. Current state: {result.get('current_state')}")
                
            except Exception as e:
                st.error(f"Error communicating with agent: {e}")
                st.exception(e)
        
        st.rerun()
    
    # ========================================================================
    # Chat Display
    # ========================================================================
    
    st.title("💬 Learning Chat(Static Autosuggestions and Last 4 Messages as Conversation History)")
    
    # Display all messages
    for i, (role, content) in enumerate(st.session_state.messages):
        with st.chat_message(role):
            st.write(content)
    
    # Display static autosuggestions below the chat
    if st.session_state.messages:
        display_autosuggestions()
    
    # ========================================================================
    # User Input
    # ========================================================================
    
    # Check if session is complete
    session_complete = False
    if st.session_state.last_result:
        if st.session_state.last_result.get("current_state") == "END":
            session_complete = True
    
    if session_complete:
        st.markdown("---")
        st.success("🎉 Learning Session Complete!")
        
        result = st.session_state.last_result
        
        # Display session summary if available
        if result.get("session_summary"):
            st.subheader("📊 Session Summary")
            st.json(result["session_summary"])
        
        # New session button
        st.markdown("---")
        if st.button("🔄 Start New Session", type="primary"):
            reset_session()
            st.rerun()
    else:
        # Text input for user response
        user_input = st.chat_input("💬 Type your response here...")
        
        if user_input:
            # Append user message
            st.session_state.messages.append(("user", user_input))
            st.session_state.processing = True
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("🤖 Powered by Educational Agent V5 (Simulation + Autosuggestion)")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
