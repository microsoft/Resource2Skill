# CSS Variable Theme Switcher with Custom Checkbox Toggle

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: CSS Variable Theme Switcher with Custom Checkbox Toggle

* **Core Visual Mechanism**: This pattern implements a smooth, animated transition between light and dark modes. It relies on a two-part mechanism: 
  1. A data-attribute on the `<body>` tag (e.g., `data-theme="dark"`) that dictates global CSS variables (custom properties) for colors.
  2. A native HTML checkbox hidden from view, paired with a `<label>` styled as a pill-shaped toggle switch. The CSS `:checked` pseudo-class is used to animate the toggle thumb and visually indicate the state.
* **Why Use This Skill (Rationale)**: By delegating the color definitions to CSS variables based on a single root attribute, you strictly separate application state (managed by a tiny JavaScript snippet) from visual rendering (managed purely by CSS). The custom toggle switch leverages native HTML form behaviors without needing complex JS animation libraries, ensuring a tactile and satisfying micro-interaction.
* **Overall Applicability**: Essential for almost modern web applications, SaaS dashboards, blogs, and portfolios where user reading comfort (eye strain reduction) is a priority.
* **Value Addition**: Transforms a standard webpage into a personalized experience. The animated transition of both the UI colors and the physical toggle switch creates a premium, polished feel that standard abrupt color-swapping lacks.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard CSS Custom Properties (Variables), the `:checked` pseudo-class, and CSS Transitions.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A structural container holding the main content (a card) and a specialized container for the switcher (`input[type="checkbox"]` + `<label>`).
  - **Color Logic (extracted from tutorial)**:
    - *Light Theme*: Background `#C4DCF1` (Light Blue), Surface/Card `#FFFFFF`, Text `#50526E`.
    - *Dark Theme*: Background `#1E1F26` (Very Dark Grey), Surface/Card `#292C33`, Text `#BABACA`.
  - **Typographic Hierarchy**: Uses **Montserrat** (sans-serif) for clean, geometric readability. Uppercase headings and buttons establish a strong structural hierarchy.
  - **CSS Constructs**: `data-theme` attribute selectors define the color palette map.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main body uses Flexbox (`display: flex; align-items: center; justify-content: center;`) to perfectly center the card in the viewport.
  - **Card Composition**: Max-width of around 500px, 40px padding, subtle border-radius (8px-12px) to give a modern "floating" surface look.
  - **Switcher Positioning**: Absolutely positioned (`position: absolute; top: 20px; right: 30px;`) so it remains accessible independently of the document flow.

* **Step C: Interactive Behavior & Animations**
  - **The Checkbox Hack**: The `<input>` is visually hidden (`visibility: hidden; width: 0; height: 0;`). The `<label>` acts as the clickable surface. Because they are linked via `id` and `for` attributes, clicking the label toggles the checkbox state.
  - **Toggle Animation**: A pseudo-element (`label::after`) forms the circular "thumb". When the input is checked (`input:checked + label::after`), the circle translates across the pill.
  - **Color Transitions**: `transition: background-color 0.5s ease, color 0.5s ease;` is applied universally (or specifically to the body and card elements) ensuring that when the `data-theme` attribute swaps, the colors cross-fade rather than snap.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theming System** | CSS Custom Properties (`var()`) | The most performant and scalable way to implement themes. Updating one attribute cascades colors globally. |
| **Custom Toggle Switch** | HTML Checkbox + CSS `:checked` + `<label>` | Avoids unnecessary JavaScript event mapping for the visual state of the switch. Native HTML behavior handles the toggle logic. |
| **Color Cross-fade** | CSS `transition` | Hardware-accelerated, zero-JS approach to morphing backgrounds and text colors. |
| **State Management** | Vanilla JS Event Listener | A simple 5-line script is all that's needed to listen to the checkbox and update the `data-theme` attribute. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "THIS IS TITLE",
    body_text: str = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident, laudantium laboriosam optio ipsum, corrupti possimus necessitatibus reprehenderit, sint vero sunt explicabo. Ea eligendi porro laborum? Inventore, molestias commodi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Theme Switcher visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Safe text injection
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)
    
    # Determine initial states based on configured default theme
    is_dark = color_scheme == "dark"
    initial_theme = "dark" if is_dark else "light"
    checked_attr = "checked" if is_dark else ""

    # === CSS ===
    # We use a slightly optimized version of the tutorial's logic:
    # `transform: translateX` is used instead of `left` for the toggle animation (better performance).
    css = f"""/* Theme Switcher Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Theme Variables (Default fallback) */
:root, body[data-theme="light"] {{
    --bg-color: #c4dcf1;
    --surface-color: #ffffff;
    --text-primary: #1e1f26;
    --text-secondary: #50526e;
    --toggle-bg: #1e1f26;
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
}}

/* Dark Theme Variables */
body[data-theme="dark"] {{
    --bg-color: #1e1f26;
    --surface-color: #292c33;
    --text-primary: #ffffff;
    --text-secondary: #babaca;
    --toggle-bg: {accent_color};
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Smooth crossfade for theme switching */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.layout-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* --- Custom Theme Switcher --- */
.theme-switcher {{
    position: absolute;
    top: 30px;
    right: 40px;
    display: flex;
    align-items: center;
}}

.theme-switcher input[type="checkbox"] {{
    width: 0;
    height: 0;
    visibility: hidden;
    position: absolute;
}}

.theme-switcher label {{
    display: block;
    width: 60px;
    height: 30px;
    background-color: var(--toggle-bg);
    border-radius: 50px;
    cursor: pointer;
    position: relative;
    transition: background-color 0.4s ease;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}}

.theme-switcher label::after {{
    content: '';
    position: absolute;
    top: 50%;
    left: 5px;
    width: 20px;
    height: 20px;
    background-color: var(--toggle-thumb);
    border-radius: 50px;
    /* Combine translateY (centering) with translateX (horizontal movement) */
    transform: translateY(-50%) translateX(0);
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Checked State */
.theme-switcher input:checked + label::after {{
    /* 60px width - 20px thumb - 10px total padding (5px each side) = 30px translation */
    transform: translateY(-50%) translateX(30px);
}}

/* --- Content Card --- */
.card {{
    background-color: var(--surface-color);
    padding: 40px;
    border-radius: 12px;
    max-width: 480px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
    transition: background-color 0.5s ease, box-shadow 0.5s ease;
}}

.card h1 {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
    color: var(--text-primary);
    transition: color 0.5s ease;
}}

.card p {{
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 30px;
    transition: color 0.5s ease;
}}

.card button {{
    background-color: var(--toggle-bg);
    color: var(--surface-color);
    border: none;
    padding: 12px 30px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.4s ease, color 0.4s ease, transform 0.2s ease;
}}

.card button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Switcher Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body data-theme="{initial_theme}">
    <div class="layout-wrapper">
        
        <!-- Theme Switcher UI -->
        <div class="theme-switcher">
            <input type="checkbox" id="switcher" {checked_attr} aria-label="Toggle dark mode">
            <label for="switcher"></label>
        </div>

        <!-- Main Content -->
        <section class="card">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
            <button type="button">HELLO!</button>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const switcher = document.getElementById('switcher');
    const body = document.body;

    // Listen for state changes on the checkbox
    switcher.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // If checked, switch to dark theme
            body.setAttribute('data-theme', 'dark');
        }} else {{
            // If unchecked, switch to light theme
            body.setAttribute('data-theme', 'light');
        }}
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

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**:
  * **Input Labeling**: Added an `aria-label="Toggle dark mode"` to the hidden checkbox. Screen readers will still interact with the hidden input (even if `visibility: hidden`, depending on screen reader strictness, it's safer to use `opacity: 0` or visually-hidden utility classes in production, but we stuck close to the tutorial's logic while patching the most critical gap).
  * **System Preferences**: In a fully production-ready application, you would wrap the initial variable setup in a `@media (prefers-color-scheme: dark)` query so that the default state matches the user's OS-level preferences before they even touch the toggle.
* **Performance**:
  * **Hardware Acceleration**: The tutorial used CSS `left` and `calc()` combinations to animate the toggle thumb. Animating dimensional/layout properties like `left` triggers CPU repaints. I upgraded the reproduction code to use `transform: translateX(...)` instead. Transform runs on the GPU (compositor thread) ensuring a silky-smooth 60fps animation without layout recalculations.
  * **Cross-fade Efficiency**: By applying `transition` globally to backgrounds and text colors, the DOM seamlessly shifts states. No JavaScript-driven interval loops are used, offloading all rendering to the browser's optimized CSS engine.