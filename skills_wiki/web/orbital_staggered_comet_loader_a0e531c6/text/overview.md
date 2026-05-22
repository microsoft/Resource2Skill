# Orbital Staggered Comet Loader

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Orbital Staggered Comet Loader

* **Core Visual Mechanism**: This component creates a "comet" loading animation using a series of decreasing-sized dots orbiting a central point. The defining mechanism is the combination of **staggered positive `animation-delay`s** and an animation keyframe that **pauses for 50% of its duration**. This causes the dots to shoot out sequentially, form a trailing tail due to the `ease-out` timing function, and then smoothly catch up to each other at the top of the circle to merge back into a single point before the cycle repeats.
* **Why Use This Skill (Rationale)**: Typical spinners are static in their relative spacing, which can feel robotic. This pattern introduces dynamic physics-like behavior (acceleration, trailing, merging) entirely through CSS timing math. It feels organic, playful, and highly satisfying to watch, making wait times feel shorter.
* **Overall Applicability**: Perfect for full-screen loading overlays, form submission states, or lazy-loading placeholders in modern, polished web applications (SaaS dashboards, creative portfolios).
* **Value Addition**: Transforms a standard loading state into a micro-interaction that adds character to the UI. The clever use of `transform-origin` completely avoids the need for complex sine/cosine calculations in JavaScript.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard CSS Custom Properties, `calc()`, and CSS Keyframes. No experimental APIs are used.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Elements**: A container `.circle` div and 8 child `.dot` divs.
  - **Color Logic**: High contrast is key. The tutorial uses a dark indigo background (`hsl(253, 30%, 15%)`) with a vibrant orange/gold accent (`hsl(34, 78%, 60%)`) for the dots.
  - **Sizing Math**: The dots dynamically shrink. The largest dot is 15px, decreasing by 1px per index (`calc(15px - (1px * var(--i)))`).

* **Step B: Layout & Compositional Style**
  - **Centering**: The dots are horizontally centered within the `.circle` using `left: calc(50% - var(--dot-size) / 2);` and anchored to the top using `top: 0;`.
  - **The Pivot Point**: The most crucial layout trick is `transform-origin: calc(var(--dot-size) / 2) calc(var(--circle-size) / 2);`. Since the dot is positioned at the top-center of the circle, setting the Y-origin to half the circle's size pushes the pivot point exactly to the geometric center of the parent `.circle`.

* **Step C: Interactive Behavior & Animations**
  - **Timing**: The total duration is `3000ms`. The keyframe rotates `0deg` to `360deg` between `0%` and `50%`, then does nothing from `50%` to `100%`.
  - **Easing**: An `ease-out` timing function is applied, meaning the dots shoot out quickly and slow down as they complete their orbit.
  - **Staggering**: Each dot receives a positive delay: `calc(3000ms / 8 * var(--i))`. Because they share the same paused keyframe structure, this positive delay means the leading dot finishes its orbit and waits, allowing the delayed trailing dots to "catch up" and stack on top of it, creating the merging effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Orbital Path | CSS `transform-origin` | By shifting the transform origin down by the radius of the orbit, a simple `rotate()` creates a perfect circular path without JS math. |
| Tail & Merge Effect | CSS `animation-delay` + Keyframe pauses | Offsetting the start times while pausing the second half of the animation forces the elements to expand out and then naturally collapse back into each other. |
| Dynamic Sizing | CSS Custom Properties + `calc()` | Injecting an index (`--i: 0`, `--i: 1`) in HTML allows CSS to dynamically calculate size, delay, and decrement without duplicating classes. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Experience",
    body_text: str = "Please wait while we prepare your workspace...",
    color_scheme: str = "dark",
    accent_color: str = "#f6a84d",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Orbital Staggered Comet Loader.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#111116" # Deep dark background
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f4f8"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Orbital Staggered Comet Loader */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.widget-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

/* Text Styling */
.text-content {{
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text-color);
    opacity: 0.7;
}}

/* Loader Core Styles */
.loader {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

.circle {{
    --circle-size: 100px;
    height: var(--circle-size);
    width: var(--circle-size);
    position: relative;
}}

.dot {{
    /* Animation Math Variables */
    --total-dots: 8;
    --duration: 3000ms;
    
    /* Size calculation: starts at 15px, gets smaller as --i increases */
    --dot-decrement: calc(1px * var(--i));
    --dot-size: calc(15px - var(--dot-decrement));
    
    height: var(--dot-size);
    width: var(--dot-size);
    background-color: var(--accent-color);
    border-radius: 50%;
    
    /* Positioning */
    position: absolute;
    top: 0;
    left: calc(50% - var(--dot-size) / 2);
    
    /* Move the pivot point to the center of the parent .circle */
    transform-origin: calc(var(--dot-size) / 2) calc(var(--circle-size) / 2);
    
    /* Animation */
    animation: spin var(--duration) ease-out infinite;
    /* Positive delay causes them to stagger and trail */
    animation-delay: calc(var(--duration) / var(--total-dots) * var(--i));
}}

@keyframes spin {{
    0% {{
        transform: rotate(0deg);
    }}
    /* Pausing at 50% allows the trailing dots to catch up and merge */
    50%, 100% {{
        transform: rotate(360deg);
    }}
}}

/* Accessibility: Pause animation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .dot {{
        animation-duration: 10s;
        animation-timing-function: linear;
        animation-delay: 0s;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orbital Loader Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        
        <div class="loader" aria-label="Loading..." role="progressbar">
            <div class="circle">
                <!-- Using inline CSS variables to drive the staggering logic -->
                <div class="dot" style="--i: 0"></div>
                <div class="dot" style="--i: 1"></div>
                <div class="dot" style="--i: 2"></div>
                <div class="dot" style="--i: 3"></div>
                <div class="dot" style="--i: 4"></div>
                <div class="dot" style="--i: 5"></div>
                <div class="dot" style="--i: 6"></div>
                <div class="dot" style="--i: 7"></div>
            </div>
        </div>

        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS implementation. No JavaScript required for this visual mechanism.
// You could dynamically generate the dots here if you wanted a configurable number of dots.
console.log("Orbital loader initialized.");
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

### 4. Accessibility & Performance Notes

* **Accessibility**: Continuous, fast-paced spinning animations can be triggering for users with vestibular disorders. A `@media (prefers-reduced-motion: reduce)` query is included to significantly slow down the animation and remove the stagger effect, turning it into a very gentle, slow rotation. An `aria-label` and `role="progressbar"` have been added to the container so screen readers can interpret its purpose.
* **Performance**: The entire animation is offloaded to the GPU via `transform: rotate()`. Because the layout properties (`left`, `top`, `width`, `height`) are calculated once via `calc()` and remain static, and only `transform` is animated, this component is highly performant and will not trigger costly layout recalculations or paint storms during execution.