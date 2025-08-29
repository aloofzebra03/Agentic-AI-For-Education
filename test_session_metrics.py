#!/usr/bin/env python3
"""Simple test script to verify session metrics functionality"""

def test_imports():
    """Test if all required imports work"""
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
        
        import langfuse
        print("✅ Langfuse imported successfully")
        
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_metrics():
    """Test session metrics computation without Langfuse upload"""
    try:
        from tester_agent.session_metrics import MetricsComputer, SessionMetrics
        
        # Sample conversation data
        history = [
            {'role': 'user', 'content': 'What is photosynthesis?'},
            {'role': 'assistant', 'content': 'Photosynthesis is the process by which plants convert light energy into chemical energy.'},
            {'role': 'user', 'content': 'That makes sense! Can you give me a quiz on this?'},
            {'role': 'assistant', 'content': 'Sure! What is the main product of photosynthesis? A) Oxygen B) Carbon dioxide C) Glucose D) Water'},
            {'role': 'user', 'content': 'I think it is C, glucose'},
            {'role': 'assistant', 'content': 'Excellent! That is correct. Glucose is indeed the main product.'}
        ]
        
        session_state = {'quiz_score': 85.0}
        
        # Create metrics computer
        computer = MetricsComputer()
        
        # Compute metrics without upload
        metrics = computer.compute_session_metrics(
            session_id='test_session_123',
            history=history,
            session_state=session_state,
            persona_name='test_student'
        )
        
        print("✅ Session metrics computed successfully!")
        print(f"📊 Metrics: {metrics.model_dump()}")
        return True
        
    except Exception as e:
        print(f"❌ Session metrics error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Testing Session Metrics System\n")
    
    # Test imports first
    if test_imports():
        print("\n" + "="*50)
        # Test metrics computation
        test_session_metrics()
    else:
        print("❌ Import test failed, skipping metrics test")
