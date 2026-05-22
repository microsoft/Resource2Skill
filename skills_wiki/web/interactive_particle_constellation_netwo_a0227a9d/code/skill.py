def create_component(
    output_dir: str,
    title_text: str = "Connected Future",
    body_text: str = "Building the neural networks of tomorrow with intelligent data infrastructure.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for particles and lines
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Particle Constellation Network.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#ffffff"
        text_secondary = "#a0aab2"
        surface_gradient = "radial-gradient(circle at center, #11151d 0%, #0a0c10 100%)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        text_secondary = "#4b5563"
        surface_gradient = "radial-gradient(circle at center, #ffffff 0%, #f4f6f8 100%)"

    # === CSS ===
    css = f"""/* Interactive Particle Constellation Network — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    background-image: {surface_gradient};
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}}

/* The container establishes boundaries for our preview */
.preview-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background: var(--bg-color);
    background-image: {surface_gradient};
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* The canvas is placed behind the text content */
#particle-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    pointer-events: auto; /* Required to catch mouse movements */
}}

/* Foreground UI overlay */
.hero-content {{
    position: relative;
    z-index: 2;
    pointer-events: none; /* Let mouse pass through to canvas */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    padding: 2rem;
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
    line-height: 1.1;
    text-shadow: 0 4px 24px rgba(0,0,0,0.2);
}}

.title span {{
    color: var(--accent);
}}

.body-text {{
    font-size: clamp(1rem, 1.5vw, 1.25rem);
    color: var(--text-secondary);
    max-width: 600px;
    line-height: 1.6;
    margin-bottom: 2.5rem;
}}

.cta-button {{
    pointer-events: auto; /* Re-enable pointer for the button */
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px {accent_color}80;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        <canvas id="particle-canvas"></canvas>
        <div class="hero-content">
            <h1 class="title">Connected <span>Future</span></h1>
            <p class="body-text">{body_text}</p>
            <button class="cta-button">Explore Network</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Particle Constellation Network
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.preview-container');
    
    let particlesArray = [];
    
    // Config
    const ACCENT_HEX = '{accent_color}';
    const CONNECT_DISTANCE = 130; 
    const MOUSE_RADIUS = 100;

    // Helper: Convert Hex to RGB for dynamic opacity assignment in strokes
    function hexToRgb(hex) {{
        let r = 0, g = 0, b = 0;
        hex = hex.replace('#', '');
        if (hex.length === 3) {{
            r = parseInt(hex.charAt(0) + hex.charAt(0), 16);
            g = parseInt(hex.charAt(1) + hex.charAt(1), 16);
            b = parseInt(hex.charAt(2) + hex.charAt(2), 16);
        }} else if (hex.length === 6) {{
            r = parseInt(hex.substring(0, 2), 16);
            g = parseInt(hex.substring(2, 4), 16);
            b = parseInt(hex.substring(4, 6), 16);
        }}
        return `${{r}}, ${{g}}, ${{b}}`;
    }}
    
    const rgbAccent = hexToRgb(ACCENT_HEX);

    // Track mouse
    let mouse = {{
        x: null,
        y: null,
        radius: MOUSE_RADIUS
    }};

    // Handle Resize
    function setCanvasSize() {{
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
    }}
    setCanvasSize();

    window.addEventListener('resize', () => {{
        setCanvasSize();
        init(); // Recreate particles to fit new dimensions
    }});

    // Mouse Events
    canvas.addEventListener('mousemove', (event) => {{
        const rect = canvas.getBoundingClientRect();
        mouse.x = event.clientX - rect.left;
        mouse.y = event.clientY - rect.top;
    }});

    canvas.addEventListener('mouseleave', () => {{
        mouse.x = null;
        mouse.y = null;
    }});

    // Particle Class
    class Particle {{
        constructor(x, y, directionX, directionY, size, color) {{
            this.x = x;
            this.y = y;
            this.directionX = directionX;
            this.directionY = directionY;
            this.size = size;
            this.color = color;
            // Density affects how fast they get pushed by the mouse
            this.density = (Math.random() * 30) + 1;
        }}

        // Draw individual particle
        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }}

        // Update particle position and handle collisions
        update() {{
            // Canvas boundaries collision
            if (this.x > canvas.width || this.x < 0) {{
                this.directionX = -this.directionX;
            }}
            if (this.y > canvas.height || this.y < 0) {{
                this.directionY = -this.directionY;
            }}

            // Mouse collision / repulsion
            if (mouse.x != null && mouse.y != null) {{
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < mouse.radius + this.size) {{
                    // Calculate vector to push particle away
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (mouse.radius - distance) / mouse.radius;
                    
                    const directionX = forceDirectionX * force * this.density;
                    const directionY = forceDirectionY * force * this.density;

                    // Push outward
                    this.x -= directionX;
                    this.y -= directionY;
                }}
            }}

            // Move particle
            this.x += this.directionX;
            this.y += this.directionY;

            // Draw
            this.draw();
        }}
    }}

    // Initialize particle array
    function init() {{
        particlesArray = [];
        // Calculate amount of particles based on screen area (density logic)
        let numberOfParticles = (canvas.width * canvas.height) / 9000;
        
        for (let i = 0; i < numberOfParticles; i++) {{
            let size = (Math.random() * 2) + 1; // Size between 1 and 3
            // Ensure particles spawn fully inside canvas
            let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
            let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
            
            // Random velocities
            let directionX = (Math.random() * 2) - 1;
            let directionY = (Math.random() * 2) - 1;
            
            let color = ACCENT_HEX;

            particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
        }}
    }}

    // Check distances and draw lines
    function connect() {{
        let opacityValue = 1;
        // Optimization: iterate from current particle onward (O(N^2 / 2))
        for (let a = 0; a < particlesArray.length; a++) {{
            for (let b = a; b < particlesArray.length; b++) {{
                let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) 
                             + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                
                // Comparing against squared distance avoids expensive Math.sqrt calls
                if (distance < (CONNECT_DISTANCE * CONNECT_DISTANCE)) {{
                    // Calculate opacity based on actual distance
                    opacityValue = 1 - (Math.sqrt(distance) / CONNECT_DISTANCE);
                    ctx.strokeStyle = `rgba(${{rgbAccent}}, ${{opacityValue}})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }}
            }}
        }}
    }}

    // Animation Loop
    function animate() {{
        // Respect prefers-reduced-motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particlesArray.length; i++) {{
            if (prefersReducedMotion) {{
                // Stop autonomous movement, but still draw and allow mouse interaction
                particlesArray[i].directionX = 0;
                particlesArray[i].directionY = 0;
            }}
            particlesArray[i].update();
        }}
        connect();
    }}

    // Boot
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
