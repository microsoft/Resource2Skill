# Interactive Polygon Mesh Background

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Polygon Mesh Background

* **Core Visual Mechanism**: A dynamic, web-like constellation effect rendered on an HTML5 Canvas. Floating nodes (particles) drift slowly across the screen, and lines are dynamically drawn between them when they come within a specific proximity threshold. The opacity of the connecting lines is inversely proportional to the distance between nodes, creating a breathing, elastic mesh effect.
* **Why Use This Skill (Rationale)**: This pattern transforms a static background into a living, high-tech environment. It provides subtle continuous motion that catches the eye without distracting from the foreground content. It visually communicates concepts like connectivity, networking, data, AI, and modern technology.
* **Overall Applicability**: Ideal for hero sections on tech company landing pages, SaaS product websites, Web3/crypto projects, data visualization dashboards, or digital agency portfolios.
* **Value Addition**: Replaces heavy background videos or static images with a lightweight, mathematically generated animation that scales perfectly to any resolution and adds a layer of interactivity (as particles can react to the cursor).
* **Browser Compatibility**: Excellent. Requires standard HTML5 Canvas and `requestAnimationFrame`, which are supported in all modern browsers (Chrome, Firefox, Safari, Edge) for over a decade.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Canvas Element**: A `<canvas>` stretching 100% of its container acts as the rendering surface.
  - **Color Logic**:
    - *Dark Mode*: Deep charcoal/black background (e.g., `#0f0f11`) with semi-transparent white or cyan nodes/lines.
    - *Light Mode*: Off-white/light gray background (e.g., `#f4f4f9`) with dark gray or primary brand color nodes/lines.
    - *Accent*: The lines and nodes take on the `accent_color`, utilizing Canvas `globalAlpha` to manage fading based on distance.
  - **Typography**: Foreground text overlaid on the canvas uses a clean, modern sans-serif (like Inter) with high contrast to ensure readability against the moving lines.

* **Step B: Layout & Compositional Style**
  - **Layering System**:
    - Base layer: `div.container` with the background color.
    - Middle layer: `canvas` positioned absolutely to fill the container (`inset: 0`, `z-index: 1`).
    - Top layer: `div.content` positioned absolutely in the center using Flexbox or Transform (`z-index: 10`, `pointer-events: none` to let mouse events pass through to the canvas if needed).

* **Step C: Interactive Behavior & Animations**
  - **Particle Motion**: Nodes are assigned random sub-pixel velocities (e.g., between -0.5 and 0.5 pixels per frame) upon creation.
  - **Boundary Collision**: When a particle hits the edge of the canvas, its velocity vector is inverted, causing it to "bounce."
  - **Proximity Calculation**: Every frame, the Pythagorean theorem ($a^2 + b^2 = c^2$) calculates the distance between every pair of particles.
  - **Alpha Fading**: Opacity = $1 - (\text{distance} / \text{threshold})$. As particles drift apart, the line connecting them smoothly fades out.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

While the original tutorial utilized a specific, dated jQuery plugin (`polygonizr.js`), building this effect in **Vanilla JavaScript with the Canvas API** is the modern best practice. It eliminates external dependencies, drastically improves performance, and guarantees long-term stability.

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Particle rendering | HTML5 Canvas API | High performance for drawing hundreds of lines/circles per frame. DOM elements would cause severe lag. |
| Fluid Animation | `requestAnimationFrame` | Native browser API that syncs with screen refresh rate for smooth, tear-free motion. |
| Distance Calculation | JS Math (`Math.hypot`) | Fast, native mathematical operations to compute vector distances every frame. |
| Overlay Layout | CSS Absolute Positioning | Ensures the canvas acts purely as a background without disrupting document flow. |

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - The canvas itself is purely decorative. The `pointer-events: none` on the text container ensures that if interactive elements (like buttons) are added later, they won't be blocked by the canvas layer.
  - The text is given a subtle `text-shadow` to ensure it maintains WCAG passing contrast ratios even if a dense cluster of bright particles happens to pass behind the letters.
* **Performance**:
  - **O(N^2) Complexity Mitigation**: The nested `for` loop in the `connect()` function compares every particle to every other particle. To prevent CPU spikes on large screens, the `numberOfParticles` is strictly capped (`if(numberOfParticles > 200) numberOfParticles = 200`).
  - **Math Optimization**: `Math.hypot(dx, dy)` is used as a slightly cleaner/optimized native method compared to manual `Math.sqrt`.
  - **Debounced Resize**: The `resize` event listener includes a basic debounce `setTimeout`. Continuously recreating the particle array while a user drags the window bounds causes heavy lag; the debounce ensures it only resets once the user stops resizing.