# Interactive 3D CSS Transform Explorer

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive 3D CSS Transform Explorer

* **Core Visual Mechanism**: The defining visual mechanism is the projection of a 2D DOM element into 3D space using the CSS `transform` functions: `rotateX()`, `rotateY()`, and `rotateZ()`. By coupling these transforms with a parent container that has a defined `perspective`, the browser calculates foreshortening, giving the element a realistic sense of depth and physical presence as it spins.

* **Why Use This Skill (Rationale)**: Native CSS 3D transforms allow web developers to create physical, spatial interfaces without the heavy overhead of WebGL or Canvas libraries. Rotating elements along the X, Y, and Z axes adds a tactile layer of interactivity that makes UI elements feel like real-world objects, improving engagement and delight.

* **Overall Applicability**: This technique is foundational for building "flip cards" (flipping on `rotateY`), premium interactive product showcases, dynamic hero sections, complex spatial navigation menus, and educational data visualizations. 

* **Value Addition**: It elevates a flat, static layout into an interactive, spatial dimension. Instead of objects simply appearing or fading in, they can unfold, swing, or flip into view.

* **Browser Compatibility**: CSS 3D Transforms (`rotateX/Y/Z` and `perspective`) have near-universal support across modern browsers (Chrome, Firefox, Safari, Edge).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent `.scene` container establishes the 3D space, and a child `.target-box` acts as the object being manipulated. Standard form `<input type="range">` elements are used as controls.
  - **Color Logic**: A high-contrast theme. In dark mode, a deep background (`#0f172a`) with a bright accent (e.g., `#e11d48`) makes the 3D object pop. Gridlines in the scene background (`rgba(255,255,255,0.1)`) help visualize the rotation in space.
  - **Typography**: Clean, system-level sans-serif fonts for the controls, with clear data readouts for the degree values.
  - **Key CSS Properties**: 
    - `perspective: 800px;` (on the parent, creates depth)
    - `transform-style: preserve-3d;` (ensures child elements behave as 3D objects)
    - `transform: rotateX(...) rotateY(...) rotateZ(...)` (the actual manipulation)
    - `transition: transform 0.1s ease-out;` (smooths out rapid slider movements)

* **Step B: Layout & Compositional Style**
  - Uses CSS Flexbox to split the layout into two main areas: the 3D viewport (left) and the control panel (right).
  - The 3D viewport uses a center-aligned flex layout so the object rotates around the absolute center of the view.

* **Step C: Interactive Behavior & Animations**
  - JavaScript listens to the `input` event on three range sliders (mapped to X, Y, and Z axes).
  - As the sliders move, JS dynamically updates the inline `transform` CSS property of the target box.
  - A small transition duration (`0.1s`) creates a fluid, interpolated movement feeling, mirroring a smooth 3D engine.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| 3D Object Rotation | CSS `transform: rotate*()` | Native CSS is highly performant and exactly replicates the tutorial's core concept. |
| Depth Perception | CSS `perspective` | Without it, `rotateX` and `rotateY` just look like the element is being squished. `perspective` adds true 3D foreshortening. |
| Interactivity | JS Event Listeners | Binding range sliders to CSS transforms allows the user to intuitively understand how each axis works. |
| Smooth interpolation | CSS `transition` | Prevents jagged movements when sliding the controls quickly. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS 3D Transform Playground",
    body_text: str = "Manipulate the sliders to rotate the element across the X, Y, and Z axes in 3D space.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e11d48",     # CSS hex color for accent (e.g., red)
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS 3D Transform visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "#1e293b"
        border_color = "#334155"
        grid_color = "rgba(255, 255, 255, 0.05)"
        text_muted = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "#cbd5e1"
        grid_color = "rgba(0, 0, 0, 0.05)"
        text_muted = "#64748b"

    # === CSS ===
    css = f"""/* CSS 3D Transform Explorer */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --grid: {grid_color};
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
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 95vw;
    max-height: 95vh;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.header {{
    padding: 24px 32px;
    border-bottom: 1px solid var(--border);
}}

.header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.header p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

.workspace {{
    display: flex;
    flex: 1;
    overflow: hidden;
}}

/* 3D Scene Viewport */
.scene-container {{
    flex: 3;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: 
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center;
    border-right: 1px solid var(--border);
    position: relative;
}}

.scene {{
    /* This is the magic property that gives the 3D space depth */
    perspective: 800px;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.target-object {{
    width: 220px;
    height: 280px;
    background: linear-gradient(135deg, var(--accent) 0%, rgba(255,255,255,0.2) 100%);
    background-color: var(--accent);
    color: #ffffff;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3), inset 0 0 0 1px rgba(255,255,255,0.2);
    /* Ensure smooth transitions when dragging sliders */
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
    padding: 20px;
}}

.target-object p {{
    font-size: 0.85rem;
    font-weight: 400;
    margin-top: 12px;
    opacity: 0.9;
}}

/* Controls Panel */
.controls-container {{
    flex: 2;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    background: var(--surface);
    overflow-y: auto;
}}

.control-group {{
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.control-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.95rem;
    font-weight: 500;
}}

.val-badge {{
    background: var(--bg);
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    font-family: monospace;
    font-size: 0.85rem;
    min-width: 65px;
    text-align: right;
}}

/* Custom Range Slider */
input[type=range] {{
    -webkit-appearance: none;
    width: 100%;
    background: transparent;
}}

input[type=range]:focus {{
    outline: none;
}}

input[type=range]::-webkit-slider-thumb {{
    -webkit-appearance: none;
    height: 20px;
    width: 20px;
    border-radius: 50%;
    background: var(--accent);
    cursor: grab;
    margin-top: -8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    transition: transform 0.1s;
}}

input[type=range]::-webkit-slider-thumb:active {{
    cursor: grabbing;
    transform: scale(1.1);
}}

input[type=range]::-webkit-slider-runnable-track {{
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: var(--border);
    border-radius: 2px;
}}

.btn-reset {{
    margin-top: auto;
    padding: 12px 20px;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}

.btn-reset:hover {{
    border-color: var(--text-muted);
    background: var(--border);
}}

@media (max-width: 768px) {{
    .workspace {{
        flex-direction: column;
    }}
    .scene-container {{
        border-right: none;
        border-bottom: 1px solid var(--border);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="workspace">
            <div class="scene-container">
                <div class="scene">
                    <div class="target-object" id="target-box">
                        <div>CSS 3D Object</div>
                        <p>Watch me rotate across multiple axes.</p>
                    </div>
                </div>
            </div>
            
            <div class="controls-container">
                <div class="control-group">
                    <div class="control-header">
                        <label for="x-slider">X-Axis (rotateX)</label>
                        <span class="val-badge" id="x-val">0deg</span>
                    </div>
                    <input type="range" id="x-slider" min="-360" max="360" value="0">
                </div>
                
                <div class="control-group">
                    <div class="control-header">
                        <label for="y-slider">Y-Axis (rotateY)</label>
                        <span class="val-badge" id="y-val">0deg</span>
                    </div>
                    <input type="range" id="y-slider" min="-360" max="360" value="0">
                </div>
                
                <div class="control-group">
                    <div class="control-header">
                        <label for="z-slider">Z-Axis (rotateZ)</label>
                        <span class="val-badge" id="z-val">0deg</span>
                    </div>
                    <input type="range" id="z-slider" min="-360" max="360" value="0">
                </div>

                <button class="btn-reset" id="btn-reset">Reset Transformations</button>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const targetBox = document.getElementById('target-box');
    
    const sliders = {{
        x: document.getElementById('x-slider'),
        y: document.getElementById('y-slider'),
        z: document.getElementById('z-slider')
    }};
    
    const badges = {{
        x: document.getElementById('x-val'),
        y: document.getElementById('y-val'),
        z: document.getElementById('z-val')
    }};

    const btnReset = document.getElementById('btn-reset');

    function updateTransform() {{
        const x = sliders.x.value;
        const y = sliders.y.value;
        const z = sliders.z.value;
        
        // Apply 3D rotation based on slider values
        targetBox.style.transform = `rotateX(${{x}}deg) rotateY(${{y}}deg) rotateZ(${{z}}deg)`;
        
        // Update UI badges
        badges.x.textContent = `${{x}}deg`;
        badges.y.textContent = `${{y}}deg`;
        badges.z.textContent = `${{z}}deg`;
    }}

    // Bind event listeners to sliders
    Object.values(sliders).forEach(slider => {{
        slider.addEventListener('input', updateTransform);
    }});

    // Reset button functionality
    btnReset.addEventListener('click', () => {{
        sliders.x.value = 0;
        sliders.y.value = 0;
        sliders.z.value = 0;
        updateTransform();
    }});

    // Initial render
    updateTransform();
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
  - Standard HTML form `<input type="range">` elements are used, ensuring keyboard navigability (users can tab to the sliders and use arrow keys to adjust rotations).
  - Explicit `<label>` elements and `.control-header` bindings make it clear to screen readers what each slider controls.
  - A subtle detail: CSS `transform` does not affect the logical layout flow of the document. The text inside the rotating box remains selectable and readable by assistive technologies, regardless of its rotational state.
* **Performance**: 
  - CSS 3D transforms (`rotateX`, `rotateY`, `rotateZ`) are **GPU-accelerated** by modern browsers.
  - Using `transform` ensures we are avoiding layout trashing; mutating it rapidly via JavaScript during slider drags will not trigger expensive browser repaints/reflows, ensuring a smooth 60fps interaction.
  - A `0.1s` transition allows the JavaScript to fire at its native event rate while the CSS engine handles smoothly interpolating the visual frames between those events.