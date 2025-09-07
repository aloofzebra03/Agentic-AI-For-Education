"""
Simulation HTML Generation Utilities
Standalone module for creating pendulum simulation HTML without app dependencies
"""

import json

def create_pendulum_simulation_html(config):
    """
    Generate HTML for pendulum simulation based on configuration.
    Uses the simulation from index.html with automated before/after demonstration.
    
    Args:
        config (dict): Simulation configuration with keys:
            - before_params: {"length": float, "gravity": float, "amplitude": float}
            - after_params: {"length": float, "gravity": float, "amplitude": float}  
            - timing: {"before_duration": int, "transition_duration": int, "after_duration": int}
            - agent_message: str
    
    Returns:
        str: Complete HTML with embedded JavaScript for pendulum animation
    """
    before_params = config['before_params']
    after_params = config['after_params']
    timing = config['timing']
    agent_message = config['agent_message']
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .simulation-container {{
                width: 100%;
                max-width: 600px;
                margin: 10px auto;
                background: #f0f6ff;
                border: 2px solid #c4afe9;
                border-radius: 15px;
                padding: 15px;
                text-align: center;
                position: relative;
            }}
            .simulation-canvas {{
                background: #ede9fe;
                border-radius: 12px;
                margin: 10px auto;
                display: block;
            }}
            .simulation-controls {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 10px 0;
                font-family: 'Segoe UI', sans-serif;
            }}
            .param-display {{
                background: rgba(124, 58, 237, 0.1);
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            .agent-message {{
                background: rgba(124, 58, 237, 0.9);
                color: white;
                padding: 10px 15px;
                border-radius: 10px;
                margin: 10px 0;
                font-size: 16px;
                font-weight: 500;
            }}
            .phase-indicator {{
                background: #7c3aed;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="simulation-container">
            <div class="agent-message">{agent_message}</div>
            <div id="phase-indicator" class="phase-indicator">Phase: Before Change</div>
            
            <canvas id="pendulum-canvas" class="simulation-canvas" width="400" height="300"></canvas>
            
            <div class="simulation-controls">
                <div class="param-display">
                    Length: <span id="length-display">{before_params['length']:.1f}m</span>
                </div>
                <div class="param-display">
                    Gravity: <span id="gravity-display">{before_params['gravity']:.1f} m/s²</span>
                </div>
                <div class="param-display">
                    Amplitude: <span id="amplitude-display">{before_params['amplitude']}°</span>
                </div>
            </div>
        </div>
        
        <script>
            // Simulation parameters
            const beforeParams = {json.dumps(before_params)};
            const afterParams = {json.dumps(after_params)};
            const timing = {json.dumps(timing)};
            
            // Canvas setup
            const canvas = document.getElementById('pendulum-canvas');
            const ctx = canvas.getContext('2d');
            const originX = 200, originY = 60;
            const baseScale = 80;
            
            // Animation state
            let currentParams = {{...beforeParams}};
            let angle = (currentParams.amplitude * Math.PI) / 180;
            let aVel = 0, aAcc = 0;
            const dt = 0.02;
            let startTime = Date.now();
            let phase = 'before'; // 'before', 'transition', 'after'
            
            function updatePhaseIndicator() {{
                const indicator = document.getElementById('phase-indicator');
                const elapsed = (Date.now() - startTime) / 1000;
                
                if (elapsed < timing.before_duration) {{
                    indicator.textContent = 'Phase: Before Change';
                    phase = 'before';
                }} else if (elapsed < timing.before_duration + timing.transition_duration) {{
                    indicator.textContent = 'Phase: Changing Parameters...';
                    phase = 'transition';
                    
                    // Smooth transition
                    const transitionProgress = (elapsed - timing.before_duration) / timing.transition_duration;
                    const progress = Math.min(transitionProgress, 1);
                    
                    // Interpolate parameters
                    currentParams.length = beforeParams.length + (afterParams.length - beforeParams.length) * progress;
                    currentParams.gravity = beforeParams.gravity + (afterParams.gravity - beforeParams.gravity) * progress;
                    currentParams.amplitude = beforeParams.amplitude + (afterParams.amplitude - beforeParams.amplitude) * progress;
                    
                    // Reset pendulum when transition completes
                    if (progress === 1) {{
                        angle = (currentParams.amplitude * Math.PI) / 180;
                        aVel = 0;
                    }}
                }} else {{
                    indicator.textContent = 'Phase: After Change';
                    phase = 'after';
                    currentParams = {{...afterParams}};
                }}
                
                // Update displays
                document.getElementById('length-display').textContent = currentParams.length.toFixed(1) + 'm';
                document.getElementById('gravity-display').textContent = currentParams.gravity.toFixed(1) + ' m/s²';
                document.getElementById('amplitude-display').textContent = Math.round(currentParams.amplitude) + '°';
            }}
            
            function drawPendulum() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Calculate pendulum physics
                const lengthPixels = currentParams.length * baseScale;
                aAcc = (-currentParams.gravity / currentParams.length) * Math.sin(angle);
                aVel += aAcc * dt;
                aVel *= 0.998; // Damping
                angle += aVel * dt;
                
                // Calculate bob position
                const bobX = originX + lengthPixels * Math.sin(angle);
                const bobY = originY + lengthPixels * Math.cos(angle);
                
                // Draw pivot point
                ctx.beginPath();
                ctx.arc(originX, originY, 6, 0, 2 * Math.PI);
                ctx.fillStyle = '#7c3aed';
                ctx.fill();
                
                // Draw string
                ctx.beginPath();
                ctx.moveTo(originX, originY);
                ctx.lineTo(bobX, bobY);
                ctx.strokeStyle = '#7c3aed';
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // Draw bob
                ctx.beginPath();
                ctx.arc(bobX, bobY, 15, 0, 2 * Math.PI);
                ctx.fillStyle = '#ede9fe';
                ctx.strokeStyle = '#7c3aed';
                ctx.lineWidth = 2.5;
                ctx.fill();
                ctx.stroke();
            }}
            
            function animate() {{
                updatePhaseIndicator();
                drawPendulum();
                requestAnimationFrame(animate);
            }}
            
            // Start animation
            animate();
        </script>
    </body>
    </html>
    """
