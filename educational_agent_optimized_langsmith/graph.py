from langchain_core.runnables import RunnableConfig
import uuid
from typing import TypedDict, List, Dict, Any, Optional, Annotated
import os
import dotenv

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

# from langfuse import get_client
# from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.memory import InMemorySaver

from educational_agent_optimized.main_nodes_simulation_agent_no_mh import (
    start_node, apk_node, ci_node, ge_node,
    ar_node, tc_node, rlc_node, end_node,
)

# ▶ NEW: import simulation agent nodes
from educational_agent_optimized.simulation_nodes_no_mh_ge import (
    sim_concept_creator_node,
    sim_vars_node,
    sim_action_node,
    sim_expect_node,
    sim_execute_node,
    sim_observe_node,
    sim_insight_node,
    sim_reflection_node,
)

dotenv.load_dotenv(dotenv_path=".env", override=True)

# -----------------------------------------------------------------------------
# // 3. Define AgentState TypedDict
# -----------------------------------------------------------------------------
class AgentState(TypedDict, total=False):
    messages: Annotated[List[AnyMessage], add_messages]
    current_state: str
    last_user_msg: str
    agent_output: str
    asked_apk: bool
    asked_ci: bool
    asked_ge: bool
    asked_mh: bool
    asked_ar: bool
    asked_tc: bool
    asked_rlc: bool
    apk_tries: int
    ci_tries: int
    ge_tries: int
    mh_tries: int
    rlc_tries: int
    definition_echoed: bool
    sim_concepts: List[str]
    sim_total_concepts: int
    sim_current_idx: int
    concepts_completed: bool
    in_simulation: bool
    misconception_detected: bool
    retrieval_score: float
    transfer_success: bool
    last_correction: str
    quiz_score: float
    session_summary: Dict[str, Any]
    # NEW: Simulation-related state fields
    sim_variables: List[Dict[str, Any]]  # List of variable dictionaries for JSON serialization
    sim_action_config: Dict[str, Any]
    show_simulation: bool
    simulation_config: Dict[str, Any]
    # NEW: Memory optimization fields
    node_transitions: List[Dict[str, Any]]
    summary: str
    summary_last_index: int

# -----------------------------------------------------------------------------
# // 4. Initialize state and wrap helper
# -----------------------------------------------------------------------------
def _INIT(state: AgentState,config: RunnableConfig = None) -> AgentState:
    # state.setdefault("messages", [])
    # state.setdefault("last_user_msg", "")
    # state.setdefault("sim_concepts", [])
    # state.setdefault("sim_total_concepts", 0)
    # state.setdefault("sim_current_idx", 0)
    # state.setdefault("concepts_completed", False)
    # state.setdefault("in_simulation", False)
    
    # # Misconception and performance tracking
    # state.setdefault("misconception_detected", False)
    # state.setdefault("retrieval_score", 0.0)
    # state.setdefault("transfer_success", False)
    state.setdefault("last_correction", "")
    # state.setdefault("quiz_score", 0.0)
    # state.setdefault("session_summary", {})
    
    # # Simulation state - use dictionaries instead of Pydantic objects for serialization
    # state.setdefault("sim_variables", [])  # List of dict with keys: name, role, note
    state.setdefault("sim_action_config", {})
    state.setdefault("show_simulation", False)
    state.setdefault("simulation_config", {})
    # # NEW: Initialize memory optimization state
    # state.setdefault("node_transitions", [])
    state.setdefault("summary", "")
    state.setdefault("summary_last_index", 0)
    return state

def _wrap(fn):
    def inner(state: AgentState) -> AgentState:
        print(f"🔧 _WRAP DEBUG - Node processing started")
        print(f"📊 Messages count: {len(state.get('messages', []))}")
        
        # CAPTURE OLD STATE BEFORE PROCESSING
        old_state = state.get("current_state")
        
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], HumanMessage):
            text = msgs[-1].content or ""
            if text and text != state.get("last_user_msg"):
                state["last_user_msg"] = text
                print(f"📝 Updated last_user_msg: {text[:50]}...")
        
        # CALL THE ORIGINAL NODE FUNCTION
        result = fn(state)
        
        # Handle both full state returns (legacy) and partial state updates (LangGraph best practice)
        if isinstance(result, dict) and result.get("messages") is None:
            # Partial state update - merge with existing state (LangGraph best practice)
            print(f"🔄 _WRAP DEBUG - Merging partial state update with keys: {list(result.keys())}")
            state.update(result)
        else:
            # Full state return (legacy behavior) - update the original state dictionary
            state.update(result)
        
        st = state # Always use the original state reference
        
        # CAPTURE NEW STATE AFTER PROCESSING
        new_state = st.get("current_state")
        final_message_count = len(st.get("messages", []))
        
        # TRACK TRANSITION IF STATE CHANGED
        # The transition happens AFTER the current agent response is added
        if old_state != new_state and old_state is not None:
            transitions = st.setdefault("node_transitions", [])
            transitions.append({
                "from_node": old_state,
                "to_node": new_state,
                "transition_after_message_index": final_message_count,
            })
            print(f"🔄 NODE TRANSITION: {old_state} -> {new_state} after message {final_message_count}")
        
        print(f"🏁 _WRAP DEBUG - Node processing completed")
        print(f"📊 Final messages count: {final_message_count}")
        return st
    return inner

# Node wrappers (core)
def _START(s): return _wrap(start_node)(s)
def _APK(s):   return _wrap(apk_node)(s)
def _CI(s):    return _wrap(ci_node)(s)
def _GE(s):    return _wrap(ge_node)(s)
# def _MH(s):    return _wrap(mh_node)(s)
def _AR(s):    return _wrap(ar_node)(s)
def _TC(s):    return _wrap(tc_node)(s)
def _RLC(s):   return _wrap(rlc_node)(s)
def _END(s):   return _wrap(end_node)(s)

# NEW: Node wrappers (simulation)
def _SIM_CC(s):       return _wrap(sim_concept_creator_node)(s)
def _SIM_VARS(s):     return _wrap(sim_vars_node)(s)
def _SIM_ACTION(s):   return _wrap(sim_action_node)(s)
def _SIM_EXPECT(s):   return _wrap(sim_expect_node)(s)
def _SIM_EXECUTE(s):  return _wrap(sim_execute_node)(s)
def _SIM_OBSERVE(s):  return _wrap(sim_observe_node)(s)
def _SIM_INSIGHT(s):  return _wrap(sim_insight_node)(s)
# def _SIM_NEXT(s):     return _wrap(sim_next_concept_node)(s)
def _SIM_REFLECT(s):  return _wrap(sim_reflection_node)(s)

# -----------------------------------------------------------------------------
# // 5. Build the StateGraph
# -----------------------------------------------------------------------------
g = StateGraph(AgentState)
g.add_node("INIT", _INIT)
g.add_node("START", _START)
g.add_node("APK", _APK)
g.add_node("CI",  _CI)
g.add_node("GE",  _GE)
# g.add_node("MH",  _MH)
g.add_node("AR",  _AR)
g.add_node("TC",  _TC)
g.add_node("RLC", _RLC)
g.add_node("END", _END)

# ▶ NEW: Simulation nodes
g.add_node("SIM_CC", _SIM_CC)
g.add_node("SIM_VARS", _SIM_VARS)
g.add_node("SIM_ACTION", _SIM_ACTION)
g.add_node("SIM_EXPECT", _SIM_EXPECT)
g.add_node("SIM_EXECUTE", _SIM_EXECUTE)
g.add_node("SIM_OBSERVE", _SIM_OBSERVE)
g.add_node("SIM_INSIGHT", _SIM_INSIGHT)
# g.add_node("SIM_NEXT", _SIM_NEXT)
g.add_node("SIM_REFLECT", _SIM_REFLECT)

def _route(state: AgentState) -> str:
    return state.get("current_state")

# g.add_edge(START, "INIT")
# g.add_edge("INIT", "START")
g.add_edge(START,"START")

g.add_edge("START","APK")
# Core flow
g.add_conditional_edges("APK", _route, {"APK": "APK", "CI": "CI"})
g.add_conditional_edges("CI",  _route, {"CI": "CI","SIM_CC":"SIM_CC"})
# g.add_conditional_edges("GE",  _route, {"MH": "MH", "AR": "AR","GE": "GE"})
g.add_conditional_edges("GE",  _route, {"GE": "GE","SIM_VARS":"SIM_VARS"})
# g.add_conditional_edges("MH", _route,{"MH": "MH", "SIM_VARS": "SIM_VARS", "AR": "AR"})
# g.add_conditional_edges("MH", _route,{"MH": "MH", "SIM_VARS": "SIM_VARS"})
g.add_conditional_edges("AR", _route, {"AR": "AR","TC": "TC", "GE": "GE"})
# g.add_conditional_edges("AR", _route, {"AR": "AR","TC": "TC"})
g.add_conditional_edges("TC", _route, {"TC": "TC","RLC": "RLC"})
g.add_conditional_edges("RLC", _route, {"RLC": "RLC","END": "END"})
g.add_edge("END", END)

# Simulation flow edges
g.add_conditional_edges("SIM_CC", _route, {"GE": "GE"})
# g.add_edge("SIM_CC", "SIM_VARS")
g.add_edge("SIM_VARS", "SIM_ACTION")
g.add_edge("SIM_ACTION", "SIM_EXPECT")
g.add_edge("SIM_EXPECT", "SIM_EXECUTE")
g.add_edge("SIM_EXECUTE", "SIM_OBSERVE")
g.add_edge("SIM_OBSERVE", "SIM_INSIGHT")
g.add_edge("SIM_INSIGHT", "SIM_REFLECT")
g.add_edge("SIM_REFLECT", "AR")   # After simulation, go to AR to ask question about the concept

checkpointer = InMemorySaver()
# checkpointer = SqliteSaver.from_conn_string("sqlite:///./.lg_memory.db")

def build_graph():
    compiled = g.compile(
        checkpointer=checkpointer,
        # checkpointer=CHECKPOINTER,
        interrupt_after=[
            "START", "APK", "CI","GE", "AR", "TC", "RLC",
            # ▶ NEW: pause points for simulation path
            "SIM_CC", "SIM_VARS", "SIM_EXPECT",
            "SIM_EXECUTE", "SIM_OBSERVE", "SIM_INSIGHT",
            "SIM_REFLECT",
        ],
    )
    return compiled

graph = build_graph()
