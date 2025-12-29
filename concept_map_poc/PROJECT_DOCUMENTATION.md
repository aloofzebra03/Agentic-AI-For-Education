# Concept Map Character-Based Platform – Detailed Documentation

## 1. Project Overview
This repository hosts a dual-delivery platform that converts free-form descriptions into narrated, animated concept maps. Two fully supported systems share the same knowledge extraction core but differ in how the experience is delivered:

1. **Part I – Streamlit Standalone Application**: a single-page app (`streamlit_app_standalone.py`) that orchestrates LLM extraction, character-based timing, gTTS audio, and live visualization inside Streamlit.
2. **Part II – LangGraph CLI Workflow**: a LangGraph-based pipeline (`main_universal.py`) that can run headless, trace each node, and optionally launch an enhanced Streamlit visualizer with pre-computed assets.

Both systems rely on common modules (analysis, timing, metrics, configuration). This document walks through each component in flow order so a new contributor can understand *exactly* how data moves through the project.

---

## 2. Part I – Streamlit Standalone Application
### 2.1 Purpose
Deliver an end-to-end, browser-based experience where a user pastes a description, selects an educational level, and receives:
- Extracted concepts ranked by importance
- Keyword-timed narration generated with gTTS
- Progressive graph visualization on a smart 3×3 grid
- Downloadable JSON of the timeline
- Local metrics for every run

### 2.2 High-Level Flow
1. **User Input (Streamlit UI)** → description, level, optional topic.
2. **Timeline Generation (`timeline_mapper.py`)** → single Gemini call produces concepts, relationships, reveal timings.
3. **Pre-computation (`precompute_engine.py`)** → gTTS audio + smart-grid positions.
4. **Visualization (`streamlit_app_standalone.py`)** → render graph, orchestrate audio playback, reveal nodes in sync.
5. **Metrics (`metrics_logger.py`)** → persist token/timing/output data; view later via `view_metrics.py`.

### 2.3 Component Reference (Flow Order)
| Order | File | Role |
| --- | --- | --- |
| 1 | `streamlit_app_standalone.py` | Streamlit UI, event handlers, visualization logic, audio playback, download/export. |
| 2 | `timeline_mapper.py` | Calls Gemini (via `google.generativeai`) once using prompts from description + `description_analyzer.py`. Produces: concepts (with `importance_rank`), relationships, sentences, reveal times, metadata. Logs token/timing metrics and optionally patches LangSmith runs. |
| 3 | `description_analyzer.py` | Analyzes word count, unique terms, sentence length. Provides `analyze_description_complexity`, `adjust_complexity_for_educational_level`, and topic extraction used by timeline mapper. Reads defaults from `complexity_config.py` (placeholder for override constants). |
| 4 | `complexity_config.py` | Reserved for customizing scaling constants (empty scaffold today). Keeps tuning in a single place. |
| 5 | `precompute_engine.py` | `PrecomputeEngine` generates gTTS audio with exponential backoff, calculates character-based durations, filters edges (max 2 incoming), and computes smart-grid positions (root centered, sequential fill). `precompute_all` ties audio+layout together. |
| 6 | `tts_handler.py` | Utility for optional text-to-speech narration outside Streamlit (used by CLI as well). Encapsulates `pyttsx3` settings and sentence-level playback. |
| 7 | `metrics_logger.py` | Persists every run (input preview, tokens, timing, outputs, success/error) into `metrics_logs/run_*.json`. Used by timeline mapper on success and failure paths. |
| 8 | `view_metrics.py` | CLI dashboard for JSON logs. Supports summary, recent runs, full history, and detail view (`python view_metrics.py --detail 3`). |
| 9 | `metrics_logs/` | Runtime folder (git-ignored) storing JSON metrics. |

### 2.4 Execution Narrative
1. **Initialization**: Streamlit app loads environment (.env) to find `GOOGLE_API_KEY`, configures logging, imports dependencies, and initializes pygame (dummy driver for Streamlit Cloud compatibility).
2. **User Interaction**: The UI (custom CSS) renders text areas, controls for educational level/layout, status panels, and persistent JSON download button.
3. **Timeline Creation**:
   - `create_timeline()` splits sentences, computes word timings (0.08 s/character), prompts Gemini 2.5 Flash Lite for `target_concepts` ranked 1…N, and maps concepts to sentences via keyword positions.
   - Relationships are validated to ensure referenced nodes exist; missing nodes are added with fallback attributes.
   - Metadata includes timing histogram, API durations, parse durations, total wall-clock durations, and `importance_rank` distribution.
4. **Precomputation**:
   - `PrecomputeEngine.generate_all_audio()` uses gTTS for the full text (legacy fallback: per-sentence audio). Retries up to five times (3–48 s backoff) to overcome 429 rate limits.
   - `calculate_positions()` arranges nodes on a 3×3 grid based on importance ranks (root stays at (0,0)). `_filter_edges_by_incoming_limit()` ensures no concept exceeds two inbound edges.
5. **Visualization Loop**:
   - `render_graph()` draws nodes with Matplotlib (Agg backend), coloring new nodes orange/gold, existing nodes blue, and arcs with textual labels.
   - `reveal_concepts_progressively()` gradually increases `alpha_map` and `scale_map` to fade/pop nodes in when `elapsed_time >= reveal_time`.
   - `play_audio()` streams MP3 via Streamlit’s audio player and blocks for estimated duration (via `mutagen` or size heuristic).
6. **User Feedback**: Concept list, relationships, metadata, and JSON download remain visible while the animation progresses.
7. **Metrics**: After each timeline run, `log_metrics()` stores tokens, durations, outputs, and errors. Developers can inspect aggregated stats with `view_metrics.py` or read the generated JSON directly.

### 2.5 Data Contracts
- **Concept Object**: `{ "name": str, "type": str, "importance": "high/medium/low", "importance_rank": int, "definition": str, "reveal_time": float }`
- **Relationship Object**: `{ "from": str, "to": str, "relationship": str }`
- **Timeline Metadata**: `total_concepts`, `total_relationships`, `total_duration`, `api_duration`, `parse_duration`, `word_count`, `audio_file`, `layout_style`.

### 2.6 Metrics & Observability
- **Local logging**: `metrics_logger.py` + `metrics_logs/` directory (git-ignored).
- **CLI visualization**: `view_metrics.py` for summaries, history, or per-run dumps.
- **LangSmith**: If `LANGCHAIN_API_KEY` is set, timeline mapper wraps `create_timeline()` with `traceable`, starts a LangSmith run, updates token counts, and keeps local logging in sync.
- **Documentation**: `METRICS_README.md` details the JSON schema and viewer commands; `STANDALONE_APP_README.md` provides additional UX notes.

### 2.7 Running & Configuration
```bash
# Install dependencies
pip install -r requirements.txt

# Provide environment variables
cp .env.example .env  # ensure GOOGLE_API_KEY is set

# Launch the app
streamlit run streamlit_app_standalone.py

# Inspect metrics after a few runs
python view_metrics.py --recent 5
```
Key environment variables: `GOOGLE_API_KEY`, optional `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`. `.gitignore` keeps `.env`, `metrics_logs/`, and other artifacts out of version control; `.gitattributes` enforces LF endings and basic text diff settings.

---

## 3. Part II – LangGraph CLI Workflow
### 3.1 Purpose
Provide a scripted workflow with explicit state transitions, token tracking, and additional tooling (CLI prompts, matplotlib visualizations, dynamic Streamlit launcher). Ideal for experimentation, automated testing, or non-UI deployments.

### 3.2 Flow Summary
1. **`main_universal.py`** parses CLI args, prints workflow summaries, checks LangSmith flags, and invokes the LangGraph graph for description-based extraction.
2. **LangGraph Construction (`graph.py`)** uses `StateGraph(ConceptMapState)` to wire `extract_all_in_one_call` followed by `initialize_legacy_fields`. It compiles to a runnable graph consumed by the CLI.
3. **Node Logic (`nodes.py`)** hosts the full node implementations:
   - `extract_all_in_one_call()` combines concept/relationship/hierarchy extraction via a single Gemini call, logging processing decisions and token usage via `token_tracker.py`.
   - `analyze_concept_relationships()`, `build_concept_hierarchy()`, and `enrich_with_educational_metadata()` remain for legacy multi-node flows.
   - Utility functions sanitize JSON, chunk descriptions, and enrich outputs.
4. **State Definition (`states.py`)** enumerates every field stored in `ConceptMapState`, ensuring compatibility between nodes and visualizers.
5. **Visualization (`graph_visualizer.py`)** can render saved JSON concept maps, while **`dynamic_orchestrator.py`** ties timeline creation, `PrecomputeEngine.precompute_all()`, and `streamlit_visualizer_enhanced.py` into a scripted experience.
6. **Token Tracking (`token_tracker.py`)** approximates Gemini token usage, logs per-node totals, and estimates cost.

### 3.3 File Reference Table
| File | Responsibility |
| --- | --- |
| `main_universal.py` | CLI entry point. Handles TTS narration (via `tts_handler.py`), prompts user for mode (static vs dynamic), triggers LangGraph execution, prints summaries, and can launch dynamic orchestrator. |
| `graph.py` | Builds/compiles the LangGraph `StateGraph`. Defines the ultra-optimized 1-node flow (combined extraction + legacy initialization) and exposes helper functions (`print_description_based_workflow_summary`). |
| `nodes.py` | Contains all LangGraph node functions plus helpers for prompt construction, JSON cleaning, fallback logic, and logging. Integrates `description_analyzer.py` and `token_tracker.py`. |
| `states.py` | TypedDict describing every state attribute (inputs, analysis, extracted data, enrichment, metadata, errors). Ensures nodes share a consistent contract. |
| `dynamic_orchestrator.py` | High-level script that: (1) calls `create_timeline`, (2) precomputes assets, (3) writes timeline JSON to temp files, (4) spawns Streamlit using an auto-generated runner script, and (5) cleans up temp artifacts. |
| `streamlit_visualizer_enhanced.py` | Standalone Streamlit component used by the orchestrator. Supports precomputed layouts, pygame-based audio, fade/pop animations, custom color palettes by concept type, and edge relationship labelling. |
| `graph_visualizer.py` | Offline matplotlib visualizer for saved concept map JSON files. Supports hierarchical layouts, statistics gathering, and PNG export. |
| `token_tracker.py` | Estimates tokens per node, aggregates totals, computes cost, and logs a summary banner. Used inside `nodes.py` and `main_universal.py`. |

### 3.4 Execution Narrative
1. **CLI Invocation**: `python main_universal.py --description "..." --level "high school" --dynamic` (flags vary per README).
2. **Workflow Summary**: The script warns if LangSmith tracing is disabled, narrates the description via `tts_handler.py`, then submits the description to the LangGraph workflow.
3. **LangGraph Execution**: The compiled graph runs `combined_extraction` to populate `ConceptMapState` with extracted data, then sets legacy fields for backward compatibility.
4. **Post-processing**: Depending on flags, the script may export JSON, call `ConceptMapVisualizer` to save PNGs, or invoke `dynamic_orchestrator.run_dynamic_mode()` for live playback.
5. **Dynamic Mode**: The orchestrator regenerates the timeline (reusing the same single-call approach), precomputes audio/layout, writes `concept_map_timeline.json` to a temp directory, and spawns `streamlit_visualizer_enhanced.py` via a temporary runner so users can watch the enhanced visualization in a browser.
6. **Cleanup**: `dynamic_orchestrator.cleanup_temp_files()` runs on exit to delete the runner script and timeline JSON.

### 3.5 Token & Metrics Strategy
- `token_tracker.py` tracks per-node token estimates and surfaces totals/costs to the CLI.
- Timeline generation still logs to `metrics_logger.py`, so both systems share the same JSON metrics store.
- LangSmith can be enabled via `.env` (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_PROJECT`) so the CLI workflow appears in the same tracing workspace as the Streamlit app.

### 3.6 Running the LangGraph System
```bash
# Example: run CLI workflow with narration and dynamic visualization
env GOOGLE_API_KEY=... LANGCHAIN_API_KEY=... \
python main_universal.py \
    --description "Photosynthesis is ..." \
    --educational-level "high school" \
    --dynamic
```
Refer to `README.md` and `QUICKSTART_CHARACTER_BASED.md` for full CLI flags and sample commands.

---

## 4. Workflow Differences & Dynamic Mode Behavior

### 4.1 Streamlit vs. LangGraph Execution Flow
| Step | Streamlit Standalone (UI-first) | LangGraph Workflow (CLI-first) |
| --- | --- | --- |
| 1 | `streamlit_app_standalone.py` loads `.env`, renders UI, waits for the user to click **Generate Concept Map**. | `main_universal.py` parses CLI flags, optionally narrates the prompt (via `tts_handler.py`), and constructs `ConceptMapState`. |
| 2 | `description_analyzer.py` + `complexity_config.py` size the request (target concept count, pacing). | Same analyzer helpers run inside `nodes.py` to tune prompts per description. |
| 3 | `timeline_mapper.py` issues a **single Gemini call** that already includes reveal timestamps, narration sentences, keyword hits, and metadata tailored for animation. | `graph.py` runs `nodes.py` (usually `extract_all_in_one_call`) to fill `ConceptMapState` with concepts, relationships, hierarchy, enrichment data—optimized for static inspection/export. |
| 4 | `precompute_engine.py` (and optionally `tts_handler.py`) generate audio + layout before visualization. | `main_universal.py` saves the LangGraph results to `output/*.json`, optionally plots with `graph_visualizer.py`. |
| 5 | Visualization and playback happen immediately in Streamlit (matplotlib drawing + audio synced reveals). | **Dynamic mode only**: `main_universal.py` imports `dynamic_orchestrator.py`, which *re-enters* the Streamlit stack by calling `timeline_mapper.py` and `precompute_engine.py` again before launching `streamlit_visualizer_enhanced.py`. |

### 4.2 Why Dynamic Mode Triggers Another API Call
- LangGraph’s output (`ConceptMapState` → JSON) lacks the sentence-level timing and audio-ready metadata that the Streamlit animator expects.
- `dynamic_orchestrator.run_dynamic_mode()` therefore rebuilds a timeline by calling `timeline_mapper.create_timeline(...)` again, ensuring reveal timestamps, narration text, and layout hints exist for the enhanced visualizer.
- This means the **LangGraph run + dynamic mode** path performs two Gemini requests: one inside `nodes.py`, and a second inside `timeline_mapper.py`. The first call is never wasted (it produces the static JSON and metrics), but its result isn’t currently transformed into the timeline format.
- To avoid the duplicate call in the future, a contributor would need to add a converter that maps `ConceptMapState` → timeline schema, letting the orchestrator reuse LangGraph output instead of invoking `timeline_mapper.py`.

### 4.3 When to Use Each Path
- Choose **Streamlit standalone** when you want the fastest path from prompt to animated concept map (single API call, self-contained UI).
- Choose **LangGraph** when you need scripted runs, LangSmith tracing, token accounting, or headless exports—and optionally bolt on the dynamic Streamlit experience afterward via the orchestrator.

---

## 5. Shared Utilities, Configuration, and Documentation
| Artifact | Description |
| --- | --- |
| `.env` | Stores sensitive keys (`GOOGLE_API_KEY`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`). Never committed; `.gitignore` keeps it private. |
| `.gitignore` / `.gitattributes` | Ignore rules (e.g., `.env`, `metrics_logs/`, temp audio) and Git attributes (line endings). |
| `requirements.txt` | Single source of Python dependencies (Streamlit, google-generativeai, gTTS, pygame, matplotlib, networkx, langsmith, mutagen, etc.). Install this for both systems. |
| `README.md` | Landing page with summary, prerequisites, and quick instructions. |
| `QUICKSTART_CHARACTER_BASED.md` | Walkthrough focused on the character-based timing approach. |
| `STANDALONE_APP_README.md` | Additional notes for the Streamlit UI (controls, tips, troubleshooting). |
| `METRICS_README.md` | Deep dive into the metrics subsystem and usage of `view_metrics.py`. |
| `metrics_logs/` | JSON datastore generated at runtime. Safe to delete; recreated automatically. |

---

## 6. Complete File Inventory (Alphabetical)
| File / Directory | System(s) | Summary |
| --- | --- | --- |
| `.env` | Both | Environment variables (keys, tracing flags). |
| `.gitattributes` | Both | Git text/binary rules and LF normalization. |
| `.gitignore` | Both | Ignores `.env`, `metrics_logs/`, temp files, caches. |
| `complexity_config.py` | Shared | Placeholder for overrides of analysis/timing constants referenced by `description_analyzer.py`. |
| `description_analyzer.py` | Shared | Complexity analysis, topic extraction, education-level adjustments. |
| `dynamic_orchestrator.py` | LangGraph system | Automates timeline creation, asset precomputation, Streamlit launch, cleanup. |
| `graph.py` | LangGraph system | LangGraph workflow definition + print helpers. |
| `graph_visualizer.py` | LangGraph system | Matplotlib-based concept map renderer for saved JSON outputs. |
| `main_universal.py` | LangGraph system | CLI entry, LangGraph execution, narration, optional dynamic mode launch. |
| `metrics_logger.py` | Shared | Local metrics writer (tokens, timing, outputs) to `metrics_logs/`. |
| `metrics_logs/` | Shared | JSON metrics directory (auto-created, git-ignored). |
| `METRICS_README.md` | Shared | Documentation for the metrics subsystem. |
| `nodes.py` | LangGraph system | LangGraph node implementations (combined extraction, relationship analysis, enrichment). |
| `precompute_engine.py` | Both | gTTS audio generation, character-based timing, smart-grid layout, edge filtering, asset bundling. |
| `PROJECT_DOCUMENTATION.md` | Shared | This document. |
| `QUICKSTART_CHARACTER_BASED.md` | Shared | Step-by-step quickstart using character-based timing. |
| `README.md` | Shared | Project overview and initial instructions. |
| `requirements.txt` | Shared | Dependency manifest for both systems. |
| `STANDALONE_APP_README.md` | Streamlit system | Detailed tips for using the single-page Streamlit app. |
| `states.py` | LangGraph system | TypedDict defining the LangGraph state contract. |
| `streamlit_app_standalone.py` | Streamlit system | One-page Streamlit application orchestrating timeline creation, audio, and visualization. |
| `streamlit_visualizer_enhanced.py` | LangGraph system | Enhanced Streamlit component used by the dynamic orchestrator. |
| `timeline_mapper.py` | Both | Core timeline generation module (Gemini prompt, parsing, reveal-time computation, metrics logging). |
| `token_tracker.py` | LangGraph system | Token estimation + logging utilities. |
| `tts_handler.py` | Both | Text-to-speech helper (pyttsx3) for CLI narration. |
| `view_metrics.py` | Shared | CLI tool for inspecting JSON metrics.

---

## 7. Next Steps
- Use this document as the authoritative map when onboarding contributors.
- Update it whenever new modules are added or flows change so both systems stay documented.
- Pair it with the existing READMEs (main, quickstart, metrics, standalone) for task-specific instructions.
