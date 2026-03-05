import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from tester_agent.personas import Persona
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from langchain_groq import ChatGroq

class TesterAgent:
    def __init__(self, persona: Persona, is_kannada: bool = False):
        self.persona = persona
        self.is_kannada = is_kannada
        self.llm = ChatGoogleGenerativeAI(
            model="gemma-3-27b-it",
            api_key=os.getenv("GOOGLE_API_KEY_2"),
            temperature=0.7,
        )
    
        # self.llm = ChatGroq(
        # model="llama-3.3-70b-versatile",
        # temperature=0.5,
        # max_tokens=None,
    # )
        self.history = [
            SystemMessage(content=self._build_system_prompt())
        ]

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the tester persona based on current language setting."""
        base_prompt = (
            f"You are a student with the persona of a '{self.persona.name}'. "
            f"Your characteristics are: {self.persona.description}. "
            f"You must consistently act according to this persona."
        )
        if self.is_kannada:
            base_prompt += (
                " You are a student of Kannada origin and understand only Kannada. "
                "You must respond ONLY in Kannada language. "
                "All your responses must be in Kannada script, not English."
            )
        else:
            base_prompt += (
                " You must respond ONLY in English. "
                "All your responses must be in English, not Kannada or any other language."
            )
        return base_prompt

    def set_language(self, is_kannada: bool) -> None:
        """Switch the tester agent's response language mid-session.

        Updates is_kannada and replaces the SystemMessage in history so that
        all subsequent responses use the new language instruction.
        """
        if self.is_kannada == is_kannada:
            return  # No change needed
        self.is_kannada = is_kannada
        new_system_prompt = self._build_system_prompt()
        # Replace the first SystemMessage in history (always index 0)
        if self.history and isinstance(self.history[0], SystemMessage):
            self.history[0] = SystemMessage(content=new_system_prompt)
        else:
            self.history.insert(0, SystemMessage(content=new_system_prompt))
        lang = "Kannada" if is_kannada else "English"
        print(f"🔄 TesterAgent language switched to: {lang}")

    def respond(self, agent_msg: str) -> str:
        # Add the educational agent's latest message to the history
        self.history.append(AIMessage(content=agent_msg))

        formatted_history = self.history

        base_prompt = f"""
{formatted_history}

Your task is to provide the next response as the "User", staying true to your persona.
Your response should be on a single line.

User: """
        
        if self.is_kannada:
            base_prompt += (
                " You are a student of Kannada origin and understand only Kannada. "
                "You must respond ONLY in Kannada language. "
                "All your responses must be in Kannada script, not English."
            )
        else:
            base_prompt += (
                " You must respond ONLY in English. "
                "All your responses must be in English, not Kannada or any other language."
            )

        # Generate response using the context-rich prompt
        response = self.llm.invoke(base_prompt)
        user_response = response.content.strip()

        # Add your own response to the history
        self.history.append(HumanMessage(content=user_response))

        return user_response

    def respond_with_simulation_context(self, agent_msg: str, simulation_description: str) -> str:
        """
        Respond to the agent message with additional context about a visual simulation.
        This method provides the tester agent with textual description of what's happening
        in the simulation so it can respond appropriately.
        """
        # Add the educational agent's latest message to the history
        self.history.append(AIMessage(content=agent_msg))

        formatted_history = self.history

        prompt = f"""
{formatted_history}

{simulation_description}

Your task is to provide the next response as the "User", staying true to your persona.
Based on the simulation description provided above, respond as if you can see and observe what's happening in the simulation.
Your response should acknowledge or comment on the simulation if relevant.

User: """

        if self.is_kannada:
            prompt += (
                " You are a student of Kannada origin and understand only Kannada. "
                "You must respond ONLY in Kannada language. "
                "All your responses must be in Kannada script, not English."
            )
        else:
            prompt += (
                " You must respond ONLY in English. "
                "All your responses must be in English, not Kannada or any other language."
            )

        # Generate response using the context-rich prompt with simulation context
        response = self.llm.invoke(prompt)
        user_response = response.content.strip()

        # Add your own response to the history
        self.history.append(HumanMessage(content=user_response))

        return user_response