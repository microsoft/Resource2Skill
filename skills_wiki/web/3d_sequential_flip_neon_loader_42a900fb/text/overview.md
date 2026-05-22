### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Sequential Flip Neon Loader

* **Core Visual Mechanism**: A hollow, glowing square that sequentially flips 180 degrees along its X, Y, and Z axes. The motion is driven by a continuous CSS `@keyframes` loop and 3D transforms (`rotateX`, `rotateY`, `rotateZ`), paired with an inner and outer `box-shadow` to create a neon tubing effect.
* **Why Use This Skill (Rationale)**: This technique turns a standard waiting period into an engaging, hardware-accelerated micro-interaction. The sequential multi-axis flipping creates a continuous sense of progress and mechanical rhythm, while the glowing aesthetic draws the user's attention without being visually overwhelming.
* **Overall Applicability**: Excellent for full-page loading screens, async data fetching indicators in dark-themed dashboards, SaaS applications, or web3/tech-oriented user interfaces.
* **Value Addition**: Replaces static spinners or generic GIFs with a highly performant, resolution-independent CSS animation. It requires zero external assets (no images or SVGs) and runs entirely off the main JavaScript thread, ensuring smooth 60fps playback even during heavy data processing.
* **Browser Compatibility**: Fully supported in all modern browsers. Uses the independent `translate` property (supported in Chrome 104+, Safari 14.1+, Firefox 73+) to avoid interfering with the `transform` property used for the animation.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Element**: A single `<div>` for the square loader.
  - **Color Logic**: Deep dark blue/purple background (`#040716`) contrasting with a vivid cyan/neon accent (`#00ffff`).
  - **Effects**: A 6px solid border combined with dual `box-shadow` declarations (one standard, one `inset`) creates the glowing "neon tube" look. 
  - **Key CSS**: `transform: rotateX() rotateY() rotateZ()`, `box-shadow`, `animation`.

* **Step B: Layout & Compositional Style**
  - The loader is exactly `50px` by `50px` with a subtle `4px` border radius to soften the corners of the neon glow.
  - It is centered within its container using Flexbox, preventing layout flow disruptions.

* **Step C: Interactive Behavior & Animations**
  - **Animation Sequence**: 
    - `0% - 33%`: Flips 180° on the X-axis.
    - `33% - 67%`: Flips 180° on the Y-axis.
    - `67% - 100%`: Flips 180° on the Z-axis.
  - **Timing**: The `2s` duration utilizes an `ease-in-out` timing function, allowing the square to smoothly accelerate into each flip and softly snap into place before the next axis begins rotating.
  - **Interaction**: Features an `animation-play-state: paused` interaction triggered via JavaScript when hovered, allowing users to freeze the 3D state mid-flip.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Sequential 3D Flips** | CSS `@keyframes` + `transform` | GPU-accelerated, performant, and perfectly synced timing without JS overhead. |
| **Neon Glow** | CSS `box-shadow: inset & outset` | Creates a convincing glowing light-tube effect purely with native styling. |
| **Centering & Layout** | CSS Flexbox | Robust vertical/horizontal centering that avoids `transform: translate()` conflicts with the animation. |
| **Pause Interaction** | JavaScript DOM Events | Dynamically modifies `element.style.animationPlayState` to demonstrate dynamic CSS animation control. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Please wait while we initialize the interface...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Sequential Flip Neon Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#f0f0f0"
        subtext_color = "#8b94b0"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a1a2e"
        subtext_color = "#5a6480"
        
        # Ensure light mode has a darker default accent if neon cyan is passed
        if accent_color == "#00ffff":
            accent_color = "#0066ff"

    # === CSS ===
    css = f"""/* 3D Sequential Flip Neon Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
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
    gap: 3rem;
    position: relative;
}}

/* Loader Wrapper for isolation and click target */
.loader-wrapper {{
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    /* Optional: add 'perspective: 400px;' here for a more exaggerated 3D depth effect */
}}

/* Core Loading Square */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 
        0 0 8px var(--accent), 
        0 0 8px var(--accent) inset;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loadingSequence ease-in-out infinite;
}}

/* Text Content */
.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--subtext);
}}

/* The Sequential Flip Keyframes */
@keyframes loadingSequence {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* Accessibility: Reduced Motion Fallback */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation: 3s pulse ease-in-out infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 0.3; transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1.1); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        
        <!-- Loading Indicator -->
        <div class="loader-wrapper" aria-label="Loading indicator. Hover to pause animation." role="progressbar" aria-busy="true">
            <div class="loading"></div>
        </div>
        
        <!-- Typography -->
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Sequential Flip Neon Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loaderWrapper = document.querySelector('.loader-wrapper');
    const loadingElement = document.querySelector('.loading');

    // Demonstrate animation-play-state property via JavaScript
    // Pauses the 3D flip mid-animation when the user hovers over the loader area
    loaderWrapper.addEventListener('mouseenter', () => {{
        loadingElement.style.animationPlayState = 'paused';
    }});

    loaderWrapper.addEventListener('mouseleave', () => {{
        loadingElement.style.animationPlayState = 'running';
    }});
    
    // Toggle pause/play on click for touch devices
    let isPaused = false;
    loaderWrapper.addEventListener('click', () => {{
        isPaused = !isPaused;
        loadingElement.style.animationPlayState = isPaused ? 'paused' : 'running';
    }});
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
  - The loader includes `role="progressbar"` and `aria-busy="true"` so screen readers can announce the loading state contextually.
  - A `@media (prefers-reduced-motion: reduce)` block is included. High-speed 3D flipping can cause dizziness or nausea in susceptible users. The fallback CSS replaces the 3D axis flipping with a gentle, slow scaling and opacity pulse.
* **Performance**: 
  - CSS transforms (`rotateX`, `rotateY`, `rotateZ`) are composited layers handled by the GPU, making this extremely performant. It will not drop frames even if the main thread is locked up processing large data payloads in JavaScript.
  - The JS event listeners specifically target `animation-play-state` rather than recalculating transforms, which is computationally cheap.