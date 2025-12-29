# Metrics Logging System

## Overview
Local JSON-based metrics logging system for tracking LLM API calls, token usage, and performance.

## Features
- ✅ **Token Tracking**: Captures prompt tokens, completion tokens, and total tokens for every API call
- ✅ **Performance Metrics**: Logs API duration, parse time, and total processing time
- ✅ **Output Analysis**: Tracks number of concepts and relationships extracted
- ✅ **Success/Error Tracking**: Records both successful runs and failures with error messages
- ✅ **Human-Readable**: JSON format for easy inspection and debugging

## Files

### `metrics_logger.py`
Core module with functions:
- `log_metrics()` - Save metrics for a single run
- `load_all_metrics()` - Load all metrics files
- `get_summary_stats()` - Get aggregated statistics
- `get_recent_metrics(limit)` - Get N most recent runs
- `clear_old_metrics(days)` - Delete old metrics files

### `view_metrics.py`
Command-line tool to view metrics:

```bash
# Show summary statistics
python view_metrics.py

# Show 10 most recent runs
python view_metrics.py --recent 10

# Show all runs in a table
python view_metrics.py --all

# Show detailed JSON for run #5
python view_metrics.py --detail 5
```

### `metrics_logs/`
Directory containing JSON files (auto-created):
- `run_YYYYMMDD_HHMMSS_ffffff.json` - One file per API call
- Each file contains complete metrics for that run

## Metrics Data Structure

Each metrics file contains:

```json
{
  "timestamp": "2025-11-16T05:51:03.123456",
  "input": {
    "description_preview": "First 200 chars of description...",
    "description_length": 1234,
    "word_count": 180,
    "educational_level": "high school"
  },
  "tokens": {
    "prompt_tokens": 450,
    "completion_tokens": 320,
    "total_tokens": 770
  },
  "timing": {
    "api_duration_seconds": 1.234,
    "parse_duration_seconds": 0.012,
    "total_duration_seconds": 1.456
  },
  "output": {
    "concepts_count": 6,
    "relationships_count": 8,
    "concepts": [...],
    "relationships": [...]
  },
  "status": {
    "success": true,
    "error": null
  }
}
```

## Usage Examples

### View Summary Stats
```bash
python view_metrics.py
```
Output:
```
📊 METRICS SUMMARY
==================

🔢 TOTAL RUNS: 25
   ✅ Successful: 24
   ❌ Failed: 1
   📈 Success Rate: 96.0%

🪙 TOKEN USAGE:
   Total Tokens Used: 18,450
   ├─ Prompt Tokens: 11,200
   └─ Completion Tokens: 7,250
   Average per Run: 738.0

⏱️  TIMING:
   Average API Duration: 1.234s
   Total API Time: 30.85s

📝 OUTPUT:
   Average Concepts per Run: 6.2
   Total Concepts Extracted: 155
```

### View Recent Runs
```bash
python view_metrics.py --recent 5
```

### Clean Up Old Metrics
```python
from metrics_logger import clear_old_metrics

# Delete metrics older than 30 days
clear_old_metrics(days=30)
```

## Integration

The metrics system is automatically integrated into `timeline_mapper.py`. Every call to `extract_concepts_from_full_description()` logs metrics.

No configuration needed - it works out of the box!

## Storage Location

All metrics are saved to: `metrics_logs/run_*.json`

This directory is in `.gitignore` to prevent committing sensitive data.

## Benefits Over LangSmith

✅ Works perfectly with Google Gemini API (no integration issues)
✅ Complete token tracking (prompt, completion, total)
✅ Offline access - no need for internet to view metrics
✅ Human-readable JSON format
✅ Easy to export and analyze
✅ No API key or external service required
✅ Fast and lightweight
