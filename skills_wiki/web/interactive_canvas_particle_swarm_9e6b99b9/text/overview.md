# Interactive Canvas Particle Swarm

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Canvas Particle Swarm

* **Core Visual Mechanism**: A generative, physics-based particle system rendered on an HTML5 `<canvas>`. Hundreds of geometric shapes (circles or squares) float independently, bouncing off the container's boundaries. The defining visual signature is **proximity-based scaling**: as the user's cursor moves through the canvas, particles within a specific radius rapidly scale up in size, creating an organic, magnetic swelling effect, before gracefully shrinking back to their original dimensions when the cursor leaves.
* **Why Use This Skill (Rationale)**: This pattern transforms a static background into a playful, highly responsive environment. It leverages "micro-interactions" that reward user movement, drawing attention and creating a sense of depth and fluidity without distracting from foreground content. It breaks the rigid grid of standard web layouts.
* **Overall Applicability**: Ideal for hero sections on tech/SaaS landing pages, creative portfolios, "404 Not Found" pages, or immersive loading screens. It works best behind bold, centered typography.
* **Value Addition**: Compared to a static image or a looping CSS background, a Canvas particle system provides infinite, non-repeating variations and direct real-time interactivity. It demonstrates high technical polish and creates a memorable "tactile" feel on the web.
* **Browser Compatibility**: Excellent. The HTML5 Canvas 2D rendering context and `requestAnimationFrame` are supported in all modern browsers (Chrome 9+, Safari 5.1+, Firefox 4+, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Elements**: A single `<canvas>` element layered behind standard HTML text elements using absolute positioning.
  - **Color Logic**: A dark, deep background (e.g., `#0a0b10`) populated by particles of varied, vibrant colors. The palette relies on contrasting hues (cyans, magentas, yellows) against the dark void.
  - **Typographic Hierarchy**: Centered, high-contrast foreground text. Sans-serif (like *Inter*), heavy weights for the title (700) to ensure readability against the moving background.
  - **CSS Properties**: Minimal CSS is required for the visual effect itself; CSS merely layers the text (`z-index: 10`, `pointer-events: none`) over the canvas.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The container handles sizing, while the `<canvas>` spans 100% of the container's width and height. Foreground content is centered using standard absolute positioning (`top: 50%; left: 50%; transform: translate(-50%, -50%)`).
  - **Density strategy**: The number of particles should scale with the area of the container to maintain a consistent density (e.g., 1 particle per 4,000 square pixels) rather than a hardcoded number.

* **Step C: Interactive Behavior & Animations**
  - **Animation Loop**: Powered entirely by JavaScript's `requestAnimationFrame`. The canvas is cleared and redrawn 60 times per second.
  - **Physics**: Each particle has independent `x/y` coordinates and `dx/dy` velocities. On every frame, position is incremented by velocity. If a particle hits the canvas boundary, its velocity vector is inverted (bounce).
  - **Interaction**: A `mousemove` listener tracks cursor coordinates relative to the canvas. On every frame, the distance between the cursor and each particle is calculated using the Pythagorean theorem (`Math.hypot`). If the distance is less than a threshold (e.g., 50px), the particle's radius increases up to a maximum limit. Otherwise, it shrinks back to its minimum base radius.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Particle Rendering** | HTML5 `<canvas>` API | CSS DOM elements (like 500 individual `<div>`s) would cause severe layout thrashing and performance drops. Canvas is optimized for drawing hundreds of moving shapes. |
| **Animation Loop** | JS `requestAnimationFrame` | Provides hardware-accelerated, 60fps rendering synchronized with the monitor's refresh rate. |
| **Interaction Logic** | JS Math / Proximity checking | Requires calculating Euclidean distance per-frame based on real-time mouse coordinates, which is impossible in pure CSS. |
| **Foreground Text** | CSS Absolute Positioning | Layering DOM elements over the canvas allows text to remain selectable and accessible, while `pointer-events: none` lets mouse events pass through to the canvas beneath. |

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - The foreground text lives in standard DOM elements, so it is fully readable by screen readers. 
  - `pointer-events: none` on the text overlay ensures that the user's cursor can interact smoothly with the canvas underneath without the text bounding boxes creating "dead zones".
  - *Recommendation*: For users with vestibular disorders, motion should ideally be disabled. A `prefers-reduced-motion` media query could be tied to JavaScript via `window.matchMedia('(prefers-reduced-motion: reduce)')` to pause the `requestAnimationFrame` loop.
* **Performance**: 
  - The code uses `requestAnimationFrame`, which is highly performant and pauses rendering automatically if the user switches browser tabs, saving battery and CPU.
  - Particle density is calculated mathematically relative to the container's surface area (`area / 5000`). This ensures mobile screens aren't choked by 800 particles, while a massive 4K monitor won't look too sparse.
  - The Euclidean distance calculation (`Math.hypot`) is performed per-particle, per-frame. For < 500 particles, this is easily handled by modern JS engines. However, pushing the density calculation to `area / 1000` (creating thousands of particles) would cause frame drops. Avoid exceedingly high particle counts without switching to an instanced WebGL approach.