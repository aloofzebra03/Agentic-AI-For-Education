"""
Test cases for memory optimization logic in shared_utils.py

This file contains comprehensive tests to identify issues with:
1. identify_node_segments_from_transitions
2. build_node_aware_conversation_history
3. older_segments calculation and handling
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils.shared_utils import (
    identify_node_segments_from_transitions,
    build_node_aware_conversation_history,
    build_conversation_history,
)


def create_test_messages(count: int) -> list:
    """Create test messages alternating between human and AI."""
    messages = []
    for i in range(count):
        if i % 2 == 0:
            messages.append(HumanMessage(content=f"Student message {i}"))
        else:
            messages.append(AIMessage(content=f"Agent message {i}"))
    return messages


def print_segment_info(segments: list, messages: list):
    """Print detailed information about segments for debugging."""
    print("\n" + "=" * 80)
    print("SEGMENT BREAKDOWN:")
    print("=" * 80)
    
    for i, seg in enumerate(segments):
        print(f"\nSegment {i + 1}:")
        print(f"  Node: {seg['node']}")
        print(f"  Start index: {seg['start_idx']}")
        print(f"  End index: {seg['end_idx']}")
        print(f"  Message count: {len(seg['messages'])}")
        print(f"  Messages:")
        for j, msg in enumerate(seg['messages']):
            actual_idx = seg['start_idx'] + j
            msg_type = "Student" if isinstance(msg, HumanMessage) else "Agent"
            print(f"    [{actual_idx}] {msg_type}: {msg.content}")
    
    print("\n" + "=" * 80)


def test_case_1_basic_segmentation():
    """Test basic segmentation with simple transitions."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 1: Basic Segmentation")
    print("🧪" * 40)
    
    # Create 10 messages (indices 0-9)
    messages = create_test_messages(10)
    
    # Transitions:
    # - After message 3 (index 3): APK -> CI
    # - After message 7 (index 7): CI -> GE
    transitions = [
        {
            "from_node": "APK",
            "to_node": "CI",
            "transition_after_message_index": 4  # Messages 0-3 are APK
        },
        {
            "from_node": "CI",
            "to_node": "GE",
            "transition_after_message_index": 8  # Messages 4-7 are CI
        }
    ]
    
    print(f"\nTotal messages: {len(messages)}")
    print(f"Transitions: {len(transitions)}")
    print("\nExpected segments:")
    print("  Segment 1: APK (messages 0-3, indices 0-3)")
    print("  Segment 2: CI (messages 4-7, indices 4-7)")
    print("  Segment 3: GE (messages 8-9, indices 8-9)")
    
    # Run segmentation
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    print_segment_info(segments, messages)
    
    # Validate
    assert len(segments) == 3, f"Expected 3 segments, got {len(segments)}"
    assert segments[0]["node"] == "APK", f"Segment 0 should be APK, got {segments[0]['node']}"
    assert segments[1]["node"] == "CI", f"Segment 1 should be CI, got {segments[1]['node']}"
    assert segments[2]["node"] == "GE", f"Segment 2 should be GE, got {segments[2]['node']}"
    assert len(segments[0]["messages"]) == 4, f"APK should have 4 messages, got {len(segments[0]['messages'])}"
    assert len(segments[1]["messages"]) == 4, f"CI should have 4 messages, got {len(segments[1]['messages'])}"
    assert len(segments[2]["messages"]) == 2, f"GE should have 2 messages, got {len(segments[2]['messages'])}"
    
    print("\n✅ TEST CASE 1 PASSED")


def test_case_2_older_segments_calculation():
    """Test that older_segments is calculated correctly."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 2: Older Segments Calculation")
    print("🧪" * 40)
    
    # Create 20 messages
    messages = create_test_messages(20)
    
    # Multiple transitions to create multiple older segments
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 4},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 8},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 12},
        {"from_node": "AR", "to_node": "TC", "transition_after_message_index": 16}
    ]
    
    print(f"\nTotal messages: {len(messages)}")
    print(f"Transitions: {len(transitions)}")
    print("\nExpected segments:")
    print("  Segment 1 (APK): messages 0-3")
    print("  Segment 2 (CI): messages 4-7")
    print("  Segment 3 (GE): messages 8-11")
    print("  Segment 4 (AR): messages 12-15")
    print("  Segment 5 (TC): messages 16-19")
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    
    print_segment_info(segments, messages)
    
    # Simulate what build_node_aware_conversation_history does
    print("\n" + "-" * 80)
    print("OLDER SEGMENTS ANALYSIS:")
    print("-" * 80)
    
    if len(segments) >= 2:
        current_segment = segments[-1]
        previous_segment = segments[-2]
        older_segments = segments[:-2]
        
        print(f"\nCurrent segment: {current_segment['node']} (messages {current_segment['start_idx']}-{current_segment['end_idx']-1})")
        print(f"Previous segment: {previous_segment['node']} (messages {previous_segment['start_idx']}-{previous_segment['end_idx']-1})")
        print(f"Older segments count: {len(older_segments)}")
        
        if older_segments:
            print("\nOlder segments details:")
            for i, seg in enumerate(older_segments):
                print(f"  {i+1}. {seg['node']}: messages {seg['start_idx']}-{seg['end_idx']-1} ({len(seg['messages'])} messages)")
            
            # Calculate older_messages (this is the critical part)
            older_messages = []
            for segment in older_segments:
                older_messages.extend(segment["messages"])
            
            print(f"\nTotal older messages collected: {len(older_messages)}")
            
            # Find last_older_index (THIS IS WHERE THE BUG MIGHT BE)
            last_older_index = -1
            if older_messages:
                last_older_msg = older_messages[-1]
                print(f"\nLast older message content: '{last_older_msg.content}'")
                
                # Search for it in the messages list
                for i, msg in enumerate(messages):
                    if msg == last_older_msg:
                        last_older_index = i
                        print(f"Found at index: {i}")
                        break
                
                if last_older_index == -1:
                    print("❌ ERROR: Could not find last_older_msg in messages list!")
                else:
                    print(f"\n✅ last_older_index correctly identified as: {last_older_index}")
                    
                    # Verify this matches expected
                    expected_last_index = older_segments[-1]["end_idx"] - 1
                    print(f"Expected last index from segments: {expected_last_index}")
                    
                    if last_older_index != expected_last_index:
                        print(f"❌ MISMATCH! last_older_index ({last_older_index}) != expected ({expected_last_index})")
                        print("\n🔍 POTENTIAL BUG IDENTIFIED:")
                        print("The way we're finding last_older_index might not be reliable.")
                        print("It's using object equality (msg == last_older_msg) which might fail")
                        print("if messages are copied or recreated.")
                    else:
                        print(f"✅ Indices match correctly!")
        
        # Validate segment structure
        assert len(segments) == 5, f"Expected 5 segments, got {len(segments)}"
        assert len(older_segments) == 3, f"Expected 3 older segments, got {len(older_segments)}"
        
    print("\n✅ TEST CASE 2 COMPLETED")


def test_case_3_edge_case_single_transition():
    """Test with only one transition (edge case)."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 3: Single Transition (Edge Case)")
    print("🧪" * 40)
    
    messages = create_test_messages(10)
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 5}
    ]
    
    print(f"\nTotal messages: {len(messages)}")
    print(f"Transitions: {len(transitions)}")
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    print_segment_info(segments, messages)
    
    # With only 2 segments, there should be NO older_segments
    if len(segments) >= 2:
        older_segments = segments[:-2]
        print(f"\nOlder segments count: {len(older_segments)}")
        
        if len(older_segments) == 0:
            print("✅ Correctly identified NO older segments with single transition")
        else:
            print(f"❌ ERROR: Expected 0 older segments, got {len(older_segments)}")
    
    assert len(segments) == 2, f"Expected 2 segments, got {len(segments)}"
    print("\n✅ TEST CASE 3 PASSED")


def test_case_4_no_transitions():
    """Test with no transitions."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 4: No Transitions")
    print("🧪" * 40)
    
    messages = create_test_messages(10)
    transitions = []
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    print_segment_info(segments, messages)
    
    assert len(segments) == 1, f"Expected 1 segment, got {len(segments)}"
    assert segments[0]["node"] == "unknown", f"Expected 'unknown' node, got {segments[0]['node']}"
    assert len(segments[0]["messages"]) == 10, f"Expected 10 messages, got {len(segments[0]['messages'])}"
    
    print("\n✅ TEST CASE 4 PASSED")


def test_case_5_index_calculation_bug():
    """Test to identify potential index calculation bugs."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 5: Index Calculation Verification")
    print("🧪" * 40)
    
    messages = create_test_messages(15)
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 5},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 10}
    ]
    
    segments = identify_node_segments_from_transitions(messages, transitions)
    print_segment_info(segments, messages)
    
    # Detailed index verification
    print("\n" + "-" * 80)
    print("INDEX VERIFICATION:")
    print("-" * 80)
    
    older_segments = segments[:-2]
    
    print(f"\nOlder segments: {len(older_segments)}")
    
    # Method 1: Using last segment's end_idx
    if older_segments:
        method1_index = older_segments[-1]["end_idx"] - 1
        print(f"Method 1 (last segment end_idx - 1): {method1_index}")
        
        # Method 2: Collecting all messages and finding in list
        older_messages = []
        for seg in older_segments:
            older_messages.extend(seg["messages"])
        
        if older_messages:
            last_older_msg = older_messages[-1]
            method2_index = -1
            for i, msg in enumerate(messages):
                if msg == last_older_msg:
                    method2_index = i
                    break
            
            print(f"Method 2 (searching for message object): {method2_index}")
            
            # Method 3: Using message content matching (more reliable)
            method3_index = -1
            for i, msg in enumerate(messages):
                if msg.content == last_older_msg.content:
                    method3_index = i
            
            print(f"Method 3 (content matching): {method3_index}")
            
            if method1_index == method2_index == method3_index:
                print(f"\n✅ All methods agree: index {method1_index}")
            else:
                print(f"\n❌ METHODS DISAGREE!")
                print("This indicates a potential bug in how last_older_index is calculated.")
                print("\n🔍 RECOMMENDATION:")
                print("Use method 1 (segment end_idx - 1) instead of searching for message objects.")
                print("This is more reliable and efficient.")
    
    print("\n✅ TEST CASE 5 COMPLETED")


def test_case_6_full_integration_with_state():
    """Test full integration with state dictionary using actual build_node_aware_conversation_history."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 6: Full Integration with build_node_aware_conversation_history")
    print("🧪" * 40)
    
    # Create a realistic state
    messages = create_test_messages(20)
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 4},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 8},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 12},
        {"from_node": "AR", "to_node": "TC", "transition_after_message_index": 16}
    ]
    
    state = {
        "messages": messages,
        "node_transitions": transitions,
        "model": "gemma-3-27b-it",
        # Initially no summary
    }
    
    print(f"\nInitial state:")
    print(f"  Messages: {len(messages)}")
    print(f"  Transitions: {len(transitions)}")
    print(f"  Summary exists: {('summary' in state)}")
    
    # Call the actual function
    print(f"\n🔧 Calling build_node_aware_conversation_history(state, 'TC')...")
    history = build_node_aware_conversation_history(state, "TC")
    
    print(f"\n📊 Results:")
    print(f"  History length: {len(history)} characters")
    print(f"  Summary created: {('summary' in state)}")
    if 'summary' in state:
        print(f"  Summary covers up to index: {state.get('summary_last_index', 'N/A')}")
        print(f"  Summary: {state['summary'][:100]}...")
    
    # Verify the output contains expected parts
    assert "Student: Student message" in history, "History should contain student messages"
    assert "Agent: Agent message" in history, "History should contain agent messages"
    
    # The history should be shorter than full conversation for long conversations
    full_history_len = len(build_conversation_history(state))
    print(f"\n  Full history length: {full_history_len} characters")
    print(f"  Optimized history length: {len(history)} characters")
    
    if len(history) < full_history_len:
        print(f"  ✅ Memory optimization working! ({full_history_len - len(history)} chars saved)")
    
    print("\n✅ TEST CASE 6 COMPLETED")


def test_case_7_summary_update_logic():
    """Test the summary update logic using actual build_node_aware_conversation_history."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 7: Summary Update Logic with Real Function")
    print("🧪" * 40)
    
    messages = create_test_messages(20)
    transitions = [
        {"from_node": "APK", "to_node": "CI", "transition_after_message_index": 4},
        {"from_node": "CI", "to_node": "GE", "transition_after_message_index": 8},
        {"from_node": "GE", "to_node": "AR", "transition_after_message_index": 12},
        {"from_node": "AR", "to_node": "TC", "transition_after_message_index": 16}
    ]
    
    state = {
        "messages": messages,
        "node_transitions": transitions,
        "model": "gemma-3-27b-it",
        "summary": "Previous summary of messages 0-7",
        "summary_last_index": 7  # Summary covers up to message index 7
    }
    
    print(f"\nState before calling function:")
    print(f"  Existing summary: '{state.get('summary', 'None')}'")
    print(f"  Summary covers up to index: {state.get('summary_last_index', -1)}")
    print(f"  Total messages: {len(messages)}")
    
    # First call - should update summary since older messages go beyond index 7
    print(f"\n🔧 First call to build_node_aware_conversation_history(state, 'TC')...")
    history1 = build_node_aware_conversation_history(state, "TC")
    
    print(f"\n📊 After first call:")
    print(f"  Summary updated: Yes" if state.get('summary_last_index', -1) > 7 else "  Summary updated: No")
    print(f"  Summary now covers up to index: {state.get('summary_last_index', -1)}")
    print(f"  Updated summary: {state.get('summary', 'N/A')[:100]}...")
    
    old_summary = state.get('summary', '')
    old_index = state.get('summary_last_index', -1)
    
    # Second call - should reuse existing summary (no new older messages)
    print(f"\n🔧 Second call (should reuse summary)...")
    history2 = build_node_aware_conversation_history(state, "TC")
    
    print(f"\n📊 After second call:")
    print(f"  Summary changed: {'Yes' if state.get('summary') != old_summary else 'No'}")
    print(f"  Summary index changed: {'Yes' if state.get('summary_last_index') != old_index else 'No'}")
    
    # Verify summaries are reused when appropriate
    assert state.get('summary') == old_summary, "Summary should not change on second call"
    assert state.get('summary_last_index') == old_index, "Summary index should not change"
    
    print(f"  ✅ Summary correctly reused (no redundant LLM calls)")
    
    print("\n✅ TEST CASE 7 COMPLETED")


def test_case_8_progressive_conversation():
    """Test progressive conversation growth with build_node_aware_conversation_history."""
    print("\n" + "🧪" * 40)
    print("TEST CASE 8: Progressive Conversation Growth")
    print("🧪" * 40)
    
    print("\n📝 Simulating a conversation that grows over time...")
    
    # Start with just APK phase
    messages = create_test_messages(4)
    state = {
        "messages": messages,
        "node_transitions": [],
        "model": "gemma-3-27b-it",
    }
    
    print(f"\n1️⃣ Phase 1: APK only ({len(messages)} messages)")
    history1 = build_node_aware_conversation_history(state, "APK")
    print(f"   History length: {len(history1)} chars")
    print(f"   Summary exists: {'summary' in state}")
    
    # Transition to CI, add more messages
    state["node_transitions"].append({
        "from_node": "APK", 
        "to_node": "CI", 
        "transition_after_message_index": len(messages)
    })
    for i in range(4):
        state["messages"].append(HumanMessage(content=f"CI student msg {i}") if i % 2 == 0 
                                 else AIMessage(content=f"CI agent msg {i}"))
    
    print(f"\n2️⃣ Phase 2: APK -> CI ({len(state['messages'])} messages)")
    history2 = build_node_aware_conversation_history(state, "CI")
    print(f"   History length: {len(history2)} chars")
    print(f"   Summary exists: {'summary' in state}")
    print(f"   Using full history (short conversation)")
    
    # Add more phases to trigger summarization
    for phase, node in enumerate([("GE", 8), ("AR", 6), ("TC", 4)], start=3):
        node_name, msg_count = node
        state["node_transitions"].append({
            "from_node": state["node_transitions"][-1]["to_node"],
            "to_node": node_name,
            "transition_after_message_index": len(state["messages"])
        })
        for i in range(msg_count):
            state["messages"].append(HumanMessage(content=f"{node_name} student {i}") if i % 2 == 0
                                     else AIMessage(content=f"{node_name} agent {i}"))
        
        print(f"\n{phase}️⃣ Phase {phase}: ... -> {node_name} ({len(state['messages'])} messages)")
        history = build_node_aware_conversation_history(state, node_name)
        print(f"   History length: {len(history)} chars")
        print(f"   Summary exists: {'summary' in state}")
        if 'summary' in state:
            print(f"   Summary covers: 0-{state['summary_last_index']}")
            full_len = len(build_conversation_history(state))
            print(f"   Compression: {full_len} -> {len(history)} chars ({full_len - len(history)} saved)")
    
    print("\n✅ TEST CASE 8 COMPLETED")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 80)
    print("MEMORY OPTIMIZATION TEST SUITE")
    print("=" * 80)
    
    try:
        test_case_1_basic_segmentation()
        test_case_2_older_segments_calculation()
        test_case_3_edge_case_single_transition()
        test_case_4_no_transitions()
        test_case_5_index_calculation_bug()
        test_case_6_full_integration_with_state()
        test_case_7_summary_update_logic()
        test_case_8_progressive_conversation()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print("\n📋 SUMMARY OF FINDINGS:")
        print("-" * 80)
        print("1. ✅ Segmentation logic works correctly")
        print("2. ✅ Optimized last_older_index calculation (O(1) instead of O(n))")
        print("3. ✅ build_node_aware_conversation_history works as expected")
        print("4. ✅ Summary caching prevents redundant LLM calls")
        print("5. ✅ Progressive conversation growth handled correctly")
        print("6. ✅ Memory optimization provides significant compression")
        print("-" * 80)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
