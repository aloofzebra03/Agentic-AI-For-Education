# General doubt endpoint

`POST /doubts` is implemented directly in `api_servers/api_server_v5.py`.
The request/response models are in `api_servers/schemas.py`; the prompt and
endpoint function stay in the main API file. The endpoint calls the existing
`utils.shared_utils.invoke_llm_with_fallback()` helper, which selects a tracked
key/model, records the call, invokes Gemini once, and normalizes its response.
Authentication and the existing quota responses remain at the API layer.

Request:

```json
{
  "question": "Why do we have leap years?",
  "context": "Optional background or previous explanation"
}
```

`question` is required (1-4000 characters with visible text). `context` is
optional (up to 8000 characters). No subject, concept, or session ID is required.
The prompt accepts general doubts across subjects and adapts to the question.

Response:

```json
{
  "success": true,
  "answer": "A year does not last exactly 365 days..."
}
```

```powershell
$headers = @{ 'X-API-Key' = '<your existing endpoint access key>' }
$body = @{ question = 'Why do we have leap years?' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/doubts' `
  -Headers $headers -ContentType 'application/json' -Body $body
```

Existing Bearer authentication also works. The endpoint uses
`get_current_user_rate_limited`: authentication failures return `401/403`,
the student's daily allowance returns `429`, and tracked Gemini minute/day
exhaustion returns `501/502`. Invalid input returns `422`; unexpected LLM
failures return a structured `500` without exposing internal details.

Rebuild and redeploy the main image to make this route available on the server.
