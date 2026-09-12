# Whiteboard Tutor in the Main API Image

The whiteboard implementation remains in the sibling
`Whiteboard_Tutor_Education_POC` repository. Docker copies its reusable
`whiteboard_tutor` package at build time; no second copy is committed here.

## Build

Both repositories must be side by side. From `Agentic-AI-For-Education` run:

```powershell
docker build `
  --build-context whiteboard_poc=../Whiteboard_Tutor_Education_POC `
  -t educational-api:whiteboard .
```

BuildKit must be enabled. In CI, check out both repositories and pin the POC
checkout to the desired commit before building.

For running the main API directly from Python instead of Docker, install the
sibling package once in the active environment:

```powershell
python -m pip install -e ../Whiteboard_Tutor_Education_POC
```

## Run

```powershell
docker run --rm `
  --name educational-api `
  --env-file .env `
  -p 8000:8000 `
  educational-api:whiteboard
```

The main API still requires its usual Postgres, authentication, numbered
`GOOGLE_API_KEY_*`, and tracker settings. Whiteboard sessions use the shared
Postgres checkpointer. Use one Uvicorn worker for this POC because request locks
are process-local.

## Call the API

Supply either the existing `X-API-Key` header or Bearer token:

```powershell
$base = 'http://127.0.0.1:8000/whiteboard-tutor'
$headers = @{ 'X-API-Key' = 'your-existing-api-key' }

$concepts = Invoke-RestMethod -Headers $headers -Uri "$base/concepts"

$start = Invoke-RestMethod -Method Post -Headers $headers `
  -ContentType 'application/json' -Uri "$base/session/start" `
  -Body (@{ concept_id='ch10-1'; student_id='android-001' } | ConvertTo-Json)

$threadId = $start.thread_id
$turn = Invoke-RestMethod -Method Post -Headers $headers `
  -ContentType 'application/json' -Uri "$base/session/continue" `
  -Body (@{ thread_id=$threadId; user_message='Plants use sunlight.' } | ConvertTo-Json)

$status = Invoke-RestMethod -Headers $headers -Uri "$base/session/status/$threadId"
$history = Invoke-RestMethod -Headers $headers -Uri "$base/session/history/$threadId"
$manifest = Invoke-RestMethod -Headers $headers -Uri "$base/scenes/manifest"
```

Reset only the board:

```powershell
Invoke-RestMethod -Method Post -Headers $headers `
  -Uri "$base/session/$threadId/whiteboard/reset"
```

Delete the whole session:

```powershell
Invoke-RestMethod -Method Delete -Headers $headers `
  -Uri "$base/session/$threadId"
```

Relevant errors are `401/403` for authentication/ownership, `404` for missing
resources, `409` for a busy or completed session, `422` for invalid input,
`501` when all tracked key/model pairs have exhausted their minute allowance,
`502` when they have exhausted their daily allowance, and `500` otherwise.
