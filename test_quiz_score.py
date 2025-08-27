#!/usr/bin/env python3
"""
Quick test to verify quiz score extraction from agent state
"""

from tester_agent.session_metrics import MetricsComputer

def test_quiz_score_extraction():
    """Test the simplified quiz score extraction"""
    
    computer = MetricsComputer()
    
    # Test case 1: Quiz score present in state
    state_with_score = {"quiz_score": 85.5}
    history = []
    
    score = computer._extract_quiz_score(history, state_with_score)
    print(f"✅ Test 1 - Score from state: {score}% (expected: 85.5%)")
    assert score == 85.5, f"Expected 85.5, got {score}"
    
    # Test case 2: No quiz score in state (should default to 0)
    state_empty = {}
    
    score = computer._extract_quiz_score(history, state_empty)
    print(f"✅ Test 2 - Default score: {score}% (expected: 0%)")
    assert score == 0.0, f"Expected 0.0, got {score}"
    
    # Test case 3: Quiz score is 0 (should return 0, not default)
    state_zero_score = {"quiz_score": 0.0}
    
    score = computer._extract_quiz_score(history, state_zero_score)
    print(f"✅ Test 3 - Zero score: {score}% (expected: 0%)")
    assert score == 0.0, f"Expected 0.0, got {score}"
    
    print("\n🎉 All quiz score extraction tests passed!")

if __name__ == "__main__":
    print("🧪 Testing Simplified Quiz Score Extraction")
    print("=" * 50)
    test_quiz_score_extraction()
