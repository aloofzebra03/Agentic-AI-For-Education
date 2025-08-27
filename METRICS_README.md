# Session Metrics System

This document describes the comprehensive session metrics system that computes and uploads educational session metrics to Langfuse.

## Overview

The session metrics system automatically computes 11 key metrics at the end of each educational session and uploads them to Langfuse for tracking and analysis.

### Computed Metrics

1. **Concepts Covered** - List of concepts taught during the session
2. **Number of Concepts Covered** - Total count of concepts touched
3. **Quiz Score** - Score from formative assessments (0-100%)
4. **Clarity & Conciseness Score** - LLM-evaluated clarity rating (1-5)
5. **Error Handling Count** - Number of corrections/re-prompts
6. **User Type** - Classification as "Dull", "Medium", or "High" learner
7. **User Interest Rating** - Engagement score (1-5) based on interaction patterns
8. **User Engagement Rating** - Activity score (1-5) using response patterns
9. **Average Response Time** - Estimated seconds per interaction
10. **Adaptability** - Whether the agent dynamically adjusted to user performance
11. **Enjoyment Probability** - Likelihood (0-1) that the user enjoyed and benefited

## Usage

### Automatic Integration

The metrics system is automatically integrated into:

1. **Test Runner** (`run_test.py`) - Automatically computes metrics after each test session
2. **Streamlit App** (`app_graph.py`) - Computes metrics when a session ends
3. **Evaluator** (`evaluator.py`) - Optional metrics computation during evaluation

### Manual Computation

You can compute metrics for any existing session using the standalone script:

```bash
# Compute metrics from an evaluation report
python compute_session_metrics.py reports/evaluation_session_id.json

# Compute metrics with custom session ID
python compute_session_metrics.py reports/evaluation_session_id.json --session_id custom_session

# Compute without uploading to Langfuse
python compute_session_metrics.py data.json --no-upload

# Save metrics to a file
python compute_session_metrics.py data.json --output metrics.json
```

### Programmatic Usage

```python
from tester_agent.session_metrics import compute_and_upload_session_metrics

# Compute and upload metrics
metrics = compute_and_upload_session_metrics(
    session_id="my_session_123",
    history=conversation_history,
    session_state=agent_final_state,
    persona_name="Eager Student"
)

print(f"User type: {metrics.user_type}")
print(f"Quiz score: {metrics.quiz_score}%")
print(f"Engagement: {metrics.user_engagement_rating}/5")
```

### Compute Only (No Upload)

```python
from tester_agent.session_metrics import MetricsComputer

computer = MetricsComputer()
metrics = computer.compute_metrics(
    session_id="my_session",
    history=history,
    session_state=state,
    persona_name="Student"
)

# Manually upload later if needed
computer.upload_to_langfuse(metrics)
```

## Data Format Requirements

The system expects session data in one of these formats:

### Format 1: Complete Session Data
```json
{
  "history": [
    {"role": "user", "content": "Hi there!"},
    {"role": "assistant", "content": "Hello! Let's learn about pendulums."}
  ],
  "session_state": {
    "current_state": "END",
    "quiz_results": {"correct": 4, "total": 5},
    "concepts_taught": ["simple pendulum", "oscillation"]
  }
}
```

### Format 2: History Only
```json
{
  "history": [
    {"role": "user", "content": "Hi there!"},
    {"role": "assistant", "content": "Hello! Let's learn about pendulums."}
  ]
}
```

### Format 3: Evaluation Report Format
```json
{
  "persona": {"name": "Eager Student", "description": "..."},
  "evaluation": {"adaptability": 4, "clarity": 5},
  "history": [...]
}
```

### Format 4: Raw History Array
```json
[
  {"role": "user", "content": "Hi there!"},
  {"role": "assistant", "content": "Hello! Let's learn about pendulums."}
]
```

## Langfuse Integration

### Session-Level Metrics

Metrics are uploaded to Langfuse as:

1. **Session Metadata** - Complete metrics object stored in session metadata
2. **Individual Scores** - Each numeric metric uploaded as a separate score for easier querying

### Viewing in Langfuse

1. Navigate to your Langfuse dashboard
2. Go to "Sessions" to see session-level data
3. Click on a session to view detailed metrics
4. Use "Scores" section to analyze individual metrics across sessions

### Querying Metrics

You can query metrics using the Langfuse API:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Get all sessions with high engagement
sessions = langfuse.get_sessions(
    metadata_filter={"session_metrics.user_engagement_rating": {"gte": 4.0}}
)

# Get average quiz scores
scores = langfuse.get_scores(name="quiz_score")
avg_quiz_score = sum(s.value for s in scores) / len(scores)
```

## Customization

### Adding New Metrics

To add a new metric:

1. Add the field to `SessionMetrics` model in `session_metrics.py`
2. Implement computation logic in `MetricsComputer`
3. Update the main `compute_metrics` method

### Modifying Computation Logic

Key methods to customize:

- `_classify_user_type()` - User classification logic
- `_compute_clarity_score()` - LLM evaluation prompts
- `_compute_engagement_rating()` - Engagement calculation
- `_extract_concepts_covered()` - Concept extraction logic

### Custom Upload Logic

```python
class CustomMetricsComputer(MetricsComputer):
    def upload_to_langfuse(self, metrics: SessionMetrics) -> bool:
        # Custom upload logic
        # Add your own metadata, tags, or processing
        return super().upload_to_langfuse(metrics)
```

## Testing

Test the metrics system:

```bash
# Run the test script
python test_metrics.py

# Test with existing reports
python compute_session_metrics.py reports/evaluation_*.json --no-upload
```

## Troubleshooting

### Common Issues

1. **Import Errors** - Ensure all dependencies are installed: `pip install -r requirements.txt`
2. **Langfuse Upload Fails** - Check API keys in `.env` file
3. **No History Found** - Verify data format matches expected structure
4. **LLM Evaluation Fails** - Check Google API key for Gemini model

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run metrics computation
metrics = compute_and_upload_session_metrics(...)
```

### Validation

The system includes built-in validation using Pydantic models. Invalid data will raise clear error messages.

## Best Practices

1. **Always run metrics computation** after session completion
2. **Include persona information** when available for better classification
3. **Monitor Langfuse regularly** to track learning effectiveness
4. **Use session tags** to organize different experiment types
5. **Backup metrics locally** using the download features in the UI

## Dependencies

- `pydantic` - Data validation and serialization
- `langfuse` - Metrics upload and tracking
- `langchain-google-genai` - LLM evaluation
- `python-dotenv` - Environment variable management

## File Structure

```
tester_agent/
├── session_metrics.py     # Core metrics computation and upload
├── evaluator.py           # Enhanced evaluator with metrics
└── personas.py           # Student personas

compute_session_metrics.py  # Standalone metrics computation script
test_metrics.py            # Testing and validation script
run_test.py               # Updated test runner with metrics
app_graph.py              # Updated Streamlit app with metrics
```
