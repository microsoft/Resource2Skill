### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon 3D Rotating Loader

* **Core Visual Mechanism**: This pattern creates a faux-3D rotating cube effect using purely 2D elements and 3D CSS transforms. It relies on a multi-stage `@keyframes` sequence that rotates an element sequentially along its X, Y, and Z axes (33%, 67%, 100% keyframes). This is paired with an inset and outset `box-shadow` on a transparent element with a solid border to create a "neon hollow square" aesthetic.
* **Why Use This Skill (Rationale)**: Loading animations can often be tedious for users. A visually engaging, hardware-accelerated CSS loader captures the user's attention without blocking the main JavaScript thread. The 3D rotation provides a sense of continuous progression, and the neon glow adds a modern, polished tech aesthetic. Furthermore, tying the `animation-play-state` to user interactions (like hover or button clicks) gives the user a sense of control over the UI.
* **Overall Applicability**: Ideal for initial app loading screens, data-fetching indicators in dashboards, or processing states in futuristic, tech-oriented, or dark-mode SaaS applications.
* **Value Addition**: Compared to a standard static "Loading..." text or a basic rotating SVG spinner, this component utilizes hardware-accelerated 3D CSS transforms, making it incredibly performant while delivering a high visual impact. It demonstrates mastery over the CSS `animation` shorthand and spatial manipulation.
* **Browser Compatibility**: Broadly supported. CSS `transform` (including 3D transforms like `rotateX`), `animation`, and `box-shadow` are supported in all modern browsers (Chrome 36+, Firefox 16+, Safari 9+, Edge).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Shape & Style**: A perfectly square HTML `<div>` with a transparent background.
  - **Border**: A solid border (e.g., `6px solid var(--accent)`).
  - **Glow Logic**: Dual box-shadows. An outset shadow (`0 0 8px var(--accent)`) and an inset shadow (`inset 0 0 8px var(--accent)`) to create a convincing neon tube effect.
  - **Color Logic**: Best suited for dark backgrounds. For example, background `#040716` (deep navy) with an aqua/cyan accent `#00ffff`.

* **Step B: Layout & Compositional Style**
  - **Container**: Centered using modern CSS Flexbox or Grid (though the original tutorial used absolute positioning, Flex/Grid is more robust for component extraction).
  - **Proportions**: The loader itself is relatively small (50px by 50px) to maintain a tight, sharp glow and quick, snappy rotations without looking unwieldy.

* **Step C: Interactive Behavior & Animations**
  - **Keyframes (`loading`)**:
    - `0%`: Start state (no rotation).
    - `33%`: Rotate X by 180deg.
    - `67%`: Keep X at 180deg, add Y rotation by 180deg.
    - `100%`: Keep X and Y at 180deg, add Z rotation by 180deg.
  - **Animation Properties**: 
    - `duration`: 2 seconds (fast enough to be dynamic, slow enough to track).
    - `timing-function`: `ease-in-out` (creates a snappy, physics-based stop-and-go feel for each flip).
    - `iteration-count`: `infinite` (loops forever).
  - **Interactivity**: Pauses on hover (`animation-play-state: paused`), and can be controlled via JavaScript buttons.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| 3D Rotating Animation | Pure CSS `@keyframes` with `transform: rotate3d` | GPU-accelerated, incredibly performant, requires zero JavaScript overhead to render. |
| Neon Glow | CSS `box-shadow` (inset + outset) | Native way to create soft light falloff around and inside a bordered element. |
| Play/Pause Interactivity | CSS `:hover` + JS DOM manipulation | CSS handles the hover state trivially, while JS event listeners manipulating `style.animationPlayState` perfectly reproduce the video's interactive lesson. |

> **Feasibility Assessment**: 100% of the tutorial's final loading effect and its associated JS interactivity concepts are reproduced using modern, self-contained CSS and JS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Masterclass",
    body_text: str = "Hover over the loader to pause it, or use the controls below.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon 3D Rotating Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark navy from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Neon 3D Rotating Loader — generated component */
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
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    background: var(--surface);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

.title {{
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.body-text {{
    margin-bottom: 3rem;
    color: var(--text);
    opacity: 0.8;
    font-size: 0.95rem;
}}

/* --- Core Visual Effect Styles --- */
.loading-wrapper {{
    height: 100px; /* Give it space to rotate without hitting other elements */
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 3rem;
}}

.loader {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    /* Shorthand: name | duration | timing-function | delay | iteration-count | direction | fill-mode | play-state */
    animation: loading3D 2s ease-in-out infinite;
    cursor: pointer;
}}

/* Pause on hover as taught in the tutorial */
.loader:hover {{
    animation-play-state: paused !important;
}}

/* The precise sequential 3D rotation sequence */
@keyframes loading3D {{
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

/* --- Control Buttons --- */
.controls {{
    display: flex;
    gap: 1rem;
}}

button {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--text);
    padding: 0.6rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--text);
    color: var(--bg);
}}

button.active-btn {{
    border-color: var(--accent);
    color: var(--accent);
}}

button.active-btn:hover {{
    background: var(--accent);
    color: var(--bg);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation-duration: 10s; /* Slow down significantly */
        animation-timing-function: linear;
    }}
}}
"""

    # === HTML ===
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">{safe_title}</h1>
        <p class="body-text">{safe_body}</p>
        
        <div class="loading-wrapper">
            <!-- A11y: Role and aria-label for screen readers -->
            <div class="loader" id="neon-loader" role="status" aria-label="Loading content"></div>
        </div>

        <div class="controls">
            <button id="playButton" class="active-btn">Play</button>
            <button id="pauseButton">Pause</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon 3D Rotating Loader — Interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('neon-loader');
    const playButton = document.getElementById('playButton');
    const pauseButton = document.getElementById('pauseButton');

    // Handle Play button click
    playButton.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        playButton.classList.add('active-btn');
        pauseButton.classList.remove('active-btn');
    }});

    // Handle Pause button click
    pauseButton.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        pauseButton.classList.add('active-btn');
        playButton.classList.remove('active-btn');
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
  - The animated element features `role="status"` and `aria-label="Loading content"` so screen readers can announce the loading state to visually impaired users.
  - A `@media (prefers-reduced-motion: reduce)` block is included. Rather than stopping the animation entirely (which might look like the app has frozen), it significantly slows the animation down (e.g., to 10s) and uses a linear timing function to remove the rapid, jerky 3D flips, providing a much gentler experience.
* **Performance**:
  - The animation relies entirely on the `transform` property (`rotateX`, `rotateY`, `rotateZ`). CSS transforms are pushed to the GPU (Hardware Acceleration) and do not trigger browser layout reflows or repaints, ensuring a buttery-smooth 60fps experience even on lower-end mobile devices.
  - No continuous JavaScript loops (like `requestAnimationFrame`) are used for rendering, saving battery life and keeping the main thread completely free for actual application logic (like fetching the data the loader is waiting for).