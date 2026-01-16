"""
Quiz Evaluation Rules Engine

This module provides rule-based evaluation for quiz submissions.
Evaluates student-submitted parameters against predefined success criteria.
"""

from typing import Dict, Any, Tuple


def evaluate_condition(value: float, operator: str, threshold: float) -> bool:
    """
    Evaluate a single condition against a threshold.
    
    Args:
        value: The actual parameter value
        operator: Comparison operator (>=, <=, ==, >, <, !=)
        threshold: The threshold value to compare against
        
    Returns:
        bool: True if condition is satisfied, False otherwise
    """
    operators = {
        ">=": lambda v, t: v >= t,
        "<=": lambda v, t: v <= t,
        "==": lambda v, t: abs(v - t) < 0.01,  # Floating point comparison with tolerance
        ">": lambda v, t: v > t,
        "<": lambda v, t: v < t,
        "!=": lambda v, t: abs(v - t) >= 0.01
    }
    
    if operator not in operators:
        raise ValueError(f"Unsupported operator: {operator}")
    
    return operators[operator](value, threshold)


def check_conditions_list(
    submitted_params: Dict[str, Any],
    conditions: list
) -> bool:
    """
    Check if ALL conditions in a list are satisfied (AND logic).
    
    Args:
        submitted_params: Dictionary of parameter names to values from student
        conditions: List of condition dicts, e.g., [{"parameter": "time_period", "operator": ">=", "value": 2.0}]
        
    Returns:
        bool: True if ALL conditions are satisfied, False otherwise
    """
    for condition in conditions:
        param_name = condition.get("parameter")
        operator = condition.get("operator")
        threshold = condition.get("value")
        
        if param_name not in submitted_params:
            return False
        
        param_value = submitted_params[param_name]
        
        try:
            if not evaluate_condition(float(param_value), operator, float(threshold)):
                return False
        except (ValueError, TypeError):
            return False
    
    return True


def check_thresholds(
    submitted_params: Dict[str, Any],
    thresholds: Dict[str, Any],
    conditions: list
) -> bool:
    """
    Check if submission meets threshold requirements.
    Uses the thresholds dict along with operators from conditions.
    
    Args:
        submitted_params: Parameter values from student
        thresholds: Dict like {"time_period": 2.0} for perfect thresholds
        conditions: Original conditions list to get operators
        
    Returns:
        bool: True if thresholds are met
    """
    if not thresholds:
        return False
    
    # Build operator mapping from conditions
    operators = {}
    for cond in conditions:
        operators[cond["parameter"]] = cond["operator"]
    
    for param_name, threshold_value in thresholds.items():
        if param_name not in submitted_params:
            return False
        
        param_value = submitted_params[param_name]
        # Get operator from conditions, default to ">=" for perfect thresholds
        operator = operators.get(param_name, ">=")
        
        # Handle min/max thresholds (e.g., rotation_angle_min, rotation_angle_max)
        if param_name.endswith("_min"):
            base_param = param_name.replace("_min", "")
            if base_param not in submitted_params:
                return False
            if float(submitted_params[base_param]) < float(threshold_value):
                return False
        elif param_name.endswith("_max"):
            base_param = param_name.replace("_max", "")
            if base_param not in submitted_params:
                return False
            if float(submitted_params[base_param]) > float(threshold_value):
                return False
        else:
            try:
                if not evaluate_condition(float(param_value), operator, float(threshold_value)):
                    return False
            except (ValueError, TypeError):
                return False
    
    return True


def evaluate_quiz_submission(
    submitted_params: Dict[str, Any],
    success_rule: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Evaluate quiz submission against success criteria.
    
    Args:
        submitted_params: Dictionary of parameter names to values submitted by student
        success_rule: Success rule dictionary with conditions, scoring, and thresholds
        
    Returns:
        Tuple of (score, status) where:
            score: 1.0 (perfect), 0.5 (partial), or 0.0 (wrong)
            status: "RIGHT", "PARTIALLY_RIGHT", or "WRONG"
            
    Example:
        submitted_params = {"length": 10, "number_of_oscillations": 5}
        success_rule = {
            "conditions": [
                {"parameter": "time_period", "operator": ">=", "value": 2.0}
            ],
            "scoring": {"perfect": 1.0, "partial": 0.6, "wrong": 0.3},
            "thresholds": {
                "perfect": {"time_period": 2.0},
                "partial": {"time_period": 1.5}
            }
        }
        score, status = evaluate_quiz_submission(submitted_params, success_rule)
    """
    if not success_rule:
        raise ValueError("Invalid success_rule: empty or None")
    
    conditions = success_rule.get("conditions", [])
    scoring = success_rule.get("scoring", {})
    thresholds = success_rule.get("thresholds", {})
    
    # Debug output
    print(f"   Conditions: {conditions}")
    print(f"   Thresholds: {thresholds}")
    
    # Strategy 1: If thresholds are defined, use them for tiered scoring
    if thresholds:
        # Check perfect threshold first
        if "perfect" in thresholds:
            perfect_thresholds = thresholds["perfect"]
            if check_thresholds(submitted_params, perfect_thresholds, conditions):
                return scoring.get("perfect", 1.0), "RIGHT"
        
        # Check partial threshold
        if "partial" in thresholds:
            partial_thresholds = thresholds["partial"]
            if check_thresholds(submitted_params, partial_thresholds, conditions):
                return scoring.get("partial", 0.5), "PARTIALLY_RIGHT"
    
    # Strategy 2: Check all conditions (AND logic) - if all pass, it's perfect
    if conditions:
        if check_conditions_list(submitted_params, conditions):
            return scoring.get("perfect", 1.0), "RIGHT"
    
    # Wrong answer
    return scoring.get("wrong", 0.0), "WRONG"


def get_hint_for_attempt(hints: dict, attempt_number: int) -> str:
    """
    Get appropriate hint based on attempt number.
    
    Args:
        hints: Dictionary of hints with keys like "attempt_1", "attempt_2", "attempt_3"
        attempt_number: Current attempt number (1-based)
        
    Returns:
        str: Appropriate hint for this attempt, or last available hint
    """
    if not hints:
        return ""
    
    # Try to get hint for this specific attempt
    hint_key = f"attempt_{attempt_number}"
    if hint_key in hints:
        return hints[hint_key]
    
    # Fall back to highest available attempt hint
    for i in range(attempt_number, 0, -1):
        key = f"attempt_{i}"
        if key in hints:
            return hints[key]
    
    # Last resort: return first available hint
    return next(iter(hints.values()), "")


def should_allow_retry(attempt_number: int, max_attempts: int = 3) -> bool:
    """
    Determine if student should be allowed to retry.
    
    Args:
        attempt_number: Current attempt number (1-based)
        max_attempts: Maximum attempts allowed (default: 3)
        
    Returns:
        bool: True if retry allowed, False otherwise
    """
    return attempt_number < max_attempts


def calculate_quiz_progress(
    quiz_scores: Dict[str, float],
    total_questions: int
) -> Dict[str, Any]:
    """
    Calculate overall quiz progress and statistics.
    
    Args:
        quiz_scores: Dictionary mapping question_id to score (0.0-1.0)
        total_questions: Total number of questions in quiz
        
    Returns:
        Dictionary with progress statistics:
            - questions_completed: Number of questions answered
            - questions_remaining: Number of questions left
            - average_score: Average score across completed questions
            - perfect_count: Number of perfect scores (1.0)
            - partial_count: Number of partial scores (0.5)
            - wrong_count: Number of wrong scores (0.0)
    """
    completed = len(quiz_scores)
    remaining = total_questions - completed
    
    if completed == 0:
        avg_score = 0.0
    else:
        avg_score = sum(quiz_scores.values()) / completed
    
    # Count score types
    perfect_count = sum(1 for score in quiz_scores.values() if score >= 0.99)
    partial_count = sum(1 for score in quiz_scores.values() if 0.4 < score < 0.99)
    wrong_count = sum(1 for score in quiz_scores.values() if score <= 0.4)
    
    return {
        "questions_completed": completed,
        "questions_remaining": remaining,
        "average_score": round(avg_score, 2),
        "perfect_count": perfect_count,
        "partial_count": partial_count,
        "wrong_count": wrong_count,
        "total_questions": total_questions
    }
