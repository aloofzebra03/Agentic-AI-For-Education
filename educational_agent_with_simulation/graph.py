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

from educational_agent_with_simulation.main_nodes_simulation_agent import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node, end_node,
)

# ▶ NEW: import simulation agent nodes
from educational_agent_with_simulation.simulation_nodes import (
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
    _asked_apk: bool
    _asked_ci: bool
    _asked_ge: bool
    _asked_mh: bool
    _asked_ar: bool
    _asked_tc: bool
    _asked_rlc: bool
    _apk_tries: int
    _ci_tries: int
    _mh_tries: int
    _rlc_tries: int
    definition_echoed: bool
    sim_concepts: List[str]
    sim_total_concepts: int
    sim_current_idx: int
    concepts_completed: bool
    in_simulation: bool
    misconception_detected: bool
    retrieval_score: float
    transfer_success: bool
    last_correction: Optional[str]
    quiz_score: float
    session_summary: Dict[str, Any]
    # NEW: Simulation-related state fields
    sim_variables: List[Any]
    sim_action_config: Dict[str, Any]
    show_simulation: bool
    simulation_config: Dict[str, Any]

# -----------------------------------------------------------------------------
# // 4. Initialize state and wrap helper
# -----------------------------------------------------------------------------
def _INIT(state: AgentState,config: RunnableConfig = None) -> AgentState:
    state.setdefault("messages", [])
    state.setdefault("last_user_msg", "")
    state.setdefault("current_state", "START")
    state.setdefault("sim_concepts", [])
    state.setdefault("sim_total_concepts", 0)
    state.setdefault("sim_current_idx", 0)
    state.setdefault("concepts_completed", False)
    state.setdefault("in_simulation", False)
    # NEW: Initialize simulation state
    state.setdefault("sim_variables", [])
    state.setdefault("sim_action_config", {})
    state.setdefault("show_simulation", False)
    state.setdefault("simulation_config", {})
    return state

def _wrap(fn):
    def inner(state: AgentState) -> AgentState:
        print(f"🔧 _WRAP DEBUG - Node processing started")
        print(f"📊 Messages count: {len(state.get('messages', []))}")
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], HumanMessage):
            text = msgs[-1].content or ""
            if text and text != state.get("last_user_msg"):
                state["last_user_msg"] = text
                print(f"📝 Updated last_user_msg: {text[:50]}...")
        st = fn(state)
        print(f"🏁 _WRAP DEBUG - Node processing completed")
        print(f"📊 Final messages count: {len(st.get('messages', []))}")
        return st
    return inner

# Node wrappers (core)
def _START(s): return _wrap(start_node)(s)
def _APK(s):   return _wrap(apk_node)(s)
def _CI(s):    return _wrap(ci_node)(s)
def _GE(s):    return _wrap(ge_node)(s)
def _MH(s):    return _wrap(mh_node)(s)
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
g.add_node("MH",  _MH)
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

g.add_edge(START, "INIT")
g.add_edge("INIT", "START")

g.add_edge("START","APK")
# Core flow
g.add_conditional_edges("APK", _route, {"APK": "APK", "CI": "CI"})
g.add_conditional_edges("CI",  _route, {"CI": "CI","SIM_CC":"SIM_CC"})
g.add_conditional_edges("GE",  _route, {"MH": "MH", "AR": "AR","GE": "GE"})
g.add_conditional_edges("MH", _route,{"SIM_VARS": "SIM_VARS", "AR": "AR"})
g.add_conditional_edges("AR", _route, {"AR": "AR","TC": "TC", "GE": "GE"})
g.add_conditional_edges("TC", _route, {"TC": "TC","RLC": "RLC"})
g.add_conditional_edges("RLC", _route, {"RLC": "RLC","END": "END"})
g.add_edge("END", END)

# Simulation flow edges
g.add_conditional_edges("SIM_CC", _route, {"GE": "GE"})
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
        # checkpointer=checkpointer,
        # checkpointer=CHECKPOINTER,
        interrupt_after=[
            "START", "APK", "CI", "GE","MH", "AR", "TC", "RLC",
            # ▶ NEW: pause points for simulation path
            "SIM_CC", "SIM_VARS", "SIM_ACTION", "SIM_EXPECT",
            "SIM_EXECUTE", "SIM_OBSERVE", "SIM_INSIGHT",
            "SIM_REFLECT",
        ],
    )
    return compiled

graph = build_graph()
