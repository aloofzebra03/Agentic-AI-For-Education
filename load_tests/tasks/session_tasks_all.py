from locust import task, TaskSet
import random
import time

from config import AUTH_HEADERS, DEFAULT_MATH_PROBLEM_ID
from utils.metrics_collector import global_metrics
from utils.response_generator import ResponseGenerator


class SessionTaskSet(TaskSet):
    """Combined workload for regular education, simulation, and math endpoints."""

    def on_start(self):
        self.reg_thread_id = None
        self.reg_state = "START"
        self.reg_turn_count = 0
        self.reg_max_turns = random.randint(5, 10)
        self.reg_active = False

        self.sim_session_id = None
        self.sim_state = "none"
        self.sim_turn_count = 0
        self.sim_max_turns = random.randint(5, 10)
        self.sim_active = False

        self.math_thread_id = None
        self.math_state = "START"
        self.math_turn_count = 0
        self.math_max_turns = random.randint(5, 10)
        self.math_active = False
        self.math_problem_id = DEFAULT_MATH_PROBLEM_ID or None
        self.math_is_kannada = False

        self._start_regular_session()
        self._start_simulation_session()
        self._resolve_math_problem_id()
        self._start_math_session()

    def _start_regular_session(self):
        start_time = time.time()
        with self.client.post(
            "/session/start",
            json={
                "concept_title": "Pendulum and its Time Period",
                "student_id": f"all_load_user_{id(self)}",
                "session_label": f"all-regular-{int(time.time())}",
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/session/start",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("success"):
                response.failure(f"Session start failed: {data.get('message')}")
                return

            self.reg_thread_id = data.get("thread_id")
            self.reg_state = data.get("current_state", "START")
            self.reg_active = True
            global_metrics.record_checkpoint_operation("save", self.reg_thread_id, latency_ms)
            global_metrics.record_node_transition("NONE", self.reg_state, latency_ms)
            response.success()

    def _start_simulation_session(self):
        start_time = time.time()
        with self.client.post(
            "/simulation/session/start",
            json={
                "simulation_id": "simple_pendulum",
                "student_id": f"all_load_user_{id(self)}",
                "language": "english",
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/simulation/session/start",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code != 201:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("session_id"):
                response.failure("Simulation start failed: missing session_id")
                return

            self.sim_session_id = data.get("session_id")
            self.sim_state = data.get("learning_state", {}).get("understanding_level", "none")
            self.sim_active = True
            global_metrics.record_checkpoint_operation("save", self.sim_session_id, latency_ms)
            global_metrics.record_node_transition("NONE", self.sim_state, latency_ms)
            response.success()

    def _resolve_math_problem_id(self):
        if self.math_problem_id:
            return

        with self.client.get(
            "/math/problems",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/problems",
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            problems = response.json().get("problems", [])
            if not problems:
                response.failure("No math problems returned")
                return

            self.math_problem_id = problems[0].get("problem_id")
            response.success()

    def _start_math_session(self):
        if not self.math_problem_id:
            return

        start_time = time.time()
        with self.client.post(
            "/math/session/start",
            json={
                "problem_id": self.math_problem_id,
                "student_id": f"all_math_load_user_{id(self)}",
                "session_label": f"all-math-{int(time.time())}",
                "is_kannada": self.math_is_kannada,
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/start",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("success"):
                response.failure(f"Math session start failed: {data.get('message')}")
                return

            self.math_thread_id = data.get("thread_id")
            self.math_state = data.get("current_state", "START")
            self.math_active = True
            global_metrics.record_checkpoint_operation("save", self.math_thread_id, latency_ms)
            global_metrics.record_node_transition("NONE", self.math_state, latency_ms)
            response.success()

    @task(5)
    def continue_regular_conversation(self):
        if not self.reg_active or not self.reg_thread_id:
            return
        if self.reg_turn_count >= self.reg_max_turns:
            return

        user_message = ResponseGenerator.generate_response(self.reg_state)
        start_time = time.time()
        old_state = self.reg_state

        with self.client.post(
            "/session/continue",
            json={"thread_id": self.reg_thread_id, "user_message": user_message},
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/session/continue",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code == 404:
                self.reg_active = False
                self.reg_thread_id = None
                response.failure("Regular session not found")
                return
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("success"):
                response.failure(f"Continue failed: {data.get('message')}")
                return

            self.reg_state = data.get("current_state", old_state)
            self.reg_turn_count += 1
            if old_state != self.reg_state:
                global_metrics.record_node_transition(old_state, self.reg_state, latency_ms)
            global_metrics.record_checkpoint_operation("save", self.reg_thread_id, latency_ms * 0.1)
            if data.get("metadata", {}).get("show_simulation"):
                global_metrics.record_simulation_trigger(self.reg_state)
            if self.reg_state == "END":
                self.reg_active = False
                global_metrics.record_session_completion(self.reg_thread_id, self.reg_turn_count)
            response.success()

    @task(5)
    def continue_simulation_conversation(self):
        if not self.sim_active or not self.sim_session_id:
            return
        if self.sim_turn_count >= self.sim_max_turns:
            return

        user_message = ResponseGenerator.generate_response(self.sim_state)
        start_time = time.time()
        old_state = self.sim_state

        with self.client.post(
            f"/simulation/session/{self.sim_session_id}/respond",
            json={"student_response": user_message},
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/simulation/session/{session_id}/respond",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code == 404:
                self.sim_active = False
                self.sim_session_id = None
                response.failure("Simulation session not found")
                return
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("session_id"):
                response.failure("Simulation continue failed: missing session_id")
                return

            learning_state = data.get("learning_state", {})
            simulation_info = data.get("simulation", {})
            self.sim_state = learning_state.get("understanding_level", old_state)
            self.sim_turn_count += 1
            if old_state != self.sim_state:
                global_metrics.record_node_transition(old_state, self.sim_state, latency_ms)
            global_metrics.record_checkpoint_operation("save", self.sim_session_id, latency_ms * 0.1)
            if simulation_info.get("html_url"):
                global_metrics.record_simulation_trigger(self.sim_state)
            if learning_state.get("session_complete"):
                self.sim_active = False
                global_metrics.record_session_completion(self.sim_session_id, self.sim_turn_count)
            response.success()

    @task(5)
    def continue_math_conversation(self):
        if not self.math_active or not self.math_thread_id:
            return
        if self.math_turn_count >= self.math_max_turns:
            return

        user_message = ResponseGenerator.generate_math_response(self.math_state)
        start_time = time.time()
        old_state = self.math_state

        with self.client.post(
            "/math/session/continue",
            data={
                "thread_id": self.math_thread_id,
                "user_message": user_message,
                "is_kannada": str(self.math_is_kannada).lower(),
            },
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/continue",
        ) as response:
            latency_ms = (time.time() - start_time) * 1000
            if response.status_code == 404:
                self.math_active = False
                self.math_thread_id = None
                response.failure("Math session not found")
                return
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            data = response.json()
            if not data.get("success"):
                response.failure(f"Math continue failed: {data.get('message')}")
                return

            self.math_state = data.get("current_state", old_state)
            self.math_turn_count += 1
            if old_state != self.math_state:
                global_metrics.record_node_transition(old_state, self.math_state, latency_ms)
            global_metrics.record_checkpoint_operation("save", self.math_thread_id, latency_ms * 0.1)
            if self.math_state == "END":
                self.math_active = False
                global_metrics.record_session_completion(self.math_thread_id, self.math_turn_count)
            response.success()

    @task(1)
    def check_regular_status(self):
        if not self.reg_thread_id:
            return
        with self.client.get(
            f"/session/status/{self.reg_thread_id}",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/session/status/{thread_id}",
        ) as response:
            if response.status_code == 200 and response.json().get("exists"):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def check_simulation_status(self):
        if not self.sim_session_id:
            return
        with self.client.get(
            f"/simulation/session/{self.sim_session_id}",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/simulation/session/{session_id}",
        ) as response:
            if response.status_code == 200 and response.json().get("session_id"):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def check_math_status(self):
        if not self.math_thread_id:
            return
        with self.client.get(
            f"/math/session/status/{self.math_thread_id}",
            headers=AUTH_HEADERS,
            catch_response=True,
            name="/math/session/status/{thread_id}",
        ) as response:
            if response.status_code == 200 and response.json().get("exists"):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
