"""
Test Suite: Translation + API Integration
==========================================

Tests are split into two sections:

SECTION 1 — Translation Unit Tests
    No server or API key required. Always runnable.
    Run with: pytest test_translation_api.py -v -m "not live_api"

SECTION 2 — Live API Integration Tests
    Requires the API server to be running AND valid Gemini API keys.
    Start server first: uvicorn api_server:app --reload --port 8000
    Run with: pytest test_translation_api.py -v -m live_api

Run everything:
    pytest test_translation_api.py -v

Run only translation unit tests (safe, no keys needed):
    pytest test_translation_api.py -v -m "not live_api"
"""

import time
import pytest
import re
import requests
from typing import Dict, Any

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

API_BASE_URL = "http://localhost:8000"
TEST_SIMULATION_ID = "simple_pendulum"  # Change if needed


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def contains_kannada(text: str) -> bool:
    """Check if text contains Kannada Unicode characters (U+0C80–U+0CFF)."""
    return bool(re.search(r'[\u0C80-\u0CFF]', text))


def is_pure_english(text: str) -> bool:
    """Check that text has no Kannada characters."""
    return not contains_kannada(text)


def start_session(language: str = "english", simulation_id: str = TEST_SIMULATION_ID) -> Dict[str, Any]:
    """Helper: start a session via API and return JSON response."""
    resp = requests.post(
        f"{API_BASE_URL}/api/session/start",
        json={"simulation_id": simulation_id, "language": language},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()


def send_response(session_id: str, student_response: str) -> Dict[str, Any]:
    """Helper: send a student response via API."""
    resp = requests.post(
        f"{API_BASE_URL}/api/session/{session_id}/respond",
        json={"student_response": student_response},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()


def get_session(session_id: str) -> Dict[str, Any]:
    """Helper: fetch session state via API."""
    resp = requests.get(
        f"{API_BASE_URL}/api/session/{session_id}",
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: TRANSLATION UNIT TESTS
# (No server or API key required)
# ═══════════════════════════════════════════════════════════════════════

class TestTranslationCore:
    """Tests for the translation.py module — no server or API key needed."""

    def test_translate_english_to_kannada(self):
        """English text should be translated to Kannada characters."""
        from translation import translate_to_kannada
        result = translate_to_kannada("Hello! Today we will learn about pendulums.")
        assert contains_kannada(result), f"Expected Kannada output, got: {result}"

    def test_translate_kannada_to_english(self):
        """Kannada text should be translated back to English."""
        from translation import translate_to_kannada, translate_to_english
        kannada = translate_to_kannada("The length of the pendulum affects its speed.")
        result = translate_to_english(kannada)
        assert is_pure_english(result), f"Expected English output, got: {result}"
        # Round-trip should preserve rough meaning
        assert len(result) > 5, "Translation returned empty/too short text"

    def test_translate_empty_string(self):
        """Empty string should be returned as-is (no API call)."""
        from translation import translate_to_kannada
        result = translate_to_kannada("")
        assert result == "", f"Expected empty string, got: {result}"

    def test_translate_whitespace_only(self):
        """Whitespace-only string should be returned as-is."""
        from translation import translate_to_kannada
        result = translate_to_kannada("   ")
        assert result.strip() == "", f"Expected whitespace, got: '{result}'"

    def test_translation_caching(self):
        """Second call with same text should use cache (verify via timing)."""
        from translation import translate_to_kannada, _translation_cache, clear_cache
        clear_cache()
        text = "The pendulum swings back and forth."

        # First call — hits Google Translate
        t1 = time.time()
        result1 = translate_to_kannada(text)
        duration1 = time.time() - t1

        # Second call — should hit cache (~instant)
        t2 = time.time()
        result2 = translate_to_kannada(text)
        duration2 = time.time() - t2

        assert result1 == result2, "Cached result differs from original"
        # Cache should be at least 10x faster
        assert duration2 < duration1 * 0.1 or duration2 < 0.01, \
            f"Cache not working: first={duration1:.3f}s, second={duration2:.3f}s"

    def test_cache_stores_entry(self):
        """Translation cache should store the result."""
        from translation import translate_to_kannada, _translation_cache, clear_cache, get_cache_stats
        clear_cache()
        assert get_cache_stats()["cached_translations"] == 0
        translate_to_kannada("Time is measured in seconds.")
        assert get_cache_stats()["cached_translations"] >= 1

    def test_needs_translation_english(self):
        """English should not need translation."""
        from translation import needs_translation
        assert needs_translation("english") is False
        assert needs_translation("English") is False
        assert needs_translation("ENGLISH") is False

    def test_needs_translation_kannada(self):
        """Kannada should need translation."""
        from translation import needs_translation
        assert needs_translation("kannada") is True
        assert needs_translation("Kannada") is True

    def test_is_supported_language(self):
        """Only 'english' and 'kannada' should be supported."""
        from translation import is_supported_language
        assert is_supported_language("english") is True
        assert is_supported_language("kannada") is True
        assert is_supported_language("hindi") is False
        assert is_supported_language("french") is False
        assert is_supported_language("") is False

    def test_get_language_code(self):
        """Language codes should map correctly."""
        from translation import get_language_code
        assert get_language_code("english") == "en"
        assert get_language_code("kannada") == "kn"

    def test_get_language_code_invalid(self):
        """Invalid language should raise ValueError."""
        from translation import get_language_code
        with pytest.raises(ValueError, match="Unsupported language"):
            get_language_code("telugu")

    def test_batch_translation(self):
        """Batch should translate all strings and return in same order."""
        from translation import translate_batch
        texts = [
            "length",
            "time period",
            "oscillation"
        ]
        results = translate_batch(texts, source="en", target="kn")
        assert len(results) == len(texts), "Batch returned wrong number of results"
        for r in results:
            assert contains_kannada(r), f"Expected Kannada in: {r}"

    def test_batch_same_lang_passthrough(self):
        """Batch with source==target should return input unchanged."""
        from translation import translate_batch
        texts = ["hello", "world"]
        results = translate_batch(texts, source="en", target="en")
        assert results == texts

    def test_student_input_translation(self):
        """Kannada student input should be translated to English."""
        from translation import translate_student_input, translate_to_kannada
        # Convert something to Kannada first, then feed it back
        kannada_input = translate_to_kannada("I think the pendulum swings faster")
        result = translate_student_input(kannada_input, "kannada")
        assert is_pure_english(result), f"Expected English student input, got: {result}"

    def test_student_input_english_passthrough(self):
        """English student input should pass through unchanged."""
        from translation import translate_student_input
        text = "I think the pendulum swings faster"
        result = translate_student_input(text, "english")
        assert result == text, f"English input was modified: {result}"


class TestTranslateApiResponse:
    """Tests for translate_api_response() — verifies correct fields are translated."""

    def _make_mock_session_response(self) -> Dict[str, Any]:
        """Build a mock session response dict."""
        return {
            "session_id": "test_session_123",
            "simulation": {
                "id": "simple_pendulum",
                "title": "Time & Pendulums",
                "html_url": "https://example.com/sim.html?length=5",
                "current_params": {"length": 5.0},
                "param_change": {
                    "parameter": "length",
                    "before": 3.0,
                    "after": 5.0,
                    "reason": "Longer pendulum to demonstrate slower swing"
                }
            },
            "concepts": {
                "total": 2,
                "current_index": 0,
                "current_concept": {
                    "id": 1,
                    "title": "Time Period of a Pendulum",
                    "description": "How length affects swing time",
                    "key_insight": "Longer pendulum means slower swings",
                    "related_params": ["length"]
                },
                "all_concepts": [
                    {
                        "id": 1,
                        "title": "Time Period of a Pendulum",
                        "description": "How length affects swing time",
                        "key_insight": "Longer pendulum means slower swings",
                        "related_params": ["length"]
                    },
                    {
                        "id": 2,
                        "title": "Measuring Time with Oscillations",
                        "description": "Multiple oscillations reduce error",
                        "key_insight": "More oscillations = more accurate measurement",
                        "related_params": ["number_of_oscillations"]
                    }
                ],
                "all_completed": False,
                "previous_concept": None
            },
            "teacher_message": {
                "text": "Hi friend! Today we are going to explore how pendulums work.",
                "timestamp": "2026-03-07T10:00:00Z",
                "requires_response": True
            },
            "learning_state": {
                "understanding_level": "none",
                "exchange_count": 0,
                "concept_complete": False,
                "session_complete": False,
                "strategy": "continue",
                "teacher_mode": "encouraging"
            }
        }

    def test_teacher_message_translated_to_kannada(self):
        """teacher_message.text must be in Kannada."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        assert contains_kannada(translated["teacher_message"]["text"]), \
            f"Teacher message not in Kannada: {translated['teacher_message']['text']}"

    def test_simulation_title_translated(self):
        """simulation.title must be in Kannada."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        assert contains_kannada(translated["simulation"]["title"]), \
            f"Simulation title not in Kannada: {translated['simulation']['title']}"

    def test_current_concept_fields_translated(self):
        """current_concept title, description, key_insight all translated."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        concept = translated["concepts"]["current_concept"]
        assert contains_kannada(concept["title"]), f"Concept title not translated: {concept['title']}"
        assert contains_kannada(concept["description"]), f"Concept description not translated: {concept['description']}"
        assert contains_kannada(concept["key_insight"]), f"Concept key_insight not translated: {concept['key_insight']}"

    def test_all_concepts_list_translated(self):
        """Every concept in all_concepts list must be translated."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        for concept in translated["concepts"]["all_concepts"]:
            assert contains_kannada(concept["title"]), \
                f"all_concepts title not translated: {concept['title']}"

    def test_param_change_reason_translated(self):
        """param_change.reason must be translated."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        reason = translated["simulation"]["param_change"]["reason"]
        assert contains_kannada(reason), f"Param change reason not translated: {reason}"

    def test_language_field_added(self):
        """Response should have language field set to 'kannada'."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        assert translated.get("language") == "kannada"

    def test_english_passthrough_no_translation(self):
        """English responses should pass through unchanged."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        original_text = resp["teacher_message"]["text"]
        translated = translate_api_response(resp, "english")
        assert translated["teacher_message"]["text"] == original_text, \
            "English text was modified when it shouldn't be"

    def test_non_translatable_fields_preserved(self):
        """IDs, URLs, params, timestamps must NOT be translated."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        translated = translate_api_response(resp, "kannada")
        assert translated["session_id"] == "test_session_123", "session_id was modified"
        assert translated["simulation"]["id"] == "simple_pendulum", "simulation.id was modified"
        assert "https://example.com" in translated["simulation"]["html_url"], "URL was modified"
        assert translated["simulation"]["current_params"] == {"length": 5.0}, "Params were modified"
        assert translated["teacher_message"]["timestamp"] == "2026-03-07T10:00:00Z", "Timestamp was modified"

    def test_no_param_change_handled_gracefully(self):
        """Response with no param_change should not crash."""
        from translation import translate_api_response
        resp = self._make_mock_session_response()
        resp["simulation"]["param_change"] = None
        translated = translate_api_response(resp, "kannada")
        assert translated["simulation"]["param_change"] is None


class TestTranslateQuizResponse:
    """Tests for translate_quiz_response()."""

    def _make_mock_quiz_response(self) -> Dict[str, Any]:
        return {
            "session_id": "test_session_123",
            "question_id": "pendulum_q1",
            "score": 0.5,
            "status": "PARTIALLY_RIGHT",
            "feedback": "Good try! The length is close, but try increasing it a bit more to slow down the pendulum.",
            "attempt": 2,
            "allow_retry": True,
            "quiz_complete": False,
            "quiz_progress": {
                "current_question": 1,
                "total_questions": 2,
                "questions_completed": 0,
                "questions_remaining": 2,
                "average_score": 0.0,
                "perfect_count": 0,
                "partial_count": 0,
                "wrong_count": 0
            },
            "next_question": {
                "id": "pendulum_q2",
                "challenge": "Can you make the pendulum oscillate exactly 10 times in 20 seconds?"
            }
        }

    def test_feedback_translated(self):
        """Quiz feedback text should be in Kannada."""
        from translation import translate_quiz_response
        resp = self._make_mock_quiz_response()
        translated = translate_quiz_response(resp, "kannada")
        assert contains_kannada(translated["feedback"]), \
            f"Feedback not in Kannada: {translated['feedback']}"

    def test_next_question_challenge_translated(self):
        """next_question.challenge should be in Kannada."""
        from translation import translate_quiz_response
        resp = self._make_mock_quiz_response()
        translated = translate_quiz_response(resp, "kannada")
        assert contains_kannada(translated["next_question"]["challenge"]), \
            f"Challenge not in Kannada: {translated['next_question']['challenge']}"

    def test_scores_not_modified(self):
        """Numeric scores and status strings should not be altered."""
        from translation import translate_quiz_response
        resp = self._make_mock_quiz_response()
        translated = translate_quiz_response(resp, "kannada")
        assert translated["score"] == 0.5
        assert translated["status"] == "PARTIALLY_RIGHT"
        assert translated["attempt"] == 2
        assert translated["allow_retry"] is True
        assert translated["quiz_complete"] is False

    def test_english_quiz_passthrough(self):
        """English quiz response should not be translated."""
        from translation import translate_quiz_response
        resp = self._make_mock_quiz_response()
        original_feedback = resp["feedback"]
        translated = translate_quiz_response(resp, "english")
        assert translated["feedback"] == original_feedback

    def test_no_next_question_handled(self):
        """Quiz response without next_question should not crash."""
        from translation import translate_quiz_response
        resp = self._make_mock_quiz_response()
        resp["next_question"] = None
        translated = translate_quiz_response(resp, "kannada")
        assert translated["next_question"] is None


class TestStateAndModels:
    """Tests for state.py and api_models.py language field additions."""

    def test_create_initial_state_with_kannada(self):
        """State should store 'kannada' language."""
        from state import create_initial_state
        state = create_initial_state("test topic", {"length": 5}, "simple_pendulum", language="kannada")
        assert state["language"] == "kannada"

    def test_create_initial_state_default_english(self):
        """Default language should be 'english' when not specified."""
        from state import create_initial_state
        state = create_initial_state("test topic", {"length": 5}, "simple_pendulum")
        assert state["language"] == "english"

    def test_start_session_request_with_language(self):
        """StartSessionRequest should accept and store language field."""
        from api_models import StartSessionRequest
        req = StartSessionRequest(simulation_id="simple_pendulum", language="kannada")
        assert req.language == "kannada"

    def test_start_session_request_default_language(self):
        """StartSessionRequest should default language to 'english'."""
        from api_models import StartSessionRequest
        req = StartSessionRequest(simulation_id="simple_pendulum")
        assert req.language == "english"

    def test_session_response_has_language_field(self):
        """SessionResponse model should have a language field."""
        from api_models import SessionResponse
        fields = SessionResponse.model_fields
        assert "language" in fields, "SessionResponse missing 'language' field"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: LIVE API INTEGRATION TESTS
# (Requires running server: uvicorn api_server:app --reload --port 8000)
# (Requires valid Gemini API keys in .env)
# ═══════════════════════════════════════════════════════════════════════

def is_api_running() -> bool:
    """Check if the API server is running."""
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


@pytest.mark.live_api
class TestLiveApiEnglish:
    """Live API tests for English sessions. Requires running server + valid API keys."""

    @pytest.fixture(autouse=True)
    def check_server(self):
        if not is_api_running():
            pytest.skip("API server not running. Start with: uvicorn api_server:app --reload --port 8000")

    def test_health_check(self):
        """Server health check should return 'online'."""
        resp = requests.get(f"{API_BASE_URL}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "online"

    def test_start_session_english_returns_english_message(self):
        """English session should return teacher message in English."""
        data = start_session(language="english")
        text = data["teacher_message"]["text"]
        assert is_pure_english(text), f"Teacher message has Kannada in English session: {text}"

    def test_start_session_has_language_field(self):
        """Response should include language field."""
        data = start_session(language="english")
        assert data.get("language") == "english"

    def test_start_session_returns_session_id(self):
        """Session ID should be returned."""
        data = start_session(language="english")
        assert "session_id" in data and data["session_id"]

    def test_start_session_returns_concepts(self):
        """Session should include concepts."""
        data = start_session(language="english")
        assert data["concepts"]["total"] > 0

    def test_respond_english_session(self):
        """Sending English response to English session should return English reply."""
        data = start_session(language="english")
        session_id = data["session_id"]
        response = send_response(session_id, "I think the pendulum swings faster when it's shorter.")
        text = response["teacher_message"]["text"]
        assert is_pure_english(text), f"English session reply has Kannada: {text}"

    def test_get_session_state(self):
        """GET /api/session/{id} should return current state."""
        data = start_session(language="english")
        session_id = data["session_id"]
        info = get_session(session_id)
        assert info["session_id"] == session_id


@pytest.mark.live_api
class TestLiveApiKannada:
    """Live API tests for Kannada sessions. Requires running server + valid API keys."""

    @pytest.fixture(autouse=True)
    def check_server(self):
        if not is_api_running():
            pytest.skip("API server not running. Start with: uvicorn api_server:app --reload --port 8000")

    def test_start_session_kannada_returns_kannada_message(self):
        """Kannada session should return teacher message with Kannada characters."""
        data = start_session(language="kannada")
        text = data["teacher_message"]["text"]
        assert contains_kannada(text), \
            f"Teacher message in Kannada session has no Kannada characters: {text}"

    def test_start_session_kannada_has_language_field(self):
        """Response should indicate language as 'kannada'."""
        data = start_session(language="kannada")
        assert data.get("language") == "kannada"

    def test_start_session_kannada_concept_title_translated(self):
        """Current concept title should be in Kannada."""
        data = start_session(language="kannada")
        concept = data["concepts"]["current_concept"]
        if concept:
            assert contains_kannada(concept["title"]), \
                f"Concept title not in Kannada: {concept['title']}"

    def test_start_session_kannada_simulation_title_translated(self):
        """Simulation title should be in Kannada."""
        data = start_session(language="kannada")
        title = data["simulation"]["title"]
        assert contains_kannada(title), f"Simulation title not in Kannada: {title}"

    def test_kannada_student_input_processed_correctly(self):
        """Sending Kannada input should be understood and replied to in Kannada."""
        from translation import translate_to_kannada
        data = start_session(language="kannada")
        session_id = data["session_id"]

        # Translate a typical student answer to Kannada and send it
        kannada_input = translate_to_kannada("I think the pendulum swings slower when it is longer.")
        response = send_response(session_id, kannada_input)
        text = response["teacher_message"]["text"]

        # Reply should be in Kannada
        assert contains_kannada(text), \
            f"Reply to Kannada input has no Kannada characters: {text}"

    def test_english_input_in_kannada_session(self):
        """Sending English input to a Kannada session should still get Kannada reply."""
        data = start_session(language="kannada")
        session_id = data["session_id"]
        response = send_response(session_id, "I think the length affects the time period.")
        text = response["teacher_message"]["text"]
        assert contains_kannada(text), \
            f"English input to Kannada session did not return Kannada reply: {text}"

    def test_language_persists_across_exchanges(self):
        """Language should remain Kannada through multiple exchanges."""
        data = start_session(language="kannada")
        session_id = data["session_id"]

        for i, student_text in enumerate([
            "I see the pendulum is swinging.",
            "I think the length makes it slower.",
        ]):
            response = send_response(session_id, student_text)
            text = response["teacher_message"]["text"]
            assert contains_kannada(text), \
                f"Exchange {i+1}: Kannada not in teacher reply: {text}"

    def test_get_session_returns_language(self):
        """GET /api/session/{id} should return language field for Kannada session."""
        data = start_session(language="kannada")
        session_id = data["session_id"]
        info = get_session(session_id)
        # Language field is set by translate_api_response
        assert info.get("language") == "kannada"

    def test_kannada_and_english_sessions_independent(self):
        """Two simultaneous sessions (one each) should operate independently."""
        en_data = start_session(language="english")
        kn_data = start_session(language="kannada")

        en_text = en_data["teacher_message"]["text"]
        kn_text = kn_data["teacher_message"]["text"]

        assert is_pure_english(en_text), f"English session has Kannada: {en_text}"
        assert contains_kannada(kn_text), f"Kannada session has no Kannada: {kn_text}"

    def test_invalid_session_id_responds(self):
        """Non-existent session ID — LangGraph creates a new thread, so 200 is expected.
        
        LangGraph's PostgresSaver does not raise KeyError for unknown thread IDs;
        it creates a new empty thread and processes the input. Therefore 200,
        not 404, is the correct response here.
        """
        resp = requests.post(
            f"{API_BASE_URL}/api/session/fake_session_xyz/respond",
            json={"student_response": "hello"},
            timeout=60
        )
        # LangGraph creates a new thread for unknown session IDs → 200
        assert resp.status_code == 200, \
            f"Expected 200 (new thread created by LangGraph), got: {resp.status_code}"

    def test_invalid_language_defaults_gracefully(self):
        """Unsupported language should either reject or fallback gracefully."""
        resp = requests.post(
            f"{API_BASE_URL}/api/session/start",
            json={"simulation_id": TEST_SIMULATION_ID, "language": "telugu"},
            timeout=60
        )
        # Either 400 (validation error) or 201 with English fallback — both acceptable
        assert resp.status_code in (201, 400), \
            f"Unexpected status for unsupported language: {resp.status_code}"
