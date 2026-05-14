# Continuous Multi-Stage Keyframe Sequence

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Continuous Multi-Stage Keyframe Sequence

* **Core Visual Mechanism**: Defining complex, seamless looping animations using CSS `@keyframes` with explicit percentage waypoints (e.g., `0%`, `25%`, `50%`, `75%`, `100%`). This allows an element to transition through multiple distinct states (simultaneous color shifting and spatial translation) in a single animation cycle, specifically engineered to loop smoothly back to its origin without visually jarring jumps.

* **Why Use This Skill (Rationale)**: While simple `from`/`to` animations are great for single-state changes, percentage-based keyframes allow for choreographing complex motion paths and color evolutions. By explicitly defining the return journey within the keyframes (e.g., moving out to 300px at 50%, then back to 0px at 100%), developers gain precise control over the animation arc, which is essential for custom loading indicators, ambient background effects, and continuous attention-drawing widgets.

* **Overall Applicability**: Ideal for custom progress indicators, playful loading screens, ambient UI elements that need to signal "system active/processing", onboarding highlights, and interactive data visualization nodes.

* **Value Addition**: Transforms static or strictly linear elements into dynamic, multi-phasic visual experiences. It demonstrates how CSS alone can handle complex motion choreography that might otherwise require JavaScript libraries like GSAP, reducing payload and utilizing native browser optimization.

* **Browser Compatibility**: Fully supported in all modern browsers. CSS animations (`@keyframes`, `animation` shorthand, `transform`) have universal support (minimum IE10, but practically all evergreen browsers today).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Animated Subject**: A distinct geometric shape (e.g., a square or pill-shaped div) that acts as the focal point.
  - **Color Logic**: A spectrum shift. In the tutorial, it moves through Red -> Green -> Blue -> Yellow -> Red. In a modern UI, this translates to moving through a cohesive gradient or brand palette (e.g., Primary Accent -> Secondary Accent -> Tertiary -> back to Primary).
  - **CSS Properties**: 
    - `transform: translate()` for GPU-accelerated spatial movement.
    - `background-color` for state changes.
    - `animation` shorthand combining `name`, `duration` (e.g., `4s`), `timing-function` (`ease-in-out`), `delay` (`1s`), `iteration-count` (`infinite`), and `direction` (`alternate` or `normal`).

* **Step B: Layout & Compositional Style**
  - **Layout System**: A relative container establishing spatial bounds (a "track"), with the animated element moving within it. 
  - **Proportions**: The movement must be scaled to its container. For instance, translating from `0px` to `300px` requires a container wide enough to accommodate the motion without overflow, or using percentage-based translations (`transform: translateX(100%)`).

* **Step C: Interactive Behavior & Animations**
  - **Keyframe Arc**: 
    - `0%`: Origin position, base color.
    - `25%`: Intermediate position 1, color shift 1.
    - `50%`: Maximum extension, color shift 2.
    - `75%`: Return intermediate position, color shift 3.
    - `100%`: Back to origin, base color (ensures a seamless `infinite` loop without snapping).
  - **Timing**: `ease-in-out` softens the start and end of the entire sequence, though interpolation between individual percentage steps happens automatically.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Complex motion arc** | CSS `@keyframes` with percentages | Allows for precise multi-step choreography (0%, 25%, 50%, 75%, 100%) as demonstrated in the tutorial. |
| **Spatial movement** | CSS `transform: translateX` | Hardware/GPU accelerated, avoids layout thrashing compared to animating `margin` or `left`. |
| **Animation parameters** | CSS `animation` shorthand | Cleanly groups duration, timing, iteration count, and direction into a single line. |
| **Interactivity (Play/Pause)** | JavaScript DOM toggling | Adds practical value by allowing the user to pause/play the CSS animation via `animation-play-state`. |

> **Feasibility Assessment**: 100% reproduction. The code perfectly encapsulates the multi-stage, percentage-based CSS keyframe animation taught in the tutorial, elevated into a modern, reusable "Activity Tracker" UI component.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "System Activity Monitor",
    body_text: str = "Demonstrating multi-stage CSS keyframes with spatial translation and color morphing.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Multi-Stage Keyframe Animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        track_bg = "#334155"
        # Animation spectrum colors (modernized from Red/Green/Blue/Yellow)
        c_start = accent_color
        c_mid1 = "#10b981" # Emerald
        c_mid2 = "#8b5cf6" # Violet
        c_mid3 = "#f59e0b" # Amber
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        track_bg = "#e2e8f0"
        c_start = accent_color
        c_mid1 = "#059669" 
        c_mid2 = "#6d28d9" 
        c_mid3 = "#d97706" 

    # === CSS ===
    css = f"""/* Continuous Multi-Stage Activity Pulse */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --track-bg: {track_bg};
    
    /* Animation Color Spectrum */
    --color-0: {c_start};
    --color-25: {c_mid1};
    --color-50: {c_mid2};
    --color-75: {c_mid3};
    --color-100: {c_start};
    
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.widget-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background: var(--card-bg);
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 40px;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.025em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* The Track */
.animation-track {{
    width: 100%;
    height: 80px;
    background: var(--track-bg);
    border-radius: 40px;
    position: relative;
    padding: 10px;
    /* Box shadow for depth */
    box-shadow: inset 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

/* The Animated Element */
.animated-node {{
    width: 60px;
    height: 60px;
    background-color: var(--color-0);
    border-radius: 50%;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
    
    /* 
       Applying the multi-stage animation:
       name: complexPath
       duration: 6s
       timing-function: ease-in-out
       delay: 0s
       iteration-count: infinite
       direction: normal (relies on keyframes to loop back)
    */
    animation: complexPath 6s ease-in-out infinite;
}}

/* Pause utility class toggled by JS */
.animated-node.paused {{
    animation-play-state: paused;
}}

/* 
  The Core Skill: Percentage-based Keyframes 
  Translating across the track while shifting colors.
  We use calc() to ensure it stays within the parent track relative to its own size.
*/
@keyframes complexPath {{
    0% {{
        transform: translateX(0);
        background-color: var(--color-0);
    }}
    25% {{
        /* Move 25% across the track */
        transform: translateX(calc((100vw * 0.25) - 40px)); /* fallback */
        transform: translateX(calc((var(--container-width) - 180px) * 0.25));
        background-color: var(--color-25);
    }}
    50% {{
        /* Max extension - move to the far right */
        transform: translateX(calc(var(--container-width) - 180px));
        background-color: var(--color-50);
    }}
    75% {{
        /* Return journey intermediate step */
        transform: translateX(calc((var(--container-width) - 180px) * 0.4));
        background-color: var(--color-75);
    }}
    100% {{
        /* Seamless return to origin */
        transform: translateX(0);
        background-color: var(--color-100);
    }}
}}

/* Controls */
.controls {{
    display: flex;
    justify-content: center;
    gap: 16px;
}}

button {{
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    background: var(--track-bg);
    color: var(--text-color);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--color-50);
    color: white;
    transform: translateY(-2px);
}}

button:active {{
    transform: translateY(0);
}}

/* Responsive adjustments */
@media (max-width: 850px) {{
    .widget-container {{ width: 90%; padding: 32px; }}
    @keyframes complexPath {{
        0% {{ transform: translateX(0); background-color: var(--color-0); }}
        25% {{ transform: translateX(calc((90vw - 120px) * 0.25)); background-color: var(--color-25); }}
        50% {{ transform: translateX(calc(90vw - 120px)); background-color: var(--color-50); }}
        75% {{ transform: translateX(calc((90vw - 120px) * 0.4)); background-color: var(--color-75); }}
        100% {{ transform: translateX(0); background-color: var(--color-100); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- The core animation staging area -->
        <div class="animation-track">
            <div class="animated-node" id="targetNode"></div>
        </div>

        <div class="controls">
            <button id="toggleBtn">Pause Animation</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Behavior for Multi-Stage Animation
document.addEventListener('DOMContentLoaded', () => {{
    const node = document.getElementById('targetNode');
    const toggleBtn = document.getElementById('toggleBtn');
    
    let isPlaying = true;

    // Toggle animation-play-state
    toggleBtn.addEventListener('click', () => {{
        if (isPlaying) {{
            node.classList.add('paused');
            toggleBtn.textContent = 'Play Animation';
        }} else {{
            node.classList.remove('paused');
            toggleBtn.textContent = 'Pause Animation';
        }}
        isPlaying = !isPlaying;
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
  - **Reduced Motion**: For production environments, it is highly recommended to wrap the `@keyframes` assignment in a `@media (prefers-reduced-motion: reduce)` query to set `animation: none;` for users sensitive to continuous motion.
  - **Color Contrast**: The derived theme ensures sufficient contrast between the text and background elements. The animated node uses vibrant colors that stand out against the muted track background.
* **Performance**:
  - **Hardware Acceleration**: The animation strictly utilizes `transform: translateX(...)` and `background-color`. Browsers can offload `transform` and `opacity` operations to the GPU, making the animation butter-smooth (60fps) without triggering layout recalculations (reflows) or repaints of the layout tree.
  - **Resource Usage**: Pure CSS animations are computationally cheap. Because JavaScript is only used to toggle a class state (not to calculate per-frame positions), the main thread remains entirely unblocked.