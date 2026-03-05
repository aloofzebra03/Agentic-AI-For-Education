"""
run_test_api_language_switch.py

A test script for exercising the Kannada ↔ English language-switch use case.

Differences from run_test_api.py:
  • After PAUSE_AFTER_TURNS turns the script PAUSES and asks the tester to
    choose a language for the rest of the session.
  • The chosen language is sent on every subsequent /session/continue call so
    the agent state stays in sync.
  • Report filenames encode the full switch path, e.g. "kannada→english".

Usage:
    python -m utils.run_test_api_language_switch
"""

import sys
import os

# Ensure THIS repo's root is always first in sys.path so that local packages
# (tester_agent, utils, etc.) are imported instead of identically-named packages
# from sibling projects on the Python path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
import requests
from pprint import pprint
from typing import Optional, Dict, Any

from tester_agent.tester import TesterAgent
from tester_agent.evaluator import Evaluator
from tester_agent.personas import personas
from tester_agent.session_metrics import compute_and_upload_session_metrics
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)
if os.getenv("POSTGRES_DATABASE_URL "):
    print("✅ Loaded environment variables from .env file")

if os.getenv("LANGCHAIN_API_KEY"):
    print(f"✅ LangSmith tracing configured for project: {os.environ['LANGCHAIN_PROJECT']}")
    print(f"🔗 LangSmith endpoint: {os.environ['LANGCHAIN_ENDPOINT']}")
    try:
        from langsmith import Client
        client = Client()
        print("✅ LangSmith client connection successful")
    except Exception as e:
        print(f"❌ LangSmith connection test failed: {e}")
else:
    print("❌ Warning: LANGCHAIN_API_KEY not found. LangSmith tracing will not work.")


# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8000"  # Change if your API is hosted elsewhere

# After this many turns the script will pause and ask for a language choice.
# Change this constant to control when the pause happens.
PAUSE_AFTER_TURNS = 3


# ============================================================================
# API CLIENT
# ============================================================================

class EducationalAgentAPIClient:
    """Client for interacting with the Educational Agent API (language-switch aware)."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def start_session(
        self,
        concept_title: str,
        persona_name: str,
        session_label: Optional[str] = None,
        is_kannada: bool = False,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/session/start"
        payload = {
            "concept_title": concept_title,
            "persona_name": persona_name,
            "session_label": session_label,
            "is_kannada": is_kannada,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def continue_session(
        self,
        thread_id: str,
        user_message: str,
        is_kannada: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Continue a session, optionally updating the language flag.

        Args:
            thread_id: Session thread ID.
            user_message: Student message to send.
            is_kannada: If not None, updates is_kannada in agent state this turn.
        """
        url = f"{self.base_url}/session/continue"
        payload: Dict[str, Any] = {
            "thread_id": thread_id,
            "user_message": user_message,
        }
        if is_kannada is not None:
            payload["is_kannada"] = is_kannada
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_session_status(self, thread_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/session/status/{thread_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_session_history(self, thread_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/session/history/{thread_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_session_summary(self, thread_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/session/summary/{thread_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def delete_session(self, thread_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/session/{thread_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict[str, Any]:
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_concepts(self) -> Dict[str, Any]:
        url = f"{self.base_url}/concepts"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


# ============================================================================
# HELPERS
# ============================================================================

def format_simulation_from_metadata(metadata: Dict[str, Any]) -> Optional[str]:
    if not metadata.get("show_simulation", False):
        return None
    simulation_config = metadata.get("simulation_config", {})
    if not simulation_config:
        return None
    sim_type = simulation_config.get("type", "unknown")
    parameters = simulation_config.get("parameters", {})
    agent_message = simulation_config.get("agent_message", "")
    description = f"Simulation Type: {sim_type}\n"
    description += f"Parameters: {json.dumps(parameters, indent=2)}\n"
    if agent_message:
        description += f"Agent Message: {agent_message}\n"
    return description


def lang_label(is_kannada: bool) -> str:
    return "Kannada (ಕನ್ನಡ)" if is_kannada else "English"


def language_switch_prompt(current_is_kannada: bool) -> bool:
    """Ask the tester to choose a language; return the new is_kannada value."""
    print("\n" + "=" * 80)
    print("⏸️   — Choose the language for the rest of the session")
    print("=" * 80)
    print(f"   Current language : {lang_label(current_is_kannada)}")
    print()
    print("   1. English")
    print("   2. Kannada (ಕನ್ನಡ)")
    print()
    choice = input("   Enter 1 or 2 (or press Enter to keep current): ").strip()
    if choice == "1":
        return False
    elif choice == "2":
        return True
    else:
        print(f"   ↩️  Keeping current language: {lang_label(current_is_kannada)}")
        return current_is_kannada


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_test_api_language_switch():

    # ── Health check ─────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("🏥 Checking API Health...")
    print("=" * 80)

    api_client = EducationalAgentAPIClient()

    try:
        health = api_client.health_check()
        print(f"✅ API Status  : {health.get('status')}")
        print(f"📦 Agent Type  : {health.get('agent_type')}")
        print(f"💾 Persistence : {health.get('persistence')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API at {API_BASE_URL}")
        print(f"   Start the server first:  uvicorn api_servers.api_server_v5:app --host 0.0.0.0 --port 8000")
        print(f"   Error: {e}")
        return

    # ── Select persona ────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("👤 Select a persona to test:")
    print("=" * 80)
    for i, p in enumerate(personas):
        print(f"  {i + 1}. {p.name} — {p.description}")

    persona_idx = int(input("\nEnter persona number: ")) - 1
    persona = personas[persona_idx]
    print(f"\n✅ Selected persona: {persona.name}")

    # ── Select concept ────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("📚 Select a concept to teach:")
    print("=" * 80)

    try:
        concepts_response = api_client.list_concepts()
        if concepts_response.get("success"):
            concepts = concepts_response.get("concepts", [])
            print(f"Found {len(concepts)} available concepts:\n")
            for i, concept in enumerate(concepts):
                print(f"  {i + 1}. {concept}")
            concept_choice = input(
                "\nEnter concept number (or press Enter for default 'Pendulum And Its Time Period'): "
            ).strip()
            if concept_choice and concept_choice.isdigit():
                concept_idx = int(concept_choice) - 1
                if 0 <= concept_idx < len(concepts):
                    concept_title = concepts[concept_idx]
                else:
                    print("Invalid choice, using default")
                    concept_title = "Pendulum And Its Time Period"
            else:
                concept_title = "Pendulum And Its Time Period"
        else:
            print("Could not retrieve concepts list, using default")
            concept_title = "Pendulum And Its Time Period"
    except Exception as e:
        print(f"Error retrieving concepts: {e}")
        concept_title = "Pendulum And Its Time Period"

    print(f"\n✅ Selected concept: {concept_title}")

    # ── Select starting language ──────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("🌐 Select STARTING language for the session:")
    print("=" * 80)
    print("  1. English (default)")
    print("  2. Kannada (ಕನ್ನಡ)")

    language_choice = input("\nEnter language number (default is 1): ").strip()
    is_kannada: bool = language_choice == "2"
    print(f"\n✅ Starting language: {lang_label(is_kannada)}")

    # Record the starting language for the report filename
    start_lang = "kannada" if is_kannada else "english"

    # ── Configure pause ───────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print(f"⏸️  Language-switch pause is configured every {PAUSE_AFTER_TURNS} turns.")
    custom = input(
        f"   Press Enter to keep that, or type a different interval (turns): "
    ).strip()
    pause_at = int(custom) if custom.isdigit() else PAUSE_AFTER_TURNS
    print(f"   Will pause every {pause_at} turn(s).")

    # ── Initialise tester agent ───────────────────────────────────────────────
    tester_agent = TesterAgent(persona, is_kannada=is_kannada)

    # ── Start session via API ─────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("🚀 Starting Session via API...")
    print("=" * 80)

    try:
        start_response = api_client.start_session(
            concept_title=concept_title,
            persona_name=persona.name,
            session_label=f"langswitch-{persona.name.lower().replace(' ', '-')}",
            is_kannada=is_kannada,
        )
    except requests.exceptions.RequestException as e:
        print(f"❌ Error starting session: {e}")
        return

    if not start_response.get("success"):
        print(f"❌ Failed to start session: {start_response.get('message')}")
        return

    thread_id = start_response.get("thread_id")
    session_id = start_response.get("session_id")
    agent_msg = start_response.get("agent_response")
    current_state = start_response.get("current_state")

    print(f"✅ Session started!")
    print(f"   Thread ID : {thread_id}")
    print(f"   Session ID: {session_id}")
    print(f"   State     : {current_state}")
    print(f"\n🤖 Educational Agent: {agent_msg}")

    # Track the language switch path for report naming
    # e.g. "english→kannada" or "kannada→english" or "english" (no switch)
    lang_switch_path = start_lang
    language_switched = False

    # ── Conversation loop ─────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("💬 Starting Conversation Loop...")
    print("=" * 80)

    turn_count = 0
    continue_response: Dict[str, Any] = {}

    while current_state != "END":
        turn_count += 1
        print(f"\n--- Turn {turn_count}  |  Language: {lang_label(is_kannada)} ---")

        # ── Language-switch pause ─────────────────────────────────────────────
        if turn_count % pause_at == 0:
            new_is_kannada = language_switch_prompt(is_kannada)
            if new_is_kannada != is_kannada:
                is_kannada = new_is_kannada
                tester_agent.set_language(is_kannada)  # properly rebuilds SystemMessage in history
                end_lang = "kannada" if is_kannada else "english"
                lang_switch_path = f"{start_lang}→{end_lang}"
                language_switched = True
                print(f"\n🔄 Language switched to: {lang_label(is_kannada)}")
                print(f"   Language path so far: {lang_switch_path}")
            else:
                print(f"\n   Continuing in: {lang_label(is_kannada)}")

        # ── Check metadata for simulation ─────────────────────────────────────
        metadata = start_response.get("metadata") if turn_count == 1 else continue_response.get("metadata")
        simulation_description = None
        if metadata and metadata.get("show_simulation", False):
            simulation_description = format_simulation_from_metadata(metadata)
            if simulation_description:
                print("\n" + "=" * 80)
                print("🔬 SIMULATION DESCRIPTION FOR TESTER AGENT")
                print("=" * 80)
                print(simulation_description)
                print("=" * 80 + "\n")

        # ── Get tester response ───────────────────────────────────────────────
        if simulation_description:
            if hasattr(tester_agent, "respond_with_simulation_context"):
                user_msg = tester_agent.respond_with_simulation_context(
                    agent_msg, simulation_description
                )
            else:
                enhanced_agent_msg = (
                    f"{agent_msg}\n\n[SIMULATION CONTEXT: {simulation_description[:200]}...]"
                )
                user_msg = tester_agent.respond(enhanced_agent_msg)
        else:
            user_msg = tester_agent.respond(agent_msg)

        print(f"👤 Tester Agent ({persona.name}): {user_msg}")

        # Add delay to avoid overwhelming the API
        time.sleep(15)

        # ── Continue session via API ──────────────────────────────────────────
        try:
            # Always pass is_kannada so the agent state is always up-to-date
            continue_response = api_client.continue_session(
                thread_id=thread_id,
                user_message=user_msg,
                is_kannada=is_kannada,
            )
        except requests.exceptions.RequestException as e:
            print(f"❌ Error continuing session: {e}")
            break

        if not continue_response.get("success"):
            print(f"❌ Failed to continue session: {continue_response.get('message')}")
            break

        agent_msg = continue_response.get("agent_response")
        current_state = continue_response.get("current_state")

        print(f"🤖 Educational Agent: {agent_msg}")
        print(f"📍 Current State: {current_state}")

    # ── Session summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("📊 Retrieving Session Summary...")
    print("=" * 80)

    try:
        summary_response = api_client.get_session_summary(thread_id)
        if summary_response.get("success") and summary_response.get("exists"):
            session_summary = summary_response.get("summary", {})
            print("\n📋 Session Summary:")
            if session_summary:
                pprint(session_summary)
            else:
                print("⚠️  Summary is empty (session may not have reached END yet)")
            os.makedirs("test_reports", exist_ok=True)
            summary_filename = f"session_summary_{session_id}_{lang_switch_path}_api.json"
            summary_path = os.path.join("test_reports", summary_filename)
            with open(summary_path, "w") as f:
                json.dump(session_summary, f, indent=2)
            print(f"✅ Session summary exported to {summary_path}")
        else:
            print("⚠️  No session summary available")
            session_summary = {}
    except requests.exceptions.RequestException as e:
        print(f"❌ Error retrieving session summary: {e}")
        session_summary = {}

    # ── Session history ───────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("📜 Retrieving Session History...")
    print("=" * 80)

    try:
        history_response = api_client.get_session_history(thread_id)
        if history_response.get("success") and history_response.get("exists"):
            history_for_reports = history_response.get("messages", [])
            print(f"✅ Retrieved {len(history_for_reports)} messages from history")
        else:
            print("⚠️  No history available")
            history_for_reports = []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error retrieving session history: {e}")
        history_for_reports = []

    # ── Compute session metrics ───────────────────────────────────────────────
    session_metrics = None
    if history_for_reports:
        print("\n" + "=" * 80)
        print("📊 Computing Session Metrics...")
        print("=" * 80)
        try:
            status_response = api_client.get_session_status(thread_id)
            session_state = (
                status_response.get("progress", {}) if status_response.get("success") else {}
            )
            session_metrics = compute_and_upload_session_metrics(
                session_id=session_id,
                history=history_for_reports,
                session_state=session_state,
                persona_name=persona.name,
            )
            os.makedirs("test_reports", exist_ok=True)
            metrics_filename = f"session_metrics_{session_id}_{lang_switch_path}_api.json"
            metrics_path = os.path.join("test_reports", metrics_filename)
            with open(metrics_path, "w") as f:
                json.dump(session_metrics.model_dump(), f, indent=2)
            print(f"✅ Session metrics saved to {metrics_path}")
        except Exception as e:
            print(f"❌ Error computing session metrics: {e}")
            import traceback
            traceback.print_exc()
            print("⚠️  Continuing without metrics...")

    # ── Educational quality evaluation ────────────────────────────────────────
    if history_for_reports:
        print("\n" + "=" * 80)
        print("🎓 Evaluating Educational Quality...")
        print("=" * 80)

        evaluator = Evaluator()
        evaluation = evaluator.evaluate(persona, history_for_reports)
        print("\n--- Educational Quality Evaluation ---")
        print(evaluation)

        clean_str = evaluation.strip()
        if clean_str.startswith("```json"):
            clean_str = clean_str[7:]
        if clean_str.endswith("```"):
            clean_str = clean_str[:-3]
        clean_str = clean_str.strip()

        report = {
            "persona": persona.model_dump(),
            "educational_evaluation": json.loads(clean_str),
            "history": history_for_reports,
            "thread_id": thread_id,
            "session_id": session_id,
            "language_path": lang_switch_path,
            "language_switched": language_switched,
            "switch_at_turn": pause_at if language_switched else None,
            "api_test": True,
        }
        if session_metrics:
            report["session_metrics"] = session_metrics.model_dump()

        os.makedirs("test_reports", exist_ok=True)
        report_path = f"test_reports/evaluation_{session_id}_{lang_switch_path}_api.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Evaluation report saved to {report_path}")
    else:
        print("\n⚠️  Skipping evaluation — no history available")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("✅ LANGUAGE-SWITCH TEST COMPLETED")
    print("=" * 80)
    print(f"  Session ID      : {session_id}")
    print(f"  Thread ID       : {thread_id}")
    print(f"  Persona         : {persona.name}")
    print(f"  Total Turns     : {turn_count}")
    print(f"  Final State     : {current_state}")
    print(f"  Language Path   : {lang_switch_path}")
    if language_switched:
        print(f"  Switch at Turn  : {pause_at}")
    print("=" * 80)

    # ── Optional: delete session ──────────────────────────────────────────────
    delete_choice = input("\n🗑️  Do you want to delete this session from the API? (y/n): ").strip().lower()
    if delete_choice == "y":
        try:
            delete_response = api_client.delete_session(thread_id)
            if delete_response.get("success"):
                print(f"✅ Session deleted: {delete_response.get('message')}")
            else:
                print(f"⚠️  Session deletion failed: {delete_response.get('message')}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error deleting session: {e}")


if __name__ == "__main__":
    run_test_api_language_switch()
