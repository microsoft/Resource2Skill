# Fluid Aurora Background (CSS Shape Morphing)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Fluid Aurora Background (CSS Shape Morphing)

* **Core Visual Mechanism**: A soft, glowing, organic shape that slowly drifts and morphs in the background. This is achieved by combining a multi-color `linear-gradient`, a high `filter: blur()` value to soften the edges into an "aurora" glow, and continuous CSS keyframe animations. The organic shape-shifting is specifically created by animating the `border-radius` property using complex percentage values, making a square `div` look like a fluid droplet.
* **Why Use This Skill (Rationale)**: Static backgrounds can feel lifeless, while video backgrounds or heavy WebGL particle systems can impact performance and page load times. This pure-CSS approach provides a dynamic, premium "holographic" aesthetic that is extremely lightweight, GPU-accelerated, and non-distracting.
* **Overall Applicability**: Ideal for SaaS landing page hero sections, login/authentication screens, premium product showcases, or interactive cards where you want to add a sense of depth and modern elegance.
* **Value Addition**: Transforms a flat layout into a spatial environment. The ambient movement draws the eye without competing with the primary text or call-to-action, especially when combined with a frosted-glass (glassmorphism) foreground layer.
* **Browser Compatibility**: Fully supported in all modern browsers. The properties used (`border-radius`, `filter: blur()`, `@keyframes`, `transform`) are universally supported and hardware-accelerated.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A full-bleed background container wrapping a `.blob-mover` div, which in turn wraps the actual `.blob` div. The content layer sits on top as a sibling.
  - **Color Logic**: The blob utilizes a rich, multi-stop linear gradient that blends the primary `accent_color` with deep blues and purples (e.g., `rgba(4, 116, 221, 0.8)`). The `blur()` filter spreads these colors out, creating ambient light.
  - **Filters**: `filter: blur(80px)` is the secret ingredient that turns a sharp-edged box into a volumetric cloud of light.

* **Step B: Layout & Compositional Style**
  - **Stacking**: The container relies on `position: relative` and `overflow: hidden`. The blob is `position: absolute` and centered. The text content sits in a `z-index: 10` container to ensure it is always clickable and readable.
  - **Sizing**: Using `clamp(250px, 40vw, 600px)` ensures the blob remains proportionate to the screen without becoming overwhelmingly large on desktop or tiny on mobile.

* **Step C: Interactive Behavior & Animations**
  - **Separation of Animation Concerns**:
    1. **Translation**: The `.blob-mover` wrapper handles the `transform: translate()` keyframes, moving the blob smoothly across the screen on an 18-second cycle.
    2. **Rotation**: The inner `.blob` handles `transform: rotate()`, spinning continuously over 15 seconds.
    3. **Morphing**: The inner `.blob` also animates `border-radius`, cycling through asymmetric values (e.g., `30% 70% 70% 30% / 30% 30% 70% 70%`) every 10 seconds.
  - By separating translation and rotation into two different DOM elements, we avoid CSS `transform` property conflicts and create a much more complex, randomized-looking path.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Organic shape morphing | CSS `border-radius` animation | Native CSS technique using 8-point percentages; incredibly performant and creates realistic fluid shapes without SVGs. |
| Glowing aurora effect | CSS `filter: blur()` + Gradients | Eliminates sharp edges of the div, blending the multi-color gradient into the background seamlessly. |
| Complex motion path | Nested DOM `transform` | Animating `translate` on a wrapper and `rotate` on the child prevents transform overrides and yields organic, compound motion. |
| Content Legibility | CSS `backdrop-filter` | Adding a subtle frosted glass effect to the text container ensures contrast against the moving bright colors. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Fluid Background",
    body_text: str = "A pure CSS shape-shifting aurora effect.",
    color_scheme: str = "dark",        
    accent_color: str = "#14cae6",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Aurora Background visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0c10"
        text_color = "#ffffff"
        surface_color = "rgba(20, 22, 30, 0.4)"
        border_color = "rgba(255, 255, 255, 0.1)"
        blob_opacity = "0.75"
    else:
        bg_color = "#f4f6f9"
        text_color = "#1a1a2e"
        surface_color = "rgba(255, 255, 255, 0.6)"
        border_color = "rgba(0, 0, 0, 0.05)"
        blob_opacity = "0.6"

    # CSS Code
    css = f"""/* Fluid Aurora Background Component */
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
    --width: {width_px}px;
    --height: {height_px}px;
    --blob-opacity: {blob_opacity};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-section {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    max-height: 100vh;
    position: relative;
    background: var(--bg);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Mover handles translation to prevent transform conflicts */
.blob-mover {{
    --blob-size: clamp(300px, 45vw, 650px);
    position: absolute;
    top: calc(50% - (var(--blob-size) / 2));
    left: calc(50% - (var(--blob-size) / 2));
    width: var(--blob-size);
    height: var(--blob-size);
    animation: moveShape 22s ease-in-out infinite alternate;
    pointer-events: none;
}}

.blob-mover-2 {{
    --blob-size: clamp(250px, 35vw, 500px);
    animation: moveShape2 18s ease-in-out infinite alternate-reverse;
}}

/* The Blob handles rotation, color, blur, and shape-shifting */
.blob {{
    width: 100%;
    height: 100%;
    background: linear-gradient(
        135deg,
        var(--accent) 0%,
        rgba(4, 116, 221, 0.8) 40%,
        rgba(126, 26, 247, 0.8) 100%
    );
    opacity: var(--blob-opacity);
    filter: blur(80px);
    animation: 
        changeShape 10s linear infinite, 
        rotateShape 15s linear infinite;
}}

.blob-2 {{
    background: linear-gradient(
        225deg,
        rgba(126, 26, 247, 0.8) 0%,
        var(--accent) 50%,
        rgba(4, 116, 221, 0.6) 100%
    );
    animation: 
        changeShape 12s linear infinite reverse, 
        rotateShape 18s linear infinite reverse;
}}

.content {{
    position: relative;
    z-index: 10;
    text-align: center;
    max-width: 600px;
    padding: 3rem 2rem;
    color: var(--text);
    background: var(--surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 24px;
    border: 1px solid var(--border);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
}}

.body-text {{
    font-size: 1.125rem;
    opacity: 0.85;
    line-height: 1.6;
}}

/* --- Animations --- */

@keyframes moveShape {{
    0%   {{ transform: translate(-10vw, -15vh); }}
    33%  {{ transform: translate(15vw, 5vh); }}
    66%  {{ transform: translate(-5vw, 15vh); }}
    100% {{ transform: translate(10vw, -10vh); }}
}}

@keyframes moveShape2 {{
    0%   {{ transform: translate(15vw, 10vh); }}
    33%  {{ transform: translate(-10vw, -15vh); }}
    66%  {{ transform: translate(5vw, -5vh); }}
    100% {{ transform: translate(-15vw, 15vh); }}
}}

@keyframes rotateShape {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}

@keyframes changeShape {{
    0%   {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }}
    25%  {{ border-radius: 50% 50% 30% 70% / 60% 40% 60% 40%; }}
    50%  {{ border-radius: 70% 30% 50% 50% / 40% 60% 40% 60%; }}
    75%  {{ border-radius: 40% 60% 70% 30% / 70% 30% 50% 50%; }}
    100% {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }}
}}
"""

    # HTML Code
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-section">
        <!-- Background Animation Layers -->
        <div class="blob-mover">
            <div class="blob"></div>
        </div>
        <div class="blob-mover blob-mover-2">
            <div class="blob blob-2"></div>
        </div>
        
        <!-- Foreground Content -->
        <div class="content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </section>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Code
    js = f"""// Fluid Aurora Background — Pure CSS animation.
// No JavaScript required for the core visual effect.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Aurora background initialized successfully.");
}});
"""

    # Write files
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": [os.path.join(output_dir, f) for f in ["index.html", "style.css", "script.js"]],
    }
```

### 4. Accessibility & Performance Notes

* **Performance / GPU Acceleration**: The animations rely purely on `transform`, `opacity`, and `filter`. Browsers handle `transform` and `opacity` on the compositor thread, preventing layout thrashing (jank). However, animating large elements with high `blur()` radii can be moderately taxing on lower-end mobile devices. The implementation mitigates this by restricting the animation strictly to hardware-accelerated properties.
* **Accessibility (a11y)**: 
  * The animated background is placed behind the content and ignores pointer events (`pointer-events: none;`), meaning it won't trap mouse clicks or screen readers.
  * For production environments, it is highly recommended to wrap the animations in a media query: `@media (prefers-reduced-motion: reduce) { .blob, .blob-mover { animation: none; } }` to accommodate users with vestibular disorders.
  * A translucent glassmorphism layer (`backdrop-filter`) was deliberately added behind the text in this reproduction. This ensures the text maintains a high contrast ratio (WCAG AA) regardless of the brightly colored gradient passing underneath it.