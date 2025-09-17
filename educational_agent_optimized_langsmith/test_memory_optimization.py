"""
Simple test script to verify memory optimization is working.
"""

import sys
sys.path.append('..')

from educational_agent.shared_utils import (
    build_node_aware_conversation_history, 
    build_conversation_history,
    identify_node_segments_from_transitions
)
from langchain_core.messages import HumanMessage, AIMessage

def test_memory_optimization():
    """Test that memory optimization reduces conversation history size."""
    
    print("🧪 Testing Memory Optimization")
    print("=" * 50)
    
    # Create a mock state with a long conversation history
    mock_state = {
        "messages": [
            # Old conversation (APK node)
            HumanMessage(content="What is photosynthesis?"),
            AIMessage(content="Let me ask you - have you ever wondered how plants make their food?"),
            HumanMessage(content="I think they eat from soil?"),
            AIMessage(content="That's a common thought! Actually, they make their own food. Can you think of what they might need from their environment?"),
            
            # CI node transition  
            HumanMessage(content="Maybe sunlight?"),
            AIMessage(content="Excellent! Photosynthesis is the process where plants use sunlight to make food from carbon dioxide and water. Can you restate this definition?"),
            HumanMessage(content="Plants use sunlight to make food from CO2 and water?"),
            AIMessage(content="Perfect! You've got it. Now let's explore this further."),
            
            # GE node (current)
            HumanMessage(content="How exactly do they do this?"),
            AIMessage(content="Great question! Let me ask you - what part of the plant do you think captures the sunlight?"),
        ],
        "_node_transitions": [
            {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 6},
            {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 10},
        ]
    }
    
    # Test original vs optimized history
    original_history = build_conversation_history(mock_state)
    optimized_history = build_node_aware_conversation_history(mock_state, "GE")
    
    print(f"📊 Original history length: {len(original_history)} characters")
    print(f"📊 Optimized history length: {len(optimized_history)} characters")
    print(f"📊 Reduction: {len(original_history) - len(optimized_history)} characters")
    print(f"📊 Percentage saved: {((len(original_history) - len(optimized_history)) / len(original_history) * 100):.1f}%")
    
    print("\n" + "=" * 50)
    print("📄 ORIGINAL HISTORY:")
    print("=" * 50)
    print(original_history)
    
    print("\n" + "=" * 50) 
    print("📄 OPTIMIZED HISTORY:")
    print("=" * 50)
    print(optimized_history)
    
    # Test node segmentation
    segments = identify_node_segments_from_transitions(mock_state["messages"], mock_state["_node_transitions"])
    print(f"\n📊 Found {len(segments)} node segments:")
    for i, segment in enumerate(segments):
        print(f"  Segment {i+1}: {segment['node']} ({len(segment['messages'])} messages)")

if __name__ == "__main__":
    test_memory_optimization()
