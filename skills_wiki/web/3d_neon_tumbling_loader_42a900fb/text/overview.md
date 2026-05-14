### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Neon Tumbling Loader

* **Core Visual Mechanism**: A smooth, sequential 3D tumbling animation of a geometric square using pure CSS `@keyframes`. The element rotates sequentially along its X, Y, and Z axes. The shape itself is hollow, utilizing a semi-thick border and dual `box-shadow` (both inner and outer) to create a vibrant, glowing neon effect against a dark background.
* **Why Use This Skill (Rationale)**: Loading states can often feel tedious to users. Using a 3D, physics-defying visual (like a tumbling neon cube) retains user attention. The staggered rotation on different axes (X, then Y, then Z) creates an illusion of complex 3D rendering while actually just manipulating a flat 2D plane in standard CSS space. 
* **Overall Applicability**: Ideal for initial page loading screens, data-fetching indicators, form submission states, or tech-oriented dashboard widgets. The neon aesthetic pairs exceptionally well with dark mode web designs, Web3 applications, and developer portfolios.
* **Value Addition**: It entirely bypasses the need for heavy external animation libraries (like Lottie or GSAP) or complex WebGL/Three.js setups, replacing them with extremely lightweight, hardware-accelerated CSS transforms.
* **Browser Compatibility**: Excellent. The CSS `transform` (including rotateX, rotateY, rotateZ), `box-shadow`, and standard `animation` properties are supported universally across all modern browsers (Chrome, Edge, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A single empty `<div>` forms the core loader. Additional semantic text elements or control buttons can surround it.
  - **Color Logic**: High contrast is key. 
    - Background: Deep void colors like Deep Navy (`#040716`) or almost-black.
    - Glow/Border: High saturation cyan/aqua (`#00FFFF`), driven entirely by the `accent` color.
  - **Styling Properties**: 
    - `border`: Defines the physical shape (e.g., `6px solid var(--accent)`).
    - `box-shadow`: Creates the neon glow via a combination of outset and inset shadows (e.g., `0 0 8px var(--accent), inset 0 0 8px var(--accent)`).
    - `border-radius`: A slight curve (`4px`) softens the harsh digital edges of the square.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox or CSS Grid ensures the loader is perfectly centered within its containing space.
  - **Spatial Feel**: The loader requires ample negative space around it so the glowing effect and 3D rotation do not visually collide with surrounding text or boundaries.
  - **Proportions**: A strict 1:1 aspect ratio (e.g., 50x50px) maintains the perfect square illusion during rotation.

* **Step C: Interactive Behavior & Animations**
  - **Keyframes Setup**: The sequence spans 0% to 100%, segmented into thirds.
    - `33%`: Rotate X by 180 degrees.
    - `67%`: Maintain X, rotate Y by 180 degrees.
    - `100%`: Maintain X and Y, rotate Z by 180 degrees.
  - **Timing & Playback**: The `ease-in-out` timing function ensures smooth deceleration at the end of each flip. The `infinite` iteration count loops it endlessly.
  - **Interactivity (`animation-play-state`)**: The animation can be paused on hover or via JavaScript click events by setting `animation-play-state: paused`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Neon Glow** | CSS `box-shadow` & `border` | Combining standard and `inset` box shadows perfectly emulates a glowing light tube without needing SVG filters. |
| **3D Tumbling** | CSS `@keyframes` with `transform` | `rotateX`, `rotateY`, and `rotateZ` trigger GPU hardware acceleration, guaranteeing smooth 60fps animations without any JavaScript overhead. |
| **Play/Pause Toggle** | JS Event Listeners + CSS `animation-play-state` | Using `animation-play-state` retains the animation's exact progress frame when paused, rather than resetting it, which is the proper way to pause CSS sequences. |
| **Layout** | Flexbox | Safely centers the loader and dynamic text vertically and horizontally, replacing rigid absolute positioning. |

> **Feasibility Assessment**: 100%. The exact visual glow, 3-axis rotation sequence, and play-state interactivity demonstrated in the tutorial can be perfectly reproduced using pure CSS and minimal vanilla JavaScript.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Initializing system assets. Please wait...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Tumbling Loader visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716" # Very deep, dark blue
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Neon Tumbling Loader */
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
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    position: relative;
}}

/* Text Content */
.text-wrapper {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* Loader Core Styles */
.loader-wrapper {{
    height: 100px; /* fixed height container to prevent layout shifting during rotation */
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px; /* Optional: adds subtle 3D depth to the transform */
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Dual box shadow for neon glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* Animation Configuration */
    animation-name: tumbling;
    animation-duration: 2.5s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    
    /* Ensure play-state transitions are smooth */
    transition: transform 0.2s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

/* Dim glow slightly on hover when paused */
.loader:hover {{
    box-shadow: 0 0 6px var(--accent), inset 0 0 6px var(--accent);
    opacity: 0.8;
}}

/* Core 3D Keyframes Extraction */
@keyframes tumbling {{
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

/* Controls */
.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1.5rem;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
}}

button:hover {{
    background: var(--text);
    color: var(--bg);
}}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation: none;
        border-style: dashed;
        border-width: 4px;
        box-shadow: none;
        transform: rotate(45deg);
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
    <div class="container" role="status" aria-live="polite">
        
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="loader-wrapper">
            <!-- The tumbling shape -->
            <div class="loader" id="loaderElement" title="Hover to pause"></div>
        </div>

        <div class="controls">
            <button id="playBtn">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Tumbling Loader - Interactive Logic
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loaderElement');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Button controls using animationPlayState
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    // Hover interaction as demonstrated in the tutorial
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
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements (borders, box-shadows)?
- [x] Are `title_text` and `body_text` implemented correctly?
- [x] Does the JavaScript run without console errors (clean event listeners updating `animationPlayState`)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's 3D rotating neon square?

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - The outer container utilizes `role="status"` and `aria-live="polite"` so screen readers will announce the loading text implicitly.
  - A comprehensive `@media (prefers-reduced-motion: reduce)` media query is included. If a user prefers reduced motion, the keyframe animation is entirely disabled and replaced with a static 45-degree diamond with dashed borders to signify a "working" state without dizzying rotations.
* **Performance**:
  - CSS animations on `transform` are passed to the GPU (Hardware Acceleration), meaning this loader avoids the main UI thread. It operates at a smooth 60/120fps regardless of JS calculation blocks happening elsewhere on the page.
  - Note: Modifying `box-shadow` sizes inside `@keyframes` can be highly unperformant, but since the glow parameters stay static and we are *only* keyframing the `transform` properties, this component remains incredibly efficient.