"""
Per-email daily API rate limits — backed by Postgres (preferred), then in-process memory.

Firestore rate_limits collection is no longer used (it was burning Firebase quota on
every /session/start and /session/continue).

Env:
  RATE_LIMIT_FAIL_OPEN=true  — allow requests if all backends fail (default: true)
  POSTGRES_DATABASE_URL      — same Supabase/Postgres URL as LangGraph checkpointer
"""

from __future__ import annotations

import logging
import os
import threading
import time
from datetime import datetime, timezone, timedelta
from typing import Tuple

logger = logging.getLogger(__name__)

_IST = timezone(timedelta(hours=5, minutes=30))

_table_ready = False
_table_lock = threading.Lock()
_memory_lock = threading.Lock()
_memory_counts: dict[str, int] = {}


def _today_ist() -> str:
    return datetime.now(_IST).strftime("%Y-%m-%d")


def _fail_open() -> bool:
    return os.getenv("RATE_LIMIT_FAIL_OPEN", "true").lower() in ("1", "true", "yes")


def _ensure_postgres_table(conn) -> None:
    global _table_ready
    if _table_ready:
        return
    with _table_lock:
        if _table_ready:
            return
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS api_rate_limits (
                    email TEXT NOT NULL,
                    rate_date DATE NOT NULL,
                    count INTEGER NOT NULL DEFAULT 0,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    PRIMARY KEY (email, rate_date)
                );
                """
            )
        _table_ready = True
        logger.info("api_rate_limits table ready (Postgres)")


def _postgres_increment(email: str, today: str, daily_limit: int) -> Tuple[int, int, bool]:
    import psycopg

    postgres_url = os.getenv("POSTGRES_DATABASE_URL", "").strip()
    if not postgres_url:
        raise EnvironmentError("POSTGRES_DATABASE_URL not set")

    with psycopg.connect(
        postgres_url,
        autocommit=True,
        prepare_threshold=None,
        connect_timeout=10,
    ) as conn:
        _ensure_postgres_table(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO api_rate_limits (email, rate_date, count)
                VALUES (%s, %s::date, 1)
                ON CONFLICT (email, rate_date)
                DO UPDATE SET
                    count = api_rate_limits.count + 1,
                    updated_at = NOW()
                RETURNING count;
                """,
                (email, today),
            )
            row = cur.fetchone()
            if not row:
                raise RuntimeError("Postgres rate limit upsert returned no row")
            new_count = int(row[0])

    remaining = max(0, daily_limit - new_count)
    limit_exceeded = new_count > daily_limit
    logger.info(
        "Rate-limit [postgres] email=%s date=%s count=%s/%s exceeded=%s",
        email,
        today,
        new_count,
        daily_limit,
        limit_exceeded,
    )
    return new_count, remaining, limit_exceeded


def _memory_increment(email: str, today: str, daily_limit: int) -> Tuple[int, int, bool]:
    key = f"{email}:{today}"
    with _memory_lock:
        new_count = _memory_counts.get(key, 0) + 1
        _memory_counts[key] = new_count

    remaining = max(0, daily_limit - new_count)
    limit_exceeded = new_count > daily_limit
    logger.info(
        "Rate-limit [memory] email=%s date=%s count=%s/%s exceeded=%s",
        email,
        today,
        new_count,
        daily_limit,
        limit_exceeded,
    )
    return new_count, remaining, limit_exceeded


def check_and_increment(email: str, daily_limit: int) -> Tuple[int, int, bool]:
    """
    Atomically increment today's counter for email (IST calendar day).

    Returns:
        (new_count, remaining, limit_exceeded)
    """
    email = email.strip().lower()
    today = _today_ist()

    try:
        return _postgres_increment(email, today, daily_limit)
    except Exception as exc:
        logger.warning("Postgres rate limit unavailable for %s: %s", email, exc)

    try:
        return _memory_increment(email, today, daily_limit)
    except Exception as exc:
        logger.error("In-memory rate limit failed for %s: %s", email, exc)

    if _fail_open():
        logger.warning(
            "Rate-limit fail-open for %s (all backends failed); allowing request",
            email,
        )
        return 0, daily_limit, False

    raise RuntimeError(f"Rate limit backends unavailable for {email}")
