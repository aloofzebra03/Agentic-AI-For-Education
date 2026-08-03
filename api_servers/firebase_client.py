"""
Firebase Firestore client for:
  - Managing allowed emails (user authorization) — collection users/{email}

Daily API rate limits were moved to Postgres (see rate_limit_store.py) because
Firestore transactions on every agent call exhausted Firebase quota.

Setup:
  1. Go to Firebase Console -> Project Settings -> Service Accounts
  2. Click "Generate new private key" -> download the JSON file
  3. Set FIREBASE_SERVICE_ACCOUNT_PATH=/path/to/serviceAccountKey.json in .env
     OR set FIREBASE_SERVICE_ACCOUNT_JSON with the JSON content directly (good for Docker/cloud)

Env:
  ALLOWLIST_FAIL_OPEN=true  — if Firestore quota fails but JWT is valid, allow (default: true)
  ALLOWLIST_CACHE_TTL_SEC   — cache successful allowlist lookups (default: 300)
"""

import os
import json
import logging
import time
from typing import Tuple

import firebase_admin
from firebase_admin import credentials, firestore

from api_servers.rate_limit_store import check_and_increment as _store_check_and_increment

logger = logging.getLogger(__name__)

DAILY_REQUEST_LIMIT = int(os.getenv("DAILY_REQUEST_LIMIT", "100"))

_db = None
_allowlist_cache: dict[str, tuple[bool, float]] = {}
_allowlist_cache_lock = __import__("threading").Lock()


def _allowlist_cache_ttl_sec() -> int:
    try:
        return max(0, int(os.getenv("ALLOWLIST_CACHE_TTL_SEC", "300")))
    except ValueError:
        return 300


def _allowlist_fail_open() -> bool:
    return os.getenv("ALLOWLIST_FAIL_OPEN", "true").lower() in ("1", "true", "yes")


def _is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    if "resource_exhausted" in message or "quota exceeded" in message:
        return True
    code = getattr(exc, "code", None)
    if code is not None and str(code).upper() in ("RESOURCE_EXHAUSTED", "429"):
        return True
    return False


def _get_db():
    """Initialize Firebase app and return a Firestore client (singleton)."""
    global _db
    if _db is not None:
        return _db

    if firebase_admin._apps:
        _db = firestore.client()
        return _db

    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    if service_account_json:
        info = json.loads(service_account_json)
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(info)
        logger.info("Firebase: using inline service-account JSON from env var.")
    elif service_account_path:
        cred = credentials.Certificate(service_account_path)
        logger.info("Firebase: using service-account file at %s", service_account_path)
    else:
        raise EnvironmentError(
            "Firebase credentials not found. Set either "
            "FIREBASE_SERVICE_ACCOUNT_PATH or FIREBASE_SERVICE_ACCOUNT_JSON "
            "in your .env file."
        )

    firebase_admin.initialize_app(cred)
    _db = firestore.client()
    logger.info("Firebase initialized successfully.")
    return _db


def is_email_allowed(email: str) -> bool:
    """
    Check if the email exists in the Firestore users collection.
    Cached briefly to reduce Firestore reads during login bursts.
    """
    email = email.strip().lower()
    ttl = _allowlist_cache_ttl_sec()
    now = time.time()

    if ttl > 0:
        with _allowlist_cache_lock:
            cached = _allowlist_cache.get(email)
            if cached is not None and (now - cached[1]) < ttl:
                return cached[0]

    try:
        db = _get_db()
        doc = db.collection("users").document(email).get()
        allowed = doc.exists
        if ttl > 0:
            with _allowlist_cache_lock:
                _allowlist_cache[email] = (allowed, now)
        return allowed
    except Exception as e:
        logger.error("Failed to check if email '%s' exists in Firestore: %s", email, e)
        if _is_quota_error(e) and _allowlist_fail_open():
            logger.warning(
                "Allowlist fail-open for %s (Firestore quota/unavailable; JWT already verified)",
                email,
            )
            return True
        raise


def check_and_increment_rate_limit(
    email: str,
    daily_limit: int = DAILY_REQUEST_LIMIT,
) -> Tuple[int, int, bool]:
    """
    Increment the per-email daily counter (Postgres → in-memory → fail-open).
    """
    return _store_check_and_increment(email, daily_limit)
