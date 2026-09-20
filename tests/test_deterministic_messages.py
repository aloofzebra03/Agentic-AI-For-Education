import unittest
from unittest.mock import patch

from langchain_core.messages import AIMessage, SystemMessage

from educational_agent_optimized_langsmith_v5 import (
    main_nodes_simulation_agent_no_mh as education_nodes,
)
from revision_agent import nodes as revision_nodes
from simulation_to_concept.nodes import teacher as simulation_teacher


class EducationStartNodeTests(unittest.TestCase):
    def test_english_greeting_is_deterministic(self):
        state = {
            "concept_title": "Photosynthesis",
            "is_kannada": False,
            "messages": [],
        }

        with patch.object(education_nodes, "llm_with_history") as llm:
            result = education_nodes.start_node(state)

        llm.assert_not_called()
        self.assertEqual(
            result["agent_output"],
            "Hello! Today we'll learn about Photosynthesis. Are you ready to begin?",
        )
        self.assertEqual(result["current_state"], "APK")
        self.assertEqual(result["summary"], "")
        self.assertEqual(result["summary_last_index"], -1)
        self.assertEqual(len(result["messages"]), 1)
        self.assertIsInstance(result["messages"][0], SystemMessage)

    def test_kannada_greeting_translates_only_concept(self):
        state = {
            "concept_title": "Photosynthesis",
            "is_kannada": True,
            "messages": [],
        }

        with (
            patch.object(education_nodes, "llm_with_history") as llm,
            patch.object(
                education_nodes,
                "translate_to_kannada_google",
                return_value="ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ",
            ) as translate,
        ):
            result = education_nodes.start_node(state)

        llm.assert_not_called()
        translate.assert_called_once_with("Photosynthesis")
        self.assertEqual(
            result["agent_output"],
            "ನಮಸ್ಕಾರ! ಇಂದು ನಾವು ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ ಬಗ್ಗೆ ಕಲಿಯೋಣ. ಪ್ರಾರಂಭಿಸಲು ಸಿದ್ಧರಿದ್ದೀರಾ?",
        )

    def test_kannada_translation_errors_propagate(self):
        state = {"concept_title": "Photosynthesis", "is_kannada": True}

        with patch.object(
            education_nodes,
            "translate_to_kannada_google",
            side_effect=RuntimeError("translation unavailable"),
        ):
            with self.assertRaisesRegex(RuntimeError, "translation unavailable"):
                education_nodes.start_node(state)


class RevisionNodeTests(unittest.TestCase):
    question_bank = {
        "chapter": "Nutrition in Plants",
        "questions": [
            {"id": "q1", "question": "What is photosynthesis?"},
            {"id": "q2", "question": "Why do plants need sunlight?"},
        ],
    }

    def test_english_start_greeting_is_deterministic(self):
        state = {
            "chapter": "Nutrition in Plants",
            "is_kannada": False,
            "messages": [],
        }

        with (
            patch.object(revision_nodes, "load_question_bank", return_value=self.question_bank),
            patch.object(revision_nodes, "llm_with_history") as llm,
        ):
            result = revision_nodes.revision_start_node(state)

        llm.assert_not_called()
        self.assertEqual(
            result["agent_output"],
            "Hello! We'll revise Nutrition in Plants using 2 questions. "
            "If you need help, I'll explain the concept before we continue. Are you ready?",
        )
        self.assertEqual(result["current_state"], "QUESTION_PRESENTER")
        self.assertEqual(result["questions_total"], 2)
        self.assertEqual(result["current_question_index"], 0)
        self.assertEqual(len(result["messages"]), 1)
        self.assertIsInstance(result["messages"][0], AIMessage)

    def test_kannada_start_translates_chapter(self):
        state = {
            "chapter": "Nutrition in Plants",
            "is_kannada": True,
            "messages": [],
        }

        with (
            patch.object(revision_nodes, "load_question_bank", return_value=self.question_bank),
            patch.object(revision_nodes, "llm_with_history") as llm,
            patch.object(
                revision_nodes,
                "translate_to_kannada_google",
                return_value="ಸಸ್ಯಗಳಲ್ಲಿ ಪೋಷಣೆ",
            ) as translate,
        ):
            result = revision_nodes.revision_start_node(state)

        llm.assert_not_called()
        translate.assert_called_once_with("Nutrition in Plants")
        self.assertEqual(
            result["agent_output"],
            "ನಮಸ್ಕಾರ! ನಾವು ಸಸ್ಯಗಳಲ್ಲಿ ಪೋಷಣೆ ಅಧ್ಯಾಯವನ್ನು 2 ಪ್ರಶ್ನೆಗಳ ಮೂಲಕ ಪುನರವಲೋಕನ "
            "ಮಾಡೋಣ. ನಿಮಗೆ ಸಹಾಯ ಬೇಕಾದರೆ, ಮುಂದುವರಿಯುವ ಮೊದಲು ನಾನು ಪರಿಕಲ್ಪನೆಯನ್ನು "
            "ವಿವರಿಸುತ್ತೇನೆ. ನೀವು ಸಿದ್ಧರಿದ್ದೀರಾ?",
        )

    def test_english_question_presentation_is_exact(self):
        state = {
            "question_bank": self.question_bank["questions"],
            "current_question_index": 0,
            "questions_total": 2,
            "is_kannada": False,
            "messages": [],
        }

        with patch.object(revision_nodes, "llm_with_history") as llm:
            result = revision_nodes.question_presenter_node(state)

        llm.assert_not_called()
        self.assertEqual(
            result["agent_output"],
            "Question 1 of 2: What is photosynthesis?",
        )
        self.assertEqual(result["current_state"], "EVALUATOR")
        self.assertEqual(result["current_question"], self.question_bank["questions"][0])
        self.assertIsInstance(result["messages"][-1], AIMessage)

    def test_kannada_question_translates_exact_question(self):
        state = {
            "question_bank": self.question_bank["questions"],
            "current_question_index": 1,
            "questions_total": 2,
            "is_kannada": True,
            "messages": [],
        }

        with (
            patch.object(revision_nodes, "llm_with_history") as llm,
            patch.object(
                revision_nodes,
                "translate_to_kannada_google",
                return_value="ಸಸ್ಯಗಳಿಗೆ ಸೂರ್ಯನ ಬೆಳಕು ಏಕೆ ಬೇಕು?",
            ) as translate,
        ):
            result = revision_nodes.question_presenter_node(state)

        llm.assert_not_called()
        translate.assert_called_once_with("Why do plants need sunlight?")
        self.assertEqual(
            result["agent_output"],
            "ಪ್ರಶ್ನೆ 2/2: ಸಸ್ಯಗಳಿಗೆ ಸೂರ್ಯನ ಬೆಳಕು ಏಕೆ ಬೇಕು?",
        )
        self.assertEqual(result["current_state"], "EVALUATOR")


class SimulationStartMessageTests(unittest.TestCase):
    def test_first_teacher_message_does_not_call_llm(self):
        simulation_config = {
            "title": "Simple Pendulum",
            "description": "Explore pendulum motion.",
            "cannot_demonstrate": [],
            "parameter_info": {
                "length": {"label": "Length", "range": "1-10", "effect": "speed"}
            },
        }
        state = {
            "simulation_id": "simple_pendulum",
            "concepts": [{
                "id": 1,
                "title": "Pendulum Motion",
                "description": "Observe how it swings.",
                "key_insight": "Length changes the period.",
                "related_params": ["length"],
            }],
            "current_concept_index": 0,
            "conversation_history": [],
            "student_response": "",
            "understanding_level": "none",
            "exchange_count": 0,
            "current_params": {"length": 5},
            "parameter_history": [],
            "language": "english",
        }

        with (
            patch.object(simulation_teacher, "get_simulation", return_value=simulation_config),
            patch.object(simulation_teacher, "get_llm_with_key") as get_llm,
            patch.object(simulation_teacher, "invoke_llm_with_prompts") as invoke_llm,
        ):
            result = simulation_teacher.teacher_node(state, {})

        get_llm.assert_not_called()
        invoke_llm.assert_not_called()
        self.assertEqual(
            result["last_teacher_message"],
            "Hello! Let's explore Simple Pendulum with this interactive simulation. "
            "We'll begin with Pendulum Motion. Observe the simulation: what do you notice?",
        )
        self.assertEqual(result["exchange_count"], 1)
        self.assertTrue(result["waiting_for_input"])
        self.assertTrue(result["show_simulation"])
        self.assertEqual(result["last_displayed_params"], {"length": 5})
        self.assertEqual(len(result["conversation_history"]), 1)
        self.assertEqual(result["conversation_history"][0]["role"], "teacher")
        self.assertEqual(result["parameter_history"][0]["parameter"], "length")


if __name__ == "__main__":
    unittest.main()
