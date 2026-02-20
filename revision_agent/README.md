# Revision Agent

Quick concept review agent for students preparing for exams.

## Overview

The revision agent helps students review concepts before exams using predefined question banks. It:

- Presents questions chapter by chapter from a JSON question bank
- Evaluates answers semantically (not word-for-word) using LLM
- If wrong: extracts the concept via LLM, explains it (GE), then asks a followup question (AR)
- Tracks performance: correct first try vs. needed explanation
- Outputs a summary with performance stats and identified weak concepts

## Architecture

### Flow

```
START → REVISION_START → QUESTION_PRESENTER → EVALUATOR
                                 ↓                ↓
                          [If correct]      [If incorrect]
                             ↓                    ↓
                        Next Question     GE (Explain) → AR (Followup Q) → Next Question
                             ↓
                        REVISION_END
```

### Nodes (all in `nodes.py`)

| Node                          | Description                                                                                                                                                                      |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **REVISION_START**            | Initializes session, loads question bank, greets student. Initializes `messages`, `summary`, `summary_last_index`.                                                               |
| **QUESTION_PRESENTER**        | Presents next question with progress (Question X of Y). Routes to `EVALUATOR` or `REVISION_END` when bank exhausted.                                                             |
| **EVALUATOR**                 | Checks answer semantically with LLM. If correct → next question. If incorrect → extracts concept (separate LLM call) → routes to `GE`.                                           |
| **GE** (Guided Exploration)   | Explains the concept the student struggled with. Routes to `AR` when student seems to understand, or loops back to `GE`.                                                         |
| **AR** (Adaptive Remediation) | Asks a followup question to test understanding. After student answers (right or wrong), always moves to `QUESTION_PRESENTER`. Politely corrects if wrong and reiterates concept. |
| **REVISION_END**              | Generates summary (totals, correct count, weak concepts) and encourages the student.                                                                                             |

### Graph Routing

The graph uses `state["current_state"]` for routing (same pattern as the main learning agent):

```
REVISION_START → QUESTION_PRESENTER
QUESTION_PRESENTER → EVALUATOR | REVISION_END
EVALUATOR → QUESTION_PRESENTER | GE
GE → GE | AR
AR → QUESTION_PRESENTER
REVISION_END → END
```

### State Variables

```python
class RevisionAgentState(TypedDict, total=False):
    # Core
    messages: List[AnyMessage]        # Conversation history (shared with main agent)
    current_state: str                # Current graph node
    last_user_msg: str                # Latest student input
    agent_output: str                 # Latest agent response

    # Revision-specific
    chapter: str                      # Chapter name from question bank filename
    question_bank: List[Dict]         # Loaded questions
    current_question_index: int       # Progress pointer
    questions_total: int              # Total questions in bank
    questions_correct_first_try: int  # Count of first-try correct
    questions_needed_explanation: int # Count needing GE/AR
    concepts_for_review: List[str]    # Concepts student struggled with
    current_question: Dict            # Currently active question object
    current_concept: str              # Concept extracted by EVALUATOR (drives GE/AR)

    # Kannada support
    is_kannada: bool
    language: str

    # Node tracking
    asked_ge: bool
    asked_ar: bool

    # Optimization (mirrors main agent)
    node_transitions: List[Dict]
    summary: str
    summary_last_index: int
```

## Question Bank Format

Questions stored in `revision_agent/question_banks/{chapter_filename}.json`:

```json
{
  "chapter": "Nutrition in Plants",
  "questions": [
    {
      "id": 1,
      "question": "What is photosynthesis?",
      "expected_answer": "Process by which plants make food using sunlight, water, and carbon dioxide",
      "difficulty": "easy"
    }
  ]
}
```

**No `concept` field needed** — the EVALUATOR uses LLM to dynamically identify the concept when a student answers incorrectly, making question bank authoring simpler.

**Available question banks:**

- `nutrition_in_plants.json` — Class 7 Science
- `measurement_of_time_and_motion.json` — Class 7 Science

## Key Design Decisions

### 1. GE and AR nodes reused from learning agent

The revision agent reuses GE and AR node logic from the main learning agent with key modifications:

- `include_autosuggestions=False` everywhere (revision flow doesn't need them)
- GE uses `state["current_concept"]` (extracted by EVALUATOR) — not from CI as in the main agent
- AR always routes to `QUESTION_PRESENTER` — not to TC as in the main agent
- AR feedback: if student is wrong, politely corrects and reiterates the key idea before moving on (AR node `next_state` is always `"QUESTION_PRESENTER"`)

### 2. Same shared utilities as the main agent

Both the revision agent and all learning agent variants use the same functions from `utils/shared_utils.py`:

| Function                                 | Used by Revision Agent                                    |
| ---------------------------------------- | --------------------------------------------------------- |
| `llm_with_history()`                     | ✅ All nodes                                              |
| `build_prompt_from_template_optimized()` | ✅ All nodes (last-4-messages window, no autosuggestions) |
| `translate_if_kannada()`                 | ✅ All nodes                                              |
| `add_ai_message_to_conversation()`       | ✅ All nodes                                              |
| `extract_json_block()`                   | ✅ EVALUATOR, GE, AR                                      |
| `invoke_llm_with_fallback()`             | ✅ Via `llm_with_history`                                 |

### 3. Single-file node architecture

All 6 nodes are in one `nodes.py` for simplicity. The main agent splits nodes across `main_nodes_simulation_agent_no_mh.py` and `simulation_nodes_no_mh_ge.py`.

### 4. InMemorySaver checkpointer

The revision agent uses `InMemorySaver` (not Postgres). Sessions are not persisted across server restarts. This is simpler for the revision use case where sessions are short and ephemeral.

### 5. Node wrapper pattern

Inherits the same `_wrap()` pattern from the main agent for:

- Updating `last_user_msg` from the latest `HumanMessage`
- Tracking node transitions (`node_transitions` list)

## Running the Revision Agent

### Via Streamlit UI (Recommended)

```bash
streamlit run Streamlit_UI/revision_app.py
```

Features:

- Chapter selection dropdown (auto-discovers all `.json` files in `question_banks/`)
- Live progress in sidebar (correct count, needed help count, concepts to review)
- Downloadable JSON summary at session end

### Via Python (Direct)

```python
from revision_agent.graph import graph

config = {"configurable": {"thread_id": "my-revision-session-1"}}

# Start
result = graph.invoke(
    {"chapter": "nutrition_in_plants", "messages": [HumanMessage(content="start")]},
    config
)
print(result["agent_output"])  # Welcome message

# Continue (answer a question)
from langgraph.types import Command
result = graph.invoke(
    Command(resume=True, update={"messages": [HumanMessage(content="Photosynthesis is how plants make food")]}),
    config
)
print(result["agent_output"])
```

## File Structure

```
revision_agent/
├── README.md                          # This file
├── __init__.py
├── config.py                          # ConceptPkg model (minimal)
├── graph.py                           # State definition, node wrappers, graph construction
├── nodes.py                           # All 6 nodes
├── question_bank.py                   # load_question_bank() helper
├── langgraph.json                     # LangGraph Studio config
└── question_banks/
    ├── nutrition_in_plants.json
    └── measurement_of_time_and_motion.json
```

## Adding New Question Banks

1. Create a JSON file: `revision_agent/question_banks/{chapter_name}.json`
2. Follow the format: `chapter`, `questions[]` with `id`, `question`, `expected_answer`, `difficulty`
3. The Streamlit UI auto-discovers it on next launch — no code changes needed

## Next Steps

- Add more question banks for other chapters
- Test with actual students and fine-tune evaluation criteria
- Consider difficulty progression (start easy → harder)
- Add Postgres persistence for cross-session tracking
