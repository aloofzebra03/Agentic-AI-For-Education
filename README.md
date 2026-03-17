# Agentic AI For Education

## Project Status

This repository now contains the active, trimmed codebase.

- Active components remain here (APIs, v5/dynamic agents, revision agent, simulation-to-concept, load tests, shared utilities).
- Older/experimental files that are no longer in this repo have been moved to a separate legacy repository.
- If you need historical code, point developers to the legacy repo link used by your team.

## What Is In This Repo

### Core agents

- `educational_agent_optimized_langsmith_v5/`
  - Static autosuggestions variant.
- `educational_agent_optimized_langsmith_autosuggestion/`
  - Dynamic autosuggestions variant.
- `revision_agent/`
  - Exam/revision-focused agent with chapter question banks.

### Serving layer

- `api_servers/api_server_v5.py`
  - API for v5 graph plus simulation and revision endpoints.
- `api_servers/api_server.py`
  - API for dynamic autosuggestion graph plus simulation endpoints.
- `api_servers/schemas.py`
  - Shared request/response models.

### Simulation-to-concept module

- `simulation_to_concept/`
  - Simulation teaching API integration and quiz evaluation flow.
- `simulation_to_concept_old/`
  - Older snapshot retained for reference.

### UI

- `Streamlit_UI/app_agent_v5.py`
- `Streamlit_UI/revision_app.py`

### Shared and support modules

- `autosuggestion/`
- `utils/`
- `api_tracker_utils/`
- `tester_agent/`
- `concept_map_poc/`
- `science_jsons/`

### Load testing

- `load_tests/locustfile.py`
- `load_tests/tasks/session_tasks.py` (regular teaching session flow)
- `load_tests/tasks/session_tasks_simulation.py` (simulation-only flow)
- `load_tests/tasks/session_tasks_mixed.py` (calls both flows)
- `load_tests/config.py` with `LOAD_TEST_TASK_MODE`

## Legacy Migration Note

The previous broad codebase (older agent variants, legacy Streamlit apps, old experiments) has been moved out of this repository.

- This README intentionally documents only what currently exists in this repo.
- Add your internal/external legacy repository URL here for discoverability.

Example placeholder:

```text
Legacy repository: <add-legacy-repo-url>
```

## Architecture Summary

1. Student interaction goes through FastAPI endpoints.
2. FastAPI invokes LangGraph-based teaching/revision flows.
3. Shared utilities handle translation, prompt/history shaping, and helper functions.
4. Session persistence is checkpointer-backed for teaching agents (Postgres in v5 flow), while revision currently uses in-memory checkpointer behavior.
5. Simulation endpoints use `simulation_to_concept` orchestration for parameterized concept teaching and quiz evaluation.

## API Servers And Endpoints

## `api_server_v5.py` (port 8000)

Base educational endpoints:

- `GET /`
- `GET /health`
- `GET /concepts`
- `POST /session/start`
- `POST /session/continue`
- `GET /session/status/{thread_id}`
- `GET /session/history/{thread_id}`
- `GET /session/summary/{thread_id}`
- `DELETE /session/{thread_id}`

Testing/helper endpoints:

- `GET /test/personas`
- `POST /test/persona`
- `POST /test/images`
- `POST /test/simulation`
- `POST /concept-map/generate`

Simulation endpoints:

- `GET /simulation`
- `POST /simulation/session/start`
- `POST /simulation/session/{session_id}/respond`
- `POST /simulation/session/{session_id}/submit-quiz`
- `GET /simulation/session/{session_id}`
- `GET /simulation/simulations`

Revision endpoints (present in v5 server):

- `GET /revision/chapters`
- `POST /revision/session/start`
- `POST /revision/session/continue`
- `GET /revision/session/status/{thread_id}`
- `GET /revision/session/history/{thread_id}`
- `DELETE /revision/session/{thread_id}`

Translation endpoints (v5):

- `POST /translate/to-kannada`
- `POST /translate/to-english`

## `api_server.py` (port 8001)

Provides the same main teaching and simulation flow as above, but uses the dynamic autosuggestion graph and currently exposes:

- `POST /translate` (Kannada translation endpoint in this server)

If you run both servers side by side, treat v5 as the fuller API surface (revision + dual translation routes).

## Running Services

### Python setup

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Alternative requirements files available:

- `requirements-minimal.txt`
- `requirements_simple.txt`
- `requirements_with_streamlit_audio_video.txt`

### Start API servers

```bash
# V5 static autosuggestion server
uvicorn api_servers.api_server_v5:app --host 0.0.0.0 --port 8000 --reload

# Dynamic autosuggestion server
uvicorn api_servers.api_server:app --host 0.0.0.0 --port 8001 --reload
```

### Start Streamlit apps

```bash
streamlit run Streamlit_UI/app_agent_v5.py
streamlit run Streamlit_UI/revision_app.py
```

## Load Testing

`load_tests/locustfile.py` now supports mode selection through environment variable:

- `LOAD_TEST_TASK_MODE=regular`
- `LOAD_TEST_TASK_MODE=simulation`
- `LOAD_TEST_TASK_MODE=mixed`

Default mode is `mixed`.

Examples (PowerShell):

```powershell
$env:LOAD_TEST_TASK_MODE="mixed"
locust -f load_tests/locustfile.py --host http://localhost:8000
```

```powershell
$env:LOAD_TEST_TASK_MODE="simulation"
locust -f load_tests/locustfile.py --host http://localhost:8000
```

```powershell
$env:LOAD_TEST_TASK_MODE="regular"
locust -f load_tests/locustfile.py --host http://localhost:8000
```

Note: `load_tests/locustfile.py` attempts to call `/test/api-key-metrics` at test stop. If your running API server does not expose this endpoint, Locust will print a non-fatal error during report export.

## Key Environment Variables

Create `.env` with values used by your deployment:

```env
# Gemini keys (tracker can rotate across keys)
GOOGLE_API_KEY_1=...
GOOGLE_API_KEY_2=...

# Azure translator
AZURE_TRANSLATOR_KEY=...

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=...
LANGCHAIN_API_KEY=...

# Postgres checkpointer
POSTGRES_DATABASE_URL=postgresql://...
```

Additional settings may be required depending on which modules/endpoints you run.

## Notes On Historical References

- `main.py` references `educational_agent_with_simulation`, which is not part of the active top-level package layout in this trimmed repository.
- `pyproject.toml` still contains historical package include entries from older layouts.

If needed, clean these references as part of repository housekeeping; they do not change the current API-first runtime paths documented above.

## Recommended Entry Points

For day-to-day usage, use these entry points first:

1. `api_servers/api_server_v5.py`
2. `api_servers/api_server.py`
3. `Streamlit_UI/app_agent_v5.py`
4. `Streamlit_UI/revision_app.py`
5. `load_tests/locustfile.py`

## Repository Snapshot (Top Level)

Current important top-level folders/files include:

- `api_servers/`
- `api_tracker_utils/`
- `autosuggestion/`
- `concept_map_poc/`
- `educational_agent_optimized_langsmith_autosuggestion/`
- `educational_agent_optimized_langsmith_v5/`
- `load_tests/`
- `revision_agent/`
- `science_jsons/`
- `simulation_to_concept/`
- `simulation_to_concept_old/`
- `Streamlit_UI/`
- `tester_agent/`
- `utils/`
- `README.md`

This list is intentionally practical rather than exhaustive.
