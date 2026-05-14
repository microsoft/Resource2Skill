# Circular Neon Spinner

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Circular Neon Spinner

* **Core Visual Mechanism**: A pure CSS loading indicator featuring a continuous rotating arc over a dark, track-like background. The effect is achieved by applying a solid circular border to a pseudo-element, coloring one side (the top border) with a vibrant accent color, and spinning it infinitely using a linear CSS keyframe animation. Wide-tracked uppercase text sits perfectly centered inside the ring.

* **Why Use This Skill (Rationale)**: The circular geometry universally signals a "waiting" or "processing" state. The use of a thick track and a neon-like highlight creates a modern, technological aesthetic, while the wide letter spacing gives the typography a cinematic or dashboard-like feel. Because it relies purely on CSS borders and rotation, it is extremely performant and resolution-independent.

* **Overall Applicability**: Ideal for asynchronous data fetching states, full-screen loading overlays, form submission indicators, and futuristic UI dashboards (like SaaS platforms or gaming interfaces). 

* **Value Addition**: Compared to standard GIF spinners or default browser loading icons, this provides a highly customizable, crisp, and brandable element that scales flawlessly to any dimension without loss of fidelity.

* **Browser Compatibility**: Excellent. Relies on standard CSS Level 3 properties (`border-radius`, `transform`, `@keyframes`, flexbox), supported by all modern browsers.

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: 
    - Base background: Dark charcoal (`#262626`)
    - Ring track: Near-black (`#131313`)
    - Accent highlight & Text: Vibrant Cyan (`#2196f3`)
  - **Typography**: San-serif, uppercase, heavily spaced (`letter-spacing: 5px`), and relatively large (`40px` in the tutorial).
  - **CSS Properties**: `border-radius: 50%` creates the circle; `border` creates the track, and `border-top` creates the moving playhead. 

* **Step B: Layout & Compositional Style**
  - The component consists of a square bounding container (`350px` by `350px`).
  - Flexbox is used to perfectly center the text horizontally and vertically within the container.
  - An absolute-positioned `::before` pseudo-element stretches to fill the container, holding the actual spinning border. This separates the spinning animation from the static text, preventing the text from spinning.

* **Step C: Interactive Behavior & Animations**
  - **Animation**: `@keyframes spin` rotating from `0deg` to `360deg`.
  - **Timing Function**: `linear` is crucial here. Unlike `ease` or `ease-in-out` which would cause a stuttering speed-up/slow-down effect, `linear` ensures a seamless, infinite loop.
  - **Duration**: `2s` per full rotation.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Spinner Ring | CSS `border` + `border-radius: 50%` | Safest, most performant way to draw circular rings in pure CSS without requiring SVG. |
| Ring Highlight | CSS `border-top` | Overriding one side of the border naturally creates a 90-degree arc highlight. |
| Spinning Motion | CSS `@keyframes` (`transform: rotate`) | Hardware-accelerated, runs on the compositor thread for maximum 60fps smoothness. |
| Text Centering | CSS Flexbox | Cleaner and more robust than the tutorial's hardcoded negative pixel offsets. |

*Feasibility Assessment*: 100% reproduction. The logic has been refactored to be more robust (using Flexbox and absolute positioning `inset: 0` instead of rigid pixel offsets), ensuring the component scales properly if dimensions change.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading...",
    body_text: str = "", # Unused in this specific layout, but preserved for signature
    color_scheme: str = "dark",
    accent_color: str = "#2196f3",
    width_px: int = 350,
    height_px: int = 350,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Circular Neon Spinner effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#262626"
        ring_bg = "#131313"
        text_color = accent_color
    else:
        bg_color = "#f8f9fa"
        ring_bg = "#e0e0e0"
        text_color = accent_color

    # === CSS ===
    css = f"""/* Circular Neon Spinner */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --ring-bg: {ring_bg};
    --accent: {accent_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.loading-container {{
    width: var(--width);
    height: var(--height);
    /* Ensure it remains square on small viewports */
    max-width: 90vw;
    max-height: 90vw;
    aspect-ratio: 1 / 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The Spinning Ring */
.loading-container::before {{
    content: '';
    position: absolute;
    inset: 0; /* shorthand for top:0; left:0; width:100%; height:100% */
    border: 10px solid var(--ring-bg);
    border-top: 10px solid var(--accent);
    border-radius: 50%;
    animation: spin 2s linear infinite;
}}

.loading-text {{
    color: var(--text);
    /* Scale font down on smaller screens */
    font-size: clamp(16px, calc(var(--width) * 0.1), 40px);
    letter-spacing: 5px;
    text-transform: uppercase;
    font-weight: 500;
    
    /* Counteract the off-center effect caused by trailing letter-spacing */
    padding-left: 5px; 
    z-index: 1; /* Keeps text above the ring if overlapping */
}}

@keyframes spin {{
    0% {{
        transform: rotate(0deg);
    }}
    100% {{
        transform: rotate(360deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading-container" aria-busy="true" aria-label="Loading">
        <div class="loading-text">{title_text}</div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Circular Neon Spinner
// Pure CSS implementation. JS provided for structure.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Spinner initialized.");
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
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

---

### 4. Accessibility & Performance Notes

* **Accessibility**: Added `aria-busy="true"` and `aria-label="Loading"` to the container HTML. This ensures screen readers correctly interpret the element's purpose, since "LOADING..." is just text and could be missed as a system state.
* **Performance**: The animation is highly optimized because it only animates the `transform` property. This triggers GPU hardware acceleration and prevents expensive layout/paint recalculations per frame, resulting in a smooth, low-battery-drain loop.
* **Responsive Robustness**: By using `clamp()` for the font size and `aspect-ratio: 1 / 1` paired with `max-width: 90vw`, the component prevents overflowing on mobile viewports while staying faithful to the large `350px` design on desktop.