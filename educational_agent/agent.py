import json
from pprint import pprint
from educational_agent.nodes import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node,
    end_node, AgentState
)

class EducationalAgent:
    def __init__(self):
        """
        Initializes the agent's state and node mapping.
        """
        self.state: AgentState = {
            "current_state": "START",
            "last_user_msg": "",
            "history": [],
            "definition_echoed": False,
            "misconception_detected": False,
            "retrieval_score": 0.0,
            "transfer_success": False,
            "session_summary": {},
        }
        self.node_map = {
            "START": start_node,
            "APK": apk_node,
            "CI": ci_node,
            "GE": ge_node,
            "MH": mh_node,
            "AR": ar_node,
            "TC": tc_node,
            "RLC": rlc_node,
            "END": end_node,
        }

    def start(self) -> str:
        """
        Starts the agent, gets the initial message, and records it in the history.
        """
        node_name = self.state["current_state"]
        fn = self.node_map[node_name]
        self.state = fn(self.state)
        # Append initial agent message to history
        self.state["history"].append({
            "role": "assistant",
            "node": node_name,
            "content": self.state["agent_output"]
        })
        return self.state["agent_output"]

    def post(self, user_msg: str) -> str:
        """
        Processes a user message, updates state, and returns the agent's response.
        """
        self.state["last_user_msg"] = user_msg
        self.state["history"].append({
            "role": "user",
            "content": user_msg
        })

        node_name = self.state["current_state"]
        fn = self.node_map[node_name]
        self.state = fn(self.state)

        self.state["history"].append({
            "role": "assistant",
            "node": node_name,
            "content": self.state["agent_output"]
        })

        if self.state["current_state"] == "END":
            # This call populates the session_summary dictionary
            self.state = end_node(self.state)
            self.state["history"].append({
                "role": "assistant",
                "node": "END",
                "content": self.state["agent_output"]
            })
            # The file saving and printing logic has been moved to run_test.py

        return self.state["agent_output"]
