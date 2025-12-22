# Concurrency and Thread Safety in FastAPI Applications

**Author's Note:** This document explains how FastAPI handles concurrent requests, why thread safety matters, and how to write safe code for production environments.

---

## Table of Contents

1. [Understanding the Problem](#understanding-the-problem)
2. [How FastAPI Handles Concurrency](#how-fastapi-handles-concurrency)
3. [Thread Safety Fundamentals](#thread-safety-fundamentals)
4. [Server Architectures: Uvicorn vs Gunicorn](#server-architectures-uvicorn-vs-gunicorn)
5. [Synchronous vs Asynchronous Functions](#synchronous-vs-asynchronous-functions)
6. [Common Thread Safety Issues](#common-thread-safety-issues)
7. [Safe Patterns for Our Codebase](#safe-patterns-for-our-codebase)
8. [Real-World Examples](#real-world-examples)

---

## Understanding the Problem

### The Misconception

When you write code like this:

```python
@app.post("/continue-session")
def continue_session(request):
    # Your code here
    return response
```

It **looks** like single-threaded, sequential code. You might think: "I'm just running one server with one worker, so only one request runs at a time, right?"

**Wrong!** Even with 1 uvicorn worker, FastAPI uses a **40-thread pool** to handle concurrent requests.

### The Reality

```
Your API Server (1 uvicorn worker):
┌─────────────────────────────────────────┐
│  Single Process                         │
│                                         │
│  Main Thread (Event Loop)               │
│  ├─ Receives HTTP requests              │
│  ├─ Routes to endpoints                 │
│  └─ Manages async operations            │
│                                         │
│  External Thread Pool (40 threads)      │
│  ├─ Thread 1: def continue_session()    │
│  ├─ Thread 2: def continue_session()    │
│  ├─ Thread 3: def continue_session()    │
│  ├─ ...                                 │
│  └─ Thread 40: def continue_session()   │
│         ↑                                │
│    ALL access same global variables!    │
└─────────────────────────────────────────┘
```

**Key Insight:** Multiple users hitting your API means multiple threads executing the **same function code** simultaneously, accessing the **same global state**.

---

## How FastAPI Handles Concurrency

### The Automatic Threading Model

FastAPI (via Starlette) automatically detects whether your endpoint is synchronous (`def`) or asynchronous (`async def`):

#### For `def` Endpoints (What we're using):

```python
@app.post("/continue-session")
def continue_session(request):  # ← Synchronous function
    # Blocking code
    response = llm.invoke(messages)
    return response
```

**What happens behind the scenes:**

```python
# Starlette's internal handling (simplified):
async def handle_request(request):
    # Your synchronous 'def' function gets delegated to thread pool
    result = await anyio.to_thread.run_sync(your_continue_session_function, request)
    return result
```

**Flow:**

1. Main event loop receives HTTP request
2. Sees endpoint is `def` (synchronous)
3. Delegates execution to thread pool (one of 40 threads by default)
4. Thread executes your code (blocking during I/O)
5. Returns result to event loop
6. Event loop sends HTTP response

### Concurrent Execution Example

```
Time: 0ms - User A sends request
  → Event Loop → Delegates to Thread 1
  → Thread 1 starts executing continue_session(request_A)

Time: 50ms - User B sends request (while Thread 1 still processing)
  → Event Loop → Delegates to Thread 2
  → Thread 2 starts executing continue_session(request_B)

Time: 100ms - User C sends request (while Threads 1 & 2 still processing)
  → Event Loop → Delegates to Thread 3
  → Thread 3 starts executing continue_session(request_C)

Result: 3 THREADS running the SAME CODE simultaneously!
```

### Why This Matters

All threads share the same memory space:

```python
# Global singleton - SHARED by all threads!
_api_key_tracker = ApiKeyPerformanceTracker()

def continue_session(request):
    # Thread 1, 2, 3... all access this same object
    _api_key_tracker.record_call(api_key, latency, success)
    #                    ↑
    #    If this is not thread-safe, data corruption occurs!
```

---

## Thread Safety Fundamentals

### What is Thread Safety?

**Thread-safe code** ensures correct behavior when accessed from multiple threads simultaneously, without race conditions, data corruption, or inconsistent state.

### The CPython GIL (Global Interpreter Lock)

Python has a GIL that allows only **one thread to execute Python bytecode at a time**. However:

- **GIL releases during I/O operations** (network calls, file reads, etc.)
- **GIL releases between bytecode instructions**
- **Not all operations are atomic** (even with GIL)

### Atomic vs Non-Atomic Operations

#### ✅ Atomic Operations (Thread-Safe):

```python
# These are SAFE without locks:
my_list.append(item)           # Single bytecode operation
x = some_dict[key]             # Simple read
some_dict[key] = value         # Simple write (if key exists)
x = y                          # Variable assignment
```

#### ❌ Non-Atomic Operations (NOT Thread-Safe):

```python
# These are UNSAFE without locks:
my_dict[key] += 1              # Read + Add + Write (3 operations)
my_dict[key] = my_dict.get(key, 0) + 1  # Read + Add + Write
if key in my_dict:             # Check + Write (2 operations)
    my_dict[key] += 1
x = x + 1                      # Read + Add + Write
```

### The Race Condition

```python
# UNSAFE CODE - Race condition example:
class Counter:
    def __init__(self):
        self.count = 0
  
    def increment(self):
        # This looks simple but is actually 3 operations:
        # 1. READ:  temp = self.count
        # 2. ADD:   temp = temp + 1
        # 3. WRITE: self.count = temp
        self.count += 1

# What happens with 2 threads:
Thread 1: READ count=0
Thread 2: READ count=0  ← Still sees 0!
Thread 1: ADD → 1
Thread 2: ADD → 1
Thread 1: WRITE count=1
Thread 2: WRITE count=1  ← Should be 2, but writes 1!

# Expected: 2 increments = count is 2
# Actual: count is 1 (lost update!)
```

### Thread Safety Solutions

#### 1. Use Atomic Operations

```python
# ✅ SAFE: list.append() is atomic
class ApiKeyPerformanceTracker:
    def __init__(self):
        self._calls = []  # List
  
    def record_call(self, api_key, latency, success):
        # Atomic operation - thread-safe!
        self._calls.append({
            "api_key": api_key,
            "latency_ms": latency,
            "success": success
        })
```

#### 2. Use Locks for Non-Atomic Operations

```python
import threading

# ✅ SAFE: Protected with lock
class RateLimitTracker:
    def __init__(self):
        self.counts = {}  # Dict
        self.lock = threading.Lock()  # Protection
  
    def record_call(self, api_key):
        with self.lock:  # Only ONE thread can enter at a time
            if api_key in self.counts:
                self.counts[api_key] += 1  # Now safe!
            else:
                self.counts[api_key] = 1
        # Lock automatically released here
```

#### 3. Use Thread-Safe Data Structures

```python
from queue import Queue
from collections import deque

# ✅ Queue is thread-safe
task_queue = Queue()

# ✅ deque.append() and deque.popleft() are thread-safe
event_log = deque(maxlen=1000)
```

---

## Server Architectures: Uvicorn vs Gunicorn

### Uvicorn (Our Current Setup)

**Type:** ASGI server (Asynchronous Server Gateway Interface)

**Architecture:**

```
Single Process
├─ Main Thread: Event loop for async I/O
└─ Thread Pool: 40 threads for synchronous endpoints
```

**Command:**

```bash
uvicorn api_servers.api_server:app --host "0.0.0.0" --port 8000
```

**Characteristics:**

- ✅ Built for async frameworks (FastAPI, Starlette)
- ✅ Excellent for I/O-bound applications
- ✅ Low memory footprint
- ✅ Global variables shared (single process)
- ❌ Limited to ~40 concurrent synchronous requests
- ❌ Single process = one CPU core utilized

**Best for:**

- Development environments
- Low to moderate traffic
- Applications with mostly async code

### Gunicorn (Production Alternative)

**Type:** WSGI/ASGI server (Web Server Gateway Interface)

**Architecture:**

```
Multiple Processes (workers)
├─ Process 1: Independent Python interpreter
├─ Process 2: Independent Python interpreter
├─ Process 3: Independent Python interpreter
└─ Process 4: Independent Python interpreter
     ↑
Each has separate memory space!
```

**Command:**

```bash
# Pure Gunicorn (WSGI only - doesn't support FastAPI well)
gunicorn -w 4 api_server:app

# Better: Gunicorn + Uvicorn workers (hybrid approach)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app
```

**Characteristics:**

- ✅ Multi-process = better CPU utilization
- ✅ Fault isolation (one process crash doesn't affect others)
- ✅ Can handle more total concurrent requests
- ❌ **Global variables NOT shared** between workers
- ❌ Higher memory usage (4 workers = 4× memory)

**Global State Issue:**

```python
# In shared_utils.py
_api_key_tracker = ApiKeyPerformanceTracker()

# With 4 Gunicorn workers:
Process 1: Has its own _api_key_tracker (tracks some requests)
Process 2: Has its own _api_key_tracker (tracks other requests)
Process 3: Has its own _api_key_tracker (tracks other requests)
Process 4: Has its own _api_key_tracker (tracks other requests)

# Problem: Each process has incomplete data!
# Solution: Use shared storage (Redis, database, shared memory)
```

### Hybrid Approach: Gunicorn + Uvicorn

**Best of both worlds for production:**

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app
```

**Architecture:**

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Process 1          │  │  Process 2          │  │  Process 3          │  │  Process 4          │
│  ├─ Event Loop      │  │  ├─ Event Loop      │  │  ├─ Event Loop      │  │  ├─ Event Loop      │
│  └─ Thread Pool(40) │  │  └─ Thread Pool(40) │  │  └─ Thread Pool(40) │  │  └─ Thread Pool(40) │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘

Total capacity: 4 processes × 40 threads = 160 concurrent synchronous requests
```

**When to use:**

- Production deployments with high traffic
- Need better CPU utilization across multiple cores
- Require fault isolation
- **Must handle global state differently!**

### Comparison Table

| Feature                             | Uvicorn (1 worker)         | Gunicorn + Uvicorn (4 workers) |
| ----------------------------------- | -------------------------- | ------------------------------ |
| **Processes**                 | 1                          | 4                              |
| **Threads per process**       | 40                         | 40                             |
| **Total concurrent capacity** | ~40 requests               | ~160 requests                  |
| **Memory usage**              | Low                        | High (4×)                     |
| **CPU utilization**           | 1 core                     | 4 cores                        |
| **Global state sharing**      | ✅ Works                   | ❌ Separate per process        |
| **Fault isolation**           | ❌ Single point of failure | ✅ Process crashes isolated    |
| **Setup complexity**          | Simple                     | Moderate                       |
| **Best for**                  | Development, low traffic   | Production, high traffic       |

---

## Synchronous vs Asynchronous Functions

### `def` (Synchronous Endpoints)

**What you write:**

```python
@app.post("/continue-session")
def continue_session(request):
    # Blocking code
    response = llm.invoke(messages)  # ⏸️ Thread waits here
    return response
```

**How it executes:**

1. FastAPI delegates to **thread pool**
2. Thread **blocks** during I/O (LLM API call)
3. Thread is **unavailable** until I/O completes
4. Returns result to event loop

**Concurrency model:**

```
Thread Pool (40 threads max):
Thread 1:  [Processing Request A ──────────] (blocked waiting for LLM)
Thread 2:  [Processing Request B ──────────] (blocked waiting for LLM)
Thread 3:  [Processing Request C ──────────] (blocked waiting for LLM)
...
Thread 40: [Processing Request Z ──────────] (blocked waiting for LLM)

If all 40 threads are busy, Request 41 must WAIT!
```

**Characteristics:**

- ✅ Simple to write (normal Python code)
- ✅ Works with any library (requests, LangChain, etc.)
- ✅ Easy to debug
- ❌ Limited by thread pool size (40 concurrent max)
- ❌ Memory overhead (~8MB per thread)
- ❌ Thread context switching overhead

### `async def` (Asynchronous Endpoints)

**What you write:**

```python
@app.post("/continue-session")
async def continue_session(request):
    # Non-blocking code
    response = await llm_async.invoke(messages)  # 🔄 Yields control
    return response
```

**How it executes:**

1. Runs **directly in event loop** (main thread)
2. When hitting `await`, **yields control** to event loop
3. Event loop can process other requests while waiting
4. When I/O completes, resumes execution

**Concurrency model:**

```
Event Loop (single thread):
Main Thread: [A][B][C][A][B][C][A][B][C]
              ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
         Interleaved execution - thousands possible!

No threads blocked - event loop switches between requests
```

**Characteristics:**

- ✅ Can handle **thousands** of concurrent requests
- ✅ Very low memory footprint (single thread)
- ✅ No context switching overhead
- ❌ Requires `await` for all I/O operations
- ❌ Must use async libraries (httpx instead of requests, etc.)
- ❌ More complex code and debugging

### When to Use Each

**Use `def` (synchronous) when:**

- Using libraries without async support (like LangChain's `.invoke()`)
- Code is simple and sequential
- Traffic is moderate (<40 concurrent requests)
- Rapid development is priority

**Use `async def` (asynchronous) when:**

- Handling high concurrency (100+ concurrent requests)
- Using async-compatible libraries
- Application is I/O-bound (many network calls)
- Memory efficiency is critical

### Converting Synchronous to Asynchronous

**Current code (synchronous):**

```python
def invoke_llm_with_fallback(messages, operation_name="LLM call", model="gemma-3-27b-it"):
    available_keys = get_available_api_keys()
  
    for api_key in available_keys:
        try:
            llm = get_llm(api_key=api_key, model=model)
            response = llm.invoke(messages)  # Blocking call
            return response
        except Exception as e:
            continue
  
    raise RuntimeError("All API keys failed")
```

**Async version:**

```python
async def invoke_llm_with_fallback(messages, operation_name="LLM call", model="gemma-3-27b-it"):
    available_keys = get_available_api_keys()
  
    for api_key in available_keys:
        try:
            llm = get_async_llm(api_key=api_key, model=model)  # Async client
            response = await llm.ainvoke(messages)  # Non-blocking call
            return response
        except Exception as e:
            continue
  
    raise RuntimeError("All API keys failed")

# Endpoint must also be async
@app.post("/continue-session")
async def continue_session(request):
    response = await invoke_llm_with_fallback(...)  # Must await
    return response
```

**Trade-off:**

- Better scalability, but requires changing entire call chain to async
- For our current use case: **Synchronous `def` is fine** (moderate traffic)

---

## Common Thread Safety Issues

### 1. Lost Updates (Race Condition)

**Problem:**

```python
# UNSAFE - Multiple threads incrementing counter
class RateLimiter:
    def __init__(self):
        self.counts = {}
  
    def record_call(self, api_key):
        # NOT ATOMIC - three operations!
        if api_key in self.counts:
            self.counts[api_key] += 1  # ❌ Race condition!
        else:
            self.counts[api_key] = 1
```

**What happens:**

```
Thread 1: Check if "key1" in counts → False
Thread 2: Check if "key1" in counts → False (context switch before Thread 1 writes)
Thread 1: Set counts["key1"] = 1
Thread 2: Set counts["key1"] = 1  ← Overwrites Thread 1's write!

Expected: 2 calls recorded
Actual: 1 call recorded (lost update!)
```

**Solution:**

```python
import threading

class RateLimiter:
    def __init__(self):
        self.counts = {}
        self.lock = threading.Lock()
  
    def record_call(self, api_key):
        with self.lock:  # ✅ Only one thread at a time
            if api_key in self.counts:
                self.counts[api_key] += 1
            else:
                self.counts[api_key] = 1
```

### 2. Corrupted File Writes

**Problem:**

```python
# UNSAFE - Multiple threads writing to same file
def export_metrics():
    data = get_metrics()
    with open("metrics.txt", "w") as f:
        f.write(data)  # ❌ Multiple threads can interleave writes!
```

**What happens:**

```
Thread 1: Opens file, starts writing "Metrics for API Key 1..."
Thread 2: Opens file, starts writing "Metrics for API Key 2..."
Thread 1: Continues writing "...latency: 250ms"
Thread 2: Continues writing "...latency: 180ms"

File contents (corrupted):
"Metrics for API Key 2...Metrics for API Key 1...latency: 180ms...latency: 250ms"
```

**⚠️ FastAPI-Specific Context:**

If your Python code performs file I/O operations (writes, reads, or both) **without proper thread safety**, and you serve this code via FastAPI with synchronous `def` endpoints:

- **The problem WILL occur** - FastAPI's automatic thread pool means multiple concurrent requests will execute your file I/O code in parallel threads
- **File corruption is likely** - Interleaved writes will produce corrupted/incomplete files
- **Data loss can happen** - Lost updates, partial writes, or race conditions during read-modify-write cycles

This is **guaranteed** when using `def` endpoints under concurrent load. The framework's threading model makes this inevitable without proper locking.

**Solution:**

```python
import threading

_export_lock = threading.Lock()

def export_metrics():
    with _export_lock:  # ✅ Only one export at a time
        data = get_metrics()
        with open("metrics.txt", "w") as f:
            f.write(data)
```

### 3. Partial Reads

**Problem:**

```python
# UNSAFE - Reading while another thread is writing
def read_config():
    with open("config.json", "r") as f:
        return json.load(f)  # ❌ May read incomplete JSON!
```

**What happens:**

```
Thread 1: Writing config: {"api_key": "abc123", "timeout": 30}
Thread 2: Reading config while Thread 1 is mid-write
Thread 2: Gets: {"api_key": "abc123", "tim
Thread 2: JSON parsing fails! ❌
```

**Solution:**

```python
import threading

_config_lock = threading.Lock()

def write_config(config):
    with _config_lock:
        with open("config.json", "w") as f:
            json.dump(config, f)

def read_config():
    with _config_lock:
        with open("config.json", "r") as f:
            return json.load(f)
```

### 4. Non-Atomic Dictionary Operations

**Problem:**

```python
# UNSAFE - get() with default and assignment
def update_stats(api_key):
    # Looks atomic but is actually 2 operations
    stats[api_key] = stats.get(api_key, 0) + 1  # ❌ Race condition!
```

**What happens:**

```
stats = {"key1": 5}

Thread 1: Reads stats.get("key1", 0) → 5
Thread 2: Reads stats.get("key1", 0) → 5 (before Thread 1 writes)
Thread 1: Calculates 5 + 1 = 6
Thread 2: Calculates 5 + 1 = 6
Thread 1: Writes stats["key1"] = 6
Thread 2: Writes stats["key1"] = 6  ← Should be 7!

Expected: 7 (5 + 2 increments)
Actual: 6 (lost update!)
```

**Solution:**

```python
import threading

stats = {}
stats_lock = threading.Lock()

def update_stats(api_key):
    with stats_lock:
        stats[api_key] = stats.get(api_key, 0) + 1  # ✅ Now safe!
```

### 5. Time-of-Check to Time-of-Use (TOCTOU)

**Problem:**

```python
# UNSAFE - Check and use in separate operations
def process_request(api_key):
    if api_key_is_available(api_key):  # Check
        use_api_key(api_key)            # Use (another thread may change state!)
```

**What happens:**

```
Thread 1: Checks if API key available → True
Thread 2: Checks if API key available → True
Thread 1: Uses API key (now rate limit = 59/60)
Thread 2: Uses API key (now rate limit = 60/60) ✅
Thread 3: Uses API key (now rate limit = 61/60) ❌ Exceeded!

Race condition: Multiple threads passed the check before any updated the state!
```

**Solution:**

```python
import threading

rate_limit_lock = threading.Lock()

def process_request(api_key):
    with rate_limit_lock:
        # Check and use are atomic together
        if api_key_is_available(api_key):
            use_api_key(api_key)
            return True
        return False
```

---

## Safe Patterns for Our Codebase

### Pattern 1: List Append (Currently Using)

**✅ Safe: No lock needed**

```python
class ApiKeyPerformanceTracker:
    """Thread-safe because list.append() is atomic in CPython."""
  
    def __init__(self):
        self._calls = []  # List for storage
  
    def record_call(self, api_key_suffix, latency_ms, success, error_msg=None):
        # Atomic operation - safe without locks!
        self._calls.append({
            "api_key": api_key_suffix,
            "latency_ms": latency_ms,
            "success": success,
            "error": error_msg if not success else None,
            "timestamp": time.time()
        })
  
    def get_all_calls(self):
        # Return copy to prevent external modification
        return self._calls.copy()
```

**Why it's safe:**

- `list.append()` is a single bytecode operation
- CPython GIL ensures it completes atomically
- No read-modify-write cycle

**Use when:**

- Recording events/logs
- Collecting metrics
- Order doesn't matter
- Aggregation happens later (not real-time)

### Pattern 2: Dictionary with Lock (For Rate Limiting)

**✅ Safe: Lock protects non-atomic operations**

```python
import threading
import time

class RateLimitTracker:
    """Thread-safe rate limiting with time-windowed counters."""
  
    def __init__(self, window_seconds=30):
        self.buckets = {}  # (bucket_ts, api_key, model) → count
        self.lock = threading.Lock()
        self.window_seconds = window_seconds
  
    def record_call(self, api_key, model):
        """Record a call with automatic time bucketing."""
        bucket_ts = int(time.time() // self.window_seconds) * self.window_seconds
        key = (bucket_ts, api_key, model)
      
        with self.lock:  # ✅ Protects dictionary update
            self.buckets[key] = self.buckets.get(key, 0) + 1
  
    def get_call_count(self, api_key, model, window_seconds=60):
        """Get total calls in the last N seconds."""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
      
        with self.lock:  # ✅ Protects dictionary read
            total = 0
            for (bucket_ts, key, mdl), count in self.buckets.items():
                if key == api_key and mdl == model and bucket_ts >= cutoff_time:
                    total += count
            return total
  
    def cleanup_old_buckets(self, max_age_seconds=3600):
        """Remove old buckets to prevent memory growth."""
        current_time = time.time()
        cutoff_time = current_time - max_age_seconds
      
        with self.lock:  # ✅ Protects dictionary modification
            # Create new dict with only recent buckets
            self.buckets = {
                k: v for k, v in self.buckets.items()
                if k[0] >= cutoff_time
            }
```

**Why it's safe:**

- Lock ensures only one thread modifies dictionary at a time
- Prevents read-modify-write race conditions
- Cleanup doesn't interfere with active recording

**Use when:**

- Need real-time counters/aggregations
- Dictionary key-value updates
- Complex state modifications

### Pattern 3: Thread-Safe Queue

**✅ Safe: Built-in thread safety**

```python
from queue import Queue
import threading

class TaskProcessor:
    """Process tasks from multiple threads safely."""
  
    def __init__(self):
        self.task_queue = Queue()  # Thread-safe queue
        self.results = []
        self.results_lock = threading.Lock()  # For results list
  
    def add_task(self, task_data):
        """Add task from any thread - safe!"""
        self.task_queue.put(task_data)  # ✅ Thread-safe put
  
    def process_tasks(self):
        """Process tasks (run in background thread)."""
        while True:
            task = self.task_queue.get()  # ✅ Thread-safe get (blocks if empty)
          
            if task is None:  # Poison pill to stop
                break
          
            result = self._process_task(task)
          
            # Results list needs lock
            with self.results_lock:
                self.results.append(result)
          
            self.task_queue.task_done()
  
    def _process_task(self, task):
        # Do work here
        return f"Processed: {task}"
```

**Use when:**

- Producer-consumer patterns
- Background task processing
- Work distribution across threads

### Pattern 4: Read-Write Lock (Optimization)

**✅ Safe: Multiple readers, single writer**

```python
import threading

class ReadWriteLock:
    """Allows multiple readers OR one writer."""
  
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(threading.Lock())
        self._write_ready = threading.Condition(threading.Lock())
  
    def acquire_read(self):
        """Acquire read lock (multiple threads can hold simultaneously)."""
        self._read_ready.acquire()
        try:
            while self._writers > 0:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._read_ready.release()
  
    def release_read(self):
        """Release read lock."""
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()
        finally:
            self._read_ready.release()
  
    def acquire_write(self):
        """Acquire write lock (exclusive access)."""
        self._write_ready.acquire()
        self._writers += 1
        self._write_ready.release()
      
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()
  
    def release_write(self):
        """Release write lock."""
        self._writers -= 1
        self._read_ready.notify_all()
        self._read_ready.release()

# Usage:
class ConfigManager:
    def __init__(self):
        self.config = {}
        self.rw_lock = ReadWriteLock()
  
    def get_config(self, key):
        """Read - multiple threads can do this simultaneously."""
        self.rw_lock.acquire_read()
        try:
            return self.config.get(key)
        finally:
            self.rw_lock.release_read()
  
    def set_config(self, key, value):
        """Write - exclusive access required."""
        self.rw_lock.acquire_write()
        try:
            self.config[key] = value
        finally:
            self.rw_lock.release_write()
```

**Use when:**

- Frequent reads, rare writes
- Performance optimization needed
- Data structure accessed often but modified rarely

---

## Real-World Examples

### Example 1: Our Current API Key Tracker (Safe)

```python
class ApiKeyPerformanceTracker:
    """Current implementation - THREAD-SAFE."""
  
    def __init__(self):
        self._calls = []  # List storage
  
    def record_call(self, api_key_suffix: str, latency_ms: float, success: bool, error_msg: str = None):
        """Record API call - safe because list.append() is atomic."""
        self._calls.append({
            "api_key": api_key_suffix,
            "latency_ms": latency_ms,
            "success": success,
            "error": error_msg if not success else None,
            "timestamp": time.time()
        })
  
    def get_all_calls(self) -> List[Dict]:
        """Get all calls - returns copy for safety."""
        return self._calls.copy()

# Global singleton - accessed from all threads
_api_key_tracker = ApiKeyPerformanceTracker()

def invoke_llm_with_fallback(messages, operation_name="LLM call", model="gemma-3-27b-it"):
    """Multiple threads call this simultaneously."""
    available_keys = get_available_api_keys()
  
    for api_key in available_keys:
        api_key_suffix = api_key[-6:]
        start_time = time.time()
      
        try:
            llm = get_llm(api_key=api_key, model=model)
            response = llm.invoke(messages)
          
            latency_ms = (time.time() - start_time) * 1000
            # ✅ Thread-safe: All threads can call this safely
            _api_key_tracker.record_call(api_key_suffix, latency_ms, True)
          
            return response
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            # ✅ Thread-safe: All threads can call this safely
            _api_key_tracker.record_call(api_key_suffix, latency_ms, False, str(e))
            continue
```

**Why it works:**

- `list.append()` is atomic
- Each thread appends independently
- No read-modify-write operations
- Export happens later in single thread

### Example 2: Rate Limiting Tracker (Needs Lock)

```python
import threading
import time
from typing import Dict, Tuple

class RateLimitTracker:
    """Rate limiting with 30-second time buckets."""
  
    def __init__(self, bucket_size=30, max_age=3600):
        self.buckets: Dict[Tuple[int, str, str], int] = {}
        self.lock = threading.Lock()
        self.bucket_size = bucket_size
        self.max_age = max_age
  
    def record_call(self, api_key: str, model: str):
        """Record a call with automatic time bucketing."""
        # Calculate time bucket
        bucket_ts = int(time.time() // self.bucket_size) * self.bucket_size
        key = (bucket_ts, api_key, model)
      
        with self.lock:  # ✅ CRITICAL: Protects dictionary update
            # This is NOT atomic without lock:
            # 1. Read current value (or 0 if missing)
            # 2. Add 1
            # 3. Write back
            self.buckets[key] = self.buckets.get(key, 0) + 1
  
    def get_recent_calls(self, api_key: str, model: str, window_seconds: int = 60) -> int:
        """Get call count in the last N seconds."""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
      
        with self.lock:  # ✅ CRITICAL: Protects dictionary read
            total = 0
            for (bucket_ts, key, mdl), count in self.buckets.items():
                if key == api_key and mdl == model and bucket_ts >= cutoff_time:
                    total += count
            return total
  
    def cleanup_old_buckets(self):
        """Remove buckets older than max_age."""
        current_time = time.time()
        cutoff_time = current_time - self.max_age
      
        with self.lock:  # ✅ CRITICAL: Protects dictionary modification
            # Create new dict with only recent buckets
            self.buckets = {
                k: v for k, v in self.buckets.items()
                if k[0] >= cutoff_time
            }
            print(f"🧹 Cleaned up old buckets, {len(self.buckets)} remaining")

# Global singleton
_rate_limiter = RateLimitTracker()

def select_best_api_key(model: str) -> str:
    """Select API key with lowest recent usage."""
    available_keys = get_available_api_keys()
  
    # Find key with lowest usage in last 60 seconds
    best_key = None
    min_usage = float('inf')
  
    for api_key in available_keys:
        # ✅ Thread-safe read
        usage = _rate_limiter.get_recent_calls(api_key[-6:], model, window_seconds=60)
      
        if usage < min_usage:
            min_usage = usage
            best_key = api_key
  
    return best_key or available_keys[0]

def invoke_llm_with_rate_limiting(messages, model="gemma-3-27b-it"):
    """Invoke LLM with intelligent API key selection."""
    # Select least-used API key
    api_key = select_best_api_key(model)
    api_key_suffix = api_key[-6:]
  
    # Record the call BEFORE making it (proactive rate limiting)
    _rate_limiter.record_call(api_key_suffix, model)
  
    # Make the call
    llm = get_llm(api_key=api_key, model=model)
    response = llm.invoke(messages)
  
    return response
```

### Example 3: Unsafe File Writing (Disaster Scenario)

```python
# ❌ UNSAFE CODE - DO NOT USE!
def export_session_count(session_id):
    """This will corrupt data under concurrent access!"""
  
    # Read current count from file
    with open("session_count.txt", "r") as f:
        count = int(f.read())
  
    # Increment it
    count += 1
  
    # Write back to file
    with open("session_count.txt", "w") as f:
        f.write(str(count))
  
    return count

# What happens with 3 concurrent requests:
# Thread 1: Read count=100
# Thread 2: Read count=100 (before Thread 1 writes)
# Thread 3: Read count=100 (before Threads 1 & 2 write)
# Thread 1: Write 101
# Thread 2: Write 101 (overwrites Thread 1!)
# Thread 3: Write 101 (overwrites Thread 2!)
# 
# Expected: 103
# Actual: 101
# Lost 2 updates! ❌
```

**Fixed version:**

```python
import threading

_file_lock = threading.Lock()

def export_session_count(session_id):
    """✅ SAFE: File operations protected by lock."""
  
    with _file_lock:  # Only ONE thread can execute this block at a time
        # Read current count from file
        with open("session_count.txt", "r") as f:
            count = int(f.read())
      
        # Increment it
        count += 1
      
        # Write back to file
        with open("session_count.txt", "w") as f:
            f.write(str(count))
      
        return count

# Now with 3 concurrent requests:
# Thread 1: Acquires lock, reads 100, writes 101, releases lock
# Thread 2: [WAITING for lock]
# Thread 3: [WAITING for lock]
# Thread 2: Acquires lock, reads 101, writes 102, releases lock
# Thread 3: [WAITING for lock]
# Thread 3: Acquires lock, reads 102, writes 103, releases lock
#
# Expected: 103
# Actual: 103
# Perfect! ✅
```

### Example 4: Excel Export (Safe with Lock)

```python
import threading
from pathlib import Path
from datetime import datetime

_export_lock = threading.Lock()

def export_api_key_metrics_to_excel(output_dir="load_tests/reports"):
    """✅ SAFE: Export protected by lock to prevent concurrent writes."""
  
    with _export_lock:  # Only ONE export at a time
        # Get all calls (this is safe - returns a copy)
        all_calls = _api_key_tracker.get_all_calls()
      
        if not all_calls:
            print("⚠️ No API key metrics to export")
            return None
      
        # Aggregate data
        aggregated = defaultdict(lambda: {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "latencies_ms": [],
            "errors": []
        })
      
        for call in all_calls:
            key = call["api_key"]
            aggregated[key]["total_calls"] += 1
          
            if call["success"]:
                aggregated[key]["successful_calls"] += 1
                aggregated[key]["latencies_ms"].append(call["latency_ms"])
            else:
                aggregated[key]["failed_calls"] += 1
                if call["error"]:
                    aggregated[key]["errors"].append(call["error"])
      
        # Create DataFrame
        import pandas as pd
        rows = []
        for api_key, data in aggregated.items():
            rows.append({
                "API Key": f"...{api_key}",
                "Total Calls": data["total_calls"],
                "Successful": data["successful_calls"],
                "Failed": data["failed_calls"],
                # ... more columns
            })
      
        df = pd.DataFrame(rows)
      
        # Save to Excel (protected by lock)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"api_key_performance_{timestamp}.xlsx"
        filepath = Path(output_dir) / filename
      
        df.to_excel(filepath, index=False, engine='openpyxl')
      
        print(f"📊 Exported to: {filepath}")
        return str(filepath)

# Even if multiple threads call this simultaneously:
# Thread 1: Acquires lock, exports data, releases lock
# Thread 2: [WAITING] Can't start export until Thread 1 finishes
# Thread 3: [WAITING] Can't start export until Thread 2 finishes
#
# Each export completes fully before next one starts ✅
```

---

## Quick Reference: Thread Safety Checklist

### ✅ These Operations Are Thread-Safe (No Lock Needed)

```python
# List operations
my_list.append(item)               # ✅ Atomic
my_list.extend([item1, item2])     # ✅ Atomic
item = my_list[0]                  # ✅ Simple read

# Simple assignments
x = y                              # ✅ Atomic
my_dict[key] = value               # ✅ Atomic (if key exists)
value = my_dict.get(key)           # ✅ Simple read

# Built-in thread-safe structures
from queue import Queue
q = Queue()
q.put(item)                        # ✅ Thread-safe
item = q.get()                     # ✅ Thread-safe

from collections import deque
d = deque()
d.append(item)                     # ✅ Thread-safe
d.popleft()                        # ✅ Thread-safe
```

### ❌ These Operations Are NOT Thread-Safe (Need Lock!)

```python
# Dictionary updates
my_dict[key] += 1                  # ❌ Read + modify + write
my_dict[key] = my_dict.get(key, 0) + 1  # ❌ Not atomic
if key not in my_dict:             # ❌ Check-then-act
    my_dict[key] = 0

# Numeric operations on shared state
counter += 1                       # ❌ Read + modify + write
x = x + 1                          # ❌ Not atomic

# File operations
with open(file, "w") as f:         # ❌ Multiple threads can corrupt
    f.write(data)

# Complex list operations
my_list.sort()                     # ❌ Modifies in place
my_list.remove(item)               # ❌ Search + modify
my_list.insert(0, item)            # ❌ Shift + insert
```

### 🔒 When to Use Locks

**Use `threading.Lock()` when:**

1. Modifying dictionaries (except simple `dict[key] = value`)
2. Read-modify-write operations (`x += 1`, `dict[key] += 1`)
3. File I/O (reading or writing files)
4. Multiple operations that must be atomic together
5. Check-then-act patterns (`if condition: do_something()`)

**Example:**

```python
import threading

# Create lock
my_lock = threading.Lock()

# Use lock
with my_lock:  # Acquires lock
    # Only ONE thread can execute this code at a time
    my_dict[key] += 1
    # Lock automatically released when block exits
```

---

## Debugging Thread Safety Issues

### Signs of Thread Safety Problems

1. **Intermittent bugs** - work sometimes, fail other times
2. **Bugs under load** - work with 1 user, fail with many
3. **Data corruption** - counters wrong, files garbled
4. **Lost updates** - operations seem to disappear
5. **Deadlocks** - application hangs/freezes

### Debugging Techniques

#### 1. Add Thread Logging

```python
import threading
import time

def record_call(self, api_key):
    thread_id = threading.current_thread().name
    print(f"[{thread_id}] Recording call for {api_key} at {time.time()}")
  
    self.counts[api_key] = self.counts.get(api_key, 0) + 1
  
    print(f"[{thread_id}] Count for {api_key}: {self.counts[api_key]}")
```

#### 2. Use Thread Sanitizers

```python
# Install: pip install threading-sanitizer
import threading_sanitizer

threading_sanitizer.enable()

# Your code here
# Will detect race conditions and report them
```

#### 3. Stress Testing

```python
import threading

def stress_test():
    """Hammer the function from multiple threads."""
    threads = []
  
    for i in range(100):  # 100 concurrent threads
        t = threading.Thread(target=record_call, args=("test_key",))
        threads.append(t)
        t.start()
  
    for t in threads:
        t.join()
  
    # Check if count is correct
    expected = 100
    actual = counts.get("test_key", 0)
  
    if actual != expected:
        print(f"❌ Race condition detected! Expected {expected}, got {actual}")
    else:
        print(f"✅ Thread-safe! Got expected count: {actual}")
```

#### 4. Lock Contention Analysis

```python
import threading
import time

class MonitoredLock:
    """Lock that tracks contention."""
  
    def __init__(self):
        self.lock = threading.Lock()
        self.wait_times = []
        self.lock_times = []
  
    def __enter__(self):
        start_wait = time.time()
        self.lock.acquire()
        wait_time = time.time() - start_wait
        self.wait_times.append(wait_time)
        self.acquire_time = time.time()
        return self
  
    def __exit__(self, *args):
        hold_time = time.time() - self.acquire_time
        self.lock_times.append(hold_time)
        self.lock.release()
  
    def stats(self):
        """Print lock contention statistics."""
        if self.wait_times:
            avg_wait = sum(self.wait_times) / len(self.wait_times)
            max_wait = max(self.wait_times)
            print(f"Lock contention - Avg wait: {avg_wait*1000:.2f}ms, Max wait: {max_wait*1000:.2f}ms")
      
        if self.lock_times:
            avg_hold = sum(self.lock_times) / len(self.lock_times)
            max_hold = max(self.lock_times)
            print(f"Lock hold time - Avg: {avg_hold*1000:.2f}ms, Max: {max_hold*1000:.2f}ms")
```

---

## Best Practices Summary

### DO ✅

1. **Use atomic operations when possible**

   - `list.append()` instead of complex list operations
   - Simple assignments instead of read-modify-write
2. **Use locks for non-atomic operations**

   - Dictionary updates: `with lock: dict[key] += 1`
   - File I/O: `with lock: file.write(data)`
3. **Keep lock scopes small**

   ```python
   # ✅ Good: Lock only critical section
   data = prepare_data()  # Outside lock
   with lock:
       shared_dict[key] = data

   # ❌ Bad: Lock too much
   with lock:
       data = slow_computation()  # Don't lock during slow work!
       shared_dict[key] = data
   ```
4. **Use thread-safe data structures**

   - `queue.Queue` for producer-consumer
   - `collections.deque` for append/pop operations
5. **Document thread safety**

   ```python
   class MyClass:
       """Thread-safe tracker using atomic list operations."""
       # Clear documentation helps maintainers
   ```
6. **Test under load**

   - Run load tests with Locust
   - Monitor for race conditions
   - Check data integrity

### DON'T ❌

1. **Don't assume single-threaded execution**

   - Even 1 uvicorn worker uses 40 threads!
2. **Don't use global state without protection**

   ```python
   # ❌ Bad
   counter = 0
   def increment():
       global counter
       counter += 1  # Race condition!

   # ✅ Good
   counter = 0
   counter_lock = threading.Lock()
   def increment():
       global counter
       with counter_lock:
           counter += 1
   ```
3. **Don't hold locks during I/O**

   ```python
   # ❌ Bad: Holding lock during slow I/O
   with lock:
       data = expensive_api_call()  # Other threads blocked!
       shared_dict[key] = data

   # ✅ Good: Only lock for critical section
   data = expensive_api_call()  # No lock held
   with lock:
       shared_dict[key] = data  # Quick operation
   ```
4. **Don't nest locks (can cause deadlocks)**

   ```python
   # ❌ Dangerous: Nested locks can deadlock
   with lock_a:
       with lock_b:
           # If another thread acquires in reverse order, deadlock!
           pass
   ```
5. **Don't share state across Gunicorn workers**

   - Each process has separate memory
   - Use Redis/database for shared state

---

## Conclusion

Thread safety is critical for production FastAPI applications because:

1. **FastAPI uses thread pools** - Even 1 worker = 40 concurrent threads
2. **Shared global state** - All threads access same variables
3. **Non-atomic operations** - Many Python operations aren't thread-safe
4. **Subtle bugs** - Race conditions are hard to detect and reproduce

**Key Takeaways:**

- ✅ Use `list.append()` for simple event logging (atomic, thread-safe)
- 🔒 Use `threading.Lock()` for dictionary updates and file I/O
- 📊 Test under load to catch race conditions early
- 📚 Document thread safety assumptions
- 🚀 For production with high traffic, consider Gunicorn + Uvicorn workers

**Our Current Setup (Safe):**

```python
# ✅ Thread-safe API key tracker
_api_key_tracker = ApiKeyPerformanceTracker()  # Uses list.append()

# 🔒 Future rate limiter needs locks
_rate_limiter = RateLimitTracker()  # Uses dict with threading.Lock()
```

Remember: **When in doubt, use a lock!** The small performance cost is worth the correctness guarantee.

---

## Additional Resources

- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [FastAPI Concurrency Guide](https://fastapi.tiangolo.com/async/)
- [Real Python: Threading in Python](https://realpython.com/intro-to-python-threading/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

**Document Version:** 1.0
**Last Updated:** December 22, 2025
**Tested With:** FastAPI, Uvicorn, Python 3.10+
