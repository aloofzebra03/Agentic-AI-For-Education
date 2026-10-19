# Educational API v9.9.5

Published to Docker Hub on 12 October 2026 (IST):

- `aloofzebra03/educational-api:v9.9.5`
- `aloofzebra03/educational-api:latest`

Both tags resolve to:

`sha256:84968d854ebd09dd7ad690e4458d6d28939d5dbb7f8d71daebab1713ff744b8a`

## Source and update scope

This release uses `Dockerfile.code-update`, based on the existing `v9.9.4`
image. All 26 original layers were verified as retained. New layers replace
`/app/api_servers`, `/app/utils`, and `/app/whiteboard_tutor`. Other agent folders
and installed dependencies come from the existing release.

- Main source commit: `ebd26f4`.
- Whiteboard source commit: `eabb819`.
- Whiteboard catalog: 25 scenes (16 science and 9 maths).
- General doubts: `POST /doubts`, directly in the main FastAPI file, using
  schemas from `api_servers/schemas.py` and the shared tracked LLM helper.

The normal Dockerfile was also built locally during preparation, but its image
was replaced at the release tag by the verified code-update candidate before
publication. The published tags contain the code-update image above.

## Build commands

Run from `Agentic-AI-For-Education`, with both repositories side by side:

```powershell
docker build -f Dockerfile.code-update `
  --build-context whiteboard_poc=../Whiteboard_Tutor_Education_POC `
  --label org.opencontainers.image.version=v9.9.5 `
  --label org.opencontainers.image.revision=ebd26f4 `
  --label education.whiteboard.revision=eabb819 `
  -t aloofzebra03/educational-api:v9.9.5 .

docker tag aloofzebra03/educational-api:v9.9.5 aloofzebra03/educational-api:latest
docker push aloofzebra03/educational-api:v9.9.5
docker push aloofzebra03/educational-api:latest
```

The commands above have already been run for this release. Rebuilding later
uses the then-current repository files, so retain the source commits for an
exact reproduction.

## Pull and run on the server

```powershell
docker pull aloofzebra03/educational-api:v9.9.5
docker run -d --name educational-api --env-file .env -p 8000:8000 `
  aloofzebra03/educational-api:v9.9.5
```

Use the server's existing `.env` with Postgres, authentication, and numbered
Gemini keys. If the server already has a container with this name, replace it
through its normal deployment workflow before running the command.

## Verification performed inside the release candidate

- The complete main API imported successfully with its existing graph modules.
- Health and the science, maths, revision, simulation, and whiteboard catalog
  routes returned 200; existing start/continue routes remain registered.
- All 25 SVG endpoints returned `image/svg+xml`; manifest checksums and required
  part IDs matched.
- Doubt requests returned the expected 200, 401, 422, 501, and 502 responses.
- Science and maths whiteboard sessions supported start, status, history,
  board reset, and deletion, with reveal timelines present.

These smoke checks used an in-memory checkpointer and a mock LLM inside the
container. Production Postgres persistence and live Gemini calls were not
exercised for this release. Existing non-fatal warnings from legacy concept-map
imports appeared; they did not prevent API loading or endpoint checks.

Remote Docker Hub tag digests were checked after both pushes and matched.
Publishing the image does not replace the running container on a remote server.
