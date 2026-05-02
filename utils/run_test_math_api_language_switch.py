import json
import os
import time
from datetime import datetime
from pprint import pprint
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from tester_agent.personas import personas
from tester_agent.tester import TesterAgent


load_dotenv(dotenv_path=".env", override=True)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
PAUSE_AFTER_TURNS = int(os.getenv("MATH_TEST_LANGUAGE_PAUSE_TURNS", "3"))
MAX_TURNS = int(os.getenv("MATH_TEST_MAX_TURNS", "25"))
TURN_DELAY_SECONDS = float(os.getenv("MATH_TEST_TURN_DELAY_SECONDS", "2"))


def _first_configured_api_key() -> Optional[str]:
    api_key = os.getenv("TEST_API_KEY") or os.getenv("LOAD_TEST_API_KEY")
    if api_key:
        return api_key.strip().strip("'").strip('"')

    api_keys = os.getenv("X_API_KEYS", "")
    if api_keys:
        return api_keys.split(",")[0].strip().strip("'").strip('"')
    return None


class MathAgentAPIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        api_key = _first_configured_api_key()
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})

    def health_check(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def list_problems(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/math/problems")
        response.raise_for_status()
        return response.json()

    def start_session(
        self,
        problem_id: str,
        student_id: str,
        is_kannada: bool = False,
    ) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/math/session/start",
            json={
                "problem_id": problem_id,
                "student_id": student_id,
                "session_label": "math-api-test",
                "is_kannada": is_kannada,
            },
        )
        response.raise_for_status()
        return response.json()

    def continue_session(
        self,
        thread_id: str,
        user_message: str,
        is_kannada: Optional[bool] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, str] = {
            "thread_id": thread_id,
            "user_message": user_message,
        }
        if is_kannada is not None:
            data["is_kannada"] = str(is_kannada).lower()

        response = self.session.post(
            f"{self.base_url}/math/session/continue",
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def get_status(self, thread_id: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/math/session/status/{thread_id}")
        response.raise_for_status()
        return response.json()

    def get_history(self, thread_id: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/math/session/history/{thread_id}")
        response.raise_for_status()
        return response.json()


def lang_label(is_kannada: bool) -> str:
    return "Kannada" if is_kannada else "English"


def choose_language(current_is_kannada: bool) -> bool:
    print(f"\nCurrent language: {lang_label(current_is_kannada)}")
    print("1. English")
    print("2. Kannada")
    choice = input("Choose language for upcoming turns, or press Enter to keep current: ").strip()
    if choice == "1":
        return False
    if choice == "2":
        return True
    return current_is_kannada


def choose_persona():
    print("\nSelect a tester persona:")
    for idx, persona in enumerate(personas, 1):
        print(f"{idx}. {persona.name} - {persona.description}")
    selected = int(input("Enter persona number: ").strip()) - 1
    return personas[selected]


def choose_problem(problems: List[Dict[str, Any]]) -> str:
    print("\nSelect a math problem:")
    for idx, problem in enumerate(problems, 1):
        difficulty = problem.get("difficulty") or "unknown"
        print(f"{idx}. {problem['problem_id']} [{difficulty}] - {problem.get('topic', '')}")

    default_problem = problems[0]["problem_id"]
    choice = input(f"Enter problem number, or press Enter for {default_problem}: ").strip()
    if choice and choice.isdigit():
        selected = int(choice) - 1
        if 0 <= selected < len(problems):
            return problems[selected]["problem_id"]
    return default_problem


def run_test_math_api_language_switch():
    client = MathAgentAPIClient()

    try:
        health = client.health_check()
        print(f"API status: {health.get('status')}")
    except requests.exceptions.RequestException as exc:
        print(f"Cannot connect to API at {API_BASE_URL}")
        print("Start it with: python -m uvicorn api_servers.api_server_v5:app --host 0.0.0.0 --port 8000")
        print(f"Error: {exc}")
        return

    try:
        problems_response = client.list_problems()
    except requests.exceptions.RequestException as exc:
        print("Could not load /math/problems. Check API auth and problem catalog.")
        print(f"Error: {exc}")
        return

    problems = problems_response.get("problems", [])
    if not problems:
        print("No math problems returned by /math/problems.")
        return

    persona = choose_persona()
    problem_id = choose_problem(problems)

    print("\nStarting language:")
    print("1. English")
    print("2. Kannada")
    is_kannada = input("Enter language number (default 1): ").strip() == "2"
    language_path = "kannada" if is_kannada else "english"

    pause_input = input(f"Pause for language switch every N turns (default {PAUSE_AFTER_TURNS}): ").strip()
    pause_after = int(pause_input) if pause_input.isdigit() else PAUSE_AFTER_TURNS

    tester_agent = TesterAgent(persona, is_kannada=is_kannada)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    student_id = f"math-api-{persona.name.lower().replace(' ', '-')}-{timestamp}"

    try:
        start_response = client.start_session(
            problem_id=problem_id,
            student_id=student_id,
            is_kannada=is_kannada,
        )
    except requests.exceptions.RequestException as exc:
        print(f"Error starting math session: {exc}")
        return

    thread_id = start_response.get("thread_id")
    session_id = start_response.get("session_id")
    agent_msg = start_response.get("agent_response", "")
    current_state = start_response.get("current_state", "START")

    print("\nMath session started")
    print(f"Thread ID: {thread_id}")
    print(f"Problem ID: {problem_id}")
    print(f"State: {current_state}")
    print(f"Agent: {agent_msg}")

    turn_count = 0
    continue_response: Dict[str, Any] = {}

    while current_state != "END" and turn_count < MAX_TURNS:
        turn_count += 1
        print(f"\n--- Turn {turn_count} | {lang_label(is_kannada)} ---")

        if pause_after > 0 and turn_count % pause_after == 0:
            new_is_kannada = choose_language(is_kannada)
            if new_is_kannada != is_kannada:
                is_kannada = new_is_kannada
                tester_agent.set_language(is_kannada)
                language_path += f"_to_{'kannada' if is_kannada else 'english'}"
                print(f"Switched to {lang_label(is_kannada)}")

        user_msg = tester_agent.respond(agent_msg)
        print(f"Tester ({persona.name}): {user_msg}")

        if TURN_DELAY_SECONDS > 0:
            time.sleep(TURN_DELAY_SECONDS)

        try:
            continue_response = client.continue_session(
                thread_id=thread_id,
                user_message=user_msg,
                is_kannada=is_kannada,
            )
        except requests.exceptions.RequestException as exc:
            print(f"Error continuing math session: {exc}")
            break

        agent_msg = continue_response.get("agent_response", "")
        current_state = continue_response.get("current_state", "UNKNOWN")
        print(f"Agent: {agent_msg}")
        print(f"State: {current_state}")

    try:
        status_response = client.get_status(thread_id)
    except requests.exceptions.RequestException:
        status_response = {}

    try:
        history_response = client.get_history(thread_id)
    except requests.exceptions.RequestException:
        history_response = {}

    report = {
        "api_test": True,
        "agent": "math",
        "persona": persona.model_dump(),
        "problem_id": problem_id,
        "thread_id": thread_id,
        "session_id": session_id,
        "language_path": language_path,
        "turn_count": turn_count,
        "final_state": current_state,
        "start_response": start_response,
        "last_continue_response": continue_response,
        "status": status_response,
        "history": history_response.get("messages", []),
    }

    os.makedirs("test_reports", exist_ok=True)
    report_path = os.path.join(
        "test_reports",
        f"math_api_evaluation_{student_id}_{language_path}.json",
    )
    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\nTest completed")
    print(f"Final state: {current_state}")
    print(f"Turns: {turn_count}")
    print(f"Report: {report_path}")
    if status_response:
        pprint(status_response.get("progress", {}))


if __name__ == "__main__":
    run_test_math_api_language_switch()
