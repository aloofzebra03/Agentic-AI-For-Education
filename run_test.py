import os
import json
import time
from pprint import pprint

from educational_agent.agent import EducationalAgent
from tester_agent.tester import TesterAgent
from tester_agent.evaluator import Evaluator
from tester_agent.personas import personas
from tester_agent.session_metrics import compute_and_upload_session_metrics
from dotenv import load_dotenv

load_dotenv(dotenv_path = r"C:\Users\aryan\Desktop\Personalized_Education\Agentic-AI-For-Education\tester_agent\.env", override=True)

def run_test():
    # 1. Select Persona
    print("Select a persona to test:")
    for i, p in enumerate(personas):
        print(f"{i+1}. {p.name}")
    persona_idx = int(input("Enter persona number: ")) - 1
    persona = personas[persona_idx]

    # 2. Initialize Agents
    educational_agent = EducationalAgent(persona_name=persona.name)
    tester_agent = TesterAgent(persona)

    # 3. Start Conversation
    agent_msg = educational_agent.start()
    print(f"Educational Agent: {agent_msg}")

    # 4. Run Conversation Loop
    while educational_agent.current_state() != "END":

        user_msg = tester_agent.respond(agent_msg)
        print(f"Tester Agent ({persona.name}): {user_msg}")
        time.sleep(5)
        agent_msg = educational_agent.post(user_msg)
        print(f"Educational Agent: {agent_msg}")
        # print("#########" + educational_agent.current_state())

    # Save and print the session summary after the loop
    session_summary = educational_agent.state.get("session_summary", {})

    print("\nSession Summary:")
    pprint(session_summary)

    # Save the session summary using the Langfuse session ID
    session_id = educational_agent.session_id
    summary_filename = f"session_summary_{session_id}.json"
    os.makedirs("reports", exist_ok=True)
    summary_path = os.path.join("reports", summary_filename)
    with open(summary_path, "w") as f:
        json.dump(session_summary, f, indent=2)
    print(f"\nSession summary exported to {summary_path}")

    # 5. Compute and Upload Session Metrics to Langfuse
    print("\n📊 Computing session metrics...")
    try:
        # Convert messages to history format for metrics
        history_for_reports = educational_agent.get_history_for_reports()
        
        session_metrics = compute_and_upload_session_metrics(
            session_id=session_id,
            history=history_for_reports,
            session_state=educational_agent.state,
            persona_name=persona.name
        )

        # Save metrics locally as well
        metrics_filename = f"session_metrics_{session_id}.json"
        metrics_path = os.path.join("reports", metrics_filename)
        with open(metrics_path, "w") as f:
            json.dump(session_metrics.model_dump(), f, indent=2)
        print(f"📋 Session metrics saved to {metrics_path}")
    
    except Exception as e:
        print(f"❌ Error: Failed to compute session metrics: {e}")
        import traceback
        traceback.print_exc()
        print("⚠️ Continuing without metrics...")
        session_metrics = None

    # 6. Evaluate Educational Quality (Pedagogical Assessment)
    evaluator = Evaluator()
    # Convert messages to history format for evaluation
    history_for_reports = educational_agent.get_history_for_reports()
    evaluation = evaluator.evaluate(persona, history_for_reports)
    print("\n--- Educational Quality Evaluation ---")
    print(evaluation)

    clean_str = evaluation.strip()
    if clean_str.startswith("```json"):
        clean_str = clean_str[7:]
    if clean_str.endswith("```"):
        clean_str = clean_str[:-3]
    clean_str = clean_str.strip()

    # 7. Save Comprehensive Report
    report = {
        "persona": persona.model_dump(),
        "educational_evaluation": json.loads(clean_str),  # Pedagogical quality assessment
        "history": history_for_reports,  # Use the converted history
    }
    
    # Include quantitative metrics in the report if available
    if session_metrics:
        report["session_metrics"] = session_metrics.model_dump()
    # Use the Langfuse session ID for the evaluation report filename
    session_id = educational_agent.session_id
    report_path = f"reports/evaluation_{session_id}.json"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nEvaluation report saved to {report_path}")

if __name__ == "__main__":
    run_test()