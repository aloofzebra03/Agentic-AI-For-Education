# 📊 Fixed Metadata Structure

## Overview

The API now returns **consistent, predictable metadata** in every response. All fields are **always present**, making it easy for clients (like your Android app) to parse the response without null checks.

---

## 🎯 SessionMetadata Structure

```python
class SessionMetadata(BaseModel):
    # Simulation flags
    show_simulation: bool = False
    simulation_config: Optional[Dict[str, Any]] = None
    
    # Image metadata (only image URL and node where it appeared)
    image_url: Optional[str] = None
    image_node: Optional[str] = None
    
    # Scores and progress
    quiz_score: Optional[float] = None
    retrieval_score: Optional[float] = None
    
    # Concept tracking
    sim_concepts: Optional[List[str]] = None
    sim_current_idx: Optional[int] = None
    sim_total_concepts: Optional[int] = None
    
    # Misconception tracking
    misconception_detected: bool = False
    last_correction: Optional[str] = None
    
    # Node transitions
    node_transitions: Optional[List[Dict[str, Any]]] = None
```

---

## 📋 Field Descriptions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `show_simulation` | `bool` | `false` | Whether simulation should be displayed |
| `simulation_config` | `Dict \| null` | `null` | Simulation parameters if active |
| `image_url` | `string \| null` | `null` | Base64 encoded image URL (e.g., `data:image/png;base64,...`) |
| `image_node` | `string \| null` | `null` | Node where image was generated (e.g., `"CI"`, `"GE"`) |
| `quiz_score` | `float \| null` | `null` | Student's quiz performance (0.0 to 1.0) |
| `retrieval_score` | `float \| null` | `null` | RAG retrieval confidence score |
| `sim_concepts` | `List[str] \| null` | `null` | List of concepts in simulation sequence |
| `sim_current_idx` | `int \| null` | `null` | Current concept index in simulation |
| `sim_total_concepts` | `int \| null` | `null` | Total number of concepts in simulation |
| `misconception_detected` | `bool` | `false` | Whether student showed misconception |
| `last_correction` | `string \| null` | `null` | Last misconception correction message |
| `node_transitions` | `List[Dict] \| null` | `null` | History of node state transitions |

---

## 📝 Example Responses

### Example 1: Session Start (No Image, No Quiz)
```json
{
  "success": true,
  "session_id": "session-20251107-143022",
  "thread_id": "session-thread-20251107-143022",
  "user_id": "anonymous",
  "agent_response": "Hello! Let's learn about Pendulums...",
  "current_state": "APK",
  "concept_title": "Pendulum and its Time Period",
  "message": "Session started successfully",
  "metadata": {
    "show_simulation": false,
    "simulation_config": null,
    "image_url": null,
    "image_node": null,
    "quiz_score": null,
    "retrieval_score": null,
    "sim_concepts": null,
    "sim_current_idx": null,
    "sim_total_concepts": null,
    "misconception_detected": false,
    "last_correction": null,
    "node_transitions": null
  }
}
```

### Example 2: With Image (CI Node)
```json
{
  "success": true,
  "thread_id": "session-thread-20251107-143022",
  "agent_response": "Here's a diagram showing how a pendulum works...",
  "current_state": "CI",
  "message": "Response generated successfully",
  "metadata": {
    "show_simulation": false,
    "simulation_config": null,
    "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "image_node": "CI",
    "quiz_score": null,
    "retrieval_score": 0.92,
    "sim_concepts": null,
    "sim_current_idx": null,
    "sim_total_concepts": null,
    "misconception_detected": false,
    "last_correction": null,
    "node_transitions": [
      {"from": "APK", "to": "CI", "timestamp": "..."}
    ]
  }
}
```

### Example 3: With Quiz Score
```json
{
  "success": true,
  "thread_id": "session-thread-20251107-143022",
  "agent_response": "Great job! You got it right.",
  "current_state": "GE",
  "message": "Response generated successfully",
  "metadata": {
    "show_simulation": false,
    "simulation_config": null,
    "image_url": null,
    "image_node": null,
    "quiz_score": 0.75,
    "retrieval_score": 0.88,
    "sim_concepts": null,
    "sim_current_idx": null,
    "sim_total_concepts": null,
    "misconception_detected": false,
    "last_correction": null,
    "node_transitions": [
      {"from": "APK", "to": "CI", "timestamp": "..."},
      {"from": "CI", "to": "GE", "timestamp": "..."}
    ]
  }
}
```

### Example 4: Simulation Active
```json
{
  "success": true,
  "thread_id": "session-thread-20251107-143022",
  "agent_response": "Let's run a simulation...",
  "current_state": "GE",
  "message": "Response generated successfully",
  "metadata": {
    "show_simulation": true,
    "simulation_config": {
      "type": "pendulum",
      "parameters": {
        "length": 1.0,
        "mass": 0.5,
        "angle": 15
      }
    },
    "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "image_node": "GE",
    "quiz_score": 0.75,
    "retrieval_score": 0.88,
    "sim_concepts": ["Simple Pendulum", "Time Period", "Amplitude"],
    "sim_current_idx": 0,
    "sim_total_concepts": 3,
    "misconception_detected": false,
    "last_correction": null,
    "node_transitions": [...]
  }
}
```

### Example 5: Misconception Detected
```json
{
  "success": true,
  "thread_id": "session-thread-20251107-143022",
  "agent_response": "Actually, the time period doesn't depend on mass...",
  "current_state": "GE",
  "message": "Response generated successfully",
  "metadata": {
    "show_simulation": false,
    "simulation_config": null,
    "image_url": null,
    "image_node": null,
    "quiz_score": 0.5,
    "retrieval_score": 0.91,
    "sim_concepts": null,
    "sim_current_idx": null,
    "sim_total_concepts": null,
    "misconception_detected": true,
    "last_correction": "The time period of a pendulum is independent of its mass.",
    "node_transitions": [...]
  }
}
```

---

## 🔧 Android/Kotlin Usage

### Data Class
```kotlin
data class SessionMetadata(
    val showSimulation: Boolean = false,
    val simulationConfig: Map<String, Any>? = null,
    val imageUrl: String? = null,
    val imageNode: String? = null,
    val quizScore: Float? = null,
    val retrievalScore: Float? = null,
    val simConcepts: List<String>? = null,
    val simCurrentIdx: Int? = null,
    val simTotalConcepts: Int? = null,
    val misconceptionDetected: Boolean = false,
    val lastCorrection: String? = null,
    val nodeTransitions: List<Map<String, Any>>? = null
)

data class ContinueSessionResponse(
    val success: Boolean,
    val threadId: String,
    val agentResponse: String,
    val currentState: String,
    val metadata: SessionMetadata,
    val message: String
)
```

### Usage Example
```kotlin
// No null checks needed for boolean fields!
if (response.metadata.showSimulation) {
    displaySimulation(response.metadata.simulationConfig)
}

// Safe null checks for optional fields
response.metadata.imageUrl?.let { url ->
    loadImage(url)
    logImageSource(response.metadata.imageNode ?: "unknown")
}

// Always safe to check booleans
if (response.metadata.misconceptionDetected) {
    highlightMisconception(response.metadata.lastCorrection)
}

// Quiz score handling
response.metadata.quizScore?.let { score ->
    updateProgressBar(score)
}
```

---

## ✅ Benefits

### 1. **Consistent Structure**
- Every response has the same shape
- No need to check if `metadata` exists
- All fields are always present

### 2. **Type Safety**
```kotlin
// ✅ Always works - no null checks needed
val hasSimulation = response.metadata.showSimulation

// ❌ Old way - had to check multiple levels
val hasSimulation = response.metadata?.get("show_simulation") as? Boolean ?: false
```

### 3. **Easy Parsing**
```kotlin
// Direct access to nested data
val currentConcept = response.metadata.simConcepts?.get(
    response.metadata.simCurrentIdx ?: 0
)
```

### 4. **Documentation**
- IDE autocomplete shows all available fields
- Types are explicit (Boolean, String?, Float?, etc.)
- No guessing what might be in the dictionary

---

## 🎨 UI Logic Examples

### Display Image if Present
```kotlin
fun handleResponse(response: ContinueSessionResponse) {
    // Clean and simple
    if (response.metadata.imageUrl != null) {
        imageView.visibility = View.VISIBLE
        Glide.with(context)
            .load(response.metadata.imageUrl)
            .into(imageView)
    } else {
        imageView.visibility = View.GONE
    }
}
```

### Show Simulation
```kotlin
fun handleResponse(response: ContinueSessionResponse) {
    if (response.metadata.showSimulation) {
        val config = response.metadata.simulationConfig
        simulationFragment.show(config)
    }
}
```

### Display Quiz Progress
```kotlin
fun updateQuizProgress(metadata: SessionMetadata) {
    metadata.quizScore?.let { score ->
        progressBar.progress = (score * 100).toInt()
        scoreText.text = "${(score * 100).toInt()}%"
    }
}
```

### Track Concept Progress
```kotlin
fun showConceptProgress(metadata: SessionMetadata) {
    if (metadata.simConcepts != null && metadata.simCurrentIdx != null) {
        val progress = "${metadata.simCurrentIdx + 1}/${metadata.simTotalConcepts}"
        progressText.text = progress
        
        conceptList.text = metadata.simConcepts.joinToString("\n") { concept ->
            val idx = metadata.simConcepts.indexOf(concept)
            val marker = if (idx == metadata.simCurrentIdx) "➤" else "○"
            "$marker $concept"
        }
    }
}
```

---

## 🚀 Migration from Old Format

### Old Format (Dynamic Dictionary)
```json
{
  "metadata": {
    "quiz_score": 0.75,
    "enhanced_message_metadata": {
      "image": "data:...",
      "node": "CI"
    }
  }
}
```

### New Format (Fixed Structure)
```json
{
  "metadata": {
    "quiz_score": 0.75,
    "image_url": "data:...",
    "image_node": "CI",
    "show_simulation": false,
    "simulation_config": null,
    ...
  }
}
```

### Code Changes
```kotlin
// OLD - Unsafe casting
val imageData = metadata["enhanced_message_metadata"] as? Map<String, Any>
val imageUrl = imageData?.get("image") as? String

// NEW - Type-safe access
val imageUrl = metadata.imageUrl
```

---

## 📊 Summary

**Before:**
- ❌ Inconsistent structure (keys appeared/disappeared)
- ❌ Required null checks at multiple levels
- ❌ Nested dictionaries hard to parse
- ❌ No type safety

**After:**
- ✅ Fixed structure (all fields always present)
- ✅ Simple null checks only for optional values
- ✅ Flat structure (except simulation_config)
- ✅ Full type safety with Pydantic/Kotlin data classes
- ✅ Better IDE support and documentation

Your Android app can now reliably parse every response with minimal error handling! 🎉
