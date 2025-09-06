"""
Test Simulation Flow with Streamlit Rendering
Combines subgraph testing (option 2) with Streamlit rendering (option 4)
This allows testing the complete simulation flow including visual rendering
without running the entire educational agent.
"""

import streamlit as st
import sys
import os
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from educational_agent_with_simulation.graph import StateGraph, AgentState
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
from app_simulation import create_pendulum_simulation_html, display_simulation_if_needed

def create_simulation_subgraph():
    """Create a subgraph containing only simulation nodes for focused testing"""
    
    # Node wrappers for simulation
    def _wrap_sim(fn):
        def inner(state: AgentState) -> AgentState:
            print(f"🔧 SIMULATION NODE: {fn.__name__}")
            return fn(state)
        return inner
    
    def _SIM_CC(s): return _wrap_sim(sim_concept_creator_node)(s)
    def _SIM_VARS(s): return _wrap_sim(sim_vars_node)(s)
    def _SIM_ACTION(s): return _wrap_sim(sim_action_node)(s)
    def _SIM_EXPECT(s): return _wrap_sim(sim_expect_node)(s)
    def _SIM_EXECUTE(s): return _wrap_sim(sim_execute_node)(s)
    def _SIM_OBSERVE(s): return _wrap_sim(sim_observe_node)(s)
    def _SIM_INSIGHT(s): return _wrap_sim(sim_insight_node)(s)
    def _SIM_REFLECT(s): return _wrap_sim(sim_reflection_node)(s)
    
    # Create simulation-only graph
    sim_graph = StateGraph(AgentState)
    
    # Add simulation nodes
    sim_graph.add_node("SIM_CC", _SIM_CC)
    sim_graph.add_node("SIM_VARS", _SIM_VARS)
    sim_graph.add_node("SIM_ACTION", _SIM_ACTION)
    sim_graph.add_node("SIM_EXPECT", _SIM_EXPECT)
    sim_graph.add_node("SIM_EXECUTE", _SIM_EXECUTE)
    sim_graph.add_node("SIM_OBSERVE", _SIM_OBSERVE)
    sim_graph.add_node("SIM_INSIGHT", _SIM_INSIGHT)
    sim_graph.add_node("SIM_REFLECT", _SIM_REFLECT)
    
    # Define simulation flow
    def _route_sim(state: AgentState) -> str:
        return state.get("current_state", "SIM_CC")
    
    # Sequential simulation flow
    sim_graph.add_edge("SIM_CC", "SIM_VARS")
    sim_graph.add_edge("SIM_VARS", "SIM_ACTION")
    sim_graph.add_edge("SIM_ACTION", "SIM_EXPECT")
    sim_graph.add_edge("SIM_EXPECT", "SIM_EXECUTE")
    sim_graph.add_edge("SIM_EXECUTE", "SIM_OBSERVE")
    sim_graph.add_edge("SIM_OBSERVE", "SIM_INSIGHT")
    sim_graph.add_edge("SIM_INSIGHT", "SIM_REFLECT")
    
    # Set entry point
    sim_graph.set_entry_point("SIM_CC")
    sim_graph.set_finish_point("SIM_REFLECT")
    
    return sim_graph.compile()

def initialize_simulation_state(concept: str, student_context: str = "") -> AgentState:
    """Initialize state for simulation testing"""
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
        "misconception_detected": True,  # Trigger simulation
        "sim_variables": [],
        "sim_action_config": {},
        "show_simulation": False,
        "simulation_config": {},
        "_asked_mh": True,  # Simulate coming from MH node
        "_mh_tries": 2,     # Simulate max tries reached
    }

def main():
    st.set_page_config(
        page_title="Simulation Flow Tester", 
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 Simulation Flow Tester")
    st.markdown("**Test the complete simulation flow including Streamlit rendering**")
    
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
    
    # Step-by-step or full flow options
    test_mode = st.sidebar.radio(
        "Test Mode:",
        ["Step-by-step", "Full flow"]
    )
    
    if st.sidebar.button("🚀 Start Simulation Test"):
        st.session_state.simulation_started = True
        st.session_state.current_step = 0
        st.session_state.simulation_state = initialize_simulation_state(concept, student_context)
        st.session_state.simulation_graph = create_simulation_subgraph()
        st.session_state.step_results = []
    
    # Display test results
    if hasattr(st.session_state, 'simulation_started') and st.session_state.simulation_started:
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔄 Simulation Flow Progress")
            
            simulation_nodes = [
                "SIM_CC", "SIM_VARS", "SIM_ACTION", "SIM_EXPECT", 
                "SIM_EXECUTE", "SIM_OBSERVE", "SIM_INSIGHT", "SIM_REFLECT"
            ]
            
            if test_mode == "Step-by-step":
                # Step-by-step execution
                for i, node in enumerate(simulation_nodes):
                    if i <= st.session_state.current_step:
                        if st.button(f"▶️ Execute {node}", key=f"btn_{node}"):
                            try:
                                # Execute single node
                                st.session_state.simulation_state["current_state"] = node
                                
                                # Get the node function
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
                                
                                if node in node_functions:
                                    result_state = node_functions[node](st.session_state.simulation_state)
                                    st.session_state.simulation_state.update(result_state)
                                    st.session_state.step_results.append({
                                        "node": node,
                                        "state": dict(result_state)
                                    })
                                    st.session_state.current_step += 1
                                    st.rerun()
                                    
                            except Exception as e:
                                st.error(f"Error executing {node}: {str(e)}")
                    else:
                        st.write(f"⏳ {node} (pending)")
            
            else:
                # Full flow execution
                if st.button("🚀 Run Complete Simulation Flow"):
                    try:
                        # Execute the full simulation subgraph
                        result = st.session_state.simulation_graph.invoke(
                            st.session_state.simulation_state
                        )
                        st.session_state.simulation_state.update(result)
                        st.session_state.flow_completed = True
                        st.success("✅ Simulation flow completed!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error running simulation flow: {str(e)}")
        
        with col2:
            st.subheader("📊 Current State")
            
            # Display current simulation state
            state = st.session_state.simulation_state
            
            st.write("**Current Node:**", state.get("current_state", "None"))
            st.write("**In Simulation:**", state.get("in_simulation", False))
            st.write("**Show Simulation:**", state.get("show_simulation", False))
            
            # Display simulation concepts if available
            if state.get("sim_concepts"):
                st.write("**Simulation Concepts:**")
                for i, concept in enumerate(state["sim_concepts"]):
                    st.write(f"  {i+1}. {concept}")
            
            # Display simulation variables if available
            if state.get("sim_variables"):
                st.write("**Simulation Variables:**")
                st.json(state["sim_variables"])
            
            # Display simulation config if available
            if state.get("simulation_config"):
                st.write("**Simulation Config:**")
                st.json(state["simulation_config"])
        
        # Simulation Rendering Section
        st.subheader("🎯 Simulation Rendering")
        
        # Check if we should display simulation
        if st.session_state.simulation_state.get("show_simulation", False):
            display_simulation_if_needed(st.session_state.simulation_state)
        else:
            st.info("🔍 Simulation will appear here when SIM_EXECUTE node sets show_simulation=True")
        
        # Step Results Display
        if hasattr(st.session_state, 'step_results') and st.session_state.step_results:
            st.subheader("📋 Step Results")
            
            for step in st.session_state.step_results:
                with st.expander(f"🔍 {step['node']} Results"):
                    
                    # Show messages from this step
                    messages = step['state'].get('messages', [])
                    if messages:
                        latest_msg = messages[-1]
                        if hasattr(latest_msg, 'content'):
                            st.write("**Agent Response:**")
                            st.write(latest_msg.content)
                    
                    # Show key state changes
                    st.write("**Key State Changes:**")
                    relevant_keys = [
                        'sim_concepts', 'sim_variables', 'sim_action_config', 
                        'simulation_config', 'show_simulation', 'current_state'
                    ]
                    
                    for key in relevant_keys:
                        if key in step['state'] and step['state'][key]:
                            st.write(f"- **{key}:** {step['state'][key]}")
        
        # Reset button
        if st.sidebar.button("🔄 Reset Test"):
            for key in ['simulation_started', 'current_step', 'simulation_state', 
                       'simulation_graph', 'step_results', 'flow_completed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    else:
        st.info("👆 Configure your test in the sidebar and click 'Start Simulation Test' to begin")
        
        # Show what this test will do
        st.subheader("📋 What This Test Does")
        st.markdown("""
        This test combines **subgraph testing** with **Streamlit rendering** to:
        
        1. **🎯 Isolated Testing**: Tests only the simulation nodes (SIM_CC → SIM_VARS → ... → SIM_REFLECT)
        2. **👀 Visual Rendering**: Shows the actual pendulum simulation when SIM_EXECUTE runs
        3. **🔍 Step-by-step Debug**: Option to execute nodes one by one to see state changes
        4. **📊 State Monitoring**: Real-time view of simulation state and variables
        5. **🚀 Full Flow**: Option to run the complete simulation flow at once
        
        **Benefits:**
        - Test simulation logic without running the full educational agent
        - See the visual simulation output in Streamlit
        - Debug individual nodes and state transitions
        - Validate the complete simulation experience
        """)

if __name__ == "__main__":
    main()
