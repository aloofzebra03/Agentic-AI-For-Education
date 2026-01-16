"""
TEST APP: Demonstrating Bi-Directional Communication
====================================================

This is a minimal test app to demonstrate the complete flow:
1. Simulation sends postMessage
2. Custom component receives it
3. Python gets the data
4. We display it

This is SEPARATE from your main project - just for learning/testing!
"""

import streamlit as st
import sys
from pathlib import Path

# ==========================================
# SETUP: Add custom component to path
# ==========================================
component_path = Path(__file__).parent.parent / "04_custom_component"
sys.path.insert(0, str(component_path))

from simulation_bridge import simulation_bridge

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Test: Bi-Directional Communication",
    page_icon="🧪",
    layout="wide"
)

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "interaction_history" not in st.session_state:
    st.session_state.interaction_history = []

# ==========================================
# HEADER
# ==========================================
st.title("🧪 Test: Bi-Directional Communication")

st.markdown("""
This is a **minimal test** to demonstrate the complete approach:
- A simple simulation sends `postMessage` when you move a slider
- The custom component receives it
- Python gets the data and displays it

**Instructions:** Move the slider in the simulation below and watch the "Received Data" section update!
""")

# ==========================================
# LAYOUT: Two columns
# ==========================================
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📺 Test Simulation")
    st.caption("Move the slider to send messages")
    
    # Choose how to load the simulation
    load_method = st.radio(
        "How to load simulation:",
        ["From URL", "From local file"],
        horizontal=True
    )
    
    if load_method == "From local file":
        # Use file:// URL to load local HTML
        test_sim_path = Path(__file__).parent / "test_simulation.html"
        simulation_url = f"file://{test_sim_path.absolute()}"
        
        if not test_sim_path.exists():
            st.error(f"Test simulation not found at: {test_sim_path}")
            st.stop()
    else:
        # Let user enter a URL (useful if they host it somewhere)
        simulation_url = st.text_input(
            "Enter simulation URL:",
            value="https://imhv0609.github.io/simulation_to_concept_version3_github/study/test_example/test_simulation.html"
        )
    
    st.info(f"**Loading from:** `{simulation_url}`")
    
    # ==========================================
    # THE MAGIC: Use the custom component
    # ==========================================
    result = simulation_bridge(
        simulation_url=simulation_url,
        height=500,
        initial_params={"testValue": 50},
        key="test_sim"
    )
    
    # ==========================================
    # PROCESS THE RESULT
    # ==========================================
    if result:
        # Add to history
        st.session_state.interaction_history.append({
            "timestamp": result.get('timestamp', 'N/A'),
            "param": result.get('change', {}).get('param', 'unknown'),
            "oldValue": result.get('change', {}).get('oldValue', 'N/A'),
            "newValue": result.get('change', {}).get('newValue', 'N/A')
        })
        
        # Show success message
        st.success("🎉 Received data from simulation!")
        st.balloons()

with col2:
    st.subheader("📊 Received Data")
    
    if result:
        st.markdown("### Latest Interaction:")
        
        # Display nicely formatted
        change = result.get('change', {})
        st.metric(
            label=f"Parameter: {change.get('param', 'unknown')}",
            value=change.get('newValue', 'N/A'),
            delta=f"{change.get('newValue', 0) - change.get('oldValue', 0)}"
        )
        
        # Show full data structure
        with st.expander("📦 Full Data Structure", expanded=True):
            st.json(result)
        
        # Show Python type
        st.code(f"Type: {type(result)}\n# It's a Python dictionary!", language="python")
        
    else:
        st.info("Waiting for interaction... Move the slider in the simulation!")
    
    # ==========================================
    # INTERACTION HISTORY
    # ==========================================
    st.markdown("---")
    st.subheader("📜 Interaction History")
    
    if st.session_state.interaction_history:
        # Show last 5 interactions
        for idx, interaction in enumerate(reversed(st.session_state.interaction_history[-5:])):
            with st.container():
                st.markdown(f"""
                **#{len(st.session_state.interaction_history) - idx}:** 
                `{interaction['param']}` changed from 
                `{interaction['oldValue']}` → `{interaction['newValue']}`
                """)
        
        # Stats
        st.markdown("---")
        st.metric("Total Interactions", len(st.session_state.interaction_history))
        
        if st.button("🗑️ Clear History"):
            st.session_state.interaction_history = []
            st.rerun()
    else:
        st.write("No interactions yet")

# ==========================================
# EXPLANATION SECTION
# ==========================================
st.markdown("---")

with st.expander("🎓 How This Works", expanded=False):
    st.markdown("""
    ### The Complete Flow:
    
    1. **You move the slider** in the simulation (left side)
    
    2. **Simulation sends postMessage:**
       ```javascript
       window.parent.postMessage({
           type: 'SIMULATION_PARAM_CHANGE',
           change: {param: 'testValue', oldValue: 45, newValue: 67}
       }, '*');
       ```
    
    3. **Custom Component receives it:**
       - JavaScript in `frontend/index.html` listens for messages
       - Calls `Streamlit.setComponentValue(data)`
    
    4. **Streamlit Server translates:**
       - Receives via WebSocket
       - Converts JavaScript → Python
    
    5. **Your Python code gets it:**
       ```python
       result = simulation_bridge(url, height, key)
       # result = {'type': 'SIMULATION_PARAM_CHANGE', 'change': {...}}
       ```
    
    6. **Display it!** (What you see on the right side)
    
    ### Key Technologies:
    - **postMessage API:** Browser-to-browser communication (simulation → component)
    - **WebSocket:** Browser-to-server communication (component → Python)
    - **Streamlit Component API:** JavaScript ↔ Python bridge
    """)

# ==========================================
# DEBUG INFO
# ==========================================
with st.expander("🔧 Debug Information", expanded=False):
    st.markdown("### Component Path")
    st.code(str(component_path))
    
    st.markdown("### Simulation URL")
    st.code(simulation_url)
    
    st.markdown("### Session State")
    st.json({
        "interaction_count": len(st.session_state.interaction_history),
        "keys": list(st.session_state.keys())
    })
