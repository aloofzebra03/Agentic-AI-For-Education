"""
Comprehensive test script for get_ground_truth_from_json function.
Tests various concepts, sections, and edge cases.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.shared_utils import get_ground_truth_from_json

def test_concept(concept: str, section: str, test_name: str):
    """Test a single concept-section combination"""
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"Concept: '{concept}' | Section: '{section}'")
    print(f"{'='*80}")
    try:
        result = get_ground_truth_from_json(concept, section)
        print(f"✅ SUCCESS")
        print(f"Result length: {len(result)} characters")
        print(f"Preview: {result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive tests"""
    print("\n" + "="*80)
    print("COMPREHENSIVE GROUND TRUTH RETRIEVAL TESTS")
    print("="*80)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Pendulum concept (from file 1.json - the main use case)
    if test_concept("Pendulum and its Time Period", "Concept Definition", "Test 1: Pendulum - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: Pendulum - Details
    if test_concept("Pendulum and its Time Period", "Details (facts, sub-concepts)", "Test 2: Pendulum - Details"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Pendulum - Working
    if test_concept("Pendulum and its Time Period", "Working", "Test 3: Pendulum - Working"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Pendulum - MCQs
    if test_concept("Pendulum and its Time Period", "MCQs", "Test 4: Pendulum - MCQs"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Pendulum - Real-life applications
    if test_concept("Pendulum and its Time Period", "Real-Life Application", "Test 5: Pendulum - Real-Life Applications"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 6: Different concept from file 2.json (Acids)
    if test_concept("Acids", "Concept Definition", "Test 6: Acids - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 7: Electric Cell from file 3.json
    if test_concept("Electric cell", "Concept Definition", "Test 7: Electric Cell - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 8: Photosynthesis from file 8.json
    if test_concept("Photosynthesis", "Concept Definition", "Test 8: Photosynthesis - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 9: Case insensitivity test
    if test_concept("PENDULUM AND ITS TIME PERIOD", "concept definition", "Test 9: Case Insensitivity"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 10: Explanation with analogies
    if test_concept("Pendulum and its Time Period", "Explanation (with analogies)", "Test 10: Pendulum - Explanation"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 11: Test non-existent concept
    print(f"\n{'='*80}")
    print(f"TEST: Test 11 - Non-existent Concept (Should gracefully handle)")
    print(f"Concept: 'NonExistentConcept' | Section: 'Concept Definition'")
    print(f"{'='*80}")
    try:
        result = get_ground_truth_from_json("NonExistentConcept", "Concept Definition")
        if "not found" in result.lower():
            print(f"✅ SUCCESS - Correctly handled non-existent concept")
            print(f"Result: {result}")
            tests_passed += 1
        else:
            print(f"⚠️ WARNING - Unexpected result for non-existent concept")
            print(f"Result: {result}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        tests_failed += 1
    
    # Test 12: Test non-existent section
    print(f"\n{'='*80}")
    print(f"TEST: Test 12 - Non-existent Section")
    print(f"Concept: 'Pendulum and its Time Period' | Section: 'NonExistentSection'")
    print(f"{'='*80}")
    try:
        result = get_ground_truth_from_json("Pendulum and its Time Period", "NonExistentSection")
        if "not found" in result.lower():
            print(f"✅ SUCCESS - Correctly handled non-existent section")
            print(f"Result: {result}")
            tests_passed += 1
        else:
            print(f"⚠️ WARNING - Got result for non-existent section")
            print(f"Result preview: {result[:200]}...")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
        tests_failed += 1
    
    # Test 13: Full content retrieval
    if test_concept("Pendulum and its Time Period", "full", "Test 13: Pendulum - Full Content"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 14: Measurement of time (same file as Pendulum)
    if test_concept("Measurement of time", "Concept Definition", "Test 14: Measurement of Time - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 15: Heat from file 23.json
    if test_concept("Heat", "Concept Definition", "Test 15: Heat - Concept Definition"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 16: Different section key variations
    if test_concept("Acids", "real life applications", "Test 16: Section Key Variation - lowercase"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 17: Critical thinking section
    if test_concept("Pendulum and its Time Period", "Critical Thinking", "Test 17: Critical Thinking Section"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 18: Key topics section
    if test_concept("Pendulum and its Time Period", "Key Topics", "Test 18: Key Topics Section"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Final Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📊 Success Rate: {tests_passed}/{tests_passed + tests_failed} ({100*tests_passed/(tests_passed+tests_failed):.1f}%)")
    print("="*80)
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! The function is working correctly.")
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Please review the output above.")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
