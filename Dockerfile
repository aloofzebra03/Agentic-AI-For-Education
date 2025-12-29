# Simple, production-ready Dockerfile for Educational API on EC2
# Pass environment variables at runtime (not baked into image)

FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies (PostgreSQL client libraries + build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file FIRST (for Docker layer caching)
COPY requirements-minimal2.txt /app/requirements.txt

# Fix potential Windows CRLF line endings
RUN sed -i 's/\r$//' /app/requirements.txt

# Copy project configuration
COPY pyproject.toml /app/pyproject.toml

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir uv==0.4.21 && \
    uv pip install --system --no-cache -vvv -r /app/requirements.txt


# Copy application code
COPY utils/ /app/utils/
COPY tester_agent/ /app/tester_agent/
COPY educational_agent_optimized_langsmith_autosuggestion/ /app/educational_agent_optimized_langsmith_autosuggestion/
COPY api_tracker_utils/ /app/api_tracker_utils/ 
COPY api_servers/ /app/api_servers/
COPY NCERT/ /app/NCERT/

# Install project in editable mode (makes all modules importable)
RUN pip install --no-cache-dir -e .

# DO NOT copy .env file into image (pass secrets at runtime)

# Expose API port (documentation only)
EXPOSE 8000

# Set environment variable to skip table setup (tables must already exist)
ENV SKIP_POSTGRES_SETUP=true

# Run FastAPI server
# IMPORTANT: For Transaction Mode (port 6543), ensure tables are created beforehand
# Environment variables will be passed at runtime via docker run -e or --env-file
CMD ["uvicorn", "api_servers.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
