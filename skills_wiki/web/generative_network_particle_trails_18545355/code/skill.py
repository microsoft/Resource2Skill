def create_component(
    output_dir: str,
    title_text: str = "Digital Nexus",
    body_text: str = "Interactive Generative Network",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # Used for text highlights
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Generative Network Particle Trails effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color_hex = "#0A0A0A"
        text_color = "#FFFFFF"
        # Canvas needs an rgba equivalent for the motion blur trail effect
        trail_rgba = "rgba(10, 10, 10, 0.1)" 
    else:
        bg_color_hex = "#F0F4F8"
        text_color = "#0A0A0A"
        trail_rgba = "rgba(240, 244, 248, 0.1)"

    # === CSS ===
    css = f"""/* Generative Network Particle Trails */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color_hex};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.component-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background-color: var(--bg-color);
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Canvas styling */
#network-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    display: block;
}}

/* UI Overlay */
.content-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    pointer-events: none; /* Let mouse events pass through to the canvas */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.content-overlay h1 {{
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 20px {bg_color_hex};
}}

.content-overlay h1 span {{
    color: var(--accent-color);
}}

.content-overlay p {{
    font-size: 1.25rem;
    font-weight: 400;
    opacity: 0.8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-shadow: 0 2px 10px {bg_color_hex};
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
    <div class="component-wrapper">
        <canvas id="network-canvas" aria-label="Interactive generative particle network"></canvas>
        <div class="content-overlay">
            <h1>{title_text.replace(title_text.split()[-1], f"<span>{title_text.split()[-1]}</span>") if ' ' in title_text else title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generative Network Canvas Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('network-canvas');
    const ctx = canvas.getContext('2d');
    const wrapper = document.querySelector('.component-wrapper');

    // Canvas sizing based on container
    let width, height;
    function resizeCanvas() {{
        width = wrapper.clientWidth;
        height = wrapper.clientHeight;
        canvas.width = width;
        canvas.height = height;
    }}
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Mouse tracking
    const mouse = {{ x: undefined, y: undefined }};
    wrapper.addEventListener('pointermove', (e) => {{
        const rect = wrapper.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
        
        // Spawn multiple particles on movement to create dense web
        for (let i = 0; i < 4; i++) {{
            particlesArray.push(new Particle());
        }}
    }});

    wrapper.addEventListener('pointerleave', () => {{
        mouse.x = undefined;
        mouse.y = undefined;
    }});

    const particlesArray = [];
    let hue = 0; // Cycles through colors

    class Particle {{
        constructor() {{
            this.x = mouse.x;
            this.y = mouse.y;
            // Random size between 2 and 7
            this.size = Math.random() * 5 + 2;
            // Random trajectory
            this.speedX = Math.random() * 3 - 1.5;
            this.speedY = Math.random() * 3 - 1.5;
            // Assign current hue
            this.color = `hsl(${{hue}}, 100%, 60%)`;
        }}

        update() {{
            this.x += this.speedX;
            this.y += this.speedY;
            // Shrink over time
            if (this.size > 0.2) this.size -= 0.1;
        }}

        draw() {{
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }}
    }}

    function handleParticles() {{
        for (let i = 0; i < particlesArray.length; i++) {{
            particlesArray[i].update();
            particlesArray[i].draw();

            // Nested loop to calculate distance between all particles (The Network effect)
            for (let j = i; j < particlesArray.length; j++) {{
                const dx = particlesArray[i].x - particlesArray[j].x;
                const dy = particlesArray[i].y - particlesArray[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                // Draw connecting line if close enough
                if (distance < 100) {{
                    ctx.beginPath();
                    ctx.strokeStyle = particlesArray[i].color;
                    // Line gets thinner as particles get smaller/further
                    ctx.lineWidth = particlesArray[i].size / 3;
                    ctx.moveTo(particlesArray[i].x, particlesArray[i].y);
                    ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
                    ctx.stroke();
                }}
            }}

            // Remove dead particles to prevent memory leak and slow down
            if (particlesArray[i].size <= 0.3) {{
                particlesArray.splice(i, 1);
                i--;
            }}
        }}
    }}

    function animate() {{
        // Semi-transparent clear creates the motion trail effect
        // Using the dynamically injected trail color based on theme
        ctx.fillStyle = '{trail_rgba}';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        handleParticles();
        
        // Cycle colors slowly
        hue += 2;
        
        requestAnimationFrame(animate);
    }}

    // Start animation loop
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
