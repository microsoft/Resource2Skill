def create_component(
    output_dir: str,
    title_text: str = "Interactive Swarm",
    body_text: str = "Move your cursor across the space to interact with the particles.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3498db",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Canvas Particle Swarm effect.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0b10"
        text_color = "#ffffff"
        # Dynamic palette mixing the accent color with complementary/vibrant tones
        palette = [accent_color, "#e74c3c", "#ecf0f1", "#9b59b6", "#1abc9c"]
    else:
        bg_color = "#f4f7f6"
        text_color = "#111827"
        palette = [accent_color, "#e74c3c", "#34495e", "#9b59b6", "#f39c12"]

    palette_js = json.dumps(palette)

    # === CSS ===
    css = f"""/* Interactive Particle Swarm Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Darker backdrop for page */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.swarm-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    background: var(--bg);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* The canvas fills the container */
#particle-canvas {{
    display: block;
    width: 100%;
    height: 100%;
}}

/* Overlay text styling */
.content-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: var(--text);
    z-index: 10;
    /* Prevent text block from blocking mouse hover on canvas */
    pointer-events: none; 
    width: 80%;
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    text-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

.body-text {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    opacity: 0.85;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="swarm-container">
        <canvas id="particle-canvas"></canvas>
        <div class="content-overlay">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Canvas Particle Swarm Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.swarm-container');

    let particleArray = [];
    const colorPalette = {palette_js};

    // Track mouse position relative to canvas
    let mouse = {{
        x: undefined,
        y: undefined,
        radius: 80 // Interaction radius
    }};

    // Handle mouse movement
    canvas.addEventListener('mousemove', (event) => {{
        const rect = canvas.getBoundingClientRect();
        mouse.x = event.clientX - rect.left;
        mouse.y = event.clientY - rect.top;
    }});

    // Reset mouse position when leaving canvas
    canvas.addEventListener('mouseleave', () => {{
        mouse.x = undefined;
        mouse.y = undefined;
    }});

    // Sync canvas resolution with container size
    function resizeCanvas() {{
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        initParticles();
    }}

    window.addEventListener('resize', resizeCanvas);

    // Particle Class
    class Particle {{
        constructor(x, y, dx, dy, radius, color) {{
            this.x = x;
            this.y = y;
            this.dx = dx;
            this.dy = dy;
            this.radius = radius;
            this.minRadius = radius;
            this.maxRadius = radius * 4 + 10;
            this.color = color;
        }}

        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }}

        update() {{
            // Bounce off walls
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {{
                this.dx = -this.dx;
            }}
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {{
                this.dy = -this.dy;
            }}

            // Move particle
            this.x += this.dx;
            this.y += this.dy;

            // Interactivity: Check proximity to mouse
            if (mouse.x !== undefined && mouse.y !== undefined) {{
                // Euclidean distance
                const dist = Math.hypot(mouse.x - this.x, mouse.y - this.y);

                if (dist < mouse.radius) {{
                    if (this.radius < this.maxRadius) {{
                        this.radius += 2.5; // Growth speed
                    }}
                }} else if (this.radius > this.minRadius) {{
                    this.radius -= 1; // Shrink speed
                }}
            }} else if (this.radius > this.minRadius) {{
                // Shrink back if mouse leaves canvas
                this.radius -= 1;
            }}

            this.draw();
        }}
    }}

    // Initialize the swarm
    function initParticles() {{
        particleArray = [];
        // Determine number of particles based on container area (density approach)
        const area = canvas.width * canvas.height;
        const numberOfParticles = Math.floor(area / 5000); 

        for (let i = 0; i < numberOfParticles; i++) {{
            let radius = Math.random() * 4 + 1; // Base radius 1-5px
            // Ensure particles spawn fully inside canvas
            let x = Math.random() * (canvas.width - radius * 2) + radius;
            let y = Math.random() * (canvas.height - radius * 2) + radius;
            // Random velocities
            let dx = (Math.random() - 0.5) * 1.5;
            let dy = (Math.random() - 0.5) * 1.5;
            // Pick random color from palette
            let color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
            
            particleArray.push(new Particle(x, y, dx, dy, radius, color));
        }}
    }}

    // Animation Loop
    function animate() {{
        requestAnimationFrame(animate);
        // Clear previous frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particleArray.length; i++) {{
            particleArray[i].update();
        }}
    }}

    // Kickoff
    resizeCanvas();
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
