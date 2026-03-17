from locust import task, TaskSet
import random
import time
from utils.response_generator import ResponseGenerator
from utils.metrics_collector import global_metrics


class SessionTaskSet(TaskSet):
    """
    Mixed workload TaskSet that calls both API families:
    1) Teaching session endpoints (/session/*)
    2) Simulation session endpoints (/simulation/session/*)
    """

    def on_start(self):
        # Regular teaching session state
        self.thread_id = None
        self.current_state = "START"
        self.reg_turn_count = 0
        self.reg_max_turns = random.randint(5, 10)
        self.reg_active = False

        # Simulation session state
        self.sim_session_id = None
        self.sim_state = "none"
        self.sim_turn_count = 0
        self.sim_max_turns = random.randint(5, 10)
        self.sim_active = False

        # Bootstrap both sessions for mixed traffic
        self._start_regular_session()
        self._start_simulation_session()

    def _start_regular_session(self):
        start_time = time.time()
        with self.client.post(
            "/session/start",
            json={
                "concept_title": "Pendulum and its Time Period",
                "student_id": f"load_test_user_{id(self)}",
                "session_label": f"mixed-regular-{int(time.time())}"
            },
            catch_response=True,
            name="/session/start"
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.thread_id = data.get("thread_id")
                    self.current_state = data.get("current_state", "START")
                    self.reg_turn_count = 0
                    self.reg_active = True
                    global_metrics.record_checkpoint_operation("save", self.thread_id, latency_ms)
                    global_metrics.record_node_transition("NONE", self.current_state, latency_ms)
                    response.success()
                else:
                    response.failure(f"Session start failed: {data.get('message')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    def _start_simulation_session(self):
        start_time = time.time()
        with self.client.post(
            "/simulation/session/start",
            json={
                "simulation_id": "simple_pendulum",
                "student_id": f"load_test_user_{id(self)}",
                "language": "english"
            },
            catch_response=True,
            name="/simulation/session/start"
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 201:
                data = response.json()
                if data.get("session_id"):
                    self.sim_session_id = data.get("session_id")
                    self.sim_state = data.get("learning_state", {}).get("understanding_level", "none")
                    self.sim_turn_count = 0
                    self.sim_active = True
                    global_metrics.record_checkpoint_operation("save", self.sim_session_id, latency_ms)
                    global_metrics.record_node_transition("NONE", self.sim_state, latency_ms)
                    response.success()
                else:
                    response.failure("Simulation start failed: missing session_id")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(6)
    def continue_regular_conversation(self):
        if not self.reg_active or not self.thread_id:
            return

        if self.reg_turn_count >= self.reg_max_turns:
            return

        user_message = ResponseGenerator.generate_response(self.current_state)
        start_time = time.time()
        old_state = self.current_state

        with self.client.post(
            "/session/continue",
            json={
                "thread_id": self.thread_id,
                "user_message": user_message
            },
            catch_response=True,
            name="/session/continue"
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    new_state = data.get("current_state", old_state)
                    self.current_state = new_state
                    self.reg_turn_count += 1

                    if old_state != new_state:
                        global_metrics.record_node_transition(old_state, new_state, latency_ms)

                    metadata = data.get("metadata", {})
                    global_metrics.record_checkpoint_operation("save", self.thread_id, latency_ms * 0.1)

                    if metadata.get("show_simulation"):
                        global_metrics.record_simulation_trigger(new_state)
                    if metadata.get("misconception_detected"):
                        global_metrics.record_misconception(new_state)

                    response.success()

                    if new_state == "END":
                        self.reg_active = False
                        global_metrics.record_session_completion(self.thread_id, self.reg_turn_count)
                else:
                    response.failure(f"Continue failed: {data.get('message')}")
            elif response.status_code == 404:
                self.reg_active = False
                self.thread_id = None
                response.failure("Regular session not found")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(6)
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
            json={
                "student_response": user_message
            },
            catch_response=True,
            name="/simulation/session/{session_id}/respond"
        ) as response:
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                if data.get("session_id"):
                    new_state = data.get("learning_state", {}).get("understanding_level", old_state)
                    self.sim_state = new_state
                    self.sim_turn_count += 1

                    if old_state != new_state:
                        global_metrics.record_node_transition(old_state, new_state, latency_ms)

                    learning_state = data.get("learning_state", {})
                    simulation_info = data.get("simulation", {})
                    global_metrics.record_checkpoint_operation("save", self.sim_session_id, latency_ms * 0.1)

                    if simulation_info.get("html_url"):
                        global_metrics.record_simulation_trigger(new_state)

                    reasoning = (learning_state.get("understanding_reasoning") or "").lower()
                    if "misconception" in reasoning:
                        global_metrics.record_misconception(new_state)

                    response.success()

                    if learning_state.get("session_complete"):
                        self.sim_active = False
                        global_metrics.record_session_completion(self.sim_session_id, self.sim_turn_count)
                else:
                    response.failure("Simulation continue failed: missing session_id")
            elif response.status_code == 404:
                self.sim_active = False
                self.sim_session_id = None
                response.failure("Simulation session not found")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def check_regular_status(self):
        if not self.thread_id:
            return

        with self.client.get(
            f"/session/status/{self.thread_id}",
            catch_response=True,
            name="/session/status/{thread_id}"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("exists"):
                    response.success()
                else:
                    response.failure("Regular session does not exist")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def check_simulation_status(self):
        if not self.sim_session_id:
            return

        with self.client.get(
            f"/simulation/session/{self.sim_session_id}",
            catch_response=True,
            name="/simulation/session/{session_id}"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("session_id"):
                    response.success()
                else:
                    response.failure("Simulation session does not exist")
            else:
                response.failure(f"HTTP {response.status_code}")

    def on_stop(self):
        # Sessions are left as-is for post-test inspection.
        pass
