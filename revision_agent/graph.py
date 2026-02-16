# graph.py
"""
Revision Agent Graph - State definition, node wrappers, and routing logic.

Based on the learning agent's graph structure with optimizations for tracking
node transitions and conversation summarization.
"""

from langchain_core.runnables import RunnableConfig
import uuid
from typing import TypedDict, List, Dict, Any, Optional, Annotated
import os
import dotenv

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver

# Import revision agent nodes
from revision_agent.nodes import (
    revision_start_node,
    question_presenter_node,
    answer_evaluator_node,
    ge_node,
    ar_node,
    revision_end_node,
)

dotenv.load_dotenv(dotenv_path=".env", override=True)


# ══════════════════════════════════════════════════════════════════════════════
# STATE DEFINITION
# ══════════════════════════════════════════════════════════════════════════════

class RevisionAgentState(TypedDict, total=False):
    """State for the revision agent"""
    
    # Core message handling
    messages: Annotated[List[AnyMessage], add_messages]
    current_state: str
    last_user_msg: str
    agent_output: str
    
    # Revision-specific state
    chapter: str
    question_bank: List[Dict]
    current_question_index: int
    questions_total: int
    questions_correct_first_try: int
    questions_needed_explanation: int
    concepts_for_review: List[str]
    current_question: Dict
    current_concept: str  # For GE/AR (extracted by evaluator when answer is wrong)
    
    # Kannada support
    is_kannada: bool
    language: str
    
    # Node tracking (for GE/AR)
    asked_ge: bool
    asked_ar: bool
    
    # Optimization fields (same as learning agent)
    node_transitions: List[Dict[str, Any]]  # Track state transitions
    summary: str  # Conversation summary
    summary_last_index: int  # Last message index summarized


# ══════════════════════════════════════════════════════════════════════════════
# NODE WRAPPER PATTERN (from learning agent)
# ══════════════════════════════════════════════════════════════════════════════

def _wrap(fn):
    """
    Wrapper function to track node transitions and update last_user_msg.
    
    Same pattern as learning agent for consistency and optimization tracking.
    """
    def inner(state: RevisionAgentState) -> RevisionAgentState:
        print(f"🔧 _WRAP DEBUG - Node processing started")
        print(f"📊 Messages count: {len(state.get('messages', []))}")
        
        # CAPTURE OLD STATE BEFORE PROCESSING
        old_state = state.get("current_state")
        
        # Update last_user_msg from latest HumanMessage
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], HumanMessage):
            print(f"📝 Last message is HumanMessage")
            text = msgs[-1].content or ""
            if text and text != state.get("last_user_msg"):
                print(f"📝 Detected new user message: {text[:50]}...")
                state["last_user_msg"] = text
                print(f"📝 Updated last_user_msg: {text[:50]}...")
        
        # CALL THE ORIGINAL NODE FUNCTION
        result = fn(state)
        
        # Handle both full state returns and partial state updates
        if isinstance(result, dict) and result.get("messages") is None:
            # Partial state update - merge with existing state
            print(f"🔄 _WRAP DEBUG - Merging partial state update with keys: {list(result.keys())}")
            state.update(result)
        else:
            # Full state return - update the original state dictionary
            state.update(result)
        
        st = state  # Always use the original state reference
        
        # CAPTURE NEW STATE AFTER PROCESSING
        new_state = st.get("current_state")
        
        final_message_count = len(st.get("messages", []))
        
        # TRACK TRANSITION IF STATE CHANGED
        if old_state != new_state and old_state is not None:
            transitions = st.setdefault("node_transitions", [])
            transitions.append({
                "from_node": old_state,
                "to_node": new_state,
                "transition_after_message_index": final_message_count,
            })
            print(f"🔄 NODE TRANSITION: {old_state} → {new_state} after message {final_message_count}")
        
        print(f"🏁 _WRAP DEBUG - Node processing completed")
        print(f"📊 Final messages count: {final_message_count}")
        return st
    return inner


# Wrap all nodes
def _REV_START(s): return _wrap(revision_start_node)(s)
def _Q_PRESENTER(s): return _wrap(question_presenter_node)(s)
def _EVALUATOR(s): return _wrap(answer_evaluator_node)(s)
def _GE(s): return _wrap(ge_node)(s)
def _AR(s): return _wrap(ar_node)(s)
def _REV_END(s): return _wrap(revision_end_node)(s)


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH CONSTRUCTION
# ══════════════════════════════════════════════════════════════════════════════

g = StateGraph(RevisionAgentState)

# Add nodes
g.add_node("REVISION_START", _REV_START)
g.add_node("QUESTION_PRESENTER", _Q_PRESENTER)
g.add_node("EVALUATOR", _EVALUATOR)
g.add_node("GE", _GE)
g.add_node("AR", _AR)
g.add_node("REVISION_END", _REV_END)


# Routing logic
def _route(state: RevisionAgentState) -> str:
    """Simple routing based on current_state"""
    return state.get("current_state")


# Add edges
g.add_edge(START, "REVISION_START")

# REVISION_START → QUESTION_PRESENTER
g.add_conditional_edges("REVISION_START", _route, {"QUESTION_PRESENTER": "QUESTION_PRESENTER"})

# QUESTION_PRESENTER → EVALUATOR or REVISION_END
g.add_conditional_edges(
    "QUESTION_PRESENTER",
    _route,
    {"EVALUATOR": "EVALUATOR", "REVISION_END": "REVISION_END"}
)

# EVALUATOR → QUESTION_PRESENTER (correct) or GE (incorrect)
g.add_conditional_edges(
    "EVALUATOR",
    _route,
    {"QUESTION_PRESENTER": "QUESTION_PRESENTER", "GE": "GE"}
)

# GE → GE (keep explaining) or AR (test understanding)
g.add_conditional_edges("GE", _route, {"GE": "GE", "AR": "AR"})

# AR → GE (still struggling) or QUESTION_PRESENTER (understood, move on)
g.add_conditional_edges(
    "AR",
    _route,
    {"GE": "GE", "QUESTION_PRESENTER": "QUESTION_PRESENTER"}
)

# REVISION_END → END
g.add_edge("REVISION_END", END)


# ══════════════════════════════════════════════════════════════════════════════
# CHECKPOINTER
# ══════════════════════════════════════════════════════════════════════════════

# checkpointer = SqliteSaver.from_conn_string("sqlite:///./revision_agent/.lg_memory.db")
checkpointer = InMemorySaver()


# ══════════════════════════════════════════════════════════════════════════════
# BUILD GRAPH
# ══════════════════════════════════════════════════════════════════════════════

def build_graph():
    """Build and compile the revision agent graph"""
    compiled = g.compile(
        # checkpointer=checkpointer,
        interrupt_after=[
            "REVISION_START",      # Pause after welcome message
            "QUESTION_PRESENTER",  # Pause after presenting each question
            "GE",                  # Pause after explanation
            "AR",                  # Pause after followup question
            "REVISION_END",        # Pause after summary
        ],
    )
    return compiled


# Create the graph instance
graph = build_graph()

print("✅ Revision agent graph initialized successfully!")
