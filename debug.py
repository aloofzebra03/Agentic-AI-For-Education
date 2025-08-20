from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from educational_agent.graph_fuse import build_graph
from langgraph.types import Command 
from uuid import uuid4

def main():
    graph = build_graph()
    config = {"configurable": {"thread_id": str(uuid4())}}
    print("Interactive debug (interrupt-aware). Type 'exit' to quit.\n")


    user = input("You: ").strip()
    input_delta = {"messages": [HumanMessage(content=user)]}
    
    resp = graph.invoke(input_delta, config=config)
    response = resp.get("agent_output", "")
    state = resp.get("current_state", {})
    print(f"Agent: {response}")
    print(f"Current State: {state}")


    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        input_delta = {"messages": [HumanMessage(content=user)]}

        # seen_msg_ids = set()
        # print("Reached Here")
        resp = graph.invoke(Command(resume = True), config=config)
        response = resp.get("agent_output", "")
        state = resp.get("current_state", {})
        print(f"Agent: {response}")
        print(f"Current State: {state}")
        # for state in graph.stream(input_delta, config=config, stream_mode="values"):
        #     print(state)
        #     # state is a dict snapshot of the graph state
        #     # Example keys you showed: messages, current_state, last_user_msg, agent_output, history
        #     # Print state transitions / debug:
        #     cs = state.get("current_state")
        #     print(f"[state] current_state={cs!r}")

        #     # Print any NEW messages that we haven't seen yet
        #     # msgs = state.get("messages", [])
        #     # for m in msgs:
        #     #     mid = getattr(m, "id", None)
        #     #     if mid not in seen_msg_ids:
        #     #         seen_msg_ids.add(mid)
        #     #         role = "assistant" if m.__class__.__name__.startswith("AIMessage") else "user"
        #     #         print(f"[{role}] {getattr(m, 'content', m)}")

        #     # If your nodes write a convenience field with the latest model output:
        #     if "agent_output" in state:
        #         print("[agent_output]", state["agent_output"])

        #     # If you want to see the compact history you’re constructing:
        #     # if "history" in state:
        #     #     # history is your own list of dicts; print the last entry
        #     #     if state["history"]:
        #     #         last = state["history"][-1]
        #     #         print("[history+=]", last)


if __name__ == "__main__":
    main()
