/**
 * Simulation Parameter Change Notifier
 * =====================================
 * 
 * This JavaScript code should be added to your simulation HTML file.
 * It broadcasts parameter changes to the parent window (Streamlit app).
 * 
 * USAGE:
 * 1. Include this script in your simulation HTML
 * 2. Call initParamNotifier() when simulation loads
 * 3. Call notifyParamChange() whenever a parameter changes
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const NOTIFIER_CONFIG = {
    // Message type identifier (Streamlit will filter for this)
    MESSAGE_TYPE: 'SIMULATION_PARAM_CHANGE',
    
    // Debounce delay (ms) - prevents spam when dragging sliders
    DEBOUNCE_DELAY: 100,
    
    // Source identifier
    SOURCE: 'pendulum_simulation',
    
    // Target origin ('*' for any, or specific URL for security)
    // In production, set this to your Streamlit app's URL
    TARGET_ORIGIN: '*'
};

// ============================================================================
// STATE TRACKING
// ============================================================================

let previousParams = {};
let debounceTimer = null;
let changeHistory = [];

// ============================================================================
// CORE FUNCTIONS
// ============================================================================

/**
 * Initialize the parameter notifier
 * Call this when your simulation loads
 * 
 * @param {Object} initialParams - Initial parameter values
 */
function initParamNotifier(initialParams) {
    previousParams = { ...initialParams };
    
    // Notify parent that simulation is ready
    sendToParent({
        type: 'SIMULATION_READY',
        params: initialParams,
        timestamp: Date.now(),
        source: NOTIFIER_CONFIG.SOURCE
    });
    
    console.log('[ParamNotifier] Initialized with params:', initialParams);
}

/**
 * Notify parent of a parameter change
 * Call this whenever a parameter changes (e.g., slider moved, input changed)
 * 
 * @param {string} paramName - Name of the parameter that changed
 * @param {any} newValue - New value of the parameter
 * @param {Object} allParams - Optional: all current parameters
 */
function notifyParamChange(paramName, newValue, allParams = null) {
    // Clear any pending debounce
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    
    // Debounce to prevent spam during slider dragging
    debounceTimer = setTimeout(() => {
        const oldValue = previousParams[paramName];
        
        // Only notify if value actually changed
        if (oldValue === newValue) {
            return;
        }
        
        // Build the message
        const message = {
            type: NOTIFIER_CONFIG.MESSAGE_TYPE,
            change: {
                param: paramName,
                oldValue: oldValue,
                newValue: newValue
            },
            allParams: allParams || getCurrentParamsFromDOM(),
            timestamp: Date.now(),
            source: NOTIFIER_CONFIG.SOURCE,
            changeId: generateChangeId()
        };
        
        // Update tracking
        previousParams[paramName] = newValue;
        changeHistory.push(message);
        
        // Send to parent
        sendToParent(message);
        
        console.log('[ParamNotifier] Sent change:', message);
        
    }, NOTIFIER_CONFIG.DEBOUNCE_DELAY);
}

/**
 * Notify parent of multiple parameter changes at once
 * Useful for "reset" or "preset" buttons
 * 
 * @param {Object} newParams - Object with all new parameter values
 */
function notifyBulkParamChange(newParams) {
    const changes = [];
    
    for (const [param, newValue] of Object.entries(newParams)) {
        if (previousParams[param] !== newValue) {
            changes.push({
                param: param,
                oldValue: previousParams[param],
                newValue: newValue
            });
        }
    }
    
    if (changes.length === 0) {
        return; // No actual changes
    }
    
    const message = {
        type: 'SIMULATION_BULK_CHANGE',
        changes: changes,
        allParams: newParams,
        timestamp: Date.now(),
        source: NOTIFIER_CONFIG.SOURCE,
        changeId: generateChangeId()
    };
    
    // Update tracking
    previousParams = { ...newParams };
    changeHistory.push(message);
    
    sendToParent(message);
    
    console.log('[ParamNotifier] Sent bulk change:', message);
}

/**
 * Notify parent that student started interacting
 * Call this on mousedown/touchstart on interactive elements
 */
function notifyInteractionStart(elementName) {
    sendToParent({
        type: 'SIMULATION_INTERACTION_START',
        element: elementName,
        timestamp: Date.now(),
        source: NOTIFIER_CONFIG.SOURCE
    });
}

/**
 * Notify parent that student stopped interacting
 * Call this on mouseup/touchend
 */
function notifyInteractionEnd(elementName) {
    sendToParent({
        type: 'SIMULATION_INTERACTION_END',
        element: elementName,
        currentParams: getCurrentParamsFromDOM(),
        timestamp: Date.now(),
        source: NOTIFIER_CONFIG.SOURCE
    });
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Send message to parent window
 */
function sendToParent(message) {
    if (window.parent && window.parent !== window) {
        window.parent.postMessage(message, NOTIFIER_CONFIG.TARGET_ORIGIN);
    } else {
        console.warn('[ParamNotifier] No parent window found');
    }
}

/**
 * Generate unique change ID
 */
function generateChangeId() {
    return `change_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Get current parameters from DOM elements
 * CUSTOMIZE THIS for your specific simulation!
 */
function getCurrentParamsFromDOM() {
    // Example implementation - modify for your simulation
    return {
        length: parseFloat(document.getElementById('lengthSlider')?.value || 5),
        number_of_oscillations: parseInt(document.getElementById('oscillationsSlider')?.value || 10)
        // Add more parameters as needed
    };
}

// ============================================================================
// AUTO-ATTACH TO COMMON INPUT ELEMENTS
// ============================================================================

/**
 * Automatically attach notifiers to input elements
 * Call this after DOM is loaded
 * 
 * @param {Object} elementMap - Map of element IDs to parameter names
 * Example: { 'lengthSlider': 'length', 'oscInput': 'number_of_oscillations' }
 */
function autoAttachNotifiers(elementMap) {
    for (const [elementId, paramName] of Object.entries(elementMap)) {
        const element = document.getElementById(elementId);
        
        if (!element) {
            console.warn(`[ParamNotifier] Element not found: ${elementId}`);
            continue;
        }
        
        // Attach appropriate event listeners based on element type
        if (element.type === 'range') {
            // Slider - notify on input (while dragging) and change (on release)
            element.addEventListener('input', (e) => {
                notifyParamChange(paramName, parseFloat(e.target.value));
            });
            element.addEventListener('mousedown', () => notifyInteractionStart(paramName));
            element.addEventListener('mouseup', () => notifyInteractionEnd(paramName));
        } 
        else if (element.type === 'number' || element.type === 'text') {
            // Text/number input - notify on change (blur or enter)
            element.addEventListener('change', (e) => {
                const value = element.type === 'number' 
                    ? parseFloat(e.target.value) 
                    : e.target.value;
                notifyParamChange(paramName, value);
            });
        }
        else if (element.tagName === 'SELECT') {
            // Dropdown - notify on change
            element.addEventListener('change', (e) => {
                notifyParamChange(paramName, e.target.value);
            });
        }
        
        console.log(`[ParamNotifier] Attached to ${elementId} -> ${paramName}`);
    }
}

// ============================================================================
// EXAMPLE USAGE (add to your simulation's initialization)
// ============================================================================

/*
// In your simulation's init function:

document.addEventListener('DOMContentLoaded', function() {
    // Initialize with current params
    initParamNotifier({
        length: 5,
        number_of_oscillations: 10
    });
    
    // Auto-attach to your input elements
    autoAttachNotifiers({
        'lengthSlider': 'length',
        'lengthInput': 'length',
        'oscillationsSlider': 'number_of_oscillations',
        'oscillationsInput': 'number_of_oscillations'
    });
});

// Or manually call notifyParamChange when you handle changes:

function onLengthChange(newLength) {
    // Your existing logic...
    updateSimulation(newLength);
    
    // Notify parent
    notifyParamChange('length', newLength);
}
*/

// ============================================================================
// EXPORT (if using modules)
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initParamNotifier,
        notifyParamChange,
        notifyBulkParamChange,
        notifyInteractionStart,
        notifyInteractionEnd,
        autoAttachNotifiers,
        NOTIFIER_CONFIG
    };
}
