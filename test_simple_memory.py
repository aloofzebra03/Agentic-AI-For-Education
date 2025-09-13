#!/usr/bin/env python3
"""
Simple test for the simplified memory optimization.
"""

from langchain_core.messages import HumanMessage, AIMessage
from educational_agent.shared_utils import (
    build_node_aware_conversation_history,
    reset_memory_summary
)

def create_simple_conversation() -> dict:
    """Create a simple mock conversation"""
    state = {}
    
    messages = [
        HumanMessage(content="Hi!"),
        AIMessage(content="Hello! Let's learn about photosynthesis..."),
        HumanMessage(content="Is it about plants?"),
        AIMessage(content="Correct! Plants make their own food..."),
        HumanMessage(content="I understand now"),
        AIMessage(content="Great! Let's test your knowledge..."),
        HumanMessage(content="Plants use sunlight"),
        AIMessage(content="Excellent! You got it right.")
    ]
    
    transitions = [
        {"from_node": "START", "to_node": "APK", "transition_after_message_index": 0},
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 2}, 
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 4},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 6},
    ]
    
    state["messages"] = messages
    state["_node_transitions"] = transitions
    return state

def test_simple_optimization():
    print("🧪 TESTING SIMPLIFIED MEMORY OPTIMIZATION")
    print("=" * 50)
    
    state = create_simple_conversation()
    
    print("\n1️⃣ FIRST CALL")
    print("-" * 20)
    result1 = build_node_aware_conversation_history(state, "AR")
    print(f"Summary field: '{state.get('_summary', 'None')[:50]}...'")
    print(f"Last index: {state.get('_summary_last_index', 'None')}")
    print(f"Result length: {len(result1)} chars")
    
    print("\n2️⃣ SECOND CALL (should reuse)")
    print("-" * 30)
    result2 = build_node_aware_conversation_history(state, "AR")
    print(f"Results identical: {result1 == result2}")
    
    # Add new messages
    print("\n3️⃣ ADDING NEW MESSAGES")
    print("-" * 25)
    state["messages"].extend([
        HumanMessage(content="What about trees?"),
        AIMessage(content="Trees also do photosynthesis...")
    ])
    state["_node_transitions"].append(
        {"from_node": "AR", "to_node": "TC", "transition_after_message_index": 8}
    )
    
    result3 = build_node_aware_conversation_history(state, "TC")
    print(f"New summary: '{state.get('_summary', 'None')[:50]}...'")
    print(f"New last index: {state.get('_summary_last_index', 'None')}")
    
    print("\n✅ SIMPLIFIED OPTIMIZATION TEST COMPLETE")

if __name__ == "__main__":
    test_simple_optimization()
