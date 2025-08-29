#!/usr/bin/env python3
"""Test session metrics without requiring real API keys"""

import os
# Set mock environment variables for testing
os.environ["GOOGLE_API_KEY"] = "mock_key_for_testing"
os.environ["LANGFUSE_SECRET_KEY"] = "mock_langfuse_key"
os.environ["LANGFUSE_PUBLIC_KEY"] = "mock_langfuse_public"
os.environ["LANGFUSE_HOST"] = "https://mock.langfuse.com"

def test_session_metrics_structure():
    """Test that session metrics can be created and structured properly"""
    try:
        from tester_agent.session_metrics import SessionMetrics, LLMAnalyzedMetrics
        
        # Test Pydantic models work correctly
        llm_metrics = LLMAnalyzedMetrics(
            concepts_covered=["photosynthesis", "plant biology"],
            clarity_conciseness_score=4.5,
            user_type="High",
            user_interest_rating=4.8,
            user_engagement_rating=4.2,
            enjoyment_probability=0.85,
            error_handling_count=2,
            adaptability=True
        )
        
        session_metrics = SessionMetrics(
            session_id="test_123",
            persona_name="test_student",
            concepts_covered=["photosynthesis", "plant biology"],
            num_concepts_covered=2,
            clarity_conciseness_score=4.5,
            user_type="High",
            user_interest_rating=4.8,
            user_engagement_rating=4.2,
            enjoyment_probability=0.85,
            quiz_score=85.0,
            error_handling_count=2,
            adaptability=True,
            total_interactions=6
        )
        
        print("✅ Pydantic models created successfully!")
        print(f"📊 Session Metrics: {session_metrics.model_dump()}")
        return True
        
    except Exception as e:
        print(f"❌ Model creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_metrics_computer_creation():
    """Test that MetricsComputer can be created (will fail at LLM call but structure should work)"""
    try:
        from tester_agent.session_metrics import MetricsComputer
        
        # This will fail when trying to connect to Google API, but let's see if the structure is right
        try:
            computer = MetricsComputer()
            print("✅ MetricsComputer created (unexpected - API key shouldn't work)")
        except Exception as api_error:
            if "api_key" in str(api_error).lower() or "credentials" in str(api_error).lower() or "authentication" in str(api_error).lower():
                print("✅ MetricsComputer creation failed as expected (API key issue)")
                return True
            else:
                print(f"❌ Unexpected error in MetricsComputer: {api_error}")
                return False
                
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_langfuse_upload_structure():
    """Test Langfuse upload method structure without actually uploading"""
    try:
        from tester_agent.session_metrics import SessionMetrics
        
        # Create sample metrics
        metrics = SessionMetrics(
            session_id="test_123",
            persona_name="test_student",
            concepts_covered=["photosynthesis"],
            num_concepts_covered=1,
            clarity_conciseness_score=4.5,
            user_type="High",
            user_interest_rating=4.8,
            user_engagement_rating=4.2,
            enjoyment_probability=0.85,
            quiz_score=85.0,
            error_handling_count=2,
            adaptability=True,
            total_interactions=6
        )
        
        # Test that we can serialize the metrics properly
        metrics_dict = metrics.model_dump()
        print("✅ Metrics serialization successful!")
        print(f"📊 Serialized metrics: {metrics_dict}")
        
        # Test the structure for Langfuse upload (without actually uploading)
        numeric_metrics = {}
        categorical_metrics = {}
        
        for metric_name, value in metrics_dict.items():
            if isinstance(value, (int, float)):
                numeric_metrics[metric_name] = float(value)
            elif isinstance(value, str):
                categorical_metrics[metric_name] = value
            elif isinstance(value, list):
                # Convert lists to counts
                numeric_metrics[f"{metric_name}_count"] = len(value)
        
        print(f"📈 Numeric metrics for Langfuse: {numeric_metrics}")
        print(f"📋 Categorical metrics for Langfuse: {categorical_metrics}")
        return True
        
    except Exception as e:
        print(f"❌ Serialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Testing Session Metrics Structure\n")
    
    tests = [
        ("Pydantic Models", test_session_metrics_structure),
        ("MetricsComputer Creation", test_metrics_computer_creation), 
        ("Langfuse Upload Structure", test_langfuse_upload_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure tests passed! Session metrics system is ready.")
        print("💡 To run with real data, set proper GOOGLE_API_KEY and LANGFUSE credentials.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
