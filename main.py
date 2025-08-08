# main.py

import json
from pprint import pprint
from educational_agent.nodes import (
    start_node, apk_node, ci_node, ge_node,
    mh_node, ar_node, tc_node, rlc_node,
    end_node, AgentState
)

def main():
    state: AgentState = {
    "current_state": "START",
    "last_user_msg": "",
    "history": [],
    "definition_echoed": False,
    "misconception_detected": False,
    "retrieval_score": 0.0,
    "transfer_success": False,
    "session_summary": {},
    "_asked_apk": False,
    "_asked_ci": False,
    "_asked_ge": False,
    "_asked_mh": False,
    "_asked_ar": False,
    "_asked_tc": False,
    "_asked_rlc": False,
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
        # remember which node we're in
        node_name = state["current_state"]
        fn = node_map[node_name]

        state = fn(state)
        print(f"\nAgent [{node_name}]:", state["agent_output"])

        # record assistant turn with node tag
        state["history"].append({
            "role":    "assistant",
            "node":    node_name,
            "content": state["agent_output"]
        })

        # if END, generate full summary and break
        if state["current_state"] == "END":
            state = end_node(state)  # repopulate session_summary
            print(f"\nAgent [END]:", state["agent_output"])
            state["history"].append({
                "role":    "assistant",
                "node":    "END",
                "content": state["agent_output"]
            })
            break

        # otherwise prompt user
        user_msg = input("You: ")
        state["last_user_msg"] = user_msg
        state["history"].append({
            "role":    "user",
            "content": user_msg
        })

    # console output
    print("\nSession Summary:")
    pprint(state["session_summary"])

    # write out JSON
    with open("session_summary.json", "w") as f:
        json.dump(state["session_summary"], f, indent=2)
    print("\n Session summary exported to session_summary.json")


if __name__ == "__main__":
    main()
