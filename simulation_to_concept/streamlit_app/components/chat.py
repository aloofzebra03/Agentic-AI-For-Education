"""
Chat Component
==============
Handles the chat interface - displaying messages and input.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from streamlit_config import UI_CONFIG


def render_chat_message(role: str, content: str, timestamp: str = None):
    """
    Render a single chat message.
    
    Args:
        role: "teacher", "student", or "system"
        content: Message content
        timestamp: Optional timestamp to display
    """
    if role == "teacher":
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(content)
            if timestamp:
                st.caption(f"_{timestamp}_")
    
    elif role == "student":
        with st.chat_message("user", avatar="👩‍🎓"):
            st.markdown(content)
            if timestamp:
                st.caption(f"_{timestamp}_")
    
    else:  # system
        st.info(content)


def render_chat_history(messages: list):
    """
    Render the chat history.
    
    Args:
        messages: List of message dicts with 'role', 'content', and optional 'timestamp'
    """
    for msg in messages:
        render_chat_message(
            role=msg.get("role", "system"),
            content=msg.get("content", ""),
            timestamp=msg.get("timestamp")
        )


def render_concept_divider(concept_name: str, concept_number: int, total_concepts: int):
    """
    Render a divider when moving to a new concept.
    
    Args:
        concept_name: Name of the new concept
        concept_number: Current concept number (1-indexed)
        total_concepts: Total number of concepts
    """
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            background-color: #e8f5e9; 
            padding: 15px; 
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
        ">
            <h3>📚 Concept {concept_number} of {total_concepts}</h3>
            <h4>{concept_name}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")


def render_progress_bar(current_concept: int, total_concepts: int, understanding: str):
    """
    Render learning progress indicator.
    
    Args:
        current_concept: Current concept index (0-based)
        total_concepts: Total number of concepts
        understanding: Current understanding level
    """
    # Progress bar
    progress = (current_concept) / total_concepts if total_concepts > 0 else 0
    st.progress(progress)
    
    # Understanding indicator
    understanding_colors = {
        "none": "🔴",
        "partial": "🟠",
        "mostly": "🟡",
        "complete": "🟢"
    }
    indicator = understanding_colors.get(understanding, "⚪")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📊 Concepts: {current_concept}/{total_concepts}")
    with col2:
        st.caption(f"{indicator} Understanding: {understanding.title()}")


def render_chat_input():
    """
    Render the chat input box.
    
    Returns:
        User input string or None
    """
    return st.chat_input("Type your response here...")


def format_teacher_message(content: str) -> str:
    """
    Format teacher message for display.
    Makes certain keywords stand out.
    
    Args:
        content: Raw message content
        
    Returns:
        Formatted message
    """
    # Highlight action words
    formatted = content
    
    # Make OBSERVE, PREDICT, EXPLAIN stand out
    for keyword in ["OBSERVE:", "PREDICT:", "EXPLAIN:"]:
        if keyword in formatted:
            formatted = formatted.replace(
                keyword, 
                f"**{keyword}**"
            )
    
    return formatted


def initialize_chat_state():
    """Initialize chat-related session state variables."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "current_concept_displayed" not in st.session_state:
        st.session_state.current_concept_displayed = -1


def add_message_to_chat(role: str, content: str, simulation_data: dict = None):
    """
    Add a message to the chat history.
    
    Args:
        role: "teacher", "student", or "system"
        content: Message content
        simulation_data: Optional dict with simulation info for before/after display
                        {"before_params": {...}, "after_params": {...}}
    """
    from datetime import datetime
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    
    # Add simulation data if present (for parameter changes)
    if simulation_data:
        message["simulation_data"] = simulation_data
    
    st.session_state.chat_messages.append(message)
    
    # Trim if too long
    max_messages = UI_CONFIG.get("max_chat_history", 50)
    if len(st.session_state.chat_messages) > max_messages:
        st.session_state.chat_messages = st.session_state.chat_messages[-max_messages:]


def clear_chat():
    """Clear the chat history."""
    st.session_state.chat_messages = []
    st.session_state.current_concept_displayed = -1


def add_concept_change_marker(concept_name: str, concept_number: int, total_concepts: int):
    """
    Add a marker in chat when concept changes.
    
    Args:
        concept_name: Name of new concept
        concept_number: Concept number (1-indexed)
        total_concepts: Total concepts
    """
    st.session_state.chat_messages.append({
        "role": "system",
        "content": f"📚 **Concept {concept_number}/{total_concepts}:** {concept_name}",
        "timestamp": None,
        "is_divider": True
    })


# ═══════════════════════════════════════════════════════════════════════
# QUIZ UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

def render_quiz_question(question: dict, attempt_number: int):
    """
    Render a quiz question challenge.
    
    Args:
        question: Quiz question dict with id, challenge, hints, etc.
        attempt_number: Current attempt number (1-3)
    """
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            background-color: #fff3e0; 
            padding: 20px; 
            border-radius: 10px;
            border-left: 5px solid #ff9800;
            margin: 10px 0;
        ">
            <h3>🎯 Quiz Challenge</h3>
            <p style="font-size: 16px; margin-top: 10px;">{question['challenge']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if attempt_number > 1:
        st.info(f"💡 **Attempt {attempt_number}/3** - Adjust the simulation parameters and try again!")
    else:
        st.info("💡 Adjust the simulation parameters to achieve the goal, then click **SUBMIT ANSWER** below.")
    
    st.markdown("---")


def render_quiz_submit_button(current_params: dict) -> bool:
    """
    Render the quiz submission button with current parameters preview.
    
    Args:
        current_params: Current simulation parameters
        
    Returns:
        bool: True if button was clicked
    """
    st.markdown("### 📤 Submit Your Answer")
    
    # Show current parameters
    with st.expander("🔍 Current Parameters (what will be submitted)", expanded=False):
        for param, value in current_params.items():
            label = param.replace("_", " ").title()
            st.text(f"{label}: {value}")
    
    # Submit button
    clicked = st.button(
        "✅ SUBMIT ANSWER", 
        use_container_width=True, 
        type="primary",
        help="Submit your current simulation parameters for evaluation"
    )
    
    return clicked


def render_quiz_evaluation(evaluation: dict):
    """
    Render quiz evaluation feedback.
    
    Args:
        evaluation: Evaluation dict with score, status, feedback, etc.
    """
    score = evaluation.get("score", 0.0)
    status = evaluation.get("status", "WRONG")
    feedback = evaluation.get("feedback", "")
    attempt = evaluation.get("attempt", 1)
    allow_retry = evaluation.get("allow_retry", False)
    
    # Status indicators
    if status == "RIGHT":
        st.success(f"🎉 **Perfect!** (Score: {score})")
        st.balloons()
    elif status == "PARTIALLY_RIGHT":
        st.warning(f"⚠️ **Partially Correct** (Score: {score})")
    else:
        st.error(f"❌ **Not Quite Right** (Score: {score})")
    
    # Feedback message
    st.markdown("### 💬 Teacher's Feedback")
    st.info(feedback)
    
    # Retry info
    if allow_retry:
        st.caption(f"📊 Attempt {attempt}/3 - You can try again!")
    else:
        if status != "RIGHT":
            st.caption("📊 Maximum attempts reached. Moving to next question...")
        else:
            st.caption("✅ Moving to next question...")


def render_quiz_progress(quiz_scores: dict, total_questions: int, current_index: int):
    """
    Render quiz progress indicator.
    
    Args:
        quiz_scores: Dictionary of question_id -> score
        total_questions: Total number of questions
        current_index: Current question index (0-based)
    """
    completed = len(quiz_scores)
    
    # Progress bar
    progress = completed / total_questions if total_questions > 0 else 0
    st.progress(progress)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Questions", f"{completed}/{total_questions}")
    
    with col2:
        if completed > 0:
            avg_score = sum(quiz_scores.values()) / completed
            st.metric("Avg Score", f"{avg_score:.1f}")
        else:
            st.metric("Avg Score", "N/A")
    
    with col3:
        perfect_count = sum(1 for score in quiz_scores.values() if score >= 0.99)
        st.metric("Perfect", perfect_count)


def render_quiz_complete(quiz_scores: dict, total_questions: int):
    """
    Render quiz completion celebration.
    
    Args:
        quiz_scores: Dictionary of question_id -> score
        total_questions: Total number of questions
    """
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            background-color: #e8f5e9; 
            padding: 30px; 
            border-radius: 10px;
            text-align: center;
            border: 3px solid #4caf50;
        ">
            <h2>🎊 Quiz Complete! 🎊</h2>
            <p style="font-size: 18px; margin-top: 15px;">You've completed all quiz challenges!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.balloons()
    
    # Final statistics
    st.markdown("### 📊 Final Results")
    
    avg_score = sum(quiz_scores.values()) / len(quiz_scores) if quiz_scores else 0
    perfect_count = sum(1 for score in quiz_scores.values() if score >= 0.99)
    partial_count = sum(1 for score in quiz_scores.values() if 0.4 < score < 0.99)
    wrong_count = sum(1 for score in quiz_scores.values() if score <= 0.4)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Questions", total_questions)
    with col2:
        st.metric("Average Score", f"{avg_score:.2f}")
    with col3:
        st.metric("🟢 Perfect", perfect_count)
    with col4:
        st.metric("🟡 Partial", partial_count)
    
    # Breakdown
    st.markdown("### 📈 Performance Breakdown")
    for q_id, score in quiz_scores.items():
        if score >= 0.99:
            st.success(f"✅ {q_id}: Perfect ({score})")
        elif score > 0.4:
            st.warning(f"⚠️ {q_id}: Partial ({score})")
        else:
            st.error(f"❌ {q_id}: Wrong ({score})")

