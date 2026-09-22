"""Host adapters that mount the POC whiteboard package in the main API."""

from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Any

from api_servers.auth import get_current_user, get_current_user_rate_limited
from api_tracker_utils.error import DayLimitExhaustedError, MinuteLimitExhaustedError
from api_tracker_utils.tracker import get_next_available_api_model_pair, track_model_call
from utils.postgres_checkpointer import get_shared_checkpointer
from utils.shared_utils import get_llm, normalize_llm_response
from api_servers.request_timing import (
    bind_timing_store,
    build_server_timing_header,
    measure,
    record_duration,
)
from whiteboard_tutor.router import create_whiteboard_router
from whiteboard_tutor.runtime import create_runtime


def invoke_tracked_whiteboard_llm(
    messages: list[Any], temperature: float, operation_name: str
) -> Any:
    """Use the main API's numbered keys and existing quota tracker."""
    api_key, model = get_next_available_api_model_pair()
    track_model_call(api_key, model)
    print(
        f"[WHITEBOARD LLM] operation={operation_name} model={model} "
        f"temperature={temperature} key=***{api_key[-4:]}"
    )
    response = get_llm(api_key=api_key, model=model, temperature=temperature).invoke(messages)
    return normalize_llm_response(response)


@contextmanager
def measure_whiteboard_start(user: Any):
    timings = user.get("_server_timings", {}) if isinstance(user, dict) else {}
    with bind_timing_store(timings):
        with measure("whiteboard_session_start"):
            yield


def finish_whiteboard_start_timing(user: Any, response: Any) -> None:
    if not isinstance(user, dict):
        return
    timings = user.get("_server_timings", {})
    request_started_at = user.get("_request_started_at")
    if request_started_at is not None:
        record_duration(
            "server_total",
            (perf_counter() - request_started_at) * 1000,
            timings,
        )
    response.headers["Server-Timing"] = build_server_timing_header(timings)


whiteboard_runtime = create_runtime(
    checkpointer=get_shared_checkpointer(),
    llm_invoker=invoke_tracked_whiteboard_llm,
)

whiteboard_tutor_router = create_whiteboard_router(
    whiteboard_runtime,
    prefix="/whiteboard-tutor",
    read_auth=get_current_user,
    llm_auth=get_current_user_rate_limited,
    minute_limit_errors=(MinuteLimitExhaustedError,),
    day_limit_errors=(DayLimitExhaustedError,),
    thread_prefix="whiteboard-tutor",
    scenes_path="/scenes",
    start_timing_context=measure_whiteboard_start,
    finish_start_timing=finish_whiteboard_start_timing,
)
