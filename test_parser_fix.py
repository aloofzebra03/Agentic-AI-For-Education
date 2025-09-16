#!/usr/bin/env python3
"""
Quick test to check if parser instructions are properly preserved in optimized version.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from educational_agent.shared_utils import (
    AgentState, 
    build_prompt_from_template, 
    build_prompt_from_template_optimized
)
from educational_agent_optimized.main_nodes_simulation_agent_no_mh import apk_parser
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\aryan\Desktop\Personalized_Education\Agentic-AI-For-Education\tester_agent\.env", override=True)

def test_parser_instructions():
    """Test if parser instructions are preserved in both template functions."""
    
    # Create a simple state
    state = {
        "messages": [],
        "last_user_msg": "I think it's related to forces?"
    }
    
    system_prompt = """Current node: APK (Activate Prior Knowledge)
Possible next_state values:
- "CI": when the student's reply shows they correctly identified 'concept'.
- "APK": when the student's reply does not clearly identify 'concept'.

Task: Evaluate whether the student identified the concept correctly."""

    print("=" * 80)
    print("TESTING PARSER INSTRUCTIONS PRESERVATION")
    print("=" * 80)
    
    # Test old template function
    print("\n1. OLD build_prompt_from_template:")
    old_prompt = build_prompt_from_template(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=apk_parser
    )
    
    print(f"Length: {len(old_prompt)}")
    print(f"Contains parser instructions: {'format_instructions' in old_prompt.lower() or 'json' in old_prompt.lower()}")
    print(f"Last 300 chars:\n{old_prompt[-300:]}")
    
    # Test new optimized template function
    print("\n2. NEW build_prompt_from_template_optimized:")
    new_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,
        include_instructions=True,
        parser=apk_parser,
        current_node="APK"
    )
    
    print(f"Length: {len(new_prompt)}")
    print(f"Contains parser instructions: {'format_instructions' in new_prompt.lower() or 'json' in new_prompt.lower()}")
    print(f"Last 300 chars:\n{new_prompt[-300:]}")
    
    # Compare if both have parser instructions
    old_has_instructions = 'format_instructions' in old_prompt.lower() or 'json' in old_prompt.lower() or len(old_prompt) > len(system_prompt) + 200
    new_has_instructions = 'format_instructions' in new_prompt.lower() or 'json' in new_prompt.lower() or len(new_prompt) > len(system_prompt) + 200
    
    print(f"\n3. COMPARISON:")
    print(f"Old has parser instructions: {old_has_instructions}")
    print(f"New has parser instructions: {new_has_instructions}")
    print(f"Both preserve instructions: {old_has_instructions and new_has_instructions}")
    
    if old_has_instructions and new_has_instructions:
        print("✅ SUCCESS: Both template functions preserve parser instructions!")
    else:
        print("❌ ISSUE: Parser instructions not properly preserved!")
        
    return old_has_instructions and new_has_instructions

if __name__ == "__main__":
    success = test_parser_instructions()
    sys.exit(0 if success else 1)
