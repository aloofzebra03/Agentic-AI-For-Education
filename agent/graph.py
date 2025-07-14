from langgraph.graph import StateGraph
from .nodes2 import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node,
    rct_node, end_node, AgentState
)


def build_agent_graph() -> StateGraph[AgentState]:
    builder = StateGraph(AgentState)

    # Register all nodes
    builder.add_node("START", start_node)
    builder.add_node("APK",   apk_node)
    builder.add_node("CI",    ci_node)
    builder.add_node("GE",    ge_node)
    builder.add_node("MH",    mh_node)
    builder.add_node("AR",    ar_node)
    builder.add_node("TC",    tc_node)
    builder.add_node("RLC",   rlc_node)
    builder.add_node("RCT",   rct_node)
    builder.add_node("END",   end_node)

    # Define static transitions only (no Lambdas)
    builder.add_edge("START", "APK")
    builder.add_edge("APK",   "CI")
    builder.add_edge("CI",    "GE")
    builder.add_edge("GE",    "MH")
    builder.add_edge("GE",    "AR")
    builder.add_edge("MH",    "AR")
    builder.add_edge("AR",    "GE")
    builder.add_edge("AR",    "TC")
    builder.add_edge("TC",    "RLC")
    builder.add_edge("RLC",   "RCT")
    builder.add_edge("RCT",   "END")

    builder.set_entry_point("START")
    return builder.compile()
