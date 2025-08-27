from __future__ import annotations

from datetime import datetime
from typing import Optional, Dict, Any

from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

from langgraph.types import Command

# Import the graph factory that returns a compiled graph WITHOUT callbacks baked in
from educational_agent.graph_fuse import build_graph


class EducationalAgent:
    def __init__(
        self,
        session_label: Optional[str] = None,
        user_id: Optional[str] = None,
        persona_name: Optional[str] = None,
    ):
        
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Prefer explicit session label; otherwise use persona; otherwise "tester"
        base = session_label or persona_name or "tester"
        self.base = base
        self.persona_name = persona_name

        # Public identifiers (handy in Langfuse UI)
        self.session_id = f"{base}-{ts}"
        self.thread_id = f"{base}-thread-{ts}"
        self.user_id = user_id or "local-tester"

        # Metadata for the parent run in Langfuse (recognized by the Langfuse LC handler)
        tags = [self.base, "educational-agent"]
        if self.persona_name:
            tags.append(f"persona:{self.persona_name}")

        self._metadata: Dict[str, Any] = {
            "langfuse_session_id": self.session_id,
            "langfuse_user_id": self.user_id,
            "langfuse_tags": tags,
            "run_started_at": ts,
        }

        base_graph = build_graph()

        # Create a FRESH Langfuse handler per run and attach it + metadata at the graph level
        langfuse_handler = LangfuseCallbackHandler()
        self.graph = base_graph.with_config({
            "callbacks": [langfuse_handler],
            "metadata": self._metadata,
        })

        # Optional local state slot if you need to stash anything custom
        self.state: Dict[str, Any] = {}

    def start(self) -> str:
        final_text = ""
        last_state: Dict[str, Any] = {}
        # events = self.graph.stream(
        #     {"messages": [HumanMessage(content="__start__")],
        #      "history": self.state.get("history", [])},  # seed for Gemini
        #     stream_mode="values",
        #     config={"configurable": {"thread_id": self.thread_id}},
        # )
        # for state in events:
        #     if isinstance(state, dict):
        #         last_state = state
        #         if state.get("agent_output"):
        #             final_text = state["agent_output"]
        
        result = self.graph.invoke(
            {"messages": [HumanMessage(content="__start__")],
             "history": self.state.get("history", [])},  # seed for Gemini
            config={"configurable": {"thread_id": self.thread_id}},
        )
        if isinstance(result, dict):
            last_state = result
            if result.get("agent_output"):
                final_text = result["agent_output"]

        if last_state:
            self.state = last_state

        return final_text
    
    def post(self, user_text: str) -> str:
        final_text = ""
        last_state: Dict[str, Any] = {}
        
        cmd = Command(
            resume=True,
            update={
                "messages": [HumanMessage(content=user_text)],
                # "last_user_msg": user_text,
                "history": [{"role": "user", "content": user_text}]
            },
        )

        # events = self.graph.stream(
        #     cmd,
        #     stream_mode="values",
        #     config={"configurable": {"thread_id": self.thread_id}},
        # )
        # for state in events:
        #     if isinstance(state, dict):
        #         last_state = state
        #         if state.get("agent_output"):
        #             final_text = state["agent_output"]
        #         else:
        #             try:
        #                 msgs = state.get("messages") or []
        #                 if msgs and getattr(msgs[-1], "type", None) == "ai":
        #                     final_text = getattr(msgs[-1], "content", final_text) or final_text
        #             except Exception:
        #                 pass

        result = self.graph.invoke(
            cmd,
            config={"configurable": {"thread_id": self.thread_id}},
        )
        if isinstance(result, dict):
            last_state = result
            if result.get("agent_output"):
                final_text = result["agent_output"]
            else:
                try:
                    msgs = result.get("messages") or []
                    if msgs and getattr(msgs[-1], "type", None) == "ai":
                        final_text = getattr(msgs[-1], "content", final_text) or final_text
                except Exception:
                    pass

        # <-- persist full state
        if last_state:
            self.state = last_state

        return final_text
    
    def current_state(self) -> str:
        return self.state.get("current_state", "")


    def session_info(self) -> Dict[str, str]:
        return {
            "session_id": self.session_id,
            "thread_id": self.thread_id,
            "user_id": self.user_id,
            "tags": ", ".join(self._metadata.get("langfuse_tags", [])),
        }
