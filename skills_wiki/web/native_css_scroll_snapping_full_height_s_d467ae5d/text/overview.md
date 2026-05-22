# Native CSS Scroll Snapping (Full-Height Sections)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Native CSS Scroll Snapping (Full-Height Sections)

* **Core Visual Mechanism**: Snapping scroll positions to specific alignment points (like the start of a section) using native CSS `scroll-snap-type` and `scroll-snap-align`. The result is a rigid, presentation-like transition between full-screen blocks of content, preventing the viewport from ever settling "half-way" between sections.
* **Why Use This Skill (Rationale)**: From a UX perspective, it chunks information into distinct, digestible pieces. By forcing the viewport to snap to the top of the next block, it ensures the user always views the content exactly as the designer composed it, without clipping headers or awkward half-visible text.
* **Overall Applicability**: Highly effective for narrative-driven landing pages, fullscreen image/portfolio galleries, presentation decks built in HTML, and immersive storytelling articles.
* **Value Addition**: Previously, this effect required heavy JavaScript libraries (like fullPage.js) that intercepted scroll wheel events and manually animated the window position. Native CSS scroll snapping is significantly lighter, retains native momentum scrolling, perfectly supports mobile swipe gestures, and runs on the browser's compositor thread for maximum performance.
* **Browser Compatibility**: Excellent. Supported in all modern browsers (Chrome 69+, Safari 11+, Firefox 68+, Edge 79+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Scroll Container**: The parent wrapper that has a fixed height (e.g., `100vh`) and is set to `overflow-y: scroll`.
  - **Snap Targets (Sections)**: Child elements that take up exactly 100% of the container's height. 
  - **Color Logic**: High contrast alternating background colors (e.g., a dark grey `#1a1a2e` alternating with an accent color `#e63946`) strictly delineate the boundaries of each section, making the snap action feel more impactful.

* **Step B: Layout & Compositional Style**
  - **Layout system**: The container limits the viewport size. Inside each section, CSS Flexbox is used (`display: flex; align-items: center; justify-content: center;`) to ensure the text content is perfectly centered regardless of the screen size.
  - **Sizing**: Sections are set to `height: 100%; width: 100%;` so they match the parent container precisely.

* **Step C: Interactive Behavior & Animations**
  - **Scroll Snapping**: 
    - Parent: `scroll-snap-type: y mandatory;` forces the scrollbar to *always* land on a snap point along the vertical axis.
    - Child: `scroll-snap-align: start;` tells the browser that the top of the section should align with the top of the container.
  - **Smooth Scrolling**: Applying `scroll-behavior: smooth;` ensures that if a user clicks an anchor link to jump between sections, the browser glides to it rather than jumping instantly.
  - **No JS Required**: The entirely visual snapping behavior is handled natively by the CSS layout engine.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Section-to-section jumping | CSS `scroll-snap-type` | Native, performant API that avoids scroll-listener jank and JS math. |
| Centered typography | CSS Flexbox | Simplest and most robust way to perfectly center content inside full-height blocks. |
| Alternating section colors | CSS `:nth-child` | Clean, HTML-agnostic way to stripe colors across repetitive elements. |

> **Feasibility Assessment**: 100% reproduction. The core visual behavior in the tutorial relies entirely on standard CSS properties, which can be fully replicated without any external dependencies.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Scroll Snapping",
    body_text: str = "Scroll down to see the snapping effect in action. This section aligns perfectly to the top.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native CSS Scroll Snapping effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        body_bg = "#090a0f"
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
    else:
        body_bg = "#e9ecef"
        bg_color = "#ffffff"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* CSS Scroll Snapping — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--body-bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Prevent the body from scrolling so only the component scrolls */
    overflow: hidden; 
}}

/* The Scrolling Container */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    
    /* Enable vertical scrolling */
    overflow-y: scroll;
    /* Hide scrollbar for cleaner look (optional, but nice for components) */
    scrollbar-width: none; 
    
    /* The Magic: Force scroll to snap on the Y axis */
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}}

.container::-webkit-scrollbar {{
    display: none;
}}

/* The Snap Targets */
.section {{
    /* Match the container's height so it fills the view exactly */
    height: 100%;
    width: 100%;
    
    /* The Magic: Tell the container where to snap to this element */
    scroll-snap-align: start;
    /* Prevent snapping to the middle of the element if user scrolls fast */
    scroll-snap-stop: always;
    
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Alternating Color Logic */
.section:nth-child(odd) {{
    background: var(--bg);
    color: var(--text);
}}

.section:nth-child(even) {{
    background: var(--accent);
    color: #ffffff; /* High contrast text on accent */
}}

/* Typography */
.content {{
    max-width: 800px;
    text-align: center;
}}

.content h2 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.content p {{
    font-size: 1.25rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Responsive text scaling */
@media (max-width: 768px) {{
    .content h2 {{ font-size: 2.5rem; }}
    .content p {{ font-size: 1.1rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Section 1 -->
        <section class="section">
            <div class="content">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>
        </section>
        
        <!-- Section 2 -->
        <section class="section">
            <div class="content">
                <h2>Section Two</h2>
                <p>The second section snaps securely into place. Notice how the container refuses to let you rest halfway between the two backgrounds.</p>
            </div>
        </section>
        
        <!-- Section 3 -->
        <section class="section">
            <div class="content">
                <h2>Section Three</h2>
                <p>Because we use <code>scroll-snap-type: mandatory</code>, the browser calculates the closest snap point and automatically glides the user to perfect alignment.</p>
            </div>
        </section>
        
        <!-- Section 4 -->
        <section class="section">
            <div class="content">
                <h2>Native & Performant</h2>
                <p>No JavaScript is required for this logic. Scrolling remains hardware-accelerated and perfectly supports touch-swipes on mobile devices.</p>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for the scroll snapping logic.
// This file is included to satisfy component structure requirements.
document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Scroll Snapping Component Loaded Successfully.");
});
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

* **Accessibility (a11y)**: 
  - `scroll-snap-type: mandatory` can occasionally cause issues for users with motor control impairments who rely on trackpad clicking or small scroll-wheel movements, as it can forcefully "snap back" if they don't scroll far enough. In highly accessible applications, consider using `scroll-snap-type: y proximity` instead, which only snaps if the user gets *close* to the boundary, offering a more forgiving experience.
  - Keyboard navigation (Page Down, Spacebar, Arrow Keys) natively integrates with CSS scroll snapping without extra configuration, meaning screen reader users or keyboard-only users will experience perfectly aligned sections when tabbing through.
* **Performance**:
  - CSS scroll snapping acts entirely on the browser's compositor thread. It is infinitely more performant than listening to JavaScript `wheel` or `scroll` events and mutating inline `transform` styles, avoiding completely the main-thread blocking jank associated with old JS parallax/scroll-jacking libraries.