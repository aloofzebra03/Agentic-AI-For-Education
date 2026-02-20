# Agentic AI For Education

## 🎯 Project Overview

This project is a comprehensive **AI-powered educational system** that combines **LangGraph**, **Retrieval-Augmented Generation (RAG)**, **interactive simulations**, and **multimodal interfaces** to create an adaptive learning experience. The system features multiple educational agents with speech recognition/synthesis, visual simulations, automated testing capabilities, and a dedicated exam revision agent.

## 🏗️ Architecture Overview

```
├── 🧠 Core Educational Agents (Multiple Variants)
├── 📝 Revision Agent (Exam Preparation)
├── 🌐 FastAPI Backend (api_servers/)
├── 🎤 Streamlit Frontend (Streamlit_UI/)
├── 📦 Shared Utilities (utils/shared_utils.py)
├── 💡 Autosuggestion Module (autosuggestion/)
├── 🧪 Testing & Evaluation Framework (tester_agent/)
├── 📚 RAG Content Management
├── 🎨 Visual Simulation Engine
└── 📊 Analytics & Monitoring (LangSmith)
```

## 📁 Project Structure & Dependencies

### **Core Educational Agent Variants**

The project contains multiple variants of the educational agent, each building upon the previous with incremental improvements:

#### 1. **`educational_agent_v1/`** - Base Agent with RAG

- **Primary Files**: `agent.py`, `nodes4_rag.py`, `graph_fuse.py`, `config.py`
- **Features**: Basic conversational agent with RAG integration
- **Tracing**: Uses LangFuse/LangSmith for tracing. Header attached in `agent.py`
- **Sub-modules**:
  - `Creating_Section_Text/` - RAG content generation pipeline
  - `Filtering_GT/` - Ground truth filtering utilities

#### 2. **`educational_agent_with_simulation_v2/`** - Full Simulation Integration

- Full interactive physics simulations (pendulum demonstrations) added on top of v1
- Real-time parameter manipulation

#### 3. **`educational_agent_optimized_v3/`** - Memory-Optimized Agent

- Memory optimization via conversation summarization
- Uses `Langfuse` for tracing

#### 4. **`educational_agent_optimized_langsmith_kannada_v4/`** - Multilingual Support

- Kannada language support (system prompt + hardcoded messages changed to Kannada)
- Language-specific model configurations

#### 6. **`educational_agent_optimized_langsmith_v5/`** ⭐ - Current Production Agent (Static Autosuggestions)

- **Primary Files**: `agent.py`, `graph.py`, `main_nodes_simulation_agent_no_mh.py`, `simulation_nodes_no_mh_ge.py`, `index.html`
- **Key Feature**: **Static autosuggestions** — generated after each LLM response via `autosuggestion.generate_static_autosuggestions()`. No LLM calls involved in suggestion generation; everything is rule-based.
- **How Static Suggestions Work** (implemented in `autosuggestion/helpers.py`):
  - `positive_autosuggestion`: **Randomly selected** from `POSITIVE_POOL` (e.g., "I understand, continue") — but **suppressed** (`None`) if the agent's output contains a `?` or the phrase "let me think" (regex check)
  - `negative_autosuggestion`: **Randomly selected** from `NEGATIVE_POOL` (e.g., "I'm not sure") — always present
  - `special_handling_autosuggestion`: **Per-node fixed** based on `NODE_SPECIAL_HANDLING` map in `autosuggestion/constants.py`:
    - `APK` → always `"Can you give me a hint?"`
    - `CI` → always `"Can you explain that simpler?"`
    - `GE` → **randomly selected** from `SPECIAL_HANDLING_POOL`
    - `AR` → always `"Can you give me a hint?"`
    - `TC`, `RLC` → `None` (no special handling)
  - `dynamic_autosuggestion`: Always **`None`** in the static implementation — no LLM generation
- **Why Static?** The dynamic autosuggestion prompt doubled tokens to every LLM call (passing pools + generation instructions inline). Static generation moves this completely out of LLM context.
- **Conversation History**: Uses `build_prompt_from_template_optimized()` — last 4 messages only
- **Persistence**: Postgres via Supabase (checkpointer)
- **API**: Served by `api_servers/api_server_v5.py`
- **UI**: `Streamlit_UI/app_agent_v5.py`

#### 7. **`educational_agent_optimized_langsmith_autosuggestion/`** - Dynamic Autosuggestion Agent

- **Primary Files**: `graph.py`, `main_nodes_simulation_agent_no_mh.py`, `simulation_nodes_no_mh_ge.py`, `index.html`
- **Key Feature**: **Dynamic autosuggestions** — the LLM itself selects from the predefined pools AND generates a completely context-aware 4th suggestion (`dynamic_autosuggestion`, 12-15 words). The pool options are passed directly inside the LLM prompt via `build_prompt_from_template_optimized(..., include_autosuggestions=True)`.
- **How Dynamic Suggestions Work** (generated inside the LLM response JSON):
  - `positive_autosuggestion`: LLM chooses from `POSITIVE_POOL` — set to `null` when the message contains a question or "let me think"
  - `negative_autosuggestion`: LLM chooses from `NEGATIVE_POOL` — always non-null
  - `special_handling_autosuggestion`: LLM chooses from `SPECIAL_HANDLING_POOL`
  - `dynamic_autosuggestion`: **Unique exploration prompt** generated by the LLM, tailored to the current pedagogical moment and student level (`low`/`medium`/`advanced`) — set to `null` when the message contains a question
- **Suppression**: Same `?` / "let me think" suppression as v5, but enforced via prompt instructions to the LLM (not post-hoc regex on the output)
- **Token cost**: The autosuggestion instructions + pool lists doubles tokens per LLM call compared to v5. This motivated the creation of the static v5 approach.
- **Persistence**: Postgres via Supabase
- **API**: Served by `api_servers/api_server.py`

---

### **The Autosuggestion Module (`autosuggestion/`)**

A standalone module shared by **both** agent variants for suggestion generation, handlers, and Kannada caching. Used directly by v5 for static generation; its constants (pools, suppression patterns) are also referenced in the dynamic variant's prompt builder.

| File             | Purpose                                                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `constants.py` | `NODE_SPECIAL_HANDLING` map (per-node special suggestion), `SUPPRESSION_PATTERNS` (regex: `?` and "let me think"), `KANNADA_AUTOSUGGESTION_CACHE` (pre-translated strings to avoid Azure calls) |
| `helpers.py`   | `generate_static_autosuggestions()` — the main entry point for v5; does random pool selection, per-node special logic, regex suppression, and Kannada translation via cache                          |
| `handlers.py`  | Logic to handle what happens when a student**clicks** an autosuggestion (hint flow, example flow, simpler explanation flow)                                                                       |
| `nodes.py`     | `autosuggestion_manager_node` and `pause_for_handler` — LangGraph nodes for routing clicked suggestions in the dynamic agent's graph                                                               |

---

### **Shared Utilities (`utils/shared_utils.py`)**

This is the **single source of truth** for common functions used by **all agent variants** (learning agents and revision agent alike). Key components:

#### **Conversation History Management** _(Currently being tested/refined)_

Two strategies exist and are both implemented; the optimized one is active:

| Function                                   | Behavior                                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `build_prompt_from_template()`           | Passes the**full** conversation history to the LLM                                                                       |
| `build_prompt_from_template_optimized()` | ✅ Active — passes only the**last 4 messages** from `state['messages']` to keep prompts concise and avoid token bloat |

The node-aware history building (which knew about which node was active and built filtered history accordingly) has been **commented out** and replaced with the simpler last-4-messages approach. This is currently under evaluation.

#### **Azure Translation for Kannada**

```python
def translate_to_kannada_azure(text: str, api_key=None, endpoint=..., region="centralindia") -> str:
    """Translate English text to Kannada using Azure Cognitive Services Translator."""
```

- Replaces previously used `deep_translator` library
- Uses Azure Cognitive Services Translator API (requires `AZURE_TRANSLATOR_KEY` in `.env`)
- Called via `translate_if_kannada(state, content)` — only translates if `state["is_kannada"]` is True and content contains English characters

#### **Autosuggestion Pools (Single Source of Truth)**

```python
POSITIVE_POOL = ["I understand, continue", "Yes, got it", "That makes sense", ...]
NEGATIVE_POOL = ["I'm not sure", "I don't know", "I'm confused", ...]
SPECIAL_HANDLING_POOL = ["Can you give me a hint?", "Can you explain that simpler?", "Give me an example"]
```

These pools serve as the single source of truth for suggestion content:

- **In v5 (static)**: `autosuggestion/helpers.py` does Python-level `random.choice()` from each pool — the LLM never sees them
- **In the dynamic agent**: The pools are injected **into the LLM prompt** (via `include_autosuggestions=True`) so the LLM selects from them and generates a 4th dynamic suggestion
- **For Kannada**: `autosuggestion/constants.py` caches pre-translated versions of all pool strings to avoid repeated Azure API calls

#### **LLM Invocation**

```python
def invoke_llm_with_fallback(messages, operation_name) -> response:
    """Calls tracker to get best available API key + model, then invokes LLM."""
```

- Uses `api_tracker_utils` to load-balance across multiple Google API keys
- Raises `MinuteLimitExhaustedError` or `DayLimitExhaustedError` if limits hit
- Rate limits tracked before invocation (not after)

#### **Other Key Functions**

| Function                                                     | Description                                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `llm_with_history(state, prompt)`                          | Wraps `invoke_llm_with_fallback` for node use                                 |
| `add_ai_message_to_conversation(state, content)`           | Appends AI message to `state["messages"]`                                     |
| `build_conversation_history(state)`                        | Formats full message history as string                                          |
| `get_all_available_concepts()`                             | Auto-scans `science_jsons/` and returns concept list                          |
| `extract_json_block(text)`                                 | Robust JSON extraction from LLM output (handles fenced blocks, balanced braces) |
| `select_most_relevant_image_for_concept_introduction(...)` | Image selector for CI node                                                      |
| `create_simulation_config(...)`                            | Builds pendulum simulation config dict                                          |

---

### **Revision Agent (`revision_agent/`)**

A separate, simplified agent designed for **exam preparation**. It quizzes students on predefined question banks and provides targeted remediation for wrong answers.

> 📖 See [`revision_agent/README.md`](revision_agent/README.md) for detailed documentation.

**Key highlights:**

- Reuses `GE` (Guided Exploration) and `AR` (Adaptive Remediation) node logic from the learning agent — **with autosuggestions stripped** (`include_autosuggestions=False`)
- Shares the same utility functions from `utils/shared_utils.py` as the main agent:
  - `llm_with_history()`, `build_prompt_from_template_optimized()`, `translate_if_kannada()`, `add_ai_message_to_conversation()`, `extract_json_block()`
- Uses `InMemorySaver` as checkpointer (simpler than Postgres used by learning agents)
- Question banks stored in `revision_agent/question_banks/` as JSON files

**Question Banks Available:**

- `nutrition_in_plants.json` — Class 7 Science chapter
- `measurement_of_time_and_motion.json` — Class 7 Science chapter

---

### **API Servers (`api_servers/`)**

FastAPI backends that expose the educational agents as REST APIs.

| File                 | Serves                                                   | Notes                                                |
| -------------------- | -------------------------------------------------------- | ---------------------------------------------------- |
| `api_server.py`    | `educational_agent_optimized_langsmith_autosuggestion` | Primary production server (dynamic autosuggestions)  |
| `api_server_v5.py` | `educational_agent_optimized_langsmith_v5`             | V5 server (static autosuggestions)                   |
| `schemas.py`       | —                                                       | Shared Pydantic request/response models              |
| `test_api.py`      | —                                                       | API test scripts                                     |
| Archived versions    | —                                                       | `api_server_before_*` files for rollback reference |

**Both `api_server.py` and `api_server_v5.py` are structurally identical** — only the imported agent graph differs. They expose the same endpoints:

#### **API Endpoints**

| Method     | Endpoint                                 | Description                                                                                      |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `GET`    | `/`                                    | Root info and endpoint listing                                                                   |
| `GET`    | `/health`                              | Health check (includes persistence and agent type)                                               |
| `GET`    | `/concepts`                            | List all available teachable concepts (auto-scanned from `science_jsons/`)                     |
| `POST`   | `/session/start`                       | Start a new learning session; returns `thread_id`, initial agent response, and autosuggestions |
| `POST`   | `/session/continue`                    | Continue existing session with student message; returns agent response + autosuggestions         |
| `GET`    | `/session/status/{thread_id}`          | Get session progress (current node, asked flags, concepts, misconceptions)                       |
| `GET`    | `/session/history/{thread_id}`         | Get full conversation history and node transitions                                               |
| `GET`    | `/session/summary/{thread_id}`         | Get session summary, scores, and transfer success                                                |
| `DELETE` | `/session/{thread_id}`                 | Delete session from Postgres (checkpoints, writes, blobs)                                        |
| `GET`    | `/test/personas`                       | List available tester personas                                                                   |
| `POST`   | `/test/persona`                        | Start a session with a predefined tester persona                                                 |
| `POST`   | `/test/images`                         | Test image selection for a concept                                                               |
| `POST`   | `/test/simulation`                     | Test simulation config generation for a concept                                                  |
| `POST`   | `/concept-map/generate`                | Generate a concept map timeline from description                                                 |
| `POST`   | `/translate`                           | Translate text to Kannada using Azure Translator                                                 |
| `GET`    | `/simulation`                          | Simulation module health check                                                                   |
| `POST`   | `/simulation/session/start`            | Start a simulation-to-concept teaching session                                                   |
| `POST`   | `/simulation/session/{id}/respond`     | Send student response in simulation session                                                      |
| `POST`   | `/simulation/session/{id}/submit-quiz` | Submit quiz answer in simulation                                                                 |
| `GET`    | `/simulation/session/{id}`             | Get simulation session state                                                                     |
| `GET`    | `/simulation/simulations`              | List available simulations                                                                       |

**Running the API servers:**

```bash
# Autosuggestion agent (port 8001)
uvicorn api_servers.api_server:app --host 0.0.0.0 --port 8001 --reload

# V5 agent (port 8000)
uvicorn api_servers.api_server_v5:app --host 0.0.0.0 --port 8000 --reload
```

**Error Handling**: Custom HTTP status codes for rate limit errors:

- `501` — Minute limit exhausted (`MinuteLimitExhaustedError`)
- `502` — Day limit exhausted (`DayLimitExhaustedError`)

---

### **Streamlit UI (`Streamlit_UI/`)**

All frontend applications are in `Streamlit_UI/`:

#### **Current / Active UIs**

| File                                   | Agent                        | Features                                                             | Notes                    |
| -------------------------------------- | ---------------------------- | -------------------------------------------------------------------- | ------------------------ |
| `app_optimized_animation.py`         | `langsmith_autosuggestion` | TTS (gTTS), ASR (Whisper), lip-sync avatars, dynamic autosuggestions | Main multimodal UI       |
| `app_optimized_animation_kannada.py` | `langsmith_autosuggestion` | Kannada TTS/ASR, Kannada autosuggestions                             | Kannada language variant |
| `app_agent_v5.py`                    | `langsmith_v5`             | Text-only,**static autosuggestions**, last-4-messages sidebar  | V5 testing UI            |
| `revision_app.py`                    | `revision_agent`           | Text-only, chapter selection, progress sidebar, downloadable summary | Revision/exam prep UI    |

#### **Legacy / Development UIs**

| File                                         | Notes                              |
| -------------------------------------------- | ---------------------------------- |
| `app.py`                                   | Basic interface (legacy)           |
| `app_graph.py`                             | Graph-based visualization (legacy) |
| `app_gt.py`                                | Ground truth testing (legacy)      |
| `app_simulation.py`                        | Simulation-only interface          |
| `app_simulation_optimized.py`              | Optimized simulation interface     |
| `app_optimized_animation_old.py`           | Legacy backup                      |
| `app_optimized_animation copy.py`          | Development copy                   |
| `app_optimized_animation_kannada copy*.py` | Kannada development copies         |

#### **`app_agent_v5.py`** — Key Details

- Directly invokes `educational_agent_optimized_langsmith_v5.graph.graph` (no API layer)
- Displays **static autosuggestions** from the last agent response (`positive`, `negative`, `dynamic`) as colored HTML blocks below the chat
- Shows last 4 messages in the sidebar (mirrors the 4-message conversation history window sent to LLM)
- Uses `LangGraph Command(resume=True)` pattern for session continuation

#### **`revision_app.py`** — Key Details

- Directly invokes `revision_agent.graph.graph`
- Scans `revision_agent/question_banks/*.json` dynamically for chapter selection
- Shows live progress (correct count, needed help count, concepts to review) in sidebar
- Downloadable JSON summary at session end

---

### **Shared Infrastructure**

#### **`api_tracker_utils/`** — Multi-Key Rate-Limit Tracker

Manages multiple Google API keys and models to avoid rate limits:

- `tracker.py` — Tracks per-minute and daily call counts; selects optimal key+model pair
- `config.py` — Available models list and default model
- `error.py` — `MinuteLimitExhaustedError`, `DayLimitExhaustedError`

#### **`tester_agent/`** — Automated Testing System

- `tester.py` — Core testing orchestrator
- `personas.py` — Student persona definitions (Eager, Confused, Distracted, Dull)
- `evaluator.py` — Response evaluation metrics
- `session_metrics.py` — Learning analytics
- `simulation_descriptor.py` — Simulation analysis

#### **`utils/`** — Shared Utilities (non-`shared_utils.py`)

| File                                            | Purpose                               |
| ----------------------------------------------- | ------------------------------------- |
| `shared_utils.py`                             | All node-shared functions (see above) |
| `run_test.py`                                 | Direct graph test runner              |
| `run_test_api.py`                             | API-based test runner                 |
| `compute_session_metrics.py`                  | Session analytics computation         |
| `NCERT Class 7.json`                          | Class 7 NCERT concept catalog         |
| `index.html`                                  | Simulation HTML (pendulum, Canvas JS) |
| `animation.html`                              | Animation HTML asset                  |
| `create_character_images.py`                  | Character image generator for avatars |
| `shared_utils_old_before_tracker_28_12_25.py` | Pre-tracker backup                    |

#### **`science_jsons/`** — Content Database

JSON files containing educational content for each concept (descriptions, analogies, MCQs, real-life applications, etc.). The `_build_concept_to_file_mapping()` function in `shared_utils.py` auto-scans this directory.

#### **`concept_map_poc/`** — Concept Map Generator

POC for generating visual concept timelines from descriptions. Integrated in both API servers via the `POST /concept-map/generate` endpoint.

---

## 🤖 Agent Flow (Learning Agent)

The main learning agent follows this pedagogical flow:

```
START
  ↓
APK (Prior Knowledge Activation)
  ↓
CI (Concept Introduction) — shows image
  ↓
GE (Guided Exploration)
  ↓
AR (Adaptive Remediation) ← loops back if student struggles
  ↓
TC (Transfer Check)
  ↓
RLC (Real-Life Connection)
  ↓
END (Session Summary)
```

Simulation nodes (`sim_concept_creator`, `sim_vars`, `sim_action`, `sim_expect`, `sim_execute`, `sim_observe`, `sim_insight`, `sim_reflection`) can be injected between CI and GE when a physics simulation is appropriate.

---

## 🔄 Data Flow & Dependencies

```
educational_agent_v1 (base)
├── educational_agent_with_simulation_v2
├── educational_agent_optimized_v3
├── educational_agent_optimized_langsmith_kannada_v4
├── educational_agent_optimized_langsmith_v5 ← api_servers/api_server_v5.py ← Streamlit_UI/app_agent_v5.py
├── educational_agent_optimized_langsmith_autosuggestion ← api_servers/api_server.py ← Streamlit_UI/app_optimized_animation.py
└── revision_agent ← Streamlit_UI/revision_app.py

All agents ↑ share → utils/shared_utils.py
```

---

## 🚀 Getting Started

### **Prerequisites**

```bash
Python >= 3.10
```

### **Environment Setup**

1. **Clone Repository**:

   ```bash
   git clone <repository-url>
   cd Agentic-AI-For-Education
   ```
2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   # or for minimal setup:
   pip install -r requirements-minimal.txt
   ```
3. **Configure Environment** (`.env` file):

   ```env
   # Google Gemini API Keys (multiple for load balancing, up to GOOGLE_API_KEY_7)
   GOOGLE_API_KEY_1=...
   GOOGLE_API_KEY_2=...

   # Azure Translator (for Kannada translation)
   AZURE_TRANSLATOR_KEY=...

   # LangSmith Tracing
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=tester_agent_v5
   LANGCHAIN_API_KEY=...

   # Supabase Postgres (for session persistence — Transaction mode URL)
   POSTGRES_DATABASE_URL=postgresql://...

   # Optional: HuggingFace, Groq, Langfuse
   HF_API_TOKEN=...
   ```

### **Running the Applications**

#### **API Server (V5 — Static Autosuggestions):**

```bash
uvicorn api_servers.api_server_v5:app --host 0.0.0.0 --port 8000 --reload
```

#### **API Server (Dynamic Autosuggestions):**

```bash
uvicorn api_servers.api_server:app --host 0.0.0.0 --port 8001 --reload
```

#### **Main Multimodal Interface (TTS/ASR + Dynamic Autosuggestions):**

```bash
streamlit run Streamlit_UI/app_optimized_animation.py
```

#### **V5 Text Interface (Static Autosuggestions):**

```bash
streamlit run Streamlit_UI/app_agent_v5.py
```

#### **Revision Agent UI:**

```bash
streamlit run Streamlit_UI/revision_app.py
```

#### **Kannada Language Interface:**

```bash
streamlit run Streamlit_UI/app_optimized_animation_kannada.py
```

---

## 🎯 Core Features

### **1. Adaptive Learning Flow**

- **Multi-Node Agent Architecture**: Each educational concept flows through discrete pedagogical nodes
- **Misconception Detection**: Real-time identification of student misunderstandings
- **Personalized Paths**: Dynamic routing based on student performance
- **Student Level Tracking**: `low`, `medium`, `advanced` — affects autosuggestion depth and teaching pace

### **2. Autosuggestions (Two Variants)**

| Feature              | V5 (Static)                                                         | Autosuggestion Agent (Dynamic)                                         |
| -------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Positive suggestion  | ✅ Random from `POSITIVE_POOL` (Python `random.choice`)             | ✅ LLM selects from `POSITIVE_POOL` (passed in prompt)                 |
| Negative suggestion  | ✅ Random from `NEGATIVE_POOL` (always present)                     | ✅ LLM selects from `NEGATIVE_POOL` (always present)                   |
| Special handling     | ✅ Per-node fixed (APK/AR→hint, CI→simpler, GE→random, TC/RLC→None) | ✅ LLM selects from `SPECIAL_HANDLING_POOL`                            |
| Dynamic suggestion   | ❌ Always `None` — no LLM generation                                | ✅ LLM-generated context-aware prompt (12-15 words, adapts to level)   |
| Positive suppression | ✅ Post-hoc **regex** on agent output (`?` / "let me think")        | ✅ Via **prompt instructions** to LLM (`?` / "let me think" → `null`)  |
| Token overhead       | ✅ Zero extra tokens (no pools in LLM prompt)                       | ⚠️ ~2× tokens per call (pools + instructions injected into prompt)     |
| Kannada translations | ✅ Via cache in `autosuggestion/constants.py` (no Azure call)       | ✅ Via same cache in `autosuggestion/constants.py`                     |

### **3. Multilingual Support (Kannada)**

- **Translation**: Azure Cognitive Services Translator (`en` → `kn`) via `translate_to_kannada_azure()` in `shared_utils.py`
- **ASR**: `vasista22/whisper-kannada-tiny` for Kannada speech
- **TTS**: gTTS with `lang='kn'`
- **Autosuggestion Labels**: Pre-cached Kannada translations for all pool suggestions (no extra API calls)
- **Detection**: `is_kannada` flag in agent state controls translation throughout all nodes

### **4. Exam Revision**

- Dedicated `revision_agent` with question bank-driven flow
- LLM-extracted concept identification when student answers incorrectly
- Tracks correct-first-try vs. needed-explanation counts
- Outputs a downloadable performance summary

### **5. Visual Simulations**

- Physics pendulum simulation in `index.html` (Canvas-based JavaScript)
- `create_simulation_config()` in `shared_utils.py` generates config for simulation parameterization
- Simulation nodes handle concept → simulation → observation → insight flow

### **6. Multimodal Interface**

- **Speech-to-Text**: Whisper (English) / Whisper-Kannada
- **Text-to-Speech**: gTTS with speed optimization via Pedalboard
- **Visual Avatars**: Lip-sync animations with character selection (boy/girl)

---

## 🧪 Testing & Evaluation

### **Automated Persona Testing**

```bash
# Direct graph test
python utils/run_test.py

# API-based test
python utils/run_test_api.py
```

**Student Personas**: Eager, Confused, Distracted, Dull

### **Tester Agent**

The `tester_agent/` module simulates student personas and evaluates agent responses:

- `personas.py` — Persona behavior definitions
- `evaluator.py` — Scoring agent responses
- `session_metrics.py` — Learning effectiveness metrics

---

## 📊 Monitoring & Analytics

### **LangSmith Integration** (Primary)

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "educational_agent"
```

All LLM calls and graph executions are automatically traced for debugging, latency monitoring, and prompt optimization.

### **Session Persistence**

- **Learning Agents**: Postgres via Supabase (`langgraph-checkpoint-postgres`)
- **Revision Agent**: `InMemorySaver` (in-process memory, cleared on restart)

---

## 🌍 Multilingual Support Detail

| Component       | English      | Kannada                            |
| --------------- | ------------ | ---------------------------------- |
| Agent response  | ✅           | ✅ (Azure Translator)              |
| Autosuggestions | ✅           | ✅ (pre-cached)                    |
| ASR             | Whisper-tiny | `vasista22/whisper-kannada-tiny` |
| TTS             | gTTS (en)    | gTTS (kn)                          |
| UI labels       | ✅           | ✅ (in Kannada apps)               |

---

## 🔧 Technical Notes

### **Conversation History Strategy**

`build_prompt_from_template_optimized()` in `shared_utils.py` is actively being tested with different strategies:

```python
# CURRENT (active): Last 4 messages only
# Uses last N (slices when len(messages) > 4, otherwise takes all)
last_n_messages = messages[-4:] if len(messages) > 4 else messages

# PREVIOUS (commented out): Node-aware history building
# history = build_node_aware_conversation_history(state, current_node)
```

The node-aware approach built context-filtered history based on the current pedagogical node. The simpler last-4 approach reduces prompt size and keeps context focused.

### **Session Threading**

Thread IDs are structured for easy identification:

```
{user_id}-{label}-{concept}-{language}-thread-{timestamp}
```

### **Package Structure**

The project uses `pyproject.toml` for package configuration, enabling clean cross-directory imports:

```bash
pip install -e .  # Install in editable mode
```

---

## 🔮 Future Development

### **Planned Enhancements**

1. **Multi-Subject Support** — Expand beyond physics/science to mathematics, chemistry
2. **Advanced Simulations** — 3D visualizations
3. **Collaborative Learning** — Multi-student session support
4. **Enhanced Analytics** — Learning pattern analysis, predictive modeling
5. **Mobile Application** — React Native or Flutter
6. **Voice Cloning** — Personalized teacher voice synthesis
7. **More Revision Question Banks** — Expand across all Class 7 chapters
8. **Difficulty Progression** — Adaptive question ordering in revision agent

### **Technical Improvements**

1. **Conversation History** — Continue evaluating last-N vs. node-aware vs. summary-based approaches
2. **Docker Containerization** — Simplified deployment
3. **Database Integration** — Persistent user progress tracking across sessions
4. **A/B Testing Framework** — Systematic feature experimentation between v5 and autosuggestion variants
