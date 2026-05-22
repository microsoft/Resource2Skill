# Pure CSS Translucent 3D Cube

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Translucent 3D Cube

* **Core Visual Mechanism**: A geometrically perfect, rotating 3D cube constructed entirely with DOM elements. It uses the CSS `perspective` property on a parent container to establish a 3D camera viewpoint, `transform-style: preserve-3d` to allow children to live in the 3D space, and mathematically offset `transform: rotate() translateZ()` rules to stitch six `<div>` elements into a box. The aesthetic signature is the semi-transparent neon faces with crisp, glowing borders overlapping to create genuine optical depth.
* **Why Use This Skill (Rationale)**: Native CSS 3D transforms allow for lightweight, highly performant spatial models without the massive overhead, bundling requirements, or learning curve of WebGL/Three.js. It integrates perfectly with standard web layouts, meaning text inside the cube is selectable, indexable, and accessible.
* **Overall Applicability**: Excellent for technical portfolio hero sections, SaaS landing pages emphasizing "building blocks" or "infrastructure", loading spinners, or interactive educational components demonstrating spatial geometry.
* **Value Addition**: Transforms a flat 2D screen into a dimensional stage. It grabs user attention immediately through motion and depth, breaking the standard grid-based web layout paradigm.
* **Browser Compatibility**: Broadly supported across all modern browsers (Chrome, Firefox, Safari, Edge). The `-webkit-` prefix is mostly obsolete for these properties, but `preserve-3d` is natively supported across the board.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent scene `.scene` (the camera), a `.cube` container (the object), and six child `.face` elements.
  - **Color Logic**: Hacker/terminal aesthetic.
    - Background: Deep slate/navy `#0d111c`
    - Accent: Neon mint green `#4ade80` (or varying teals).
    - Faces use a clever trick: a solid `border: 2px solid var(--accent)` combined with a `::before` pseudo-element that has `opacity: 0.25` and `background: var(--accent)`. This guarantees crisp edges but allows translucent overlapping.
  - **Typography**: Monospace or clean sans-serif (e.g., `'Inter', monospace`).

* **Step B: Layout & Compositional Style**
  - **Perspective**: `perspective: 1000px` applied to `.scene`. This defines the distance of the camera from the Z=0 plane.
  - **Centering**: Grid or Flexbox on the body/wrapper to dead-center the scene.
  - **Face Stitching**: Each face is absolutely positioned (`inset: 0`) and rotated to face outward (`rotateY(90deg)`, `rotateX(90deg)`, etc.), then pushed outward by exactly half the cube's width using `translateZ(calc(var(--cube-size) / 2))`.

* **Step C: Interactive Behavior & Animations**
  - **Continuous Rotation**: Driven by a CSS `@keyframes` animation rotating the `.cube` container from `0deg` to `360deg` on X and Y axes simultaneously (`transform: rotateX(...) rotateY(...)`).
  - **Timing**: Linear timing function (`animation: spin 20s infinite linear`) prevents the speed-up/slow-down effect, maintaining the illusion of a constantly spinning physical object.
  - **JS Enhancement**: Pausing the animation on hover, or mapping mouse movement to adjust the perspective.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Rendering context** | CSS `perspective` | Establishes the viewport depth (the "camera") natively in the browser. |
| **Object dimensionality** | CSS `preserve-3d` | Allows child elements to stack in 3D space rather than flattening to the parent's 2D plane. |
| **Face Assembly** | CSS `transform: rotate` & `translateZ` | Pushes flat DOM nodes outward from the center to construct the geometric shape. |
| **Translucency** | CSS `opacity` on inner pseudo-elements | Keeps the text/borders solid and vibrant while making the face backgrounds sheer, mimicking the tutorial's aesthetic. |
| **Rotation** | CSS `@keyframes` | GPU-accelerated infinite linear animation. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "On Writing Code",
    body_text: str = "Understanding perspective and 3D transforms.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Translucent 3D Cube.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f8f9fa"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # CSS
    css = f"""/* CSS 3D Cube Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --cube-size: 240px; /* Size of the 3D Cube */
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Space Mono', 'Inter', monospace, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.header {{
    position: absolute;
    top: 10%;
    left: 10%;
    z-index: 10;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}}

.header p {{
    font-size: 1rem;
    opacity: 0.7;
    font-family: 'Inter', sans-serif;
}}

/* 3D Scene setup */
.scene {{
    width: var(--cube-size);
    height: var(--cube-size);
    perspective: 1000px; /* The 'Camera' distance */
    margin: auto;
}}

/* The Cube container */
.cube {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transform: translateZ(calc(var(--cube-size) * -0.5));
    animation: spin 20s infinite linear;
    transition: transform 0.2s ease-out;
}}

/* Pause animation when user hovers */
.scene:hover .cube {{
    animation-play-state: paused;
}}

/* Core Face Styles */
.face {{
    position: absolute;
    width: var(--cube-size);
    height: var(--cube-size);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--accent);
    /* Soft glowing box-shadow for depth */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.4) inset;
}}

/* Pseudo-element for translucent background to keep borders solid */
.face::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-color: var(--accent);
    opacity: 0.15;
    z-index: -1;
}}

/* Positioning the 6 faces in 3D Space */
.front  {{ transform: rotateY(  0deg) translateZ(calc(var(--cube-size) / 2)); }}
.right  {{ transform: rotateY( 90deg) translateZ(calc(var(--cube-size) / 2)); }}
.back   {{ transform: rotateY(180deg) translateZ(calc(var(--cube-size) / 2)); }}
.left   {{ transform: rotateY(-90deg) translateZ(calc(var(--cube-size) / 2)); }}
.top    {{ transform: rotateX( 90deg) translateZ(calc(var(--cube-size) / 2)); }}
.bottom {{ transform: rotateX(-90deg) translateZ(calc(var(--cube-size) / 2)); }}

/* Distinct opacity/color variations for aesthetics */
.front::before  {{ opacity: 0.25; }}
.right::before  {{ opacity: 0.15; }}
.back::before   {{ opacity: 0.10; }}
.left::before   {{ opacity: 0.20; }}
.top::before    {{ opacity: 0.30; }}
.bottom::before {{ opacity: 0.05; }}

/* Keyframes for continuous multidirectional rotation */
@keyframes spin {{
    0% {{
        transform: translateZ(calc(var(--cube-size) * -0.5)) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    100% {{
        transform: translateZ(calc(var(--cube-size) * -0.5)) rotateX(360deg) rotateY(720deg) rotateZ(180deg);
    }}
}}

/* Responsive scaling */
@media (max-width: 600px) {{
    :root {{
        --cube-size: 150px;
    }}
    .header {{ top: 5%; left: 5%; }}
    .header h1 {{ font-size: 1.8rem; }}
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="scene">
            <div class="cube" id="cube">
                <div class="face front">Front</div>
                <div class="face back">Back</div>
                <div class="face right">Right</div>
                <div class="face left">Left</div>
                <div class="face top">Top</div>
                <div class="face bottom">Bottom</div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS (Adding subtle interactive mouse tracking to the scene's perspective origin)
    js = f"""// Interactive 3D enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const scene = document.querySelector('.scene');
    
    // Smoothly alter the perspective origin based on mouse movement
    // This makes the 3D effect feel much more physical and reactive
    container.addEventListener('mousemove', (e) => {{
        const x = e.clientX;
        const y = e.clientY;
        
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        // Calculate offset percentage (from 20% to 80%)
        const percentX = ((x - centerX) / centerX) * 50 + 50;
        const percentY = ((y - centerY) / centerY) * 50 + 50;
        
        scene.style.perspectiveOrigin = `${{percentX}}% ${{percentY}}%`;
    }});
    
    // Reset on mouse leave
    container.addEventListener('mouseleave', () => {{
        scene.style.perspectiveOrigin = '50% 50%';
        scene.style.transition = 'perspective-origin 1s ease-out';
    }});
    
    container.addEventListener('mouseenter', () => {{
        scene.style.transition = 'perspective-origin 0.1s ease-out';
    }});
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - Text inside the `.face` elements is naturally readable by screen readers, which is a massive advantage over canvas-based 3D approaches. 
  - For production, if the animation causes motion sickness, you should respect the user's OS-level motion preferences by wrapping the keyframe assignment in `@media (prefers-reduced-motion: reduce) { .cube { animation: none; transform: rotateX(-30deg) rotateY(-45deg); } }`.
* **Performance**: 
  - 3D transforms (`rotateX`, `rotateY`, `translateZ`) map beautifully to hardware (GPU) compositing layers. This avoids reflowing or repainting the DOM grid on every frame. 
  - The JS mousemove event is purely additive (adjusting `perspective-origin`); if execution slows down, the core CSS animation will remain unblocked and fluid. To micro-optimize, the `mousemove` handler could be wrapped in a `requestAnimationFrame` throttle.