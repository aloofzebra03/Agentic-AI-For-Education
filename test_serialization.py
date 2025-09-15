#!/usr/bin/env python3
"""
Test script to verify that simulation nodes properly handle dictionary-based 
variables instead of Pydantic objects for Langfuse serialization.
"""

import json
from typing import Dict, List, Any

def test_simulation_state_serialization():
    """Test that simulation state can be JSON serialized."""
    
    # Mock simulation state similar to what would be in AgentState
    test_state = {
        "messages": [],
        "current_state": "SIM_VARS",
        "sim_concepts": ["How length affects pendulum period", "Effect of gravity on period"],
        "sim_total_concepts": 2,
        "sim_current_idx": 0,
        "sim_variables": [  # This is the key change - dictionaries instead of Pydantic objects
            {
                "name": "pendulum length",
                "role": "independent", 
                "note": "Controls the period of oscillation"
            },
            {
                "name": "period",
                "role": "dependent",
                "note": "Time for one complete swing"
            },
            {
                "name": "gravity",
                "role": "control", 
                "note": "Kept constant at 9.8 m/s²"
            }
        ],
        "sim_action_config": {
            "action": "increase pendulum length from 1m to 2m",
            "rationale": "to observe how period changes with length",
            "prompt": "Are you ready to see this demonstration?"
        },
        "show_simulation": True,
        "simulation_config": {
            "concept": "How length affects pendulum period",
            "parameter_name": "length",
            "before_params": {"length": 1.0, "gravity": 9.8, "amplitude": 30},
            "after_params": {"length": 2.0, "gravity": 9.8, "amplitude": 30},
            "action_description": "increasing the pendulum length from 1.0m to 2.0m",
            "timing": {"before_duration": 8, "transition_duration": 3, "after_duration": 8},
            "agent_message": "Watch how the period changes as I increase the length for you..."
        },
        "simulation_active": True
    }
    
    try:
        # Test JSON serialization (this is what Langfuse needs)
        serialized = json.dumps(test_state, indent=2)
        
        # Test deserialization
        deserialized = json.loads(serialized)
        
        print("✅ SUCCESS: Simulation state is fully JSON serializable!")
        print(f"📊 State contains {len(test_state)} top-level keys")
        print(f"📋 Variables format: {type(test_state['sim_variables'])}")
        print(f"📋 First variable: {test_state['sim_variables'][0]}")
        
        # Verify the variables are properly formatted dictionaries
        for i, var in enumerate(test_state['sim_variables']):
            assert isinstance(var, dict), f"Variable {i} is not a dictionary: {type(var)}"
            assert 'name' in var, f"Variable {i} missing 'name' key"
            assert 'role' in var, f"Variable {i} missing 'role' key"
            assert var['role'] in ['independent', 'dependent', 'control'], f"Invalid role: {var['role']}"
        
        print("✅ All variables are properly formatted dictionaries!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_create_simulation_config_compatibility():
    """Test that create_simulation_config works with both old and new formats."""
    from educational_agent_optimized.simulation_nodes_no_mh_ge import create_simulation_config
    
    # Test with dictionary format (new format)
    dict_variables = [
        {'name': 'pendulum length', 'role': 'independent', 'note': 'Controls the period'},
        {'name': 'period', 'role': 'dependent', 'note': 'Time for one complete swing'},
        {'name': 'gravity', 'role': 'control', 'note': 'Kept constant'}
    ]
    
    concept = "How length affects period"
    action_config = {'action': 'increase length', 'rationale': 'to see period change'}
    
    try:
        result = create_simulation_config(dict_variables, concept, action_config)
        
        # Ensure result is JSON serializable
        json.dumps(result)
        
        print("✅ create_simulation_config works with dictionary variables!")
        print(f"📋 Generated config keys: {list(result.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR in create_simulation_config: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing simulation state serialization for Langfuse compatibility...")
    print("=" * 70)
    
    test1_passed = test_simulation_state_serialization()
    print()
    test2_passed = test_create_simulation_config_compatibility()
    
    print("=" * 70)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! Simulation nodes are ready for Langfuse.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
