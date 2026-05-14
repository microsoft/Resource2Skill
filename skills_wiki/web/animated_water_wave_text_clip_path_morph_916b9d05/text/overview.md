# Animated Water Wave Text (Clip-Path Morphing)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Water Wave Text (Clip-Path Morphing)

* **Core Visual Mechanism**: A layered typographic effect simulating a flowing liquid wave inside text. This is achieved by stacking two identical text elements exactly on top of each other. The back layer has a transparent body and a colored outline (stroke). The front layer has a solid fill color but is masked using a CSS `clip-path` polygon. By animating the vertex coordinates of this polygon with CSS `@keyframes`, the mask smoothly morphs, creating the illusion of a flowing wave.
* **Why Use This Skill (Rationale)**: This technique creates a mesmerizing, organic visual effect using pure CSS without requiring external video files or WebGL. It immediately draws the eye and can visually reinforce themes related to fluidity, loading, progress, or nature.
* **Overall Applicability**: Perfect for creative typography in hero sections, engaging splash screens, custom "loading" percentage indicators, or thematic landing pages (e.g., beverages, analytics, dynamic data).
* **Value Addition**: Transforms static text into a dynamic, narrative element. It elevates typography from mere information delivery to an engaging, atmospheric set piece.
* **Browser Compatibility**: Excellent. `clip-path: polygon()` and `-webkit-text-stroke` are supported across all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - Uses two sibling `<h2>` tags within a wrapper. The second tag acts as the "water".
  - **Color logic**: High contrast. Dark background (`#000` or `#0d111c`), vivid accent color for the text stroke and wave fill (`#03a9f4`).
  - **Typographic hierarchy**: Requires a very thick, heavy, sans-serif font (like 'Poppins' or 'Inter', weight 700+) to give the wave enough "canvas" to be visible inside the letterforms.
  - Core CSS properties: `-webkit-text-stroke` (outline), `color: transparent` (hollow text), `clip-path` (masking), `@keyframes` (animation).

* **Step B: Layout & Compositional Style**
  - Elements are perfectly overlapped using `position: absolute`.
  - To keep the absolute elements centered gracefully, they rely on a zero-dimension relative wrapper (`.content`), and use `transform: translate(-50%, -50%)` to align precisely to the center point.

* **Step C: Interactive Behavior & Animations**
  - Pure CSS, continuous infinite animation.
  - The `@keyframes animate` rule runs for `4s` with an `ease-in-out` timing function.
  - The trick to animating `clip-path` polygons is that **all states must have the exact same number of coordinate pairs**. The animation smoothly interpolates the Y-axis percentages of the points, shifting the "peaks" and "troughs" of the wave horizontally and vertically.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Overlapped typography | `position: absolute` & `translate` | Ensures perfect pixel-alignment of the two text layers |
| Hollow outline text | `-webkit-text-stroke` | Native, performant way to stroke text while keeping fill transparent |
| Liquid mask boundary | `clip-path: polygon()` | CSS standard for masking; allows sharp, multi-point custom shapes |
| Flowing wave motion | CSS `@keyframes` | Browser natively interpolates matching polygon coordinate counts |

> **Feasibility Assessment**: 100% reproduction. The technique is a pure HTML/CSS setup. The extracted coordinates successfully recreate the specific wave shape from the tutorial. An accessibility improvement (`aria-hidden`) is added to prevent screen readers from reading the text twice.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Water",
    body_text: str = "",  # Not primarily used in this specific typographic effect
    color_scheme: str = "dark",
    accent_color: str = "#03a9f4",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Water Wave Text effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#000000"
    else:
        bg_color = "#ffffff"

    # === CSS ===
    css = f"""/* Animated Water Wave Text */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The relative wrapper ensures absolute children originate from the center */
.content {{
    position: relative;
}}

.content h2 {{
    position: absolute;
    transform: translate(-50%, -50%);
    font-size: clamp(4rem, 12vw, 12rem);
    font-weight: 700;
    white-space: nowrap;
}}

/* Back layer: Hollow Outline */
.content h2:nth-child(1) {{
    color: transparent;
    -webkit-text-stroke: 3px var(--accent);
}}

/* Front layer: Solid fill with animated clip-path */
.content h2:nth-child(2) {{
    color: var(--accent);
    animation: animateWave 4s ease-in-out infinite;
}}

/* Morphing the polygon coordinates to simulate a moving wave */
@keyframes animateWave {{
    0%, 100% {{
        clip-path: polygon(
            0% 45%, 
            15% 44%, 
            32% 50%, 
            54% 60%, 
            70% 61%, 
            84% 59%, 
            100% 52%, 
            100% 100%, 
            0% 100%
        );
    }}
    50% {{
        clip-path: polygon(
            0% 60%, 
            15% 65%, 
            34% 66%, 
            51% 62%, 
            67% 50%, 
            84% 45%, 
            100% 46%, 
            100% 100%, 
            0% 100%
        );
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Water Wave Text</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="content">
            <!-- Back layer (Outline) -->
            <h2>{title_text}</h2>
            <!-- Front layer (Animated Wave) - aria-hidden prevents duplicate screen reader announcements -->
            <h2 aria-hidden="true">{title_text}</h2>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required for the core visual wave effect.
// Animation is handled entirely via CSS @keyframes and clip-path.
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

* **Accessibility**: Because this pattern relies on duplicating DOM elements for layering, screen readers would typically read the word "Water" twice. Adding `aria-hidden="true"` to the secondary `<h2>` (the solid animated wave) ensures screen readers only parse the text once, maintaining semantic cleanliness. Ensure there is adequate contrast between the text stroke and the background color.
* **Performance**: Animating `clip-path` triggers geometry calculations in the browser. While not as cheap as animating `transform` or `opacity` (which are strictly GPU-composited), doing it on a single element or a small block of text is very performant on modern devices. If scaled up to hundreds of animated elements on a single page, it could cause layout jank, but as an isolated hero component, it is highly efficient.