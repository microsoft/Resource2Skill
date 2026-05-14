def create_component(
    output_dir: str,
    title_text: str = "Frank's Laboratory",
    body_text: str = "creative web animations",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Canvas Particle System.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        gradient_start = "#1a1a2e"
        gradient_mid = "#16213e"
        gradient_end = "#0f3460"
        text_color = "#ffffff"
        particle_color = accent_color
    else:
        # Replicating the tutorial's specific blue gradient for light/default mode
        gradient_start = "#25364f"
        gradient_mid = "#4d71a5"
        gradient_end = "#9bc4ff"
        text_color = "#ffffff"
        particle_color = accent_color

    # === CSS ===
    css = f"""/* Ambient Canvas Particle System */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --text: {text_color};
    --grad-start: {gradient_start};
    --grad-mid: {gradient_mid};
    --grad-end: {gradient_end};
}}

body {{
    font-family: 'Courier New', Courier, monospace; /* Matching tutorial's tech vibe */
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.component-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: linear-gradient(to bottom, var(--grad-start), var(--grad-mid), var(--grad-end));
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

#canvas1 {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1; /* Behind text */
}}

.content {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2; /* In front of canvas */
    text-align: center;
    color: var(--text);
    pointer-events: none; /* Let clicks pass through to canvas if needed later */
}}

.content h1 {{
    font-size: 3rem;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}

.content p {{
    font-size: 1.2rem;
    letter-spacing: 4px;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper">
        <canvas id="canvas1"></canvas>
        <div class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    
    <!-- Script loaded at the end of body to ensure DOM is ready -->
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Canvas Particle System Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('canvas1');
    const ctx = canvas.getContext('2d');
    const wrapper = document.querySelector('.component-wrapper');
    
    // Set internal canvas dimensions to match actual CSS display size
    canvas.width = wrapper.clientWidth;
    canvas.height = wrapper.clientHeight;
    
    let particlesArray;
    const particleColor = '{particle_color}';

    // Using modern ES6 Class syntax equivalent to the tutorial's Constructor/Prototype approach
    class Particle {{
        constructor(x, y, directionX, directionY, size, color) {{
            this.x = x;
            this.y = y;
            this.directionX = directionX;
            this.directionY = directionY;
            this.size = size;
            this.color = color;
        }}

        // Draw particle on canvas
        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }}

        // Update particle position and check boundaries
        update() {{
            // Check collision with right and left canvas boundaries
            if (this.x + this.size > canvas.width || this.x - this.size < 0) {{
                this.directionX = -this.directionX;
            }}
            // Check collision with bottom and top canvas boundaries
            if (this.y + this.size > canvas.height || this.y - this.size < 0) {{
                this.directionY = -this.directionY;
            }}

            // Move particle
            this.x += this.directionX;
            this.y += this.directionY;

            // Render
            this.draw();
        }}
    }}

    // Populate particle array
    function init() {{
        particlesArray = [];
        const numberOfParticles = 100; // Configurable density

        for (let i = 0; i < numberOfParticles; i++) {{
            // Random size between 1 and 21
            let size = (Math.random() * 20) + 1;
            
            // Random spawn position, ensuring particles spawn fully inside canvas bounds
            let x = (Math.random() * ((canvas.width - size * 2) - (size * 2)) + size * 2);
            let y = (Math.random() * ((canvas.height - size * 2) - (size * 2)) + size * 2);
            
            // Random speed and direction (-0.2 to +0.2)
            let directionX = (Math.random() * 0.4) - 0.2;
            let directionY = (Math.random() * 0.4) - 0.2;
            
            particlesArray.push(new Particle(x, y, directionX, directionY, size, particleColor));
        }}
    }}

    // Animation Loop
    function animate() {{
        requestAnimationFrame(animate);
        // Clear previous frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update and draw all particles
        for (let i = 0; i < particlesArray.length; i++) {{
            particlesArray[i].update();
        }}
    }}

    // Handle container resizing to prevent stretching and stuck particles
    window.addEventListener('resize', () => {{
        canvas.width = wrapper.clientWidth;
        canvas.height = wrapper.clientHeight;
        init(); // Re-initialize to distribute particles properly in new size
    }});

    // Kickoff
    init();
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
