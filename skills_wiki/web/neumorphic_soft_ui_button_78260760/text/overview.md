# Neumorphic Soft UI Button

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neumorphic Soft UI Button

* **Core Visual Mechanism**: Neumorphism (or Soft UI) is defined by elements that appear to extrude from their background. This is achieved by setting the element's background color to be *exactly the same* as its parent's background color, and then creating depth using two opposing `box-shadow` values: a light shadow on the top-left (acting as a highlight from a light source) and a dark shadow on the bottom-right (acting as the cast shadow). 
* **Why Use This Skill (Rationale)**: It creates a tactile, physical feel reminiscent of embossed plastic or clay. The aesthetic is extremely minimal and clean, reducing visual clutter while still providing clear affordances for interactive elements.
* **Overall Applicability**: Best used in utility applications, minimal dashboards, smart home control interfaces, or personal portfolios where a clean, modern, and "hardware-like" aesthetic is desired.
* **Value Addition**: Transforms a flat interface into a soft, 3D, tactile experience purely through CSS. The transition to an `inset` shadow on click perfectly mimics the physical sensation of pressing a mechanical button.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies entirely on standard CSS `box-shadow`, `border-radius`, and `transition`.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Entity**: A container (like a `<div>` or semantically a `<button>`) with centered text.
  - **Color Logic**:
    - **Light Theme (Video default)**: Background `#ebebeb`, Dark Shadow `#bebebe`, Light Shadow `#ffffff`.
    - **Dark Theme**: Background `#2a2b2f`, Dark Shadow `#1d1e21`, Light Shadow `#37383d`.
  - **Typographic Hierarchy**: System sans-serif fonts, medium weight, contrasting subtly with the background.
  - **CSS Properties**: The heavy lifter is `box-shadow: [X] [Y] [Blur] [Color], -[X] -[Y] [Blur] [Color]`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Flexbox on the parent to center the button in the viewport.
  - **Spatial Feel**: Neumorphism requires ample whitespace to let the shadows breathe. 
  - **Proportions**: A generous `padding` (e.g., `20px 40px`) and a noticeable `border-radius` (e.g., `12px` or higher) to emphasize the soft, molded aesthetic. 

* **Step C: Interactive Behavior & Animations**
  - **Click State (`:active`)**: The entire visual trick relies on swapping the outer shadows for `inset` shadows when pressed. 
    - E.g., `box-shadow: inset 6px 6px 10px #bebebe, inset -6px -6px 10px #ffffff;`
  - **Transitions**: A short, snappy transition (`transition: all 0.2s ease-in-out;`) ensures the press feels responsive but smooth.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Soft 3D extrusion | CSS `box-shadow` (multiple) | Comma-separating shadows allows simultaneous light and dark cast shadows. |
| Pressed state | CSS `:active` with `inset` | Reverses the direction of the shadow to create a concave/pressed illusion natively. |
| Smooth interaction | CSS `transition` | GPU-accelerated transition of the shadow values makes the physical "press" feel natural. |

> **Feasibility Assessment**: 100% reproduction. The tutorial relies entirely on standard CSS which is fully reproducible in a self-contained environment.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Click Me",
    body_text: str = "",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent hover
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic Soft UI Button visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Safely escape text
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#2a2b2f"
        text_color = "#e0e0e0"
        shadow_dark = "#1d1e21"
        shadow_light = "#37383d"
    else:
        # Match tutorial values exactly
        bg_color = "#ebebeb"
        text_color = "#333333"
        shadow_dark = "#bebebe"
        shadow_light = "#ffffff"

    # === CSS ===
    css = f"""/* Neumorphic Soft UI Button — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --shadow-dark: {shadow_dark};
    --shadow-light: {shadow_light};
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
    max-width: 100%;
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

.content-wrapper {{
    text-align: center;
}}

.body-text {{
    margin-top: 10px;
    opacity: 0.7;
    font-size: 14px;
}}

/* Core Visual Pattern: Neumorphic Button */
.neumorphic-button {{
    /* Match background exactly to parent to create the illusion of extrusion */
    background: var(--bg);
    color: var(--text);
    
    border: none;
    outline: none;
    border-radius: 12px;
    padding: 20px 40px;
    font-size: 18px;
    font-weight: 500;
    cursor: pointer;
    
    /* Dual Box Shadows: Bottom-Right Dark, Top-Left Light */
    box-shadow: 
        8px 8px 16px var(--shadow-dark), 
        -8px -8px 16px var(--shadow-light);
        
    transition: all 0.2s ease-in-out;
}}

.neumorphic-button:hover {{
    color: var(--accent);
}}

/* The Pressed State */
.neumorphic-button:active {{
    /* Invert shadows to inner to simulate being pushed into the surface */
    box-shadow: 
        inset 6px 6px 10px var(--shadow-dark), 
        inset -6px -6px 10px var(--shadow-light);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neumorphic Soft UI Button</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <button class="neumorphic-button">{safe_title}</button>
        
        {f'<div class="content-wrapper"><p class="body-text">{safe_body}</p></div>' if safe_body else ''}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const button = document.querySelector('.neumorphic-button');
    
    // Example interaction just to prove JS attachment
    button.addEventListener('click', () => {{
        console.log('Neumorphic button pressed!');
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
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba? *(Yes, conditionally passed into CSS vars from the Python code).*
- [x] Are all external resources loaded from CDN URLs? *(Google fonts used).*
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements? *(Yes, applied on hover).*
- [x] Are `title_text` and `body_text` properly escaped for HTML?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - The tutorial utilized a `<div>` element for the button. In the reproduction code above, this has been upgraded to a semantic `<button>` tag to ensure proper keyboard navigation (Tab-targeting) and screen-reader support out of the box. 
  - **Contrast Warning**: By definition, Neumorphism suffers from low contrast for its edges. Ensure the text inside the button has a high enough contrast ratio against the background (at least 4.5:1). The provided default hex codes meet standard readability requirements for the text, though the button edges themselves do not (which is an inherent trade-off of the Soft UI style).
  - The `outline: none;` property is used to match the minimal aesthetic, but in production, a custom focus-visible ring should be added for keyboard users.
* **Performance**: 
  - Standard `box-shadow` manipulation during the `:active` state is quite performant and handles native hardware acceleration seamlessly. There are no performance bottlenecks with this technique.