"""
Quiz Evaluation Rules Engine

This module provides rule-based evaluation for quiz submissions.
Evaluates student-submitted parameters against predefined success criteria.
Supports optimization goals (minimize/maximize) for dynamic evaluation.
"""

from typing import Dict, Any, Tuple, Optional


def parse_parameter_range(range_str: str) -> Tuple[float, float]:
    """
    Parse parameter range from string like "1-10 units" or "5-50 count".
    
    Args:
        range_str: String like "1-10 units"
        
    Returns:
        Tuple of (min_value, max_value)
    """
    try:
        # Extract numbers from string like "1-10 units"
        parts = range_str.split()
        range_part = parts[0]  # "1-10"
        min_val, max_val = range_part.split("-")
        return float(min_val), float(max_val)
    except:
        # Default range if parsing fails
        return 1.0, 10.0


def evaluate_optimization(
    value: float,
    objective: str,
    min_val: float,
    max_val: float,
    tolerance_perfect: float = 0.1,
    tolerance_partial: float = 0.3
) -> Tuple[float, str]:
    """
    Evaluate how well a value meets an optimization objective.
    
    Args:
        value: The submitted value
        objective: "minimize" or "maximize"
        min_val: Minimum possible value for this parameter
        max_val: Maximum possible value for this parameter
        tolerance_perfect: Fraction of range for perfect score (default 0.1 = 10%)
        tolerance_partial: Fraction of range for partial score (default 0.3 = 30%)
        
    Returns:
        Tuple of (score, explanation)
        
    Example:
        For length range 1-10 with objective="minimize":
        - value=1: score=1.0 (at optimal)
        - value=1.5: score=1.0 (within 10% tolerance)
        - value=3: score=0.5 (within 30% tolerance)
        - value=6: score=0.0 (too far from optimal)
    """
    range_span = max_val - min_val
    
    if objective == "minimize":
        optimal = min_val
        distance = value - optimal
    elif objective == "maximize":
        optimal = max_val
        distance = optimal - value
    else:
        return 0.0, f"Unknown objective: {objective}"
    
    # Normalize distance as fraction of range
    normalized_distance = distance / range_span
    
    if normalized_distance <= tolerance_perfect:
        return 1.0, "optimal"
    elif normalized_distance <= tolerance_partial:
        return 0.5, "close"
    else:
        return 0.0, "far"


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
    success_rule: Dict[str, Any],
    parameter_ranges: Optional[Dict[str, str]] = None
) -> Tuple[float, str]:
    """
    Evaluate quiz submission against success criteria.
    Supports both fixed thresholds and optimization goals (minimize/maximize).
    
    Args:
        submitted_params: Dictionary of parameter names to values submitted by student
        success_rule: Success rule dictionary with:
            - conditions: Required conditions that must be met
            - optimization_target (optional): {"parameter": "length", "objective": "minimize"}
            - scoring: Score values for perfect/partial/wrong
            - thresholds (optional): Fixed thresholds for backward compatibility
        parameter_ranges: Optional dict of parameter ranges from simulation config
        
    Returns:
        Tuple of (score, status) where:
            score: 1.0 (perfect), 0.5 (partial), or 0.0 (wrong)
            status: "RIGHT", "PARTIALLY_RIGHT", or "WRONG"
    """
    if not success_rule:
        raise ValueError("Invalid success_rule: empty or None")
    
    conditions = success_rule.get("conditions", [])
    scoring = success_rule.get("scoring", {})
    optimization_target = success_rule.get("optimization_target")
    thresholds = success_rule.get("thresholds", {})
    
    # Debug output
    print(f"   Conditions: {conditions}")
    print(f"   Optimization: {optimization_target}")
    print(f"   Thresholds: {thresholds}")
    
    # STEP 1: Check required conditions (must all pass)
    if conditions and not check_conditions_list(submitted_params, conditions):
        return scoring.get("wrong", 0.0), "WRONG"
    
    # STEP 2: Evaluate optimization target (if specified)
    if optimization_target and parameter_ranges:
        param_name = optimization_target.get("parameter")
        objective = optimization_target.get("objective")  # "minimize" or "maximize"
        
        if param_name in submitted_params and param_name in parameter_ranges:
            value = float(submitted_params[param_name])
            range_str = parameter_ranges[param_name]
            min_val, max_val = parse_parameter_range(range_str)
            
            # Get tolerance from scoring if specified
            tolerance_config = success_rule.get("tolerances", {})
            tol_perfect = tolerance_config.get("perfect", 0.15)  # 15% of range
            tol_partial = tolerance_config.get("partial", 0.35)  # 35% of range
            
            opt_score, opt_reason = evaluate_optimization(
                value, objective, min_val, max_val,
                tolerance_perfect=tol_perfect,
                tolerance_partial=tol_partial
            )
            
            print(f"   Optimization result: score={opt_score}, reason={opt_reason}")
            
            if opt_score >= 1.0:
                return scoring.get("perfect", 1.0), "RIGHT"
            elif opt_score >= 0.5:
                return scoring.get("partial", 0.5), "PARTIALLY_RIGHT"
            else:
                return scoring.get("wrong", 0.0), "WRONG"
    
    # STEP 3: Fallback to threshold-based evaluation (backward compatibility)
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
    
    # STEP 4: If only conditions and all passed, it's perfect
    if conditions and not optimization_target and not thresholds:
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
