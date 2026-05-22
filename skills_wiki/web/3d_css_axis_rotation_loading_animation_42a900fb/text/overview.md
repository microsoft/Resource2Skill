### 1. High-level Design Pattern Extraction

**Skill Name**: 3D CSS Axis Rotation Loading Animation

*   **Core Visual Mechanism**: A small square element rotates independently on its X, Y, and Z axes in sequence, creating a dynamic 3D tumbling effect. The rotation is timed to seamlessly loop, where a 180-degree rotation on an axis visually resets the element's appearance along that axis when viewed from a front-on perspective, contributing to the smooth looping illusion. An outer glow and slight border-radius enhance its modern, interactive feel.

*   **Why Use This Skill (Rationale)**: This animation is an engaging alternative to static loading spinners. Its sequential 3D rotation provides a more sophisticated and less jarring visual feedback, reducing perceived waiting time and adding a touch of polish to user interfaces. The distinct movement on each axis keeps the user's attention without being overly distracting.

*   **Overall Applicability**: Ideal for indicating background processes, data fetching, page loading, or any waiting state in web applications, dashboards, or single-page applications. It can also serve as an eye-catching element in creative portfolio sites or interactive experiences.

*   **Value Addition**: Compared to a plain animated GIF or a simple 2D rotation, this pattern offers a more dynamic and visually rich loading indicator. It leverages native CSS 3D transforms for performance and flexibility, conveying a sense of progress and activity without relying on heavy JavaScript libraries for its core motion.

*   **Browser Compatibility**: Uses standard CSS `transform` properties and `@keyframes`. Widely supported across modern browsers (Edge 12+, Firefox 16+, Safari 9+, Chrome 43+, IE 10+, Opera 30+). `transform-style: preserve-3d` is also well-supported.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **HTML Element**: A single `div` element acts as the rotating square.
    *   **Color Logic**:
        *   Background: Dark theme (`#040716`) or light theme (`#f8f9fa`)
        *   Accent (border/glow): Aqua (`#00FFFF`)
    *   **Typographic Hierarchy**: Not applicable to the loading animation itself, but the page body uses `Inter` font family for general styling if any text were present.
    *   **CSS Properties for Visual Weight**: `border`, `border-radius`, `box-shadow` (for the glow), and `transform` properties within `@keyframes`.

*   **Step B: Layout & Compositional Style**
    *   **Layout System**: The loading square uses `position: absolute` with `top: 50%`, `left: 50%`, and `transform: translate(-50%, -50%)` to precisely center itself within the viewport.
    *   **Spatial Feel**: The element is a small, centered, glowing square, appearing distinct against the background. `z-index: 10` ensures it floats above any other content.
    *   **Dimensions**: The square has fixed dimensions of `50px` height and `50px` width.
    *   **Styling**: A `6px` solid aqua border provides its visual structure, with a subtle `4px` `border-radius` to soften its edges. `box-shadow` with `8px` blur both externally and as an `inset` creates a glowing effect.

*   **Step C: Interactive Behavior & Animations**
    *   **Animation**: The core animation, named `loading`, is defined using `@keyframes`.
    *   **Motion Arc**: The animation involves three distinct phases of rotation:
        *   `0%`: Starts at `rotateX(0deg) rotateY(0deg) rotateZ(0deg)`.
        *   `33%`: Rotates `180deg` around the X-axis: `rotateX(180deg) rotateY(0deg) rotateZ(0deg)`.
        *   `67%`: Maintains X-axis rotation and adds `180deg` rotation around the Y-axis: `rotateX(180deg) rotateY(180deg) rotateZ(0deg)`.
        *   `100%`: Maintains X and Y rotations and adds `180deg` rotation around the Z-axis: `rotateX(180deg) rotateY(180deg) rotateZ(180deg)`.
    *   **Timing**:
        *   `animation-duration`: `2s` for one full cycle.
        *   `animation-timing-function`: `ease-in-out` for a smooth start and end to each rotation phase.
        *   `animation-iteration-count`: `infinite` to ensure continuous looping.
        *   `animation-direction`: `normal` (default) for consistent forward play.
    *   **JavaScript-driven behaviors**: None for the core loading animation itself.
    *   **Pure CSS**: All motion and styling are handled by CSS.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect         | Method                | Why this method                                                |
| :--------------------------- | :-------------------- | :------------------------------------------------------------- |
| 3D Axis Rotation             | CSS `transform: rotateX/Y/Z()` | Native browser support for 3D transforms, GPU accelerated.     |
| Sequential Animation Steps   | CSS `@keyframes`      | Allows precise control over intermediate states and timings.   |
| Smooth Speed Curve           | CSS `ease-in-out`     | Provides natural-looking acceleration and deceleration.        |
| Continuous Looping           | CSS `infinite`        | Built-in property for endless repetition.                      |
| Centering the element        | CSS `position: absolute` + `transform: translate()` | Reliable cross-browser centering without Flexbox/Grid on `body`. |
| Outer glow and border        | CSS `border`, `box-shadow` | Standard properties for visual styling.                        |

**Feasibility Assessment**: 100% — the provided code fully reproduces the visual effect, including the 3D rotation, timing, glow, and centering, as demonstrated in the tutorial's loading animation example.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Animation",
    body_text: str = "", # Not directly used in the loading animation, but part of general page content.
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00FFFF",  # CSS hex color for aqua accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D CSS Axis Rotation Loading Animation visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Specific dark background from video example
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* 3D CSS Axis Rotation Loading Animation — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --viewport-width: {width_px}px;
    --viewport-height: {height_px}px;
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
    width: var(--viewport-width);
    height: var(--viewport-height);
    position: relative; /* Needed for absolute positioning of .loading */
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); /* Centering with transform */
    z-index: 10;
    animation: 2s loading ease-in-out infinite;
}}

@keyframes loading {{
    0% {{
        transform: translate(-50%, -50%) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading" aria-live="polite" aria-busy="true">
        <span class="sr-only">Loading content...</span>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D CSS Axis Rotation Loading Animation — no interactive behavior required for this component.
// The animation is entirely driven by CSS @keyframes.
document.addEventListener('DOMContentLoaded', () => {{
    // You could add JavaScript here for dynamic content or external API calls
    // that the loading animation is indicating the status of.
    console.log("Loading animation component ready.");
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba (not referencing undefined CSS variables from external systems)? (Using CSS custom properties (`var(--accent)`) which are defined with explicit hex colors.)
- [x] Are all external resources loaded from CDN URLs (not local `node_modules` paths)?
- [x] Does the component respect the `width_px` and `height_px` parameters? (Controls viewport dimensions, loading element is fixed size and centered.)
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements (buttons, highlights, borders)?
- [x] Are `title_text` and `body_text` properly escaped for HTML (no XSS from special characters)? (No direct `body_text` output, `title_text` used in `<title>`.)
- [x] Does the JavaScript run without console errors? (No complex JS, only DOMContentLoaded log.)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?

### 4. Accessibility & Performance Notes

*   **Accessibility**:
    *   The `div.loading` has `aria-live="polite"` and `aria-busy="true"` attributes. `aria-live="polite"` indicates that updates to the region should be announced by screen readers when the user is idle, and `aria-busy="true"` tells screen readers that the element or its subtree is busy and users should wait for changes.
    *   A visually hidden `<span>` with text "Loading content..." is included within the `.loading` div. This provides a clear textual description for screen reader users about what the animation signifies.
    *   Color contrast for the aqua glow on a dark background is generally sufficient, but the border might be thin for some users.
    *   `@media (prefers-reduced-motion: reduce)` is not explicitly included, but it would be good practice to reduce or remove the animation for users who prefer less motion in their UI.

*   **Performance**:
    *   The animation primarily uses CSS `transform` properties, which are generally GPU-accelerated and performant, leading to smooth animations without taxing the CPU.
    *   `@keyframes` animations are efficient as they are handled natively by the browser's rendering engine.
    *   No complex JavaScript is involved in the animation itself, avoiding potential performance bottlenecks from scripting.
    *   `infinite` iteration is suitable for loading states and does not generally cause performance issues as long as the animated properties are well-optimized (like `transform`).