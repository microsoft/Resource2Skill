# Sliced Typography Hover Effect

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sliced Typography Hover Effect

* **Core Visual Mechanism**: A typography-centric interaction where hovering over a text link causes the word to cleanly bisect horizontally. The top and bottom halves slide apart diagonally in opposite directions, revealing a color change. Simultaneously, a rapid horizontal "strike-through" line sweeps through the newly created horizontal gap, mimicking the trajectory of a blade that just sliced the text.
* **Why Use This Skill (Rationale)**: This technique turns static navigation menus into highly tactile, mechanical experiences. It leverages unexpected motion (splitting solid typography) to delight the user. The sharp angles and fast transitions create an edgy, modern, and slightly aggressive "glitch" or "cyber" aesthetic that commands attention.
* **Overall Applicability**: Ideal for bold, full-screen primary navigation menus, high-impact hero sections, creative agency portfolios, and tech product landing pages where large, declarative typography is the primary visual element.
* **Value Addition**: It elevates a standard text link into a complex visual event using only CSS, avoiding the overhead of heavy JavaScript animation libraries. It adds a memorable layer of polish and brand personality.
* **Browser Compatibility**: Excellent. Relies on `clip-path: polygon()`, CSS `attr()`, and basic CSS `transform` transitions, all of which are universally supported in modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A standard unordered list (`<ul>`). The magic happens via a `data-text` attribute on the anchor (`<a>`) tags, which duplicates the link text so it can be injected into pseudo-elements.
  - **Color Logic**: High contrast is key. The video uses a stark white background with solid dark gray text (`#262626`). On hover, the text flashes to a vibrant red (`#ff0000`), while the animated slicing line remains dark gray.
  - **Typographic Hierarchy**: The effect demands heavy, thick typography to provide enough surface area for the slice to be legible. The tutorial uses `Catamaran` at a bold `900` weight, completely capitalized, and sized very large (e.g., `3.5rem` or `30px+`).
  - **CSS Properties**: 
    - `clip-path`: The core driver, splitting the pseudo-elements exactly at the `50%` vertical mark.
    - `content: attr(data-text)`: Generates the overlapping text layers.
    - `color: transparent`: Hides the original DOM text so only the clipped pseudo-elements are visible.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Flexbox handles centering the list on the screen and stacking the menu items vertically.
  - **Spatial Feel**: Menu items need sufficient vertical padding to allow the split halves to shift upwards and downwards without colliding with adjacent links. Horizontal padding is applied inside an `overflow: hidden` container to allow the text to shift left/right without being prematurely clipped.
  - **Z-index Layering**: The animated strike-through line sits between the background and the text layers (or directly above them) to sell the illusion that it is passing through the physical gap created by the text splitting.

* **Step C: Interactive Behavior & Animations**
  - **Hover Slicing**: On hover, the top half (`::before`) translates `10px` right and `-2px` up. The bottom half (`::after`) translates `-10px` left and `2px` down.
  - **Line Sweep**: A pseudo-element line on the parent list item begins outside the left boundary (`transform: translateX(-101%)`) and rushes to the right boundary (`transform: translateX(101%)`) on hover.
  - **Timing**: All transitions are set to `0.4s` to `0.5s` using standard easing, providing a fast, snappy mechanical feel.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text duplication | CSS `content: attr(data-text)` | Generates identical, perfectly alignable text layers purely in CSS. |
| Splitting text | CSS `clip-path: polygon()` | Hardware-accelerated, exact mathematical masking to cut the text perfectly in half. |
| Hover displacement | CSS `transform: translate()` | High-performance animation that moves the clipped halves apart smoothly without triggering layout reflows. |
| Passing Line | CSS `transform: translateX()` inside `overflow: hidden` | Optimizes the traveling line animation compared to animating the `left` property, ensuring 60fps smoothness. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "GLITCH MENU",
    body_text: str = "Hover over the menu items to see the slice effect.",
    color_scheme: str = "light",
    accent_color: str = "#ff0000",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sliced Typography Hover Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configuration
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f4f4f4"
    else:
        bg_color = "#ffffff"
        text_color = "#262626"

    # === CSS ===
    css = f"""/* Sliced Typography Hover Effect */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Catamaran', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

.header-info {{
    text-align: center;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}}

.header-info h1 {{
    font-size: 1.2rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent-color);
    margin-bottom: 0.5rem;
}}

.header-info p {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

.sliced-menu {{
    list-style: none;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.menu-item {{
    position: relative;
    /* Hide the animated line when it travels outside the item */
    overflow: hidden; 
    margin: 5px 0;
    /* Padding provides space so shifted text isn't cut off by overflow:hidden */
    padding: 10px 25px; 
}}

/* The Animated Strike-through Line */
.menu-item::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--text-color);
    /* Start entirely out of view to the left */
    transform: translate(-101%, -50%);
    transition: transform 0.5s ease-in-out;
    z-index: 10;
    pointer-events: none;
}}

.menu-item:hover::before {{
    /* Travel all the way across to the right out of view */
    transform: translate(101%, -50%);
}}

.menu-link {{
    position: relative;
    display: inline-block;
    font-size: 3.5rem;
    font-weight: 900;
    text-transform: uppercase;
    text-decoration: none;
    /* Hide the original DOM text, rely purely on pseudo-elements */
    color: transparent; 
    line-height: 1;
    letter-spacing: 2px;
}}

/* Setup overlapping text layers */
.menu-link::before,
.menu-link::after {{
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    color: var(--text-color);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), color 0.4s ease;
    white-space: nowrap;
}}

/* Clip Top Half */
.menu-link::before {{
    clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%);
}}

/* Clip Bottom Half */
.menu-link::after {{
    clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%);
}}

/* Hover Displacements */
.menu-item:hover .menu-link::before {{
    transform: translate(10px, -2px);
    color: var(--accent-color);
}}

.menu-item:hover .menu-link::after {{
    transform: translate(-10px, 2px);
    color: var(--accent-color);
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
    <link href="https://fonts.googleapis.com/css2?family=Catamaran:wght@900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header-info">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <ul class="sliced-menu">
            <li class="menu-item"><a href="#" class="menu-link" data-text="HOME">HOME</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="ABOUT">ABOUT</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="SERVICES">SERVICES</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="PORTFOLIO">PORTFOLIO</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="CONTACT">CONTACT</a></li>
        </ul>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS effect. No JavaScript required for interactions.
console.log("Sliced typography component successfully initialized.");
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
  - Using `color: transparent` to visually hide the primary anchor text is robust because screen readers will still announce the text correctly (as opposed to using `display: none` or stripping the text entirely). 
  - Modern screen readers may attempt to read the `content: attr(data-text)` pseudo-elements depending on verbosity settings, though most identify it accurately as decorative context when paired directly over identical text.
* **Limitations**: This specific effect is strictly designed for single-line text elements. If the menu text is long enough to wrap to a second line, the `50%` vertical `clip-path` will simply bisect the entire multi-line block halfway down, severing the text directly through the middle of the block rather than character-by-character, destroying the illusion.
* **Performance**: Animating the traveling line using `transform: translate()` instead of animating the `left` property (as originally done in the video) moves the operation off the main UI thread and onto the GPU via compositing. This eliminates layout thrashing and guarantees a buttery smooth 60fps animation, even on lower-powered mobile devices.