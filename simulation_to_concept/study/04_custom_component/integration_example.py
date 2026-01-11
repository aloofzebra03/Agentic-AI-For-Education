"""
Integration Example: Simulation Bridge + Teaching Agent
=======================================================

This file shows how to integrate the bi-directional simulation
bridge with your existing teaching agent setup.

The key idea:
- When the AGENT changes parameters → teach proactively
- When the STUDENT changes parameters → respond to exploration

This creates a more interactive learning experience!
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directories to path for imports
current_dir = Path(__file__).parent
study_dir = current_dir.parent
project_dir = study_dir.parent
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(project_dir / "streamlit_app"))

# Import the custom component
from simulation_bridge import simulation_bridge


def detect_exploration_context(change_data: dict) -> str:
    """
    Analyze what the student changed and generate a context message
    for the teaching agent.
    
    Returns a natural language description of the student's exploration.
    """
    if not change_data:
        return None
    
    param = change_data.get('change', {}).get('param', 'unknown')
    old_val = change_data.get('change', {}).get('oldValue', '?')
    new_val = change_data.get('change', {}).get('newValue', '?')
    
    # Generate contextual message based on what changed
    exploration_messages = {
        'length': f"I noticed you changed the pendulum length from {old_val} to {new_val}. "
                  f"This is great exploration! Let me explain what happens when we change the length...",
        
        'oscillations': f"You increased the oscillations to {new_val}. "
                       f"Running more oscillations helps us see patterns more clearly!",
        
        'gravity': f"Interesting! You changed gravity from {old_val} to {new_val}. "
                  f"This lets us see what a pendulum would do on different planets!",
        
        'amplitude': f"You adjusted the starting amplitude to {new_val}. "
                    f"For small amplitudes, the period stays nearly constant (isochronous motion).",
        
        'damping': f"You're exploring damping effects! With damping={new_val}, "
                  f"we can see how energy is gradually lost to friction.",
    }
    
    return exploration_messages.get(
        param,
        f"I see you changed {param} from {old_val} to {new_val}. "
        f"Let's explore what effect this has on the pendulum's motion!"
    )


def get_teaching_prompt_for_exploration(change_data: dict) -> str:
    """
    Generate a prompt for the teaching agent to respond to student exploration.
    
    This would be sent to your LangGraph agent to generate a contextual response.
    """
    param = change_data.get('change', {}).get('param', 'unknown')
    old_val = change_data.get('change', {}).get('oldValue', '?')
    new_val = change_data.get('change', {}).get('newValue', '?')
    all_params = change_data.get('allParams', {})
    
    prompt = f"""
The student is learning about pendulums and just made an independent exploration:
They changed the {param} from {old_val} to {new_val}.

Current simulation state: {all_params}

Please respond to their exploration:
1. Acknowledge their curiosity and initiative
2. Explain what physical effect this change has
3. Connect it to the underlying physics concept
4. If relevant, suggest what they might try next

Keep the response conversational and encouraging.
"""
    return prompt


# ============================================================
# Demo App
# ============================================================

def main():
    st.set_page_config(
        page_title="Interactive Teaching Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Interactive Teaching with Exploration Detection")
    
    st.markdown("""
    This demo shows how to detect and respond to **student-initiated exploration**.
    
    - The simulation below starts with the agent's suggested parameters
    - If you change parameters directly in the simulation, the system detects it
    - The teaching agent can then respond to your exploration!
    """)
    
    # Initialize session state
    if "agent_params" not in st.session_state:
        st.session_state.agent_params = {
            "length": 5,
            "oscillations": 10
        }
    if "exploration_history" not in st.session_state:
        st.session_state.exploration_history = []
    if "agent_responses" not in st.session_state:
        st.session_state.agent_responses = []
    
    # Build simulation URL with agent's parameters
    base_url = "https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html"
    params = st.session_state.agent_params
    simulation_url = f"{base_url}?length={params['length']}&oscillations={params['oscillations']}&autoStart=true"
    
    # Two columns: Simulation | Teaching Assistant
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("🔬 Simulation")
        st.caption(f"Current params: length={params['length']}, oscillations={params['oscillations']}")
        
        # Use our custom bridge component
        student_change = simulation_bridge(
            simulation_url=simulation_url,
            height=550,
            initial_params=params,
            key="teaching_sim"
        )
        
        # Check if student explored
        if student_change:
            st.success("🎉 Exploration detected!")
            
            # Store in history
            st.session_state.exploration_history.append(student_change)
            
            # Generate teaching response
            response = detect_exploration_context(student_change)
            st.session_state.agent_responses.append({
                "trigger": student_change,
                "response": response
            })
            
            # Update our tracked params
            if student_change.get('allParams'):
                st.session_state.agent_params.update(student_change['allParams'])
    
    with col2:
        st.subheader("💬 Teaching Assistant")
        
        # Show initial guidance
        st.info("""
        👋 Welcome! I've set up a pendulum with:
        - Length: 5 units
        - Oscillations: 10
        
        Try changing the parameters in the simulation to explore!
        """)
        
        # Show responses to student exploration
        if st.session_state.agent_responses:
            st.markdown("---")
            st.markdown("**Your Explorations:**")
            
            for item in st.session_state.agent_responses[-5:]:  # Last 5
                change = item['trigger'].get('change', {})
                with st.chat_message("assistant"):
                    st.markdown(item['response'])
                    
        # Agent-controlled teaching (would integrate with your actual agent)
        st.markdown("---")
        if st.button("🎯 Agent: Teach about Period"):
            st.session_state.agent_params = {"length": 10, "oscillations": 20}
            st.info("I've increased the length to show you how period changes!")
            st.rerun()
    
    # Debug panel
    with st.expander("🔧 Debug: Exploration History"):
        if st.session_state.exploration_history:
            for i, exp in enumerate(st.session_state.exploration_history):
                st.json(exp)
        else:
            st.write("No explorations yet. Try changing parameters in the simulation!")
        
        # Show the prompt that would go to the agent
        if st.session_state.exploration_history:
            latest = st.session_state.exploration_history[-1]
            st.markdown("**Agent Prompt (for actual integration):**")
            st.code(get_teaching_prompt_for_exploration(latest))


if __name__ == "__main__":
    main()
