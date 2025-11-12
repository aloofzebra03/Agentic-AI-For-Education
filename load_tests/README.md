# Load Testing for Educational Agent API

## 📋 Overview

This directory contains load testing infrastructure for the Educational Agent API using **Locust**, a Python-based load testing framework.

**What it does:**
- Simulates real students interacting with the agent API
- Tests concurrent user handling (10 → 100 → 1,000 → 10,000 users)
- Measures response times, throughput, and error rates
- Tracks custom metrics (node transitions, checkpoint operations)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_load_test.txt
```

### 2. Start Your API Server

Make sure your FastAPI server is running:

```bash
cd ..
python -m uvicorn api_servers.api_server:app --host 0.0.0.0 --port 8000
```

### 3. Run a Basic Load Test

**Option A: With Web UI (Recommended for first-time users)**

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Then open your browser to: **http://localhost:8089**

You'll see a web interface where you can:
- Set number of users (e.g., 10)
- Set spawn rate (e.g., 1 user/second)
- Start the test and watch real-time graphs

**Option B: Headless (for automated testing)**

```bash
locust -f locustfile.py --host=http://localhost:8000 --users=10 --spawn-rate=1 --run-time=5m --headless
```

---

## 📊 Test Scenarios

### Baseline Test (10 users)
**Purpose:** Measure cold start and baseline node latencies

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users=10 \
  --spawn-rate=1 \
  --run-time=5m \
  --headless \
  --html=reports/report_baseline.html
```

**Expected Results:**
- ✅ All requests succeed (0% error rate)
- ✅ Avg latency < 2s
- ✅ Checkpoint save time < 200ms

---

### Light Load (100 users)
**Purpose:** Test DB write stress and connection pooling

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=10m \
  --headless \
  --html=reports/report_light.html
```

**Expected Results:**
- ✅ Error rate < 0.1%
- ✅ P95 latency < 5s
- ✅ DB connection pool < 80% utilized

---

### Medium Load (1,000 users)
**Purpose:** Identify LLM call queue delays and scaling issues

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users=1000 \
  --spawn-rate=50 \
  --run-time=15m \
  --headless \
  --html=reports/report_medium.html
```

**Expected Results:**
- ⚠️ Some LLM queueing expected
- ✅ Error rate < 1%
- ✅ P95 latency < 10s

---

### Stress Test (10,000 users)
**Purpose:** Find breaking point and identify bottlenecks

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users=10000 \
  --spawn-rate=100 \
  --run-time=20m \
  --headless \
  --html=reports/report_stress.html
```

**Expected Results:**
- ⚠️ Expect failures - goal is to identify what breaks first
- 📊 Measure: DB? LLM API? Memory? Network?
- 🎯 Target: 95% of requests succeed

---

## 📁 Project Structure

```
load_tests/
├── locustfile.py              # Main test definition
├── config.py                  # Test configuration
├── requirements_load_test.txt # Dependencies
├── README.md                  # This file
├── tasks/
│   ├── __init__.py
│   └── session_tasks.py       # Session flow tasks
├── utils/
│   ├── __init__.py
│   ├── response_generator.py  # Generate realistic responses
│   └── metrics_collector.py   # Custom metrics
└── reports/                   # Generated HTML reports
    └── (reports go here)
```

---

## 📈 What Gets Measured

### Locust Built-in Metrics
- ✅ **Request latency** (avg, min, max, p50, p95, p99)
- ✅ **Throughput** (requests per second)
- ✅ **Error rates** (4xx, 5xx, timeouts)
- ✅ **Response time distribution**

### Custom Metrics (our additions)
- ✅ **Node transition latencies** (APK → CI → GE, etc.)
- ✅ **Checkpoint operations** (save/load time)
- ✅ **State-specific metrics** (simulation triggers, images loaded)

---

## 🎯 How It Works

### User Simulation Flow

Each simulated "student" follows this pattern:

1. **Start Session** (`POST /session/start`)
   - Get `thread_id`
   - Receive initial agent message

2. **Conversation Loop** (5-10 turns)
   - `POST /session/continue` with realistic responses
   - Responses vary based on current pedagogical node:
     - **APK**: Prior knowledge questions
     - **CI**: Echo definition
     - **GE**: Guided exploration responses
     - **AR**: Questions (80% correct, 20% incorrect)
     - **TC**: Transfer context examples
     - **RLC**: Quiz responses

3. **Occasional Status Checks** (10% of the time)
   - `GET /session/status/{thread_id}`

4. **Think Time** (1-3 seconds between requests)
   - Simulates realistic user behavior

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Change base URL
BASE_URL = "http://your-server:8000"

# Adjust think time
MIN_WAIT_TIME = 1  # seconds
MAX_WAIT_TIME = 3  # seconds

# Request timeout (for slow LLM calls)
REQUEST_TIMEOUT = 60  # seconds

# Disable LangSmith tracing during high load
ENABLE_LANGSMITH_TRACING = False
```

---

## 📊 Reading Results

### Web UI (Live)
Open http://localhost:8089 during test to see:
- Real-time RPS (requests per second)
- Live error rate graph
- Response time distribution
- Request breakdown by endpoint

### HTML Report (After Test)
Generated reports include:
- Summary statistics
- Response time graphs
- Failure breakdown
- Download percentiles data

### Console Output
Look for:
- ✅ **Green checkmarks** = passed thresholds
- ❌ **Red X's** = failed thresholds
- 📊 **Custom metrics summary** at end

---

## 🐛 Troubleshooting

### "Connection refused"
❌ **Problem:** API server not running
✅ **Solution:** Start FastAPI server first

```bash
cd ..
python -m uvicorn api_servers.api_server:app --host 0.0.0.0 --port 8000
```

### "Session not found" errors
❌ **Problem:** Sessions being deleted or PostgreSQL issues
✅ **Solution:** 
- Check PostgreSQL connection in `graph.py`
- Ensure checkpoint tables exist (`checkpointer.setup()`)

### High error rates at low user counts
❌ **Problem:** Agent or LLM API issue
✅ **Solution:**
1. Run a single manual test via `/docs` endpoint
2. Check LangSmith traces for errors
3. Verify Groq API key and quotas

### Timeouts after 60 seconds
❌ **Problem:** LLM calls taking too long
✅ **Solution:**
- Increase `REQUEST_TIMEOUT` in `config.py`
- Check LLM provider status (Groq/OpenAI)
- Consider using faster models

---

## 🚀 Next Steps

### Phase 1: Local Testing (Current)
- [x] Install Locust
- [x] Run baseline test (10 users)
- [ ] Run light load test (100 users)
- [ ] Run medium load test (1,000 users)
- [ ] Identify and fix bottlenecks

### Phase 2: Optimization
- [ ] Add connection pooling (if needed)
- [ ] Implement caching for common responses
- [ ] Optimize checkpoint serialization
- [ ] Add rate limiting

### Phase 3: AWS Testing
- [ ] Deploy API to AWS (ECS/EC2)
- [ ] Setup AWS RDS PostgreSQL
- [ ] Configure CloudWatch monitoring
- [ ] Run distributed Locust tests (10,000+ users)

---

## 📚 Additional Resources

- **Locust Documentation:** https://docs.locust.io/
- **LangGraph Checkpointing:** https://langchain-ai.github.io/langgraph/concepts/persistence/
- **Performance Thresholds:** See `config.py` → `PERFORMANCE_THRESHOLDS`

---

## 💡 Tips

1. **Start Small:** Always run 10-user test first to verify everything works
2. **Monitor Resources:** Use Task Manager (Windows) or `htop` (Linux) to watch CPU/memory
3. **Save Reports:** Use `--html` flag to save reports for comparison
4. **Iterate:** Fix bottlenecks between test runs
5. **Use LangSmith:** Re-enable tracing for deep-dive debugging after identifying issues

---

**Happy Load Testing! 🚀**
