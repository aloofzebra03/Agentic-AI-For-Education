"""
Backend Integration Module
==========================
Provides a clean interface between the Streamlit app and the LangGraph backend.
Handles session management, state synchronization, and response processing.
"""

import sys
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Add parent directory to path for backend imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import backend modules
try:
    from config import (
        validate_config,
        TOPIC_DESCRIPTION,
        INITIAL_PARAMS,
        MAX_EXCHANGES,
        CANNOT_DEMONSTRATE,
        PRE_DEFINED_CONCEPTS,
        build_simulation_url
    )
    from state import create_initial_state, TeachingState
    from graph import continue_session, get_session_state
    
    BACKEND_AVAILABLE = True
    
except Exception as e:
    print(f"Backend import error: {e}")
    import traceback
    traceback.print_exc()
    BACKEND_AVAILABLE = False
    # Set defaults
    INITIAL_PARAMS = {"length": 5, "number_of_oscillations": 10}
    MAX_EXCHANGES = 6


def is_backend_available() -> bool:
    """Check if the backend is available."""
    return BACKEND_AVAILABLE


def create_new_session() -> Tuple[str, Dict[str, Any]]:
    """
    Create a new teaching session.
    
    Returns:
        Tuple of (thread_id, initial_state_from_backend)
    """
    if not BACKEND_AVAILABLE:
        raise RuntimeError("Backend not available")
    
    # Reload ALL modules to pick up environment variable changes
    import importlib
    import simulations_config
    import config
    import state as state_module
    import graph as graph_module
    from nodes import teacher, evaluator, strategy, trajectory, content_loader
    
    # Reload in dependency order (most fundamental first)
    importlib.reload(simulations_config)
    importlib.reload(config)
    importlib.reload(content_loader)
    importlib.reload(teacher)
    importlib.reload(evaluator)
    importlib.reload(strategy)
    importlib.reload(trajectory)
    importlib.reload(state_module)
    importlib.reload(graph_module)
    
    # Import fresh functions and values after reload
    from config import (
        validate_config,
        TOPIC_DESCRIPTION,
        INITIAL_PARAMS,
        TOPIC_TITLE,
        CURRENT_SIMULATION_ID
    )
    from state import create_initial_state
    from graph import start_session, reset_graph
    
    # Reset the graph to force recompile with new nodes
    reset_graph()
    
    # Validate config
    validate_config()
    
    print(f"🔄 Creating session for: {TOPIC_TITLE} ({CURRENT_SIMULATION_ID})")
    
    # Create unique session ID
    thread_id = f"streamlit_session_{uuid.uuid4().hex[:8]}"
    
    # Create initial state
    initial_state = create_initial_state(
        topic_description=TOPIC_DESCRIPTION,
        initial_params=INITIAL_PARAMS.copy()
    )
    
    # Start the session - runs until first interrupt (waiting for student input)
    state = start_session(initial_state, thread_id)
    
    return thread_id, state


def send_student_response(thread_id: str, response: str) -> Dict[str, Any]:
    """
    Send a student response and get the updated state.
    
    Args:
        thread_id: The session thread ID
        response: Student's response text
        
    Returns:
        Updated state dict
    """
    if not BACKEND_AVAILABLE:
        raise RuntimeError("Backend not available")
    
    # Import fresh continue_session to ensure we're using the reloaded graph
    from graph import continue_session as fresh_continue_session
    
    state = fresh_continue_session(response, thread_id)
    return state


def get_current_state(thread_id: str) -> Dict[str, Any]:
    """
    Get the current state of a session.
    
    Args:
        thread_id: The session thread ID
        
    Returns:
        Current state dict
    """
    if not BACKEND_AVAILABLE:
        return {}
    
    # Import fresh to ensure we're using the reloaded graph
    from graph import get_session_state as fresh_get_session_state
    
    return fresh_get_session_state(thread_id)


def extract_display_data(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract data from backend state for UI display.
    
    Args:
        state: Full backend state
        
    Returns:
        Dict with UI-friendly data
    """
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    
    # Get current concept info
    current_concept = None
    if current_idx < len(concepts):
        current_concept = concepts[current_idx]
    
    # Get parameter changes for comparison
    param_history = state.get("parameter_history", [])
    has_param_change = False
    previous_params = None
    current_params = state.get("current_params", INITIAL_PARAMS.copy())
    
    # Check if there was a recent parameter change (within the last response)
    if param_history:
        last_change = param_history[-1]
        # Debug: print param change info
        print(f"   🔎 DEBUG - Last param change: {last_change.get('parameter')} = {last_change.get('old_value')} → {last_change.get('new_value')}")
        print(f"   🔎 DEBUG - student_reaction: '{last_change.get('student_reaction', '')}'")
        
        # Only show comparison if the student hasn't reacted yet (empty reaction)
        if last_change.get("student_reaction", "") == "":
            has_param_change = True
            # Reconstruct previous params
            previous_params = current_params.copy()
            previous_params[last_change["parameter"]] = last_change["old_value"]
            print(f"   ✅ DEBUG - Will show simulation comparison!")
        else:
            print(f"   ❌ DEBUG - student_reaction filled, no comparison")
    else:
        print(f"   🔎 DEBUG - No param_history yet")
    
    return {
        # Teacher message
        "teacher_message": state.get("last_teacher_message", ""),
        
        # Progress info
        "current_concept_index": current_idx,
        "total_concepts": len(concepts),
        "current_concept": current_concept,
        "concepts": concepts,
        
        # Understanding
        "understanding_level": state.get("understanding_level", "none"),
        "understanding_reasoning": state.get("understanding_reasoning", ""),
        "trajectory_status": state.get("trajectory_status", "improving"),
        
        # Exchange info
        "exchange_count": state.get("exchange_count", 0),
        "max_exchanges": MAX_EXCHANGES,
        
        # Simulation params
        "current_params": current_params,
        "previous_params": previous_params,
        "has_param_change": has_param_change,
        "param_history": param_history,
        
        # Session status
        "session_complete": state.get("session_complete", False),
        "concept_complete": state.get("concept_complete", False),
        
        # Teaching context
        "strategy": state.get("strategy", "continue"),
        "teacher_mode": state.get("teacher_mode", "encouraging"),
        
        # Conversation history
        "conversation_history": state.get("conversation_history", []),
        
        # Quiz state
        "quiz_mode": state.get("quiz_mode", False),
        "quiz_questions": state.get("quiz_questions", []),
        "current_quiz_index": state.get("current_quiz_index", 0),
        "quiz_attempts": state.get("quiz_attempts", {}),
        "quiz_scores": state.get("quiz_scores", {}),
        "quiz_complete": state.get("quiz_complete", False),
        "quiz_evaluation": state.get("quiz_evaluation", {})
    }


def get_initial_params() -> Dict[str, Any]:
    """Get the initial simulation parameters."""
    if BACKEND_AVAILABLE:
        return INITIAL_PARAMS.copy()
    return {"length": 5, "number_of_oscillations": 10}


def get_concepts() -> list:
    """Get the pre-defined concepts."""
    if BACKEND_AVAILABLE:
        return PRE_DEFINED_CONCEPTS
    return []


def get_topic_description() -> str:
    """Get the topic description."""
    if BACKEND_AVAILABLE:
        return TOPIC_DESCRIPTION
    return "Time & Pendulums"


def build_sim_url(params: Dict[str, Any], autostart: bool = True) -> str:
    """Build simulation URL with parameters."""
    if BACKEND_AVAILABLE:
        return build_simulation_url(params, autostart)
    
    # Fallback URL building
    base_url = "https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html"
    url = f"{base_url}?length={params.get('length', 5)}&oscillations={params.get('number_of_oscillations', 10)}"
    if autostart:
        url += "&autoStart=true"
    return url


def submit_quiz_answer(thread_id: str, question_id: str, submitted_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit quiz answer and get evaluation.
    
    Directly runs quiz_evaluator_node without going through the full graph,
    which avoids checkpoint issues when testing quiz mode.
    
    Args:
        thread_id: The session thread ID
        question_id: ID of the question being answered
        submitted_params: Parameters from the simulation
        
    Returns:
        Updated state dict after evaluation
    """
    if not BACKEND_AVAILABLE:
        raise RuntimeError("Backend not available")
    
    from graph import compile_graph
    from nodes.quiz_evaluator import quiz_evaluator_node, quiz_teacher_node, quiz_router
    
    print("\n" + "="*60)
    print("📥 QUIZ SUBMISSION - Direct Evaluation")
    print("="*60)
    print(f"   Thread: {thread_id}")
    print(f"   Question: {question_id}")
    print(f"   Params: {submitted_params}")
    
    # Get graph and config
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    # Get current state
    current_snapshot = graph.get_state(config)
    current_state = dict(current_snapshot.values) if current_snapshot.values else {}
    
    # Check if we're in quiz mode
    if not current_state.get("quiz_mode", False):
        print("   ⚠️ Not in quiz mode - using regular continue_session")
        from graph import continue_session
        graph.update_state(config, {"submitted_parameters": submitted_params})
        return continue_session("", thread_id)
    
    print("   ✅ Quiz mode active - running direct evaluation")
    
    # Update state with submitted parameters
    current_state["submitted_parameters"] = submitted_params
    
    # Run quiz_evaluator_node directly
    print("\n" + "="*60)
    print("🔍 QUIZ EVALUATOR - Evaluating Submission")
    print("="*60)
    
    eval_updates = quiz_evaluator_node(current_state)
    
    # Merge updates into state
    for key, value in eval_updates.items():
        current_state[key] = value
    
    print(f"   ✓ Completed: quiz_evaluator")
    
    # Check if we need to present next question or end
    route_decision = quiz_router(current_state)
    print(f"   Route decision: {route_decision}")
    
    if route_decision == "quiz_teacher":
        # Run quiz_teacher_node to present next question or retry
        teacher_updates = quiz_teacher_node(current_state)
        for key, value in teacher_updates.items():
            current_state[key] = value
        print(f"   ✓ Completed: quiz_teacher")
    else:
        print(f"   ✓ Quiz complete!")
    
    # Save the updated state back to the graph
    graph.update_state(config, current_state, as_node="quiz_teacher")
    
    # Return the updated state
    return current_state
