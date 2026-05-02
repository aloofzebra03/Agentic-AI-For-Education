from locust import task, TaskSet
import random
import time

from config import AUTH_HEADERS, DEFAULT_MATH_PROBLEM_ID
from utils.metrics_collector import global_metrics
from utils.response_generator import ResponseGenerator


class SessionTaskSet(TaskSet):
    """Load-test the v5 math tutoring endpoints."""

    def on_start(self):
        self.thread_id = None
        self.current_state = "START"
        self.turn_count = 0
        self.max_turns = random.randint(5, 10)
        self.session_active = False
        self.session_started = False
        self.problem_id = DEFAULT_MATH_PROBLEM_ID or None
        self.is_kannada = False

        self._resolve_problem_id()
        self._start_session()

    def _resolve_problem_id(self):
        if self.problem_id:
            return

        with self.client.get(
            "/math/problems",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/problems",
        ) as response:
            if response.status_code == 200:
                data = response.json()
                problems = data.get("problems", [])
                if problems:
                    self.problem_id = problems[0].get("problem_id")
                    response.success()
                else:
                    response.failure("No math problems returned")
            else:
                response.failure(f"HTTP {response.status_code}")

    def _start_session(self):
        if self.session_started or not self.problem_id:
            return

        start_time = time.time()
        with self.client.post(
            "/math/session/start",
            json={
                "problem_id": self.problem_id,
                "student_id": f"math_load_user_{id(self)}",
                "session_label": f"math-load-{int(time.time())}",
                "is_kannada": self.is_kannada,
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/start",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.thread_id = data.get("thread_id")
                    self.current_state = data.get("current_state", "START")
                    self.session_active = True
                    self.session_started = True
                    self.turn_count = 0
                    global_metrics.record_checkpoint_operation("save", self.thread_id, latency_ms)
                    global_metrics.record_node_transition("NONE", self.current_state, latency_ms)
                    response.success()
                else:
                    response.failure(f"Math session start failed: {data.get('message')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(10)
    def continue_conversation(self):
        if not self.session_active or not self.thread_id:
            return

        if self.turn_count >= self.max_turns:
            return

        user_message = ResponseGenerator.generate_math_response(self.current_state)
        start_time = time.time()
        old_state = self.current_state

        with self.client.post(
            "/math/session/continue",
            data={
                "thread_id": self.thread_id,
                "user_message": user_message,
                "is_kannada": str(self.is_kannada).lower(),
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/continue",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    new_state = data.get("current_state", old_state)
                    self.current_state = new_state
                    self.turn_count += 1

                    if old_state != new_state:
                        global_metrics.record_node_transition(old_state, new_state, latency_ms)

                    global_metrics.record_checkpoint_operation(
                        "save", self.thread_id, latency_ms * 0.1
                    )
                    response.success()

                    if new_state == "END":
                        self.session_active = False
                        global_metrics.record_session_completion(self.thread_id, self.turn_count)
                else:
                    response.failure(f"Math continue failed: {data.get('message')}")
            elif response.status_code == 404:
                response.failure("Math session not found")
                self.session_active = False
                self.thread_id = None
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def check_status(self):
        if not self.thread_id:
            return

        with self.client.get(
            f"/math/session/status/{self.thread_id}",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/status/{thread_id}",
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("exists"):
                    response.success()
                else:
                    response.failure("Math session does not exist")
            else:
                response.failure(f"HTTP {response.status_code}")
