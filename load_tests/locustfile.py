from locust import HttpUser, between, events
from tasks.session_tasks import SessionTaskSet
from utils.metrics_collector import global_metrics
from config import MIN_WAIT_TIME, MAX_WAIT_TIME, REQUEST_TIMEOUT
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# # Add parent directory to path to ensure imports work
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class EducationalAgentUser(HttpUser):

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
    
    # Export all reports
    export_reports(environment)
    
    # Request API server to export its API key metrics
    print("\n" + "=" * 80)
    print("🔑 EXPORTING API KEY PERFORMANCE METRICS")
    print("=" * 80)
    try:
        import requests
        response = requests.get(f"{environment.host}/test/api-key-metrics", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ API key metrics exported by server")
                print(f"📁 File: {data.get('filepath')}")
            else:
                print(f"⚠️ {data.get('message')}")
        else:
            print(f"❌ Server returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error requesting API key metrics from server: {e}")
    
    print("\n" + "=" * 80)
    print("💡 TIP: Check the reports/ directory for detailed analysis files")
    print("=" * 80 + "\n")


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    export_reports(environment)


# ============================================================================
# REPORT EXPORT FUNCTIONS
# ============================================================================

def export_reports(environment):

    # Get stats
    stats = environment.stats
    
    # Create reports directory if it doesn't exist
    reports_dir = Path("load_tests/reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Use target_user_count as it persists during shutdown, user_count may be 0
    user_count = getattr(environment.runner, 'target_user_count', 
                         getattr(environment.runner, 'user_count', 0))
    
    # 1. Export JSON report with all metrics
    export_json_report(stats, timestamp, user_count, reports_dir)
    
    # 2. Export CSV report with request stats
    export_csv_report(stats, timestamp, user_count, reports_dir)
    
    # 3. Export custom metrics to text file
    export_custom_metrics(timestamp, user_count, reports_dir)
    
    # 4. Export summary report
    export_summary_report(stats, timestamp, user_count, reports_dir)
    
    print(f"\n📁 Reports exported to: {reports_dir.absolute()}")
    print(f"   - report_{user_count}users_{timestamp}.json")
    print(f"   - report_{user_count}users_{timestamp}_stats.csv")
    print(f"   - report_{user_count}users_{timestamp}_custom.txt")
    print(f"   - report_{user_count}users_{timestamp}_summary.txt")


def export_json_report(stats, timestamp, user_count, reports_dir):
    report_data = {
        "test_info": {
            "timestamp": datetime.now().isoformat(),
            "users": user_count,
            "duration_seconds": stats.total.last_request_timestamp - stats.total.start_time if stats.total.num_requests > 0 else 0
        },
        "request_stats": {
            "total_requests": stats.total.num_requests,
            "total_failures": stats.total.num_failures,
            "failure_rate": stats.total.fail_ratio,
            "avg_response_time_ms": stats.total.avg_response_time,
            "min_response_time_ms": stats.total.min_response_time,
            "max_response_time_ms": stats.total.max_response_time,
            "median_response_time_ms": stats.total.median_response_time,
            "requests_per_second": stats.total.total_rps,
            "percentiles": {
                "p50": stats.total.get_response_time_percentile(0.5) if stats.total.num_requests > 0 else 0,
                "p75": stats.total.get_response_time_percentile(0.75) if stats.total.num_requests > 0 else 0,
                "p90": stats.total.get_response_time_percentile(0.90) if stats.total.num_requests > 0 else 0,
                "p95": stats.total.get_response_time_percentile(0.95) if stats.total.num_requests > 0 else 0,
                "p99": stats.total.get_response_time_percentile(0.99) if stats.total.num_requests > 0 else 0
            }
        },
        "endpoint_stats": {},
        "custom_metrics": global_metrics.get_summary()
    }
    
    # Add per-endpoint stats
    duration = stats.total.last_request_timestamp - stats.total.start_time if stats.total.num_requests > 0 else 1
    for name, endpoint_stats in stats.entries.items():
        # Calculate RPS properly for each endpoint
        rps = endpoint_stats.num_requests / duration if duration > 0 else 0
        
        report_data["endpoint_stats"][str(name)] = {
            "num_requests": endpoint_stats.num_requests,
            "num_failures": endpoint_stats.num_failures,
            "avg_response_time_ms": endpoint_stats.avg_response_time,
            "min_response_time_ms": endpoint_stats.min_response_time,
            "max_response_time_ms": endpoint_stats.max_response_time,
            "requests_per_second": rps
        }
    
    # Write JSON file
    json_file = reports_dir / f"report_{user_count}users_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)


def export_csv_report(stats, timestamp, user_count, reports_dir):
    csv_file = reports_dir / f"report_{user_count}users_{timestamp}_stats.csv"
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("Endpoint,Method,Requests,Failures,Failure Rate (%),Avg (ms),Min (ms),Max (ms),Median (ms),RPS,P95 (ms),P99 (ms)\n")
        
        # Per-endpoint stats
        for name, endpoint_stats in stats.entries.items():
            # Handle both string and StatsEntry name formats
            name_str = str(name)
            if ' ' in name_str:
                parts = name_str.split(' ', 1)
                method = parts[0]
                endpoint = parts[1]
            else:
                method = "GET"
                endpoint = name_str
            
            # Calculate RPS properly
            duration = stats.total.last_request_timestamp - stats.total.start_time if stats.total.num_requests > 0 else 1
            rps = endpoint_stats.num_requests / duration if duration > 0 else 0
            
            f.write(f"{endpoint},{method},{endpoint_stats.num_requests},{endpoint_stats.num_failures},")
            f.write(f"{endpoint_stats.fail_ratio * 100:.2f},{endpoint_stats.avg_response_time:.2f},")
            f.write(f"{endpoint_stats.min_response_time:.2f},{endpoint_stats.max_response_time:.2f},")
            f.write(f"{endpoint_stats.median_response_time:.2f},{rps:.2f},")
            p95 = endpoint_stats.get_response_time_percentile(0.95) if endpoint_stats.num_requests > 0 else 0
            p99 = endpoint_stats.get_response_time_percentile(0.99) if endpoint_stats.num_requests > 0 else 0
            f.write(f"{p95:.2f},{p99:.2f}\n")
        
        # Total/Aggregated stats
        f.write(f"\nAggregated,ALL,{stats.total.num_requests},{stats.total.num_failures},")
        f.write(f"{stats.total.fail_ratio * 100:.2f},{stats.total.avg_response_time:.2f},")
        f.write(f"{stats.total.min_response_time:.2f},{stats.total.max_response_time:.2f},")
        f.write(f"{stats.total.median_response_time:.2f},{stats.total.total_rps:.2f},")
        p95 = stats.total.get_response_time_percentile(0.95) if stats.total.num_requests > 0 else 0
        p99 = stats.total.get_response_time_percentile(0.99) if stats.total.num_requests > 0 else 0
        f.write(f"{p95:.2f},{p99:.2f}\n")


def export_custom_metrics(timestamp, user_count, reports_dir):
    txt_file = reports_dir / f"report_{user_count}users_{timestamp}_custom.txt"
    
    summary = global_metrics.get_summary()
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CUSTOM LANGGRAPH METRICS REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Users: {user_count}\n\n")
        
        # Node latencies
        f.write("🔄 Node Transition Latencies:\n")
        f.write("-" * 80 + "\n")
        node_stats = summary.get("node_latencies", {})
        if node_stats:
            f.write(f"{'Node':<15} {'Count':<10} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}\n")
            for node, stats in sorted(node_stats.items()):
                f.write(f"{node:<15} {stats['count']:<10} {stats['avg']:<12.2f} {stats['min']:<12.2f} {stats['max']:<12.2f}\n")
        else:
            f.write("No node transitions recorded\n")
        
        f.write("\n")
        
        # Checkpoint stats
        f.write("💾 Checkpoint Operations:\n")
        f.write("-" * 80 + "\n")
        checkpoint_stats = summary.get("checkpoint_stats", {})
        if checkpoint_stats:
            f.write(f"Total Operations: {checkpoint_stats.get('total_operations', 0)}\n")
            if "save_avg_ms" in checkpoint_stats:
                f.write(f"Save - Count: {checkpoint_stats['save_count']}, Avg: {checkpoint_stats['save_avg_ms']:.2f}ms, Max: {checkpoint_stats['save_max_ms']:.2f}ms\n")
            if "load_avg_ms" in checkpoint_stats:
                f.write(f"Load - Count: {checkpoint_stats['load_count']}, Avg: {checkpoint_stats['load_avg_ms']:.2f}ms, Max: {checkpoint_stats['load_max_ms']:.2f}ms\n")
        else:
            f.write("No checkpoint operations recorded\n")
        
        f.write("\n")
        
        # LangGraph-specific metrics
        f.write("🎯 LangGraph-Specific Metrics:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Transitions: {summary.get('total_transitions', 0)}\n")
        f.write(f"Simulations Triggered: {summary.get('total_simulations', 0)}\n")
        f.write(f"Images Loaded: {summary.get('total_images', 0)}\n")
        f.write(f"Videos Loaded: {summary.get('total_videos', 0)}\n")
        f.write(f"Misconceptions Detected: {summary.get('total_misconceptions', 0)}\n")
        f.write(f"Average Quiz Score: {summary.get('avg_quiz_score', 0):.2f}\n")
        f.write(f"Completed Sessions: {summary.get('completed_sessions', 0)}\n")
        
        f.write("\n" + "=" * 80 + "\n")


def export_summary_report(stats, timestamp, user_count, reports_dir):
    txt_file = reports_dir / f"report_{user_count}users_{timestamp}_summary.txt"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LOAD TEST SUMMARY REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Target: {user_count} concurrent users\n")
        duration = stats.total.last_request_timestamp - stats.total.start_time if stats.total.num_requests > 0 else 0
        f.write(f"Duration: {duration:.2f} seconds\n\n")
        
        f.write("📊 OVERALL PERFORMANCE:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Requests: {stats.total.num_requests}\n")
        f.write(f"Total Failures: {stats.total.num_failures}\n")
        f.write(f"Failure Rate: {stats.total.fail_ratio * 100:.2f}%\n")
        f.write(f"Requests per Second: {stats.total.total_rps:.2f}\n\n")
        
        f.write("⏱️  RESPONSE TIMES:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Average: {stats.total.avg_response_time:.2f}ms\n")
        f.write(f"Minimum: {stats.total.min_response_time:.2f}ms\n")
        f.write(f"Maximum: {stats.total.max_response_time:.2f}ms\n")
        f.write(f"Median: {stats.total.median_response_time:.2f}ms\n")
        
        if stats.total.num_requests > 0:
            f.write(f"\nPercentiles:\n")
            f.write(f"  P50: {stats.total.get_response_time_percentile(0.5):.2f}ms\n")
            f.write(f"  P75: {stats.total.get_response_time_percentile(0.75):.2f}ms\n")
            f.write(f"  P90: {stats.total.get_response_time_percentile(0.90):.2f}ms\n")
            f.write(f"  P95: {stats.total.get_response_time_percentile(0.95):.2f}ms\n")
            f.write(f"  P99: {stats.total.get_response_time_percentile(0.99):.2f}ms\n")
        
        f.write("\n" + "=" * 80 + "\n")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_thresholds(environment):
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

