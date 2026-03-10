"""
Simulation Component
====================
Handles displaying simulation iframes (single view).
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from simulation_to_concept.streamlit_config import build_simulation_url, get_simulation_config, UI_CONFIG


def render_simulation_single(sim_key: str, params: dict, title: str = "Simulation"):
    """
    Render a single simulation iframe.
    
    Args:
        sim_key: Simulation key (e.g., "simple_pendulum")
        params: Current parameter values
        title: Title to display above simulation
    """
    url = build_simulation_url(sim_key, params, auto_start=True)
    
    if title:
        st.markdown(f"**{title}**")
    st.components.v1.iframe(
        url,
        height=UI_CONFIG["simulation_height"],
        scrolling=True
    )

