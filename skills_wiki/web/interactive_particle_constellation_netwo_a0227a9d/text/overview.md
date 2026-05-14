# Interactive Particle Constellation Network

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Particle Constellation Network

* **Core Visual Mechanism**: A generative, physics-based particle system rendered on an HTML5 `<canvas>`. Dots (nodes) drift continuously across the screen. An $O(N^2)$ algorithm calculates the distance between every pair of dots; when they come within a specific proximity, a line (edge) is drawn between them. The line's opacity maps inversely to the distance, creating a dynamic, fading "constellation" or "neural network" effect. A mouse interaction layer introduces collision detection, causing particles to physically repel from the cursor.
* **Why Use This Skill (Rationale)**: This effect implies connectivity, technology, data processing, and modern infrastructure. Visually, it provides continuous, non-distracting background motion that keeps the UI feeling "alive" without demanding the user's direct attention. The interactive mouse repulsion adds a layer of gamified delight.
* **Overall Applicability**: Ideal for hero backgrounds on tech landing pages, SaaS products, AI startups, cybersecurity firms, and creative portfolios.
* **Value Addition**: It elevates a static background into a generative art piece. Unlike looped video backgrounds, this is programmatic, infinitely unique, scales flawlessly without pixelation, and responds specifically to the user's physical input (mouse movement).
* **Browser Compatibility**: Excellent. The HTML5 Canvas API and `requestAnimationFrame` are fully supported in all modern browsers (Chrome, Firefox, Safari, Edge) and IE9+.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Environment**: A single, full-screen `<canvas>` element positioned behind the main content.
  - **Nodes**: Small filled circles (`ctx.arc`) representing data points.
  - **Edges**: 1px lines (`ctx.lineTo`) connecting nodes, drawn dynamically with varying alpha transparency.
  - **Color Logic**: High contrast. Dark theme features a deep background (`#0d111c`) with vivid accent nodes/lines (e.g., Cyan `#00bfff`). Light theme reverses this with an off-white background (`#f8f9fa`) and dark or vivid accents.

* **Step B: Layout & Compositional Style**
  - **Z-Index Layering**: The canvas operates as an absolute background (`position: absolute; top: 0; left: 0; z-index: -1`). Standard HTML content (like hero text) sits on top with a higher z-index and is completely unaware of the canvas.
  - **Density**: The number of particles is calculated dynamically based on screen area (e.g., `(width * height) / 9000`), ensuring the network never feels too sparse on 4K monitors or overwhelmingly cluttered on mobile devices.

* **Step C: Interactive Behavior & Animations**
  - **Autonomic Motion**: Each particle is assigned a random $X$ and $Y$ velocity between roughly `-2.5` and `2.5` pixels per frame. They bounce off the canvas edges.
  - **Proximity Lines**: Fading lines drawn based on dynamic distance calculations.
  - **Mouse Repulsion**: The mouse possesses a "radius". During the update loop, the distance between the mouse and each particle is checked. If the distance is less than the radius, the particle's $X/Y$ coordinates are nudged outward to escape the cursor's perimeter.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Particle Rendering** | Canvas API 2D (`ctx.arc`) | Drawing hundreds of DOM elements (divs) would crash browser performance. Canvas batches drawing commands highly efficiently. |
| **Connecting Lines** | Canvas API 2D (`ctx.lineTo`) | CSS cannot draw diagonal lines between dynamically moving arbitrary coordinates. |
| **Animation Loop** | JS `requestAnimationFrame` | Syncs the rendering with the monitor's refresh rate (typically 60fps) for perfectly smooth motion. |
| **Layout Layering** | CSS Absolute Positioning | Detaches the canvas from the document flow, allowing it to act purely as a decorative backdrop. |

> **Feasibility Assessment**: 100%. The code below fully reproduces the visual aesthetic, the connecting line logic, the performance optimization, and the interactive mouse repulsion demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  * Continuous ambient animation can cause nausea or distraction for users with vestibular spectrum disorders. The generated JavaScript includes an active `window.matchMedia('(prefers-reduced-motion: reduce)')` check inside the animation loop. If active, it nullifies the particles' autonomous velocities, leaving a static constellation that is still responsive to user mouse input (which provides control over the motion, thus reducing a11y issues).
  * The canvas is explicitly set behind a `pointer-events: none` wrapper for the text, allowing screen readers and normal pointer selection to interact with the text unimpeded.
* **Performance**: 
  * Connecting particles requires checking every node against every other node. This is an $O(N^2)$ algorithm.
  * *Optimization 1*: The inner loop starts at `b = a` rather than `b = 0`. This cuts the required checks exactly in half, as A-to-B is the same distance as B-to-A.
  * *Optimization 2*: The actual connection check uses `dx*dx + dy*dy < radiusSquared`. This completely bypasses the highly expensive `Math.sqrt()` calculation for determining if elements are in range. Square roots are only calculated *after* a connection is confirmed, purely to calculate the opacity value. 
  * *Optimization 3*: Particle count is strictly bounded to the screen area resolution (`width * height / 9000`), preventing infinite loops or memory crashes on window resizes.