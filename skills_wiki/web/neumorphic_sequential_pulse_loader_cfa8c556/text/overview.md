# Neumorphic Sequential Pulse Loader

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neumorphic Sequential Pulse Loader

* **Core Visual Mechanism**: This component utilizes **Neumorphism** (soft UI) to create a set of interconnected nodes that appear physically pressed into the surface. The aesthetic signature is achieved by applying multiple `box-shadow` values (both `inset` and outset) to elements that share the exact same background color as the body. An inner "active" dot scales up and down sequentially, driven by staggered CSS `animation-delay` variables, creating a snake-like filling motion. A continuous `hue-rotate` filter cycles the active dot through the color spectrum.

* **Why Use This Skill (Rationale)**: Neumorphism creates a highly tactile, satisfying visual experience. By making the loading indicators feel like physical hardware buttons or indentations, it grounds the digital experience. The sequential filling animation provides a clear sense of progress and directionality, while the hue rotation keeps the user visually engaged during longer wait times.

* **Overall Applicability**: Perfect for high-end web applications, modern dashboards, creative portfolios, or tech-focused SaaS platforms where a distinctive, custom loading state is preferred over standard spinners. It works exceptionally well as a full-screen transition loader or a dedicated status indicator for complex operations.

* **Value Addition**: It elevates a mundane state (waiting/loading) into a micro-interaction showpiece. It proves that depth and complex geometry can be faked entirely with CSS shadows without requiring heavy 3D libraries or SVG assets.

* **Browser Compatibility**: Excellent. Relies on standard CSS properties (`box-shadow`, `transform`, `filter`, CSS variables) supported by all modern browsers (Chrome 8+, Firefox 4+, Safari 6+, Edge). 


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent container (`.loader`) holding multiple `<span>` elements. Each span represents a node and carries a custom CSS variable (e.g., `style="--i:0"`) to track its index.
  - **Color Logic**: Neumorphism requires the element's background color to precisely match the surrounding container's background. Depth is created purely through shadows.
    - *Light Scheme*: Background `#eaeef0`. Highlight shadow `rgba(255,255,255,1)`. Dark shadow `rgba(0,0,0,0.15)`.
    - *Dark Scheme*: Background `#2a2b2f`. Highlight shadow `rgba(255,255,255,0.05)`. Dark shadow `rgba(0,0,0,0.5)`.
  - **Key CSS Properties**:
    - `box-shadow`: The true engine of this component. Combines four distinct shadows (two outset for the raised rim, two inset for the depressed center) to create a 3D "doughnut" indentation.
    - `filter: hue-rotate()`: Continuously shifts the color spectrum of the inner dot.

* **Step B: Layout & Compositional Style**
  - **Grid/Flex**: The loader nodes are arranged in a horizontal line using Flexbox (`display: flex; gap: 20px;`).
  - **Proportions**: Each node is a perfect circle (`50px` by `50px`, `border-radius: 50%`) with a thick `6px` border matching the background to create the "rim" effect.
  - **Layering**: The colored pulsing dot is implemented as an absolutely positioned `::before` pseudo-element. Because the parent has a border and uses default `box-sizing` behaviors, `inset: 0` perfectly fits the dot inside the padding box of the rim.

* **Step C: Interactive Behavior & Animations**
  - **Sequential Scale Animation**: The inner dot runs an `@keyframes` animation alternating `transform: scale(0)` to `transform: scale(1)`.
  - **Staggered Delays**: The true magic happens via `animation-delay: calc(var(--i) * 0.2s);`. Node 0 starts immediately, Node 1 starts 0.2s later, creating a cascading wave. 
  - **Duration Math**: The animation duration is carefully tuned (e.g., `4s`) so that the final node finishes its scale sequence exactly as the loop restarts, avoiding jarring visual jumps.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Neumorphic Geometry** | CSS `box-shadow` | Multiple inset/outset shadows on a single element generate the complex 3D shape effortlessly. |
| **Sequential Staggering** | CSS Variables + `calc()` | Inline variables (`--i`) paired with `animation-delay` eliminates the need for JS or complex CSS `:nth-child` targeting. |
| **Color Shifting** | CSS `filter: hue-rotate` | Hardware-accelerated and cycles base colors automatically without requiring complex color-stop keyframes. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "System Processing",
    body_text: str = "Establishing secure connection to the server...",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#5c89ff",     # Base color of the pulsing dots
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic Sequential Pulse Loader.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors for Neumorphism ===
    if color_scheme == "dark":
        bg_color = "#2a2b2f"
        text_color = "#e0e0e0"
        shadow_light = "rgba(255, 255, 255, 0.05)"
        shadow_dark = "rgba(0, 0, 0, 0.6)"
        inner_shadow_light = "rgba(255, 255, 255, 0.1)"
        inner_shadow_dark = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#eaeef0"
        text_color = "#666666"
        shadow_light = "rgba(255, 255, 255, 1)"
        shadow_dark = "rgba(0, 0, 0, 0.15)"
        inner_shadow_light = "rgba(255, 255, 255, 0.8)"
        inner_shadow_dark = "rgba(0, 0, 0, 0.2)"

    # === CSS ===
    css = f"""/* Neumorphic Sequential Pulse Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --shadow-light: {shadow_light};
    --shadow-dark: {shadow_dark};
    --inner-light: {inner_shadow_light};
    --inner-dark: {inner_shadow_dark};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
}}

.text-content {{
    text-align: center;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 1px;
}}

.body-text {{
    font-size: 15px;
    opacity: 0.8;
}}

/* Loader Core Styles */
.loader {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
}}

.loader span {{
    position: relative;
    width: 50px;
    height: 50px;
    background: var(--bg);
    border-radius: 50%;
    border: 6px solid var(--bg);
    /* The Neumorphic Magic: Outset for the rim, Inset for the crater */
    box-shadow: 
        -8px -8px 15px var(--shadow-light),
        8px 8px 15px var(--shadow-dark),
        inset 3px 3px 5px var(--shadow-dark),
        inset -1px -1px 5px var(--shadow-light);
}}

.loader span::before {{
    content: '';
    position: absolute;
    inset: 0; /* Fills the inside of the border perfectly */
    border-radius: inherit;
    background: var(--accent);
    /* Gives the inner dot a slight 3D spherical feel */
    box-shadow: 
        inset 3px 3px 5px var(--inner-dark),
        inset -1px -1px 5px var(--inner-light);
    transform: scale(0);
    
    /* 4s duration gives enough time for the wave to complete across 7 nodes */
    animation: 
        pulseWave 4s cubic-bezier(0.4, 0, 0.2, 1) infinite,
        colorCycle 6s linear infinite;
    
    /* The core staggering mechanic */    
    animation-delay: calc(var(--i) * 0.2s);
}}

/* Pop in, hold, and pop out smoothly */
@keyframes pulseWave {{
    0%, 5% {{ transform: scale(0); }}
    15%, 70% {{ transform: scale(1); }}
    80%, 100% {{ transform: scale(0); }}
}}

/* Continuous color shift */
@keyframes colorCycle {{
    0% {{ filter: hue-rotate(0deg); }}
    100% {{ filter: hue-rotate(360deg); }}
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
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader">
            <!-- Inline CSS variables drive the staggered animation delay -->
            <span style="--i:0;"></span>
            <span style="--i:1;"></span>
            <span style="--i:2;"></span>
            <span style="--i:3;"></span>
            <span style="--i:4;"></span>
            <span style="--i:5;"></span>
            <span style="--i:6;"></span>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For this specific component, no JS is required for the visual effect.
    # It is included to satisfy the output format requirements.
    js = f"""// Neumorphic Loader Logic
document.addEventListener('DOMContentLoaded', () => {{
    // The visual mechanics are handled entirely by CSS variables and keyframes.
    console.log("Neumorphic Loader Initialized.");
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
  - Loading states should always communicate their state to screen readers. In a production environment, wrap the loader in an `aria-live="polite"` region and provide visually hidden text detailing the loading state.
  - The heavy reliance on CSS animations means `prefers-reduced-motion` should be respected. You can implement `@media (prefers-reduced-motion: reduce)` to disable the scaling and hue-rotate animations, perhaps leaving a static, solid state for the nodes.
* **Performance**: 
  - Modifying `transform` (scale) and `filter` (hue-rotate) is generally hardware-accelerated, making this component highly performant despite the complex visual outcome.
  - `box-shadow` rendering is the most expensive part of this component. While modern devices handle it with ease, applying this specific 4-shadow neumorphic stack to dozens of elements simultaneously could cause minor paint lag on low-end mobile devices. Limit its use to isolated focal points.