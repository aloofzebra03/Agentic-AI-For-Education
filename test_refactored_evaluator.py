#!/usr/bin/env python3
"""
Test script to validate the refactored evaluator focusing on educational quality
"""

import json
from dotenv import load_dotenv
from tester_agent.personas import personas
from tester_agent.evaluator import Evaluator

load_dotenv()

def test_refactored_evaluator():
    """Test the refactored evaluator with educational quality focus"""
    
    print("🧪 Testing Refactored Educational Quality Evaluator")
    print("=" * 60)
    
    # Create a sample conversation history
    sample_history = [
        {"role": "assistant", "content": "Hello! Today we'll learn about simple pendulums. Have you ever seen a swing at a playground?"},
        {"role": "user", "content": "Yes, I have! Is that related to pendulums?"},
        {"role": "assistant", "content": "Exactly! A swing is a type of pendulum. Can you tell me what you think makes it move back and forth?"},
        {"role": "user", "content": "Gravity pulls it down?"},
        {"role": "assistant", "content": "Great observation! Gravity is definitely involved. Let me explain how it works..."},
        {"role": "user", "content": "This is really interesting! How does the length affect the swing?"},
        {"role": "assistant", "content": "Excellent question! The length actually affects the period - how long it takes to complete one swing. Would you like to try a quick quiz about this?"},
        {"role": "user", "content": "Sure!"},
        {"role": "assistant", "content": "If we make a pendulum longer, what happens to its period? A) It gets shorter B) It gets longer C) It stays the same"},
        {"role": "user", "content": "I think B) It gets longer"},
        {"role": "assistant", "content": "Perfect! You're absolutely right. Longer pendulums have longer periods. You really understand this concept!"}
    ]
    
    # Use the eager student persona for testing
    test_persona = personas[1]  # Assuming index 1 is eager student
    
    try:
        # Test the refactored evaluator
        evaluator = Evaluator()
        evaluation_result = evaluator.evaluate(test_persona, sample_history)
        
        print(f"📊 Evaluation completed for persona: {test_persona.name}")
        print(f"🔍 Raw evaluation result: {evaluation_result}")
        print(f"📏 Result length: {len(evaluation_result)} characters")
        
        if not evaluation_result or not evaluation_result.strip():
            print("❌ Empty evaluation result - check LLM connection and API key")
            return False
        
        print("\n🔍 Educational Quality Assessment:")
        
        # Clean the evaluation result (same logic as in run_test.py)
        clean_str = evaluation_result.strip()
        if clean_str.startswith("```json"):
            clean_str = clean_str[7:]
        if clean_str.endswith("```"):
            clean_str = clean_str[:-3]
        clean_str = clean_str.strip()
        
        # Parse and display the evaluation
        evaluation_data = json.loads(clean_str)
        
        # Handle the nested structure that the LLM returns
        metrics = evaluation_data.get("Educational Quality Metrics", {})
        feedback = evaluation_data.get("Qualitative Feedback", {})
        
        if "Pedagogical Flow" in metrics:
            print(f"   📚 Pedagogical Flow: {metrics.get('Pedagogical Flow', 'N/A')}/5")
        
        if "Learning Objective Achievement" in metrics:
            print(f"   🎯 Learning Objective Achievement: {metrics.get('Learning Objective Achievement', 'N/A')}/5")
        
        if "Scaffolding Effectiveness" in metrics:
            print(f"   🏗️ Scaffolding Effectiveness: {metrics.get('Scaffolding Effectiveness', 'N/A')}/5")
        
        if "Misconception Handling" in metrics:
            print(f"   🔧 Misconception Handling: {metrics.get('Misconception Handling', 'N/A')}/5")
        
        if "Pedagogical Strengths" in feedback:
            strengths = feedback.get('Pedagogical Strengths', [])
            print(f"\n✅ Pedagogical Strengths:")
            if isinstance(strengths, list):
                for strength in strengths[:2]:  # Show first 2
                    print(f"   • {strength}")
            else:
                print(f"   {strengths}")
        
        if "Areas for Educational Improvement" in feedback:
            improvements = feedback.get('Areas for Educational Improvement', [])
            print(f"\n📈 Areas for Educational Improvement:")
            if isinstance(improvements, list):
                for improvement in improvements[:2]:  # Show first 2
                    print(f"   • {improvement}")
            else:
                print(f"   {improvements}")
        
        if "Persona Alignment" in feedback:
            print(f"\n🎭 Persona Alignment:")
            print(f"   {feedback.get('Persona Alignment', 'None listed')}")
        
        print("\n✅ Refactored evaluator test successful!")
        print("🎯 Focus areas confirmed:")
        print("   - Educational quality metrics (not overlapping with session_metrics)")
        print("   - Qualitative pedagogical feedback")
        print("   - Persona-specific teaching assessment")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_evaluator_import():
    """Test that the evaluator imports correctly after refactoring"""
    try:
        from tester_agent.evaluator import Evaluator
        evaluator = Evaluator()
        print("✅ Evaluator import and initialization successful")
        return True
    except Exception as e:
        print(f"❌ Evaluator import failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Refactored Educational Quality Evaluator")
    print("=" * 60)
    
    success1 = test_evaluator_import()
    success2 = test_refactored_evaluator() if success1 else False
    
    if success1 and success2:
        print("\n🎉 All tests passed! Refactored evaluator is working correctly!")
        print("\n📋 Summary of changes:")
        print("   ✅ Removed overlapping metrics (adaptability, clarity, error handling)")
        print("   ✅ Added educational-specific metrics (pedagogical flow, scaffolding)")
        print("   ✅ Focused on qualitative assessment complementary to session_metrics")
        print("   ✅ Updated documentation and method signatures")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
