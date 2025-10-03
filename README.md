# Agentic AI For Education

## 🎯 Project Overview

This project is a comprehensive **AI-powered educational system** that combines **LangGraph**, **Retrieval-Augmented Generation (RAG)**, **interactive simulations**, and **multimodal interfaces** to create an adaptive learning experience. The system features multiple educational agents with speech recognition/synthesis, visual simulations, and automated testing capabilities.

## 🏗️ Architecture Overview

```
├── 🧠 Core Educational Agents (Multiple Variants)
├── 🎤 Multimodal Interface (Streamlit Apps)  
├── 🧪 Testing & Evaluation Framework
├── 📚 RAG Content Management System
├── 🎨 Visual Simulation Engine
└── 📊 Analytics & Monitoring (LangFuse/LangSmith)
```

## 📁 Project Structure & Dependencies

### **Core Educational Agent Variants**

The project contains **5 different variants** of the educational agent, each building upon the previous with incremental improvements:

#### 1. **`educational_agent_v1/`** - Base Agent with RAG

- **Primary Files**: `agent.py`, `nodes4_rag.py`, `graph_fuse.py`, `config.py`
- **Features**: Basic conversational agent with RAG integration
- **Tracing**: Uses LangFuse/Langmsith for tracing.Header attached in agent.py
- **Sub-modules**:
  - `Creating_Section_Text/` - RAG content generation pipeline
  - `Filtering_GT/` - Ground truth filtering utilities

#### 2. **`educational_agent_with_simulation_v2/`** - Full Simulation Integration

- **Primary Files**: Complete simulation implementation alongwith above
- **Key Features**:
  - Full interactive physics simulations
  - Visual pendulum demonstrations
  - Real-time parameter manipulation
- **Dependencies**: Most feature-complete variant

#### 3. **`educational_agent_optimized_v3/`** - Memory-Optimized Agent

- **Primary Files**: `agent.py`, `graph.py`, `main_nodes_simulation_agent_no_mh.py`
- Includes everything from above  + memory optimization.
- **Key Differences**:
  - Memory optimization techniques integerated by summarizing conversation history.
- **Dependencies**: Imports from base `educational_agent` for shared utilities
- **Tracing**: Uses `Langfuse` for tracing.Header attached in agent.py

#### 3. **`educational_agent_optimized_langsmith/`** - LangSmith Integration

- **Primary Files**: Identical structure to `educational_agent_optimized/`
- **Key Differences**:
  - Uses Langsmith instead of Langfuse
  - Enhanced tracing and monitoring capabilities
- **Dependencies**: Imports from base `utils` for shared utilities

#### 4. **`educational_agent_optimized_langsmith_kannada/`** - Multilingual Support

- **Primary Files**: Same structure as above
- **Key Differences**:
  - Kannada language support for Indian education market(System Prompt Changed)
  - Hard Coded Messages also changed to Kannada
  - Language-specific model configurations
- **Dependencies**: Imports from base `utils` for shared utilities

### **Streamlit Application Variants**

The project includes **10+ Streamlit applications**, many with overlapping functionality but specific optimizations:

#### Core Applications(Previous versions with old code.Built Stage Wise):

1. **`app.py`** - Basic Streamlit interface
2. **`app_graph.py`** - Graph-based visualization interface
3. **`app_gt.py`** - Ground truth testing interface
4. **`app_simulation.py`** - Simulation-focused interface.Integerates Pendulum Simulation
5. **`app_simulation_optimized.py`** - Performance-optimized simulation

#### Advanced Animation Applications(Viseme):

6. **`app_optimized_animation.py`** - Main production interface with TTS/ASR
7. **`app_optimized_animation_old.py`** - Legacy version (backup)
8. **`app_optimized_animation copy.py`** - Development copy
9. **`app_optimized_animation_kannada.py`** - Kannada language support.Changed TTS and STT libraries
10. **`app_optimized_animation_kannada copy.py`** - Development copy

#### **Key Shared Features Across Apps:**

- **Speech Recognition**: WhisperASR integration (English/Kannada)
- **Text-to-Speech**: gTTS with speed optimization via Pedalboard
- **Visual Animations**: Lip-sync avatars and physics simulations
- **Session Management**: LangFuse/LangSmith tracking
- **Audio Processing**: Real-time transcription and playback

#### **Differences Between App Variants:**

| App Variant                            | Language | ASR Model       | Animation   | Simulation | Tracing   |
| -------------------------------------- | -------- | --------------- | ----------- | ---------- | --------- |
| `app_optimized_animation.py`         | English  | Whisper-tiny    | ✅ Lip-sync | ✅ Physics | LangSmith |
| `app_optimized_animation_kannada.py` | Kannada  | Whisper-Kannada | ✅ Lip-sync | ✅ Physics | LangSmith |
| `app_simulation.py`                  | English  | Whisper-tiny    | ❌          | ✅ Basic   | LangFuse  |
| `app_graph.py`                       | English  | Whisper-tiny    | ❌          | ❌         | LangFuse  |

### **Testing & Evaluation Framework**

#### **`tester_agent/`** - Automated Testing System

- **`tester.py`** - Core testing orchestrator
- **`personas.py`** - Student persona definitions (Eager, Confused, Distracted, Dull)
- **`evaluator.py`** - Response evaluation metrics
- **`session_metrics.py`** - Learning analytics computation
- **`simulation_descriptor.py`** - Simulation performance analysis

### **Supporting Infrastructure**

#### **`reports/`** - Evaluation Results Storage

- Contains JSON files with evaluation results for different personas
- Session metrics and summaries for performance analysis
- Naming convention: `evaluation_{persona}-{timestamp}.json`

#### **`static/`** - Media Assets

- Character images for avatar animations
- Visual resources for simulation interfaces

#### **Build & Distribution**

- **`build/`** - Compiled Python packages
- **`agentic_ai_for_education.egg-info/`** - Package metadata
- **`pyproject.toml`** - Modern Python packaging configuration.Useful for importing different files from different folders seamlessly
- **`requirements.txt`** - Comprehensive dependency list (100+ packages) generated using py code

## 🔄 Data Flow & Dependencies

### **Inter-Module Dependencies:**

1. **Agent Hierarchy**:

   ```
   educational_agent (base)
   ├── educational_agent_with_simulation (base + full simulation capabilities)
   ├── educational_agent_optimized (simulation + memory optimization)
   │   └── educational_agent_optimized_langsmith (optimized + LangSmith tracing)
   │       └── educational_agent_optimized_langsmith_kannada (langsmith + multilingual)
   └── tester_agent (uses base for evaluation)
   ```
2. **Streamlit App Dependencies**:

   ```
   All apps → educational_agent variants (imports)
   Animation apps → static/ (character images)
   Simulation apps → physics simulation nodes
   Kannada apps → language detection & translation utilities
   ```
3. **Shared Components**:

   - **ASR/TTS Functions**: Identical across most apps (code duplication for modularity)
   - **Session Management**: Common patterns with LangFuse/LangSmith integration
   - **State Management**: Similar Streamlit session state handling

## 🚀 Getting Started

### **Prerequisites**

```bash
Python >= 3.10
Node.js (for LangGraph Studio)
Others included in requirements.txt
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
   ```

### **Running the Applications**

#### **Main Production Interface** (Recommended):

```bash
streamlit run Streamlit_UI/app_optimized_animation.py
```

#### **Kannada Language Support**:

```bash
streamlit run Streamlit_UI/app_optimized_animation_kannada.py
```

#### **Command Line Interface**:

```bash
python main.py
```

#### **Testing Framework**:

```bash
python run_test.py
```

## 🎯 Core Features

### **1. Adaptive Learning Flow**

- **Multi-Node Agent Architecture**: Each educational concept broken into discrete nodes
- **Misconception Detection**: Real-time identification of student misunderstandings
- **Personalized Paths**: Dynamic routing based on student performance
- **Memory Optimization**: Efficient state management for long conversations

### **2. Multimodal Interface**

- **Voice Interaction**:
  - Speech-to-text via Whisper (English) or Whisper-Kannada
  - Text-to-speech via gTTS with speed optimization
  - Real-time audio transcription
- **Visual Avatars**: Lip-sync animations with character selection (boy/girl)
- **Interactive Simulations**: Physics demonstrations (pendulum, oscillations)

### **3. Content Management**

- **RAG Pipeline**: Automated extraction from NCERT textbooks
- **Concept Mapping**: Hierarchical educational content organization
- **Ground Truth Filtering**: Quality assurance for generated content

### **4. Evaluation & Analytics**

- **Student Personas**: Automated testing with 4 distinct student types
- **Performance Metrics**: Learning effectiveness measurement
- **Session Analytics**: Comprehensive interaction tracking
- **Real-time Monitoring**: LangFuse/LangSmith integration for observability

## 🔧 Technical Implementation Details

### **Speech Processing Pipeline**

#### **ASR (Automatic Speech Recognition)**:

```python
class WhisperASR:
    def __init__(self, model_name="tiny" | "vasista22/whisper-kannada-tiny"):
        # Model selection based on language requirements
  
    def recognize(self, audio_path: str) -> str:
        # Transcription with error handling and fallback mechanisms
```

#### **TTS (Text-to-Speech)**:

```python
def play_text_as_audio(text, speed_factor=1.25):
    # gTTS → Pedalboard speed adjustment → WAV output
    # Automatic language detection for multi-lingual support
```

### **Simulation Engine**

#### **Physics Simulation Nodes**:

1. **`sim_concept_creator_node`** - Define simulation objectives
2. **`sim_vars_node`** - Configure simulation variables
3. **`sim_action_node`** - Set up interactive parameters
4. **`sim_expect_node`** - Prediction phase
5. **`sim_execute_node`** - Run simulation
6. **`sim_observe_node`** - Guide observation
7. **`sim_insight_node`** - Extract learning insights
8. **`sim_reflection_node`** - Consolidate understanding

#### **Visual Rendering**:

```javascript
// Real-time pendulum animation with configurable parameters
function createPendulumSimulation(config) {
    // Canvas-based physics simulation
    // Parameter manipulation interface
    // Real-time visualization updates
}
```

### **RAG Implementation(Not being used in the latest version)**

#### **Content Generation Pipeline**:

```python
# educational_agent/Creating_Section_Text/
├── pdf_loader.py      # NCERT textbook ingestion
├── embedder.py        # Vector embedding generation  
├── retriever.py       # Similarity-based content retrieval
├── prompt_builder.py  # Context-aware prompt construction
└── main.py           # Orchestration pipeline
```

#### **Usage**:

```bash
# Content ingestion
python -m educational_agent.Creating_Section_Text.main ingest

# Section generation  
python -m educational_agent.Creating_Section_Text.main generate \
    --ongoing_concept "Simple Harmonic Motion" \
    --section_params_file params.json
```

## 🧪 Testing & Evaluation

### **Automated Persona Testing**

#### **Student Personas**:

1. **Eager Student** - Motivated and engaged learner
2. **Confused Student** - Struggles with concept comprehension
3. **Distracted Student** - Attention and focus challenges
4. **Dull Student** - Processing and retention difficulties

#### **Evaluation Metrics**:

```python
class SessionMetrics:
    concept_coverage: float      # % of concepts successfully taught
    misconception_rate: float    # Frequency of misunderstandings  
    engagement_score: float      # Interaction quality assessment
    transfer_success: bool       # Knowledge application ability
    session_duration: int        # Time to completion
```

#### **Running Evaluations**:

```bash
python run_test.py --persona "Eager Student" --iterations 5
```

### **Performance Analysis**

Results are stored in `reports/` with comprehensive analytics:

- Response accuracy and appropriateness
- Learning progression tracking
- Simulation effectiveness measurement
- Comparative analysis across personas

## 🌍 Multilingual Support

### **Kannada Language Integration**

The project includes comprehensive support for Kannada (Indian regional language):

#### **Language Detection & Translation**:

```python
from langdetect import detect
from deep_translator import GoogleTranslator

# Automatic language detection
detected_lang = detect(user_input)

# Bidirectional translation  
if detected_lang == 'kn':
    english_text = GoogleTranslator(source='kn', target='en').translate(user_input)
```

#### **Kannada-Specific Components**:

- **ASR Model**: `vasista22/whisper-kannada-tiny` for speech recognition
- **TTS**: gTTS with Kannada language support (`lang='kn'`)
- **UI Adaptations**: Streamlit interface optimizations for regional users

## 📊 Monitoring & Analytics

### **LangFuse Integration** (Not being used in the latest version)

```python
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

# Session tracking with rich metadata
langfuse_handler = LangfuseCallbackHandler(
    session_id=f"{persona}-{timestamp}",
    user_id="educational-system",
    metadata={
        "persona": student_persona,
        "concept": current_concept,
        "simulation_used": bool(simulation_config)
    }
)
```

### **LangSmith Integration** (Primary)

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "educational_agent"

# Automatic trace collection for debugging and optimization
```

### **Analytics Dashboard**

- Real-time conversation monitoring
- Learning effectiveness metrics
- Error tracking and debugging
- Performance optimization insights

### **Shared Components**:

- **`tester_agent/`** - Used by all variants for evaluation
- **`static/`** - Common media assets
- **`.env`** - Centralized configuration management
- **`requirements.txt`** - Unified dependency specification
- `educational_agent/shared_utils.py `- Commonly used functions in all agent variants

## 🔮 Future Development

### **Planned Enhancements**:

1. **Multi-Subject Support** - Expand beyond physics to mathematics, chemistry
2. **Advanced Simulations** - 3D visualizations, VR integration
3. **Collaborative Learning** - Multi-student session support
4. **Enhanced Analytics** - Learning pattern analysis, predictive modeling
5. **Mobile Application** - React Native or Flutter implementation
6. **Voice Cloning** - Personalized teacher voice synthesis
7. **Gesture Recognition** - Computer vision for engagement tracking

### **Technical Improvements**:

1. **Code Consolidation** - Reduce duplication while maintaining modularity
2. **Docker Containerization** - Simplified deployment and scaling
3. **API Gateway** - Microservices architecture for better scalability
4. **Database Integration** - Persistent user progress tracking
5. **A/B Testing Framework** - Systematic feature experimentation
6. **Real-time Collaboration** - WebRTC for synchronous learning sessions
