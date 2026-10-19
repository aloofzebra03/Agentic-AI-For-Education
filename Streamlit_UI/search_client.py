"""Small HTTP client for search and the existing education API endpoints."""

from urllib.parse import urlsplit

import requests


class ApiError(RuntimeError):
    pass


class EducationApi:
    def __init__(self, base_url, api_key):
        url = urlsplit(base_url)
        if url.scheme not in {"http", "https"} or not url.netloc or url.username or url.password or url.query or url.fragment:
            raise ApiError("Set EDUCATION_API_BASE_URL to an HTTP(S) API URL without credentials or query parameters.")
        if not api_key:
            raise ApiError("Set EDUCATION_API_KEY in Streamlit secrets or the environment.")
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key

    def request(self, method, path, **kwargs):
        try:
            response = requests.request(
                method, self.base_url + path, headers={"X-API-Key": self._api_key},
                timeout=(5, 120 if method == "POST" else 15), **kwargs,
            )
        except requests.Timeout as error:
            raise ApiError("The API timed out. The lesson may have advanced; do not automatically resend your message.") from error
        except requests.RequestException as error:
            raise ApiError("Cannot connect to the education API. Check its address and that the server is running.") from error
        messages = {
            401: "API authentication failed. Check EDUCATION_API_KEY.",
            403: "You do not have access to this resource or session.",
            404: "Endpoint or content not found. Check that the backend includes /search and the selected lesson.",
            409: "The session is busy or complete. Wait, or start a new lesson.",
            422: "The request is invalid. Search must be at most 300 characters; doubt questions at most 4000.",
            429: "Your daily request allowance is exhausted. Try again after the reset.",
            501: "The model's per-minute allowance is exhausted. Please wait and try again.",
            502: "The model's per-day allowance is exhausted. Try again after the reset.",
        }
        if not response.ok:
            raise ApiError(messages.get(response.status_code, f"The API could not complete this request (HTTP {response.status_code})."))
        try:
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("Expected an object")
            return data
        except ValueError as error:
            raise ApiError("The API returned an unexpected response format.") from error

    def search(self, query="", subject="auto", mode="auto", randomize=False):
        params = {"q": query, "limit": 5, "random": randomize}
        if subject != "auto":
            params["subject"] = subject
        if mode != "auto":
            params["mode"] = mode
        return self.request("GET", "/search", params=params)

    def start(self, action, title):
        if action["type"] == "whiteboard":
            kind, path, body = "whiteboard", "/whiteboard-tutor/session/start", {"concept_id": action["concept_id"]}
        elif action["type"] == "tutor" and action.get("problem_id"):
            kind, path, body = "math", "/math/session/start", {"problem_id": action["problem_id"]}
        elif action["type"] == "tutor" and action.get("concept_title"):
            kind, path, body = "science", "/session/start", {"concept_title": action["concept_title"]}
        else:
            raise ApiError("This learning action is not supported.")
        data = self.request("POST", path, json=body)
        if not data.get("thread_id"):
            raise ApiError("The API did not return a session ID.")
        return {"kind": kind, "title": title, "thread_id": data["thread_id"],
                "turn": normalize_turn(data, kind)}

    def continue_lesson(self, lesson, message):
        body = {"thread_id": lesson["thread_id"], "user_message": message}
        kind = lesson["kind"]
        path = {"science": "/session/continue", "math": "/math/session/continue",
                "whiteboard": "/whiteboard-tutor/session/continue"}[kind]
        # Maths continuation uses form data; the other routes use JSON.
        data = self.request("POST", path, **({"data": body} if kind == "math" else {"json": body}))
        return normalize_turn(data, kind)

    def doubt(self, question, context=""):
        answer = self.request("POST", "/doubts", json={"question": question, "context": context}).get("answer")
        if not isinstance(answer, str) or not answer.strip():
            raise ApiError("The API did not return a doubt explanation.")
        return answer


def normalize_turn(data, kind):
    turn = data.get("turn") if kind == "whiteboard" else data
    if not isinstance(turn, dict):
        raise ApiError("The API did not return a tutor turn.")
    message = turn.get("message") if kind == "whiteboard" else turn.get("agent_response")
    if not isinstance(message, str):
        raise ApiError("The API did not return tutor text.")
    return {
        "message": message,
        "current_state": turn.get("current_state", ""),
        "whiteboard_state": turn.get("whiteboard_state", {}),
        "whiteboard_patch": turn.get("whiteboard_patch", {}),
        "metadata": turn.get("metadata") or {},
    }
