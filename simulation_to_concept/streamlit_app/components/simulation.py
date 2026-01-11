"""
Simulation Component
====================
Handles displaying simulation iframes - single or before/after comparison.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from streamlit_config import build_simulation_url, get_simulation_config, UI_CONFIG


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


def render_simulation_comparison(
    sim_key: str, 
    before_params: dict, 
    after_params: dict,
    before_title: str = "Before",
    after_title: str = "After"
):
    """
    Render two simulations side by side for comparison.
    
    Args:
        sim_key: Simulation key (e.g., "simple_pendulum")
        before_params: Parameters for the "before" state
        after_params: Parameters for the "after" state
        before_title: Title for left simulation
        after_title: Title for right simulation
    """
    config = get_simulation_config(sim_key)
    
    # Build URLs
    before_url = build_simulation_url(sim_key, before_params, auto_start=True)
    after_url = build_simulation_url(sim_key, after_params, auto_start=True)
    
    # Get changed parameters for display
    changed_params = []
    for param_config in config["parameters"]:
        name = param_config["name"]
        display_name = param_config["display_name"]
        unit = param_config.get("unit", "")
        
        before_val = before_params.get(name, "?")
        after_val = after_params.get(name, "?")
        
        if before_val != after_val:
            changed_params.append({
                "name": display_name,
                "before": f"{before_val} {unit}".strip(),
                "after": f"{after_val} {unit}".strip()
            })
    
    # Header showing what changed
    if changed_params:
        change_text = " | ".join([
            f"**{p['name']}**: {p['before']} → {p['after']}" 
            for p in changed_params
        ])
        st.markdown(f"📊 **Parameter Change:** {change_text}")
    
    st.markdown("---")
    
    # Two columns for side-by-side display
    col1, col2 = st.columns(2)
    
    with col1:
        # Before state
        st.markdown(f"### ⬅️ {before_title}")
        if changed_params:
            for p in changed_params:
                st.caption(f"{p['name']}: **{p['before']}**")
        
        st.components.v1.iframe(
            before_url,
            height=UI_CONFIG["simulation_height"],
            scrolling=False
        )
    
    with col2:
        # After state
        st.markdown(f"### ➡️ {after_title}")
        if changed_params:
            for p in changed_params:
                st.caption(f"{p['name']}: **{p['after']}**")
        
        st.components.v1.iframe(
            after_url,
            height=UI_CONFIG["simulation_height"],
            scrolling=False
        )


def render_simulation_container(
    sim_key: str,
    current_params: dict,
    previous_params: dict = None,
    show_comparison: bool = False
):
    """
    Main simulation container - decides whether to show single or comparison view.
    
    Args:
        sim_key: Simulation key
        current_params: Current parameter values
        previous_params: Previous parameter values (for comparison)
        show_comparison: Whether to show before/after comparison
    """
    config = get_simulation_config(sim_key)
    
    # Container with border
    with st.container():
        st.markdown(f"### 🔬 {config['name']}")
        
        if show_comparison and previous_params:
            # Check if params actually changed
            params_changed = any(
                current_params.get(p["name"]) != previous_params.get(p["name"])
                for p in config["parameters"]
            )
            
            if params_changed:
                render_simulation_comparison(
                    sim_key=sim_key,
                    before_params=previous_params,
                    after_params=current_params,
                    before_title="Previous State",
                    after_title="Current State"
                )
            else:
                # No change, show single
                render_simulation_single(sim_key, current_params, "Current State")
        else:
            # Single view
            render_simulation_single(sim_key, current_params, "Current State")
        
        st.markdown("---")


def should_show_simulation(state: dict) -> bool:
    """
    Determine if simulation should be displayed based on state.
    
    Shows simulation when:
    - Teacher suggested a parameter change
    - There's a param change in the latest interaction
    
    Args:
        state: Current teaching state
        
    Returns:
        True if simulation should be shown
    """
    # Check if teacher suggested param change
    if state.get("_last_response", {}).get("suggests_param_change", False):
        return True
    
    # Check if there was a recent param change
    param_history = state.get("parameter_history", [])
    if param_history:
        # Show if there's been any param change
        return True
    
    return False


def get_comparison_params(state: dict) -> tuple:
    """
    Get before and after params for comparison from state.
    
    Args:
        state: Current teaching state
        
    Returns:
        Tuple of (previous_params, current_params, should_compare)
    """
    current_params = state.get("current_params", {})
    param_history = state.get("parameter_history", [])
    
    if param_history:
        last_change = param_history[-1]
        param_name = last_change.get("parameter")
        old_value = last_change.get("old_value")
        
        # Build previous params
        previous_params = current_params.copy()
        if param_name and old_value is not None:
            previous_params[param_name] = old_value
        
        return previous_params, current_params, True
    
    return current_params, current_params, False
