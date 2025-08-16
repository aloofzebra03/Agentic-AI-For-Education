from typing import Any, Dict
from langchain_core.messages import HumanMessage, AIMessage
from educational_agent import graph_fuse


class EducationalAgent:
    def __init__(self):
        self.graph = graph_fuse.graph
        self.state: Dict[str, Any] = {}

    def start(self) -> str:

        events = self.graph.stream(
            {"messages": []},  # initial empty state
            stream_mode="values"
        )
        for ev in events:
            self.state = ev
        return self.state.get("agent_output", "")

    def post(self, user_msg: str) -> str:

        human_message = HumanMessage(content=user_msg)
        events = self.graph.stream(
            {"messages": [human_message]},
            stream_mode="values",
            config={"configurable": {"thread_id": "test-thread"}}
        )
        for ev in events:
            self.state = ev
        return self.state.get("agent_output", "")
