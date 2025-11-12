"""
Session-based load testing tasks
"""
from locust import task, TaskSet
import random
import time
from utils.response_generator import ResponseGenerator
from utils.metrics_collector import global_metrics


class SessionTaskSet(TaskSet):
    """
    Basic session flow: start → continue (5-10 turns) → complete
    """
    
    def on_start(self):
        """Called when a user starts - initialize session"""
        self.thread_id = None
        self.current_state = "START"
        self.turn_count = 0
        self.max_turns = random.randint(5, 10)  # Each user does 5-10 conversation turns
        self.session_active = False
        
        # Start a new session
        self.start_session()
    
    @task(1)
    def start_session(self):
        """Start a new learning session"""
        if self.session_active:
            return  # Already have an active session
        
        start_time = time.time()
        
        with self.client.post(
            "/session/start",
            json={
                "concept_title": "Pendulum and its Time Period",
                "student_id": f"load_test_user_{id(self)}",
                "session_label": f"load_test_{int(time.time())}"
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
                    self.session_active = True
                    self.turn_count = 0
                    
                    # Record metrics
                    global_metrics.record_checkpoint_operation(
                        "save", self.thread_id, latency_ms
                    )
                    
                    response.success()
                else:
                    response.failure(f"Session start failed: {data.get('message')}")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(8)
    def continue_conversation(self):
        """Continue existing conversation - main interaction"""
        if not self.session_active or not self.thread_id:
            # Need to start session first
            self.start_session()
            return
        
        # Check if we've reached max turns
        if self.turn_count >= self.max_turns:
            return
        
        # Generate realistic student response based on current state
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
                    new_state = data.get("current_state")
                    self.current_state = new_state
                    self.turn_count += 1
                    
                    # Record node transition
                    if old_state != new_state:
                        global_metrics.record_node_transition(
                            old_state, new_state, latency_ms
                        )
                    
                    # Check for simulation or images in metadata
                    metadata = data.get("metadata", {})
                    if metadata.get("show_simulation"):
                        print(f"🔬 Simulation triggered at {new_state}")
                    
                    if metadata.get("image_url"):
                        print(f"🖼️  Image loaded at {new_state}")
                    
                    response.success()
                    
                    # End session if we reach END state
                    if new_state == "END":
                        self.session_active = False
                else:
                    response.failure(f"Continue failed: {data.get('message')}")
            
            elif response.status_code == 404:
                # Session not found - need to restart
                response.failure("Session not found - restarting")
                self.session_active = False
                self.thread_id = None
            
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)
    def check_status(self):
        """Occasionally check session status"""
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
                    response.failure("Session does not exist")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    def on_stop(self):
        """Called when user stops - cleanup"""
        if self.thread_id:
            # Optionally delete session (comment out if you want to preserve sessions)
            # self.client.delete(f"/session/{self.thread_id}")
            pass
