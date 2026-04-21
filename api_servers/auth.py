import os
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, APIKeyHeader
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging

from api_servers.firebase_client import is_email_allowed, check_and_increment_rate_limit, DAILY_REQUEST_LIMIT

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Auth Configuration
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
API_KEYS = set(k.strip().strip("'").strip('"') for k in filter(None, os.getenv("API_KEYS", "").split(",")))
DOCS_USERNAME = os.getenv("DOCS_USERNAME", "admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "password")

security_bearer = HTTPBearer(auto_error=False)
security_basic = HTTPBasic()
api_key_schema = APIKeyHeader(name="X-API-Key", auto_error=False)


def _verify_user_base(
    auth_header: HTTPAuthorizationCredentials | None = Depends(security_bearer),
    api_key: str | None = Depends(api_key_schema),
) -> dict:
    """
    Base dependency that ONLY authenticates the user (via API Key or Google JWT).
    It checks if the email is allowed, but it DOES NOT process rate limits.
    """
    # ── 1. API Key Authentication (highest priority) ────────
    if api_key:
        api_key_clean = api_key.strip().strip("'").strip('"')
        if api_key_clean in API_KEYS:
            return {"user": "admin_api_user", "auth_method": "api_key"}
        # Invalid key — fall through so JWT path can run (or 401 below)
        logger.warning("Invalid API key provided; attempting JWT fallback.")

    # ── 2. Google JWT Authentication ───────────────────────────────────────────
    if auth_header:
        token = auth_header.credentials
        try:
            # Verify the token with Google's OAuth2 infrastructure
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
            email = idinfo.get("email")

            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: No email claim found.",
                )

            # Authorization: email must exist in 'users' collection
            if not is_email_allowed(email):
                logger.warning(f"Unauthorized email attempted access: {email}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Email not authorized: Must be a registered user.",
                )

            return {
                "user": "app_user",
                "email": email,
                "auth_method": "jwt",
            }

        except HTTPException:
            raise  # Re-raise 403 as-is without wrapping
        except ValueError as e:
            logger.error(f"JWT Verification Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Google JWT token.",
            )

    # ── 3. No valid credentials provided ──────────────────────────────────────
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid authentication credentials. Provide a Bearer token or X-API-Key.",
    )


def get_current_user(user: dict = Depends(_verify_user_base)) -> dict:
    """
    Dependency to get the current authenticated user WITHOUT counting towards rate limits.
    Use this for read-heavy setup/polling endpoints like /concepts or /status.
    """
    return user


def get_current_user_rate_limited(
    response: Response,
    user: dict = Depends(_verify_user_base)
) -> dict:
    """
    Dependency to get the current authenticated user AND increment the daily rate limit count.
    Use this for heavy/LLM-based endpoints. Adds X-RateLimit-* headers to the response.
    """
    if user.get("auth_method") == "jwt":
        email = user["email"]
        
        # Per-email daily rate limit
        new_count, remaining, limit_exceeded = check_and_increment_rate_limit(email)

        # Always attach rate-limit headers so clients can display usage
        response.headers["X-RateLimit-Limit"]     = str(DAILY_REQUEST_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Policy"]    = f"{DAILY_REQUEST_LIMIT};w=86400"

        if limit_exceeded:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    f"Daily limit of {DAILY_REQUEST_LIMIT} requests exceeded. "
                    "Counter resets at midnight IST (Indian Standard Time)."
                ),
                headers={
                    "X-RateLimit-Limit":     str(DAILY_REQUEST_LIMIT),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Policy":    f"{DAILY_REQUEST_LIMIT};w=86400",
                    "Retry-After":           "86400",
                },
            )
            
        user["requests_today"] = new_count
        user["requests_remaining"] = remaining
        
    return user


def get_docs_username(credentials: HTTPBasicCredentials = Depends(security_basic)) -> str:
    """
    Dependency to secure API documentation (/docs, /openapi.json) with HTTP Basic auth.
    """
    correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
