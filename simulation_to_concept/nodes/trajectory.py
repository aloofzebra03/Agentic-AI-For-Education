"""
Trajectory Analyzer Node
========================
Analyzes the student's learning trajectory to detect patterns.

This node looks at the history of understanding levels to determine:
1. Is the student improving? (none → partial → mostly)
2. Are they stagnating? (partial → partial → partial)
3. Are they regressing? (partial → none)

This information is crucial for the strategy selector to adapt teaching.
"""

from typing import Dict, Any, List


def calculate_trajectory_status(trajectory: List[str]) -> str:
    """
    Analyze understanding trajectory to determine learning status.
    
    Args:
        trajectory: List of understanding levels over time
        
    Returns:
        "improving" | "stagnating" | "regressing"
        
    Examples:
        ["none", "partial", "mostly"] → "improving"
        ["partial", "partial", "partial"] → "stagnating"
        ["partial", "none"] → "regressing"
    """
    if len(trajectory) < 2:
        return "improving"  # Default - benefit of the doubt
    
    # Map levels to numbers for comparison
    level_scores = {
        "none": 0,
        "partial": 1,
        "mostly": 2,
        "complete": 3
    }
    
    # Look at last 3 entries (or all if fewer)
    recent = trajectory[-3:] if len(trajectory) >= 3 else trajectory
    scores = [level_scores.get(level, 1) for level in recent]
    
    # Calculate trend
    if len(scores) >= 2:
        # Compare first half average to second half average
        mid = len(scores) // 2
        first_half = sum(scores[:mid]) / max(mid, 1)
        second_half = sum(scores[mid:]) / max(len(scores) - mid, 1)
        
        diff = second_half - first_half
        
        if diff > 0.3:
            return "improving"
        elif diff < -0.3:
            return "regressing"
        else:
            # Check for pure stagnation (same level repeated)
            if len(set(recent)) == 1 and len(recent) >= 2:
                return "stagnating"
            # Check if last two are same but different from before
            if len(scores) >= 3 and scores[-1] == scores[-2] and scores[-1] != scores[0]:
                return "stagnating"
            return "stagnating" if scores[-1] <= scores[-2] else "improving"
    
    return "improving"


def trajectory_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the learning trajectory to detect patterns.
    
    Input State:
        - understanding_trajectory: History of levels
        - understanding_level: Current level
        - exchange_count: How many exchanges
        - parameter_history: What we've tried
        
    Output State:
        - trajectory_status: improving/stagnating/regressing
        - concept_complete: True if understanding is complete
        
    The trajectory status guides the strategy selector:
        - "improving" → Keep going, current approach is working
        - "stagnating" → Need to change approach
        - "regressing" → Something's wrong, maybe simplify
    """
    print("\n" + "="*60)
    print("📈 TRAJECTORY ANALYZER: Detecting learning patterns")
    print("="*60)
    
    trajectory = state.get("understanding_trajectory", [])
    current_level = state.get("understanding_level", "none")
    exchange_count = state.get("exchange_count", 0)
    
    print(f"   Trajectory: {trajectory}")
    print(f"   Current level: {current_level}")
    print(f"   Exchange count: {exchange_count}")
    
    # Calculate trajectory status
    status = calculate_trajectory_status(trajectory)
    
    # Check for concept completion
    # ONLY "complete" counts as understood
    # BUT: Safety valve - if they got "mostly" twice, they understand (just not explaining)
    concept_complete = False
    
    if current_level == "complete":
        concept_complete = True
    elif current_level == "mostly":
        # Safety valve: 2 "mostly" in a row = advance (they clearly get it)
        if len(trajectory) >= 2 and trajectory[-2] == "mostly":
            concept_complete = True
            print("   🔓 Safety valve: 2x 'mostly' - advancing (student understands but not explaining)")
    
    # Additional analysis
    if len(trajectory) >= 3:
        # Detect oscillation (going back and forth)
        last_three = trajectory[-3:]
        level_scores = {"none": 0, "partial": 1, "mostly": 2, "complete": 3}
        scores = [level_scores.get(l, 1) for l in last_three]
        
        if scores[0] > scores[1] < scores[2] or scores[0] < scores[1] > scores[2]:
            print("   ⚠️ Detected oscillation - student seems uncertain")
            status = "stagnating"  # Treat oscillation as stagnation
    
    # Log insights
    status_emoji = {
        "improving": "📈",
        "stagnating": "📊",
        "regressing": "📉"
    }
    
    print(f"\n   {status_emoji.get(status, '📊')} Trajectory Status: {status.upper()}")
    print(f"   ✅ Concept Complete: {concept_complete}")
    
    # Provide additional context for strategy selector
    insights = []
    if status == "stagnating" and exchange_count >= 3:
        insights.append("Student has been stuck for multiple exchanges")
    if status == "regressing":
        insights.append("Student understanding decreased - may need simpler approach")
    if concept_complete:
        insights.append("Ready to move to next concept")
    
    if insights:
        print(f"   💡 Insights: {'; '.join(insights)}")
    
    return {
        "trajectory_status": status,
        "concept_complete": concept_complete,
        "_trajectory_insights": insights
    }
