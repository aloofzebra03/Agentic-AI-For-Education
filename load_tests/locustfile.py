"""
Main Locust Load Testing File for Educational Agent API
Run with: locust -f locustfile.py --host=http://localhost:8000
"""
from locust import HttpUser, between, events
from tasks.session_tasks import SessionTaskSet
from utils.metrics_collector import global_metrics
from config import MIN_WAIT_TIME, MAX_WAIT_TIME, REQUEST_TIMEOUT
import sys
import os

# Add parent directory to path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class EducationalAgentUser(HttpUser):
    """
    Simulates a student using the Educational Agent API
    
    Each user:
    1. Starts a learning session
    2. Has 5-10 conversation turns with the agent
    3. Waits 1-3 seconds between requests (simulates thinking)
    4. May check session status occasionally
    """
    
    # Task set defining user behavior
    tasks = [SessionTaskSet]
    
    # Wait time between tasks (simulates student thinking)
    wait_time = between(MIN_WAIT_TIME, MAX_WAIT_TIME)
    
    # Request timeout (LLM calls can be slow)
    connection_timeout = REQUEST_TIMEOUT
    network_timeout = REQUEST_TIMEOUT


# ============================================================================
# EVENT HANDLERS (for test lifecycle)
# ============================================================================

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when load test starts"""
    print("\n" + "=" * 80)
    print("🚀 LOAD TEST STARTING")
    print("=" * 80)
    print(f"Target Host: {environment.host}")
    print(f"User Class: {EducationalAgentUser.__name__}")
    print(f"Tasks: {EducationalAgentUser.tasks}")
    print(f"Wait Time: {MIN_WAIT_TIME}-{MAX_WAIT_TIME} seconds")
    print("=" * 80 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when load test stops - print custom metrics"""
    print("\n" + "=" * 80)
    print("🏁 LOAD TEST COMPLETED")
    print("=" * 80)
    
    # Print Locust's built-in stats
    stats = environment.stats
    print(f"\n📈 Request Statistics:")
    print(f"Total Requests: {stats.total.num_requests}")
    print(f"Total Failures: {stats.total.num_failures}")
    print(f"Failure Rate: {stats.total.fail_ratio * 100:.2f}%")
    print(f"Average Response Time: {stats.total.avg_response_time:.2f}ms")
    print(f"Min Response Time: {stats.total.min_response_time:.2f}ms")
    print(f"Max Response Time: {stats.total.max_response_time:.2f}ms")
    print(f"Requests per Second: {stats.total.total_rps:.2f}")
    
    # Print percentile stats
    if stats.total.num_requests > 0:
        print(f"\n📊 Percentile Response Times:")
        print(f"50th percentile: {stats.total.get_response_time_percentile(0.5):.2f}ms")
        print(f"75th percentile: {stats.total.get_response_time_percentile(0.75):.2f}ms")
        print(f"90th percentile: {stats.total.get_response_time_percentile(0.90):.2f}ms")
        print(f"95th percentile: {stats.total.get_response_time_percentile(0.95):.2f}ms")
        print(f"99th percentile: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    
    # Print custom metrics
    global_metrics.print_summary()
    
    print("\n" + "=" * 80)
    print("💡 TIP: Open the Locust web UI for detailed graphs and charts")
    print("=" * 80 + "\n")


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    """Called when Locust is quitting"""
    # Could save metrics to file here if needed
    pass


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_thresholds(environment):
    """
    Validate if test meets performance thresholds
    Called manually or via CI/CD
    """
    from config import PERFORMANCE_THRESHOLDS
    
    stats = environment.stats.total
    user_count = environment.runner.user_count
    
    # Find closest threshold
    threshold_key = min(PERFORMANCE_THRESHOLDS.keys(), 
                        key=lambda x: abs(x - user_count))
    thresholds = PERFORMANCE_THRESHOLDS[threshold_key]
    
    print(f"\n🎯 Validating against {threshold_key}-user thresholds:")
    
    passed = True
    
    # Check avg latency
    if stats.avg_response_time > thresholds["avg_latency_ms"]:
        print(f"❌ Average latency: {stats.avg_response_time:.2f}ms (threshold: {thresholds['avg_latency_ms']}ms)")
        passed = False
    else:
        print(f"✅ Average latency: {stats.avg_response_time:.2f}ms (threshold: {thresholds['avg_latency_ms']}ms)")
    
    # Check error rate
    error_rate = stats.fail_ratio * 100
    if error_rate > thresholds["error_rate_percent"]:
        print(f"❌ Error rate: {error_rate:.2f}% (threshold: {thresholds['error_rate_percent']}%)")
        passed = False
    else:
        print(f"✅ Error rate: {error_rate:.2f}% (threshold: {thresholds['error_rate_percent']}%)")
    
    # Check p95 latency
    if stats.num_requests > 0:
        p95 = stats.get_response_time_percentile(0.95)
        if p95 > thresholds["p95_latency_ms"]:
            print(f"❌ P95 latency: {p95:.2f}ms (threshold: {thresholds['p95_latency_ms']}ms)")
            passed = False
        else:
            print(f"✅ P95 latency: {p95:.2f}ms (threshold: {thresholds['p95_latency_ms']}ms)")
    
    return passed


# ============================================================================
# MAIN ENTRY POINT (for direct execution)
# ============================================================================

if __name__ == "__main__":
    """
    This allows running the test directly with Python (though Locust CLI is preferred)
    """
    print("=" * 80)
    print("📚 Educational Agent Load Testing")
    print("=" * 80)
    print("\n✨ To run the load test, use one of these commands:\n")
    print("1. Basic test (10 users):")
    print("   locust -f locustfile.py --host=http://localhost:8000 --users=10 --spawn-rate=1 --run-time=5m --headless\n")
    print("2. With Web UI (interactive):")
    print("   locust -f locustfile.py --host=http://localhost:8000\n")
    print("   Then open: http://localhost:8089\n")
    print("3. Baseline scenario:")
    print("   locust -f locustfile.py --host=http://localhost:8000 --users=10 --spawn-rate=1 --run-time=5m --headless --html=reports/report_baseline.html\n")
    print("4. Light load scenario:")
    print("   locust -f locustfile.py --host=http://localhost:8000 --users=100 --spawn-rate=10 --run-time=10m --headless --html=reports/report_light.html\n")
    print("=" * 80)
