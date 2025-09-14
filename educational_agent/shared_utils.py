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


def build_prompt_from_template_optimized(system_prompt: str, state: AgentState, 
                                       include_last_message: bool = False, 
                                       include_instructions: bool = False,
                                       parser=None, current_node: str = None) -> str:
    """
    Build a comprehensive prompt from template with memory optimization.
    This is the optimized version that uses node-aware conversation history.
    """
    
    # Build the template string based on what we need
    template_parts = ["{system_prompt}"]
    template_vars = ["system_prompt"]
    
    # Add optimized history if available
    if current_node:
        optimized_history = build_node_aware_conversation_history(state, current_node)
        if optimized_history:
            template_parts.append("\n\nConversation History:\n{history}")
            template_vars.append("history")
    else:
        # Fall back to regular history if no current_node provided
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
    
    # Add history (optimized or regular)
    if current_node:
        optimized_history = build_node_aware_conversation_history(state, current_node)
        if optimized_history:
            template_values["history"] = optimized_history
    else:
        history = build_conversation_history(state)
        if history:
            template_values["history"] = history
    
    if include_last_message and state.get("last_user_msg"):
        template_values["last_user_message"] = state["last_user_msg"]
    
    if include_instructions and parser:
        template_values["instructions"] = parser.get_format_instructions()
    
    # Format the prompt
    return prompt_template.format(**template_values)


def get_ground_truth(concept: str, section_name: str) -> str:
    # """Retrieve ground truth content for a given concept and section."""
    # try:
    #     # 🔍 GROUND TRUTH RETRIEVAL - INPUT 🔍
    #     print("=" * 70)
    #     print("📚 GROUND TRUTH RETRIEVAL - STARTED")
    #     print("=" * 70)
    #     print(f"🎯 CONCEPT: {concept}")
    #     print(f"📋 SECTION_NAME: {section_name}")
    #     print("=" * 70)
        
    #     # Build a minimal NextSectionChoice object; other fields are dummy since retriever only uses section_name
    #     params = NextSectionChoice(
    #         section_name=section_name,
    #         difficulty=1,
    #         board_exam_importance=1,
    #         olympiad_importance=1,
    #         avg_study_time_min=1,
    #         interest_evoking=1,
    #         curiosity_evoking=1,
    #         critical_reasoning_needed=1,
    #         inquiry_learning_scope=1,
    #         example_availability=1,
    #     )
    #     docs = retrieve_docs(concept, params)
    #     combined = [f"# Page: {d.metadata['page_label']}\n{d.page_content}" for d in docs]
    #     full_doc = "\n---\n".join(combined)
    #     result = filter_relevant_section(concept, section_name, full_doc)
        
    #     # 🔍 GROUND TRUTH RETRIEVAL - OUTPUT 🔍
    #     print("📚 GROUND TRUTH RETRIEVAL - COMPLETED")
    #     print(f"📄 DOC_COUNT: {len(docs)} documents")
    #     print(f"📏 FULL_DOC_LENGTH: {len(full_doc)} characters")
    #     print(f"📏 FILTERED_LENGTH: {len(result)} characters")
    #     print(f"📄 RESULT_PREVIEW: {result[:300]}...")
    #     print("=" * 70)
        
    #     return result
    # except Exception as e:
    #     print(f"Error retrieving ground truth for {concept} - {section_name}: {e}")
    #     raise
    return ""


# ─── Memory Optimization Functions ─────────────────────────────────────────────

def identify_node_segments_from_transitions(messages: list, transitions: list) -> list:
    """
    Split messages into segments based on recorded node transitions.
    Transition happens AFTER the agent response, so messages belong to the 'from_node'.
    """
    if not transitions:
        # No transitions recorded, treat all messages as one segment  
        return [{"node": "unknown", "messages": messages, "start_idx": 0, "end_idx": len(messages)}]
    
    segments = []
    start_idx = 0
    
    for transition in transitions:
        # Messages up to (and including) transition point belong to 'from_node'
        end_idx = transition["transition_after_message_index"] 
        
        if end_idx > start_idx:
            segments.append({
                "node": transition["from_node"],
                "messages": messages[start_idx:end_idx],
                "start_idx": start_idx,
                "end_idx": end_idx
            })
        start_idx = end_idx
    
    # Add the final segment (current node messages) - messages after last transition
    if start_idx < len(messages):
        current_node = transitions[-1]["to_node"] if transitions else "current"
        segments.append({
            "node": current_node,
            "messages": messages[start_idx:], 
            "start_idx": start_idx,
            "end_idx": len(messages)
        })
    
    return segments

def create_educational_summary(messages: list) -> str:
    """
    Use LLM to create a proper educational summary of the conversation.
    """
    if not messages:
        return ""
    
    # Extract agent messages for summarization
    agent_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    student_messages = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
    
    if not agent_messages:
        return f"Student made {len(student_messages)} responses"
    
    # Build conversation text for summarization
    conversation_text = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation_text += f"Student: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_text += f"Agent: {msg.content}\n"
    
    # Limit conversation text to avoid token overflow
    if len(conversation_text) > 2000:
        conversation_text = conversation_text[:2000] + "..."
    
    # Use LLM to summarize
    summary_prompt = f"""Summarize the following educational conversation in 2-3 sentences, focusing on:
- What concept was being taught
- Student's understanding level
- Key pedagogical interactions

Conversation:
{conversation_text}

Summary:"""
    
    try:
        summary_response = get_llm().invoke([HumanMessage(content=summary_prompt)])
        return summary_response.content.strip()
    except Exception as e:
        print(f"❌ Error creating LLM summary: {e}")
        # Fallback to simple summary if LLM fails
        return f"Educational discussion with {len(messages)} exchanges about the concept"

def create_educational_summary_from_text(conversation_text: str) -> str:
    """
    Create an LLM-generated summary from conversation text.
    """
    try:
        if not conversation_text.strip():
            return "Empty conversation segment"
        
        # Limit conversation text to avoid token overflow
        if len(conversation_text) > 2000:
            conversation_text = conversation_text[:2000] + "..."
        
        # Create educational summary prompt
        summary_prompt = f"""Summarize the following educational conversation in 2-3 sentences, focusing on:
- What concept was being taught
- Student's understanding level  
- Key pedagogical interactions

Conversation:
{conversation_text}

Summary:"""
        
        summary_response = get_llm().invoke([HumanMessage(content=summary_prompt)])
        return summary_response.content.strip()
    except Exception as e:
        print(f"❌ Error creating LLM summary: {e}")
        # Fallback to simple summary if LLM fails
        return "Educational discussion about the concept"

def build_node_aware_conversation_history(state: AgentState, current_node: str) -> str:
    """
    Keep exact messages from current and previous node interactions.
    Use cached summaries and only summarize new content incrementally.
    """
    messages = state.get("messages", [])
    transitions = state.get("_node_transitions", [])
    
    # For short conversations, use full history
    if len(messages) <= 6:
        return build_conversation_history(state)
    
    # Get node segments based on recorded transitions
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    print(f"📊 MEMORY OPTIMIZATION: Found {len(segments)} node segments")
    
    if len(segments) >= 2:
        # Keep current + previous node segments exact
        current_segment = segments[-1]  # Current node
        previous_segment = segments[-2]  # Previous node
        older_segments = segments[:-2]   # Everything before previous node
        
        print(f"📊 Current node: {current_segment['node']} ({len(current_segment['messages'])} messages)")
        print(f"📊 Previous node: {previous_segment['node']} ({len(previous_segment['messages'])} messages)")
        print(f"📊 Older segments: {len(older_segments)} segments")
        
        # Handle summary efficiently
        summary = ""
        
        if older_segments:
            # Calculate what needs to be summarized
            older_messages = []
            for segment in older_segments:
                older_messages.extend(segment["messages"])
            
            # Find the highest index in older_messages in the original messages list
            last_older_index = -1
            if older_messages:
                last_older_msg = older_messages[-1]
                for i, msg in enumerate(messages):
                    if msg == last_older_msg:
                        last_older_index = i
                        break
            
            # Check if we need to update summary
            if last_older_index <= state["summary_last_index"]:
                # Use existing summary - no new messages to summarize
                summary = state["summary"]
                print(f"📊 ✅ Using existing summary (covers up to index {state['summary_last_index']})")
            else:
                # Need to update summary with new messages
                new_messages_start = state["summary_last_index"] + 1
                new_messages = messages[new_messages_start:last_older_index + 1]
                
                if state["summary"]:
                    # Combine old summary with new messages
                    combined_content = f"Previous summary: {state['summary']}\n\nNew messages:\n"
                    for msg in new_messages:
                        if isinstance(msg, HumanMessage):
                            combined_content += f"Student: {msg.content}\n"
                        elif isinstance(msg, AIMessage):
                            combined_content += f"Agent: {msg.content}\n"
                    
                    print(f"📊 🔄 Updating summary: old summary + {len(new_messages)} new messages...")
                    summary = create_educational_summary_from_text(combined_content)
                else:
                    # First time - just summarize the messages
                    print(f"📊 🔄 Creating first summary for {len(new_messages)} messages...")
                    summary = create_educational_summary(new_messages)
                
                # Update summary state
                state["summary"] = summary
                state["summary_last_index"] = last_older_index
                print(f"📊 💾 Updated summary (now covers up to index {last_older_index})")
            
            summary = f"Previous conversation summary: {summary}\n\n"
        
        # Format recent messages (previous + current node) exactly
        recent_messages = previous_segment["messages"] + current_segment["messages"]
        recent_text = ""
        for msg in recent_messages:
            if isinstance(msg, HumanMessage):
                recent_text += f"Student: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                recent_text += f"Agent: {msg.content}\n"
        
        optimized_history = summary + recent_text.strip()
        print(f"📊 OPTIMIZATION RESULT: {len(build_conversation_history(state))} -> {len(optimized_history)} chars")
        return optimized_history
    
    else:
        # Not enough transitions, fall back to regular history
        print(f"📊 Not enough transitions, using full history")
        return build_conversation_history(state)

def reset_memory_summary(state: AgentState):
    """
    Reset the memory summary. Useful for testing or manual management.
    """
    if "summary" in state:
        del state["summary"]
        del state["summary_last_index"]
        print("📊 🗑️ Memory summary reset")

# ─── Pedagogical‐move context (shared between traditional and simulation nodes) ───────────

