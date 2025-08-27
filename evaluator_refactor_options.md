"""
SUGGESTED REFACTORING FOR evaluator.py

Option 1: Remove Overlapping Metrics
- Remove Adaptability, Clarity, Error Handling from evaluator
- Focus on unique metrics: Pedagogical Flow + Qualitative Feedback
- Use session_metrics for quantitative analysis

Option 2: Specialized Educational Evaluator  
- Keep all current metrics but mark them as "Educational Quality" focus
- Add educational-specific metrics like:
  - Scaffolding Effectiveness
  - Conceptual Progression Quality  
  - Misconception Handling
  - Learning Objective Achievement
- Position as complement to session_metrics

Option 3: Merge Into session_metrics
- Add Pedagogical Flow to LLMAnalyzedMetrics
- Move qualitative feedback to session_metrics
- Deprecate evaluator.py
"""
