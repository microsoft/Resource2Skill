# Pure CSS Isometric 3D Cube

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Isometric 3D Cube

* **Core Visual Mechanism**: Creating a simulated 3D object (a cube) on a 2D screen using CSS transforms. While the original video uses complex 2D matrix math (`rotate`, `skew`, `scale`) to manually distort flat `div`s into an isometric perspective, the underlying pattern is the **isometric projection**. This style creates a clean, technical, depth-enhancing visual without perspective distortion (parallel lines remain parallel).
* **Why Use This Skill (Rationale)**: Isometric elements add engaging depth and a modern "builder" or "technical" aesthetic to flat interfaces without the heavy performance overhead of WebGL/Canvas 3D engines. They are lightweight, highly customizable, and scale perfectly.
* **Overall Applicability**: Excellent for decorative hero graphics, technical illustrations, interactive data visualizations, features grids (e.g., stacked features), or custom loading animations. 
* **Value Addition**: Transforms standard flat DOM elements into volumetric shapes. By upgrading the technique from the video's manual 2D skews to native CSS 3D transforms (`transform-style: preserve-3d`), the component gains true depth, making it infinitely easier to scale, rotate interactively, and theme.
* **Browser Compatibility**: Excellent. CSS 3D transforms (`perspective`, `rotateX`, `rotateY`, `translateZ`) have >98% global support across all modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A scene container, a volume container (`.cube`), and three visible faces (`.top`, `.left`, `.right`).
  - **Color Logic**: The component uses a base accent color (vibrant pink `#ff2a85` in the video). To create the illusion of 3D lighting, three distinct shades are needed:
    - Top face: Lightest (simulating overhead light).
    - Left face: Darkest (simulating shadow).
    - Right face: Mid-tone.
  - **Typography**: Minimal, used only for supporting context around the structural element.

* **Step B: Layout & Compositional Style**
  - **Centering**: The scene uses standard CSS Flexbox/Grid to center the object in the viewport.
  - **Sizing**: Faces are perfectly square (e.g., 150px by 150px).
  - **Layering**: The CSS 3D rendering engine automatically handles Z-index depth sorting when `preserve-3d` is active, removing the need for manual `z-index` management.

* **Step C: Interactive Behavior & Animations**
  - The tutorial demonstrates a static build. However, utilizing CSS 3D space makes it trivial to add engaging interactions. We will add a subtle "levitation" hover effect to demonstrate the volumetric nature of the component.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Isometric Projection | CSS 3D Transforms (`rotateX`, `rotateY`) | **Deviation from Video:** The video uses complex 2D `skew()` and `scale()` math on flat elements. We upgrade this to native CSS 3D (`preserve-3d`). It produces the exact same visual result but is mathematically perfect, easier to scale responsively, and allows for actual 3D rotation animations. |
| Dynamic Shading | CSS `::after` overlays with `rgba` | Allows the component to accept *any* single base hex color and automatically generate the correct lighting/shades for the top, left, and right faces using semi-transparent black/white overlays. |

*Feasibility Assessment*: 100% reproduction of the core visual effect, significantly improved in technical implementation for reusability, responsiveness, and theming.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Isometric Cube",
    body_text: str = "Pure CSS 3D projection using preserve-3d and dynamic shading.",
    color_scheme: str = "light",        
    accent_color: str = "#ff2a85",     # Vibrant pink matching the tutorial
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Isometric Cube visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f9fafb"
    else:
        bg_color = "#ffffff"
        text_color = "#1f2937"

    # CSS
    css = f"""/* Pure CSS Isometric Cube generated styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --cube-size: 160px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    gap: 4rem;
}}

.header {{
    text-align: center;
    z-index: 10;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

p {{
    color: {text_color};
    opacity: 0.7;
    font-size: 1.1rem;
}}

/* --- Isometric Cube Scene --- */
.scene {{
    width: var(--cube-size);
    height: var(--cube-size);
    /* Perspective isn't strictly necessary for true isometric (which lacks perspective), 
       but a very high value keeps the 3D engine engaged while appearing orthographic */
    perspective: 4000px; 
    position: relative;
}}

.cube {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    /* Standard isometric projection angles */
    transform: rotateX(-35.264deg) rotateY(45deg);
    transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}}

/* Value Addition: Interactive Hover State */
.scene:hover .cube {{
    transform: rotateX(-35.264deg) rotateY(45deg) translateY(-15px) scale(1.05);
}}

.face {{
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--accent);
    /* Smooth edges slightly */
    outline: 1px solid transparent; 
}}

/* Dynamic Shading System using overlays */
.face::after {{
    content: '';
    position: absolute;
    inset: 0;
}}

/* Position faces to form a cube */
.top {{
    transform: rotateX(90deg) translateZ(calc(var(--cube-size) / 2));
}}
.top::after {{
    /* Lightest face */
    background-color: rgba(255, 255, 255, 0.15);
}}

.left {{
    transform: rotateY(-90deg) translateZ(calc(var(--cube-size) / 2));
}}
.left::after {{
    /* Darkest face (shadow) */
    background-color: rgba(0, 0, 0, 0.25);
}}

.right {{
    transform: translateZ(calc(var(--cube-size) / 2));
}}
.right::after {{
    /* Mid-tone face */
    background-color: rgba(0, 0, 0, 0.08);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- 3D Component -->
    <div class="scene">
        <div class="cube">
            <div class="face top"></div>
            <div class="face left"></div>
            <div class="face right"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # JS (Empty but included for strict structural compliance, interaction is pure CSS)
    js = f"""// Component logic
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Isometric Cube initialized.");
    // 3D rotation and shading are handled entirely via CSS preserve-3d
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