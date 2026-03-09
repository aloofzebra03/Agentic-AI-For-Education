"""
Test Script: Verify Before/After Removal Modifications
=======================================================
Verifies that the single-simulation URL changes work correctly.
"""

import json
from simulation_to_concept.api_models import ParameterChange, SimulationState
from simulation_to_concept.api_integration import format_api_response
from simulation_to_concept.config import build_simulation_url


def test_parameter_change_model():
    """Test 1: ParameterChange Pydantic model has no URL fields"""
    print("\n" + "="*60)
    print("TEST 1: ParameterChange Model Structure")
    print("="*60)
    
    fields = ParameterChange.model_fields
    
    # Check removed fields
    if 'before_url' in fields or 'after_url' in fields:
        print("❌ FAIL: ParameterChange still has before_url/after_url")
        return False
    else:
        print("✅ PASS: No before_url/after_url fields")
    
    # Check retained fields
    required = ['parameter', 'before', 'after', 'reason']
    missing = [f for f in required if f not in fields]
    if missing:
        print(f"❌ FAIL: Missing fields: {missing}")
        return False
    else:
        print(f"✅ PASS: Has required metadata fields: {required}")
    
    # Create instance
    try:
        pc = ParameterChange(
            parameter="length",
            before=5,
            after=8,
            reason="Test change"
        )
        print(f"✅ PASS: Can create ParameterChange instance")
        print(f"   {pc.model_dump()}")
    except Exception as e:
        print(f"❌ FAIL: Cannot create instance: {e}")
        return False
    
    return True


def test_simulation_state_response():
    """Test 2: format_api_response builds single simulation URL"""
    print("\n" + "="*60)
    print("TEST 2: format_api_response() Output")
    print("="*60)
    
    # Mock state with parameter change
    mock_state = {
        'current_params': {'length': 8, 'number_of_oscillations': 10},
        'parameter_history': [
            {
                'parameter': 'length',
                'old_value': 5,
                'new_value': 8,
                'reason': 'To demonstrate longer pendulum',
                'prediction_asked': 'What do you think will happen?',
                'student_reaction': '',
                'understanding_before': 'none',
                'understanding_after': '',
                'was_effective': False
            }
        ],
        'concepts': [
            {
                'id': 1,
                'title': 'Time Period',
                'description': 'How length affects swing',
                'key_insight': 'Longer = slower',
                'related_params': ['length']
            }
        ],
        'current_concept_index': 0,
        'last_teacher_message': 'Test message',
        'understanding_level': 'none',
        'exchange_count': 1,
        'concept_complete': False,
        'session_complete': False,
        'strategy': 'continue',
        'teacher_mode': 'encouraging'
    }
    
    try:
        response = format_api_response(
            thread_id='test_thread_123',
            state=mock_state,
            simulation_id='simple_pendulum'
        )
        
        print("✅ PASS: format_api_response() executed without error")
        
        # Check simulation field
        sim = response['simulation']
        print(f"\n📊 Simulation field:")
        print(f"   - id: {sim['id']}")
        print(f"   - title: {sim['title']}")
        print(f"   - html_url: {sim['html_url'][:80]}...")
        
        # Check html_url exists and has new params
        if 'html_url' not in sim:
            print("❌ FAIL: No html_url in simulation")
            return False
        if 'length=8' not in sim['html_url']:
            print("❌ FAIL: html_url doesn't have updated params")
            return False
        print("✅ PASS: html_url has current parameters")
        
        # Check param_change
        pc = sim.get('param_change')
        if pc is None:
            print("❌ FAIL: param_change is None (should have data)")
            return False
        
        print(f"\n📊 param_change field:")
        for key, val in pc.items():
            print(f"   - {key}: {val}")
        
        # Check NO URL fields in param_change
        if 'before_url' in pc or 'after_url' in pc:
            print("❌ FAIL: param_change has before_url/after_url")
            return False
        print("✅ PASS: param_change has NO before_url/after_url")
        
        # Check has metadata
        if pc.get('parameter') != 'length':
            print("❌ FAIL: Wrong parameter")
            return False
        if pc.get('before') != 5:
            print("❌ FAIL: Wrong before value")
            return False
        if pc.get('after') != 8:
            print("❌ FAIL: Wrong after value")
            return False
        print("✅ PASS: param_change has correct metadata (parameter, before, after, reason)")
        
    except Exception as e:
        print(f"❌ FAIL: Error in format_api_response(): {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_sample_json():
    """Test 3: sample_api_responses.json has no URL fields"""
    print("\n" + "="*60)
    print("TEST 3: sample_api_responses.json Structure")
    print("="*60)
    
    try:
        with open('sample_api_responses.json', 'r') as f:
            data = json.load(f)
        
        print("✅ PASS: JSON is valid")
        
        # Search for any before_url/after_url
        json_str = json.dumps(data)
        if 'before_url' in json_str or 'after_url' in json_str:
            print("❌ FAIL: sample_api_responses.json still contains before_url/after_url")
            return False
        
        print("✅ PASS: No before_url/after_url in sample JSON")
        
        # Find a param_change and verify structure
        examples = data.get('simple_pendulum_examples', [])
        for ex in examples:
            pc = ex.get('response', {}).get('simulation', {}).get('param_change')
            if pc and isinstance(pc, dict) and 'parameter' in pc:
                print(f"\n📊 Sample param_change from JSON:")
                print(f"   - parameter: {pc.get('parameter')}")
                print(f"   - before: {pc.get('before')}")
                print(f"   - after: {pc.get('after')}")
                print(f"   - reason: {pc.get('reason', '')[:60]}...")
                
                if 'before_url' in pc or 'after_url' in pc:
                    print("❌ FAIL: param_change in sample JSON has URL fields")
                    return False
                print("✅ PASS: Sample param_change has correct structure")
                break
        
    except Exception as e:
        print(f"❌ FAIL: Error reading sample JSON: {e}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 TESTING BEFORE/AFTER REMOVAL MODIFICATIONS")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("ParameterChange Model", test_parameter_change_model()))
    results.append(("format_api_response()", test_simulation_state_response()))
    results.append(("sample_api_responses.json", test_sample_json()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n{'='*60}")
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("="*60)
        print("\n✅ Modifications working correctly!")
        print("   - ParameterChange has no before_url/after_url")
        print("   - API responses contain single html_url")
        print("   - param_change has metadata only (parameter, before, after, reason)")
        return 0
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print("="*60)
        return 1


if __name__ == "__main__":
    exit(main())
