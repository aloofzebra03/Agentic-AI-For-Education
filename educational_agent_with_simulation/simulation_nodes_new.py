# simulation_nodes.py
import json
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field, conlist
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from educational_agent.config_rag import concept_pkg
from educational_agent.shared_utils import (
    AgentState,
    add_ai_message_to_conversation,
    llm_with_history,
    build_prompt_from_template,
    extract_json_block,
)

# ─────────────────────────────────────────────────────────────────────
# Simulation moves
# ─────────────────────────────────────────────────────────────────────

SIM_MOVES: Dict[str, Dict[str, str]] = {
    "SIM_CC":     {"goal": "Propose 1–5 distinct, independently variable core concepts for simulation.", "constraints": "Clear, learner-friendly; testable via observable changes."},
    "SIM_VARS":   {"goal": "List variables; mark independent/dependent/controls.", "constraints": "Only relevant variables; concise."},
    "SIM_ACTION": {"goal": "Describe a single, testable change to perform.", "constraints": "Alter one independent variable; keep controls fixed."},
    "SIM_EXPECT": {"goal": "Elicit the learner's prediction and brief why.", "constraints": "No leading hints; accept 'not sure'."},
    "SIM_EXECUTE":{"goal": "Perform/narrate the action steps.", "constraints": "Describe observable effects only; no interpretation."},
    "SIM_OBSERVE":{"goal": "Ask for raw observations from the learner.", "constraints": "Allow multiple valid answers; don't judge yet."},
    "SIM_INSIGHT":{"goal": "Map observation → principle; compare with prediction.", "constraints": "Reinforce why it happened; ≤3 sentences."},
    "SIM_REFLECT":{"goal": "Synthesize learning across the simulated concept(s).", "constraints": "Encourage metacognition; concise bullets."},
}

# ─────────────────────────────────────────────────────────────────────
# Pydantic response models + parsers (same style as main nodes)
# ─────────────────────────────────────────────────────────────────────

# SIM_CC: 1–5 concepts
class SimConcepts(BaseModel):
    concepts: conlist(str, min_length=1, max_length=5)


# SIM_VARS: declare variables
class SimVariable(BaseModel):
    name: str
    role: Literal["independent", "dependent", "control"]
    note: Optional[str] = None

class SimVarsResponse(BaseModel):
    variables: conlist(SimVariable, min_length=2)
    prompt_to_learner: str

# SIM_ACTION
class SimActionResponse(BaseModel):
    action: str
    rationale: str
    prompt_to_learner: str

# SIM_EXPECT
class SimExpectResponse(BaseModel):
    question: str
    hint: Optional[str] = None

# SIM_EXECUTE
class SimExecuteResponse(BaseModel):
    steps: conlist(str, min_length=1)
    what_to_watch: str

# SIM_OBSERVE
class SimObserveResponse(BaseModel):
    observation_prompt: str
    expected_observations: List[str]

# SIM_INSIGHT
class SimInsightResponse(BaseModel):
    micro_explanation: str
    compared_to_prediction: str

# SIM_REFLECT
class SimReflectResponse(BaseModel):
    bullets: conlist(str, min_length=2, max_length=5)
    closing_prompt: str

sim_cc_parser = PydanticOutputParser(pydantic_object=SimConcepts)
sim_vars_parser = PydanticOutputParser(pydantic_object=SimVarsResponse)
sim_action_parser = PydanticOutputParser(pydantic_object=SimActionResponse)
sim_expect_parser = PydanticOutputParser(pydantic_object=SimExpectResponse)
sim_execute_parser = PydanticOutputParser(pydantic_object=SimExecuteResponse)
sim_observe_parser = PydanticOutputParser(pydantic_object=SimObserveResponse)
sim_insight_parser = PydanticOutputParser(pydantic_object=SimInsightResponse)
sim_reflect_parser = PydanticOutputParser(pydantic_object=SimReflectResponse)


# ─────────────────────────────────────────────────────────────────────
# Node implementations (each uses build_prompt_from_template directly)
# ─────────────────────────────────────────────────────────────────────

def sim_concept_creator_node(state: AgentState) -> AgentState:
    """
    SIM_CC: Generate 1–5 independently variable, testable concepts.
    Stores:
      - sim_concepts: List[str]
      - sim_total_concepts: int
      - sim_current_idx: int
    Handover: set current_state="GE" so graph routes to your GE node.
    """

    context = json.dumps(SIM_MOVES["SIM_CC"], indent=2)
    system_prompt = f"""Current node: SIM_CC (Simulation Concept Creator)

Concept in focus: "{concept_pkg.title}"

Context:
{context}

Task:
Return JSON ONLY with 1–5 clear, independent, testable simulation concepts for a class 7 learner.

Guidelines:
- Keep each concept short (≤15 words), concrete, and experimentally manipulable.
- They must be independently variable (changing one doesn't implicitly change the others).
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=True,
        parser=sim_cc_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimConcepts = sim_cc_parser.parse(json_text)

    # Save & speak
    state["sim_concepts"] = parsed.concepts
    state["sim_total_concepts"] = len(parsed.concepts)
    state["sim_current_idx"] = 0

    speak = (
        "We'll explore these concepts one by one:\n"
        + "\n".join([f"{i+1}. {c}" for i, c in enumerate(parsed.concepts)])
        + f"\n\nNow let's start with the first concept: '{parsed.concepts[0]}'"
    )
    add_ai_message_to_conversation(state, speak)
    state["agent_output"] = speak

    # Handover to GE (your graph: SIM_CC → GE)
    state["current_state"] = "GE"
    return state


def sim_vars_node(state: AgentState) -> AgentState:
    """
    SIM_VARS: List variables (independent/dependent/control) for current concept.
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    concept = concepts[idx]

    context = json.dumps(SIM_MOVES["SIM_VARS"], indent=2)
    system_prompt = f"""Current node: SIM_VARS (Variables Declaration)

We are on Simulation Concept #{idx+1}: "{concept}"

Context:
{context}

Task:
Respond with JSON ONLY: declare variables (independent/dependent/control) that matter to this concept, and a short prompt to the learner to confirm/ask questions.

Keep it concise and age-appropriate.
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=sim_vars_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimVarsResponse = sim_vars_parser.parse(json_text)

    lines = ["Here are the variables we'll use:"]
    for v in parsed.variables:
        note = f" — {v.note}" if v.note else ""
        lines.append(f"- {v.name} ({v.role}){note}")
    lines.append(parsed.prompt_to_learner)
    msg = "\n".join(lines)

    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg
    state["current_state"] = "SIM_ACTION"
    return state


def sim_action_node(state: AgentState) -> AgentState:
    """
    SIM_ACTION: Propose one concrete action to isolate the concept.
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    concept = concepts[idx]

    context = json.dumps(SIM_MOVES["SIM_ACTION"], indent=2)
    system_prompt = f"""Current node: SIM_ACTION (Single Manipulation)

We are on Simulation Concept #{idx+1}: "{concept}"

Context:
{context}

Task:
Return JSON ONLY describing:
- 'action': one specific manipulation on the independent variable
- 'rationale': why this isolates the concept
- 'prompt_to_learner': a quick check like "Shall we try this? (yes/no)"
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=True,
        parser=sim_action_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimActionResponse = sim_action_parser.parse(json_text)

    msg = f"{parsed.action}\n\nWhy this works: {parsed.rationale}\n{parsed.prompt_to_learner}"
    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg
    state["current_state"] = "SIM_EXPECT"
    return state


def sim_expect_node(state: AgentState) -> AgentState:
    """
    SIM_EXPECT: Ask the learner's prediction before executing.
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    concept = concepts[idx]

    context = json.dumps(SIM_MOVES["SIM_EXPECT"], indent=2)
    system_prompt = f"""Current node: SIM_EXPECT (Prediction)

We are on Simulation Concept #{idx+1}: "{concept}"

Context:
{context}

Task:
Return JSON ONLY with:
- 'question': the prediction prompt (direct and short)
- 'hint': optional tiny nudge (or null)
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=True,
        parser=sim_expect_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimExpectResponse = sim_expect_parser.parse(json_text)

    hint = f"\n(Hint: {parsed.hint})" if parsed.hint else ""
    msg = f"{parsed.question}{hint}"
    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg
    state["current_state"] = "SIM_EXECUTE"
    return state


def sim_execute_node(state: AgentState) -> AgentState:
    """
    SIM_EXECUTE: Execute the simulation action.
    """
    msg = "[SIM_EXECUTE] (skeleton) Let's execute the action steps; watch for observable effects. We are only testing and this feature is not available yet."
    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg
    state["current_state"] = "SIM_OBSERVE"
    return state


def sim_observe_node(state: AgentState) -> AgentState:
    """
    SIM_OBSERVE: Ask for raw observations (no judging).
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    concept = concepts[idx]

    context = json.dumps(SIM_MOVES["SIM_OBSERVE"], indent=2)
    system_prompt = f"""Current node: SIM_OBSERVE (What did you notice?)

We are on Simulation Concept #{idx+1}: "{concept}"

Context:
{context}

Task:
Return JSON ONLY with:
- 'observation_prompt': a short, neutral request for what the learner saw
- 'expected_observations': 2–5 strings (internal guide, not printed verbatim later)
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=sim_observe_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimObserveResponse = sim_observe_parser.parse(json_text)

    add_ai_message_to_conversation(state, parsed.observation_prompt)
    state["agent_output"] = parsed.observation_prompt
    state["sim_expected_observations"] = parsed.expected_observations
    state["current_state"] = "SIM_INSIGHT"
    return state


def sim_insight_node(state: AgentState) -> AgentState:
    """
    SIM_INSIGHT: Micro-explanation + compare to prediction.
    (Graph will route to SIM_REFLECT next.)
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    concept = concepts[idx]

    context = json.dumps(SIM_MOVES["SIM_INSIGHT"], indent=2)
    system_prompt = f"""Current node: SIM_INSIGHT (Why did that happen?)

We are on Simulation Concept #{idx+1}: "{concept}"

Context:
{context}

Task:
Return JSON ONLY with:
- 'micro_explanation': ≤3 sentences connecting observation → principle
- 'compared_to_prediction': 1 sentence linking to the learner's prediction (agree or differ)
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=sim_insight_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimInsightResponse = sim_insight_parser.parse(json_text)

    msg = f"{parsed.micro_explanation}\n{parsed.compared_to_prediction}"
    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg

    # Next hop per your graph: SIM_REFLECT
    state["current_state"] = "SIM_REFLECT"
    return state


def sim_reflection_node(state: AgentState) -> AgentState:
    """
    SIM_REFLECT: Short synthesis across sim concept(s).
    Handover: set current_state="AR" to ask question about the concept.
    """
    idx = state.get("sim_current_idx", 0)
    concepts = state.get("sim_concepts", [])
    current_concept = concepts[idx] if concepts and idx < len(concepts) else "current concept"

    context = json.dumps(SIM_MOVES["SIM_REFLECT"], indent=2)
    system_prompt = f"""Current node: SIM_REFLECT (Synthesis)

We just completed a simulation for: "{current_concept}"

Context:
{context}

Task:
Return JSON ONLY with:
- 'bullets': 2–5 concise takeaways from this simulation
- 'closing_prompt': a short reflective question to the learner about what they learned
"""

    final_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=True,
        parser=sim_reflect_parser,
    )
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    parsed: SimReflectResponse = sim_reflect_parser.parse(json_text)

    msg = "Quick recap from our simulation:\n" + "\n".join([f"• {b}" for b in parsed.bullets]) + f"\n\n{parsed.closing_prompt}"
    add_ai_message_to_conversation(state, msg)
    state["agent_output"] = msg

    # Handover to AR to ask a question about this concept
    state["current_state"] = "AR"
    state["_asked_ar"] = False  # Reset AR flag for this concept
    return state
