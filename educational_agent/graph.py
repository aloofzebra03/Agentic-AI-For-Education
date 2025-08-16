from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage , AIMessage

import dotenv
dotenv.load_dotenv(dotenv_path=".env", override=True)

from educational_agent.nodes4_rag_studio import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node, end_node,
)

class AgentState(TypedDict, total=False):
    # Chat-compatible messages list
    messages: Annotated[List[AnyMessage], add_messages]

    current_state: str
    last_user_msg: str
    agent_output: str
    history: List[Dict[str, str]]
    _asked_apk: bool
    _asked_ci: bool
    _asked_ge: bool
    _asked_mh: bool
    _asked_ar: bool
    _asked_tc: bool
    _asked_rlc: bool
    definition_echoed: bool
    misconception_detected: bool
    retrieval_score: float
    transfer_success: bool
    last_correction: Optional[str]
    session_summary: Dict[str, Any]


def _INIT(state: AgentState) -> AgentState:
    state.setdefault("messages", [])
    # state["messages"].append(HumanMessage(content="Hi"))
    state.setdefault("history", [])
    state.setdefault("last_user_msg", "")
    state.setdefault("current_state", "START")
    return state


def _wrap(fn):
    def inner(state: AgentState) -> AgentState:
        # --- pull latest real user input from Studio ---
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], HumanMessage):
            text = (msgs[-1].content or "")
            if text and text != state.get("last_user_msg"):
                state["last_user_msg"] = text
                state.setdefault("history", []).append({"role":"user","content":text})

        # --- run node ---
        st = fn(state) or state

        # --- persist display text + log  ---
        out = (st.get("agent_output") or "").strip()
        if out:
            st.setdefault("history", []).append({
                "role": "assistant",
                "content": out,
                "node": st.get("current_state")
            })

        return st
    return inner



def _START(s): return _wrap(start_node)(s)
def _APK(s):   return _wrap(apk_node)(s)
def _CI(s):    return _wrap(ci_node)(s)
def _GE(s):    return _wrap(ge_node)(s)
def _MH(s):    return _wrap(mh_node)(s)
def _AR(s):    return _wrap(ar_node)(s)
def _TC(s):    return _wrap(tc_node)(s)
def _RLC(s):   return _wrap(rlc_node)(s)
def _END(s):   return _wrap(end_node)(s)


g = StateGraph(AgentState)

g.add_node("INIT", _INIT)
g.add_node("START", _START)
g.add_node("APK", _APK)
g.add_node("CI", _CI)
g.add_node("GE", _GE)
g.add_node("MH", _MH)
g.add_node("AR", _AR)
g.add_node("TC", _TC)
g.add_node("RLC", _RLC)
g.add_node("END", _END)

def _route(state: AgentState) -> str:
    return state.get("current_state", "APK")

g.add_edge(START, "INIT")
g.add_edge("INIT", "START")

g.add_edge("START", "APK")
g.add_conditional_edges("APK", _route, {"APK": "APK", "CI": "CI"})
g.add_conditional_edges("CI",  _route, {"CI": "CI",  "GE": "GE"})
g.add_conditional_edges("GE",  _route, {"MH": "MH",  "AR": "AR","GE": "GE"})
g.add_edge("MH", "AR")
g.add_edge("AR", "TC")
g.add_edge("TC", "RLC")
g.add_edge("RLC", "END")
g.add_edge("END", END)

checkpointer = SqliteSaver.from_conn_string("sqlite:///./.lg_memory.db")

graph = g.compile(checkpointer=checkpointer,interrupt_after=["START","APK","CI","GE","AR","TC","RLC"])

