"""
Test SIM_EXECUTE Node and HTML Rendering Only
Focused test for simulation execution and rendering with hardcoded state
"""

import streamlit as st
import sys
import os
from typing import Dict, Any

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import only what we need
try:
    from educational_agent_with_simulation.simulation_nodes import sim_execute_node
    from app_simulation import create_pendulum_simulation_html
    import streamlit.components.v1 as components
    
    IMPORTS_SUCCESS = True
except ImportError as e:
    st.error(f"Import error: {e}")
    IMPORTS_SUCCESS = False

def create_hardcoded_state(test_concept: str = "gravity") -> Dict[str, Any]:
    """Create hardcoded state for testing SIM_EXECUTE node with different physics concepts"""
    
    # Simulate a SimVariable object
    class MockSimVariable:
        def __init__(self, name, role, note=None):
            self.name = name
            self.role = role
            self.note = note
    
    # Define different test scenarios
    test_configs = {
        "gravity": {
            "concept": "pendulum gravity effect on period",
            "last_user_msg": "I don't understand pendulum gravity effect",
            "variables": [
                MockSimVariable("gravity", "independent", "What we will change"),
                MockSimVariable("period", "dependent", "What we will observe"),
                MockSimVariable("pendulum length", "control", "Kept constant at 1m"),
                MockSimVariable("amplitude", "control", "Kept constant at 30°")
            ],
            "action": "change pendulum gravity to see period effect"
        },
        "length": {
            "concept": "pendulum length effect on period", 
            "last_user_msg": "I don't understand pendulum length effect",
            "variables": [
                MockSimVariable("pendulum length", "independent", "What we will change"),
                MockSimVariable("period", "dependent", "What we will observe"),
                MockSimVariable("gravity", "control", "Kept constant at 9.8 m/s²"),
                MockSimVariable("amplitude", "control", "Kept constant at 30°")
            ],
            "action": "change pendulum length to see period effect"
        },
        "amplitude": {
            "concept": "amplitude effect on period",
            "last_user_msg": "I don't understand amplitude effect", 
            "variables": [
                MockSimVariable("amplitude", "independent", "What we will change"),
                MockSimVariable("period", "dependent", "What we will observe"),
                MockSimVariable("pendulum length", "control", "Kept constant at 1m"),
                MockSimVariable("gravity", "control", "Kept constant at 9.8 m/s²")
            ],
            "action": "change starting amplitude to see period effect"
        },
        "mass": {
            "concept": "mass independence in pendulum motion",
            "last_user_msg": "I don't understand why mass doesn't affect period",
            "variables": [
                MockSimVariable("bob mass", "independent", "What we will change"),
                MockSimVariable("period", "dependent", "What we will observe"),
                MockSimVariable("pendulum length", "control", "Kept constant at 1m"),
                MockSimVariable("gravity", "control", "Kept constant at 9.8 m/s²")
            ],
            "action": "change bob mass to show period independence"
        }
    }
    
    config = test_configs.get(test_concept, test_configs["gravity"])
    
    return {
        # Basic state
        "messages": [],
        "current_state": "SIM_EXECUTE",
        "last_user_msg": config["last_user_msg"],
        "agent_output": "",
        
        # Simulation concepts (from SIM_CC)
        "sim_concepts": [config["concept"]],
        "sim_total_concepts": 1,
        "sim_current_idx": 0,

        # Variables (from SIM_VARS) - dynamically set based on test_concept
        "sim_variables": config["variables"],
        
        # Action config (from SIM_ACTION) - simplified
        "sim_action_config": {
            "action": config["action"],
            "rationale": f"this isolates the {test_concept} effect on period",
            "prompt": "Shall we try this demonstration?"
        },
        
        # Simulation flags
        "show_simulation": False,
        "simulation_config": {},
        "in_simulation": True,
        "misconception_detected": True,
        
        # Execute config - will be populated by create_simulation_config() in main simulation
        "sim_execute_config": None,
        
        # Other required state
        "_asked_mh": True,
        "_mh_tries": 2,
        "concepts_completed": False,
        "definition_echoed": False,
        "retrieval_score": 0.0,
        "transfer_success": False,
        "last_correction": None,
        "quiz_score": 0.0,
        "session_summary": {},
    }

def test_sim_execute_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Test the SIM_EXECUTE node with our hardcoded state"""
    try:
        result_state = sim_execute_node(state)
        return result_state
    except Exception as e:
        st.error(f"Error in SIM_EXECUTE node: {str(e)}")
        return state

def test_html_rendering(simulation_config: Dict[str, Any]):
    """Test HTML rendering directly"""
    try:
        if simulation_config:
            st.success("✅ Simulation config found! Attempting to render...")
            
            # Show the config first
            st.subheader("🔧 Simulation Config")
            st.json(simulation_config)
            
            # Try to create HTML
            st.subheader("🎯 HTML Generation Test")
            simulation_html = create_pendulum_simulation_html(simulation_config)
            
            st.success("✅ HTML generated successfully!")
            st.write(f"HTML length: {len(simulation_html)} characters")
            
            # Show a snippet of the HTML
            with st.expander("📄 HTML Preview (first 500 chars)"):
                st.code(simulation_html[:500] + "...", language="html")
            
            # Try to render it
            st.subheader("🎬 Simulation Rendering")
            components.html(simulation_html, height=500, scrolling=True)
            
            st.info("🔬 **Simulation should be running above** - Look for the pendulum animation!")
            
        else:
            st.error("❌ No simulation config found")
            
    except Exception as e:
        st.error(f"❌ Error in HTML rendering: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def main():
    st.set_page_config(
        page_title="SIM_EXECUTE & Rendering Test", 
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 SIM_EXECUTE Node & HTML Rendering Test")
    st.markdown("**Focused test for simulation execution and rendering**")
    
    if not IMPORTS_SUCCESS:
        st.error("❌ Could not import required modules. Please check your environment.")
        return
    
    # Concept selection
    st.subheader("🔬 Select Physics Concept to Test")
    test_concept = st.selectbox(
        "Choose which physics concept to test:",
        options=["gravity", "length", "amplitude", "mass"],
        index=0,  # Default to gravity
        help="Each concept tests different pendulum parameters"
    )
    
    # Show what this concept tests
    concept_info = {
        "gravity": "🌍 Tests how gravity affects pendulum period (9.8 → 50.0 m/s²)",
        "length": "📏 Tests how length affects pendulum period (1.0 → 2.0 m)", 
        "amplitude": "📐 Tests how amplitude affects pendulum period (30° → 60°)",
        "mass": "⚖️ Tests mass independence in pendulum motion (1.0 → 5.0 kg)"
    }
    st.info(concept_info[test_concept])
    
    # Initialize test state
    if st.button("🔧 Initialize Hardcoded State"):
        st.session_state.test_state = create_hardcoded_state(test_concept)
        st.success(f"✅ Hardcoded state initialized for {test_concept} concept!")
        st.json(st.session_state.test_state)
    
    if hasattr(st.session_state, 'test_state'):
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎮 Execute SIM_EXECUTE Node")
            
            # Show current state before execution
            st.write("**Before Execution:**")
            st.write(f"- show_simulation: {st.session_state.test_state.get('show_simulation')}")
            st.write(f"- simulation_config: {bool(st.session_state.test_state.get('simulation_config'))}")
            
            if st.button("▶️ Execute SIM_EXECUTE Node"):
                with st.spinner("Executing SIM_EXECUTE node..."):
                    result_state = test_sim_execute_node(st.session_state.test_state)
                    st.session_state.test_state.update(result_state)
                
                st.success("✅ SIM_EXECUTE completed!")
                
                # Show state after execution
                st.write("**After Execution:**")
                st.write(f"- show_simulation: {st.session_state.test_state.get('show_simulation')}")
                st.write(f"- simulation_config: {bool(st.session_state.test_state.get('simulation_config'))}")
                
                # Show agent output
                agent_output = st.session_state.test_state.get('agent_output', '')
                if agent_output:
                    st.write("**Agent Message:**")
                    st.info(agent_output)
        
        with col2:
            st.subheader("📊 State Monitor")
            
            state = st.session_state.test_state
            
            # Key indicators
            st.metric("Show Simulation", "✅ Yes" if state.get("show_simulation") else "❌ No")
            st.metric("Has Config", "✅ Yes" if state.get("simulation_config") else "❌ No")
            
            # Current concept
            concepts = state.get("sim_concepts", [])
            current_idx = state.get("sim_current_idx", 0)
            if concepts and current_idx < len(concepts):
                st.write(f"**Current Concept:** {concepts[current_idx]}")
            
            # Variables summary
            variables = state.get("sim_variables", [])
            if variables:
                st.write("**Variables:**")
                for var in variables:
                    st.write(f"- {var.name} ({var.role})")
        
        # Rendering Test Section
        st.subheader("🎯 Simulation Rendering Test")
        
        if st.session_state.test_state.get("show_simulation", False):
            simulation_config = st.session_state.test_state.get("simulation_config")
            test_html_rendering(simulation_config)
        else:
            st.info("🔍 Execute SIM_EXECUTE node first to trigger simulation rendering")
    
    else:
        st.info("👆 Click 'Initialize Hardcoded State' to begin testing")
        
        # Show what this test does
        st.subheader("📋 About This Test")
        st.markdown("""
        This test focuses specifically on:
        
        1. **🎯 SIM_EXECUTE Node**: Tests the node that creates simulation config and sets rendering flags
        2. **🎨 HTML Generation**: Tests `create_pendulum_simulation_html()` function
        3. **🖥️ Streamlit Rendering**: Tests `components.html()` display
        4. **🔧 State Management**: Uses hardcoded state to isolate rendering issues
        
        **Test Flow:**
        1. Initialize hardcoded state with length-based simulation
        2. Execute SIM_EXECUTE node
        3. Check if simulation config is created
        4. Test HTML generation and rendering
        
        **Focus**: Only testing pendulum length effect for now
        """)

if __name__ == "__main__":
    main()
