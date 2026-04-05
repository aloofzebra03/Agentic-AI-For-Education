import os
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, APIKeyHeader
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging

from api_servers.firebase_client import is_email_allowed

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


def get_current_user(
    auth_header: HTTPAuthorizationCredentials | None = Depends(security_bearer),
    api_key: str | None = Depends(api_key_schema)
) -> dict:
    """
    Dependency to get the current authenticated user.
    Authenticates using either an API Key or a Google JWT token verifyable through Firebase.
    """
    # 1. API Key Authentication (highest priority)
    if api_key:
        api_key_clean = api_key.strip().strip("'").strip('"')
        if api_key_clean in API_KEYS:
            return {"user": "admin_api_user", "auth_method": "api_key"}
        else:
            logger.warning("Invalid API key provided.")
            
    # 2. Google JWT Authentication
    if auth_header:
        token = auth_header.credentials
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
            email = idinfo.get('email')

            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid token: No email found."
                )

            # Verify the email corresponds to a registered user document in Firestore 'users' collection
            if not is_email_allowed(email):
                logger.warning(f"Unauthorized email attempted access: {email}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Email not authorized: Must be a registered user."
                )

            return {"user": "app_user", "email": email, "auth_method": "jwt"}

        except ValueError as e:
            logger.error(f"JWT Verification Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired Google JWT token."
            )
            
    # If neither is provided or valid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Missing or invalid authentication credentials. Provide a Bearer token or X-API-Key."
    )


def get_docs_username(credentials: HTTPBasicCredentials = Depends(security_basic)) -> str:
    """
    Dependency to secure API documentation (/docs, /openapi.json) with Basic auth.
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
