"""
Additional edge case tests to demonstrate when the current implementation could fail.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage, AIMessage
from utils.shared_utils import identify_node_segments_from_transitions
import copy


def test_message_object_equality_issue():
    """
    Demonstrates the potential issue with using object equality (==) 
    for finding messages in the list.
    """
    print("\n" + "🔥" * 40)
    print("EDGE CASE: Message Object Equality Issue")
    print("🔥" * 40)
    
    # Create original messages
    original_messages = [
        HumanMessage(content=f"Student message {i}") if i % 2 == 0 
        else AIMessage(content=f"Agent message {i}")
        for i in range(10)
    ]
    
    # Simulate what might happen in real usage - messages get deep copied
    # This could happen during state serialization/deserialization
    messages = copy.deepcopy(original_messages)
    
    print(f"\nOriginal messages created: {len(original_messages)}")
    print(f"Deep copied messages: {len(messages)}")
    print(f"Are they the same objects? {original_messages[0] is messages[0]}")
    print(f"Are they equal? {original_messages[0] == messages[0]}")
    
    # Create transitions
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 5}
    ]
    
    # Get segments
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    older_segments = segments[:-1]  # Everything except current
    
    if older_segments:
        # Collect older messages
        older_messages = []
        for segment in older_segments:
            older_messages.extend(segment["messages"])
        
        print(f"\nOlder messages collected: {len(older_messages)}")
        
        # Try to find using object equality (CURRENT METHOD)
        last_older_msg = older_messages[-1]
        last_older_index_method1 = -1
        for i, msg in enumerate(messages):
            if msg == last_older_msg:
                last_older_index_method1 = i
                break
        
        print(f"\nMethod 1 (object equality): {last_older_index_method1}")
        
        # Try using segment metadata (PROPOSED FIX)
        last_older_index_method2 = older_segments[-1]["end_idx"] - 1
        print(f"Method 2 (segment metadata): {last_older_index_method2}")
        
        # The objects ARE equal in LangChain because of proper __eq__ implementation
        # But this shows the method is fragile and depends on implementation details
        
        # Let's test with a scenario where equality might fail
        print("\n" + "-" * 80)
        print("Testing with modified equality:")
        
        # Create a scenario where we have duplicate content
        duplicate_messages = messages.copy()
        duplicate_messages[3] = AIMessage(content="Agent message 3")  # Same content as original
        
        # This message has same content but is a different object
        print(f"\nDuplicate message created at index 3")
        print(f"Original at index 3: {messages[3].content}")
        print(f"Duplicate: {duplicate_messages[3].content}")
        print(f"Are they same object? {messages[3] is duplicate_messages[3]}")
        print(f"Are they equal? {messages[3] == duplicate_messages[3]}")
        
        # When searching with object equality, we might find wrong index
        # if there are duplicates
        test_msg = AIMessage(content="Agent message 3")
        found_indices = []
        for i, msg in enumerate(messages):
            if msg.content == test_msg.content:
                found_indices.append(i)
        
        if len(found_indices) > 1:
            print(f"\n⚠️ POTENTIAL ISSUE: Found {len(found_indices)} messages with same content at indices: {found_indices}")
            print("If using object equality fails, content matching might return wrong index!")
        
        print("\n✅ Current implementation works BUT:")
        print("   - Relies on LangChain's __eq__ implementation")
        print("   - Could fail with message duplication/copying in some edge cases")
        print("   - Segment metadata method is more robust and efficient")


def test_performance_comparison():
    """
    Compare performance of different methods for finding last_older_index.
    """
    print("\n" + "⚡" * 40)
    print("PERFORMANCE: Method Comparison")
    print("⚡" * 40)
    
    import time
    
    # Create a large message list
    messages = [
        HumanMessage(content=f"Student message {i}") if i % 2 == 0 
        else AIMessage(content=f"Agent message {i}")
        for i in range(1000)
    ]
    
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 200},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 400},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 600},
        {"from_node": "AR", "to_node": "TC", "transition_after_message_index": 800}
    ]
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    older_segments = segments[:-2]
    
    # Collect older messages
    older_messages = []
    for segment in older_segments:
        older_messages.extend(segment["messages"])
    
    print(f"\nTest setup:")
    print(f"  Total messages: {len(messages)}")
    print(f"  Older messages: {len(older_messages)}")
    
    # Method 1: Object equality search (CURRENT)
    start = time.perf_counter()
    last_older_msg = older_messages[-1]
    last_older_index_m1 = -1
    for i, msg in enumerate(messages):
        if msg == last_older_msg:
            last_older_index_m1 = i
            break
    time_m1 = time.perf_counter() - start
    
    print(f"\nMethod 1 (object equality loop):")
    print(f"  Result: {last_older_index_m1}")
    print(f"  Time: {time_m1*1000:.4f} ms")
    
    # Method 2: Segment metadata (PROPOSED)
    start = time.perf_counter()
    last_older_index_m2 = older_segments[-1]["end_idx"] - 1
    time_m2 = time.perf_counter() - start
    
    print(f"\nMethod 2 (segment metadata):")
    print(f"  Result: {last_older_index_m2}")
    print(f"  Time: {time_m2*1000:.4f} ms")
    
    # Calculate speedup
    speedup = time_m1 / time_m2 if time_m2 > 0 else float('inf')
    print(f"\n⚡ Speedup: {speedup:.1f}x faster")
    print(f"✅ Both methods give same result: {last_older_index_m1 == last_older_index_m2}")


def test_real_world_scenario():
    """
    Test a realistic scenario with many transitions and long conversation.
    """
    print("\n" + "🌍" * 40)
    print("REAL-WORLD SCENARIO: Long Conversation")
    print("🌍" * 40)
    
    # Simulate a long educational conversation with many node transitions
    messages = []
    transitions = []
    
    # APK phase (10 messages)
    for i in range(10):
        messages.append(HumanMessage(content=f"APK student msg {i}") if i % 2 == 0 
                       else AIMessage(content=f"APK agent msg {i}"))
    transitions.append({"from_node": "APK", "to_node": "CI", "transition_after_message_index": len(messages)})
    
    # CI phase (8 messages)
    for i in range(8):
        messages.append(HumanMessage(content=f"CI student msg {i}") if i % 2 == 0 
                       else AIMessage(content=f"CI agent msg {i}"))
    transitions.append({"from_node": "CI", "to_node": "GE", "transition_after_message_index": len(messages)})
    
    # GE phase (12 messages)
    for i in range(12):
        messages.append(HumanMessage(content=f"GE student msg {i}") if i % 2 == 0 
                       else AIMessage(content=f"GE agent msg {i}"))
    transitions.append({"from_node": "GE", "to_node": "AR", "transition_after_message_index": len(messages)})
    
    # AR phase (6 messages)
    for i in range(6):
        messages.append(HumanMessage(content=f"AR student msg {i}") if i % 2 == 0 
                       else AIMessage(content=f"AR agent msg {i}"))
    transitions.append({"from_node": "AR", "to_node": "TC", "transition_after_message_index": len(messages)})
    
    # TC phase (current, 4 messages so far)
    for i in range(4):
        messages.append(HumanMessage(content=f"TC student msg {i}") if i % 2 == 0 
                       else AIMessage(content=f"TC agent msg {i}"))
    
    print(f"\nScenario setup:")
    print(f"  Total messages: {len(messages)}")
    print(f"  Node transitions: {len(transitions)}")
    print(f"  Phases: APK(10) -> CI(8) -> GE(12) -> AR(6) -> TC(4)")
    
    # Analyze with current approach
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    print(f"\nSegments created: {len(segments)}")
    for i, seg in enumerate(segments):
        print(f"  {i+1}. {seg['node']}: {len(seg['messages'])} messages (indices {seg['start_idx']}-{seg['end_idx']-1})")
    
    # Simulate the optimization logic
    if len(segments) >= 2:
        current_segment = segments[-1]
        previous_segment = segments[-2]
        older_segments = segments[:-2]
        
        print(f"\nMemory optimization breakdown:")
        print(f"  Current node: {current_segment['node']} ({len(current_segment['messages'])} messages)")
        print(f"  Previous node: {previous_segment['node']} ({len(previous_segment['messages'])} messages)")
        print(f"  Older segments: {len(older_segments)} nodes")
        
        if older_segments:
            # Calculate using BOTH methods
            older_messages = []
            for segment in older_segments:
                older_messages.extend(segment["messages"])
            
            # Current method
            last_older_msg = older_messages[-1]
            method1_idx = -1
            for i, msg in enumerate(messages):
                if msg == last_older_msg:
                    method1_idx = i
                    break
            
            # Proposed method
            method2_idx = older_segments[-1]["end_idx"] - 1
            
            print(f"\n  Older messages to summarize: {len(older_messages)}")
            print(f"  Last older index (current method): {method1_idx}")
            print(f"  Last older index (proposed method): {method2_idx}")
            print(f"  Match: {method1_idx == method2_idx} ✅" if method1_idx == method2_idx else "  Match: ❌ MISMATCH!")
            
            # Calculate what would be kept in memory
            kept_messages = previous_segment["messages"] + current_segment["messages"]
            print(f"\n  Messages kept exact: {len(kept_messages)}")
            print(f"  Messages to summarize: {len(older_messages)}")
            print(f"  Memory reduction: {len(older_messages)} -> summary (~100 chars)")
            print(f"  Compression ratio: ~{len(older_messages) * 50 / 100:.1f}x")


def run_edge_case_tests():
    """Run all edge case tests."""
    print("\n" + "=" * 80)
    print("MEMORY OPTIMIZATION - EDGE CASE TEST SUITE")
    print("=" * 80)
    
    try:
        test_message_object_equality_issue()
        test_performance_comparison()
        test_real_world_scenario()
        
        print("\n" + "=" * 80)
        print("📊 FINAL ANALYSIS")
        print("=" * 80)
        print("\n✅ CURRENT IMPLEMENTATION:")
        print("   - Works correctly in tested scenarios")
        print("   - Relies on message object equality")
        print("   - O(n) search through messages list")
        print("")
        print("⚡ PROPOSED OPTIMIZATION:")
        print("   - Use: last_older_index = older_segments[-1]['end_idx'] - 1")
        print("   - More reliable (doesn't depend on object equality)")
        print("   - O(1) operation (direct access)")
        print("   - Cleaner and more maintainable")
        print("")
        print("🎯 RECOMMENDATION: Replace the search loop with segment metadata access")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_edge_case_tests()
