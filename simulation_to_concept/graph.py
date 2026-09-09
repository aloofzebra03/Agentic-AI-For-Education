"""
LangGraph Definition for Version 3 Teaching Agent
=================================================
Defines the graph structure, routing logic, and execution helpers.

Graph Flow:
    ┌─────────────────┐
    │ content_loader  │ (Start - extracts concepts)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    teacher      │◄────────────────────────────┐
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   [INTERRUPT]   │ (Wait for student input)   │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   evaluator     │                             │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   trajectory    │                             │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │    strategy     │─────────────────────────────┘
    └────────┬────────┘          (if not complete)
             │
             ▼ (if session_complete)
    ┌─────────────────┐
    │      END        │
    └─────────────────┘
"""

from typing import Dict, Any
import os
import dotenv

from langgraph.graph import StateGraph, END
from utils.postgres_checkpointer import get_shared_checkpointer

from simulation_to_concept.state import TeachingState

# Load environment variables
dotenv.load_dotenv(dotenv_path=".env", override=True)
from simulation_to_concept.nodes import (
    content_loader_node,
    teacher_node,
    understanding_evaluator_node,
    trajectory_analyzer_node,
    strategy_selector_node
)
from simulation_to_concept.nodes.quiz_evaluator import (
    quiz_initializer_node,
    quiz_teacher_node,
    quiz_evaluator_node,
    quiz_router
)


# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL CHECKPOINTER (PostgreSQL)
# ═══════════════════════════════════════════════════════════════════════════

_compiled_graph = None

# PostgreSQL is mandatory so sessions are never silently made non-persistent.
_checkpointer = get_shared_checkpointer()


# ═══════════════════════════════════════════════════════════════════════════
# ROUTING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def route_after_strategy(state: TeachingState) -> str:
    """
    Route after strategy selector.
    
    Priority order:
    1. If all concepts taught and NOT in quiz mode → quiz_initializer
    2. If session complete → END
    3. Otherwise → back to teacher
    """
    session_complete = state.get("session_complete", False)
    quiz_mode = state.get("quiz_mode", False)
    
    # Check if all concepts have been taught
    concepts = state.get("concepts", [])
    current_concept_index = state.get("current_concept_index", 0)
    all_concepts_taught = current_concept_index >= len(concepts)
    
    # If all concepts taught and not yet in quiz mode, start quiz
    if all_concepts_taught and not quiz_mode:
        print("\n🔀 [ROUTING] All concepts taught → quiz_initializer")
        return "quiz_initializer"
    
    if session_complete:
        print("\n🔀 [ROUTING] Session complete → END")
        return END
    else:
        print("\n🔀 [ROUTING] Continue teaching → teacher")
        return "teacher"


# ═══════════════════════════════════════════════════════════════════════════
# GRAPH CREATION
# ═══════════════════════════════════════════════════════════════════════════

def create_teaching_graph() -> StateGraph:
    """Create the adaptive teaching workflow graph."""
    
    workflow = StateGraph(TeachingState)
    
    # Add teaching nodes
    workflow.add_node("content_loader", content_loader_node)
    workflow.add_node("teacher", teacher_node)
    workflow.add_node("evaluator", understanding_evaluator_node)
    workflow.add_node("trajectory", trajectory_analyzer_node)
    workflow.add_node("strategy", strategy_selector_node)
    
    # Add quiz nodes
    workflow.add_node("quiz_initializer", quiz_initializer_node)
    workflow.add_node("quiz_teacher", quiz_teacher_node)
    workflow.add_node("quiz_evaluator", quiz_evaluator_node)
    
    # Set entry point
    workflow.set_entry_point("content_loader")
    
    # Define teaching flow edges
    workflow.add_edge("content_loader", "teacher")
    # Teacher → [INTERRUPT] → Evaluator (interrupt handled in compile)
    workflow.add_edge("teacher", "evaluator")
    workflow.add_edge("evaluator", "trajectory")
    workflow.add_edge("trajectory", "strategy")
    
    # Conditional routing after strategy (teaching → quiz or continue teaching)
    workflow.add_conditional_edges(
        "strategy",
        route_after_strategy,
        {
            "teacher": "teacher",
            "quiz_initializer": "quiz_initializer",
            END: END
        }
    )
    
    # Define quiz flow edges
    workflow.add_edge("quiz_initializer", "quiz_teacher")
    # Quiz Teacher → [INTERRUPT] → Quiz Evaluator (interrupt handled in compile)
    workflow.add_edge("quiz_teacher", "quiz_evaluator")
    
    # Conditional routing after quiz evaluation (retry/next/end)
    workflow.add_conditional_edges(
        "quiz_evaluator",
        quiz_router,
        {
            "quiz_teacher": "quiz_teacher",
            END: END
        }
    )
    
    return workflow


def compile_graph(force_recompile: bool = False):
    """Compile graph with checkpointer and interrupt points (singleton)."""
    global _compiled_graph, _checkpointer
    
    if _compiled_graph is None or force_recompile:
        # Continue using the shared persistent checkpointer when recompiling.
        if force_recompile:
            _checkpointer = get_shared_checkpointer()
        
        print("\n" + "="*60)
        print("🔧 COMPILING TEACHING GRAPH")
        print("="*60)
        
        workflow = create_teaching_graph()
        _compiled_graph = workflow.compile(
            checkpointer=_checkpointer,
            interrupt_before=["evaluator", "quiz_evaluator"]  # Pause for student input
        )
        
        print("✅ Graph compiled with:")
        print("   • PostgresSaver checkpointer")
        print("   • Interrupt before: evaluator, quiz_evaluator")
        print("   • Teaching Flow: content_loader → teacher → [WAIT] → evaluator → trajectory → strategy → [loop]")
        print("   • Quiz Flow: strategy → quiz_initializer → quiz_teacher → [WAIT] → quiz_evaluator → [retry/next/END]")
    
    return _compiled_graph


def reset_graph():
    """Force reset the compiled graph. Call this when simulation changes."""
    global _compiled_graph, _checkpointer
    _compiled_graph = None
    _checkpointer = get_shared_checkpointer()
    print("🔄 Graph reset - will recompile on next use")


# ═══════════════════════════════════════════════════════════════════════════
# EXECUTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def start_session(initial_state: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
    """
    Start a new teaching session.
    
    Runs the graph until it hits the interrupt point (waiting for student input).
    
    Args:
        initial_state: Starting state with topic_description and initial_params
        thread_id: Unique ID for this session
        
    Returns:
        Current state after teacher's first message
    """
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "="*60)
    print(f"🚀 STARTING SESSION: {thread_id}")
    print("="*60)
    
    # Run until interrupt
    for event in graph.stream(initial_state, config=config):
        for node_name in event.keys():
            print(f"   ✓ Completed: {node_name}")
    
    # Get full state
    snapshot = graph.get_state(config)
    return dict(snapshot.values)


def continue_session(student_response: str, thread_id: str, student_changed_params: dict = None) -> Dict[str, Any]:
    """
    Continue session with student's response.
    
    Updates state with student response and continues graph execution.
    
    Args:
        student_response: What the student said
        thread_id: Session ID
        student_changed_params: Optional dict of params the student manually changed
                                in the simulation this turn. E.g. {"length": 3}.
        
    Returns:
        Updated state after processing and teacher's next message
    """
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "="*60)
    print("📥 PROCESSING STUDENT RESPONSE")
    print("="*60)
    print(f"   Response: \"{student_response[:100]}...\"" if len(student_response) > 100 else f"   Response: \"{student_response}\"")
    if student_changed_params:
        print(f"   🎛️ Student changed params: {student_changed_params}")
    
    # Check current state before updating
    current_state = graph.get_state(config)
    print(f"   DEBUG: Before update - next nodes = {current_state.next}")
    
    # Build state update — always include student_response
    state_update = {"student_response": student_response}
    
    # Inject student-changed params if provided
    if student_changed_params:
        state_update["student_changed_params"] = student_changed_params
        state_update["student_changed_params_this_turn"] = True
        print(f"   🎛️ Injecting student_changed_params into state: {student_changed_params}")
    else:
        # Always reset the flag each turn so it doesn't persist from previous turns
        state_update["student_changed_params"] = {}
        state_update["student_changed_params_this_turn"] = False
    
    # Update state with student response - preserve the current checkpoint position
    if current_state.next:
        # Use as_node to preserve the checkpoint position
        last_node = current_state.next[0] if current_state.next else None
        if last_node:
            # Get the node that ran before the interrupt
            # If next is quiz_evaluator, we came from quiz_teacher
            # If next is evaluator, we came from teacher
            as_node_map = {
                "quiz_evaluator": "quiz_teacher",
                "evaluator": "teacher"
            }
            as_node = as_node_map.get(last_node, None)
            if as_node:
                print(f"   DEBUG: Updating state as_node={as_node}")
                graph.update_state(config, state_update, as_node=as_node)
            else:
                graph.update_state(config, state_update)
        else:
            graph.update_state(config, state_update)
    else:
        graph.update_state(config, state_update)
    
    # Check state after updating
    updated_state = graph.get_state(config)
    print(f"   DEBUG: After update - next nodes = {updated_state.next}")
    
    # Continue execution
    for event in graph.stream(None, config=config):
        for node_name in event.keys():
            print(f"   ✓ Completed: {node_name}")
    
    # Get full state
    snapshot = graph.get_state(config)
    return dict(snapshot.values)


def get_session_state(thread_id: str) -> Dict[str, Any]:
    """Get current state of a session."""
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)
    return dict(snapshot.values) if snapshot.values else {}
