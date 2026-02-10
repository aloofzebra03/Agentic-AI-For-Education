"""Handler functions for special autosuggestions.

This module contains handler functions that generate pedagogical responses
when users click special handling autosuggestions:
- Hint: Provides contextual hints without revealing answers
- Explain Simpler: Rephrases explanations in simpler language
- Example: Provides concrete examples
"""

from typing import Dict

from utils.shared_utils import (
    extract_json_block,
    llm_with_history,
    build_prompt_from_template_optimized,
    translate_if_kannada,
)


def handle_hint(state) -> Dict:
    """Generate a contextual hint without revealing the answer.
    
    Creates a supportive 2-3 sentence hint that helps students think
    through the problem without giving away the full answer.
    
    Args:
        state: AgentState dictionary
        
    Returns:
        Partial state update with 'agent_output' set to generated hint
    """
    current_node = state.get("current_state", "UNKNOWN")
    
    hint_prompt = """The student requested a hint to help them answer the question.

Generate a supportive hint (2-3 sentences) that:
1. Helps the student think through the problem without revealing the full answer
2. References what was just discussed in the conversation
3. Uses tone and encouragement appropriate to the conversation context

Be natural and conversational."""
    
    # Build prompt - conversation history included automatically, no autosuggestions needed
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=hint_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node=current_node,
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    hint_content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Translate and update agent output
    translated_hint = translate_if_kannada(state, hint_content)
    
    print("=" * 80)
    print("🔍 HANDLER: HINT GENERATED")
    print("=" * 80)
    print(f"💡 HINT: {translated_hint[:100]}...")
    print("=" * 80)
    
    return {"agent_output": translated_hint}


def handle_explain_simpler(state) -> Dict:
    """Rephrase the last explanation in simpler language.
    
    Rephrases the agent's last explanation using very simple words
    and shorter sentences suitable for a class 7 student.
    
    Args:
        state: AgentState dictionary
        
    Returns:
        Partial state update with 'agent_output' set to simplified explanation
    """
    current_node = state.get("current_state", "UNKNOWN")
    
    simplify_prompt = """The student asked for a simpler explanation.

Rephrase the last explanation you gave using:
1. Very simple words suitable for a class 7 student
2. Shorter sentences
3. Everyday examples if helpful

Keep the same meaning but make it much easier to understand. Use tone and follow-up appropriate to the conversation context."""
    
    # Build prompt - conversation history included automatically, no autosuggestions needed
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=simplify_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node=current_node,
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    simple_content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Translate and update agent output
    translated_simple = translate_if_kannada(state, simple_content)
    
    print("=" * 80)
    print("🔍 HANDLER: SIMPLIFIED EXPLANATION")
    print("=" * 80)
    print(f"📝 SIMPLIFIED: {translated_simple[:100]}...")
    print("=" * 80)
    
    return {"agent_output": translated_simple}


def handle_example(state) -> Dict:
    """Provide a concrete example to illustrate the concept.
    
    Generates a simple, concrete example using everyday situations
    that a class 7 student can relate to.
    
    Args:
        state: AgentState dictionary
        
    Returns:
        Partial state update with 'agent_output' set to generated example
    """
    concept_title = state.get("concept_title", "")
    current_node = state.get("current_state", "UNKNOWN")
    
    example_prompt = f"""The student asked for an example.

Provide a simple, concrete example related to '{concept_title}' that:
1. Is brief (2-3 sentences)
2. Uses everyday situations a class 7 student can relate to
3. Helps illustrate what was just discussed

Use tone and follow-up appropriate to the conversation context."""
    
    # Build prompt - conversation history included automatically, no autosuggestions needed
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=example_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node=current_node,
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    example_content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Translate and update agent output
    translated_example = translate_if_kannada(state, example_content)
    
    print("=" * 80)
    print("🔍 HANDLER: EXAMPLE PROVIDED")
    print("=" * 80)
    print(f"🎯 EXAMPLE: {translated_example[:100]}...")
    print("=" * 80)
    
    return {"agent_output": translated_example}

def handle_dynamic_suggestion(state: AgentState) -> AgentState:
    """Process dynamic autosuggestion based on student level and their specific request."""
    student_level = state.get("student_level", "medium")
    dynamic_request = state.get("last_user_msg", "")
    current_node = state.get("current_state", "UNKNOWN")
    
    # Level-specific context for tailored responses
    level_instructions = {
        "low": "Use very simple language, short sentences, and provide step-by-step guidance. Avoid complex terminology.",
        "medium": "Use clear explanations with moderate complexity. Balance detail with accessibility.",
        "advanced": "Provide deeper insights, encourage critical thinking, and explore nuances of the concept."
    }
    
    instruction = level_instructions.get(student_level, level_instructions["medium"])
    
    dynamic_prompt = f"""The student (ability level: {student_level}) asked: "{dynamic_request}"

Task: Respond to their specific request keeping in mind they are a {student_level}-level student.
{instruction}

Your response should:
1. Be brief (2-3 sentences) and directly address what they asked
2. Reference the ongoing conversation context
3. Use tone and follow-up appropriate to the conversation flow

Be natural and supportive.and follow-up appropriate to the conversation context."""
    
    # Build prompt - conversation history included automatically, no autosuggestions needed
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=dynamic_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node=current_node,
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    dynamic_content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Translate once and update agent output
    translated_dynamic = translate_if_kannada(state, dynamic_content)
    state["agent_output"] = translated_dynamic
    
    print("=" * 80)
    print("🔍 HANDLER: DYNAMIC SUGGESTION PROCESSED")
    print("=" * 80)
    print(f"🎯 STUDENT_LEVEL: {student_level}")
    print(f"💬 REQUEST: {dynamic_request}")
    print(f"📝 RESPONSE: {translated_dynamic[:100]}...")
    print("=" * 80)
    
    return state
