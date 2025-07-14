# main.py
from pprint import pprint
from agent.nodes4 import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node,
    end_node, AgentState
)

def main():
    state: AgentState = {
        "current_state":       "START",
        "last_user_msg":       "",
        "history":             [],    # now holds dicts with 'role' & 'content'
        "definition_echoed":   False,
        "misconception_detected": False,
        "retrieval_score":     0.0,
        "transfer_success":    False,
        "session_summary":     {},
    }

    node_map = {
        "START": start_node,
        "APK":   apk_node,
        "CI":    ci_node,
        "GE":    ge_node,
        "MH":    mh_node,
        "AR":    ar_node,
        "TC":    tc_node,
        "RLC":   rlc_node,
        "END":   end_node,
    }

    while True:
        fn = node_map[state["current_state"]]
        state = fn(state)
        print("\nAgent:", state["agent_output"])

        # append assistant’s turn
        state["history"].append({
            "role":    "assistant",
            "content": state["agent_output"]
        })

        if state["current_state"] == "END":
            break

        # read learner’s reply
        user_msg = input("You: ")
        state["last_user_msg"] = user_msg

        # append user’s turn
        state["history"].append({
            "role":    "user",
            "content": user_msg
        })

    print("\nSession Summary:")
    pprint(state["session_summary"])


if __name__ == "__main__":
    main()
