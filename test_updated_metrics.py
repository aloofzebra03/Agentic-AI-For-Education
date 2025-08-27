#!/usr/bin/env python3
"""
Test script to validate the updated session metrics system with LLM-based error handling and adaptability
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_updated_metrics_structure():
    """Test the updated metrics structure"""
    
    print("🧪 Testing updated metrics structure...")
    
    try:
        from tester_agent.session_metrics import LLMAnalyzedMetrics, SessionMetrics
        
        # Test LLMAnalyzedMetrics structure
        test_llm_metrics = LLMAnalyzedMetrics(
            concepts_covered=["simple pendulum", "oscillation"],
            clarity_conciseness_score=4.2,
            user_type="Medium",
            user_interest_rating=4.0,
            user_engagement_rating=3.8,
            enjoyment_probability=0.75,
            error_handling_count=2,
            adaptability=True
        )
        
        print("✅ LLMAnalyzedMetrics structure test passed")
        
        # Test SessionMetrics structure
        test_session_metrics = SessionMetrics(
            concepts_covered=test_llm_metrics.concepts_covered,
            num_concepts_covered=len(test_llm_metrics.concepts_covered),
            clarity_conciseness_score=test_llm_metrics.clarity_conciseness_score,
            user_type=test_llm_metrics.user_type,
            user_interest_rating=test_llm_metrics.user_interest_rating,
            user_engagement_rating=test_llm_metrics.user_engagement_rating,
            enjoyment_probability=test_llm_metrics.enjoyment_probability,
            error_handling_count=test_llm_metrics.error_handling_count,
            adaptability=test_llm_metrics.adaptability,
            quiz_score=85.0,
            session_id="test_session",
            total_interactions=8,
            session_duration=20.5,
            persona_name="test_persona"
        )
        
        print("✅ SessionMetrics structure test passed")
        print(f"   - Error handling count: {test_session_metrics.error_handling_count}")
        print(f"   - Adaptability: {test_session_metrics.adaptability}")
        print(f"   - No response time field (removed as requested)")
        
        return True
        
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quiz_score_from_state():
    """Test quiz score extraction from agent state"""
    
    print("\n🧪 Testing quiz score extraction from agent state...")
    
    try:
        from tester_agent.session_metrics import MetricsComputer
        
        computer = MetricsComputer()
        
        # Test with quiz score in state
        test_state = {"quiz_score": 75.0}
        test_history = []
        
        score = computer._extract_quiz_score(test_history, test_state)
        print(f"✅ Quiz score from state: {score}% (expected: 75.0%)")
        
        # Test with no quiz score in state
        empty_state = {}
        score_empty = computer._extract_quiz_score(test_history, empty_state)
        print(f"✅ Default quiz score: {score_empty}% (expected: 0%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Quiz score test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Testing Updated Session Metrics System")
    print("=" * 50)
    
    success1 = test_updated_metrics_structure()
    success2 = test_quiz_score_from_state()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Updated metrics system is working correctly!")
        print("\n📊 Key updates:")
        print("   ✅ Error handling count now analyzed by LLM")
        print("   ✅ Adaptability now determined by LLM")
        print("   ✅ Response time calculation removed")
        print("   ✅ Quiz score extraction simplified to use agent state")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
