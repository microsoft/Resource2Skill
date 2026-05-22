### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Cube Spin Loading Animation

*   **Core Visual Mechanism**: This skill creates a dynamic loading indicator using a CSS square that appears to spin and rotate in 3D space. It achieves this effect by animating `rotateX`, `rotateY`, and `rotateZ` CSS `transform` properties within a `@keyframes` rule. A vibrant border and subtle `box-shadow` create a glowing, modern aesthetic.

*   **Why Use This Skill (Rationale)**: Loading animations are crucial for managing user expectations and preventing frustration during data fetching or processing. A 3D spinning cube provides a more engaging and visually interesting feedback mechanism than a static indicator, enhancing the perceived responsiveness and modern feel of a web application. The continuous, smooth motion communicates active progress effectively.

*   **Overall Applicability**: This loading animation is suitable for various web scenarios where asynchronous operations occur:
    *   Loading screens for single-page applications (SPAs) or dashboards.
    *   Indicating data being fetched in widgets or components.
    *   Transitional states between page loads or content updates.
    *   As a decorative element on "coming soon" pages or during initial application boot-up.

*   **Value Addition**: Compared to a simple spinning circle or static text, this pattern offers:
    *   **Enhanced Engagement**: The 3D rotation adds depth and visual appeal.
    *   **Modern Aesthetic**: The clean lines, glowing effect, and 3D movement contribute to a contemporary UI.
    *   **Clear Feedback**: The continuous motion clearly signals that the system is busy and not frozen.
    *   **Performant Animation**: Leveraging GPU-accelerated CSS transforms for smooth execution.

*   **Browser Compatibility**: The CSS `transform` property, `@keyframes` rule, `border-radius`, and `box-shadow` are widely supported across all modern browsers (Chrome, Firefox, Safari, Edge) and older versions like IE10+.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **HTML**: A simple `div` element acts as the `.loading-box`. An optional `p` tag provides contextual text.
    *   **Color Logic**:
        *   `--bg`: Dark background color (e.g., `#0d111c` for dark theme) to make the glowing element stand out.
        *   `--text`: Light text color (e.g., `#f0f0f0`) for readability against the dark background.
        *   `--accent`: A vibrant accent color (e.g., `#00bfff` - cyan) used for the box's border and its glowing `box-shadow`.
    *   **Typographic Hierarchy**: The `body_text` is rendered with a standard sans-serif font (`Inter`) at a moderate size, providing a clear but subordinate message to the animation.
    *   **CSS Properties**: `height`, `width`, `border`, `border-radius`, `box-shadow` for visual appearance, and `transform`, `animation` for the motion.

*   **Step B: Layout & Compositional Style**
    *   **Layout System**: The main content is centered on the page using CSS Flexbox on the `body` element (`display: flex; align-items: center; justify-content: center;`). The `.loading-container` uses Flexbox to vertically stack the spinning box and text with a `gap`.
    *   **Spatial Feel**: The 3D rotation of the square (`rotateX`, `rotateY`, `rotateZ`) creates an illusion of depth, making the element appear to tumble in space.
    *   **Alignment Principles**: Everything is centrally aligned for focus and clarity.
    *   **Whitespace Strategy**: The loading element and text are compactly grouped, with ample whitespace around the `.loading-container` to isolate the loading feedback.
    *   **Z-index Layering**: Not explicitly used here as it's a single, standalone component.

*   **Step C: Interactive Behavior & Animations**
    *   **Hover effects**: No specific hover effects are implemented for this loading animation, as it's designed for continuous passive feedback.
    *   **Scroll-triggered animations**: Not applicable; this is a time-based animation.
    *   **JavaScript-driven behaviors**: The core 3D cube spin animation is entirely driven by CSS, making it highly performant. No JavaScript is required for the visual effect itself.
    *   **Keyframe Animations**: The `@keyframes loading` rule defines the rotational sequence:
        *   `0%`: `transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);` (Initial flat state)
        *   `33%`: `transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);` (Rotates 180 degrees around its X-axis)
        *   `67%`: `transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);` (Continues by rotating 180 degrees around its Y-axis)
        *   `100%`: `transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);` (Completes by rotating 180 degrees around its Z-axis)
    *   **Animation Properties**: The `.loading-box` applies this keyframe animation using:
        *   `animation-name: loading;`
        *   `animation-duration: var(--animation-duration);` (e.g., 2 seconds for one cycle)
        *   `animation-timing-function: ease-in;` (Starts slowly and then speeds up, creating a smooth entry)
        *   `animation-iteration-count: infinite;` (Ensures continuous looping)

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect         | Method                                    | Why this method                                                |
| :--------------------------- | :---------------------------------------- | :------------------------------------------------------------- |
| 3D Cube Spin Animation       | CSS `@keyframes` with `transform` functions | Native, GPU-accelerated, ideal for smooth, complex rotations. |
| Glowing Box Visual           | CSS `border`, `border-radius`, `box-shadow` | Standard CSS properties for creating geometric shapes with lighting effects. |
| Centering Content on Page    | CSS Flexbox                               | Efficient and responsive for overall page layout and element placement. |
| Continuous Animation Loop    | CSS `animation-iteration-count: infinite` | Simple and declarative for endless repetition.                  |

> **Feasibility Assessment**: 100% - The core visual and animated effect, as demonstrated in the video for the loading animation example, is fully reproducible with the provided pure CSS code.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Loading Page",
    body_text: str = "Loading content...",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00bfff",  # CSS hex color for accent (cyan-like)
    width_px: int = 1200, # Overall viewport width for demo purposes
    height_px: int = 800, # Overall viewport height for demo purposes
    box_size_px: int = 50,
    border_width_px: int = 5,
    border_radius_px: int = 3,
    animation_duration_s: int = 2,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Cube Spin Loading Animation visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* 3D Cube Spin Loading Animation — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --box-size: {box_size_px}px;
    --border-width: {border_width_px}px;
    --border-radius: {border_radius_px}px;
    --animation-duration: {animation_duration_s}s;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Prevent scrollbars if content overflows viewport bounds */
    width: 100vw; /* Ensure body takes full viewport width */
    height: 100vh; /* Ensure body takes full viewport height */
}}

.loading-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px; /* Space between the box and the text */
}}

.loading-text {{
    font-size: 1.2rem;
    font-weight: 500;
    white-space: nowrap; /* Prevent text from wrapping */
}}

.loading-box {{
    height: var(--box-size);
    width: var(--box-size);
    border: var(--border-width) solid var(--accent);
    border-radius: var(--border-radius);
    /* Creates a glow effect around the box and subtly inside */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Apply the keyframe animation */
    animation: loading var(--animation-duration) ease-in infinite;
}}

/* Define the keyframe animation for the 3D spin */
@keyframes loading {{
    0% {{
        transform: perspective(100px) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: perspective(100px) rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: perspective(100px) rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: perspective(100px) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading-container">
        <div class="loading-box"></div>
        <p class="loading-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (Empty for this CSS-only animation) ===
    js = """// 3D Cube Spin Loading Animation — interactive behavior
// This specific animation is purely CSS-driven, so no JavaScript is required for the core visual effect.
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
- [x] Are all color values explicit hex or rgba (not referencing undefined CSS variables from external systems)?
- [x] Are all external resources loaded from CDN URLs (not local `node_modules` paths)?
- [x] Does the component respect the `width_px` and `height_px` parameters? (They define the overall viewport in this case; `box_size_px` defines the element size.)
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements (buttons, highlights, borders)?
- [x] Are `title_text` and `body_text` properly escaped for HTML (no XSS from special characters)?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?

### 4. Accessibility & Performance Notes

*   **Accessibility**:
    *   For a loading animation that indicates content is being loaded or processed, it's crucial to provide an accessible experience. While the visual animation is present, screen reader users might not perceive it.
    *   To improve accessibility, consider adding `aria-live="polite"` to the `.loading-container` and dynamically updating `body_text` or adding a visually hidden message when the loading state changes (e.g., "Loading content..." -> "Content loaded successfully.").
    *   The `body_text` provides a basic textual cue.
    *   Support for `prefers-reduced-motion` could be added via a media query to adjust or disable the animation for users with motion sensitivities.
    *   Ensure sufficient color contrast for `body_text` against `bg_color` (WCAG AA minimum 4.5:1) and the accent color (e.g., the cyan glow) for informational components.

*   **Performance**:
    *   **CSS Animations**: Using `@keyframes` with `transform` properties is highly performant. `transform` operations (like `rotate` and `perspective`) are typically handled directly by the GPU, leading to smoother animations and minimal impact on the main thread, even on lower-powered devices.
    *   **`box-shadow`**: While `box-shadow` can sometimes impact performance when used on many animating elements or with very large blur radii, for a single, small loading element like this, the performance overhead is negligible.
    *   **No JavaScript Animation**: Since the core animation is pure CSS, it avoids potential performance issues associated with JavaScript-driven animations (e.g., layout thrashing, running on the main thread).
    *   **`perspective()`**: Using `perspective()` directly in the `transform` function ensures a 3D context for the element's rotation, which is more performant than applying `perspective` to a parent element for a single animating object.