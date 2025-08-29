from langchain_core.runnables import RunnableConfig
import uuid
from typing import TypedDict, List, Dict, Any, Optional, Annotated
import os
import dotenv

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
# from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

# from langfuse import get_client
# from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.memory import InMemorySaver

import operator

from educational_agent.nodes4_rag_studio import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node, end_node,
)

dotenv.load_dotenv(dotenv_path=".env", override=True)

# langfuse = get_client()  
# if not langfuse.auth_check():
#     raise RuntimeError("Langfuse auth failed – check your .env keys")

# langfuse_handler = CallbackHandler()

# -----------------------------------------------------------------------------
# 3. Define AgentState TypedDict
# -----------------------------------------------------------------------------
class AgentState(TypedDict, total=False):
    messages: Annotated[List[AnyMessage], add_messages]
    current_state: str
    last_user_msg: str
    agent_output: str
    history: Annotated[List[Dict[str, Any]],operator.add]
    _asked_apk: bool
    _asked_ci: bool
    _asked_ge: bool
    _asked_mh: bool
    _asked_ar: bool
    _asked_tc: bool
    _asked_rlc: bool
    _ci_tries: int
    _rlc_tries: int
    definition_echoed: bool
    misconception_detected: bool
    retrieval_score: float
    transfer_success: bool
    last_correction: Optional[str]
    quiz_score: float
    session_summary: Dict[str, Any]

# -----------------------------------------------------------------------------
# 4. Initialize state and wrap helper
# -----------------------------------------------------------------------------
def _INIT(state: AgentState,config: RunnableConfig = None) -> AgentState:
    state.setdefault("messages", [])
    state.setdefault("history", [])
    state.setdefault("last_user_msg", "")
    state.setdefault("current_state", "START")
    return state

def _wrap(fn):
    def inner(state: AgentState) -> AgentState:
        # 1. Capture latest user input
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], HumanMessage):
            text = msgs[-1].content or ""
            if text and text != state.get("last_user_msg"):
                state["last_user_msg"] = text

        st = fn(state)

        updates = {}
        out = st.get("agent_output")
        if out:
            updates["history"] = [{
                "role": "assistant",
                "content": out,
                "node": st.get("current_state"),
            }]

        if updates:
            return {**st, **updates}
        return st
    return inner

# Node wrappers
def _START(s): return _wrap(start_node)(s)
def _APK(s):   return _wrap(apk_node)(s)
def _CI(s):    return _wrap(ci_node)(s)
def _GE(s):    return _wrap(ge_node)(s)
def _MH(s):    return _wrap(mh_node)(s)
def _AR(s):    return _wrap(ar_node)(s)
def _TC(s):    return _wrap(tc_node)(s)
def _RLC(s):   return _wrap(rlc_node)(s)
def _END(s):   return _wrap(end_node)(s)

# -----------------------------------------------------------------------------
# 5. Build the StateGraph
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

def _route(state: AgentState) -> str:
    return state.get("current_state", "CI")

g.add_edge(START, "INIT")
g.add_edge("INIT", "START")
g.add_edge("START", "APK")
g.add_conditional_edges("APK", _route, {"APK": "APK", "CI": "CI"})
g.add_conditional_edges("CI",  _route, {"CI": "CI", "GE": "GE"})
g.add_conditional_edges("GE",  _route, {"MH": "MH", "AR": "AR","GE": "GE"})
g.add_edge("MH", "AR")
g.add_conditional_edges("AR", _route, {"AR": "AR","TC": "TC"})
g.add_conditional_edges("TC", _route, {"TC": "TC","RLC": "RLC"})
g.add_conditional_edges("RLC", _route, {"RLC": "RLC","END": "END"})
g.add_edge("END", END)

# checkpointer = SqliteSaver.from_conn_string("sqlite:///./.lg_memory.db")
CHECKPOINTER = InMemorySaver()


def build_graph():
    compiled = g.compile(
        # checkpointer=checkpointer,
        checkpointer=CHECKPOINTER,
        interrupt_after=["START", "APK", "CI", "GE", "AR", "TC", "RLC"],
    )
    return compiled

graph = build_graph()
