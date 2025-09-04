# shared_utils.py
"""
Shared utilities for educational agents.
Contains common helper functions used by both traditional nodes and simulation nodes.
"""

import os
import json
import re
from typing import Dict, Optional, Any
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from educational_agent.config_rag import concept_pkg
from educational_agent.Creating_Section_Text.retriever import retrieve_docs
from educational_agent.Filtering_GT.filter_utils import filter_relevant_section
from educational_agent.Creating_Section_Text.schema import NextSectionChoice

dotenv.load_dotenv(dotenv_path=".env", override=True)

# Type alias for AgentState - flexible to work with different state structures
AgentState = Dict[str, Any]

def extract_json_block(text: str) -> str:
    """Extract JSON from text, handling various formats including markdown code blocks."""
    s = text.strip()

    # 🔍 JSON EXTRACTION INPUT 🔍
    print("=" * 60)
    print("🔧 JSON EXTRACTION - INPUT TEXT")
    print("=" * 60)
    print(f"📄 INPUT_LENGTH: {len(s)} characters")
    print(f"📄 INPUT_PREVIEW: {s[:200]}...")
    print("=" * 60)

    # 1) Try to find a fenced code block containing JSON (language tag optional)
    m = re.search(r"```(?:json)?\s*({.*?})\s*```", s, flags=re.DOTALL | re.IGNORECASE)
    if m:
        result = m.group(1).strip()
        print("🎯 JSON EXTRACTED - METHOD: Fenced code block")
        print(f"📦 EXTRACTED_JSON: {result}")
        print("=" * 60)
        return result

    # 2) Try to find the first balanced JSON object in the text
    start = s.find("{")
    if start != -1:
        depth = 0
        in_str = False
        esc = False
        for i, ch in enumerate(s[start:], start=start):
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        result = s[start:i+1].strip()
                        print("🎯 JSON EXTRACTED - METHOD: Balanced braces")
                        print(f"📦 EXTRACTED_JSON: {result}")
                        print("=" * 60)
                        return result

    # 3) Nothing found — return original (let parser raise)
    print("⚠️ JSON EXTRACTION - METHOD: No JSON found, returning original")
    print(f"📦 RETURNED_TEXT: {s}")
    print("=" * 60)
    return s


def get_llm():
    """Get configured LLM instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Please set GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.5,
    )


def add_ai_message_to_conversation(state: AgentState, content: str):
    """Add AI message to conversation after successful processing."""
    state["messages"].append(AIMessage(content=content))
    print(f"📝 Added AI message to conversation: {content[:50]}...")


def add_system_message_to_conversation(state: AgentState, content: str):
    """Add System message to conversation after successful processing."""
    state["messages"].append(SystemMessage(content=content))
    print(f"📝 Added System message to conversation: {content[:50]}...")


def llm_with_history(state: AgentState, final_prompt: str):
    """Invoke LLM with history context and return response."""
    # 🔍 LLM INVOCATION - INPUT 🔍
    print("=" * 70)
    print("🤖 LLM INVOCATION - STARTED")
    print("=" * 70)
    print(f"📝 PROMPT_LENGTH: {len(final_prompt)} characters")
    print(f"📝 PROMPT_PREVIEW: {final_prompt[:200]}...")
    print("=" * 70)
    
    # Send the final prompt directly as a human message
    # Note: The final_prompt already contains conversation history via build_prompt_from_template
    request_msgs = [HumanMessage(content=final_prompt)]
    
    resp = get_llm().invoke(request_msgs)
    
    # 🔍 LLM INVOCATION - OUTPUT 🔍
    print("🤖 LLM INVOCATION - COMPLETED")
    print(f"📤 RESPONSE_LENGTH: {len(resp.content)} characters")
    print(f"📤 RESPONSE_PREVIEW: {resp.content[:200]}...")
    print(f"📊 RESPONSE_TYPE: {type(resp).__name__}")
    print("=" * 70)
    
    # DO NOT append to messages here - let the calling node handle it after parsing
    return resp


def build_conversation_history(state: AgentState) -> str:
    """Build formatted conversation history from messages for prompt inclusion."""
    conversation = state.get("messages", [])
    history_text = ""
    
    for msg in conversation:
        if isinstance(msg, HumanMessage) and msg.content == "__start__":
            continue
        elif isinstance(msg, HumanMessage):
            history_text += f"Student: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history_text += f"Agent: {msg.content}\n"
        elif isinstance(msg, SystemMessage):
            history_text += f"System: {msg.content}\n"
    
    return history_text.strip()


def build_prompt_from_template(system_prompt: str, state: AgentState, 
                             include_last_message: bool = False, 
                             include_instructions: bool = False,
                             parser=None) -> str:
    """Build a comprehensive prompt from template with optional components."""
    
    # Build the template string based on what we need
    template_parts = ["{system_prompt}"]
    template_vars = ["system_prompt"]
    
    # Add history if available
    history = build_conversation_history(state)
    if history:
        template_parts.append("\n\nConversation History:\n{history}")
        template_vars.append("history")
    
    # Add last user message if requested
    if include_last_message and state.get("last_user_msg"):
        template_parts.append("\n\nStudent's Latest Response: {last_user_message}")
        template_vars.append("last_user_message")
    
    # Add instructions at the end if requested
    if include_instructions and parser:
        template_parts.append("\n\n{instructions}")
        template_vars.append("instructions")
    
    # Create the template
    template_string = "".join(template_parts)
    prompt_template = PromptTemplate(
        input_variables=template_vars,
        template=template_string
    )
    
    # Prepare the values
    template_values = {"system_prompt": system_prompt}
    
    if history:
        template_values["history"] = history
    
    if include_last_message and state.get("last_user_msg"):
        template_values["last_user_message"] = state["last_user_msg"]
    
    if include_instructions and parser:
        template_values["instructions"] = parser.get_format_instructions()
    
    # Format the prompt
    return prompt_template.format(**template_values)


def get_ground_truth(concept: str, section_name: str) -> str:
    """Retrieve ground truth content for a given concept and section."""
    try:
        # 🔍 GROUND TRUTH RETRIEVAL - INPUT 🔍
        print("=" * 70)
        print("📚 GROUND TRUTH RETRIEVAL - STARTED")
        print("=" * 70)
        print(f"🎯 CONCEPT: {concept}")
        print(f"📋 SECTION_NAME: {section_name}")
        print("=" * 70)
        
        # Build a minimal NextSectionChoice object; other fields are dummy since retriever only uses section_name
        params = NextSectionChoice(
            section_name=section_name,
            difficulty=1,
            board_exam_importance=1,
            olympiad_importance=1,
            avg_study_time_min=1,
            interest_evoking=1,
            curiosity_evoking=1,
            critical_reasoning_needed=1,
            inquiry_learning_scope=1,
            example_availability=1,
        )
        docs = retrieve_docs(concept, params)
        combined = [f"# Page: {d.metadata['page_label']}\n{d.page_content}" for d in docs]
        full_doc = "\n---\n".join(combined)
        result = filter_relevant_section(concept, section_name, full_doc)
        
        # 🔍 GROUND TRUTH RETRIEVAL - OUTPUT 🔍
        print("📚 GROUND TRUTH RETRIEVAL - COMPLETED")
        print(f"📄 DOC_COUNT: {len(docs)} documents")
        print(f"📏 FULL_DOC_LENGTH: {len(full_doc)} characters")
        print(f"📏 FILTERED_LENGTH: {len(result)} characters")
        print(f"📄 RESULT_PREVIEW: {result[:300]}...")
        print("=" * 70)
        
        return result
    except Exception as e:
        print(f"Error retrieving ground truth for {concept} - {section_name}: {e}")
        raise


# ─── Pedagogical‐move context (shared between traditional and simulation nodes) ───────────

