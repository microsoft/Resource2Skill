# Interactive Canvas Dot Polygon

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Canvas Dot Polygon

* **Core Visual Mechanism**: This technique uses the HTML5 Canvas API and trigonometry (polar coordinates) to plot points evenly distributed around a center origin. Instead of drawing lines to connect these vertices into a solid shape, it renders standalone circles (dots) at each coordinate. The entire system is hooked into a `requestAnimationFrame` loop and pointer events, creating a mesmerizing, rotating geometric formation that spins based on user interaction (drag/swipe).
* **Why Use This Skill (Rationale)**: Drawing DOM elements (like `<div>` tags) in a circle requires complex CSS positioning and can suffer from performance issues during rapid rotation. The Canvas API allows for immediate-mode rendering of mathematical shapes at a smooth 60fps. The interaction physics (dragging to spin) provides high tactile satisfaction.
* **Overall Applicability**: Excellent for interactive loading screens, creative portfolio hero backgrounds, web-based data visualizations, or interactive branding elements.
* **Value Addition**: Transforms a static page into an interactive, physics-based environment. It demonstrates high technical proficiency by utilizing mathematics (Sine/Cosine for vertex plotting) to drive visual UI elements.
* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard HTML5 `<canvas>`, `requestAnimationFrame`, and modern ES6 JS syntax. No external libraries are required.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML**: A single `<canvas>` element occupying the designated space.
  - **Color Logic**: Uses a base background (e.g., dark `#0d111c` or light `#f8f9fa`) and an array of colors or a single accent color for the dots. The video eventually maps distinct colors to different dots.
  - **Graphics**: Pure mathematical rendering using `ctx.arc(x, y, radius, 0, Math.PI * 2)` to draw perfect circles.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Absolute positioning of the canvas to fill the container.
  - **Spatial Feel**: The polygon is perfectly centered. This is achieved by translating the canvas context origin to `(width / 2, height / 2)` before drawing.
  - **Device Pixel Ratio**: The technique accounts for Retina/High-DPI displays by scaling the canvas internal resolution by `window.devicePixelRatio` while keeping the CSS dimensions standard.

* **Step C: Interactive Behavior & Animations**
  - **Animation Loop**: Driven by `window.requestAnimationFrame`.
  - **Trigonometry**: The angle between dots is calculated as `(Math.PI * 2) / number_of_sides`. Each dot's X and Y are found using `radius * Math.cos(angle * i)` and `radius * Math.sin(angle * i)`.
  - **Interaction**: Mouse/Touch drag controls the rotational velocity. The delta of the X-axis pointer movement (`moveX`) is multiplied by a friction/speed coefficient (e.g., `0.008`) and added to the polygon's rotation property.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Drawing Area | HTML5 `<canvas>` | High-performance immediate-mode rendering, ideal for animating shapes frame-by-frame. |
| Circular Positioning | Trigonometry (JS Math) | `Math.sin` and `Math.cos` are the mathematically correct and performant way to plot polar coordinates. |
| Interactive Spinning | JS Pointer Events | Tracks mouse/touch drag (`pointerdown`, `pointermove`, `pointerup`) to calculate momentum for rotation. |
| Smooth Animation | `requestAnimationFrame` | Synchronizes rendering with the display refresh rate for fluid 60fps motion. |

> **Feasibility Assessment**: 100%. The provided code fully reproduces the final state of the video tutorial: a centered polygon made of dots that rotates and accelerates based on horizontal drag interactions.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Interactive Dot Polygon",
    body_text: str = "Drag horizontally to spin the shape.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#22c55e",     # Base accent color (will generate a palette from this)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Canvas Dot Polygon effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f3f4f6"
    else:
        bg_color = "#d9d4c7" # Matching the earthy tone from the video
        text_color = "#1f2937"

    # === CSS ===
    css = f"""/* Interactive Canvas Dot Polygon */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #f0f0f0; /* Page background */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    color: var(--text-color);
}}

.wrapper {{
    text-align: center;
    margin-bottom: 20px;
}}

h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: #111;
}}

p {{
    font-size: 0.9rem;
    color: #555;
}}

.canvas-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background-color: var(--bg-color);
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    touch-action: none; /* Prevent scrolling while dragging on mobile */
    cursor: grab;
}}

.canvas-container:active {{
    cursor: grabbing;
}}

canvas {{
    display: block;
    width: 100%;
    height: 100%;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    
    <div class="canvas-container">
        <canvas id="stage"></canvas>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Canvas Dot Polygon
const PI2 = Math.PI * 2;

class Polygon {{
    constructor(x, y, radius, sides, baseColor) {{
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.sides = sides;
        this.rotate = 0;
        
        // Generate a palette around the base color for the dots
        this.colors = this.generatePalette(baseColor, sides);
    }}

    generatePalette(baseHex, count) {{
        const colors = [];
        // Extract RGB from hex
        let r = parseInt(baseHex.slice(1, 3), 16);
        let g = parseInt(baseHex.slice(3, 5), 16);
        let b = parseInt(baseHex.slice(5, 7), 16);
        
        for(let i = 0; i < count; i++) {{
            // Shift hues slightly for variation
            let shiftedR = (r + i * 15) % 255;
            let shiftedG = (g + i * 10) % 255;
            let shiftedB = (b + i * 20) % 255;
            colors.push(`rgb(${{shiftedR}}, ${{shiftedG}}, ${{shiftedB}})`);
        }}
        return colors;
    }}

    animate(ctx, moveX) {{
        ctx.save();
        
        const angle = PI2 / this.sides;
        
        // Translate to center
        ctx.translate(this.x, this.y);
        
        // Apply rotation based on user interaction momentum
        this.rotate += moveX * 0.005; 
        ctx.rotate(this.rotate);

        // Draw the dots
        for (let i = 0; i < this.sides; i++) {{
            const px = this.radius * Math.cos(angle * i);
            const py = this.radius * Math.sin(angle * i);

            ctx.beginPath();
            ctx.arc(px, py, 20, 0, PI2, false); // Dot radius is 20
            ctx.fillStyle = this.colors[i];
            ctx.fill();
            ctx.closePath();
        }}

        ctx.restore();
    }}
}}

class App {{
    constructor() {{
        this.canvas = document.getElementById('stage');
        this.ctx = this.canvas.getContext('2d');
        
        this.pixelRatio = window.devicePixelRatio > 1 ? 2 : 1;
        
        // Interaction State
        this.isDown = false;
        this.moveX = 0;
        this.offsetX = 0;
        this.momentum = 0.5; // Auto-spin base speed

        // Bind events
        window.addEventListener('resize', this.resize.bind(this), false);
        
        // Pointer events for drag-to-spin
        this.canvas.addEventListener('pointerdown', this.onDown.bind(this), false);
        this.canvas.addEventListener('pointermove', this.onMove.bind(this), false);
        window.addEventListener('pointerup', this.onUp.bind(this), false);

        this.resize();
        window.requestAnimationFrame(this.animate.bind(this));
    }}

    resize() {{
        this.stageWidth = this.canvas.parentElement.clientWidth;
        this.stageHeight = this.canvas.parentElement.clientHeight;

        // Account for Retina displays
        this.canvas.width = this.stageWidth * this.pixelRatio;
        this.canvas.height = this.stageHeight * this.pixelRatio;
        this.ctx.scale(this.pixelRatio, this.pixelRatio);

        // Re-initialize polygon on resize to keep it centered
        const radius = Math.min(this.stageWidth, this.stageHeight) * 0.35;
        this.polygon = new Polygon(
            this.stageWidth / 2, 
            this.stageHeight / 2, 
            radius, 
            12, // 12 sided polygon (12 dots)
            '{accent_color}'
        );
    }}

    animate() {{
        window.requestAnimationFrame(this.animate.bind(this));

        this.ctx.clearRect(0, 0, this.stageWidth, this.stageHeight);

        // Friction/Decay logic for momentum
        if (!this.isDown) {{
            // Slowly decay momentum towards a constant slow auto-spin (0.5)
            this.momentum += (0.5 - this.momentum) * 0.05;
        }}

        this.polygon.animate(this.ctx, this.momentum);
    }}

    onDown(e) {{
        this.isDown = true;
        this.moveX = 0;
        this.offsetX = e.clientX;
    }}

    onMove(e) {{
        if (this.isDown) {{
            // Calculate drag delta
            this.moveX = e.clientX - this.offsetX;
            this.offsetX = e.clientX;
            // Map drag to momentum
            this.momentum = this.moveX; 
        }}
    }}

    onUp(e) {{
        this.isDown = false;
    }}
}}

// Initialize App
window.onload = () => {{
    new App();
}};
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
  - HTML Canvas elements are inherently inaccessible to screen readers. If this component conveyed essential information, fallback content or `aria-label` attributes on the `<canvas>` would be required. In this context, it acts as a decorative element.
  - Users with `prefers-reduced-motion` settings might find constant rotation distracting. In a production environment, you should check `window.matchMedia('(prefers-reduced-motion: reduce)')` and set `this.momentum = 0` if true.
  - The `touch-action: none` CSS property prevents the browser from scrolling the page when the user touches the canvas, ensuring the drag gesture only affects the polygon.
* **Performance**: 
  - **Resolution Scaling**: The code utilizes `window.devicePixelRatio` to prevent the canvas from looking blurry on high-resolution (Retina) screens.
  - **Animation Frame**: The `requestAnimationFrame` API ensures the browser only runs the rendering math when the screen is actually refreshing, saving battery and CPU cycles.
  - **Immediate Mode Optimization**: Clearing the canvas with `clearRect` and redrawing is highly optimized in modern browsers compared to manipulating the rotation of 12 distinct DOM nodes via CSS on every frame.