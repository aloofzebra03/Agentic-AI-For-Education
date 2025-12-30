"""
FastAPI Application for Concept Map Timeline Generation
========================================================
Provides REST API endpoints to generate concept maps with reveal times from educational descriptions.

Endpoints:
- POST /generate-concept-map: Generate timeline JSON from description
- GET /health: Health check endpoint
"""

import os
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Import core functions (no UI dependencies)
from concept_map_poc.timeline_mapper import create_timeline
from concept_map_poc.streamlit_app_standalone import save_timeline_json_to_disk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Verify API key is loaded
if not os.getenv('GOOGLE_API_KEY'):
    logger.error("⚠️ GOOGLE_API_KEY not found in environment variables!")
    raise RuntimeError("GOOGLE_API_KEY is required. Please set it in your .env file.")

# Initialize FastAPI app
app = FastAPI(
    title="Concept Map Timeline API",
    description="Generate educational concept maps with character-based timing from text descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Request/Response Models
class ConceptMapRequest(BaseModel):
    """Request model for concept map generation"""
    description: str = Field(
        ...,
        min_length=1,
        description="Educational description text to analyze (1 word to 3000+ words)",
        example="Photosynthesis is the process by which plants convert light energy into chemical energy."
    )
    educational_level: str = Field(
        default="high school",
        description="Target educational level for concept extraction",
        example="high school"
    )
    topic_name: Optional[str] = Field(
        default=None,
        description="Optional topic name (auto-extracted if not provided)",
        example="Photosynthesis"
    )

    class Config:
        schema_extra = {
            "example": {
                "description": "Photosynthesis is the process by which green plants convert light energy into chemical energy using chlorophyll in chloroplasts.",
                "educational_level": "high school",
                "topic_name": "Photosynthesis"
            }
        }


class ConceptMapResponse(BaseModel):
    """Response model for concept map generation"""
    success: bool = Field(description="Whether the operation was successful")
    filepath: str = Field(description="Path to the saved JSON file in concept_json_timings/ folder")
    timeline: dict = Field(description="Complete timeline data with concepts and reveal times")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "filepath": "concept_json_timings/photosynthesis_20251221_143022.json",
                "timeline": {
                    "metadata": {
                        "topic_name": "Photosynthesis",
                        "educational_level": "high school",
                        "total_duration": 25.5,
                        "total_concepts": 6
                    },
                    "concepts": [
                        {
                            "name": "Photosynthesis",
                            "reveal_time": 0.0,
                            "importance_rank": 1
                        }
                    ]
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    service: str
    version: str
    api_key_configured: bool


# API Endpoints
@app.post(
    "/generate-concept-map",
    response_model=ConceptMapResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Concept Map Timeline",
    description="Analyzes educational description and generates a timeline JSON with concept reveal times"
)
async def generate_concept_map(request: ConceptMapRequest):
    """
    Generate concept map timeline from educational description.
    
    This endpoint:
    1. Accepts educational text description
    2. Extracts key concepts using Google Gemini AI
    3. Calculates character-based reveal times for each concept
    4. Saves complete timeline JSON to concept_json_timings/ folder
    5. Returns both the filepath and complete timeline data
    
    The generated JSON includes:
    - Concepts with reveal_time values (when to show each concept)
    - Relationships between concepts
    - Word-level timings (character-based: 0.08s per character)
    - Metadata (duration, concept count, etc.)
    """
    try:
        logger.info(f"📥 Received request: {len(request.description)} characters, level: {request.educational_level}")
        
        # Validate description length
        if len(request.description.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description cannot be empty"
            )
        
        # Step 1: Create timeline using core function
        # This calls Gemini API, calculates timings, and assigns reveal times
        logger.info("🔄 Creating timeline...")
        timeline = create_timeline(
            description=request.description,
            educational_level=request.educational_level,
            topic_name=request.topic_name or ""
        )
        
        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create timeline. Check logs for details."
            )
        
        concepts_count = len(timeline.get('concepts', []))
        duration = timeline.get('metadata', {}).get('total_duration', 0.0)
        logger.info(f"✅ Timeline created: {concepts_count} concepts, {duration:.1f}s duration")
        
        # Step 2: Save JSON to disk (concept_json_timings/ folder)
        logger.info("💾 Saving timeline to disk...")
        filepath = save_timeline_json_to_disk(timeline)
        
        if not filepath:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save timeline JSON to disk"
            )
        
        logger.info(f"✅ Saved to: {filepath}")
        
        # Return success response with filepath and timeline data
        return ConceptMapResponse(
            success=True,
            filepath=filepath,
            timeline=timeline
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors and return 500
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check API health and configuration status"
)
async def health_check():
    """
    Health check endpoint to verify the API is running and properly configured.
    
    Returns service status, version, and configuration details.
    """
    return HealthResponse(
        status="healthy",
        service="concept-map-api",
        version="1.0.0",
        api_key_configured=bool(os.getenv('GOOGLE_API_KEY'))
    )


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - redirects to docs"""
    return {
        "message": "Concept Map Timeline API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("🚀 Concept Map Timeline API starting...")
    logger.info(f"📁 Working directory: {os.getcwd()}")
    logger.info(f"🔑 API Key configured: {bool(os.getenv('GOOGLE_API_KEY'))}")
    
    # Ensure output directory exists
    output_dir = Path("concept_json_timings")
    output_dir.mkdir(exist_ok=True)
    logger.info(f"📂 Output directory ready: {output_dir.absolute()}")
    
    logger.info("✅ API ready to accept requests")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("🛑 Concept Map Timeline API shutting down...")


if __name__ == "__main__":
    # Run with uvicorn when executed directly
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (disable in production)
        log_level="info"
    )
