def create_component(
    output_dir: str,
    title_text: str = "FRONTEND",
    body_text: str = "Hover over the text to interact",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Canvas Particle Image effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        secondary_color = "#a200ff" # Purple gradient end
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        secondary_color = "#ff007f" # Pink gradient end
        
    # Sanitize inputs for JS injection
    safe_title = title_text.replace('"', '\\"').replace('\n', ' ')

    # === CSS ===
    css = f"""/* Particle Image Animation Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    background-image: radial-gradient(var(--surface) 1px, transparent 1px);
    background-size: 24px 24px;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    max-width: 95vw;
    aspect-ratio: var(--width) / var(--height);
    position: relative;
    border-radius: 16px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.2);
    background: var(--bg);
    border: 1px solid var(--surface);
    overflow: hidden;
}}

#particleCanvas {{
    display: block;
    width: 100%;
    height: 100%;
    cursor: crosshair;
}}

.content-overlay {{
    position: absolute;
    bottom: 32px;
    left: 0;
    width: 100%;
    text-align: center;
    pointer-events: none; /* Allows mouse events to pass through to canvas */
}}

.body-text {{
    font-size: 1.1rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    color: var(--text);
    opacity: 0.6;
    text-transform: uppercase;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particle Image Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Canvas contains the interactive particle image -->
        <canvas id="particleCanvas" aria-label="{safe_title}" role="img"></canvas>
        
        <div class="content-overlay">
            <h1 class="sr-only" style="display: none;">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Particle Image Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
    
    // Set internal resolution based on config
    canvas.width = {width_px};
    canvas.height = {height_px};

    // Physics & Configuration Constants
    const PARTICLE_DIAMETER = Math.max(4, Math.floor(canvas.width / 150));
    const REPEL_RADIUS = Math.max(50, canvas.width / 12);
    const REPEL_SPEED = 12;
    const RETURN_SPEED = 0.1;

    let particles = [];
    let mouseX = Infinity;
    let mouseY = Infinity;

    // Track mouse with CSS scaling correction
    canvas.addEventListener('mousemove', (e) => {{
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        mouseX = (e.clientX - rect.left) * scaleX;
        mouseY = (e.clientY - rect.top) * scaleY;
    }});

    canvas.addEventListener('mouseleave', () => {{
        mouseX = Infinity;
        mouseY = Infinity;
    }});

    function initParticles() {{
        // We use an offscreen canvas to generate an image (text + gradient).
        // This gracefully bypasses Cross-Origin Resource Sharing (CORS) errors 
        // that occur when trying to read external image pixels from a local file://
        const offCanvas = document.createElement('canvas');
        offCanvas.width = canvas.width;
        offCanvas.height = canvas.height;
        const offCtx = offCanvas.getContext('2d', {{ willReadFrequently: true }});

        // Generate graphics
        const text = "{safe_title}";
        const fontSize = Math.min(canvas.width / (text.length * 0.65), canvas.height / 3);
        offCtx.font = `900 ${{fontSize}}px 'Inter', sans-serif`;
        offCtx.textAlign = 'center';
        offCtx.textBaseline = 'middle';

        // Apply theme gradient
        const gradient = offCtx.createLinearGradient(0, 0, canvas.width, 0);
        gradient.addColorStop(0, '{accent_color}');
        gradient.addColorStop(1, '{secondary_color}');
        offCtx.fillStyle = gradient;
        offCtx.fillText(text, canvas.width / 2, canvas.height / 2);

        // Extract pixel data array
        const imgData = offCtx.getImageData(0, 0, offCanvas.width, offCanvas.height);
        const data = imgData.data;

        const numRows = Math.floor(canvas.height / PARTICLE_DIAMETER);
        const numColumns = Math.floor(canvas.width / PARTICLE_DIAMETER);

        // Map pixels to particles
        for (let row = 0; row < numRows; row++) {{
            for (let column = 0; column < numColumns; column++) {{
                const pixelX = column * PARTICLE_DIAMETER;
                const pixelY = row * PARTICLE_DIAMETER;
                
                // Convert 2D x,y to 1D array index (4 values per pixel: R,G,B,A)
                const pixelIndex = (pixelY * offCanvas.width + pixelX) * 4;
                const a = data[pixelIndex + 3];
                
                // Only create particles for visible pixels
                if (a > 30) {{
                    const r = data[pixelIndex];
                    const g = data[pixelIndex + 1];
                    const b = data[pixelIndex + 2];
                    
                    particles.push({{
                        x: Math.random() * canvas.width,    // Start in random chaotic positions
                        y: Math.random() * canvas.height,
                        originX: pixelX + PARTICLE_DIAMETER / 2,
                        originY: pixelY + PARTICLE_DIAMETER / 2,
                        color: `rgba(${{r}}, ${{g}}, ${{b}}, ${{a / 255}})`
                    }});
                }}
            }}
        }}
    }}

    function updateParticles() {{
        particles.forEach(particle => {{
            // Calculate distance to mouse
            const dxMouse = particle.x - mouseX;
            const dyMouse = particle.y - mouseY;
            const distanceMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);

            if (distanceMouse < REPEL_RADIUS) {{
                // Push particle away from mouse using angle and force
                const angle = Math.atan2(dyMouse, dxMouse);
                const force = (REPEL_RADIUS - distanceMouse) / REPEL_RADIUS;
                const moveX = Math.cos(angle) * force * REPEL_SPEED;
                const moveY = Math.sin(angle) * force * REPEL_SPEED;
                
                particle.x += moveX;
                particle.y += moveY;
                
            }} else if (Math.abs(particle.originX - particle.x) > 0.1 || Math.abs(particle.originY - particle.y) > 0.1) {{
                // If out of range, smoothly return to origin position using Linear Interpolation (Lerp).
                // Note: Mathematically equivalent to the video's trig approach but much faster to compute.
                particle.x += (particle.originX - particle.x) * RETURN_SPEED;
                particle.y += (particle.originY - particle.y) * RETURN_SPEED;
            }}
        }});
    }}

    function drawParticles() {{
        // Clear frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Update physics
        updateParticles();
        
        // Render
        particles.forEach(particle => {{
            ctx.beginPath();
            // Divide by 2.2 instead of 2 to leave a tiny aesthetic gap between particles
            ctx.arc(particle.x, particle.y, PARTICLE_DIAMETER / 2.2, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.fill();
        }});
        
        requestAnimationFrame(drawParticles);
    }}

    // Kickoff
    initParticles();
    drawParticles();
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": files,
    }
