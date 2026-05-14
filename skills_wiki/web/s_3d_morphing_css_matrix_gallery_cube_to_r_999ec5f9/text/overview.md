# 3D Morphing CSS Matrix Gallery (Cube-to-Ring)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Morphing CSS Matrix Gallery (Cube-to-Ring)

* **Core Visual Mechanism**: This interaction relies purely on CSS 3D transforms (`rotateX`, `rotateY`, `translateZ`, `scale3d`) and structural DOM changes controlled by CSS classes. It takes 12 individual 2D HTML elements (panels) and positions them in 3D space. By toggling a parent class (`.cube` to `.ring`), the browser's rendering engine automatically interpolates the 3D matrices, creating a majestic, fluid morphing animation from a set of nested cubes into a large cylindrical ring. A continuous CSS keyframe animation (`spin`) revolves the entire structure, enhancing the depth perception.
* **Why Use This Skill (Rationale)**: Native CSS 3D transforms are hardware-accelerated (GPU) and highly performant. This technique allows for complex, spatial UI transitions without needing heavy WebGL libraries like Three.js. The ability to smoothly interpolate between entirely different 3D shapes creates a high-end, immersive "wow factor" that delights users and encourages interaction. 
* **Overall Applicability**: Ideal for interactive portfolios, product feature showcases (where each face highlights a feature), immersive hero sections on modern landing pages, or digital art galleries.
* **Browser Compatibility**: Requires modern browsers supporting `transform-style: preserve-3d`, 3D transforms, and transitions. Supported in all modern Chrome, Firefox, Safari, and Edge versions (minimum versions from ~2014+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A container (`.scene`) providing the camera's 3D perspective, a `.stage` (for static tilting), a `.shape` (for dynamic spinning), and 12 `.panel` elements (the actual visual faces).
  - **Color Logic**: A dramatic radial gradient background to draw focus to the center. For a dark theme, it fades from a dark inner color (`#1a1a24`) to a near-black outer color (`#09090d`). The panels themselves use `rgba(255,255,255,0.1)` backgrounds and rely on background images with differing opacities to simulate depth and glass-like layering.
  - **Typography**: Clean, sans-serif UI overlay using Google Fonts (Inter) with the primary title colored by the `accent_color`.

* **Step B: Layout & Compositional Style**
  - **Perspective**: The scene has `perspective: 1200px` to define the 3D vanishing point.
  - **Cube Math**: To form a perfect cube, faces are translated outward by exactly half their scaled size. Outer faces scale by `1.2`, inner faces scale by `0.8`. The `scale3d()` applies before `translateZ()`, properly scaling the distance from the center.
  - **Ring Math**: 12 faces form a full circle. $360^\circ / 12 = 30^\circ$ per face. To make 200px wide faces align into a smooth ring without massive overlap, a radius of `380px` (`translateZ(380px)`) is mathematically ideal.

* **Step C: Interactive Behavior & Animations**
  - **Continuous Spin**: The `.shape` wrapper revolves indefinitely on the Y-axis using a linear CSS animation: `@keyframes spin { to { transform: rotateY(-360deg); } }`.
  - **Morph Transition**: `transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 1.5s ease-in-out` on the panels ensures the movement between the cube state and the ring state feels smooth and physically grounded.
  - **Backface Toggling**: A JavaScript event listener adjusts the `backface-visibility` property, showing how CSS handles polygon culling in 3D space.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Rendering & Positioning** | CSS 3D Transforms | Native, performant, and exactly replicates the tutorial without needing Three.js or WebGL. |
| **Morphing Animation** | CSS Transitions | Interpolating `transform` matrices automatically produces the complex paths seen during the morph. |
| **Continuous Rotation** | CSS `@keyframes` | A simple linear animation on the parent element applies to all children while preserving their individual 3D offsets. |
| **State Management** | Vanilla JS | A simple script toggles parent classes and updates `backface-visibility`, avoiding heavy framework overhead. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "The Morphing Cube",
    body_text: str = "A 3D CSS animation that transforms 12 image panels between nested cubes and a continuous rotating ring. Toggle the shape or visibility below.",
    color_scheme: str = "dark",
    accent_color: str = "#ff3366",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Morphing CSS Cube-to-Ring effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_inner = "#1a1a24"
        bg_outer = "#09090d"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        btn_text = "#000"
    else:
        bg_inner = "#ffffff"
        bg_outer = "#d0d4dc"
        text_color = "#1a1a2e"
        surface_color = "rgba(255, 255, 255, 0.6)"
        btn_text = "#fff"

    # Generate CSS transform rules mathematically
    css_cube_rules = ""
    rotations = [
        "rotateY(0deg)",    # Front
        "rotateY(90deg)",   # Right
        "rotateY(180deg)",  # Back
        "rotateY(270deg)",  # Left
        "rotateX(90deg)",   # Top
        "rotateX(-90deg)"   # Bottom
    ]
    
    # Faces 1-6: Outer Cube (transparent, scaled up)
    for i in range(1, 7):
        css_cube_rules += f"        .shape.cube .p{i} {{ transform: scale3d(1.2, 1.2, 1.2) {rotations[i-1]} translateZ(100px); opacity: 0.5; }}\n"
    
    # Faces 7-12: Inner Cube (more opaque, scaled down)
    for i in range(7, 13):
        css_cube_rules += f"        .shape.cube .p{i} {{ transform: scale3d(0.8, 0.8, 0.8) {rotations[i-7]} translateZ(100px); opacity: 0.95; }}\n"

    # Faces 1-12: Ring Mode (12-sided cylinder)
    css_ring_rules = ""
    for i in range(1, 13):
        angle = (i - 1) * 30
        css_ring_rules += f"        .shape.ring .p{i} {{ transform: rotateY({angle}deg) translateZ(380px); opacity: 0.85; }}\n"

    # Generate HTML panels
    html_panels = ""
    for i in range(1, 13):
        html_panels += f'                <div class="panel p{i}" style="background-image: url(\'https://picsum.photos/seed/morph{i}/400/400\');"><span>{i}</span></div>\n'

    css = f"""/* 3D Morphing CSS Matrix Gallery */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-inner: {bg_inner};
    --bg-outer: {bg_outer};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at center, var(--bg-inner) 0%, var(--bg-outer) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* === UI Overlay === */
.controls {{
    position: absolute;
    top: 32px;
    left: 32px;
    z-index: 100;
    max-width: 320px;
    background: var(--surface);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 24px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}}

.title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--accent);
    letter-spacing: -0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    margin-bottom: 24px;
    opacity: 0.85;
    line-height: 1.5;
}}

button {{
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    padding: 12px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 1rem;
    transition: transform 0.2s, filter 0.2s;
    width: 100%;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}

button:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

button:active {{
    transform: translateY(1px);
}}

.checkbox-label {{
    display: flex;
    align-items: center;
    font-size: 0.95rem;
    cursor: pointer;
    gap: 10px;
    user-select: none;
}}

input[type="checkbox"] {{
    accent-color: var(--accent);
    width: 18px;
    height: 18px;
}}

/* === 3D Scene Elements === */
.scene {{
    perspective: 1200px;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.stage {{
    transform-style: preserve-3d;
    transform: rotateX(-10deg); /* Slight downward tilt to view depth better */
}}

.shape {{
    position: relative;
    width: 200px;
    height: 200px;
    transform-style: preserve-3d;
    animation: spin 24s infinite linear;
}}

@keyframes spin {{
    0% {{ transform: rotateY(0deg); }}
    100% {{ transform: rotateY(-360deg); }}
}}

.panel {{
    position: absolute;
    width: 200px;
    height: 200px;
    background-size: cover;
    background-position: center;
    border: 3px solid var(--accent);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.6) inset;
    transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 1.5s ease-in-out;
    display: flex;
    align-items: center;
    justify-content: center;
    backface-visibility: visible;
}}

.panel span {{
    font-size: 4rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 4px 10px rgba(0,0,0,0.8), 0 0 20px var(--accent);
    pointer-events: none;
}}

/* State 1: Nested Cubes */
{css_cube_rules}
/* State 2: 12-Sided Ring */
{css_ring_rules}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {{
    .shape {{ animation: none; }}
    .panel {{ transition: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- Controls Overlay -->
        <div class="controls">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <button id="toggleBtn">Toggle Shape</button>
            <label class="checkbox-label">
                <input type="checkbox" id="backfaceBtn" checked> Backfaces Visible
            </label>
        </div>

        <!-- 3D Environment -->
        <div class="scene">
            <div class="stage">
                <!-- Class toggles between "cube" and "ring" -->
                <div class="shape cube" id="shape">
{html_panels}                </div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction Logic for Morphing Cube
document.addEventListener('DOMContentLoaded', () => {
    const shape = document.getElementById('shape');
    const toggleBtn = document.getElementById('toggleBtn');
    const backfaceBtn = document.getElementById('backfaceBtn');
    const panels = document.querySelectorAll('.panel');

    // Toggle between nested cubes and ring configurations
    toggleBtn.addEventListener('click', () => {
        if (shape.classList.contains('cube')) {
            shape.classList.replace('cube', 'ring');
        } else {
            shape.classList.replace('ring', 'cube');
        }
    });

    // Toggle CSS backface-visibility
    backfaceBtn.addEventListener('change', (e) => {
        const isVisible = e.target.checked;
        panels.forEach(panel => {
            panel.style.backfaceVisibility = isVisible ? 'visible' : 'hidden';
        });
    });
});
"""

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

#### 3c. Verification Checklist
- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs? (Picsum photos, Google Fonts).
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to buttons and borders?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (The multi-stage cube and large expanded ring).

### 4. Accessibility & Performance Notes

* **Accessibility**: The CSS includes a media query for `@media (prefers-reduced-motion: reduce)`. This turns off the infinite spinning animation and disables the complex CSS morph transitions, as rotating 3D environments can cause vestibular issues or motion sickness for some users.
* **Performance**: 
  - CSS 3D transforms (`scale3d`, `translateZ`) and `opacity` are fully hardware-accelerated. The GPU handles the matrix interpolation natively, making this component remarkably lightweight compared to achieving the same visual via JS frame calculation.
  - Using `backdrop-filter` in the `.controls` class can be heavy on some older GPUs, but separating it from the 3D `.scene` stacking context prevents overlapping redraw performance penalties.