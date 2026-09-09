"""Shared PostgreSQL resources for LangGraph checkpoint persistence."""

import os
import threading
from typing import Optional

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool


_POOL_MIN_SIZE = 5
_POOL_MAX_SIZE = 40

_lock = threading.Lock()
_pool: Optional[ConnectionPool] = None
_checkpointer: Optional[PostgresSaver] = None


def _create_pool(postgres_url: str) -> ConnectionPool:
    connection_kwargs = {
        "autocommit": True,
        # Supabase Transaction Mode doesn't support session-level prepared
        # statements reliably because transactions can use different backends.
        "prepare_threshold": None,
        "gssencmode": "disable",
        # Detect broken network paths promptly instead of retaining dead sockets.
        "keepalives": 1,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

    return ConnectionPool(
        conninfo=postgres_url,
        min_size=_POOL_MIN_SIZE,
        max_size=_POOL_MAX_SIZE,
        timeout=30,
        max_idle=120,
        max_lifetime=1800,
        reconnect_timeout=30,
        kwargs=connection_kwargs,
        # A pool doesn't validate idle connections by default. This prevents a
        # connection dropped by the database/pooler from reaching PostgresSaver.
        check=ConnectionPool.check_connection,
        name="langgraph-checkpoints",
    )


def get_shared_checkpointer() -> PostgresSaver:
    """Return the process-wide PostgresSaver backed by one pool of at most 40."""
    global _pool, _checkpointer

    if _checkpointer is not None:
        return _checkpointer

    with _lock:
        if _checkpointer is not None:
            return _checkpointer

        postgres_url = os.getenv("POSTGRES_DATABASE_URL")
        if not postgres_url:
            raise ValueError("POSTGRES_DATABASE_URL environment variable is not set")

        pool = _create_pool(postgres_url)
        try:
            checkpointer = PostgresSaver(pool)

            if os.getenv("SKIP_POSTGRES_SETUP", "true").lower() != "true":
                checkpointer.setup()
        except Exception:
            pool.close()
            raise

        _pool = pool
        _checkpointer = checkpointer
        print(
            "Shared Postgres checkpointer initialized "
            f"(pool size: {_POOL_MIN_SIZE}-{_POOL_MAX_SIZE}, connection validation enabled)"
        )
        return checkpointer


def close_shared_postgres_pool() -> None:
    """Close the shared pool during application shutdown."""
    global _pool, _checkpointer

    with _lock:
        if _pool is not None:
            _pool.close()
        _pool = None
        _checkpointer = None
