import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from tester_agent.personas import Persona

class Evaluator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
        )

    def evaluate(self, persona: Persona, history: list) -> str:
        """
        Evaluates the conversation and provides feedback.
        """
        prompt = f"""
You are an expert in evaluating educational conversations.
Your task is to analyze the following conversation between an educational agent and a student with the persona of a "{persona.name}".

**Persona Description:** {persona.description}

**Conversation History:**
{json.dumps(history, indent=2)}

**Evaluation Metrics:**
- **Adaptability:** How well did the agent adapt to the student's persona? (1-5)
- **Pedagogical Flow:** Did the conversation follow a logical and effective teaching structure? (1-5)
- **Clarity & Conciseness:** Were the agent's explanations easy to understand? (1-5)
- **Error Handling:** How did the agent handle unexpected or incorrect student inputs? (1-5)

**Feedback:**
- **Strengths:** What did the agent do well?
- **Areas for Improvement:** What could the agent do better?
- **Bugs/Issues:** Were there any bugs or issues with the agent's responses?

**Output Format:**
Please provide your evaluation in JSON format.Give me the json object directly WITHOUT any additional text like ```json in the beginning etc.
I want to run the function json.loads on your output directly.

"""
        response = self.llm.invoke(prompt)
        return response.content