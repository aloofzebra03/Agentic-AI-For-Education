"""Request-local timing helpers exposed through the Server-Timing header."""

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from time import perf_counter
from typing import Callable, Iterator, MutableMapping, Optional


TimingStore = MutableMapping[str, dict[str, float | int]]
_active_timing_store: ContextVar[Optional[TimingStore]] = ContextVar(
    "active_timing_store", default=None
)


def new_timing_store() -> TimingStore:
    return {}


def record_duration(
    name: str,
    duration_ms: float,
    store: Optional[TimingStore] = None,
) -> None:
    target = store if store is not None else _active_timing_store.get()
    if target is None:
        return

    metric = target.setdefault(name, {"duration_ms": 0.0, "calls": 0})
    metric["duration_ms"] = float(metric["duration_ms"]) + duration_ms
    metric["calls"] = int(metric["calls"]) + 1


@contextmanager
def measure(name: str, store: Optional[TimingStore] = None) -> Iterator[None]:
    started_at = perf_counter()
    try:
        yield
    finally:
        record_duration(name, (perf_counter() - started_at) * 1000, store)


def timed(name: str):
    """Decorate a synchronous function with request-local timing."""
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with measure(name):
                return function(*args, **kwargs)
        return wrapper
    return decorator


@contextmanager
def bind_timing_store(store: TimingStore) -> Iterator[None]:
    token = _active_timing_store.set(store)
    try:
        yield
    finally:
        _active_timing_store.reset(token)


def build_server_timing_header(store: TimingStore) -> str:
    parts = []
    for name, metric in store.items():
        duration_ms = float(metric["duration_ms"])
        calls = int(metric["calls"])
        parts.append(f'{name};dur={duration_ms:.3f};desc="calls={calls}"')
    return ", ".join(parts)
