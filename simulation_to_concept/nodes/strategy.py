"""
Strategy Selector Node
======================
Decides the next teaching strategy based on all available information.

This node is the "brain" that decides:
1. What teaching strategy to use next
2. What mode the teacher should be in
3. Whether to scaffold (break down the concept)
4. Whether to advance to the next concept

It uses:
- Understanding level and trajectory
- Exchange count and limits
- Parameter history effectiveness
- Detected misconceptions
"""

from typing import Dict, Any, List

from simulation_to_concept.config import MAX_EXCHANGES, SCAFFOLD_TRIGGER, PARAMETER_INFO


def analyze_param_effectiveness(param_history: List[dict]) -> dict:
    """
    Analyze which parameter changes have been effective.
    
    Returns:
        {
            "effective_params": ["length", ...],
            "ineffective_params": ["mass", ...],
            "untried_params": ["gravity", ...]
        }
    """
    # Get all params from current simulation config instead of hardcoding
    all_params = set(PARAMETER_INFO.keys())
    tried_params = set()
    effective = set()
    ineffective = set()
    
    for change in param_history:
        param = change.get("parameter")
        if param:
            tried_params.add(param)
            if change.get("was_effective"):
                effective.add(param)
            else:
                ineffective.add(param)
    
    return {
        "effective_params": list(effective),
        "ineffective_params": list(ineffective),
        "untried_params": list(all_params - tried_params)
    }


def strategy_selector_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Select the next teaching strategy based on current state.
    
    Input State:
        - understanding_level: Current level
        - trajectory_status: improving/stagnating/regressing
        - exchange_count: How many exchanges this concept
        - parameter_history: What we've tried
        - concept_complete: Is current concept understood
        - concepts: All concepts
        - current_concept_index: Current position
        
    Output State:
        - strategy: continue/try_different/scaffold/give_hint/summarize_advance
        - teacher_mode: encouraging/challenging/simplifying
        - should_scaffold: Boolean
        - current_concept_index: Updated if advancing
        - concept_complete: Reset if advancing
        
    Strategy Decision Matrix:
    
    | Trajectory  | Understanding | Exchange | → Strategy          |
    |-------------|---------------|----------|---------------------|
    | improving   | complete      | any      | summarize_advance   |
    | improving   | mostly        | any      | continue (challenge)|
    | improving   | partial       | < 3      | continue            |
    | improving   | partial       | >= 3     | try_different       |
    | stagnating  | any           | < 3      | try_different       |
    | stagnating  | any           | >= 3     | scaffold            |
    | stagnating  | any           | >= 5     | give_hint           |
    | regressing  | any           | < 3      | scaffold            |
    | regressing  | any           | >= 3     | give_hint           |
    | any         | any           | >= MAX   | summarize_advance   |
    """
    print("\n" + "="*60)
    print("🧠 STRATEGY SELECTOR: Choosing next approach")
    print("="*60)
    
    # Gather inputs
    understanding = state.get("understanding_level", "none")
    trajectory = state.get("trajectory_status", "improving")
    exchange_count = state.get("exchange_count", 0)
    concept_complete = state.get("concept_complete", False)
    param_history = state.get("parameter_history", [])
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    
    print(f"   Understanding: {understanding}")
    print(f"   Trajectory: {trajectory}")
    print(f"   Exchange count: {exchange_count}")
    print(f"   Concept complete: {concept_complete}")
    
    # Analyze parameter effectiveness
    param_analysis = analyze_param_effectiveness(param_history)
    print(f"   Effective params: {param_analysis['effective_params']}")
    print(f"   Untried params: {param_analysis['untried_params']}")
    
    # Initialize outputs
    strategy = "continue"
    teacher_mode = "encouraging"
    should_scaffold = False
    advance_concept = False
    
    # ═══════════════════════════════════════════════════════════════════════
    # DECISION LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    
    # Rule 1: Max exchanges reached - graceful exit
    if exchange_count >= MAX_EXCHANGES:
        print(f"   ⚠️ Max exchanges ({MAX_EXCHANGES}) reached")
        strategy = "summarize_advance"
        teacher_mode = "encouraging"
        advance_concept = True
    
    # Rule 2: Concept is complete - celebrate and advance
    elif concept_complete or understanding == "complete":
        print("   ✅ Concept understood!")
        strategy = "summarize_advance"
        teacher_mode = "encouraging"
        advance_concept = True
    
    # Rule 3: Mostly understood - can push a bit
    elif understanding == "mostly":
        if trajectory == "improving":
            strategy = "continue"
            teacher_mode = "challenging"  # Push them to complete understanding
        else:
            strategy = "summarize_advance"  # Good enough, move on
            advance_concept = True
    
    # Rule 4: Handle by trajectory
    elif trajectory == "improving":
        if exchange_count < 3:
            strategy = "continue"
            teacher_mode = "encouraging"
        else:
            strategy = "try_different"
            teacher_mode = "encouraging"
    
    elif trajectory == "stagnating":
        if exchange_count < SCAFFOLD_TRIGGER:
            strategy = "try_different"
            teacher_mode = "encouraging"
        elif exchange_count < 5:
            strategy = "scaffold"
            teacher_mode = "simplifying"
            should_scaffold = True
        else:
            strategy = "give_hint"
            teacher_mode = "simplifying"
    
    elif trajectory == "regressing":
        if exchange_count < SCAFFOLD_TRIGGER:
            strategy = "scaffold"
            teacher_mode = "simplifying"
            should_scaffold = True
        else:
            strategy = "give_hint"
            teacher_mode = "simplifying"
    
    # ═══════════════════════════════════════════════════════════════════════
    # APPLY DECISIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    updates = {
        "strategy": strategy,
        "teacher_mode": teacher_mode,
        "should_scaffold": should_scaffold
    }
    
    # Handle concept advancement
    if advance_concept:
        new_idx = current_idx + 1
        updates["current_concept_index"] = new_idx
        updates["concept_complete"] = False
        updates["understanding_level"] = "none"
        updates["understanding_trajectory"] = []
        updates["exchange_count"] = 0
        
        if new_idx >= len(concepts):
            # Don't set session_complete here - let quiz mode handle it
            # Session only completes after quiz is done
            print("   ✅ All concepts complete! Ready for quiz mode.")
        else:
            print(f"   ➡️ Advancing to concept {new_idx + 1}: {concepts[new_idx]['title']}")
    
    # Log decision
    print(f"\n   📋 Decision:")
    print(f"      Strategy: {strategy}")
    print(f"      Mode: {teacher_mode}")
    print(f"      Scaffold: {should_scaffold}")
    print(f"      Advance: {advance_concept}")
    
    return updates
