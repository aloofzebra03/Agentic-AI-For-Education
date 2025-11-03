"""
Pydantic schemas for Educational Agent API
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ============================================================================
# REQUEST MODELS
# ============================================================================

class StartSessionRequest(BaseModel):
    """Request to start a new learning session"""
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
    """Request to continue an existing session with user input"""
    thread_id: str = Field(
        ..., 
        description="The thread ID of the session to continue"
    )
    user_message: str = Field(
        ..., 
        description="The student's message/response"
    )


class SessionStatusRequest(BaseModel):
    """Request to get status of a session"""
    thread_id: str = Field(
        ..., 
        description="The thread ID of the session"
    )


class TestPersonaRequest(BaseModel):
    """Request to test with a predefined persona"""
    persona_name: str = Field(
        ..., 
        description="Persona to test: 'Confused Student', 'Distracted Student', 'Dull Student', etc."
    )
    concept_title: str = Field(
        default="Pendulum and its Time Period",
        description="Concept to teach"
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class StartSessionResponse(BaseModel):
    """Response when starting a new session"""
    success: bool
    session_id: str
    thread_id: str
    user_id: str
    agent_response: str
    current_state: str
    concept_title: str
    message: str = "Session started successfully"
    metadata: Optional[Dict[str, Any]] = None


class ContinueSessionResponse(BaseModel):
    """Response when continuing a session"""
    success: bool
    thread_id: str
    agent_response: str
    current_state: str
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata: scores, images, simulation configs, etc."
    )
    message: str = "Response generated successfully"


class SessionStatusResponse(BaseModel):
    """Response with session status and progress"""
    success: bool
    thread_id: str
    exists: bool
    current_state: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None
    concept_title: Optional[str] = None
    message: str = "Status retrieved successfully"


class SessionHistoryResponse(BaseModel):
    """Response with full conversation history"""
    success: bool
    thread_id: str
    exists: bool
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    node_transitions: List[Dict[str, Any]] = Field(default_factory=list)
    concept_title: Optional[str] = None
    message: str = "History retrieved successfully"


class SessionSummaryResponse(BaseModel):
    """Response with session summary and metrics"""
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
    """Health check response"""
    status: str
    version: str
    persistence: str
    agent_type: str
    available_endpoints: List[str]


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
