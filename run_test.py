import os
import json
import time
from pprint import pprint
import re # We'll use this for better string cleaning

from educational_agent.agent import EducationalAgent
from tester_agent.tester import TesterAgent
from tester_agent.evaluator import Evaluator
from tester_agent.personas import personas
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\aryan\Desktop\Personalized_Education\Agentic-AI-For-Education\tester_agent\.env", override=True)

def run_test():
    # 1. Select Persona
    print("Select a persona to test:")
    for i, p in enumerate(personas):
        print(f"{i+1}. {p.name}")
    persona_idx = int(input("Enter persona number: ")) - 1
    persona = personas[persona_idx]

    # 2. Initialize Agents
    educational_agent = EducationalAgent()
    tester_agent = TesterAgent(persona)

    # 3. Start Conversation
    agent_msg = educational_agent.start()
    print(f"Educational Agent: {agent_msg}")

    # 4. Run Conversation Loop
    while educational_agent.state["current_state"] != "END":
        user_msg = tester_agent.respond(agent_msg)
        print(f"Tester Agent ({persona.name}): {user_msg}")
        time.sleep(5)
        agent_msg = educational_agent.post(user_msg)
        print(f"Educational Agent: {agent_msg}")

    # Save and print the session summary after the loop
    session_summary = educational_agent.state.get("session_summary", {})

    print("\nSession Summary:")
    pprint(session_summary)

    # Save the session summary to a persona-specific file
    summary_filename = f"session_summary_{persona.name.lower().replace(' ', '_')}.json"
    os.makedirs("reports", exist_ok=True)
    summary_path = os.path.join("reports", summary_filename)
    with open(summary_path, "w") as f:
        json.dump(session_summary, f, indent=2)
    print(f"\nSession summary exported to {summary_path}")

    # 5. Evaluate Conversation
    evaluator = Evaluator()
    evaluation = evaluator.evaluate(persona, educational_agent.state["history"])
    print("\n--- Evaluation ---")
    print(evaluation)

    clean_str = evaluation.strip()
    
    # Use regular expressions for more robust code block extraction
    match = re.search(r'```json(.*?)```', clean_str, re.DOTALL)
    if match:
        clean_str = match.group(1).strip()
    
    # Handle the JSON parsing with a try-except block
    try:
        evaluation_data = json.loads(clean_str)
        print("\nJSON parsing successful!")
    except json.decoder.JSONDecodeError as e:
        print(f"\nERROR: Failed to parse JSON evaluation.")
        print(f"JSONDecodeError: {e}")
        print("\nAttempting to handle common JSON issues...")
        # Add common fixes here
        # Example: remove trailing commas in lists/dictionaries
        fixed_str = re.sub(r',\s*([}\]])', r'\1', clean_str, flags=re.MULTILINE)
        try:
            evaluation_data = json.loads(fixed_str)
            print("Successfully parsed JSON after fixing trailing commas.")
        except json.decoder.JSONDecodeError as e_fixed:
            print(f"ERROR: Failed to parse even after fixing. The error is likely more complex.")
            print(f"Final JSONDecodeError: {e_fixed}")
            print("Saving raw string to debug.")
            evaluation_data = {"error": str(e_fixed), "raw_evaluation_string": clean_str}

    # 6. Save Report
    report = {
        "persona": persona.model_dump(),
        "evaluation": evaluation_data, # Use the parsed data here
        "history": educational_agent.state["history"],
    }
    report_path = f"reports/evaluation_{persona.name.lower().replace(' ', '_')}.json"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nEvaluation report saved to {report_path}")

if __name__ == "__main__":
    run_test()