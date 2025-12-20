from locust import task, TaskSet
import random
import time
from utils.response_generator import ResponseGenerator
from utils.metrics_collector import global_metrics


class SessionTaskSet(TaskSet):
    
    def on_start(self):
        self.thread_id = None
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
            "/session/start",
            json={
                "concept_title": "Pendulum and its Time Period",
                "student_id": f"load_test_user_{id(self)}",
                "session_label": f"gemini-2.5-flash_{int(time.time())}"
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
                    self.session_started = True
                    self.turn_count = 0
                    
                    # Record metrics - session start includes checkpoint save
                    global_metrics.record_checkpoint_operation(
                        "save", self.thread_id, latency_ms
                    )
                    
                    # Record the initial state
                    global_metrics.record_node_transition(
                        "NONE", self.current_state, latency_ms
                    )
                    
                    response.success()
                else:
                    response.failure(f"Session start failed: {data.get('message')}")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(10)
    def continue_conversation(self):
        if not self.session_active or not self.thread_id:
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
                    
                    # Record node transition if state changed
                    if old_state != new_state:
                        global_metrics.record_node_transition(
                            old_state, new_state, latency_ms
                        )
                    
                    # Extract and record additional metrics from metadata
                    metadata = data.get("metadata", {})
                    
                    # Record checkpoint operation (every continue involves checkpoint save)
                    global_metrics.record_checkpoint_operation(
                        "save", self.thread_id, latency_ms * 0.1  # Estimate checkpoint is ~10% of total
                    )
                    
                    # Track simulation triggers
                    if metadata.get("show_simulation"):
                        print(f"🔬 Simulation triggered at {new_state}")
                        global_metrics.record_simulation_trigger(new_state)
                    
                    # Track image loading
                    if metadata.get("image_url"):
                        print(f"🖼️  Image loaded at {new_state}")
                        global_metrics.record_image_load(new_state, metadata.get("image_node"))
                    
                    # Track video loading
                    if metadata.get("video_url"):
                        print(f"🎥 Video loaded at {new_state}")
                        global_metrics.record_video_load(new_state, metadata.get("video_node"))
                    
                    # Track misconceptions
                    if metadata.get("misconception_detected"):
                        print(f"⚠️  Misconception detected at {new_state}")
                        global_metrics.record_misconception(new_state)
                    
                    # Track quiz scores
                    quiz_score = metadata.get("quiz_score", -1.0)
                    if quiz_score >= 0:
                        global_metrics.record_quiz_score(quiz_score)
                    
                    # Track node transitions from metadata
                    node_transitions = metadata.get("node_transitions", [])
                    for transition in node_transitions:
                        global_metrics.record_graph_transition(
                            transition.get("from_node"),
                            transition.get("to_node"),
                            transition.get("transition_after_message_index")
                        )
                    
                    response.success()
                    
                    # End session if we reach END state
                    if new_state == "END":
                        self.session_active = False
                        global_metrics.record_session_completion(self.thread_id, self.turn_count)
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
        if self.thread_id:
            # Optionally delete session (comment out if you want to preserve sessions)
            # self.client.delete(f"/session/{self.thread_id}")
            pass
