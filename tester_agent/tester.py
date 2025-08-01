import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from tester_agent.personas import Persona

class TesterAgent:
    def __init__(self, persona: Persona):
        self.persona = persona
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            # api_key=os.getenv("GOOGLE_API_KEY"),
            api_key='AIzaSyBQwzJ2LniqqvhULi3vOL1Zy9nRaEPzYhw',
            temperature=0.7,
        )
        # Initialize history with the persona's description as a system prompt
        self.history = [
            {"role": "system", "content": f"You are a student with the persona of a '{self.persona.name}'. Your characteristics are: {self.persona.description}. You must consistently act according to this persona."}
        ]

    def respond(self, agent_msg: str) -> str:
        """
        Generates a response to the educational agent's message based on the persona
        and the full conversation history.
        """
        # Add the educational agent's latest message to the history
        self.history.append({"role": "assistant", "content": agent_msg})

        # Format the history for the prompt
        # We can pass the structured history directly to some models,
        # but for clarity in a text-based prompt, we format it.
        formatted_history = "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in self.history])

        prompt = f"""
{formatted_history}

Your task is to provide the next response as the "User", staying true to your persona.
Your response should be on a single line.

User: """

        # Generate response using the context-rich prompt
        response = self.llm.invoke(prompt)
        user_response = response.content.strip()

        # Add your own response to the history
        self.history.append({"role": "user", "content": user_response})

        return user_response