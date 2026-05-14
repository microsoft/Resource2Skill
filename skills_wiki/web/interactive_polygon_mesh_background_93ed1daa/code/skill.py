def create_component(
    output_dir: str,
    title_text: str = "Connected Network",
    body_text: str = "Visualizing data points in a dynamic polygon mesh environment.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00e5ff",     # CSS hex color for accent/particles
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Polygon Mesh Background visual effect.
    Uses Vanilla JS and HTML5 Canvas (no jQuery or external plugins required).
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121214"
        text_color = "#ffffff"
        body_text_color = "#a0a0ab"
        particle_color = accent_color
    else:
        bg_color = "#f4f4f9"
        text_color = "#111111"
        body_text_color = "#555560"
        particle_color = accent_color

    # === CSS ===
    css = f"""/* Polygon Mesh Background */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --body-text: {body_text_color};
    --accent: {accent_color};
    --particle-color: {particle_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.mesh-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background-color: var(--bg);
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
    border-radius: 12px;
}}

canvas#mesh-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    display: block;
}}

.overlay-content {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    text-align: center;
    color: var(--text);
    pointer-events: none; /* Let clicks pass through to canvas if needed later */
    width: 80%;
    max-width: 600px;
}}

.overlay-content h1 {{
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    line-height: 1.1;
    text-shadow: 0 4px 24px rgba(0,0,0,0.4);
}}

.overlay-content p {{
    font-size: 1.25rem;
    color: var(--body-text);
    line-height: 1.6;
    text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}}

/* Ensure responsiveness within defined dimensions */
@media (max-width: 768px) {{
    .overlay-content h1 {{
        font-size: 2rem;
    }}
    .overlay-content p {{
        font-size: 1rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="mesh-container">
        <!-- Canvas for the background mesh -->
        <canvas id="mesh-canvas"></canvas>
        
        <!-- Foreground content -->
        <div class="overlay-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Polygon Mesh Implementation
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('mesh-canvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.mesh-container');

    // Get color from CSS variables
    const styles = getComputedStyle(document.documentElement);
    const pColor = styles.getPropertyValue('--particle-color').trim();

    let particlesArray = [];
    
    // Configuration
    const baseParticleDensity = 10000; // 1 particle per 10,000 sq pixels
    const maxDistance = 120; // Max distance to draw a line
    const particleRadius = 1.5;
    const baseSpeed = 0.5;

    // Handle Resize
    let width, height;
    function resizeCanvas() {{
        width = container.clientWidth;
        height = container.clientHeight;
        canvas.width = width;
        canvas.height = height;
        initParticles();
    }}

    window.addEventListener('resize', () => {{
        // Basic debounce
        clearTimeout(window.resizeTimer);
        window.resizeTimer = setTimeout(resizeCanvas, 200);
    }});

    // Particle Object
    class Particle {{
        constructor() {{
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            // Random direction and speed
            this.vx = (Math.random() - 0.5) * baseSpeed * 2;
            this.vy = (Math.random() - 0.5) * baseSpeed * 2;
            this.radius = Math.random() * particleRadius + 0.5;
        }}

        update() {{
            // Move
            this.x += this.vx;
            this.y += this.vy;

            // Bounce off edges
            if (this.x < 0 || this.x > width) this.vx = -this.vx;
            if (this.y < 0 || this.y > height) this.vy = -this.vy;
        }}

        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = pColor;
            ctx.fill();
        }}
    }}

    // Initialize Particles
    function initParticles() {{
        particlesArray = [];
        const area = width * height;
        let numberOfParticles = Math.floor(area / baseParticleDensity);
        
        // Cap particles for performance on huge screens
        if(numberOfParticles > 200) numberOfParticles = 200; 
        
        for (let i = 0; i < numberOfParticles; i++) {{
            particlesArray.push(new Particle());
        }}
    }}

    // Connect Particles
    function connect() {{
        for (let a = 0; a < particlesArray.length; a++) {{
            for (let b = a + 1; b < particlesArray.length; b++) {{
                let dx = particlesArray[a].x - particlesArray[b].x;
                let dy = particlesArray[a].y - particlesArray[b].y;
                let distance = Math.hypot(dx, dy);

                if (distance < maxDistance) {{
                    // Calculate opacity based on distance
                    const opacity = 1 - (distance / maxDistance);
                    ctx.globalAlpha = opacity * 0.7; // Max opacity 0.7
                    ctx.strokeStyle = pColor;
                    ctx.lineWidth = 1;
                    
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }}
            }}
        }}
        ctx.globalAlpha = 1; // Reset alpha
    }}

    // Animation Loop
    function animate() {{
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Update and draw nodes
        for (let i = 0; i < particlesArray.length; i++) {{
            particlesArray[i].update();
            particlesArray[i].draw();
        }}
        
        // Draw connecting mesh
        connect();
        
        requestAnimationFrame(animate);
    }}

    // Boot
    resizeCanvas(); // Sets initial size and creates particles
    animate();
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
