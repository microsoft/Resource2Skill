### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Rotating Neon Loader

* **Core Visual Mechanism**: A sequential 3D tumbling effect achieved by animating CSS `rotateX`, `rotateY`, and `rotateZ` transforms across percentage-based `@keyframes`. The loader is styled with a prominent border and a dual `box-shadow` (inset and outset) to create a glowing, neon-like aesthetic that mimics a physical, illuminated hollow cube tumbling in space.
* **Why Use This Skill (Rationale)**: Loading states need to reassure the user that a process is active. The rhythmic, three-stage rotational snapping (created by applying an `ease-in-out` timing function across three keyframe intervals) gives a sense of mechanical precision, progression, and high performance.
* **Overall Applicability**: Ideal for splash screens, data-fetching placeholder states, heavy media loading overlays, or tech/SaaS themed web applications.
* **Value Addition**: This technique is 100% pure CSS, meaning it is hardware-accelerated (via GPU) and extremely performant. It also elegantly demonstrates how to separate positioning logic (`translate`) from visual manipulation (`transform`), a modern CSS best practice.
* **Browser Compatibility**: Requires modern browsers that support independent CSS transform properties (e.g., `translate` without needing the `transform` function). This is supported in Chrome 104+, Safari 14.1+, and Firefox 73+.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A single, hollow `div` element acts as the geometry.
  - **Color Logic**: A deep, dark background (`#040716`) contrasts sharply with a vivid cyan/aqua accent (`#00ffff`). The "glow" is achieved using two box shadows: `0 0 8px var(--accent)` for the outer radiance and `0 0 8px var(--accent) inset` for the inner illumination.
  - **Typographic Hierarchy**: Clean sans-serif (Inter/system-ui), with uppercase tracking on the title to maintain a technical, UI-focused aesthetic.

* **Step B: Layout & Compositional Style**
  - **Modern Centering System**: The loader utilizes modern CSS spatial separation. It is centered inside its container using `position: absolute; top: 50%; left: 50%;` and the independent `translate: -50% -50%;` property. 
  - **Why this matters**: Because `translate` is separate from `transform`, the heavy `@keyframes` rotation logic (`transform: rotateX(...)`) does not accidentally overwrite the element's centering coordinates.

* **Step C: Interactive Behavior & Animations**
  - **Keyframe Sequence**: The animation divides exactly into thirds:
    - `0% - 33%`: Flips 180° on the X-axis.
    - `33% - 67%`: Flips 180° on the Y-axis.
    - `67% - 100%`: Flips 180° on the Z-axis.
  - **Timing Rhythm**: The global `animation-timing-function: ease-in-out` applies to *each individual keyframe segment*. This causes the box to speed up and slow down (snap and settle) three distinct times per loop, generating a highly satisfying rhythm.
  - **JS State Management**: JavaScript buttons (Play/Pause) directly manipulate the element's `style.animationPlayState` property, combined with mouse hover events, allowing the user to freeze the loader in mid-air.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Sequential 3D Tumbling** | CSS `@keyframes` | Native GPU-accelerated rotation; avoids heavy JS animation loops. |
| **Neon Glow Effect** | CSS `box-shadow` | Combining standard and `inset` shadows perfectly mimics a glowing physical rim. |
| **Centering vs. Rotation** | Independent `translate` property | Prevents CSS `transform` overrides, allowing complex 3D rotations without losing layout coordinates. |
| **Play/Pause Interaction** | JS `animationPlayState` | Directly hooks into the CSS animation engine, freezing the transform matrix instantly. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Establishing secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan/Aqua
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Rotating Neon Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716"  # Exact dark background from tutorial
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.1)"
        btn_hover = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f7fb"
        text_color = "#040716"
        surface_color = "rgba(0, 0, 0, 0.1)"
        btn_hover = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* 3D Rotating Neon Loader — generated component */
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
    --btn-hover: {btn_hover};
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

.app-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    border-radius: 16px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    border: 1px solid var(--surface);
}}

/* Visual Stage for the 3D Element */
.visual-stage {{
    position: relative;
    width: 100%;
    height: 200px;
    margin-bottom: 1rem;
}}

.loading-box {{
    /* Modern Centering: Independent Translate */
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    
    /* Box Styles */
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Neon Glow */
    box-shadow: 0 0 12px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation Configuration */
    animation: 2s loading ease-in-out infinite;
    cursor: pointer;
}}

/* 3D Rotation Keyframes */
@keyframes loading {{
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

/* Typography */
.content-wrapper {{
    text-align: center;
    z-index: 10;
}}

h1.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}}

p.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
    max-width: 400px;
    margin: 0 auto 2rem auto;
    line-height: 1.5;
}}

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 1rem;
}}

.control-btn {{
    background: transparent;
    color: var(--text);
    border: 1px solid var(--surface);
    padding: 0.5rem 1.25rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
    outline: none;
}}

.control-btn:hover, .control-btn:focus-visible {{
    background: var(--btn-hover);
    border-color: var(--accent);
}}

/* Accessibility: Respect Reduced Motion Preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-box {{
        animation: none;
        transform: rotate(45deg); /* Static, aesthetically pleasing resting state */
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
    <div class="app-container">
        
        <div class="visual-stage">
            <div class="loading-box" id="loaderElement" aria-label="Loading animation" role="progressbar"></div>
        </div>
        
        <div class="content-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="controls">
            <button id="playBtn" class="control-btn" aria-label="Play Animation">Play</button>
            <button id="pauseBtn" class="control-btn" aria-label="Pause Animation">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Rotating Neon Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loaderElement');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Control animation state via buttons
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    // Provide interactive pausing on hover (as demonstrated in tutorial)
    // Using JS events avoids CSS specificity conflicts with inline styles
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    loader.addEventListener('mouseleave', () => {{
        loader.style.animationPlayState = 'running';
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Are `title_text` and `body_text` properly handled?
- [x] Does the JavaScript run without console errors and successfully toggle `animation-play-state`?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect (tumbling 3D neon square)?

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  - An `aria-label` and `role="progressbar"` have been added to the tumbling div so screen readers can contextualize its presence.
  - A `@media (prefers-reduced-motion: reduce)` block is fully implemented. If the user's OS has motion disabled, the infinite rotation loop is killed, and the box is parked at a static `45deg` angle, which looks intentionally designed rather than broken.
* **Performance**: 
  - CSS transforms (`rotateX`, `rotateY`, `rotateZ`) do not trigger browser layout reflows or repaints; they are strictly composited on the GPU. This is the most performant way to achieve 3D rendering in the browser without spinning up WebGL.
  - Using `animationPlayState` to pause the animation stops GPU computation immediately, saving battery on mobile devices.