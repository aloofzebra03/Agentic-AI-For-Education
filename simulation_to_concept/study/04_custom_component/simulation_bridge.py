"""
Simulation Bridge - Custom Streamlit Component
=============================================

This is a custom Streamlit component that:
1. Embeds a simulation iframe
2. Listens for postMessage events from the simulation
3. Sends received data back to Python/Streamlit

Usage:
    from simulation_bridge import simulation_bridge
    
    params = simulation_bridge(
        simulation_url="https://your-simulation-url.com",
        key="my_simulation"
    )
    
    if params:
        st.write(f"Student changed: {params}")
"""

import os
import streamlit.components.v1 as components

# Determine if we're in development or release mode
_RELEASE = False  # Set to True when packaging for distribution

if not _RELEASE:
    # Development mode: serve from local frontend folder
    _component_func = components.declare_component(
        "simulation_bridge",
        path=os.path.join(os.path.dirname(__file__), "frontend")
    )
else:
    # Release mode: component is built and served from package
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _component_func = components.declare_component("simulation_bridge", path=build_dir)


def simulation_bridge(
    simulation_url: str,
    height: int = 600,
    initial_params: dict = None,
    key: str = None
) -> dict:
    """
    Create a simulation bridge component.
    
    This component embeds a simulation iframe and listens for parameter
    changes that the student makes directly in the simulation.
    
    Parameters
    ----------
    simulation_url : str
        URL of the simulation to embed
    height : int
        Height of the iframe in pixels
    initial_params : dict
        Initial parameters (for display/reference)
    key : str
        Unique key for this component instance
        
    Returns
    -------
    dict or None
        Dictionary containing parameter change info when student
        interacts with simulation, None otherwise.
        
        Structure:
        {
            'type': 'SIMULATION_PARAM_CHANGE',
            'change': {
                'param': 'length',
                'oldValue': 5,
                'newValue': 8
            },
            'allParams': {'length': 8, 'oscillations': 10},
            'timestamp': 1703750400000,
            'source': 'pendulum_simulation'
        }
    """
    component_value = _component_func(
        simulation_url=simulation_url,
        height=height,
        initial_params=initial_params or {},
        key=key,
        default=None
    )
    
    return component_value


# For testing the component directly
if __name__ == "__main__":
    import streamlit as st
    
    st.set_page_config(page_title="Simulation Bridge Test", layout="wide")
    st.title("🔬 Simulation Bridge Component Test")
    
    st.markdown("""
    This page tests the custom Streamlit component that bridges
    communication between the simulation iframe and Streamlit.
    
    **How it works:**
    1. The component embeds the simulation in an iframe
    2. It listens for `postMessage` events from the simulation
    3. When the simulation sends a parameter change, it's returned to Python
    """)
    
    # Test with a simulation URL
    simulation_url = st.text_input(
        "Simulation URL",
        value="https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html?length=5&oscillations=10&autoStart=true"
    )
    
    height = st.slider("Height", 400, 800, 600)
    
    st.markdown("---")
    st.subheader("Simulation (interact with it!)")
    
    # Use the component
    result = simulation_bridge(
        simulation_url=simulation_url,
        height=height,
        initial_params={"length": 5, "number_of_oscillations": 10},
        key="test_simulation"
    )
    
    # Display results
    st.markdown("---")
    st.subheader("Received from Simulation")
    
    if result:
        st.success("🎉 Parameter change detected!")
        st.json(result)
        
        # Store in session state for tracking
        if "param_changes" not in st.session_state:
            st.session_state.param_changes = []
        st.session_state.param_changes.append(result)
        
        st.subheader("Change History")
        for i, change in enumerate(st.session_state.param_changes[-5:]):  # Last 5
            st.write(f"{i+1}. {change.get('change', {}).get('param')}: "
                    f"{change.get('change', {}).get('oldValue')} → "
                    f"{change.get('change', {}).get('newValue')}")
    else:
        st.info("Waiting for student to interact with simulation...")
        st.caption("(If your simulation doesn't send postMessage events, you won't see anything here)")
