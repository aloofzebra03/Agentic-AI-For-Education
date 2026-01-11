"""
State Definition for Version 3 Teaching Agent
==============================================
Rich state structure with understanding tracking, parameter history,
and conversation metadata for adaptive teaching.
"""

from typing import TypedDict, List, Dict, Optional, Any
from datetime import datetime


class ConversationMessage(TypedDict):
    """A single message in the conversation with rich metadata."""
    role: str                           # "teacher" | "student"
    content: str                        # The actual message
    timestamp: str                      # ISO format timestamp
    understanding_level: Optional[str]  # Level at time of message
    exchange_number: int                # Which exchange this belongs to


class ParameterChange(TypedDict):
    """Record of a simulation parameter change with context."""
    parameter: str                      # Which param changed (length, mass, etc.)
    old_value: float                    # Previous value
    new_value: float                    # New value
    reason: str                         # Why the change was made
    prediction_asked: str               # What we asked student to predict
    student_reaction: str               # How student responded
    understanding_before: str           # Level before this change
    understanding_after: str            # Level after this change
    was_effective: bool                 # Did this help understanding?


class Concept(TypedDict):
    """A teachable concept extracted from the topic."""
    id: int                             # Concept number
    title: str                          # Short title
    description: str                    # What to teach
    key_insight: str                    # The "aha" moment
    related_params: List[str]           # Which params illustrate this


class TeachingState(TypedDict):
    """
    Complete state for the adaptive teaching agent.
    
    This state tracks everything needed for:
    - Understanding student progress
    - Adapting teaching strategy
    - Maintaining natural conversation
    - Avoiding repetition
    """
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONTENT
    # ═══════════════════════════════════════════════════════════════════════
    topic_description: str              # The source material
    concepts: List[Concept]             # Extracted teachable concepts
    current_concept_index: int          # Which concept we're on
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONVERSATION
    # ═══════════════════════════════════════════════════════════════════════
    conversation_history: List[ConversationMessage]  # Full chat with metadata
    student_response: str               # Latest student input
    last_teacher_message: str           # What teacher just said
    
    # ═══════════════════════════════════════════════════════════════════════
    # UNDERSTANDING TRACKING
    # ═══════════════════════════════════════════════════════════════════════
    understanding_level: str            # Current: "none" | "partial" | "mostly" | "complete"
    understanding_trajectory: List[str] # History of levels for this concept
    understanding_reasoning: str        # LLM's explanation of the assessment
    
    # ═══════════════════════════════════════════════════════════════════════
    # PARAMETER HISTORY (Rich)
    # ═══════════════════════════════════════════════════════════════════════
    parameter_history: List[ParameterChange]  # Full history of param changes
    current_params: Dict[str, float]    # Current simulation state
    
    # ═══════════════════════════════════════════════════════════════════════
    # TEACHING CONTROL
    # ═══════════════════════════════════════════════════════════════════════
    exchange_count: int                 # Back-and-forth count for current concept
    strategy: str                       # Current: continue|try_different|scaffold|give_hint|summarize_advance
    teacher_mode: str                   # Current: encouraging|challenging|simplifying
    trajectory_status: str              # improving|stagnating|regressing
    
    # ═══════════════════════════════════════════════════════════════════════
    # FLAGS
    # ═══════════════════════════════════════════════════════════════════════
    should_scaffold: bool               # Break down current concept?
    concept_complete: bool              # Current concept understood?
    session_complete: bool              # All concepts done?
    waiting_for_input: bool             # Paused for student response?
    needs_deeper: bool                  # Ask student to explain WHY (observation without reasoning)
    cannot_demonstrate: List[str]       # Topics NOT in this simulation (don't mention)
    
    # ═══════════════════════════════════════════════════════════════════════
    # STUDENT RESPONSE TYPE FLAGS (set by evaluator)
    # ═══════════════════════════════════════════════════════════════════════
    student_asked_question: bool        # True if student asked a question
    question_asked: str                 # The actual question they asked
    student_requested_param: bool       # True if student requested param change
    requested_param: str                # Which param they want to change
    requested_value: Any                # What value they want
    is_factually_wrong: bool            # True if student stated something incorrect
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUIZ MODE (activated after all concepts taught)
    # ═══════════════════════════════════════════════════════════════════════
    quiz_mode: bool                     # True when in quiz mode, False during teaching
    quiz_questions: List[Dict[str, Any]]  # Loaded quiz questions for this simulation
    current_quiz_index: int             # Which quiz question (0, 1, 2...)
    quiz_attempts: Dict[str, int]       # {"q1": 2, "q2": 1} - attempts per question
    quiz_scores: Dict[str, float]       # {"q1": 1.0, "q2": 0.6} - score per question
    quiz_complete: bool                 # All quiz questions answered
    
    # Quiz submission (from API)
    submitted_parameters: Dict[str, Any]  # Parameters submitted by student via Android
    quiz_evaluation: Dict[str, Any]     # Last evaluation result (score, status, feedback)


def create_initial_state(topic_description: str, initial_params: Dict[str, float]) -> TeachingState:
    """
    Create a fresh initial state for a new teaching session.
    
    Args:
        topic_description: The source material to teach from
        initial_params: Starting simulation parameters
        
    Returns:
        Initialized TeachingState
    """
    return {
        # Content (concepts will be filled by content_loader)
        "topic_description": topic_description,
        "concepts": [],
        "current_concept_index": 0,
        
        # Conversation
        "conversation_history": [],
        "student_response": "",
        "last_teacher_message": "",
        
        # Understanding
        "understanding_level": "none",
        "understanding_trajectory": [],
        "understanding_reasoning": "",
        
        # Parameters
        "parameter_history": [],
        "current_params": initial_params.copy(),
        
        # Control
        "exchange_count": 0,
        "strategy": "continue",
        "teacher_mode": "encouraging",
        "trajectory_status": "improving",
        
        # Flags
        "should_scaffold": False,
        "concept_complete": False,
        "session_complete": False,
        "waiting_for_input": False,
        "needs_deeper": False,
        "cannot_demonstrate": [],
        
        # Student response type flags
        "student_asked_question": False,
        "question_asked": "",
        "student_requested_param": False,
        "requested_param": "",
        "requested_value": None,
        "is_factually_wrong": False,
        
        # Quiz mode (initialized as False, activated after concepts complete)
        "quiz_mode": False,
        "quiz_questions": [],
        "current_quiz_index": 0,
        "quiz_attempts": {},
        "quiz_scores": {},
        "quiz_complete": False,
        "submitted_parameters": {},
        "quiz_evaluation": {}
    }


def add_message_to_history(
    state: TeachingState, 
    role: str, 
    content: str
) -> ConversationMessage:
    """
    Helper to add a message with proper metadata.
    
    Args:
        state: Current state
        role: "teacher" or "student"
        content: The message content
        
    Returns:
        The created ConversationMessage
    """
    message: ConversationMessage = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "understanding_level": state.get("understanding_level", "none"),
        "exchange_number": state.get("exchange_count", 0)
    }
    return message


def add_parameter_change(
    state: TeachingState,
    parameter: str,
    new_value: float,
    reason: str,
    prediction_asked: str
) -> ParameterChange:
    """
    Helper to record a parameter change.
    
    Args:
        state: Current state
        parameter: Which parameter to change
        new_value: New value
        reason: Why this change
        prediction_asked: The prediction question asked
        
    Returns:
        The created ParameterChange record
    """
    old_value = state["current_params"].get(parameter, 0)
    
    change: ParameterChange = {
        "parameter": parameter,
        "old_value": old_value,
        "new_value": new_value,
        "reason": reason,
        "prediction_asked": prediction_asked,
        "student_reaction": "",  # Filled later
        "understanding_before": state.get("understanding_level", "none"),
        "understanding_after": "",  # Filled after evaluation
        "was_effective": False  # Determined later
    }
    return change
