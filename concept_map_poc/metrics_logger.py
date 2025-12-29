"""
Metrics Logger Module
=====================
Local metrics logging system for tracking LLM API calls, token usage, and performance.

Saves each run to JSON files in metrics_logs/ directory for easy inspection and analysis.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Directory for storing metrics
METRICS_DIR = Path(__file__).parent / "metrics_logs"


def ensure_metrics_dir():
    """Create metrics directory if it doesn't exist"""
    METRICS_DIR.mkdir(exist_ok=True)


def log_metrics(
    description: str,
    educational_level: str,
    token_usage: Dict[int, int],
    timing_metrics: Dict[str, float],
    concepts: List[Dict],
    relationships: List[Dict],
    success: bool = True,
    error: Optional[str] = None
) -> str:
    """
    Log metrics for a single LLM API call to a JSON file.
    
    Args:
        description: The input description (will be truncated for storage)
        educational_level: Educational level used
        token_usage: Dict with 'prompt_tokens', 'completion_tokens', 'total_tokens'
        timing_metrics: Dict with 'api_duration', 'parse_duration', 'total_duration'
        concepts: List of extracted concepts
        relationships: List of extracted relationships
        success: Whether the extraction was successful
        error: Error message if failed
        
    Returns:
        Path to the saved metrics file
    """
    ensure_metrics_dir()
    
    timestamp = datetime.now()
    filename = f"run_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
    filepath = METRICS_DIR / filename
    
    metrics_data = {
        "timestamp": timestamp.isoformat(),
        "input": {
            "description_preview": description[:200] + "..." if len(description) > 200 else description,
            "description_length": len(description),
            "word_count": len(description.split()),
            "educational_level": educational_level
        },
        "tokens": {
            "prompt_tokens": token_usage.get('prompt_tokens', 0),
            "completion_tokens": token_usage.get('completion_tokens', 0),
            "total_tokens": token_usage.get('total_tokens', 0)
        },
        "timing": {
            "api_duration_seconds": round(timing_metrics.get('api_duration', 0), 3),
            "parse_duration_seconds": round(timing_metrics.get('parse_duration', 0), 3),
            "total_duration_seconds": round(timing_metrics.get('total_duration', 0), 3)
        },
        "output": {
            "concepts_count": len(concepts),
            "relationships_count": len(relationships),
            "concepts": [
                {
                    "name": c.get('name'),
                    "type": c.get('type'),
                    "importance": c.get('importance'),
                    "importance_rank": c.get('importance_rank')
                }
                for c in concepts
            ],
            "relationships": [
                {
                    "from": r.get('from'),
                    "to": r.get('to'),
                    "relationship": r.get('relationship')
                }
                for r in relationships
            ]
        },
        "status": {
            "success": success,
            "error": error
        }
    }
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)
        logger.info(f"📊 Metrics saved to: {filepath.name}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to save metrics: {e}")
        return None


def load_all_metrics() -> List[Dict]:
    """
    Load all metrics files from the metrics_logs directory.
    
    Returns:
        List of all metrics data, sorted by timestamp (newest first)
    """
    ensure_metrics_dir()
    
    all_metrics = []
    
    for filepath in METRICS_DIR.glob("run_*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['filename'] = filepath.name
                all_metrics.append(data)
        except Exception as e:
            logger.warning(f"Failed to load {filepath.name}: {e}")
    
    # Sort by timestamp, newest first
    all_metrics.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return all_metrics


def get_summary_stats() -> Dict:
    """
    Get aggregated statistics across all logged metrics.
    
    Returns:
        Dict with summary statistics
    """
    all_metrics = load_all_metrics()
    
    if not all_metrics:
        return {
            "total_runs": 0,
            "message": "No metrics data available"
        }
    
    total_tokens = sum(m['tokens']['total_tokens'] for m in all_metrics)
    total_prompt_tokens = sum(m['tokens']['prompt_tokens'] for m in all_metrics)
    total_completion_tokens = sum(m['tokens']['completion_tokens'] for m in all_metrics)
    
    successful_runs = [m for m in all_metrics if m['status']['success']]
    failed_runs = [m for m in all_metrics if not m['status']['success']]
    
    avg_api_duration = sum(m['timing']['api_duration_seconds'] for m in all_metrics) / len(all_metrics)
    avg_concepts = sum(m['output']['concepts_count'] for m in all_metrics) / len(all_metrics)
    
    return {
        "total_runs": len(all_metrics),
        "successful_runs": len(successful_runs),
        "failed_runs": len(failed_runs),
        "success_rate": f"{(len(successful_runs) / len(all_metrics) * 100):.1f}%",
        "tokens": {
            "total_tokens_used": total_tokens,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "avg_tokens_per_run": round(total_tokens / len(all_metrics), 1)
        },
        "timing": {
            "avg_api_duration_seconds": round(avg_api_duration, 3),
            "total_api_time_seconds": round(sum(m['timing']['api_duration_seconds'] for m in all_metrics), 3)
        },
        "output": {
            "avg_concepts_per_run": round(avg_concepts, 1),
            "total_concepts_extracted": sum(m['output']['concepts_count'] for m in all_metrics)
        },
        "date_range": {
            "first_run": all_metrics[-1]['timestamp'] if all_metrics else None,
            "last_run": all_metrics[0]['timestamp'] if all_metrics else None
        }
    }


def get_recent_metrics(limit: int = 10) -> List[Dict]:
    """
    Get the most recent N metrics entries.
    
    Args:
        limit: Number of recent entries to return
        
    Returns:
        List of recent metrics data
    """
    all_metrics = load_all_metrics()
    return all_metrics[:limit]


def clear_old_metrics(days: int = 30):
    """
    Delete metrics files older than specified days.
    
    Args:
        days: Keep metrics from last N days, delete older ones
    """
    ensure_metrics_dir()
    
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = 0
    
    for filepath in METRICS_DIR.glob("run_*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                file_date = datetime.fromisoformat(data['timestamp'])
                
                if file_date < cutoff_date:
                    filepath.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old metrics: {filepath.name}")
        except Exception as e:
            logger.warning(f"Failed to process {filepath.name}: {e}")
    
    logger.info(f"🧹 Cleaned up {deleted_count} old metrics files (older than {days} days)")
    return deleted_count
