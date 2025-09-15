#!/usr/bin/env python3
"""
Test script to verify that ci_node returns partial state updates and wrapper handles them correctly.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ci_node_partial_updates():
    """Test that ci_node returns only changed keys and wrapper merges correctly."""
    
    # Mock imports and dependencies
    from unittest.mock import Mock, patch
    
    # Mock the shared utils and config
    mock_state = {
        "messages": [],
        "current_state": "CI",
        "last_user_msg": "test message",
        "_asked_ci": False,
        "_ci_tries": 0,
        "agent_output": ""
    }
    
    print("🧪 Testing CI node partial state updates...")
    print("=" * 70)
    
    try:
        # Mock all the dependencies
        with patch('educational_agent_optimized.main_nodes_simulation_agent_no_mh.get_ground_truth', return_value="Mock ground truth"), \
             patch('educational_agent_optimized.main_nodes_simulation_agent_no_mh.build_prompt_from_template_optimized', return_value="Mock prompt"), \
             patch('educational_agent_optimized.main_nodes_simulation_agent_no_mh.llm_with_history') as mock_llm, \
             patch('educational_agent_optimized.main_nodes_simulation_agent_no_mh.extract_json_block', return_value="Mock content"), \
             patch('educational_agent_optimized.main_nodes_simulation_agent_no_mh.add_ai_message_to_conversation'):
            
            # Setup mock LLM response
            mock_response = Mock()
            mock_response.content = "Mock AI response"
            mock_llm.return_value = mock_response
            
            # Import the actual ci_node function
            from educational_agent_optimized.main_nodes_simulation_agent_no_mh import ci_node
            
            # Test first call (when _asked_ci is False)
            result = ci_node(mock_state)
            
            print("✅ CI Node executed successfully")
            print(f"📋 Result type: {type(result)}")
            print(f"📋 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Full state'}")
            
            # Verify it returns only changed keys
            if isinstance(result, dict) and not hasattr(result, 'get'):
                expected_keys = {'_asked_ci', '_ci_tries', 'agent_output'}
                actual_keys = set(result.keys())
                if actual_keys == expected_keys:
                    print(f"✅ Correct partial state update with keys: {actual_keys}")
                else:
                    print(f"❌ Unexpected keys. Expected: {expected_keys}, Got: {actual_keys}")
                    return False
            else:
                print("❌ Should return a plain dict, not full state object")
                return False
            
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_wrapper_merge():
    """Test that the wrapper correctly merges partial state updates."""
    
    from educational_agent_optimized.graph import _wrap
    
    print("🧪 Testing wrapper merge functionality...")
    print("=" * 70)
    
    try:
        # Mock state
        mock_state = {
            "messages": [],
            "current_state": "CI", 
            "last_user_msg": "",
            "_asked_ci": False,
            "_ci_tries": 0,
            "agent_output": "",
            "other_key": "should_remain"
        }
        
        # Mock node function that returns partial update
        def mock_node(state):
            return {
                "_asked_ci": True,
                "_ci_tries": 1,
                "agent_output": "New output"
            }
        
        # Wrap the mock node
        wrapped_node = _wrap(mock_node)
        
        # Execute
        result = wrapped_node(mock_state)
        
        print("✅ Wrapper executed successfully")
        print(f"📋 Result type: {type(result)}")
        
        # Verify merge worked correctly
        expected_state = {
            "messages": [],
            "current_state": "CI",
            "last_user_msg": "",
            "_asked_ci": True,  # Updated
            "_ci_tries": 1,     # Updated  
            "agent_output": "New output",  # Updated
            "other_key": "should_remain"   # Preserved
        }
        
        # Check each key
        all_correct = True
        for key, expected_value in expected_state.items():
            if result.get(key) != expected_value:
                print(f"❌ Key '{key}': expected '{expected_value}', got '{result.get(key)}'")
                all_correct = False
            else:
                print(f"✅ Key '{key}': {result.get(key)}")
        
        return all_correct
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing LangGraph best practices implementation...")
    print("=" * 70)
    
    test1_passed = test_ci_node_partial_updates()
    print()
    test2_passed = test_wrapper_merge()
    
    print("=" * 70)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! CI node follows LangGraph best practices.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
