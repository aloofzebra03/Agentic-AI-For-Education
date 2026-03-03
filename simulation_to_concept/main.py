"""
Main Entry Point - Terminal Runner
==================================
Interactive terminal interface for the Version 3 Teaching Agent.

Run with: python main.py
"""

import uuid
import sys
from typing import Dict, Any

import webbrowser

from config import (
    validate_config, 
    TOPIC_DESCRIPTION, 
    INITIAL_PARAMS,
    MAX_EXCHANGES,
    build_simulation_url
)
from state import create_initial_state
from graph import start_session, continue_session


def print_header():
    """Print welcome header."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🎓 ADAPTIVE PHYSICS TUTOR - Version 3".center(68) + "║")
    print("║" + "  Interactive Teaching with Parameter History".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    print()


def print_simulation_state(params: Dict[str, float]):
    """Display current simulation parameters."""
    print("\n┌" + "─"*50 + "┐")
    print("│" + " 🧪 SIMULATION STATE".ljust(50) + "│")
    print("├" + "─"*50 + "┤")
    print(f"│  Length:       {params.get('length', 5)} units".ljust(51) + "│")
    print(f"│  Oscillations: {params.get('number_of_oscillations', 10)} count".ljust(51) + "│")
    print("└" + "─"*50 + "┘")


def print_teacher_message(message: str):
    """Display teacher's message in a nice format."""
    print("\n" + "─"*60)
    print("🎓 Teacher Alex:")
    print("─"*60)
    # Word wrap the message
    words = message.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > 58:
            print(f"  {line}")
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        print(f"  {line}")
    print("─"*60)


def print_progress(state: Dict[str, Any]):
    """Display learning progress."""
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    understanding = state.get("understanding_level", "none")
    trajectory = state.get("trajectory_status", "improving")
    exchange = state.get("exchange_count", 0)
    
    # Progress bar - current_idx IS the number of completed concepts
    # (we're working on concept at index current_idx, so current_idx concepts are done)
    total = len(concepts)
    completed = current_idx  # Index 0 = working on 1st, 0 done. Index 1 = working on 2nd, 1 done.
    
    print("\n┌" + "─"*50 + "┐")
    print("│" + " 📊 LEARNING PROGRESS".ljust(50) + "│")
    print("├" + "─"*50 + "┤")
    
    # Concepts progress
    progress_bar = "█" * completed + "▒" * (total - completed)
    print(f"│  Concepts: [{progress_bar}] {completed}/{total}".ljust(51) + "│")
    
    # Current concept
    if current_idx < len(concepts):
        concept_title = concepts[current_idx].get("title", "Unknown")[:30]
        print(f"│  Current:  {concept_title}".ljust(51) + "│")
    
    # Understanding
    level_display = {
        "none": "⬜⬜⬜⬜",
        "partial": "🟨⬜⬜⬜",
        "mostly": "🟨🟨🟨⬜",
        "complete": "🟩🟩🟩🟩"
    }
    print(f"│  Understanding: {level_display.get(understanding, '⬜⬜⬜⬜')} ({understanding})".ljust(51) + "│")
    
    # Trajectory
    trajectory_emoji = {"improving": "📈", "stagnating": "📊", "regressing": "📉"}
    print(f"│  Trend: {trajectory_emoji.get(trajectory, '📊')} {trajectory}".ljust(51) + "│")
    
    # Exchange count
    print(f"│  Exchange: {exchange}/{MAX_EXCHANGES}".ljust(51) + "│")
    
    print("└" + "─"*50 + "┘")


def get_student_input() -> str:
    """Get input from the student."""
    print("\n👩‍🎓 Your response (or 'quit' to exit):")
    print(">>> ", end="")
    try:
        response = input().strip()
        return response
    except EOFError:
        return "quit"
    except KeyboardInterrupt:
        return "quit"


def open_simulation_if_changed(current_params: Dict[str, Any], previous_params: Dict[str, Any]) -> bool:
    """Open simulation in browser if parameters have changed."""
    if current_params != previous_params:
        url = build_simulation_url(current_params)
        print(f"\n🔗 Opening simulation with new parameters...")
        webbrowser.open(url)
        return True
    return False


def run_teaching_session():
    """Main teaching session loop."""
    print_header()
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    
    # Create session
    thread_id = f"session_{uuid.uuid4().hex[:8]}"
    print(f"📝 Session ID: {thread_id}")
    
    # Create initial state
    initial_state = create_initial_state(
        topic_description=TOPIC_DESCRIPTION,
        initial_params=INITIAL_PARAMS
    )
    
    print("\n📖 Topic: Time & Pendulums")
    print("   We'll explore how time period is measured and how it depends on length!")
    
    # Start session
    print("\n⏳ Initializing teaching session...")
    state = start_session(initial_state, thread_id)
    
    # Track previous params to detect changes
    previous_params = INITIAL_PARAMS.copy()
    
    # Main loop
    while True:
        # Show current state
        print_simulation_state(state.get("current_params", INITIAL_PARAMS))
        print_progress(state)
        
        # Show teacher's message
        teacher_msg = state.get("last_teacher_message", "")
        if teacher_msg:
            print_teacher_message(teacher_msg)
        
        # Check if session is complete
        if state.get("session_complete", False):
            print("\n" + "="*60)
            print("🎉 CONGRATULATIONS! You've completed the lesson!")
            print("="*60)
            
            # Show final summary
            concepts = state.get("concepts", [])
            print(f"\n📚 Concepts covered: {len(concepts)}")
            for c in concepts:
                print(f"   ✓ {c['title']}")
            
            param_history = state.get("parameter_history", [])
            effective_count = sum(1 for p in param_history if p.get("was_effective"))
            print(f"\n🧪 Parameter explorations: {len(param_history)}")
            print(f"   Effective changes: {effective_count}")
            
            print("\n👋 Thanks for learning with us!")
            break
        
        # Get student input
        response = get_student_input()
        
        if response.lower() in ["quit", "exit", "q"]:
            print("\n👋 Thanks for learning! See you next time!")
            break
        
        if not response:
            print("   (Please type a response)")
            continue
        
        # Continue session with response
        print("\n⏳ Processing your response...")
        state = continue_session(response, thread_id)
        
        # Check if params changed and open simulation
        current_params = state.get("current_params", INITIAL_PARAMS)
        if open_simulation_if_changed(current_params, previous_params):
            previous_params = current_params.copy()


def main():
    """Entry point."""
    run_teaching_session()


if __name__ == "__main__":
    main()
