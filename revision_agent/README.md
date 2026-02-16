# Revision Agent

Quick concept review agent for students preparing for exams.

## Overview

The revision agent helps students quickly review concepts before exams using predefined questions. It:

- Presents questions from a question bank
- Evaluates answers and provides immediate feedback
- Explains concepts if students struggle
- Asks followup questions to verify understanding
- Tracks progress and identifies weak areas

## Architecture

### Flow

```
START → REVISION_START → QUESTION_PRESENTER → EVALUATOR
                                ↓                ↓
                         [If correct]      [If incorrect]
                                ↓                ↓
                        Next Question           GE (Explain) → AR (Followup Q) → Next Question
                                ↓
                         REVISION_END
```

### Nodes

1. **REVISION_START**: Initializes session, loads question bank, greets student
2. **QUESTION_PRESENTER**: Presents next question with progress tracking
3. **EVALUATOR**: Checks answer, extracts concept if wrong, routes accordingly
4. **GE** (Guided Exploration): Explains the concept student struggled with
5. **AR** (Adaptive Remediation): Asks followup question to test understanding
6. **REVISION_END**: Shows summary with performance and weak concepts

### State Variables

- `chapter`: Chapter name for revision
- `question_bank`: List of loaded questions
- `current_question_index`: Progress through questions
- `questions_correct_first_try`: Count of correct answers
- `questions_needed_explanation`: Count needing help
- `concepts_for_review`: List of concepts student struggled with
- `current_concept`: Concept being explained (LLM-extracted)
- `is_kannada`: Kannada language support flag

## Question Bank Format

Questions stored in `revision_agent/question_banks/{chapter_name}.json`:

```json
{
  "chapter": "Nutrition in Plants",
  "questions": [
    {
      "id": 1,
      "question": "What is photosynthesis?",
      "expected_answer": "Process by which plants make food",
      "difficulty": "easy"
    }
  ]
}
```

**Note**: No `concept` field needed - evaluator extracts it using LLM when student answers incorrectly.

## Key Design Decisions

1. **Simplified from Learning Agent**:
   - No autosuggestions (set `include_autosuggestions=False` everywhere)
   - Reuses GE and AR nodes with modifications
   - Same optimization pattern (`_wrap`, `node_transitions`, `summary`)

2. **Dynamic Concept Extraction**:
   - Question bank is simpler (no predefined concepts)
   - Evaluator uses LLM to identify concept when student fails
   - More flexible and context-aware

3. **Single File Architecture**:
   - All 6 nodes in one `nodes.py` file for simplicity
   - Easier to maintain than split files

## Utilities Used

From `utils/shared_utils.py`:

- `llm_with_history()` - LLM calls with API tracker
- `build_prompt_from_template_optimized()` - Prompt building (autosuggestions=False)
- `translate_if_kannada()` - Kannada translation
- `add_ai_message_to_conversation()` - Message tracking
- `extract_json_block()` - JSON extraction

## Testing

Run the revision agent on "Nutrition in Plants" chapter:

```python
from revision_agent.graph import graph

# Initialize state
state = {
    "chapter": "Nutrition in Plants",
    "is_kannada": False,  # Set to True for Kannada
    "language": "english"
}

# Run graph
config = {"configurable": {"thread_id": "test-session-1"}}
for event in graph.stream(state, config):
    print(event)
```

## Adding New Question Banks

1. Create JSON file: `revision_agent/question_banks/{chapter_name}.json`
2. Follow the format above (id, question, expected_answer, difficulty)
3. Load by setting `state["chapter"] = "{chapter_name}"`

## Files Structure

```
revision_agent/
├── __init__.py
├── config.py                          # ConceptPkg model
├── graph.py                           # State + graph definition + routing
├── nodes.py                           # All 6 nodes
├── question_bank.py                   # Helper functions
├── langgraph.json                     # LangGraph config
└── question_banks/
    └── nutrition_in_plants.json       # Sample question bank
```

## Next Steps

- Add more question banks for other chapters
- Test with students
- Fine-tune evaluation criteria
- Add difficulty progression (start easy → harder)
