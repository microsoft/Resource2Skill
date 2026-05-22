# Sliding Text Push Button

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sliding Text Push Button

* **Core Visual Mechanism**: A split-text hover animation driven by CSS transforms. The button contains two identical text elements stacked on top of each other inside a container with `overflow: hidden`. Initially, one text element is centered while the other sits out of view to the left. On hover, both text elements slide to the right simultaneously, creating the illusion of a new word pushing the old word out of the frame.
* **Why Use This Skill (Rationale)**: This technique turns a standard outlined button into a highly engaging, dynamic interaction. It provides immediate, satisfying visual feedback that makes the interface feel modern and polished without being overly distracting.
* **Overall Applicability**: Ideal for primary Call-to-Action (CTA) buttons in hero sections, portfolio website links, landing page focal points, or any scenario where you want a button to command attention upon interaction.
* **Value Addition**: It elevates a simple "ghost button" (bordered, no background) into a sophisticated micro-interaction using purely declarative CSS, requiring zero JavaScript overhead.
* **Browser Compatibility**: Excellent. Relies on standard CSS2/CSS3 properties (`position`, `overflow`, `transform`, `transition`), supported by all modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Construct**: A semantic interactive container (like `<a>` or `<button>`) wrapping two duplicate `<span>` elements holding the same text.
  - **Color Logic**: High contrast minimal aesthetic. The tutorial uses a dark background (`#262626`) with a vibrant yellow accent (`#eccf00`) for the text and border.
  - **Typographic Hierarchy**: The text acts as a strong graphical element: uppercase text, clean sans-serif font, large font size (`24px`), and wide letter-spacing (`4px`) to ensure legibility during motion.
  - **Key CSS Properties**: `overflow: hidden` (to mask the text outside the box), `position: absolute` (to layer the text), and `transform: translateX` (to move the text).

* **Step B: Layout & Compositional Style**
  - **Container**: Fixed dimensions (`200px` width, `60px` height) with a solid `2px` border. The `line-height` is set equal to the height (`60px`) to perfectly vertically center the text.
  - **Layering**: The outer container acts as a positioning context (`position: relative`). Both inner spans are `position: absolute`, covering `100%` width and height, ensuring they occupy the exact same physical space.

* **Step C: Interactive Behavior & Animations**
  - **Initial State**: Span 1 (incoming) is translated off-screen left (`transform: translateX(-100%)`). Span 2 (outgoing) sits at the origin (`transform: translateX(0)`).
  - **Hover State**: Span 1 moves to the center (`translateX(0)`). Span 2 moves off-screen right (`translateX(100%)`).
  - **Motion Profile**: A linear or ease-based `transition` of `0.5s` is applied to the `transform` property on both spans, ensuring they move in unison.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split-text layering | Absolute Positioning | Allows two text elements to occupy the exact same space within the button container. |
| Sliding animation | CSS `transform: translateX` | Native GPU-accelerated property for smooth horizontal motion without triggering layout recalculations (jank). |
| Content clipping | CSS `overflow: hidden` | Masks the incoming and outgoing text elements when they are outside the button boundaries. |
| Hover logic | CSS `:hover` pseudo-class | Pure CSS state management, eliminating the need for JavaScript event listeners. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Sliding Text Push Button",
    body_text: str = "Hover over the button below to see the continuous sliding text effect.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#eccf00",     # CSS hex color for accent (yellow from video)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sliding Text Push Button visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#262626"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        
    button_label = "CREATIVE"

    # === CSS ===
    css = f"""/* Sliding Text Push Button — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 40px;
}}

.title {{
    font-size: 2rem;
    font-weight: 600;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* === Core Visual Effect Styles === */

.sliding-button {{
    position: relative;
    display: inline-block;
    width: 200px;
    height: 60px;
    line-height: 60px; /* Vertically centers the text */
    text-align: center;
    text-transform: uppercase;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 24px;
    letter-spacing: 4px;
    color: var(--accent);
    border: 2px solid var(--accent);
    overflow: hidden; /* Crucial for masking the sliding text */
    cursor: pointer;
}}

.sliding-button span {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: transform 0.5s ease-in-out;
}}

/* Incoming text: Starts off-screen to the left */
.sliding-button span:nth-child(1) {{
    transform: translateX(-100%);
}}

/* Incoming text on hover: Slides into the center */
.sliding-button:hover span:nth-child(1) {{
    transform: translateX(0);
}}

/* Outgoing text: Starts in the center */
.sliding-button span:nth-child(2) {{
    transform: translateX(0);
}}

/* Outgoing text on hover: Slides off-screen to the right */
.sliding-button:hover span:nth-child(2) {{
    transform: translateX(100%);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- Button Component -->
        <!-- Note: aria-label is provided for screen readers, and duplicate text spans are hidden to prevent reading the word twice -->
        <a href="#" class="sliding-button" aria-label="{button_label}">
            <span aria-hidden="true">{button_label}</span>
            <span aria-hidden="true">{button_label}</span>
        </a>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sliding Text Push Button — No JS required for the core visual effect.
// The animation is handled entirely by CSS transforms and transitions.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded successfully.");
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

* **Accessibility (A11y)**: Since the HTML structural requirement for this effect involves duplicating the text inside two `<span>` tags, a screen reader would normally read "CREATIVE CREATIVE". To prevent this confusing experience, the parent container (`<a>`) is given an `aria-label="CREATIVE"`, and both inner `<span>` elements are given `aria-hidden="true"`. This ensures the visual trick does not degrade the semantic meaning for assistive technologies.
* **Performance**: This is an extremely performant animation. It exclusively animates the CSS `transform` property (`translateX`), which is handed off to the GPU for compositing. It does not animate layout properties (like `margin` or `width`) or paint properties (like `color`), ensuring smooth 60fps animations without causing browser reflow or repaint cycles.