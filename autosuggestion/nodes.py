"""Node functions for autosuggestion flow management.

This module contains graph nodes that manage the autosuggestion flow:
- Autosuggestion Manager: Routes clicked autosuggestions to handlers
- Pause Handler: Clears autosuggestions before graph interrupt
"""

from typing import Dict

from .handlers import handle_hint, handle_explain_simpler, handle_example


def autosuggestion_manager_node(state) -> Dict:
    """Manager node that handles clicked autosuggestions.
    
    This node runs ONLY when user clicks an autosuggestion button.
    It routes special handling suggestions to appropriate handler functions
    and sets flags for graph routing decisions.
    
    CRITICAL: Sets handler_triggered flag which graph uses to decide
    whether to interrupt and show handler output to user.
    
    Args:
        state: AgentState dictionary
        
    Returns:
        Partial state update with handler_triggered and clicked_autosuggestion flags
    """
    print("=" * 80)
    print("🎯 AUTOSUGGESTION MANAGER NODE - ENTRY")
    print("=" * 80)
    
    last_user_msg = state.get("last_user_msg", "")
    special_handling = state.get("special_handling_autosuggestion", "")
    
    # Check if user clicked the SPECIAL HANDLING suggestion
    if last_user_msg == special_handling and special_handling:
        print(f"🔧 SPECIAL HANDLING TRIGGERED: {last_user_msg}")
        
        # Route to appropriate handler based on suggestion text
        if last_user_msg == "Can you give me a hint?":
            handler_result = handle_hint(state)
        elif last_user_msg == "Can you explain that simpler?":
            handler_result = handle_explain_simpler(state)
        elif last_user_msg == "Give me an example":
            handler_result = handle_example(state)
        else:
            handler_result = {}
        
        # Update state with handler result (partial update)
        state.update(handler_result)
        
        # Mark that we need to show the handler output to user (interrupt)
        state["handler_triggered"] = True
    
    else:
        print(f"📝 NORMAL FLOW AUTOSUGGESTION: {last_user_msg}")
        print("   (Positive or negative suggestion - flow continues without pause)")
        state["handler_triggered"] = False
    
    # Reset click flag for next interaction
    state["clicked_autosuggestion"] = False
    
    print(f"🔄 PRESERVING current_state: {state.get('current_state', 'UNKNOWN')}")
    print(f"📤 AUTOSUGGESTIONS ALREADY SET: {state.get('autosuggestions', [])}")
    print(f"⏸️ HANDLER TRIGGERED: {state.get('handler_triggered', False)}")
    print("=" * 80)
    
    # CRITICAL: Preserve current_state - do NOT modify pedagogical routing
    return state


def pause_for_handler(state) -> Dict:
    """Pass-through node that clears autosuggestions before pause.
    
    Allows graph to interrupt after handler execution to show the handler
    output to the user. Clears stale autosuggestions so user sees only
    the handler output. Fresh autosuggestions will be generated when
    flow resumes.
    
    Args:
        state: AgentState dictionary
        
    Returns:
        Partial state update with cleared autosuggestion fields
    """
    return {
        "handler_triggered": False,  # Reset flag
        "autosuggestions": [],  # Clear final autosuggestions
        "positive_autosuggestion": "",  # Clear positive selection
        "negative_autosuggestion": "",  # Clear negative selection
        "special_handling_autosuggestion": "",  # Clear special handling selection
        "dynamic_autosuggestion": "",  # Clear dynamic suggestion
    }
