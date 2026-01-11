"""
Streamlit PostMessage Receiver - Study Example
==============================================

This file demonstrates different approaches to receive postMessage
events from an iframe in Streamlit.

IMPORTANT: Standard Streamlit doesn't natively support receiving postMessage.
We need workarounds or custom components.

Run with: streamlit run 03_streamlit_receiver.py
"""

import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="PostMessage Receiver Study", layout="wide")

st.title("📨 Receiving PostMessage in Streamlit")

st.markdown("""
## The Challenge

Streamlit runs Python on the server, but `postMessage` is a browser-side JavaScript API.
We need a bridge between the browser (where the iframe sends messages) and Python (where Streamlit runs).

Below are different approaches to solve this:
""")

# =============================================================================
# APPROACH 1: Using streamlit-javascript (Simple but Limited)
# =============================================================================

st.header("Approach 1: streamlit-javascript")

st.markdown("""
**Install:** `pip install streamlit-javascript`

This package lets you run JavaScript in the browser and return results to Python.

**Limitation:** It's synchronous - you can't continuously listen for events.
""")

st.code("""
from streamlit_javascript import st_javascript

# This runs JS in the browser and waits for a result
result = st_javascript('''
    // This is a one-time execution, not a listener
    // Limited usefulness for continuous event listening
    "Hello from JavaScript!"
''')
st.write(f"JavaScript returned: {result}")
""", language="python")

# Try it (if installed)
try:
    from streamlit_javascript import st_javascript
    
    if st.button("Run JavaScript (One-time)"):
        result = st_javascript('"Hello from JS at " + new Date().toLocaleTimeString()')
        st.success(f"JavaScript returned: {result}")
except ImportError:
    st.warning("Install with: `pip install streamlit-javascript`")

# =============================================================================
# APPROACH 2: Using streamlit-js-eval (Better for Complex JS)
# =============================================================================

st.header("Approach 2: streamlit-js-eval")

st.markdown("""
**Install:** `pip install streamlit-js-eval`

More powerful - supports Promises, can wait for events (with timeout).

**Limitation:** Still not truly real-time, each call is a new execution context.
""")

st.code("""
from streamlit_js_eval import streamlit_js_eval

# Wait for a postMessage event (with timeout)
result = streamlit_js_eval(js_expressions='''
    new Promise((resolve) => {
        const handler = (event) => {
            if (event.data && event.data.type === 'SIMULATION_PARAM_CHANGE') {
                window.removeEventListener('message', handler);
                resolve(JSON.stringify(event.data));
            }
        };
        window.addEventListener('message', handler);
        
        // Timeout after 30 seconds
        setTimeout(() => {
            window.removeEventListener('message', handler);
            resolve(null);
        }, 30000);
    });
''')

if result:
    data = json.loads(result)
    st.write("Received:", data)
""", language="python")

# =============================================================================
# APPROACH 3: Custom Streamlit Component (Recommended)
# =============================================================================

st.header("Approach 3: Custom Streamlit Component (Recommended)")

st.markdown("""
**The proper solution** - create a custom Streamlit component that:
1. Renders in the browser (can listen for events)
2. Communicates back to Python via Streamlit's component API

**Structure:**
```
components/
└── simulation_bridge/
    ├── __init__.py           # Python interface
    ├── frontend/
    │   ├── index.html        # Component HTML
    │   └── main.js           # Event listener logic
    └── setup.py              # Package setup
```

See `study/04_custom_component/` for a complete example.
""")

# =============================================================================
# APPROACH 4: Polling with Session State
# =============================================================================

st.header("Approach 4: Polling with Auto-Refresh")

st.markdown("""
**Install:** `pip install streamlit-autorefresh`

Simple approach: store messages in browser storage, poll from Streamlit.

**Limitation:** 
- Not real-time (polling delay)
- Only works if simulation is same-origin (can share localStorage)
- Your simulation is on GitHub Pages (different origin) - won't work directly
""")

st.code("""
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 2 seconds
count = st_autorefresh(interval=2000, key="datarefresh")

# In same-origin scenario, you could read localStorage:
# result = st_javascript('localStorage.getItem("simulation_params")')
""", language="python")

# =============================================================================
# APPROACH 5: WebSocket Bridge (Most Powerful)
# =============================================================================

st.header("Approach 5: WebSocket Bridge")

st.markdown("""
**Architecture:**
```
Simulation (Browser) ──WebSocket──> Server <──HTTP Poll── Streamlit
```

**Components needed:**
1. WebSocket server (FastAPI, Flask-SocketIO, etc.)
2. Simulation connects via WebSocket
3. Streamlit polls server for updates

**Pros:** Real-time, works cross-origin, scalable
**Cons:** More infrastructure, more complex

See `study/05_websocket_bridge/` for example implementation.
""")

# =============================================================================
# APPROACH 6: Embedded HTML Component with Callbacks
# =============================================================================

st.header("Approach 6: st.components.v1.html with Callbacks")

st.markdown("""
Using `st.components.v1.html()` we can embed custom HTML/JS that communicates
back to Streamlit via the Streamlit component communication protocol.

This is a lightweight version of a custom component.
""")

# Example embedded component
component_code = """
<div id="message-display" style="padding: 20px; background: #f0f0f0; border-radius: 8px;">
    <h3>📡 PostMessage Listener</h3>
    <p>Waiting for messages from simulation...</p>
    <div id="log" style="font-family: monospace; max-height: 200px; overflow-y: auto;"></div>
</div>

<script>
    const logEl = document.getElementById('log');
    const displayEl = document.getElementById('message-display');
    
    window.addEventListener('message', function(event) {
        // Log all messages for debugging
        const entry = document.createElement('div');
        entry.style.borderBottom = '1px solid #ddd';
        entry.style.padding = '5px';
        entry.innerHTML = '<strong>' + new Date().toLocaleTimeString() + '</strong>: ' + 
                          JSON.stringify(event.data).substring(0, 100);
        logEl.appendChild(entry);
        
        // Check if it's a simulation param change
        if (event.data && event.data.type === 'SIMULATION_PARAM_CHANGE') {
            displayEl.style.background = '#e8f5e9';  // Green tint
            
            // Here we would send to Streamlit...
            // But st.components.v1.html doesn't support bidirectional communication
            // This is why we need a proper custom component
        }
    });
    
    // For demo: send a test message after 2 seconds
    setTimeout(() => {
        window.postMessage({
            type: 'SIMULATION_PARAM_CHANGE',
            param: 'length',
            oldValue: 5,
            newValue: 8
        }, '*');
    }, 2000);
</script>
"""

st.markdown("**Live Demo** (self-contained, sends test message after 2 seconds):")
st.components.v1.html(component_code, height=300)

st.warning("""
⚠️ **Limitation**: `st.components.v1.html()` is one-way only (Python → Browser).
It cannot send data back to Python. For bidirectional communication, you need
a proper custom Streamlit component.
""")

# =============================================================================
# SUMMARY & RECOMMENDATION
# =============================================================================

st.header("📊 Summary & Recommendation")

comparison_data = """
| Approach | Real-time | Cross-Origin | Complexity | Best For |
|----------|-----------|--------------|------------|----------|
| streamlit-javascript | ❌ | ✅ | Low | One-time JS execution |
| streamlit-js-eval | ⚠️ | ✅ | Low | Waiting for single event |
| Custom Component | ✅ | ✅ | Medium | **Production use** |
| Polling + localStorage | ❌ | ❌ | Low | Same-origin only |
| WebSocket Bridge | ✅ | ✅ | High | Complex real-time apps |
| st.components.html | ❌ | N/A | Low | Display only, no callback |
"""

st.markdown(comparison_data)

st.success("""
**🎯 Recommendation for Your Project:**

**Custom Streamlit Component** is the best approach because:
1. Your simulation is on GitHub Pages (cross-origin) - postMessage works
2. You need real-time detection of student interactions
3. It integrates cleanly with your existing Streamlit app
4. You have full control over the communication protocol

See `study/04_custom_component/` for a working implementation!
""")

# =============================================================================
# NEXT STEPS
# =============================================================================

st.header("🚀 Next Steps")

st.markdown("""
1. **Study the custom component example** in `study/04_custom_component/`
2. **Modify your simulation** to include the sender script from `02_simulation_sender.js`
3. **Test locally** with the custom component
4. **Integrate with your teaching agent** to respond to student exploration
5. **Consider the teaching flow:**
   - Student explores → Simulation notifies → Agent acknowledges → Teaching adapts
""")
