# API-backed topic search POC

The screen stays in `Streamlit_UI/search_app.py`. It calls a running main
education API for search, teaching and doubts. It never invokes a tutor graph,
model or database directly. `search_client.py` handles HTTP requests only.

## Configuration

Set these in Streamlit Secrets or the Streamlit process environment:

```toml
EDUCATION_API_BASE_URL = "https://your-education-api.example.com"
EDUCATION_API_KEY = "your-main-backend-access-key"
```

The URL is the base address, without `/search` or `/docs`. The access key must
match one of the backend's `X_API_KEYS`; it is **not** a Gemini key. Credentials
are sent server-side through `X-API-Key` and are not printed. Use HTTPS when
connecting over the internet. Do not commit real secrets.

For a local API use `http://127.0.0.1:8000`. A hosted Streamlit app must use the
reachable AWS/backend address; localhost there refers to its own machine.

From the main repository, run:

```powershell
python -X utf8 -m streamlit run Streamlit_UI/search_app.py --server.port 8503
```

The frontend needs Streamlit, requests and python-dotenv. Gemini keys, model
selection, request tracking, LangSmith and Postgres belong on the API server.
The existing backend must include the new `/search` endpoint. No image was
built or deployed by this change.

## Whiteboard rendering dependency

Search, regular-tutor chat and doubts do not import the local agent packages.
To display whiteboard visuals, the Streamlit host additionally needs the
matching `whiteboard_tutor` package, its dependencies and bundled SVG assets.
In this workspace the app finds the sibling `Whiteboard_Tutor_Education_POC`
folder. The main Docker image already copies that package during its normal
BuildKit build. If Streamlit is hosted separately (including Streamlit Cloud),
that host must also be supplied with the package/assets; pointing at an API
does not install a frontend renderer. If missing, chat still works and the
screen displays a warning instead of the board. No local LLM is called.

## Requests

| Action | Endpoint |
| --- | --- |
| Search/suggestions | `GET /search` |
| Science start/continue | `POST /session/start`, `POST /session/continue` |
| Maths start/continue | `POST /math/session/start`, `POST /math/session/continue` |
| Whiteboard start/continue | `POST /whiteboard-tutor/session/start`, `POST /whiteboard-tutor/session/continue` |
| Submitted doubt | `POST /doubts` |

Maths continuation uses form fields; the other start/continue requests use
JSON. The client retains `thread_id` and normalizes the different turn formats.
No session is started by searching. A doubt form must be submitted before it
calls the backend. The panel supports text chat, not the complete simulation UI.

Try `science`, `maths`, `give five random topics`, `photosynthesis`,
`photosynthesis whiteboard`, `photosynthesis manual` or `photosynthesis help`.
Filters override inferred words. Unknown queries return no unrelated results
and offer the general doubt form. Search is cached catalog matching, not an LLM.

## Files and behaviour

- `Streamlit_UI/search_app.py`: search form, cards and learning panel.
- `Streamlit_UI/search_client.py`: HTTP calls, authentication, response formats
  and connection/quota errors. The local `search_tutors.py` has been removed.
- `api_servers/search_service.py`: backend catalog matching.
- `utils/problem_catalog.py`: shared maths catalog parser, used by the backend.
- `utils/shared_utils.py`: existing LLM helpers and the backend's doubt helper.

Search results survive failed learning requests. Requests are not automatically
retried: a timeout can occur after the backend has already advanced a session.
Authentication and HTTP 501/502 quota errors retain their existing backend
behaviour. Keep access to this trusted-user demo restricted: anyone with access
to its UI can initiate requests using its server-side backend access key.

The science/maths graph changes made for the direct-call experiment have been
reverted. Existing standalone whiteboard science/maths apps are unchanged.
