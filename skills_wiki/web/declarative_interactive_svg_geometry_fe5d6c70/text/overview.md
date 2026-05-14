# Declarative Interactive SVG Geometry

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Declarative Interactive SVG Geometry

* **Core Visual Mechanism**: A resolution-independent, grid-based illustration composed of fundamental SVG primitives (`<rect>`, `<circle>`, `<polygon>`, `<path>`). These elements animate individually via CSS state changes, demonstrating coordinate-space transformations, stroke drawing/erasing, and color shifting.
* **Why Use This Skill (Rationale)**: SVGs are math-based, meaning they scale infinitely without losing quality (unlike raster PNGs/JPEGs). Because their internal geometric structure is exposed directly to the browser's DOM, developers can use standard CSS to target individual nodes inside the graphic. This allows for complex, hardware-accelerated micro-interactions (like rotating an inner shape or tracing a path) without needing any heavy JavaScript animation libraries.
* **Overall Applicability**: This pattern is highly effective for hero illustrations, feature highlight cards, empty state graphics, and custom interactive dashboard icons.
* **Browser Compatibility**: Broadly supported. SVG 1.1 primitives and applying CSS transforms/transitions to SVG elements are fully supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Coordinate System**: The `<svg viewBox="0 0 100 100">` establishes a normalized 100x100 canvas. All internal values (like `x="30"`) are relative to this grid, making the graphic fluidly responsive.
  - **Primitives**: Basic structural shapes use `<rect>`, `<circle>`, and `<polygon>`.
  - **Paths**: The organic swooshes utilize the `<path>` element and the `d` (draw) attribute, specifically using the `M` (Move) and `C` (Cubic Bézier) commands.
  - **Color Logic**: The background grid is subtle (low opacity), while the primary shapes use the `accent` color for fills and the `text` color for structural strokes.

* **Step B: Layout & Compositional Style**
  - **Concentric Layering**: The geometry is layered outwards from the center `(50, 50)` coordinate. 
  - **Z-Indexing**: In SVG, z-index is determined purely by document order. The background grid (`<pattern>`) is drawn first, followed by the outer ring, the square, the triangle, and finally the Bézier curves overlapping the top.

* **Step C: Interactive Behavior & Animations**
  - **Transform Origins**: By default, SVG elements rotate around `0,0` (top left). CSS `transform-origin: 50px 50px` re-centers the pivot point to the middle of the `viewBox` for smooth, symmetrical rotation.
  - **Path Animations**: Modifying the `stroke-dasharray` (length of dashes) and `stroke-dashoffset` (where the dash starts) creates a smooth "draw/erase" tracing effect on the organic curves.
  - **Choreographed Hover**: A single parent `.card:hover` selector triggers different, independent transitions on the child SVG elements, creating a mechanical, morphing composition.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Resolution-independent canvas** | `<svg viewBox="...">` | Maps abstract coordinate math directly to a scalable container. |
| **Basic geometric shapes** | `<rect>`, `<circle>`, `<polygon>` | Native SVG primitives; clean, semantic, and easy to position. |
| **Organic curves** | `<path d="...">` | Uses native Cubic Bézier (`C`) draw commands for smooth curves. |
| **Hover animations** | CSS Transforms & Transitions | GPU-accelerated, performant, and declarative—no JS required. |
| **Path drawing effect** | CSS `stroke-dashoffset` | Creates the illusion of a path tracing itself by shifting the dash stroke. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Interactive SVG",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#facc15",  # Default to a vibrant yellow/orange
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Declarative Interactive SVG Geometry effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Provide default body text if none is supplied
    if not body_text:
        body_text = "Scalable Vector Graphics use mathematical geometry rather than pixels, allowing infinite scaling, crisp rendering, and deep CSS integration."

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#e2e8f0"
        surface_color = "#1e2130"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.4)"
        grid_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.06)"
        grid_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Declarative Interactive SVG Geometry */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --grid: {grid_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 40px;
    width: 100%;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    box-shadow: 0 20px 40px var(--shadow);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    cursor: pointer;
    user-select: none;
}}

.card:hover, .card.active {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 30px 60px var(--shadow);
}}

.svg-wrapper {{
    width: 100%;
    aspect-ratio: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    box-shadow: inset 0 4px 20px rgba(0,0,0,0.05);
}}

.vector-graphic {{
    width: 100%;
    height: 100%;
    display: block;
    overflow: visible;
}}

/* SVG Element Styling & Origins */
.dashed-ring {{
    transform-origin: 50px 50px;
    animation: spin 20s linear infinite;
}}

.awesome-square {{
    transform-origin: 50px 50px;
    transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), fill 0.4s ease;
}}

.awesome-triangle {{
    transform-origin: 50px 50px;
    transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), fill 0.4s ease;
}}

.wave-1, .wave-2 {{
    stroke-dasharray: 120;
    stroke-dashoffset: 0;
    transition: stroke-dashoffset 0.8s ease-in-out, stroke 0.4s ease;
}}

.wave-1 {{
    filter: drop-shadow(0 0 4px var(--accent));
}}

/* Hover & Active Interactions */
.card:hover .awesome-square,
.card.active .awesome-square {{
    transform: rotate(90deg) scale(0.85);
    fill: transparent;
}}

.card:hover .awesome-triangle,
.card.active .awesome-triangle {{
    transform: rotate(180deg) scale(1.3);
    fill: var(--bg);
}}

.card:hover .wave-1,
.card.active .wave-1 {{
    stroke-dashoffset: 120;
}}

.card:hover .wave-2,
.card.active .wave-2 {{
    stroke-dashoffset: -120;
    stroke: var(--accent);
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* Typography */
.content {{
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.75;
    line-height: 1.6;
}}
"""

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
    
    <div class="card">
        <div class="svg-wrapper">
            <!-- Master viewBox maps relative coordinates 0 to 100 -->
            <svg viewBox="0 0 100 100" class="vector-graphic">
                
                <!-- Background Grid Pattern -->
                <defs>
                    <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                        <path d="M 10 0 L 0 0 0 10" fill="none" stroke="var(--grid)" stroke-width="0.5" />
                    </pattern>
                </defs>
                <rect width="100" height="100" fill="url(#grid)" rx="8" class="base-rect"/>

                <!-- Geometric Primitives Group -->
                <g class="geometry-group">
                    <!-- Dashed Outer Circle -->
                    <circle class="dashed-ring" cx="50" cy="50" r="35" fill="none" stroke="var(--text)" stroke-width="1" stroke-dasharray="4 6" />

                    <!-- Rotating Base Rectangle -->
                    <rect class="awesome-square" x="30" y="30" width="40" height="40" fill="var(--accent)" stroke="var(--text)" stroke-width="2" rx="6" />

                    <!-- Inner Polygon -->
                    <polygon class="awesome-triangle" points="50,35 63,55 37,55" fill="var(--surface)" stroke="var(--text)" stroke-width="1.5" stroke-linejoin="round" />

                    <!-- Center Fixed Dot -->
                    <circle class="center-dot" cx="50" cy="50" r="4" fill="var(--text)" />
                </g>

                <!-- Complex Organic Paths using Cubic Béziers -->
                <path class="wave-1" d="M 10 50 C 30 20, 70 80, 90 50" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" />
                <path class="wave-2" d="M 10 50 C 30 80, 70 20, 90 50" fill="none" stroke="var(--text)" stroke-width="2.5" stroke-linecap="round" />
            </svg>
        </div>
        
        <div class="content">
            <h2 class="title">{title_text}</h2>
            <p class="body-text">{body_text}</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Declarative Interactive SVG Geometry
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    
    // Add click listener to toggle persistent active state
    // This allows users on touch devices to lock the animation state
    card.addEventListener('click', () => {{
        card.classList.toggle('active');
    }});
}});
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