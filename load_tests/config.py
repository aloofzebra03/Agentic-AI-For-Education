"""
Load Testing Configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv


LOAD_TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = LOAD_TESTS_DIR.parent
load_dotenv(dotenv_path=REPO_ROOT / ".env", override=False)

# API Configuration
BASE_URL = os.getenv("LOAD_TEST_BASE_URL", "http://localhost:8000")
AUTH_HEADERS = {}


def _clean_secret(value: str) -> str:
    return value.strip().strip("'").strip('"')


def first_api_key_from_env() -> str:
    """Return the first endpoint access key from X_API_KEYS."""
    for raw_key in os.getenv("X_API_KEYS", "").split(","):
        key = _clean_secret(raw_key)
        if key:
            return key
    return ""

# Task mode selection:
# - regular: calls /session/* endpoints
# - simulation: calls /simulation/session/* endpoints
# - mixed: calls both flows in one workload
# - math: calls /math/* endpoints
# - all: calls regular + simulation + math endpoints
LOAD_TEST_TASK_MODE = os.getenv("LOAD_TEST_TASK_MODE", "simulation").strip().lower()

# Default test parameters
DEFAULT_CONCEPT = "Pendulum and its Time Period"
DEFAULT_STUDENT_ID = "load_test_student"
DEFAULT_MATH_PROBLEM_ID = os.getenv("LOAD_TEST_MATH_PROBLEM_ID", "").strip()


def configure_runtime_options(
    task_mode: str | None = None,
    api_key: str | None = None,
    math_problem_id: str | None = None,
) -> None:
    """Apply CLI/env runtime options while preserving imported AUTH_HEADERS refs."""
    global LOAD_TEST_TASK_MODE, DEFAULT_MATH_PROBLEM_ID

    if task_mode:
        LOAD_TEST_TASK_MODE = task_mode.strip().lower()

    if math_problem_id is not None:
        DEFAULT_MATH_PROBLEM_ID = math_problem_id.strip()

    selected_api_key = _clean_secret(api_key or "") or first_api_key_from_env()
    AUTH_HEADERS.clear()
    if selected_api_key:
        AUTH_HEADERS["X-API-Key"] = selected_api_key


configure_runtime_options()

# Load test scenarios
LOAD_SCENARIOS = {
    "baseline": {
        "users": 10,
        "spawn_rate": 1,
        "run_time": "5m",
        "description": "Baseline test - measure cold start and node latencies"
    },
    "light": {
        "users": 100,
        "spawn_rate": 10,
        "run_time": "10m",
        "description": "Light load - test DB write stress and connection pooling"
    },
    "medium": {
        "users": 1000,
        "spawn_rate": 50,
        "run_time": "15m",
        "description": "Medium load - identify LLM call queue delays"
    },
    "stress": {
        "users": 10000,
        "spawn_rate": 100,
        "run_time": "20m",
        "description": "Stress test - find breaking point and dropped requests"
    }
}

# Performance thresholds (for validation)
PERFORMANCE_THRESHOLDS = {
    10: {
        "avg_latency_ms": 2000,
        "error_rate_percent": 0,
        "p95_latency_ms": 3000
    },
    100: {
        "avg_latency_ms": 5000,
        "error_rate_percent": 0.1,
        "p95_latency_ms": 7000
    },
    1000: {
        "avg_latency_ms": 10000,
        "error_rate_percent": 1,
        "p95_latency_ms": 15000
    },
    10000: {
        "avg_latency_ms": 20000,
        "error_rate_percent": 5,
        "p95_latency_ms": 30000
    }
}

# LangSmith tracing (disable during high load)
# ENABLE_LANGSMITH_TRACING = os.getenv("ENABLE_LANGSMITH_TRACING", "false").lower() == "true"

# Request timeouts
REQUEST_TIMEOUT = 60  # seconds (LLM calls can be slow)

# Think time between requests (simulates real users)
MIN_WAIT_TIME = 20  # seconds
MAX_WAIT_TIME = 30 # seconds

print("=" * 80)
print("🔬 Load Testing Configuration Loaded")
print("=" * 80)
print(f"Base URL: {BASE_URL}")
print(f"Initial Task Mode: {LOAD_TEST_TASK_MODE}")
print(f"Default Concept: {DEFAULT_CONCEPT}")
print(f"Math Problem Override: {DEFAULT_MATH_PROBLEM_ID or 'first problem from /math/problems'}")
print(f"Auth Header: {'X-API-Key configured' if AUTH_HEADERS else 'not configured'}")
print(f"Request Timeout: {REQUEST_TIMEOUT}s")
print(f"Think Time: {MIN_WAIT_TIME}-{MAX_WAIT_TIME}s")
# print(f"LangSmith Tracing: {'Enabled' if ENABLE_LANGSMITH_TRACING else 'Disabled (recommended for load tests)'}")
print("=" * 80)
