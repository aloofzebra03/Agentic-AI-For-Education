"""
FastAPI Server for Teaching Agent
==================================
REST API endpoints for Android app to interact with the teaching agent.

Run with: uvicorn api_server:app --reload --port 8000
API docs available at: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from api_models import (
    StartSessionRequest,
    StudentResponseRequest,
    SessionResponse,
    HealthCheckResponse,
    ErrorResponse,
    QuizSubmissionRequest,
    QuizEvaluationResponse
)
from api_integration import (
    create_teaching_session,
    process_student_input,
    get_session_info,
    get_available_simulations,
    validate_simulation_id,
    submit_quiz_answer
)


# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Adaptive Teaching Agent API",
    description="""
    REST API for the adaptive physics teaching agent.
    
    ## Features
    * Start new teaching sessions for different simulations
    * Send student responses and receive teacher feedback
    * Retrieve session state for recovery
    * Automatic parameter adjustments for visual demonstrations
    
    ## Available Simulations
    * `simple_pendulum` - Time & Pendulums
    * `earth_rotation_revolution` - Earth's Rotation & Revolution  
    * `light_shadows` - Light & Shadows
    
    ## Integration
    Designed for Android app integration with bi-directional communication
    between the teaching agent and interactive HTML5 simulations.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ═══════════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════

# Enable CORS for cross-origin requests (Android app, web testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ═══════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

@app.get(
    "/",
    response_model=HealthCheckResponse,
    tags=["Health Check"],
    summary="API Health Check"
)
async def root():
    """
    Health check endpoint to verify API is running.
    
    Returns basic information about the service and available simulations.
    """
    return {
        "status": "online",
        "service": "Teaching Agent API",
        "version": "1.0.0",
        "available_simulations": get_available_simulations()
    }


@app.post(
    "/api/session/start",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Session Management"],
    summary="Start New Teaching Session"
)
async def start_session(request: StartSessionRequest):
    """
    Start a new teaching session for a specific simulation.
    
    ## Process
    1. Validates the simulation_id
    2. Creates a new session with unique session_id
    3. Loads concepts for the simulation
    4. Generates initial teacher message
    5. Returns session state with simulation URL
    
    ## Response
    Returns complete session state including:
    - Unique session_id for subsequent requests
    - Initial simulation URL with parameters
    - First teacher message
    - All concepts for the simulation
    - Initial learning state
    
    ## Example
    ```json
    {
      "simulation_id": "simple_pendulum",
      "student_id": "student_12345"
    }
    ```
    """
    try:
        # Validate simulation ID
        if not validate_simulation_id(request.simulation_id):
            available = get_available_simulations()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid Simulation",
                    "message": f"Simulation '{request.simulation_id}' not found",
                    "available_simulations": available
                }
            )
        
        # Create session
        session_id, response = create_teaching_session(
            simulation_id=request.simulation_id,
            student_id=request.student_id
        )
        
        return response
        
    except ValueError as e:
        # Invalid simulation or configuration error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid Request",
                "message": str(e)
            }
        )
    except Exception as e:
        # Unexpected error
        print(f"\n❌ Error creating session:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "Failed to create teaching session",
                "detail": str(e)
            }
        )


@app.post(
    "/api/session/{session_id}/respond",
    response_model=SessionResponse,
    tags=["Session Management"],
    summary="Send Student Response"
)
async def send_response(session_id: str, request: StudentResponseRequest):
    """
    Send a student's response and receive teacher's reply.
    
    ## Process
    1. Validates session exists
    2. Processes student response through teaching agent
    3. Evaluates understanding level
    4. Generates teacher response
    5. May change simulation parameters for demonstration
    6. Returns updated session state
    
    ## Response
    Returns updated session state including:
    - Teacher's response message
    - Updated simulation URL (if parameters changed)
    - Parameter change details (before/after comparison)
    - Updated understanding level and learning state
    - Concept progression information
    
    ## Example
    ```json
    {
      "student_response": "I think it swings faster?"
    }
    ```
    """
    try:
        # Process student input
        response = process_student_input(
            session_id=session_id,
            student_response=request.student_response
        )
        
        return response
        
    except KeyError:
        # Session not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Session Not Found",
                "message": f"Session '{session_id}' does not exist or has expired",
                "session_id": session_id
            }
        )
    except Exception as e:
        # Unexpected error
        print(f"\n❌ Error processing response:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "Failed to process student response",
                "detail": str(e),
                "session_id": session_id
            }
        )


@app.get(
    "/api/session/{session_id}",
    response_model=SessionResponse,
    tags=["Session Management"],
    summary="Get Session State"
)
async def get_session(session_id: str):
    """
    Retrieve current state of a teaching session.
    
    ## Purpose
    Used for recovering session state after:
    - App crashes or restarts
    - Network interruptions
    - Device changes
    
    ## Response
    Returns complete session state including:
    - Full conversation history
    - Current simulation state and parameters
    - Current concept and learning progress
    - Understanding level and trajectory
    - All metadata for state restoration
    
    ## Use Case
    Android app can save session_id in SharedPreferences and restore
    the exact state when user reopens the app.
    """
    try:
        # Retrieve session state
        response = get_session_info(session_id)
        
        return response
        
    except KeyError:
        # Session not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Session Not Found",
                "message": f"Session '{session_id}' does not exist or has expired",
                "session_id": session_id
            }
        )
    except Exception as e:
        # Unexpected error
        print(f"\n❌ Error retrieving session:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "Failed to retrieve session state",
                "detail": str(e),
                "session_id": session_id
            }
        )


# ═══════════════════════════════════════════════════════════════════════
# ADDITIONAL UTILITY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

@app.post(
    "/api/session/{session_id}/submit-quiz",
    response_model=QuizEvaluationResponse,
    tags=["Quiz Management"],
    summary="Submit Quiz Answer"
)
async def submit_quiz(session_id: str, request: QuizSubmissionRequest):
    """
    Submit quiz answer with parameters from simulation.
    
    ## Process
    1. Validates session exists and is in quiz mode
    2. Evaluates submitted parameters against success rules (fast, rule-based)
    3. Generates adaptive feedback using LLM based on score and attempt
    4. Determines if retry is allowed (max 3 attempts)
    5. Returns evaluation with feedback and quiz progress
    
    ## Request Body
    ```json
    {
      "question_id": "pendulum_q1",
      "submitted_parameters": {
        "length": 5.0,
        "mass": 1.0,
        "number_of_oscillations": 10
      },
      "attempt_number": 1
    }
    ```
    
    ## Response
    Returns evaluation including:
    - Score (1.0=perfect, 0.5=partial, 0.0=wrong)
    - Status (RIGHT, PARTIALLY_RIGHT, WRONG)
    - Adaptive teacher feedback
    - Whether retry is allowed
    - Quiz progress statistics
    - Next question details (if applicable)
    
    ## Scoring
    - **Perfect (1.0)**: All parameters meet perfect criteria
    - **Partial (0.5)**: Parameters meet partial criteria
    - **Wrong (0.0)**: Parameters don't meet minimum criteria
    
    ## Retry Logic
    - Maximum 3 attempts per question
    - Progressive hints provided with each attempt
    - After 3 attempts or correct answer, moves to next question
    """
    try:
        # Submit quiz answer and get evaluation
        response = submit_quiz_answer(
            session_id=session_id,
            question_id=request.question_id,
            submitted_parameters=request.submitted_parameters
        )
        
        return response
        
    except KeyError as e:
        # Session not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Session Not Found",
                "message": str(e)
            }
        )
    except ValueError as e:
        # Invalid state (e.g., not in quiz mode)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid Request",
                "message": str(e)
            }
        )
    except Exception as e:
        # Unexpected error
        print(f"\n❌ Error submitting quiz:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "Failed to evaluate quiz submission",
                "detail": str(e)
            }
        )


@app.get(
    "/api/simulations",
    tags=["Information"],
    summary="List Available Simulations"
)
async def list_simulations():
    """
    Get list of all available simulations.
    
    Returns simulation IDs that can be used with /api/session/start
    """
    from simulations_config import get_all_simulations
    
    all_sims = get_all_simulations()
    
    return {
        "simulations": [
            {
                "id": sim_id,
                "title": sim_data["title"],
                "description": sim_data["description"].strip(),
                "concepts_count": len(sim_data["concepts"])
            }
            for sim_id, sim_data in all_sims.items()
        ]
    }


# ═══════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": str(request.url)
        }
    )


# ═══════════════════════════════════════════════════════════════════════
# SERVER STARTUP
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting Teaching Agent API Server")
    print("="*60)
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
