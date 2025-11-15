"""
Load Testing Configuration
"""
import os

# API Configuration
BASE_URL = os.getenv("LOAD_TEST_BASE_URL", "http://localhost:8000")

# Default test parameters
DEFAULT_CONCEPT = "Pendulum and its Time Period"
DEFAULT_STUDENT_ID = "load_test_student"

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
MIN_WAIT_TIME = 10  # seconds
MAX_WAIT_TIME = 20 # seconds

print("=" * 80)
print("🔬 Load Testing Configuration Loaded")
print("=" * 80)
print(f"Base URL: {BASE_URL}")
print(f"Default Concept: {DEFAULT_CONCEPT}")
print(f"Request Timeout: {REQUEST_TIMEOUT}s")
print(f"Think Time: {MIN_WAIT_TIME}-{MAX_WAIT_TIME}s")
# print(f"LangSmith Tracing: {'Enabled' if ENABLE_LANGSMITH_TRACING else 'Disabled (recommended for load tests)'}")
print("=" * 80)
