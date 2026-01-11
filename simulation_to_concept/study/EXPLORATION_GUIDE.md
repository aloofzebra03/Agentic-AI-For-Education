# Exploring Bi-Directional Communication: Simulation ↔ Streamlit

## The Challenge

Currently, communication is **one-way**:
```
Streamlit App → (URL parameters) → Simulation iframe
```

What we want is **two-way** communication:
```
Streamlit App ↔ Simulation iframe
```

When a student interacts with the simulation directly (e.g., dragging a slider to change pendulum length), we want the Streamlit app (and thus the teaching agent) to know about it.

---

## ✅ Study Materials Created

| File | Description | Status |
|------|-------------|--------|
| [01_postmessage_basics.html](01_postmessage_basics.html) | Interactive HTML demo of postMessage API | ✅ |
| [02_simulation_sender.js](02_simulation_sender.js) | JavaScript module to add to simulations | ✅ |
| [03_streamlit_receiver.py](03_streamlit_receiver.py) | 6 approaches to receive postMessage in Streamlit | ✅ |
| **04_custom_component/** | **Full working custom component (RECOMMENDED)** | ✅ |
| └── simulation_bridge.py | Python interface for the component | ✅ |
| └── frontend/index.html | Component UI + JS logic | ✅ |
| └── integration_example.py | Shows how to integrate with your agent | ✅ |

**Recommended Path:** Start with `04_custom_component/` - it's a complete working solution!

---

## Approaches to Explore

### 1. **PostMessage API** (Recommended)
The standard web API for cross-origin/cross-frame communication.

**How it works:**
- Simulation sends messages to parent window using `window.parent.postMessage()`
- Parent listens for messages using `window.addEventListener('message', ...)`

**Pros:**
- Standard web API, well-supported
- Works cross-origin
- Real-time communication

**Cons:**
- Requires modifying the simulation HTML
- Streamlit doesn't natively support receiving postMessage (needs custom component)

---

### 2. **Streamlit Custom Component**
Build a custom Streamlit component that wraps the iframe and handles bi-directional communication.

**How it works:**
- Create a React/JS component that embeds the simulation
- Component listens for postMessage from simulation
- Component sends data back to Python using Streamlit's component API

**Pros:**
- Full control over communication
- Integrates cleanly with Streamlit
- Can handle complex interactions

**Cons:**
- More complex to implement
- Requires JavaScript/React knowledge

---

### 3. **URL Fragment Polling**
The simulation updates the URL hash with current parameters, and Streamlit polls for changes.

**How it works:**
- Simulation updates: `#length=8&oscillations=10`
- Parent periodically checks iframe URL

**Pros:**
- Simple to implement
- No complex setup

**Cons:**
- Not real-time (polling delay)
- Can't read cross-origin iframe URLs (security restriction)
- Only works if simulation is same-origin

---

### 4. **WebSocket / Server-Side Events**
Both simulation and Streamlit connect to a shared WebSocket server.

**How it works:**
- Run a WebSocket server (e.g., FastAPI with WebSockets)
- Simulation connects and sends parameter changes
- Streamlit connects and receives updates

**Pros:**
- Real-time
- Works across origins
- Can support multiple clients

**Cons:**
- Additional infrastructure (WebSocket server)
- More complex architecture

---

### 5. **Shared Backend State (REST API)**
Simulation posts changes to a backend, Streamlit polls the backend.

**How it works:**
- Simulation: `POST /api/params {length: 8}`
- Streamlit: `GET /api/params` (polling)

**Pros:**
- Simple REST API
- Stateless communication

**Cons:**
- Not real-time
- Requires backend infrastructure

---

### 6. **LocalStorage / SessionStorage**
If simulation and app are same-origin, they can share browser storage.

**How it works:**
- Simulation writes: `localStorage.setItem('params', JSON.stringify({...}))`
- Parent reads: `localStorage.getItem('params')`

**Pros:**
- Very simple
- Persistent storage

**Cons:**
- **Only works if same origin** (your simulation is on GitHub Pages, different origin)
- Not real-time (needs polling)

---

## Recommendation: PostMessage + Custom Streamlit Component

For your use case, I recommend **Approach 1 + 2**: Using PostMessage API with a custom Streamlit component.

### Why?
1. **PostMessage** is the standard way for iframe communication
2. **Custom component** gives you full control in Streamlit
3. **Works cross-origin** (GitHub Pages simulation → localhost Streamlit)
4. **Real-time** - no polling needed

---

## Implementation Plan

### Step 1: Modify Simulation HTML to Send Messages

Add JavaScript to your simulation that broadcasts parameter changes:

```javascript
// In your simulation HTML/JS
function notifyParentOfParamChange(params) {
    // Send message to parent window
    window.parent.postMessage({
        type: 'SIMULATION_PARAM_CHANGE',
        params: params,
        timestamp: Date.now()
    }, '*');  // '*' allows any origin, or specify your Streamlit URL
}

// Call this whenever a parameter changes
// Example: when user drags a slider
lengthSlider.addEventListener('change', function(e) {
    notifyParentOfParamChange({
        length: e.target.value,
        number_of_oscillations: getCurrentOscillations()
    });
});
```

### Step 2: Create Custom Streamlit Component

Create a component that:
1. Renders an iframe
2. Listens for postMessage events
3. Sends received data back to Python

```
streamlit_app/
└── components/
    └── simulation_bridge/
        ├── __init__.py
        ├── frontend/
        │   ├── index.html
        │   └── main.js
        └── simulation_bridge.py
```

### Step 3: Integrate with Teaching Agent

When student changes params:
1. Custom component receives postMessage
2. Component sends data to Streamlit Python
3. Streamlit updates session state
4. Agent is notified of student's exploration
5. Agent can respond: "I see you changed the length to 8! What did you observe?"

---

## Quick Prototype: PostMessage Listener (No Custom Component)

While custom components are the "right" way, here's a quick experiment you can try:

### Option A: Streamlit-JavaScript Bridge (streamlit-js-eval)

```python
# Install: pip install streamlit-js-eval
from streamlit_js_eval import streamlit_js_eval

# This runs JavaScript in the browser
result = streamlit_js_eval(js_expressions="""
    new Promise((resolve) => {
        window.addEventListener('message', function handler(event) {
            if (event.data && event.data.type === 'SIMULATION_PARAM_CHANGE') {
                window.removeEventListener('message', handler);
                resolve(JSON.stringify(event.data.params));
            }
        });
        // Timeout after 30 seconds
        setTimeout(() => resolve(null), 30000);
    });
""")

if result:
    st.write(f"Student changed params to: {result}")
```

### Option B: Polling with streamlit-autorefresh

```python
# Install: pip install streamlit-autorefresh
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 2 seconds to check for changes
st_autorefresh(interval=2000, key="param_checker")
```

---

## Files to Study

I'll create example files for you to study each approach:

1. `study/01_postmessage_basics.html` - Basic postMessage example
2. `study/02_simulation_sender.js` - JS code to add to simulation
3. `study/03_streamlit_receiver.py` - Streamlit code to receive messages
4. `study/04_custom_component/` - Full custom component example

---

## Security Considerations

1. **Origin Validation**: Always check `event.origin` in postMessage handlers
2. **Data Validation**: Validate incoming parameter values
3. **Rate Limiting**: Prevent spam from rapid parameter changes

---

## Next Steps

1. **Study the basics**: Read through the example files
2. **Modify simulation**: Add postMessage sender to your simulation HTML
3. **Create custom component**: Build a Streamlit component to receive messages
4. **Integrate with agent**: Update the teaching flow to respond to student exploration

Would you like me to create the study files with working examples?
