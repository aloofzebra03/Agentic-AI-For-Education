"""
API Integration Layer
=====================
Bridges FastAPI to the LangGraph teaching agent backend.
Converts between API format and internal state representation.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple

from simulation_to_concept.config import build_simulation_url, CURRENT_SIMULATION_ID
from simulation_to_concept.simulations_config import get_simulation, get_simulation_list


# ═══════════════════════════════════════════════════════════════════════
# ENVIRONMENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

def set_simulation_environment(simulation_id: str):
    """
    Set environment variable for simulation selection.
    
    This updates the environment so that config.py loads the correct
    simulation when modules are reloaded.
    """
    os.environ['SIMULATION_ID'] = simulation_id
    print(f"🔧 Environment set to simulation: {simulation_id}")


# ═══════════════════════════════════════════════════════════════════════
# STATE FORMATTING
# ═══════════════════════════════════════════════════════════════════════

def format_concept_info(concept: Dict[str, Any]) -> Dict[str, Any]:
    """Format a single concept for API response"""
    return {
        "id": concept.get("id"),
        "title": concept.get("title"),
        "description": concept.get("description"),
        "key_insight": concept.get("key_insight"),
        "related_params": concept.get("related_params", [])
    }


def format_api_response(thread_id: str, state: Dict[str, Any], simulation_id: str) -> Dict[str, Any]:
    """
    Convert LangGraph state to API response format.
    
    This takes the raw state from the teaching agent and packages it
    in the format expected by the Android app (matching sample_api_responses.json).
    
    Args:
        thread_id: The session thread ID
        state: Raw state from LangGraph
        simulation_id: Which simulation this session is for
        
    Returns:
        Formatted API response dictionary
    """
    # Get simulation configuration
    sim_config = get_simulation(simulation_id)
    if not sim_config:
        raise ValueError(f"Unknown simulation: {simulation_id}")
    
    # Extract current parameters
    current_params = state.get('current_params', {})
    
    # Build current simulation URL with correct simulation_id
    sim_url = build_simulation_url(current_params, autostart=True, simulation_id=simulation_id)
    
    # Check for parameter changes
    param_change = None
    param_history = state.get('parameter_history', [])
    if param_history:
        last_change = param_history[-1]
        
        # Build before and after URLs with correct simulation_id
        before_params = current_params.copy()
        before_params[last_change['parameter']] = last_change['old_value']
        before_url = build_simulation_url(before_params, autostart=True, simulation_id=simulation_id)
        after_url = sim_url
        
        param_change = {
            "parameter": last_change['parameter'],
            "before": last_change['old_value'],
            "after": last_change['new_value'],
            "reason": last_change.get('reason', 'Parameter adjustment for demonstration'),
            "before_url": before_url,
            "after_url": after_url
        }
    
    # Format concepts
    concepts = state.get('concepts', [])
    current_idx = state.get('current_concept_index', 0)
    
    # Get current concept info
    current_concept = None
    if current_idx < len(concepts):
        current_concept = format_concept_info(concepts[current_idx])
    
    # Format all concepts
    all_concepts = [format_concept_info(c) for c in concepts]
    
    # Check if all concepts completed
    all_completed = current_idx >= len(concepts)
    
    # Check for previous concept (during transitions)
    previous_concept = None
    if current_idx > 0 and current_idx <= len(concepts):
        previous_concept = {
            "id": concepts[current_idx - 1].get("id"),
            "title": concepts[current_idx - 1].get("title"),
            "completed": True
        }
    
    # Build response following sample_api_responses.json format
    response = {
        "session_id": thread_id,
        "simulation": {
            "id": simulation_id,
            "title": sim_config['title'],
            "html_url": sim_url,
            "current_params": current_params,
            "param_change": param_change
        },
        "concepts": {
            "total": len(concepts),
            "current_index": current_idx,
            "current_concept": current_concept,
            "all_concepts": all_concepts,
            "all_completed": all_completed,
            "previous_concept": previous_concept
        },
        "teacher_message": {
            "text": state.get('last_teacher_message', ''),
            "timestamp": datetime.now().isoformat() + 'Z',
            "requires_response": not state.get('session_complete', False),
            "correction_made": state.get('correction_made', False),
            "asks_for_reasoning": state.get('asks_for_reasoning', False),
            "concept_transition": state.get('concept_transition', False),
            "session_ending": state.get('session_complete', False)
        },
        "learning_state": {
            "understanding_level": state.get('understanding_level', 'none'),
            "understanding_reasoning": state.get('understanding_reasoning'),
            "exchange_count": state.get('exchange_count', 0),
            "concept_complete": state.get('concept_complete', False),
            "session_complete": state.get('session_complete', False),
            "strategy": state.get('strategy', 'continue'),
            "teacher_mode": state.get('teacher_mode', 'encouraging'),
            "trajectory_status": state.get('trajectory_status'),
            "needs_deeper": state.get('needs_deeper', False)
        }
    }
    
    # Add summary if session is complete
    if state.get('session_complete', False):
        response["summary"] = {
            "concepts_mastered": current_idx,
            "total_exchanges": sum(
                1 for msg in state.get('conversation_history', []) 
                if msg.get('role') == 'student'
            ),
            "parameter_changes_made": len(param_history),
            "understanding_progression": state.get('understanding_trajectory', [])
        }
    
    return response


# ═══════════════════════════════════════════════════════════════════════
# MAIN API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def create_teaching_session(simulation_id: str, student_id: str = None) -> Tuple[str, Dict[str, Any]]:
    """
    Create a new teaching session for specified simulation.
    
    Args:
        simulation_id: Which simulation to use
        student_id: Optional student identifier
        
    Returns:
        Tuple of (session_id, formatted_api_response)
    """
    # Validate simulation exists
    if not get_simulation(simulation_id):
        from simulation_to_concept.simulations_config import SIMULATIONS
        available = list(SIMULATIONS.keys())
        raise ValueError(
            f"Invalid simulation_id: '{simulation_id}'. "
            f"Available: {', '.join(available)}"
        )
    
    # Set simulation in environment (for any modules that still use it)
    set_simulation_environment(simulation_id)
    
    # Import directly from backend modules (bypass backend_integration.py)
    import uuid
    from simulation_to_concept.config import validate_config
    from simulation_to_concept.state import create_initial_state
    from simulation_to_concept.graph import start_session
    
    # Get simulation config dynamically (NOT from cached module constants!)
    sim_config = get_simulation(simulation_id)
    topic_description = sim_config['description']
    initial_params = sim_config['initial_params']
    
    print(f"\n{'='*60}")
    print(f"🚀 Creating new teaching session")
    print(f"   Simulation: {simulation_id}")
    print(f"   Topic: {sim_config['title']}")
    if student_id:
        print(f"   Student: {student_id}")
    print(f"{'='*60}")
    
    # Validate config
    validate_config()
    
    # Create unique session ID
    thread_id = f"api_session_{uuid.uuid4().hex[:8]}"
    
    # Create initial state with simulation_id for downstream nodes
    initial_state = create_initial_state(
        topic_description=topic_description,
        initial_params=initial_params.copy(),
        simulation_id=simulation_id  # Pass simulation_id for content_loader
    )
    
    # Start the session - runs until first interrupt
    state = start_session(initial_state, thread_id)
    
    print(f"✅ Session created: {thread_id}")
    print(f"📝 Initial message: {state.get('last_teacher_message', '')[:80]}...")
    
    # Format for API
    response = format_api_response(thread_id, state, simulation_id)
    
    return thread_id, response


def process_student_input(session_id: str, student_response: str) -> Dict[str, Any]:
    """
    Process student's response and return formatted API response.
    
    Args:
        session_id: The session thread ID
        student_response: What the student said
        
    Returns:
        Formatted API response dictionary
    """
    # Import directly from backend modules
    from simulation_to_concept.graph import continue_session
    
    print(f"\n{'='*60}")
    print(f"💬 Processing student response")
    print(f"   Session: {session_id}")
    print(f"   Student said: {student_response[:80]}...")
    print(f"{'='*60}")
    
    # Get simulation from environment
    simulation_id = os.environ.get('SIMULATION_ID', 'simple_pendulum')
    
    # Continue conversation using graph
    state = continue_session(student_response, session_id)
    
    print(f"✅ Response generated")
    print(f"📝 Teacher: {state.get('last_teacher_message', '')[:80]}...")
    print(f"📊 Understanding: {state.get('understanding_level', 'unknown')}")
    
    # Check for parameter changes
    param_history = state.get('parameter_history', [])
    if param_history:
        last_change = param_history[-1]
        print(f"⚙️  Parameter changed: {last_change['parameter']} "
              f"{last_change['old_value']} → {last_change['new_value']}")
    
    # Format for API
    response = format_api_response(session_id, state, simulation_id)
    
    return response


def get_session_info(session_id: str) -> Dict[str, Any]:
    """
    Get current session state.
    
    Args:
        session_id: The session thread ID
        
    Returns:
        Formatted API response dictionary
    """
    # Import directly from backend modules
    from simulation_to_concept.graph import get_session_state
    
    print(f"\n{'='*60}")
    print(f"🔍 Retrieving session state")
    print(f"   Session: {session_id}")
    print(f"{'='*60}")
    
    # Get state from graph
    state = get_session_state(session_id)
    
    if not state:
        raise KeyError(f"Session {session_id} not found")
    
    # Determine simulation from environment
    simulation_id = os.environ.get('SIMULATION_ID', 'simple_pendulum')
    
    print(f"✅ Session found")
    print(f"📊 Concept: {state.get('current_concept_index', 0) + 1} of {len(state.get('concepts', []))}")
    print(f"💬 Exchanges: {state.get('exchange_count', 0)}")
    
    # Format for API
    response = format_api_response(session_id, state, simulation_id)
    
    return response


# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_available_simulations() -> list:
    """Get list of available simulation IDs (just the string IDs)"""
    from simulations_config import SIMULATIONS
    return list(SIMULATIONS.keys())


def validate_simulation_id(simulation_id: str) -> bool:
    """Check if simulation ID is valid"""
    return get_simulation(simulation_id) is not None


def submit_quiz_answer(session_id: str, question_id: str, submitted_parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit quiz answer and get evaluation with feedback.
    
    Directly runs quiz_evaluator_node without going through the full graph,
    which avoids checkpoint issues when in quiz mode.
    
    Args:
        session_id: The session thread ID
        question_id: ID of question being answered
        submitted_parameters: Parameters from simulation
        
    Returns:
        Quiz evaluation response dictionary
    """
    from simulation_to_concept.graph import compile_graph, get_session_state
    from simulation_to_concept.nodes.quiz_evaluator import quiz_evaluator_node, quiz_teacher_node, quiz_router
    from simulation_to_concept.quiz_rules import calculate_quiz_progress
    
    print(f"\n{'='*60}")
    print(f"🎯 Processing quiz submission")
    print(f"   Session: {session_id}")
    print(f"   Question: {question_id}")
    print(f"   Parameters: {submitted_parameters}")
    print(f"{'='*60}")
    
    # Get current state to verify quiz mode
    graph = compile_graph()
    config = {"configurable": {"thread_id": session_id}}
    
    current_snapshot = graph.get_state(config)
    state = dict(current_snapshot.values) if current_snapshot.values else {}
    
    if not state:
        raise KeyError(f"Session {session_id} not found")
    
    if not state.get('quiz_mode', False):
        raise ValueError("Session is not in quiz mode")
    
    print("   ✅ Quiz mode active - running direct evaluation")
    
    # Update state with submitted parameters
    state["submitted_parameters"] = submitted_parameters
    
    # Run quiz_evaluator_node directly
    print("\n" + "="*60)
    print("🔍 QUIZ EVALUATOR - Evaluating Submission")
    print("="*60)
    
    eval_updates = quiz_evaluator_node(state)
    
    # Merge updates into state
    for key, value in eval_updates.items():
        state[key] = value
    
    print(f"   ✓ Completed: quiz_evaluator")
    
    # Check if we need to present next question or end
    route_decision = quiz_router(state)
    print(f"   Route decision: {route_decision}")
    
    if route_decision == "quiz_teacher":
        # Run quiz_teacher_node to present next question or retry
        teacher_updates = quiz_teacher_node(state)
        for key, value in teacher_updates.items():
            state[key] = value
        print(f"   ✓ Completed: quiz_teacher")
    else:
        print(f"   ✓ Quiz complete!")
    
    # Save the updated state back to the graph
    graph.update_state(config, state, as_node="quiz_teacher")
    
    # Extract evaluation result
    evaluation = state.get('quiz_evaluation', {})
    quiz_scores = state.get('quiz_scores', {})
    quiz_questions = state.get('quiz_questions', [])
    current_index = state.get('current_quiz_index', 0)
    quiz_complete = state.get('quiz_complete', False)
    
    print(f"✅ Evaluation complete")
    print(f"   Score: {evaluation.get('score', 0)} | Status: {evaluation.get('status', 'UNKNOWN')}")
    print(f"   Quiz Complete: {quiz_complete}")
    
    # Calculate progress
    progress = calculate_quiz_progress(quiz_scores, len(quiz_questions))
    
    # Format next question if available and quiz not complete
    next_question = None
    if not quiz_complete and current_index < len(quiz_questions):
        next_q = quiz_questions[current_index]
        next_question = {
            "id": next_q['id'],
            "challenge": next_q['challenge']
        }
    
    # Build response
    response = {
        "session_id": session_id,
        "question_id": evaluation.get('question_id', question_id),
        "score": evaluation.get('score', 0.0),
        "status": evaluation.get('status', 'WRONG'),
        "feedback": evaluation.get('feedback', 'Evaluation failed'),
        "attempt": evaluation.get('attempt', 1),
        "allow_retry": evaluation.get('allow_retry', False),
        "quiz_complete": quiz_complete,
        "quiz_progress": progress,
        "next_question": next_question
    }
    
    return response
