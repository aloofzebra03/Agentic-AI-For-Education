# simulation_nodes.py

import json
from typing import Dict

from langchain_core.messages import HumanMessage, AIMessage

# Import shared utilities and AgentState from the parent educational_agent package
from educational_agent.shared_utils import (
    AgentState,
    add_ai_message_to_conversation,
    llm_with_history,
    build_prompt_from_template,
    extract_json_block,
    PEDAGOGICAL_MOVES
)

# ─── Simulation Agent: States & Parsers ─────────────────────────

# New simulation-specific states
#   SIM_CC        : Concept Creator Agent (generate 3 core concepts)
#   SIM_VARS      : Mention variables at play
#   SIM_ACTION    : State action to be performed
#   SIM_EXPECT    : Ask expected outcome
#   SIM_EXECUTE   : Execute action
#   SIM_OBSERVE   : Ask observations
#   SIM_INSIGHT   : Mention insights
#   SIM_NEXT      : Repeat for Concept 2 & 3 controller
#   SIM_REFLECT   : Reflection & summary

SIM_NODE_ORDER = ["SIM_VARS", "SIM_ACTION", "SIM_EXPECT",
                  "SIM_EXECUTE", "SIM_OBSERVE", "SIM_INSIGHT"]

SIM_MOVES: Dict[str, Dict[str, str]] = {
    "SIM_CC":     {"goal": "Propose 3 distinct, independently variable core concepts.", "constraints": "Clear, learner-friendly language."},
    "SIM_VARS":   {"goal": "List variables; mark which are held constant.", "constraints": "Only relevant variables; concise."},
    "SIM_ACTION": {"goal": "Describe the single, testable change.", "constraints": "Alter key variable(s) only; isolate concept."},
    "SIM_EXPECT": {"goal": "Elicit prediction and brief why.", "constraints": "No leading hints; accept 'not sure'."},
    "SIM_EXECUTE":{"goal": "Perform the action in the sim.", "constraints": "Show observable effects; no interpretation."},
    "SIM_OBSERVE":{"goal": "Collect raw observations.", "constraints": "Allow multiple valid answers; no feedback yet."},
    "SIM_INSIGHT":{"goal": "Map observation → principle; compare to prediction.", "constraints": "Reinforce why it happened."},
    "SIM_NEXT":   {"goal": "Advance to next concept.", "constraints": "Proceed only after insights captured."},
    "SIM_REFLECT":{"goal": "Synthesize learning across concepts.", "constraints": "Encourage metacognition; concise summary."},
}

# ─── Simulation Agent Node Stubs (no logic, structure only) ─────────────────────

def sim_concept_creator_node(state: AgentState) -> AgentState:
    """SIM_CC: Generates 3 core concepts for simulation-based learning."""
    state.setdefault("sim_concepts", [])
    state.setdefault("sim_current_idx", 0)
    state.setdefault("sim_per_concept_data", {})
    state.setdefault("sim_total_concepts", 3)

    # Use the shared utilities to create a more sophisticated response
    context = json.dumps(SIM_MOVES["SIM_CC"], indent=2)
    system_prompt = f"""You are an educational simulation agent. Your task is to design 3 distinct core concepts for simulation-based learning.

Context: {context}

Generate 3 core concepts that can be explored through interactive simulation. Each concept should:
1. Be independently variable (changing one doesn't automatically change others)
2. Be testable through observable changes
3. Use clear, learner-friendly language
4. Be suitable for a class 7 student

Present the concepts clearly and prepare to begin with Concept #1."""

    # Build final prompt using shared template utility
    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False
    )
    
    # Use shared LLM utility
    resp = llm_with_history(state, final_prompt)
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Use shared conversation utility
    add_ai_message_to_conversation(state, content)
    
    state["agent_output"] = content
    state["current_state"] = "SIM_VARS"
    return state


def sim_vars_node(state: AgentState) -> AgentState:
    """SIM_VARS: Mention variables at play and identify constants."""
    idx = state.get("sim_current_idx", 0)
    
    context = json.dumps(SIM_MOVES["SIM_VARS"], indent=2)
    system_prompt = f"""You are working on Concept #{idx+1} in a simulation-based learning session.

Context: {context}

Your task: List the variables that are relevant to this concept. Clearly mark which variables will be held constant during our simulation and which ones we might change.

Be concise and learner-friendly. Focus only on the most relevant variables for understanding the core concept."""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,  # Include student's latest response about the concept
        include_instructions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    add_ai_message_to_conversation(state, content)
    
    state["agent_output"] = content
    state["current_state"] = "SIM_ACTION"
    return state


def sim_action_node(state: AgentState) -> AgentState:
    """SIM_ACTION: State action to be performed (skeleton)."""
    idx = state.get("sim_current_idx", 0)
    placeholder = f"[SIM_ACTION] (skeleton) Concept #{idx+1}: describe single, testable change."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_EXPECT"
    return state


def sim_expect_node(state: AgentState) -> AgentState:
    """SIM_EXPECT: Ask expected outcome (skeleton)."""
    idx = state.get("sim_current_idx", 0)
    placeholder = f"[SIM_EXPECT] (skeleton) Concept #{idx+1}: prompt prediction + why."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_EXECUTE"
    return state


def sim_execute_node(state: AgentState) -> AgentState:
    """SIM_EXECUTE: Execute action (skeleton)."""
    idx = state.get("sim_current_idx", 0)
    placeholder = f"[SIM_EXECUTE] (skeleton) Concept #{idx+1}: perform action; show observable effect."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_OBSERVE"
    return state


def sim_observe_node(state: AgentState) -> AgentState:
    """SIM_OBSERVE: Ask observations (skeleton)."""
    idx = state.get("sim_current_idx", 0)
    placeholder = f"[SIM_OBSERVE] (skeleton) Concept #{idx+1}: capture raw observations."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_INSIGHT"
    return state


def sim_insight_node(state: AgentState) -> AgentState:
    """SIM_INSIGHT: Mention insights (skeleton)."""
    idx = state.get("sim_current_idx", 0)
    placeholder = f"[SIM_INSIGHT] (skeleton) Concept #{idx+1}: map observations to principle; compare with prediction."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_NEXT"
    return state


def sim_next_concept_node(state: AgentState) -> AgentState:
    """SIM_NEXT: Controller to move across concepts (skeleton)."""
    total = state.get("sim_total_concepts", 3)
    idx = state.get("sim_current_idx", 0)

    if idx + 1 < total:
        state["sim_current_idx"] = idx + 1
        placeholder = f"[SIM_NEXT] (skeleton) Proceeding to Concept #{state['sim_current_idx']+1}."
        add_ai_message_to_conversation(state, placeholder)
        state["agent_output"] = placeholder
        state["current_state"] = "SIM_VARS"
        return state

    placeholder = "[SIM_NEXT] (skeleton) All concepts done. Moving to Reflection."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "SIM_REFLECT"
    return state


def sim_reflection_node(state: AgentState) -> AgentState:
    """SIM_REFLECT: Reflection & summary (skeleton)."""
    placeholder = "[SIM_REFLECT] (skeleton) Reflection & summary across concepts."
    add_ai_message_to_conversation(state, placeholder)
    state["agent_output"] = placeholder
    state["current_state"] = "END"
    return state
