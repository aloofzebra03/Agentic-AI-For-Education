# How to Verify Load Test Reports

## ✅ Verification Checklist

After running a load test, verify that the reports are generated correctly:

### 1. Check Report Files Exist

In the `load_tests/reports/` directory, you should see 4 files:
```
report_10users_YYYYMMDD_HHMMSS.json           # Complete metrics in JSON
report_10users_YYYYMMDD_HHMMSS_stats.csv      # Request statistics for Excel
report_10users_YYYYMMDD_HHMMSS_custom.txt     # LangGraph-specific metrics
report_10users_YYYYMMDD_HHMMSS_summary.txt    # Human-readable summary
```

**Verify:** The filename shows the CORRECT user count (e.g., `10users`, not `0users`)

---

## 2. Verify CSV Report (RPS Values)

Open `report_*_stats.csv` in Excel or a text editor.

### Expected Format:
```csv
Endpoint,Method,Requests,Failures,Failure Rate (%),Avg (ms),Min (ms),Max (ms),Median (ms),RPS,P95 (ms),P99 (ms)
/session/start,POST,10,2,20.00,3519.00,3211.00,4481.00,3211.00,0.08,4500.00,4500.00
/session/continue,POST,190,170,89.47,2535.00,1464.00,4109.00,2500.00,1.61,3100.00,4100.00
/session/status/{thread_id},GET,21,0,0.00,65.00,27.00,437.00,50.00,0.18,170.00,290.00

Aggregated,ALL,221,172,77.83,2345.29,27.94,4481.39,2600.00,1.87,3300.00,4100.00
```

### ✅ What to Check:

#### RPS Column (Position 10):
The RPS values should be **SMALL NUMBERS** (typically 0.01 to 100):

| Endpoint | Expected RPS | What It Means |
|----------|--------------|---------------|
| `/session/start` | 0.05 - 0.15 | Slow (3+ seconds per request) |
| `/session/continue` | 0.5 - 5.0 | Medium (2-3 seconds per request) |
| `/session/status` | 1.0 - 10.0 | Fast (<1 second per request) |
| **Aggregated** | 1.0 - 10.0 | **Total throughput** |

#### ❌ Common Issues:

**Problem:** RPS shows large numbers like 3211.83, 2500.00
```csv
/session/start,POST,10,2,20.00,3519.00,3211.00,4481.00,3211.00,3211.83,4500.00,4500.00
                                                                    ^^^^^^^^ WRONG!
```
**Reason:** Response time leaked into RPS column
**Fix:** Run test again after the code fix

**Problem:** All RPS values are 0.00
```csv
/session/start,POST,10,2,20.00,3519.00,3211.00,4481.00,3211.00,0.00,4500.00,4500.00
```
**Reason:** Test duration was too short or test crashed before recording
**Fix:** Run longer test (--run-time=2m minimum)

---

## 3. Verify JSON Report (RPS Values)

Open `report_*_users_*.json` in a text editor or VS Code.

### Check Overall RPS:
```json
{
  "request_stats": {
    "requests_per_second": 1.87,  // ✅ Should be > 0
    "total_requests": 221,
    "total_failures": 172
  }
}
```

### Check Per-Endpoint RPS:
```json
{
  "endpoint_stats": {
    "POST /session/start": {
      "requests_per_second": 0.08,  // ✅ Should be small (0.05-0.15)
      "num_requests": 10,
      "avg_response_time_ms": 3519.00
    },
    "POST /session/continue": {
      "requests_per_second": 1.61,  // ✅ Should match CSV
      "num_requests": 190
    }
  }
}
```

### ✅ Validation Formula:
Manually calculate RPS to verify:
```
RPS = num_requests / duration_seconds

Example:
- Requests: 10
- Duration: 118 seconds
- Expected RPS = 10 / 118 = 0.08 ✅ CORRECT
```

---

## 4. Verify Summary Report

Open `report_*_summary.txt` to see human-readable stats:

```
📊 OVERALL PERFORMANCE:
Total Requests: 221
Requests per Second: 1.87  ✅ Should match JSON

⏱️  RESPONSE TIMES:
Average: 2345.29ms
P95: 3300.00ms
```

---

## 5. Quick Validation Commands

### Check if reports exist:
```powershell
dir load_tests/reports/report_*users_*.* | Select-Object Name, Length, LastWriteTime
```

### Count report files:
```powershell
(dir load_tests/reports/report_*users_*.*).Count  # Should be 4 per test run
```

### View CSV in terminal:
```powershell
Get-Content load_tests/reports/report_*_stats.csv | Select-Object -First 10
```

### Extract RPS values from CSV:
```powershell
Import-Csv load_tests/reports/report_10users_*_stats.csv | Select-Object Endpoint, RPS
```

---

## 6. Troubleshooting

### Issue: RPS values look like response times (e.g., 3211.83)
**Cause:** Bug in old code where `endpoint_stats.total_rps` was incorrect
**Fix:** Code has been updated to calculate RPS manually
**Action:** Delete old reports and re-run test

### Issue: All RPS values are 0
**Cause:** Test ran for <1 second or crashed
**Fix:** Run longer test: `--run-time=2m`

### Issue: Aggregated RPS ≠ Sum of endpoint RPS
**Expected:** This is NORMAL because:
- Users have wait times (1-3 seconds) between requests
- Some requests overlap
- Failures consume time without throughput

---

## 7. Expected Values for Your Test

### 10 Users, 2 Minutes, Current Performance:

| Metric | Expected Range | Your Current | Status |
|--------|----------------|--------------|--------|
| Total Requests | 150-300 | 221 | ✅ Normal |
| Aggregated RPS | 1.0-5.0 | 1.87 | ✅ Expected |
| `/session/start` RPS | 0.05-0.15 | 0.08 | ✅ Expected |
| `/session/continue` RPS | 0.5-3.0 | 1.61 | ✅ Expected |
| Failure Rate | <5% | 77% | ❌ **FIX REQUIRED** |

**Priority:** Fix the 77% failure rate first - this is killing your RPS!

---

## 8. How to Improve RPS

Once reports are verified and failure rate is reduced:

1. **Fix API errors** → Reduce failure rate from 77% to <5%
2. **Optimize LLM calls** → Reduce avg response time from 2.3s to <1.5s
3. **Scale users** → Increase from 10 to 100 users
4. **Remove wait times** (for pure throughput): Set `MIN_WAIT_TIME=0, MAX_WAIT_TIME=0`

**Target RPS after fixes:**
- 10 users: 3-5 RPS
- 100 users: 20-50 RPS
- 1000 users: 100+ RPS

---

## Summary

**After every test run:**
1. ✅ Check 4 report files exist in `load_tests/reports/`
2. ✅ Open CSV and verify RPS column has small values (0.08, 1.61, etc.)
3. ✅ Open JSON and verify `requests_per_second` matches expectations
4. ✅ Manually calculate: RPS = requests / duration
5. ✅ If RPS looks wrong (too high or equals response time), re-run test

**RPS should always be:**
- Smaller than 1000 for your use case
- Between 0.01 and 10 for individual endpoints
- Match the formula: num_requests / test_duration
