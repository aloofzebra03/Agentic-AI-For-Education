"""
Test Client for Teaching Agent API
===================================
Simulates how Android app will interact with the FastAPI server.

Run with: python test_api_client.py

Make sure the API server is running first:
    uvicorn api_server:app --reload --port 8000
"""

import requests
import json
import time
from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

BASE_URL = "http://localhost:8000"


# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def pretty_print(title: str, data: Any):
    """Print JSON data nicely with a title"""
    print("\n" + "="*60)
    print(f"📋 {title}")
    print("="*60)
    print(json.dumps(data, indent=2))
    print("="*60)


def print_section(title: str):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)


def extract_key_info(response_data: Dict[str, Any]):
    """Extract and display key information from response"""
    print(f"\n📌 Key Information:")
    print(f"   Session ID: {response_data.get('session_id', 'N/A')}")
    
    # Teacher message
    teacher_msg = response_data.get('teacher_message', {})
    text = teacher_msg.get('text', '')
    print(f"   Teacher: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    # Simulation
    sim = response_data.get('simulation', {})
    print(f"   Simulation: {sim.get('title', 'N/A')}")
    print(f"   URL: {sim.get('html_url', 'N/A')[:80]}...")
    
    # Parameter change
    if sim.get('param_change'):
        change = sim['param_change']
        print(f"   ⚙️  Parameter Changed: {change['parameter']}")
        print(f"      {change['before']} → {change['after']}")
        print(f"      Reason: {change['reason']}")
    
    # Learning state
    learning = response_data.get('learning_state', {})
    print(f"   Understanding: {learning.get('understanding_level', 'N/A')}")
    print(f"   Exchange Count: {learning.get('exchange_count', 0)}")
    print(f"   Concept Complete: {learning.get('concept_complete', False)}")
    print(f"   Session Complete: {learning.get('session_complete', False)}")
    
    # Concepts
    concepts = response_data.get('concepts', {})
    current_concept = concepts.get('current_concept', {})
    if current_concept:
        print(f"   Current Concept: {current_concept.get('title', 'N/A')}")
        print(f"   Progress: Concept {concepts.get('current_index', 0) + 1} of {concepts.get('total', 0)}")


# ═══════════════════════════════════════════════════════════════════════
# TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def test_health_check():
    """Test 1: Health Check"""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print("✅ API is online!")
            data = response.json()
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            print(f"   Available Simulations: {', '.join(data.get('available_simulations', []))}")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server!")
        print("   Make sure the server is running:")
        print("   uvicorn api_server:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_start_session(simulation_id: str = "simple_pendulum"):
    """Test 2: Start New Session"""
    print_section(f"TEST 2: Start New Session ({simulation_id})")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/session/start",
            json={"simulation_id": simulation_id}
        )
        
        if response.status_code == 201:
            print("✅ Session created successfully!")
            data = response.json()
            extract_key_info(data)
            return data.get('session_id')
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_send_response(session_id: str, student_response: str):
    """Test 3: Send Student Response"""
    print_section("TEST 3: Send Student Response")
    print(f"   Student says: \"{student_response}\"")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/session/{session_id}/respond",
            json={"student_response": student_response}
        )
        
        if response.status_code == 200:
            print("✅ Response processed successfully!")
            data = response.json()
            extract_key_info(data)
            return data
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_session(session_id: str):
    """Test 4: Get Session State"""
    print_section("TEST 4: Get Session State")
    
    try:
        response = requests.get(f"{BASE_URL}/api/session/{session_id}")
        
        if response.status_code == 200:
            print("✅ Session state retrieved successfully!")
            data = response.json()
            extract_key_info(data)
            return data
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_complete_conversation():
    """Test 5: Complete Conversation Flow"""
    print_section("TEST 5: Complete Conversation Flow")
    
    # Start session
    print("\n📍 Step 1: Starting session...")
    session_id = test_start_session("simple_pendulum")
    
    if not session_id:
        print("❌ Cannot continue - session creation failed")
        return
    
    time.sleep(1)  # Simulate human thinking time
    
    # First response - incorrect answer
    print("\n📍 Step 2: Student gives wrong answer...")
    test_send_response(session_id, "I think it swings faster?")
    
    time.sleep(1)
    
    # Second response - observation
    print("\n📍 Step 3: Student observes correctly...")
    test_send_response(session_id, "Yes, I see it's slower now")
    
    time.sleep(1)
    
    # Third response - explanation
    print("\n📍 Step 4: Student explains reasoning...")
    test_send_response(session_id, "Because it has to travel a longer distance?")
    
    time.sleep(1)
    
    # Get final state
    print("\n📍 Step 5: Retrieving final state...")
    test_get_session(session_id)
    
    print("\n" + "="*60)
    print("✅ Complete conversation flow tested!")
    print("="*60)


def test_list_simulations():
    """Test 6: List Available Simulations"""
    print_section("TEST 6: List Available Simulations")
    
    try:
        response = requests.get(f"{BASE_URL}/api/simulations")
        
        if response.status_code == 200:
            print("✅ Simulations retrieved successfully!")
            data = response.json()
            
            print(f"\n📚 Available Simulations: {len(data.get('simulations', []))}")
            for sim in data.get('simulations', []):
                print(f"\n   ID: {sim.get('id')}")
                print(f"   Title: {sim.get('title')}")
                print(f"   Concepts: {sim.get('concepts_count')}")
                print(f"   Description: {sim.get('description', '')[:100]}...")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "🚀"*30)
    print("🧪 TEACHING AGENT API TEST SUITE")
    print("🚀"*30)
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Server not available. Stopping tests.")
        return
    
    time.sleep(1)
    
    # Test 2: List simulations
    test_list_simulations()
    
    time.sleep(1)
    
    # Test 3-5: Complete conversation
    test_complete_conversation()
    
    print("\n" + "🎉"*30)
    print("✅ ALL TESTS COMPLETED!")
    print("🎉"*30)


def interactive_mode():
    """Interactive mode for manual testing"""
    print("\n" + "🎮"*30)
    print("🎮 INTERACTIVE TEST MODE")
    print("🎮"*30)
    
    # Health check first
    if not test_health_check():
        return
    
    # Start session
    sim_id = input("\nEnter simulation ID (simple_pendulum/light_shadows/earth_rotation_revolution): ").strip()
    if not sim_id:
        sim_id = "simple_pendulum"
    
    session_id = test_start_session(sim_id)
    
    if not session_id:
        return
    
    # Interactive conversation loop
    print("\n💬 Now you can chat! (type 'quit' to exit, 'state' to see current state)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'state':
            test_get_session(session_id)
        elif user_input:
            test_send_response(session_id, user_input)


# ═══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_all_tests()
        
        print("\n💡 Tip: Run in interactive mode with:")
        print("   python test_api_client.py --interactive")
