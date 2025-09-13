"""
Simple test for memory optimization functions without LLM dependencies.
"""

def test_node_segmentation():
    """Test node segmentation logic."""
    
    # Mock messages list (simplified)
    messages = [f"Message {i}" for i in range(10)]
    
    # Mock transitions
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 4},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 8},
    ]
    
    def identify_node_segments_from_transitions(messages, transitions):
        """Simple version of the segmentation function."""
        if not transitions:
            return [{"node": "unknown", "messages": messages, "start_idx": 0, "end_idx": len(messages)}]
        
        segments = []
        start_idx = 0
        
        for transition in transitions:
            end_idx = transition["transition_after_message_index"] 
            
            if end_idx > start_idx:
                segments.append({
                    "node": transition["from_node"],
                    "messages": messages[start_idx:end_idx],
                    "start_idx": start_idx,
                    "end_idx": end_idx
                })
            start_idx = end_idx
        
        # Add the final segment
        if start_idx < len(messages):
            current_node = transitions[-1]["to_node"] if transitions else "current"
            segments.append({
                "node": current_node,
                "messages": messages[start_idx:], 
                "start_idx": start_idx,
                "end_idx": len(messages)
            })
        
        return segments
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    print("🧪 Testing Node Segmentation")
    print("=" * 40)
    print(f"📊 Total messages: {len(messages)}")
    print(f"📊 Transitions: {len(transitions)}")
    print(f"📊 Segments found: {len(segments)}")
    
    for i, segment in enumerate(segments):
        print(f"  Segment {i+1}: {segment['node']} - messages {segment['start_idx']}-{segment['end_idx']} ({len(segment['messages'])} messages)")
        
    # Test memory optimization logic
    if len(segments) >= 2:
        current_segment = segments[-1]  # Current node (GE)
        previous_segment = segments[-2]  # Previous node (CI) 
        older_segments = segments[:-2]   # Everything before (APK)
        
        print(f"\n📊 Memory Optimization Results:")
        print(f"  - Current segment: {current_segment['node']} ({len(current_segment['messages'])} messages)")
        print(f"  - Previous segment: {previous_segment['node']} ({len(previous_segment['messages'])} messages)")
        print(f"  - Older segments to summarize: {len(older_segments)} segments")
        
        # Calculate what would be preserved vs summarized
        preserved_messages = len(previous_segment['messages']) + len(current_segment['messages'])
        older_messages = sum(len(seg['messages']) for seg in older_segments)
        
        print(f"  - Messages preserved exactly: {preserved_messages}")
        print(f"  - Messages to be summarized: {older_messages}")
        print(f"  - Reduction ratio: {older_messages}/{len(messages)} = {older_messages/len(messages)*100:.1f}% summarized")

if __name__ == "__main__":
    test_node_segmentation()
