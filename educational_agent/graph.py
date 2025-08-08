# educational_agent/graph.py
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.sqlite import SqliteSaver

# --- import your node functions exactly as they are ---
from educational_agent.nodes4_rag import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node, end_node,
    AgentState as _AgentStateDict  # if you defined one; we’ll define our own TypedDict anyway
)

# ----- Define a typed state for nicer diffs in Studio -----
class AgentState(TypedDict, total=False):
    # Routing
    current_state: str

    # IO
    last_user_msg: str
    agent_output: str
    history: List[Dict[str, str]]

    # First-pass flags
    _asked_apk: bool
    _asked_ci: bool
    _asked_ge: bool
    _asked_mh: bool
    _asked_ar: bool
    _asked_tc: bool
    _asked_rlc: bool

    # Pedagogy / metrics
    definition_echoed: bool
    misconception_detected: bool
    retrieval_score: float
    transfer_success: bool
    last_correction: Optional[str]

    # Summary
    session_summary: Dict[str, Any]

# ---- Wrap your functions (LangGraph merges returned dicts) ----
def _START(state: AgentState) -> AgentState: return start_node(state) or state
def _APK(state: AgentState) -> AgentState:   return apk_node(state) or state
def _CI(state: AgentState) -> AgentState:    return ci_node(state) or state
def _GE(state: AgentState) -> AgentState:    return ge_node(state) or state
def _MH(state: AgentState) -> AgentState:    return mh_node(state) or state
def _AR(state: AgentState) -> AgentState:    return ar_node(state) or state
def _TC(state: AgentState) -> AgentState:    return tc_node(state) or state
def _RLC(state: AgentState) -> AgentState:   return rlc_node(state) or state
def _END(state: AgentState) -> AgentState:   return end_node(state) or state

# ---- Build the graph ----
g = StateGraph(AgentState)

g.add_node("START", _START)
g.add_node("APK",   _APK)
g.add_node("CI",    _CI)
g.add_node("GE",    _GE)
g.add_node("MH",    _MH)
g.add_node("AR",    _AR)
g.add_node("TC",    _TC)
g.add_node("RLC",   _RLC)
g.add_node("END",   _END)

# Router: decide next hop from state["current_state"]
def _route(state: AgentState) -> str:
    return state.get("current_state", "APK")

g.add_edge(START,"START");
g.add_edge("START", "APK")
g.add_conditional_edges("APK", _route, {"APK": "APK", "CI": "CI"})
g.add_conditional_edges("CI",  _route, {"CI": "CI",  "GE": "GE"})
g.add_conditional_edges("GE",  _route, {"MH": "MH",  "AR": "AR"})
g.add_edge("MH", "AR")
g.add_edge("AR", "TC")
g.add_edge("TC", "RLC")
g.add_edge("RLC", "END")
g.add_edge("END", END)

# Checkpointer so Studio can pause/resume runs
checkpointer = SqliteSaver.from_conn_string("sqlite:///./.lg_memory.db")

# Final compiled graph object that Studio will import
graph = g.compile(checkpointer=checkpointer)
