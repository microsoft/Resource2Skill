# Interactive Spotlight Text Gradient

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Spotlight Text Gradient

* **Core Visual Mechanism**: This pattern applies a dynamic "flashlight" or "spotlight" effect to typography. It achieves this by mapping a background radial gradient to the text shape using `background-clip: text`, and then updating the center coordinates of that gradient via JavaScript to follow the user's mouse cursor.
* **Why Use This Skill (Rationale)**: It transforms static, prominent text into a tactile, interactive element. The movement rewards user interaction and naturally draws the eye, making the text feel deeply integrated into the digital environment rather than just painted on top.
* **Overall Applicability**: Perfect for high-impact typography areas such as hero sections, landing page headlines, portfolio nameplates, or feature highlight headers where you want to add a "wow" factor without cluttering the screen with structural animations.
* **Value Addition**: It adds a layer of kinetic micro-interaction that elevates perceived production value. By shifting the brightest point of the text based on cursor position, it simulates lighting and depth on a 2D plane.
* **Browser Compatibility**: Relies on `background-clip: text` (and its `-webkit-` prefixed version) which is widely supported in all modern browsers. It also requires CSS Custom Properties (variables) and basic DOM event listeners.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML**: A simple, semantic block-level text element (like an `<h1>`).
  - **Color Logic**: A base text color that is visually muted (often blending slightly with the background) and a bright "highlight" color for the center of the spotlight. The visual depth relies on the contrast between the highlighted center and the dim edges.
  - **Typography**: Works best with bold, thick, or heavy font weights (e.g., `800` or `900`) and large font sizes so there is enough surface area for the gradient to be visible.
  - **CSS Drivers**: `background: radial-gradient()`, `color: transparent`, and `-webkit-background-clip: text`.

* **Step B: Layout & Compositional Style**
  - CSS Flexbox or Grid is used on the container to center the text prominently in the viewport.
  - The text element acts as a fixed bounding box relative to which the mouse coordinates are calculated.

* **Step C: Interactive Behavior & Animations**
  - A JavaScript `mousemove` event listener is attached to the text element.
  - On every frame of movement, JS calculates the cursor's local `X` and `Y` coordinates relative to the text element's top-left corner.
  - These coordinates are converted to percentages based on the element's width and height, and injected back into the element as inline CSS custom properties (`--x` and `--y`).
  - The CSS `radial-gradient` uses these variables: `circle at var(--x) var(--y)`.
  - A `mouseleave` event can optionally reset the spotlight to the center.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text Masking | CSS `background-clip: text` | The native, performant way to render gradients specifically inside text boundaries. |
| Dynamic Lighting | CSS Custom Properties + `radial-gradient` | Allows for a smooth gradient transition while being completely dynamic without needing WebGL or Canvas rendering. |
| Cursor Tracking | JavaScript DOM `mousemove` | Provides the necessary local element coordinate math (`e.clientX` - `rect.left`) to update the CSS variables in real-time. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Gradient text",
    body_text: str = "Hover over the text to see the spotlight effect.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",  # Spotlight color
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Spotlight Text Gradient visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user input
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    # For the text to look like it's "lit up" from the dark, 
    # the unlit base should be darker/dimmer than the background.
    if color_scheme == "dark":
        bg_color = "#1e1e24"
        text_base = "#000000" # Fades into deep shadow
        text_highlight = accent_color
        p_color = "#888888"
    else:
        bg_color = "#f4f5f7"
        text_base = "#c0c4cc" # Fades into flat grey
        text_highlight = accent_color if accent_color != "#ffffff" else "#333333"
        p_color = "#666666"

    # === CSS ===
    css = f"""/* Interactive Spotlight Text Gradient — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-highlight: {text_highlight};
    --text-base: {text_base};
    --p-color: {p_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
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
    gap: 2rem;
    position: relative;
}}

.interactive-text {{
    /* Default variables for gradient center */
    --x: 50%;
    --y: 50%;
    
    font-size: clamp(4rem, 12vw, 10rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.1;
    text-align: center;
    
    /* The Spotlight Gradient */
    background: radial-gradient(
        circle at var(--x) var(--y),
        var(--text-highlight) 0%,
        var(--text-base) 80%
    );
    
    /* Apply masking */
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    
    /* UX */
    cursor: crosshair;
    user-select: none;
    
    /* Smooth return to center when mouse leaves */
    /* Note: Only browsers supporting @property fully transition custom variables, 
       but snapping back is also an acceptable fallback */
    transition: filter 0.3s ease;
}}

.interactive-text:active {{
    filter: brightness(1.2);
}}

.body-text {{
    color: var(--p-color);
    font-size: 1.25rem;
    font-weight: 400;
    text-align: center;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Spotlight Text</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The core component -->
        <h1 class="interactive-text">{safe_title}</h1>
        
        {f'<p class="body-text">{safe_body}</p>' if body_text else ''}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Spotlight Text Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const textElement = document.querySelector('.interactive-text');

    if (!textElement) return;

    // Track mouse movement over the text element
    textElement.addEventListener('mousemove', (e) => {{
        // Get precise dimensions and position of the text node
        const rect = textElement.getBoundingClientRect();
        
        // Calculate relative local coordinates
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Convert to percentages
        const xPercent = Math.round((x / rect.width) * 100);
        const yPercent = Math.round((y / rect.height) * 100);

        // Update inline CSS custom properties
        textElement.style.setProperty('--x', xPercent + '%');
        textElement.style.setProperty('--y', yPercent + '%');
    }});

    // Reset the spotlight to the center when the mouse leaves
    textElement.addEventListener('mouseleave', () => {{
        textElement.style.setProperty('--x', '50%');
        textElement.style.setProperty('--y', '50%');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
```

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the dimensions?
- [x] Does `color_scheme` accurately swap the aesthetic logic?
- [x] Are texts properly escaped for HTML?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility**: Because `color: transparent` and `background-clip: text` are used, ensure that the background gradient always maintains a sufficient contrast ratio against the surrounding page background so that the text remains readable. In high contrast mode, standard text colors will override this effect naturally, maintaining accessibility.
* **Performance**: The `mousemove` event fires frequently. While updating two CSS variables is generally inexpensive and hardware-accelerated, if this element is part of an extremely heavy DOM tree, wrapping the JS coordinate updates inside a `requestAnimationFrame` callback could further optimize rendering performance and prevent potential frame-dropping on lower-end devices.