# Animated Morphing Hamburger & Off-Screen Slide Menu

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Morphing Hamburger & Off-Screen Slide Menu

* **Core Visual Mechanism**: A traditional mobile/responsive navigation pattern combining two effects: an off-screen menu that smoothly slides in from the edge of the viewport, and a hamburger icon (three horizontal bars) that morphs into a 'Close' (X) icon using CSS transforms (translation and rotation).
* **Why Use This Skill (Rationale)**: This is a foundational UX pattern for mobile-first and responsive design. It conserves screen real estate by hiding secondary navigation links until actively requested. Morphing the toggle icon provides immediate, satisfying micro-interaction feedback, anchoring the user’s context and clearly communicating the new state (open -> close).
* **Overall Applicability**: Essential for mobile web headers, progressive web apps (PWAs), SaaS application sidebars, and minimalist portfolio headers where a clean, uncluttered default view is preferred.
* **Value Addition**: Compared to a standard jumping display toggle (`display: none` to `block`), the sliding transition adds spatial context (the menu "lives" off to the right). The CSS-animated 'X' eliminates the need to load separate icon SVGs or fonts, remaining lightweight and highly customizable.
* **Browser Compatibility**: Broadly supported. Relies on standard CSS Flexbox, absolute positioning, `transform` (`translate`, `rotate`), and `transition`. Works perfectly on modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A semantic `<nav>` wrapper, an `.off-screen-menu` (fixed overlay container) holding an unordered list of links, and a `.ham-menu` (the toggle button) containing three `<span>` tags acting as the bars.
  - **Color Logic**:
    - Dark background for the sliding menu (`#222531` or derived from dark theme).
    - Vivid accent color for the hamburger bars (e.g., `#6F86FF`).
  - **Typography**: Clean sans-serif, scaled up significantly (`3rem`) within the sliding menu to act as large, tap-friendly touch targets.
  - **CSS Properties**: Primary weight is carried by `position: fixed` (for the overlay), `position: absolute` (for the hamburger bars), and `transition` for the animation timing.

* **Step B: Layout & Compositional Style**
  - **Layout System**:
    - *Navbar*: Flexbox (`display: flex`) with the hamburger menu pushed to the far right using `margin-left: auto`.
    - *Sliding Menu*: Fixed positioning (`position: fixed`), anchoring to `top: 0` and `right: -450px`. It takes up `100vh` and uses Flexbox to center the navigation links vertically and horizontally.
  - **Z-Index Layering**: The hamburger toggle must sit above the off-screen menu (`z-index: 1000` vs `z-index: 999`) so it remains visible and clickable to close the menu.

* **Step C: Interactive Behavior & Animations**
  - **Menu Slide**: Toggled via a JS class (`.active`). Changes the `right` property from `-450px` to `0` over `.3s ease`.
  - **Hamburger Morph**:
    - *Default*: 3 bars stacked vertically using `top: 25%`, `top: 50%`, and `top: 75%`.
    - *Active*: 
      - Middle bar: fades out (`opacity: 0`).
      - Top bar: moves to center (`top: 50%`) and rotates `45deg`.
      - Bottom bar: moves to center (`top: 50%`) and rotates `-45deg`.
    - *Timing*: `transition: .3s ease`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Hamburger morphing icon** | Pure CSS (`transform`, `opacity`) | Avoids loading external SVG/fonts. Smooth interpolation between bars and 'X'. |
| **Off-screen menu layout** | CSS Fixed Positioning | Detaches the menu from the normal document flow so it can overlap the page content smoothly. |
| **State Toggle** | Vanilla JavaScript | A simple event listener is the most lightweight, robust way to toggle the `.active` class on multiple DOM elements. |

> **Feasibility Assessment**: 100%. The reproduction code completely encapsulates the visual logic, layout, and animated transitions demonstrated in the tutorial using pure CSS and vanilla JS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Animated Menu Tutorial",
    body_text: str = "Click the hamburger icon in the top right to reveal the off-screen navigation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6F86FF",     # CSS hex color for accent (e.g. the hamburger bars)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Morphing Hamburger & Off-Screen Slide Menu.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        nav_bg = "#161b22"
        menu_bg = "#222531"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        nav_bg = "#ffffff"
        menu_bg = "#e9ecef"

    # === CSS ===
    css = f"""/* Animated Hamburger & Off-screen Menu — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --nav-bg: {nav_bg};
    --menu-bg: {menu_bg};
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
    overflow-x: hidden;
}}

/* Viewport Container (Simulating the window for demonstration) */
.viewport-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 8px;
}}

/* Navbar */
nav {{
    padding: 1rem 2rem;
    display: flex;
    background-color: var(--nav-bg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    text-decoration: none;
    line-height: 50px; /* Align with hamburger */
}}

/* Main Content Area */
main {{
    padding: 3rem 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* ===============================
   OFF-SCREEN MENU STYLES
   =============================== */
.off-screen-menu {{
    background-color: var(--menu-bg);
    height: 100%; /* Constrained to container for demo, normally 100vh */
    width: 100%;
    max-width: 450px;
    position: absolute; /* Using absolute for container demo, normally fixed */
    top: 0;
    right: -450px; /* Hidden by default */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: right .3s ease;
    z-index: 999;
}}

.off-screen-menu.active {{
    right: 0;
}}

.off-screen-menu ul {{
    list-style: none;
    text-align: center;
}}

.off-screen-menu li {{
    margin: 2rem 0;
}}

.off-screen-menu a {{
    color: var(--text);
    text-decoration: none;
    font-size: 3rem;
    font-weight: 600;
    transition: color 0.2s ease;
}}

.off-screen-menu a:hover {{
    color: var(--accent);
}}

/* ===============================
   HAMBURGER TOGGLE STYLES
   =============================== */
.ham-menu {{
    height: 50px;
    width: 50px;
    margin-left: auto;
    position: relative;
    cursor: pointer;
    z-index: 1000; /* Stays above the sliding menu */
}}

.ham-menu span {{
    height: 5px;
    width: 100%;
    background-color: var(--accent);
    border-radius: 25px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    transition: .3s ease;
}}

/* Default Positions */
.ham-menu span:nth-child(1) {{
    top: 25%;
}}
.ham-menu span:nth-child(2) {{
    top: 50%;
}}
.ham-menu span:nth-child(3) {{
    top: 75%;
}}

/* Active/Open Morphing Positions */
.ham-menu.active span:nth-child(1) {{
    top: 50%;
    transform: translate(-50%, -50%) rotate(45deg);
}}
.ham-menu.active span:nth-child(2) {{
    opacity: 0;
}}
.ham-menu.active span:nth-child(3) {{
    top: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="viewport-container">
        
        <!-- Off-Screen Navigation Menu -->
        <div class="off-screen-menu" id="nav-menu" role="dialog" aria-hidden="true">
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>

        <!-- Main Navbar -->
        <nav>
            <a href="#" class="logo">Brand.</a>
            <div class="ham-menu" role="button" aria-expanded="false" aria-controls="nav-menu" tabindex="0" aria-label="Toggle Navigation">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>

        <!-- Main Body Content -->
        <main>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Hamburger & Off-screen Menu — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamMenu = document.querySelector('.ham-menu');
    const offScreenMenu = document.querySelector('.off-screen-menu');

    // Function to toggle menu states
    const toggleMenu = () => {{
        const isActive = hamMenu.classList.toggle('active');
        offScreenMenu.classList.toggle('active');
        
        // Update accessibility attributes
        hamMenu.setAttribute('aria-expanded', isActive);
        offScreenMenu.setAttribute('aria-hidden', !isActive);
    }};

    // Mouse click event
    hamMenu.addEventListener('click', toggleMenu);

    // Keyboard accessibility (Enter or Space key)
    hamMenu.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            toggleMenu();
        }}
    }});
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

* **Accessibility**: 
  - Standard HTML `<div>` toggles are inaccessible to screen readers. The generated code enhances the tutorial's logic by adding `role="button"`, `tabindex="0"`, `aria-label`, `aria-expanded`, and `aria-controls` to the `.ham-menu`.
  - A keyboard event listener allows users to trigger the toggle using `Enter` or `Space`, ensuring the component is fully keyboard navigable.
* **Performance**: 
  - The tutorial uses `right` transitioning (e.g., `right: -450px` to `right: 0`), which can occasionally trigger layout recalculations. While the code implements exactly what was instructed for parity, for a high-performance production build, swapping `right: -100%` / `right: 0` for `transform: translateX(100%)` / `transform: translateX(0)` is recommended to ensure the animation stays completely on the compositor layer via the GPU.
  - The morphing icon uses `transform` (`translate` and `rotate`) and `opacity` properties, which are extremely performant CSS animations and will not cause reflow jank.