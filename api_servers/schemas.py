from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ============================================================================
# REQUEST MODELS
# ============================================================================

class StartSessionRequest(BaseModel):
    concept_title: str = Field(
        ..., 
        description="The concept to teach (e.g., 'Pendulum and its Time Period')"
    )
    student_id: Optional[str] = Field(
        None, 
        description="Optional student identifier for tracking"
    )
    persona_name: Optional[str] = Field(
        None, 
        description="Optional persona name for testing (e.g., 'Confused Student')"
    )
    session_label: Optional[str] = Field(
        None, 
        description="Optional custom session label"
    )


class ContinueSessionRequest(BaseModel):
    thread_id: str = Field(
        ..., 
        description="The thread ID of the session to continue"
    )
    user_message: str = Field(
        ..., 
        description="The student's message/response"
    )


class SessionStatusRequest(BaseModel):
    thread_id: str = Field(
        ..., 
        description="The thread ID of the session"
    )


class TestPersonaRequest(BaseModel):
    persona_name: str = Field(
        ..., 
        description="Persona to test. Available: 'Eager Student' (engaged & motivated), "
                    "'Confused Student' (struggling to understand), "
                    "'Distracted Student' (easily distracted, off-topic), "
                    "'Dull Student' (not very bright, needs extra help)"
    )
    concept_title: str = Field(
        default="Pendulum and its Time Period",
        description="Concept to teach"
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class SessionMetadata(BaseModel):
    """Fixed structure for session metadata - always includes all fields"""
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


class StartSessionResponse(BaseModel):
    success: bool
    session_id: str
    thread_id: str
    user_id: str
    agent_response: str
    current_state: str
    concept_title: str
    message: str = "Session started successfully"
    metadata: SessionMetadata = Field(
        default_factory=SessionMetadata,
        description="Session metadata with consistent structure"
    )


class ContinueSessionResponse(BaseModel):
    success: bool
    thread_id: str
    agent_response: str
    current_state: str
    metadata: SessionMetadata = Field(
        default_factory=SessionMetadata,
        description="Session metadata with consistent structure"
    )
    message: str = "Response generated successfully"


class SessionStatusResponse(BaseModel):
    success: bool
    thread_id: str
    exists: bool
    current_state: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None
    concept_title: Optional[str] = None
    message: str = "Status retrieved successfully"


class SessionHistoryResponse(BaseModel):
    success: bool
    thread_id: str
    exists: bool
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    node_transitions: List[Dict[str, Any]] = Field(default_factory=list)
    concept_title: Optional[str] = None
    message: str = "History retrieved successfully"


class SessionSummaryResponse(BaseModel):
    success: bool
    thread_id: str
    exists: bool
    summary: Optional[Dict[str, Any]] = None
    quiz_score: Optional[float] = None
    transfer_success: Optional[bool] = None
    misconception_detected: Optional[bool] = None
    definition_echoed: Optional[bool] = None
    message: str = "Summary retrieved successfully"


class HealthResponse(BaseModel):
    status: str
    version: str
    persistence: str
    agent_type: str
    available_endpoints: List[str]


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None


class PersonaInfo(BaseModel):
    """Information about a test persona"""
    name: str
    description: str
    sample_phrases: List[str]


class PersonasListResponse(BaseModel):
    """Response listing all available test personas"""
    success: bool = True
    personas: List[PersonaInfo]
    total: int
    message: str = "Available test personas retrieved successfully"
