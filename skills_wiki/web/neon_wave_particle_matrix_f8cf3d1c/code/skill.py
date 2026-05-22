def create_component(
    output_dir: str,
    title_text: str = "Neon Matrix",
    body_text: str = "Generative sine-wave particle system built with HTML5 Canvas.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Wave Particle Matrix effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors (Glow looks best on dark backgrounds)
    if color_scheme == "dark":
        bg_color = "#000000"
        text_color = "#ffffff"
        surface_color = "rgba(13, 17, 28, 0.7)"
    else:
        # Note: Neon glow requires contrast. On light themes, we use a dark surface behind text
        # and a slightly softer dark canvas background to maintain the visual effect.
        bg_color = "#111111" 
        text_color = "#f8f9fa"
        surface_color = "rgba(0, 0, 0, 0.6)"

    # === CSS ===
    css = f"""/* Neon Wave Particle Matrix — generated component */
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
    background: var(--bg);
    color: var(--text);
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
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

#particleCanvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    display: block;
}}

.content-overlay {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    pointer-events: none; /* Let clicks pass through if needed */
}}

.text-card {{
    background: var(--surface);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    pointer-events: auto;
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.05em;
    color: var(--text);
    text-shadow: 0 4px 20px rgba(0,0,0,0.8);
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    max-width: 500px;
    color: rgba(255, 255, 255, 0.8);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper">
        <canvas id="particleCanvas"></canvas>
        <div class="content-overlay">
            <div class="text-card">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Wave Particle Matrix Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    const wrapper = document.querySelector('.component-wrapper');
    
    let particlesArray = [];
    const waveHeight = 80;
    const gap = 40;
    const bgColor = "{bg_color}";
    
    // Set canvas size to match wrapper
    function resizeCanvas() {{
        canvas.width = wrapper.clientWidth;
        canvas.height = wrapper.clientHeight;
        init();
    }}

    class Particle {{
        constructor(x, y) {{
            this.x = x;
            this.y = y;
            this.baseY = y;
            this.size = Math.random() * 3 + 2;
            this.color = `hsl(${{Math.random() * 360}}, 100%, 50%)`;
            this.speed = Math.random() * 0.05 + 0.02;
            this.angle = Math.random() * Math.PI * 2;
        }}
        
        update() {{
            this.angle += this.speed;
            this.y = this.baseY + Math.sin(this.angle) * waveHeight;
        }}
        
        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowColor = this.color;
            ctx.shadowBlur = 15; // Adjusted slightly for consistent performance
            ctx.fill();
        }}
    }}

    function init() {{
        particlesArray = [];
        // Overshoot boundaries slightly to prevent pop-in at the edges
        for (let x = -gap; x < canvas.width + gap; x += gap) {{
            for (let y = -gap; y < canvas.height + gap; y += gap) {{
                particlesArray.push(new Particle(x, y));
            }}
        }}
    }}

    function animate() {{
        // Solid fill clears the previous frame cleanly
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        particlesArray.forEach(particle => {{
            particle.update();
            particle.draw();
        }});
        
        requestAnimationFrame(animate);
    }}

    window.addEventListener('resize', resizeCanvas);
    
    // Initial Setup
    resizeCanvas();
    animate();
}});
"""

    # Write files
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
