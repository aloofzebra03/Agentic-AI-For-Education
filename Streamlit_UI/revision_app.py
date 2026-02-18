"""
Simple Streamlit UI for Revision Agent

A text-only chatbot interface for the revision agent with chapter selection.
No audio/TTS/ASR functionality - just clean text input and output.
"""

import os
import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Import the revision agent graph
try:
    from revision_agent.graph import graph, RevisionAgentState
    from langchain_core.messages import HumanMessage
    from langgraph.types import Command
except ImportError as e:
    st.error(f"Could not import revision agent: {e}")
    st.info("Make sure you're running this from the project root directory.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Revision Agent", 
    page_icon="📚",
    layout="centered"
)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_available_chapters():
    """
    Scan the question_banks directory and return available chapters.
    
    Returns:
        List of tuples: (display_name, filename_without_extension)
    """
    question_banks_dir = Path("revision_agent/question_banks")
    
    if not question_banks_dir.exists():
        return []
    
    chapters = []
    for json_file in question_banks_dir.glob("*.json"):
        # Read the file to get the chapter name
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                chapter_name = data.get("chapter", json_file.stem.replace("_", " ").title())
                num_questions = len(data.get("questions", []))
                display_name = f"{chapter_name} ({num_questions} questions)"
                chapters.append((display_name, json_file.stem))
        except Exception as e:
            st.warning(f"Could not load {json_file.name}: {e}")
    
    return sorted(chapters, key=lambda x: x[1])


def initialize_session_state():
    """Initialize all session state variables."""
    if "session_started" not in st.session_state:
        st.session_state.session_started = False
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    
    if "selected_chapter" not in st.session_state:
        st.session_state.selected_chapter = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "last_result" not in st.session_state:
        st.session_state.last_result = None


def reset_session():
    """Reset session state to start a new session."""
    st.session_state.session_started = False
    st.session_state.session_id = None
    st.session_state.selected_chapter = None
    st.session_state.messages = []
    st.session_state.processing = False
    st.session_state.last_result = None


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main Streamlit application."""
    
    initialize_session_state()
    
    # Load all available chapters
    all_chapters = get_available_chapters()
    
    if not all_chapters:
        st.error("No question banks found in `revision_agent/question_banks/`")
        st.info("Please add JSON files to the question_banks directory.")
        st.stop()
    
    # ========================================================================
    # Start Screen (Chapter Selection)
    # ========================================================================
    
    if not st.session_state.session_started:
        st.title("📚 Revision Agent")
        st.caption("Test your knowledge with interactive revision sessions")
        st.markdown("---")
        
        st.subheader("Select a Chapter to Begin")
        
        # Chapter selection dropdown
        selected_chapter_display = st.selectbox(
            "Choose a chapter:",
            options=[display for display, _ in all_chapters],
            index=0
        )
        
        # Get the actual chapter identifier
        selected_chapter = next(
            filename for display, filename in all_chapters 
            if display == selected_chapter_display
        )
        
        # Start button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Revision Session", type="primary", use_container_width=True):
                # Generate session ID
                st.session_state.session_id = f"revision_{selected_chapter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.selected_chapter = selected_chapter
                st.session_state.session_started = True
                st.session_state.processing = True
                st.rerun()
        
        # Preview of selected chapter
        st.markdown("---")
        st.markdown("### Preview")
        try:
            question_bank_path = Path(f"revision_agent/question_banks/{selected_chapter}.json")
            with open(question_bank_path, 'r', encoding='utf-8') as f:
                preview_data = json.load(f)
                st.write(f"**Chapter:** {preview_data.get('chapter', 'N/A')}")
                st.write(f"**Number of Questions:** {len(preview_data.get('questions', []))}")
        except Exception as e:
            st.warning(f"Could not load preview: {e}")
        
        st.stop()
    
    # ========================================================================
    # Active Session Interface
    # ========================================================================
    
    # Sidebar with session info
    with st.sidebar:
        st.header("📚 Revision Session")
        
        # Current chapter display
        if st.session_state.selected_chapter:
            chapter_info = next(
                (display for display, filename in all_chapters if filename == st.session_state.selected_chapter),
                st.session_state.selected_chapter
            )
            st.info(f"**{chapter_info}**")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 New Chapter", use_container_width=True):
            reset_session()
            st.rerun()
        
        st.markdown("---")
        
        # Debug information
        st.markdown("### Session Info")
        
        if st.session_state.last_result:
            result = st.session_state.last_result
            
            st.metric("Current State", result.get("current_state", "Unknown"))
            
            # Progress
            current_idx = result.get("current_question_idx", 0)
            total = result.get("total_questions", 0)
            if total > 0:
                st.metric("Progress", f"{current_idx}/{total}")
                st.progress(current_idx / total)
            
            # Statistics
            st.markdown("**Statistics:**")
            st.write(f"✅ Correct first try: {result.get('correct_first_try_count', 0)}")
            st.write(f"💡 Needed help: {result.get('needed_help_count', 0)}")
            
            # Concepts for review
            concepts = result.get("concepts_for_review", [])
            if concepts:
                st.markdown("**📝 To Review:**")
                for concept in concepts:
                    st.write(f"• {concept}")
        else:
            st.caption("Starting session...")
        
        st.markdown("---")
        st.markdown("**💡 How to use:**")
        st.markdown("1. Answer questions in the chat")
        st.markdown("2. Get help if you struggle")
        st.markdown("3. Review summary at the end")
    
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
                        "chapter": st.session_state.selected_chapter,
                        "messages": [user_message]
                    }
                    result = graph.invoke(initial_state, config)
                    
                    # Extract AI response from initial greeting
                    ai_response = result.get("agent_output", "No response from agent")
                    print(f"✅ Session started successfully")
                    
                    # Append assistant message
                    st.session_state.messages.append(("assistant", ai_response))
                    
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
                                "messages": [user_message],  # LangGraph will add this to existing messages
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
                        print(f"📋 Result type: {type(result)}")
                        print(f"🎯 Current state: {result.get('current_state', 'N/A')}")
                        print(f"💬 Agent output: {result.get('agent_output', 'N/A')[:100] if result.get('agent_output') else 'None'}...")
                        
                        # Extract AI response
                        ai_response = result.get("agent_output", "No response from agent")
                        
                        # Append assistant message
                        st.session_state.messages.append(("assistant", ai_response))
                        
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
    
    st.title("💬 Revision Chat")
    
    # Display all messages
    for i, (role, content) in enumerate(st.session_state.messages):
        with st.chat_message(role):
            st.write(content)
    
    # ========================================================================
    # User Input
    # ========================================================================
    
    # Check if session is complete
    session_complete = False
    if st.session_state.last_result:
        if st.session_state.last_result.get("current_state") == "REVISION_END":
            session_complete = True
    
    if session_complete:
        # Display session summary
        st.markdown("---")
        st.success("🎉 Revision Session Complete!")
        
        result = st.session_state.last_result
        
        # Display summary metrics
        st.subheader("📊 Session Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", result.get("total_questions", 0))
        
        with col2:
            st.metric("Correct First Try", result.get("correct_first_try_count", 0))
        
        with col3:
            st.metric("Needed Help", result.get("needed_help_count", 0))
        
        # Concepts for review
        concepts = result.get("concepts_for_review", [])
        if concepts:
            st.markdown("### 📝 Concepts to Review")
            for i, concept in enumerate(concepts, 1):
                st.write(f"{i}. {concept}")
        else:
            st.success("🌟 Great job! You got all questions right on the first try!")
        
        # Create downloadable summary
        summary_data = {
            "chapter": result.get("chapter", ""),
            "total_questions": result.get("total_questions", 0),
            "correct_first_try": result.get("correct_first_try_count", 0),
            "needed_help": result.get("needed_help_count", 0),
            "concepts_for_review": concepts,
            "node_transitions": result.get("node_transitions", [])
        }
        
        summary_json = json.dumps(summary_data, indent=2)
        
        st.download_button(
            label="📥 Download Session Summary",
            data=summary_json,
            file_name=f"revision_summary_{result.get('chapter', 'session')}.json",
            mime="application/json"
        )
        
        # New session button
        st.markdown("---")
        if st.button("🔄 Start New Session", type="primary"):
            reset_session()
            st.rerun()
    else:
        # Text input for user response
        user_input = st.chat_input("💬 Type your answer here...")
        
        if user_input:
            # Append user message
            st.session_state.messages.append(("user", user_input))
            st.session_state.processing = True
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("🤖 Powered by Revision Agent")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
