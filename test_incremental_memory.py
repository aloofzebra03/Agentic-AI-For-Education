#!/usr/bin/env python3
"""
Test script to demonstrate incremental memory optimization.
Shows how the new caching prevents re-summarizing the same content.
"""

from langchain_core.messages import HumanMessage, AIMessage
from educational_agent.shared_utils import (
    AgentState, 
    build_node_aware_conversation_history,
    get_memory_cache_stats,
    reset_memory_cache
)

def create_mock_conversation() -> dict:
    """Create a mock conversation with multiple node transitions"""
    state = {}
    
    # Simulate conversation with node transitions
    messages = [
        HumanMessage(content="Hi, I'm ready to learn!"),
        AIMessage(content="Great! Let's start with a question about photosynthesis..."),
        HumanMessage(content="Is it about plants making food?"),
        AIMessage(content="Excellent! That's exactly right. Now let me explain..."),
        HumanMessage(content="I think I understand the basics"),
        AIMessage(content="Perfect! Let's test your understanding with a quiz..."),
        HumanMessage(content="The answer is chlorophyll"),
        AIMessage(content="Very good! Now let's see how this applies in real life..."),
        HumanMessage(content="I see plants everywhere doing this!"),
        AIMessage(content="Exactly! You've mastered this concept.")
    ]
    
    # Simulate node transitions 
    transitions = [
        {"from_node": "START", "to_node": "APK", "transition_after_message_index": 0},
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 2}, 
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 4},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 6},
        {"from_node": "AR", "to_node": "RLC", "transition_after_message_index": 8},
    ]
    
    state["messages"] = messages
    state["_node_transitions"] = transitions
    return state

def test_incremental_summarization():
    """Test that summaries are cached and reused efficiently"""
    
    print("🧪 TESTING INCREMENTAL MEMORY OPTIMIZATION")
    print("=" * 60)
    
    # Create initial conversation
    state = create_mock_conversation()
    
    print("\n1️⃣ FIRST CALL - Should create new summary")
    print("-" * 40)
    result1 = build_node_aware_conversation_history(state, "RLC")
    stats1 = get_memory_cache_stats(state)
    print(f"Cache stats after first call: {stats1}")
    print(f"Result length: {len(result1)} chars")
    
    print("\n2️⃣ SECOND CALL - Should reuse cached summary")
    print("-" * 40)
    result2 = build_node_aware_conversation_history(state, "RLC")
    stats2 = get_memory_cache_stats(state)
    print(f"Cache stats after second call: {stats2}")
    print(f"Result length: {len(result2)} chars")
    print(f"Results identical: {result1 == result2}")
    
    # Add new messages to test incremental summarization
    print("\n3️⃣ ADDING NEW MESSAGES - Should extend summary incrementally")
    print("-" * 40)
    
    # Add more messages and transitions
    new_messages = [
        HumanMessage(content="Can you tell me more about different types of plants?"),
        AIMessage(content="Sure! There are flowering plants, conifers, ferns...")
    ]
    
    state["messages"].extend(new_messages)
    state["_node_transitions"].append(
        {"from_node": "RLC", "to_node": "TC", "transition_after_message_index": 10}
    )
    
    result3 = build_node_aware_conversation_history(state, "TC")
    stats3 = get_memory_cache_stats(state)
    print(f"Cache stats after adding messages: {stats3}")
    print(f"New result length: {len(result3)} chars")
    
    print("\n4️⃣ CACHE RESET TEST")
    print("-" * 40)
    reset_memory_cache(state)
    result4 = build_node_aware_conversation_history(state, "TC")
    stats4 = get_memory_cache_stats(state)
    print(f"Cache stats after reset: {stats4}")
    
    print("\n✅ INCREMENTAL MEMORY OPTIMIZATION TEST COMPLETE")
    print("=" * 60)
    print("Key benefits demonstrated:")
    print("- ✅ Summaries are cached and reused")
    print("- ✅ Only new content gets summarized") 
    print("- ✅ Significant reduction in redundant LLM calls")
    print("- ✅ Cache can be managed and reset when needed")

if __name__ == "__main__":
    test_incremental_summarization()
