from locust import task, TaskSet
import random
import time
from utils.response_generator import ResponseGenerator
from utils.metrics_collector import global_metrics


class SessionTaskSet(TaskSet):
    
    def on_start(self):
        self.session_id = None
        self.current_state = "START"
        self.turn_count = 0
        self.max_turns = random.randint(5, 10)  # Each user does 5-10 conversation turns
        self.session_active = False
        self.session_started = False
        
        # Start a new session immediately (only happens once per user)
        self._start_session()
    
    def _start_session(self):
        if self.session_started:
            return  # Already started a session
        
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
                    self.session_id = data.get("session_id")
                    self.current_state = data.get("learning_state", {}).get("understanding_level", "none")
                    self.session_active = True
                    self.session_started = True
                    self.turn_count = 0
                    
                    # Record metrics for session bootstrap
                    global_metrics.record_checkpoint_operation(
                        "save", self.session_id, latency_ms
                    )
                    
                    # Record the initial state
                    global_metrics.record_node_transition(
                        "NONE", self.current_state, latency_ms
                    )
                    
                    response.success()
                else:
                    response.failure("Simulation session start failed: missing session_id")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(10)
    def continue_conversation(self):
        if not self.session_active or not self.session_id:
            # Session not properly started - skip this task
            return
        
        # Check if we've reached max turns
        if self.turn_count >= self.max_turns:
            return
        
        # Generate realistic student response based on current state
        user_message = ResponseGenerator.generate_response(self.current_state)
        
        start_time = time.time()
        old_state = self.current_state
        
        with self.client.post(
            f"/simulation/session/{self.session_id}/respond",
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
                    new_state = data.get("learning_state", {}).get("understanding_level", self.current_state)
                    self.current_state = new_state
                    self.turn_count += 1
                    
                    # Record node transition if state changed
                    if old_state != new_state:
                        global_metrics.record_node_transition(
                            old_state, new_state, latency_ms
                        )
                    
                    # Extract and record additional metrics from metadata
                    learning_state = data.get("learning_state", {})
                    simulation_info = data.get("simulation", {})
                    
                    # Record checkpoint operation (every continue involves checkpoint save)
                    global_metrics.record_checkpoint_operation(
                        "save", self.session_id, latency_ms * 0.1  # Estimate checkpoint is ~10% of total
                    )
                    
                    # Simulation flow is always active on this endpoint.
                    if simulation_info.get("html_url"):
                        global_metrics.record_simulation_trigger(new_state)

                    # Track misconceptions if indicated in reasoning text.
                    reasoning = (learning_state.get("understanding_reasoning") or "").lower()
                    if "misconception" in reasoning:
                        print(f"⚠️  Misconception detected at {new_state}")
                        global_metrics.record_misconception(new_state)
                    
                    response.success()
                    
                    # End session when simulation API reports completion
                    if learning_state.get("session_complete"):
                        self.session_active = False
                        global_metrics.record_session_completion(self.session_id, self.turn_count)
                else:
                    response.failure(f"Continue failed: {data.get('message')}")
            
            elif response.status_code == 404:
                # Session not found - need to restart
                response.failure("Session not found - restarting")
                self.session_active = False
                self.session_id = None
            
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)
    def check_status(self):
        if not self.session_id:
            return
        
        with self.client.get(
            f"/simulation/session/{self.session_id}",
            catch_response=True,
            name="/simulation/session/{session_id}"
        ) as response:
            
            if response.status_code == 200:
                data = response.json()
                if data.get("session_id"):
                    response.success()
                else:
                    response.failure("Session does not exist")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    def on_stop(self):
        if self.session_id:
            # Optionally delete session (comment out if you want to preserve sessions)
            # self.client.delete(f"/session/{self.session_id}")
            pass
