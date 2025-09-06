"""
Simplified Simulation Flow Tester
Direct testing of simulation nodes with Streamlit rendering
No graph compilation required - just direct node execution
"""

import streamlit as st
import sys
import os
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import simulation nodes directly
try:
    from educational_agent_with_simulation.simulation_nodes import (
        sim_concept_creator_node,
        sim_vars_node,
        sim_action_node,
        sim_expect_node,
        sim_execute_node,
        sim_observe_node,
        sim_insight_node,
        sim_reflection_node,
    )
    from app_simulation import display_simulation_if_needed
    
    IMPORTS_SUCCESS = True
except ImportError as e:
    st.error(f"Import error: {e}")
    IMPORTS_SUCCESS = False

def initialize_test_state(concept: str, student_context: str = "") -> Dict[str, Any]:
    """Initialize state for direct node testing"""
    return {
        "messages": [
            HumanMessage(content=f"I'm struggling with {concept}. {student_context}")
        ],
        "current_state": "SIM_CC",
        "last_user_msg": f"I'm struggling with {concept}. {student_context}",
        "sim_concepts": [],
        "sim_total_concepts": 0,
        "sim_current_idx": 0,
        "concepts_completed": False,
        "in_simulation": True,
        "misconception_detected": True,
        "sim_variables": [],
        "sim_action_config": {},
        "show_simulation": False,
        "simulation_config": {},
        "_asked_mh": True,
        "_mh_tries": 2,
        "agent_output": "",
        "_asked_apk": False,
        "_asked_ci": False,
        "_asked_ge": False,
        "_asked_ar": False,
        "_asked_tc": False,
        "_asked_rlc": False,
        "_apk_tries": 0,
        "_ci_tries": 0,
        "_rlc_tries": 0,
        "definition_echoed": False,
        "retrieval_score": 0.0,
        "transfer_success": False,
        "last_correction": None,
        "quiz_score": 0.0,
        "session_summary": {},
    }

def execute_simulation_node(node_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single simulation node and return updated state"""
    
    node_functions = {
        "SIM_CC": sim_concept_creator_node,
        "SIM_VARS": sim_vars_node,
        "SIM_ACTION": sim_action_node,
        "SIM_EXPECT": sim_expect_node,
        "SIM_EXECUTE": sim_execute_node,
        "SIM_OBSERVE": sim_observe_node,
        "SIM_INSIGHT": sim_insight_node,
        "SIM_REFLECT": sim_reflection_node,
    }
    
    if node_name not in node_functions:
        raise ValueError(f"Unknown node: {node_name}")
    
    # Set current state
    state["current_state"] = node_name
    
    try:
        # Execute the node function
        result_state = node_functions[node_name](state)
        return result_state
    except Exception as e:
        st.error(f"Error executing {node_name}: {str(e)}")
        return state

def main():
    st.set_page_config(
        page_title="Simple Simulation Tester", 
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 Simple Simulation Flow Tester")
    st.markdown("**Direct testing of simulation nodes with Streamlit rendering**")
    
    if not IMPORTS_SUCCESS:
        st.error("❌ Could not import required modules. Please check your environment.")
        return
    
    # Sidebar for test configuration
    st.sidebar.header("Test Configuration")
    
    concept = st.sidebar.selectbox(
        "Select Concept to Test:",
        ["pendulum motion", "simple harmonic motion", "oscillations", "wave motion", "frequency and period"]
    )
    
    student_context = st.sidebar.text_area(
        "Student Context (optional):",
        placeholder="e.g., I don't understand why the period doesn't depend on mass...",
        height=100
    )
    
    if st.sidebar.button("🔄 Initialize Test State"):
        st.session_state.test_state = initialize_test_state(concept, student_context)
        st.session_state.execution_log = []
        st.success("✅ Test state initialized!")
    
    # Main content
    if hasattr(st.session_state, 'test_state'):
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎮 Manual Node Execution")
            
            simulation_nodes = [
                ("SIM_CC", "Concept Creator"),
                ("SIM_VARS", "Variables Identification"),
                ("SIM_ACTION", "Action Planning"),
                ("SIM_EXPECT", "Expectation Setting"),
                ("SIM_EXECUTE", "Simulation Execution"),
                ("SIM_OBSERVE", "Observation"),
                ("SIM_INSIGHT", "Insight Generation"),
                ("SIM_REFLECT", "Reflection"),
            ]
            
            st.write("**Click any node to execute:**")
            
            for node_code, node_name in simulation_nodes:
                if st.button(f"▶️ {node_name} ({node_code})", key=f"btn_{node_code}"):
                    try:
                        # Execute the node
                        with st.spinner(f"Executing {node_name}..."):
                            result_state = execute_simulation_node(node_code, st.session_state.test_state)
                            st.session_state.test_state.update(result_state)
                            
                            # Log the execution
                            st.session_state.execution_log.append({
                                "node": node_code,
                                "name": node_name,
                                "timestamp": str(st.session_state.get('execution_count', 0)),
                                "success": True
                            })
                            
                            st.session_state.execution_count = st.session_state.get('execution_count', 0) + 1
                            
                        st.success(f"✅ {node_name} executed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error executing {node_name}: {str(e)}")
                        st.session_state.execution_log.append({
                            "node": node_code,
                            "name": node_name,
                            "timestamp": str(st.session_state.get('execution_count', 0)),
                            "success": False,
                            "error": str(e)
                        })
            
            # Auto-flow execution
            st.write("---")
            if st.button("🚀 Execute Full Simulation Flow"):
                progress_bar = st.progress(0)
                
                for i, (node_code, node_name) in enumerate(simulation_nodes):
                    try:
                        with st.spinner(f"Executing {node_name}..."):
                            result_state = execute_simulation_node(node_code, st.session_state.test_state)
                            st.session_state.test_state.update(result_state)
                            
                            progress_bar.progress((i + 1) / len(simulation_nodes))
                            
                            st.session_state.execution_log.append({
                                "node": node_code,
                                "name": node_name,
                                "timestamp": f"auto_{i}",
                                "success": True
                            })
                    
                    except Exception as e:
                        st.error(f"❌ Error in {node_name}: {str(e)}")
                        break
                
                st.success("✅ Full simulation flow completed!")
                st.rerun()
        
        with col2:
            st.subheader("📊 Current State Monitor")
            
            state = st.session_state.test_state
            
            # Key state indicators
            st.metric("Current Node", state.get("current_state", "None"))
            st.metric("In Simulation", "✅ Yes" if state.get("in_simulation") else "❌ No")
            st.metric("Show Simulation", "✅ Yes" if state.get("show_simulation") else "❌ No")
            
            # Concepts and variables
            if state.get("sim_concepts"):
                st.write("**📝 Simulation Concepts:**")
                for i, concept in enumerate(state["sim_concepts"]):
                    st.write(f"  {i+1}. {concept}")
            
            if state.get("sim_variables"):
                st.write("**🔧 Simulation Variables:**")
                st.json(state["sim_variables"])
            
            if state.get("simulation_config"):
                st.write("**⚙️ Simulation Config:**")
                st.json(state["simulation_config"])
            
            # Latest message
            messages = state.get("messages", [])
            if messages:
                latest_msg = messages[-1]
                if hasattr(latest_msg, 'content') and latest_msg.content:
                    st.write("**💬 Latest Agent Response:**")
                    st.text_area(
                        "Response:",
                        latest_msg.content,
                        height=150,
                        disabled=True
                    )
        
        # Simulation Rendering Section
        st.subheader("🎯 Simulation Rendering Test")
        
        if st.session_state.test_state.get("show_simulation", False):
            st.success("🎉 Simulation is ready to display!")
            try:
                display_simulation_if_needed(st.session_state.test_state)
            except Exception as e:
                st.error(f"Error displaying simulation: {str(e)}")
        else:
            st.info("🔍 Execute SIM_EXECUTE node to trigger simulation display")
        
        # Execution Log
        if hasattr(st.session_state, 'execution_log') and st.session_state.execution_log:
            st.subheader("📋 Execution Log")
            
            for entry in reversed(st.session_state.execution_log[-10:]):  # Show last 10
                status = "✅" if entry["success"] else "❌"
                st.write(f"{status} **{entry['name']}** ({entry['node']})")
                if not entry["success"] and "error" in entry:
                    st.text(f"   Error: {entry['error']}")
        
        # Debug state dump
        with st.expander("🔍 Full State Debug"):
            st.json(st.session_state.test_state)
    
    else:
        st.info("👆 Click 'Initialize Test State' in the sidebar to begin testing")
        
        # Show what this test does
        st.subheader("📋 About This Tester")
        st.markdown("""
        This simplified tester allows you to:
        
        1. **🎯 Direct Node Testing**: Execute simulation nodes individually without graph compilation
        2. **👀 Visual Rendering**: See the pendulum simulation when SIM_EXECUTE runs  
        3. **📊 State Monitoring**: Real-time view of simulation state changes
        4. **🚀 Full Flow Testing**: Execute the complete simulation sequence
        5. **🐛 Debug Support**: Full state inspection and execution logging
        
        **Perfect for:**
        - Testing individual node logic
        - Debugging state transitions
        - Validating simulation rendering
        - Quick iteration during development
        """)

if __name__ == "__main__":
    main()
