"""Run exactly 10 sequential education or simulation start calls with phase timing."""

import csv
import json
import os
import re
import threading
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv
from locust import HttpUser, constant, events, task


LOAD_TESTS_DIR = Path(__file__).resolve().parent
load_dotenv(LOAD_TESTS_DIR.parent / ".env", override=False)

TOTAL_CALLS = 10
_counter_lock = threading.Lock()
_next_call = 0
_samples = []


def _clean_secret(value: str) -> str:
    return value.strip().strip("'").strip('"')


def _auth_headers() -> dict[str, str]:
    bearer_token = _clean_secret(os.getenv("LOAD_TEST_BEARER_TOKEN", ""))
    if bearer_token:
        return {"Authorization": f"Bearer {bearer_token}"}

    for raw_key in os.getenv("X_API_KEYS", "").split(","):
        api_key = _clean_secret(raw_key)
        if api_key:
            return {"X-API-Key": api_key}
    return {}


def parse_server_timing(header: str) -> dict[str, float]:
    metrics = {}
    for item in header.split(","):
        match = re.match(
            r"\s*([A-Za-z0-9_-]+).*?;\s*dur=([0-9]+(?:\.[0-9]+)?)",
            item,
        )
        if match:
            metrics[match.group(1)] = float(match.group(2))
    return metrics


def _take_call_number() -> int | None:
    global _next_call
    with _counter_lock:
        if _next_call >= TOTAL_CALLS:
            return None
        _next_call += 1
        return _next_call


class StartTimingUser(HttpUser):
    wait_time = constant(0)
    fixed_count = 1

    def on_start(self):
        self.headers = _auth_headers()
        if not self.headers:
            raise RuntimeError(
                "Set X_API_KEYS in .env or LOAD_TEST_BEARER_TOKEN before running the test."
            )

    @task
    def start_session(self):
        call_number = _take_call_number()
        if call_number is None:
            self.environment.runner.quit()
            return

        is_kannada = os.getenv("LOAD_TEST_IS_KANNADA", "false").lower() == "true"
        start_kind = os.getenv("LOAD_TEST_START_KIND", "education").strip().lower()
        student_id = f"start-timing-{datetime.now():%Y%m%d%H%M%S%f}-{call_number}"
        if start_kind == "simulation":
            endpoint = "/simulation/session/start"
            payload = {
                "simulation_id": os.getenv("LOAD_TEST_SIMULATION_ID", "simple_pendulum"),
                "student_id": student_id,
                "language": "kannada" if is_kannada else "english",
            }
        elif start_kind == "whiteboard":
            endpoint = "/whiteboard-tutor/session/start"
            payload = {
                "concept_id": os.getenv(
                    "LOAD_TEST_WHITEBOARD_CONCEPT_ID",
                    "math-p1-ch7-triangle-angles",
                ),
                "student_id": student_id,
            }
        elif start_kind == "education":
            endpoint = "/session/start"
            payload = {
                "concept_title": os.getenv("LOAD_TEST_CONCEPT", "Pendulum and its Time Period"),
                "student_id": student_id,
                "session_label": f"timing-{call_number}",
                "is_kannada": is_kannada,
                "student_level": "medium",
            }
        else:
            raise RuntimeError(
                "LOAD_TEST_START_KIND must be 'education', 'simulation', or 'whiteboard'."
            )

        started_at = perf_counter()
        with self.client.post(
            endpoint,
            json=payload,
            headers=self.headers,
            name=f"{endpoint} [timing]",
            timeout=60,
            catch_response=True,
        ) as response:
            client_total_ms = (perf_counter() - started_at) * 1000
            timing_header = response.headers.get("Server-Timing", "")
            server_metrics = parse_server_timing(timing_header)

            if response.status_code >= 400:
                response.failure(f"HTTP {response.status_code}: {response.text[:300]}")
            elif not timing_header:
                response.failure(
                    "Server-Timing header missing; deploy the timing instrumentation first."
                )
            else:
                response.success()

            sample = {
                "call": call_number,
                "status_code": response.status_code,
                "client_total_ms": round(client_total_ms, 3),
                **server_metrics,
            }
            if "server_total" in server_metrics:
                sample["client_unattributed_ms"] = round(
                    max(client_total_ms - server_metrics["server_total"], 0.0),
                    3,
                )
            _samples.append(sample)
            print(f"start timing {call_number}/{TOTAL_CALLS}: {json.dumps(sample, sort_keys=True)}")

        if call_number == TOTAL_CALLS:
            self.environment.runner.quit()


@events.test_stop.add_listener
def report_start_timings(environment, **kwargs):
    if not _samples:
        return

    values_by_metric = defaultdict(list)
    for sample in _samples:
        for metric, value in sample.items():
            if metric not in {"call", "status_code"} and isinstance(value, (int, float)):
                values_by_metric[metric].append(float(value))

    print("\nPer-stage timing summary (milliseconds)")
    print(f"{'stage':<28} {'count':>5} {'average':>12} {'minimum':>12} {'maximum':>12}")
    for metric, values in sorted(values_by_metric.items()):
        print(
            f"{metric:<28} {len(values):>5} "
            f"{sum(values) / len(values):>12.3f} {min(values):>12.3f} {max(values):>12.3f}"
        )

    reports_dir = LOAD_TESTS_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = reports_dir / f"start_timing_{timestamp}.json"
    csv_path = reports_dir / f"start_timing_{timestamp}.csv"

    json_path.write_text(json.dumps(_samples, indent=2), encoding="utf-8")
    fieldnames = sorted({key for sample in _samples for key in sample})
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_samples)

    print(f"Raw JSON: {json_path}")
    print(f"Raw CSV:  {csv_path}")
