"""
FastAPI server for Educational Agent (educational_agent_optimized_langsmith)
Stateful API with persistent conversation management using LangGraph checkpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Dict, Optional, Any
import sys
import os
from pathlib import Path

# Add parent directory to path to import educational agent
sys.path.insert(0, str(Path(__file__).parent.parent))

from educational_agent_optimized_langsmith.agent import EducationalAgent
from educational_agent_optimized_langsmith.config import concept_pkg
from api_servers.schemas import (
    StartSessionRequest, StartSessionResponse,
    ContinueSessionRequest, ContinueSessionResponse,
    SessionStatusRequest, SessionStatusResponse,
    SessionHistoryResponse, SessionSummaryResponse,
    TestPersonaRequest, HealthResponse, ErrorResponse
)

# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Educational Agent API",
    version="1.0.0",
    description="Stateful API for personalized education with LangGraph-based agent"
)

# CORS middleware for web/mobile app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# IN-MEMORY SESSION STORE
# ============================================================================
# Maps thread_id -> EducationalAgent instance
# Note: This is in-memory. For production, consider Redis or database storage
_active_sessions: Dict[str, EducationalAgent] = {}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_session(thread_id: str) -> Optional[EducationalAgent]:
    """Retrieve an active session by thread_id"""
    return _active_sessions.get(thread_id)


def extract_metadata_from_state(agent: EducationalAgent) -> Dict[str, Any]:
    """Extract useful metadata from agent state for API response"""
    state = agent.state
    metadata = {}
    
    # Simulation flags
    if state.get("show_simulation"):
        metadata["show_simulation"] = True
        metadata["simulation_config"] = state.get("simulation_config", {})
    
    # Image metadata
    if state.get("enhanced_message_metadata"):
        metadata["enhanced_message_metadata"] = state["enhanced_message_metadata"]
    
    # Scores and progress
    if state.get("quiz_score") is not None:
        metadata["quiz_score"] = state["quiz_score"]
    
    if state.get("retrieval_score") is not None:
        metadata["retrieval_score"] = state["retrieval_score"]
    
    # Current concept tracking
    if state.get("sim_concepts"):
        metadata["sim_concepts"] = state["sim_concepts"]
        metadata["sim_current_idx"] = state.get("sim_current_idx", 0)
        metadata["sim_total_concepts"] = state.get("sim_total_concepts", len(state["sim_concepts"]))
    
    # Misconception tracking
    if state.get("misconception_detected"):
        metadata["misconception_detected"] = True
        metadata["last_correction"] = state.get("last_correction", "")
    
    # Node transition info
    if state.get("node_transitions"):
        metadata["node_transitions"] = state["node_transitions"]
    
    return metadata


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_model=Dict[str, Any])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Educational Agent API is running!",
        "version": "1.0.0",
        "agent_type": "educational_agent_optimized_langsmith",
        "endpoints": [
            "GET  /health - Health check",
            "POST /session/start - Start new learning session",
            "POST /session/continue - Continue existing session",
            "GET  /session/status/{thread_id} - Get session status",
            "GET  /session/history/{thread_id} - Get conversation history",
            "GET  /session/summary/{thread_id} - Get session summary",
            "DELETE /session/{thread_id} - Delete session",
            "POST /test/persona - Test with predefined persona"
        ]
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        persistence="InMemorySaver (LangGraph)",
        agent_type="educational_agent_optimized_langsmith",
        available_endpoints=[
            "/",
            "/health",
            "/session/start",
            "/session/continue",
            "/session/status/{thread_id}",
            "/session/history/{thread_id}",
            "/session/summary/{thread_id}",
            "/session/{thread_id}",
            "/test/persona"
        ]
    )


@app.post("/session/start", response_model=StartSessionResponse)
def start_session(request: StartSessionRequest):
    """
    Start a new learning session
    
    Creates a new EducationalAgent instance and begins the conversation.
    Returns the initial greeting and session identifiers.
    """
    try:
        print(f"API /session/start - concept: {request.concept_title}, student: {request.student_id}")
        
        # Create new agent instance
        agent = EducationalAgent(
            session_label=request.session_label,
            user_id=request.student_id,
            persona_name=request.persona_name,
        )
        
        # Store in active sessions
        _active_sessions[agent.thread_id] = agent
        
        # Start the conversation
        greeting = agent.start()
        
        # Extract metadata
        metadata = extract_metadata_from_state(agent)
        
        return StartSessionResponse(
            success=True,
            session_id=agent.session_id,
            thread_id=agent.thread_id,
            user_id=agent.user_id,
            agent_response=greeting,
            current_state=agent.current_state(),
            concept_title=request.concept_title,
            message="Session started successfully. Agent is ready for student input.",
            metadata=metadata
        )
        
    except Exception as e:
        print(f"API error in /session/start: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting session: {str(e)}")


@app.post("/session/continue", response_model=ContinueSessionResponse)
def continue_session(request: ContinueSessionRequest):
    """
    Continue an existing session with user input
    
    Processes student's message and returns agent's response.
    Automatically handles state transitions and simulations.
    """
    try:
        print(f"API /session/continue - thread: {request.thread_id}, message: {request.user_message[:50]}...")
        
        # Retrieve session
        agent = get_session(request.thread_id)
        if not agent:
            raise HTTPException(
                status_code=404, 
                detail=f"Session not found for thread_id: {request.thread_id}. Please start a new session."
            )
        
        # Process user message
        response = agent.post(request.user_message)
        
        # Extract metadata
        metadata = extract_metadata_from_state(agent)
        
        return ContinueSessionResponse(
            success=True,
            thread_id=agent.thread_id,
            agent_response=response,
            current_state=agent.current_state(),
            metadata=metadata,
            message="Response generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"API error in /session/continue: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error continuing session: {str(e)}")


@app.get("/session/status/{thread_id}", response_model=SessionStatusResponse)
def get_session_status(thread_id: str):
    """
    Get current status and progress of a session
    
    Returns current pedagogical state, concept progress, and other metrics.
    """
    try:
        print(f"API /session/status - thread: {thread_id}")
        
        agent = get_session(thread_id)
        if not agent:
            return SessionStatusResponse(
                success=True,
                thread_id=thread_id,
                exists=False,
                message="Session not found"
            )
        
        state = agent.state
        progress = {
            "current_state": agent.current_state(),
            "asked_apk": state.get("asked_apk", False),
            "asked_ci": state.get("asked_ci", False),
            "asked_ge": state.get("asked_ge", False),
            "asked_ar": state.get("asked_ar", False),
            "asked_tc": state.get("asked_tc", False),
            "asked_rlc": state.get("asked_rlc", False),
            "concepts": state.get("sim_concepts", []),
            "current_concept_idx": state.get("sim_current_idx", 0),
            "total_concepts": len(state.get("sim_concepts", [])),
            "in_simulation": state.get("in_simulation", False),
            "misconception_detected": state.get("misconception_detected", False),
        }
        
        return SessionStatusResponse(
            success=True,
            thread_id=thread_id,
            exists=True,
            current_state=agent.current_state(),
            progress=progress,
            concept_title=concept_pkg.title,
            message="Status retrieved successfully"
        )
        
    except Exception as e:
        print(f"API error in /session/status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving status: {str(e)}")


@app.get("/session/history/{thread_id}", response_model=SessionHistoryResponse)
def get_session_history(thread_id: str):
    """
    Get full conversation history for a session
    
    Returns all messages and node transitions for analysis or display.
    """
    try:
        print(f"API /session/history - thread: {thread_id}")
        
        agent = get_session(thread_id)
        if not agent:
            return SessionHistoryResponse(
                success=True,
                thread_id=thread_id,
                exists=False,
                message="Session not found"
            )
        
        # Get conversation history
        history = agent.get_history_for_reports()
        
        # Get node transitions
        node_transitions = agent.state.get("node_transitions", [])
        
        return SessionHistoryResponse(
            success=True,
            thread_id=thread_id,
            exists=True,
            messages=history,
            node_transitions=node_transitions,
            concept_title=concept_pkg.title,
            message="History retrieved successfully"
        )
        
    except Exception as e:
        print(f"API error in /session/history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@app.get("/session/summary/{thread_id}", response_model=SessionSummaryResponse)
def get_session_summary(thread_id: str):
    """
    Get session summary with metrics
    
    Returns quiz scores, transfer success, misconceptions, and other performance indicators.
    """
    try:
        print(f"API /session/summary - thread: {thread_id}")
        
        agent = get_session(thread_id)
        if not agent:
            return SessionSummaryResponse(
                success=True,
                thread_id=thread_id,
                exists=False,
                message="Session not found"
            )
        
        state = agent.state
        summary = state.get("session_summary", {})
        
        return SessionSummaryResponse(
            success=True,
            thread_id=thread_id,
            exists=True,
            summary=summary,
            quiz_score=state.get("quiz_score"),
            transfer_success=state.get("transfer_success"),
            misconception_detected=state.get("misconception_detected"),
            definition_echoed=state.get("definition_echoed"),
            message="Summary retrieved successfully"
        )
        
    except Exception as e:
        print(f"API error in /session/summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving summary: {str(e)}")


@app.delete("/session/{thread_id}")
def delete_session(thread_id: str):
    """
    Delete/clear a session
    
    Removes session from active sessions. Note: LangGraph checkpoint may still exist.
    """
    try:
        print(f"API /session DELETE - thread: {thread_id}")
        
        if thread_id in _active_sessions:
            del _active_sessions[thread_id]
            return {
                "success": True,
                "thread_id": thread_id,
                "message": "Session deleted successfully"
            }
        else:
            return {
                "success": False,
                "thread_id": thread_id,
                "message": "Session not found"
            }
            
    except Exception as e:
        print(f"API error in DELETE /session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


@app.post("/test/persona")
def test_with_persona(request: TestPersonaRequest):
    """
    Test endpoint to create a session with predefined persona
    
    Useful for automated testing with different student behaviors.
    """
    try:
        print(f"API /test/persona - persona: {request.persona_name}, concept: {request.concept_title}")
        
        # Create session with persona
        start_request = StartSessionRequest(
            concept_title=request.concept_title,
            persona_name=request.persona_name,
            session_label=f"test-{request.persona_name.lower().replace(' ', '-')}"
        )
        
        return start_session(start_request)
        
    except Exception as e:
        print(f"API error in /test/persona: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating test session: {str(e)}")


@app.get("/sessions")
def list_sessions():
    """
    List all active sessions (debugging endpoint)
    
    Returns basic info about all currently active sessions.
    """
    try:
        sessions_info = []
        for thread_id, agent in _active_sessions.items():
            sessions_info.append({
                "thread_id": thread_id,
                "session_id": agent.session_id,
                "user_id": agent.user_id,
                "current_state": agent.current_state(),
                "persona_name": agent.persona_name,
            })
        
        return {
            "success": True,
            "total_sessions": len(_active_sessions),
            "sessions": sessions_info
        }
        
    except Exception as e:
        print(f"API error in /sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing sessions: {str(e)}")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🎓 Educational Agent API Server Starting...")
    print("=" * 80)
    print(f"Agent Type: educational_agent_optimized_langsmith")
    print(f"Default Concept: {concept_pkg.title}")
    print(f"Persistence: InMemorySaver (LangGraph)")
    print("=" * 80)
    print("Available Endpoints:")
    print("  GET  / - API information")
    print("  GET  /health - Health check")
    print("  POST /session/start - Start new learning session")
    print("  POST /session/continue - Continue existing session")
    print("  GET  /session/status/{thread_id} - Get session status")
    print("  GET  /session/history/{thread_id} - Get conversation history")
    print("  GET  /session/summary/{thread_id} - Get session summary")
    print("  DELETE /session/{thread_id} - Delete session")
    print("  POST /test/persona - Test with predefined persona")
    print("  GET  /sessions - List all active sessions")
    print("=" * 80)
    print("Starting server on http://0.0.0.0:8000")
    print("API Docs available at http://localhost:8000/docs")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
