# Simulation Bridge - Custom Streamlit Component

This is a custom Streamlit component that enables **bi-directional communication** between your Streamlit app and embedded simulations.

## 📋 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP (Parent)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               Custom Component (iframe)                   │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │         Simulation (nested iframe)                  │  │  │
│  │  │                                                     │  │  │
│  │  │   Student interacts → sends postMessage ────────┐   │  │  │
│  │  │                                                 │   │  │  │
│  │  └─────────────────────────────────────────────────│───┘  │  │
│  │                                                    │      │  │
│  │  Component receives message, sends to Streamlit ←──┘      │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  Python code receives the parameter change data ←───────────────│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# No additional dependencies needed beyond Streamlit
pip install streamlit
```

### 2. Basic Usage
```python
import streamlit as st
from simulation_bridge import simulation_bridge

# Embed simulation with bi-directional communication
result = simulation_bridge(
    simulation_url="https://your-simulation.com?param1=5",
    height=600,
    key="my_sim"
)

# When student changes parameters, result will contain the change
if result:
    st.success(f"Student changed {result['change']['param']}")
    st.write(f"Old: {result['change']['oldValue']} → New: {result['change']['newValue']}")
```

## 📦 Component Structure

```
04_custom_component/
├── simulation_bridge.py   # Python interface
├── frontend/
│   └── index.html         # Component UI + JS logic
└── README.md              # This file
```

## 🔧 How It Works

### 1. Python Side (`simulation_bridge.py`)
- Declares a Streamlit component using `components.declare_component()`
- Passes simulation URL and config to the frontend
- Receives parameter change events from the frontend

### 2. Frontend Side (`frontend/index.html`)
- Embeds the simulation in an iframe
- Listens for `postMessage` events from the simulation
- Normalizes different message formats
- Sends normalized data back to Streamlit via `setComponentValue`

### 3. Simulation Side (Your simulation HTML)
- Detects when user changes parameters
- Sends `postMessage` to parent with change details

## 📡 Message Format

The simulation should send messages in one of these formats:

### Format A (Recommended)
```javascript
window.parent.postMessage({
    type: 'SIMULATION_PARAM_CHANGE',
    change: {
        param: 'length',
        oldValue: 5,
        newValue: 8
    },
    allParams: {
        length: 8,
        oscillations: 10
    },
    timestamp: Date.now(),
    source: 'pendulum_simulation'
}, '*');
```

### Format B (Simple)
```javascript
window.parent.postMessage({
    param: 'length',
    value: 8,
    oldValue: 5
}, '*');
```

### Format C (Alternative)
```javascript
window.parent.postMessage({
    parameter: 'length',
    newValue: 8,
    previousValue: 5
}, '*');
```

All formats are automatically normalized by the component.

## 🔗 Integration with Teaching Agent

Here's how to integrate this with your teaching agent:

```python
# In your app.py or main teaching loop

from simulation_bridge import simulation_bridge

# After agent provides a lesson with simulation
def handle_lesson_display(lesson_content, simulation_url):
    st.markdown(lesson_content)
    
    # Embed simulation with bridge
    student_interaction = simulation_bridge(
        simulation_url=simulation_url,
        height=600,
        key=f"sim_{session_id}"
    )
    
    # Check if student explored on their own
    if student_interaction:
        param = student_interaction['change']['param']
        new_val = student_interaction['change']['newValue']
        
        # Tell the agent about student's exploration
        agent_response = send_student_response(
            thread_id=session_id,
            response=f"[STUDENT EXPLORED] Changed {param} to {new_val}"
        )
        
        # The agent can now respond to this exploration!
        st.write(agent_response['teacher_output'])
```

## 🧪 Testing

1. Run the test app:
```bash
cd study/04_custom_component
streamlit run simulation_bridge.py
```

2. Enter a simulation URL that sends postMessage events

3. Interact with the simulation and see changes logged

## 📝 Adding postMessage to Your Simulation

If your simulation doesn't send postMessage events yet, add this to its JavaScript:

```javascript
// Add this to your simulation's JavaScript file

// 1. Track parameter values
let params = {
    length: 5,
    oscillations: 10
    // ... your parameters
};

// 2. Send change notifications
function onParamChange(paramName, newValue) {
    const oldValue = params[paramName];
    params[paramName] = newValue;
    
    // Send to parent (the Streamlit component)
    window.parent.postMessage({
        type: 'SIMULATION_PARAM_CHANGE',
        change: {
            param: paramName,
            oldValue: oldValue,
            newValue: newValue
        },
        allParams: {...params},
        timestamp: Date.now()
    }, '*');
}

// 3. Hook into your existing UI controls
// Example for a slider:
document.getElementById('lengthSlider').addEventListener('change', (e) => {
    onParamChange('length', parseFloat(e.target.value));
});
```

## ⚠️ Limitations

1. **Cross-Origin**: Works across different domains (uses `postMessage`)
2. **Simulation Modification**: Requires adding JS to the simulation
3. **One-Way for Now**: Simulation → Streamlit (Streamlit → Simulation via URL params)

## 🔜 Next Steps

1. **Fork your simulation** on GitHub Pages
2. **Add the postMessage code** to detect user interactions
3. **Deploy** the modified simulation
4. **Use this component** to receive student interactions

See also:
- `02_simulation_sender.js` - Ready-to-use JavaScript module
- `05_websocket_bridge/` - Alternative approach using WebSockets
