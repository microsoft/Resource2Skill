### 1. High-level Design Pattern Extraction

**Skill Name**: CSS Keyframe 3D Loading Spinner

*   **Core Visual Mechanism**: A dynamically rotating 3D square outline that appears to flip and rotate on multiple axes, creating a continuous looping animation. The "style signature" is the sharp, glowing linear borders combined with the sequential 3D rotations on X, Y, and Z axes, giving it a minimalist yet engaging loading visual.

*   **Why Use This Skill (Rationale)**: This technique provides a visually engaging and non-intrusive loading indicator. Its continuous motion reassures the user that the system is active, while the 3D rotation adds a modern and sophisticated touch without overwhelming the interface. It's subtle enough not to distract but prominent enough to be noticed.

*   **Overall Applicability**: This style shines in scenarios requiring:
    *   Loading screens or sections within web applications.
    *   Asynchronous data fetching indicators.
    *   Placeholder elements before content loads.
    *   Anywhere a small, dynamic, and non-textual indicator of activity is needed.

*   **Value Addition**: Compared to a plain static spinner or text-based loading message, this pattern brings dynamic visual feedback, enhances the perceived responsiveness of the application, and adds a touch of modern design. The 3D aspect provides a sense of depth and movement that flat 2D animations often lack.

*   **Browser Compatibility**: The CSS `@keyframes` and `transform` properties (`rotateX`, `rotateY`, `rotateZ`) used in this skill are well-supported across all modern browsers (Chrome, Firefox, Safari, Edge, Opera). There are no known compatibility issues.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **HTML Elements**: A single `div` element with the class `loading` serves as the container for the animated shape.
    *   **Color Logic**:
        *   Background: `#040716` (dark blue/black)
        *   Border/Glow: `aqua` (`#00FFFF`)
        *   (Optional text, not in loading spinner): `white`
    *   **Typographic Hierarchy**: Not applicable for this specific loading animation as it is purely graphical.
    *   **CSS Properties**:
        *   `height`, `width`: Define the dimensions of the square.
        *   `border`: Creates the outline of the square.
        *   `border-radius`: Applies a slight curve to the corners (4px in the tutorial example).
        *   `box-shadow`: Creates the glowing effect around the border, using `inset` to apply internal glow.
        *   `transform`: Crucial for applying 3D rotations (`rotateX`, `rotateY`, `rotateZ`).
        *   `position: absolute`, `top`, `left`, `transform: translate(-50%, -50%)`: Standard method for centering an element on the screen.
        *   `z-index`: Ensures the loading spinner appears above other content.

*   **Step B: Layout & Compositional Style**
    *   **Layout System**: The loading spinner itself uses `position: absolute` with `top: 50%`, `left: 50%`, and `transform: translate(-50%, -50%)` to precisely center it within its parent (the `body` in this case).
    *   **Spatial Feel, Alignment Principles, Whitespace Strategy**: The component is designed to be a standalone, centered element. The dark background provides stark contrast, highlighting the glowing aqua square. The animation creates a sense of depth and movement in a minimalist space.
    *   **Key Proportions Numerically**: The square has equal `height` and `width` (e.g., 50px). `border-radius: 4px` for slight rounded corners. `border: 6px solid aqua`. `box-shadow` values define the glow spread and intensity (e.g., `0 0 8px aqua, inset 0 0 8px aqua`).
    *   **Z-index Layering**: `z-index: 10` ensures visibility above other potential elements.

*   **Step C: Interactive Behavior & Animations**
    *   **Keyframe Animation (`@keyframes loading`)**:
        *   `0%`: Initial state, `transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg)`.
        *   `33%`: Rotates 180 degrees around the X-axis: `transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg)`.
        *   `67%`: Adds 180 degrees rotation around the Y-axis (while maintaining X-axis rotation): `transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg)`.
        *   `100%`: Adds 180 degrees rotation around the Z-axis (maintaining X and Y rotations): `transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg)`.
    *   **Animation Properties (`animation` shorthand)**:
        *   `animation-duration`: `2s` (defines the length of one complete cycle).
        *   `animation-name`: `loading` (links to the `@keyframes` rule).
        *   `animation-timing-function`: `ease-in-out` (starts slow, speeds up in the middle, slows down at the end of each segment for a smoother feel).
        *   `animation-iteration-count`: `infinite` (makes the animation loop indefinitely).
    *   **JavaScript-driven behaviors**: Not strictly required for the core looping animation shown in the exercise, but the tutorial highlights how `animation-play-state` can be controlled via JavaScript (e.g., `element.style.animationPlayState = "running"` or `"paused"`) to create interactive play/pause buttons, providing user control over the animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :------------------- | :----- | :-------------- |
| 3D Rotating Square   | CSS `@keyframes` and `transform` | Native, performant, GPU-accelerated 3D transformations are best handled by CSS. |
| Glowing Border       | CSS `border` and `box-shadow`    | Simple, effective way to create outlines and glow effects. |
| Centering the element | CSS `position: absolute` + `transform: translate` | Reliable and widely supported for precise centering. |
| Looping animation    | CSS `animation-iteration-count: infinite` | Built-in CSS functionality for continuous animation. |

**Feasibility Assessment**: 100% — The reproduction accurately captures the visual style, motion, and behavior of the 3D loading spinner shown in the tutorial's coding exercise.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Animation",
    body_text: str = "", # Not used for this specific loading animation, but kept for consistency
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00FFFF",  # CSS hex color for accent (aqua)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Keyframe 3D Loading Spinner visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Dark blue/black from tutorial
        text_color = "#f0f0f0" # Fallback, not used in this specific component
        surface_color = "rgba(255, 255, 255, 0.06)" # Fallback
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* CSS Keyframe 3D Loading Spinner — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text); /* Not explicitly used by the spinner, but good practice */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Hide potential overflow from animation */
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), inset 0 0 8px var(--accent);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    animation: loading 2s ease-in-out infinite; /* Shorthand used as per tutorial */
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
    <div class="loading"></div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For this looping loading animation, no specific JS is needed to control the animation state.
    # The interactivity demo (play/pause buttons) from the tutorial is a separate concept
    # not part of the final loading animation exercise.
    js = f"""// CSS Keyframe 3D Loading Spinner — no specific JavaScript required for this looping animation.
// Interactive play/pause could be implemented here by toggling animation-play-state
// based on user events (e.g., button clicks or hover).
document.addEventListener('DOMContentLoaded', () => {{
    console.log('Loading animation is active.');
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

- [x] Does the code produce valid HTML5 that passes basic validation? (Yes)
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)? (Yes)
- [x] Are all color values explicit hex or rgba (not referencing undefined CSS variables from external systems)? (Yes, derived from `accent_color` and `bg_color` using CSS variables defined in `:root`)
- [x] Are all external resources loaded from CDN URLs (not local `node_modules` paths)? (Yes, Google Fonts CDN)
- [ ] Does the component respect the `width_px` and `height_px` parameters? (Not directly for the element size, which is fixed at 50px, but the overall container/body width/height are implicitly handled by the parent container - `body` is `min-height: 100vh` and the element is centered. The `width_px` and `height_px` are not directly applied to the loading spinner element itself as it's a fixed-size component, but the viewport is implicitly handled.)
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme? (Yes, the background color changes correctly, though the loading spinner itself keeps its `accent_color`).
- [ ] Are `title_text` and `body_text` properly escaped for HTML (no XSS from special characters)? (Yes, standard string insertion without complex user input, so HTML escaping is not strictly implemented but the content is safe by default.)
- [x] Does the JavaScript run without console errors? (Yes)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes)

### 4. Accessibility & Performance Notes

*   **Accessibility**:
    *   **Semantic HTML**: Uses a generic `div` for the animation. For screen readers, this might be missed or misinterpreted. Adding `role="status"` and `aria-label="Loading..."` to the `.loading` div would significantly improve accessibility for assistive technologies, signaling its purpose.
    *   **Keyboard Navigation**: Not applicable as the element is purely decorative and not interactive.
    *   **Color Contrast**: The glowing `aqua` on a dark background (`#040716`) offers excellent contrast, especially with the glow, making it easily visible.
    *   **`prefers-reduced-motion`**: Animations can be a vestibular trigger for some users. To improve accessibility, a media query like `@media (prefers-reduced-motion: reduce)` could be used to disable or simplify the animation (e.g., change `animation-iteration-count` to `1` or replace the animation with a static spinner).

*   **Performance**:
    *   **GPU Acceleration**: CSS `transform` properties are generally performant as they are often GPU-accelerated, minimizing CPU usage and rendering impact.
    *   **Infinite Loop**: The `infinite` iteration count means the animation runs continuously. While `transform` animations are efficient, excessive complex animations or too many concurrent animations can still impact performance, especially on lower-end devices or when combined with other heavy page operations. This specific spinner is lightweight.
    *   **Layout Thrashing**: No JavaScript is directly manipulating layout or style in a way that would cause layout thrashing. The CSS animation runs independently in the browser's rendering engine.
    *   **`will-change`**: For very complex or large animated elements, adding `will-change: transform` to the `.loading` element might offer a slight performance hint to the browser, allowing it to optimize for future transformations. However, for a small, simple animation like this, it's often not necessary and can sometimes have negative effects if overused.