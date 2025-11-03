# Educational Agent API Server

FastAPI-based REST API for the Educational Agent (`educational_agent_optimized_langsmith`). Provides stateful, personalized learning experiences with persistent conversation management using LangGraph checkpoints.

## 🚀 Quick Start

### Installation

1. Ensure all dependencies are installed:
```bash
pip install fastapi uvicorn
```

2. Make sure the educational agent package is in your Python path (already configured in the API server)

### Running the Server

From the `api_servers` directory:
```bash
python api_server.py
```

Or from the project root:
```bash
python api_servers/api_server.py
```

The server will start on `http://0.0.0.0:8000`

### Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### 1. **Root Endpoint**
```http
GET /
```

Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Educational Agent API is running!",
  "version": "1.0.0",
  "agent_type": "educational_agent_optimized_langsmith",
  "endpoints": [...]
}
```

---

### 2. **Health Check**
```http
GET /health
```

Check API health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "persistence": "InMemorySaver (LangGraph)",
  "agent_type": "educational_agent_optimized_langsmith",
  "available_endpoints": [...]
}
```

---

### 3. **Start New Session**
```http
POST /session/start
```

Initialize a new learning session with the educational agent.

**Request Body:**
```json
{
  "concept_title": "Pendulum and its Time Period",
  "student_id": "student_123",
  "persona_name": "Curious Student",
  "session_label": "my-session"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `concept_title` | string | Yes | The concept to teach |
| `student_id` | string | No | Student identifier for tracking |
| `persona_name` | string | No | Persona name for testing |
| `session_label` | string | No | Custom session label |

**Response:**
```json
{
  "success": true,
  "session_id": "my-session-20250103-143022",
  "thread_id": "my-session-thread-20250103-143022",
  "user_id": "student_123",
  "agent_response": "Hello! Welcome to learning about Pendulum and its Time Period. Are you ready to begin?",
  "current_state": "APK",
  "concept_title": "Pendulum and its Time Period",
  "message": "Session started successfully. Agent is ready for student input.",
  "metadata": {}
}
```

**Important:** Save the `thread_id` - you'll need it for all subsequent requests!

---

### 4. **Continue Session**
```http
POST /session/continue
```

Send student's message and get agent's response. This is the main interaction endpoint.

**Request Body:**
```json
{
  "thread_id": "my-session-thread-20250103-143022",
  "user_message": "Yes, I'm ready to learn!"
}
```

**Response:**
```json
{
  "success": true,
  "thread_id": "my-session-thread-20250103-143022",
  "agent_response": "Great! Let me ask you a question...",
  "current_state": "APK",
  "metadata": {
    "quiz_score": 85.0,
    "sim_concepts": ["oscillation", "frequency", "amplitude"],
    "sim_current_idx": 0,
    "sim_total_concepts": 3,
    "show_simulation": false
  },
  "message": "Response generated successfully"
}
```

**Metadata Fields:**

| Field | Description |
|-------|-------------|
| `show_simulation` | Boolean - if true, Android app should start simulation |
| `simulation_config` | Dict - configuration for which simulation to run |
| `enhanced_message_metadata` | Dict - contains image URLs and other media |
| `quiz_score` | Float - student's quiz performance (0-100) |
| `sim_concepts` | List - concepts being explored |
| `sim_current_idx` | Int - current concept index |
| `misconception_detected` | Boolean - if misconception was identified |
| `last_correction` | String - correction provided for misconception |
| `node_transitions` | List - pedagogical state transitions |

**Simulation Response Example:**
```json
{
  "success": true,
  "thread_id": "...",
  "agent_response": "Let's explore this with a simulation!",
  "current_state": "SIM_VARS",
  "metadata": {
    "show_simulation": true,
    "simulation_config": {
      "type": "pendulum_simulation",
      "variables": [
        {"name": "length", "role": "independent", "note": "Length of pendulum string"},
        {"name": "period", "role": "dependent", "note": "Time for one swing"}
      ]
    }
  }
}
```

**Image Response Example:**
```json
{
  "metadata": {
    "enhanced_message_metadata": {
      "image": {
        "url": "https://example.com/pendulum.png",
        "caption": "Simple pendulum diagram",
        "relevance_score": 0.95
      },
      "node": "CI"
    }
  }
}
```

---

### 5. **Get Session Status**
```http
GET /session/status/{thread_id}
```

Get current status and progress of a learning session.

**Response:**
```json
{
  "success": true,
  "thread_id": "my-session-thread-20250103-143022",
  "exists": true,
  "current_state": "GE",
  "progress": {
    "current_state": "GE",
    "asked_apk": true,
    "asked_ci": true,
    "asked_ge": true,
    "asked_ar": false,
    "asked_tc": false,
    "asked_rlc": false,
    "concepts": ["oscillation", "frequency", "amplitude"],
    "current_concept_idx": 1,
    "total_concepts": 3,
    "in_simulation": false,
    "misconception_detected": false
  },
  "concept_title": "Pendulum and its Time Period",
  "message": "Status retrieved successfully"
}
```

**Pedagogical States:**
- `START` - Initial greeting
- `APK` - Activate Prior Knowledge
- `CI` - Concept Introduction
- `GE` - Guided Exploration
- `SIM_CC` - Simulation Concept Creator
- `SIM_VARS` - Simulation Variables
- `SIM_ACTION` - Simulation Action
- `SIM_EXPECT` - Simulation Expectation
- `SIM_EXECUTE` - Simulation Execute
- `SIM_OBSERVE` - Simulation Observe
- `SIM_INSIGHT` - Simulation Insight
- `SIM_REFLECT` - Simulation Reflection
- `AR` - Application & Retrieval (Quiz)
- `TC` - Transfer & Critical Thinking
- `RLC` - Real-Life Context
- `END` - Session Summary

---

### 6. **Get Session History**
```http
GET /session/history/{thread_id}
```

Retrieve full conversation history with all messages and node transitions.

**Response:**
```json
{
  "success": true,
  "thread_id": "my-session-thread-20250103-143022",
  "exists": true,
  "messages": [
    {
      "role": "user",
      "content": "Yes, I'm ready!"
    },
    {
      "role": "assistant",
      "content": "Great! Let me ask you...",
      "node": "APK"
    }
  ],
  "node_transitions": [
    {
      "from_node": "START",
      "to_node": "APK",
      "transition_after_message_index": 2
    }
  ],
  "concept_title": "Pendulum and its Time Period",
  "message": "History retrieved successfully"
}
```

---

### 7. **Get Session Summary**
```http
GET /session/summary/{thread_id}
```

Get session metrics and performance indicators.

**Response:**
```json
{
  "success": true,
  "thread_id": "my-session-thread-20250103-143022",
  "exists": true,
  "summary": {
    "quiz_score": 0.85,
    "transfer_success": true,
    "definition_echoed": true,
    "misconception_detected": false,
    "last_user_msg": "That makes sense now!"
  },
  "quiz_score": 85.0,
  "transfer_success": true,
  "misconception_detected": false,
  "definition_echoed": true,
  "message": "Summary retrieved successfully"
}
```

---

### 8. **Delete Session**
```http
DELETE /session/{thread_id}
```

Remove session from active sessions. Note: LangGraph checkpoint may still persist.

**Response:**
```json
{
  "success": true,
  "thread_id": "my-session-thread-20250103-143022",
  "message": "Session deleted successfully"
}
```

---

### 9. **Test with Persona**
```http
POST /test/persona
```

Create a test session with predefined student persona for automated testing.

**Request Body:**
```json
{
  "persona_name": "Confused Student",
  "concept_title": "Pendulum and its Time Period"
}
```

**Supported Personas:**
- `"Confused Student"`
- `"Distracted Student"`
- `"Dull Student"`
- `"Curious Student"`
- Or any custom persona name

**Response:** Same as `/session/start`

---

### 10. **List Active Sessions**
```http
GET /sessions
```

Debug endpoint to list all currently active sessions.

**Response:**
```json
{
  "success": true,
  "total_sessions": 3,
  "sessions": [
    {
      "thread_id": "session-1-thread-...",
      "session_id": "session-1-...",
      "user_id": "student_123",
      "current_state": "GE",
      "persona_name": "Curious Student"
    }
  ]
}
```

---

## 🔄 Typical Usage Flow

### Example: Complete Learning Session

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Start session
start_response = requests.post(f"{BASE_URL}/session/start", json={
    "concept_title": "Pendulum and its Time Period",
    "student_id": "student_456"
})
thread_id = start_response.json()["thread_id"]
print(start_response.json()["agent_response"])

# 2. Continue conversation
continue_response = requests.post(f"{BASE_URL}/session/continue", json={
    "thread_id": thread_id,
    "user_message": "Yes, I'm ready to learn!"
})
print(continue_response.json()["agent_response"])

# 3. Check if simulation needed
metadata = continue_response.json()["metadata"]
if metadata.get("show_simulation"):
    print("⚠️ Start simulation:", metadata["simulation_config"])

# 4. Get status
status = requests.get(f"{BASE_URL}/session/status/{thread_id}")
print(f"Current state: {status.json()['current_state']}")

# 5. Get history
history = requests.get(f"{BASE_URL}/session/history/{thread_id}")
print(f"Total messages: {len(history.json()['messages'])}")

# 6. Get summary (when session ends)
summary = requests.get(f"{BASE_URL}/session/summary/{thread_id}")
print(f"Quiz score: {summary.json()['quiz_score']}")
```

---

## 🤖 Android App Integration

### Key Integration Points

1. **Starting a Session:**
```kotlin
val response = apiService.startSession(
    StartSessionRequest(
        conceptTitle = "Pendulum and its Time Period",
        studentId = userId
    )
)
val threadId = response.threadId
// Display: response.agentResponse
```

2. **Continuing Conversation:**
```kotlin
val response = apiService.continueSession(
    ContinueSessionRequest(
        threadId = threadId,
        userMessage = userInput
    )
)

// Display agent response
textView.text = response.agentResponse

// Check for simulation trigger
if (response.metadata.showSimulation == true) {
    val config = response.metadata.simulationConfig
    startSimulation(config)
}

// Check for images
response.metadata.enhancedMessageMetadata?.image?.let { image ->
    loadImage(image.url)
}
```

3. **Handling Simulations:**
```kotlin
fun handleResponse(response: ContinueSessionResponse) {
    // Display agent text
    displayMessage(response.agentResponse)
    
    // Check simulation flag
    val metadata = response.metadata
    if (metadata["show_simulation"] == true) {
        val simConfig = metadata["simulation_config"] as Map<String, Any>
        val simType = simConfig["type"] as String
        
        when (simType) {
            "pendulum_simulation" -> {
                val variables = simConfig["variables"] as List<Map<String, String>>
                launchPendulumSimulation(variables)
            }
            // Add more simulation types as needed
        }
    }
}
```

4. **Displaying Images:**
```kotlin
metadata["enhanced_message_metadata"]?.let { meta ->
    meta["image"]?.let { imageData ->
        val url = imageData["url"]
        val caption = imageData["caption"]
        Glide.with(context)
            .load(url)
            .into(imageView)
        captionView.text = caption
    }
}
```

---

## 🧪 Testing

### Using cURL

**Start a session:**
```bash
curl -X POST "http://localhost:8000/session/start" \
  -H "Content-Type: application/json" \
  -d '{
    "concept_title": "Pendulum and its Time Period",
    "student_id": "test_student"
  }'
```

**Continue conversation:**
```bash
curl -X POST "http://localhost:8000/session/continue" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "YOUR_THREAD_ID",
    "user_message": "Yes, I am ready!"
  }'
```

### Using Python

See example in "Typical Usage Flow" section above.

### Using Swagger UI

Navigate to `http://localhost:8000/docs` and use the interactive interface to test all endpoints.

---

## ⚙️ Configuration

### Environment Variables

The API server uses the same environment variables as the educational agent:
- LLM API keys (Gemini, OpenAI, etc.)
- LangSmith configuration (optional)

### Changing Concepts

Currently, the concept is hardcoded in `educational_agent_optimized_langsmith/config.py`:
```python
concept_pkg = ConceptPkg(title="Pendulum and its Time Period")
```

To support multiple concepts, you'll need to modify the agent initialization to accept dynamic concepts.

### Persistence

Currently using `InMemorySaver` for LangGraph checkpoints. Sessions are lost on server restart.

**To upgrade to PostgreSQL:**
1. Replace `InMemorySaver` with `PostgresSaver` in `graph.py`
2. Configure database connection
3. Update session storage (`_active_sessions`) to use Redis or database

---

## 🔐 Security Considerations

**For Production Deployment:**

1. **Add Authentication:**
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/session/start")
async def start_session(request: StartSessionRequest, token: str = Depends(security)):
    # Verify token
    pass
```

2. **Configure CORS Properly:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

3. **Add Rate Limiting:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/session/continue")
@limiter.limit("10/minute")
async def continue_session(...):
    pass
```

4. **Input Validation:**
- Already handled by Pydantic schemas
- Consider adding content filtering for inappropriate messages

---

## 📊 Monitoring

### Logging

The API logs all requests to console:
```
API /session/start - concept: Pendulum and its Time Period, student: student_123
API /session/continue - thread: session-thread-..., message: Yes, I'm ready!...
```

### Metrics to Track

- Session creation rate
- Average conversation length
- Common drop-off points (pedagogical states)
- Quiz scores distribution
- Misconception frequency
- Response times

---

## 🐛 Troubleshooting

### Common Issues

**1. "Session not found" error:**
- Session may have been deleted or server restarted (InMemorySaver is volatile)
- Solution: Start a new session

**2. Agent not responding:**
- Check LLM API keys in environment
- Verify network connectivity to LLM providers
- Check console logs for errors

**3. Simulation not triggering:**
- Verify `show_simulation` in metadata
- Check agent's internal state transitions
- May require specific student responses to trigger

**4. Import errors:**
- Ensure `educational_agent_optimized_langsmith` is in Python path
- Check all dependencies are installed
- Verify `.env` file configuration

---

## 📝 License

Same as parent project.

---

## 🤝 Contributing

When modifying the API:
1. Update schemas in `schemas.py`
2. Update endpoint handlers in `api_server.py`
3. Update this README with examples
4. Test all endpoints with Swagger UI

---

## 📞 Support

For issues related to:
- **API Server**: Check logs and Swagger docs
- **Educational Agent**: See `educational_agent_optimized_langsmith/` documentation
- **LangGraph**: Check LangGraph documentation

---

**Happy Teaching! 🎓**
