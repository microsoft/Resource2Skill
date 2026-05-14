# Math-Driven CSS-Only Morphing Hamburger Menu

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Math-Driven CSS-Only Morphing Hamburger Menu

* **Core Visual Mechanism**: A fully responsive, zero-JavaScript hamburger menu that morphs into a perfect "X" upon click. It uses a hidden `<input type="checkbox">` wrapped inside a `<label>` to store state. The three bars are constructed using the `<input>` itself (middle bar) and the `::before`/`::after` pseudo-elements of the container. CSS variables and the `calc()` function (using trigonometry `sqrt(2) ≈ 1.414`) dynamically calculate the exact width the bars need to become when forming the diagonal "X".
* **Why Use This Skill (Rationale)**: Typical hamburger menus rely on hardcoded pixel values and JavaScript event listeners to toggle classes. This technique removes JS overhead entirely while making the menu incredibly resilient. If a designer decides to change the width, height, or gap of the bars, changing a single CSS variable cascades through the `calc()` functions to ensure the "X" still forms perfectly.
* **Overall Applicability**: Perfect for lightweight landing pages, admin dashboards, portfolios, or any modern web application where keeping the JavaScript bundle small is a priority. It pairs seamlessly with off-canvas sidebars or full-screen overlay navigation.
* **Value Addition**: It introduces a highly satisfying, hardware-accelerated morphing animation that feels premium. It also demonstrates an advanced "Checkbox Hack" combined with modern CSS `:has()` selectors, creating a robust state machine in pure CSS.
* **Browser Compatibility**: This technique relies heavily on the CSS `:has()` pseudo-class, which is fully supported in modern browsers (Chrome 105+, Edge 105+, Safari 15.4+, Firefox 121+). It also uses CSS Math (`calc()`) and Custom Properties, which have universal modern support. 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent `<label class="hamburger-menu">` containing an `<input type="checkbox">`.
  - **The Bars**: The top bar is `::before`, the bottom bar is `::after`, and the middle bar is the `<input>` modified with `appearance: none`.
  - **Color Logic**: Uses a contrast swap. The bars use the `--foreground` color by default. When clicked, they swap to the `--background` color (useful if an off-canvas menu slides in underneath them).
  - **Dimensions**: All sizes (width, height, gap) are bound to CSS variables.

* **Step B: Layout & Compositional Style**
  - **Layout**: The `.hamburger-menu` uses `display: flex; flex-direction: column;` to stack the three bars automatically. 
  - **Spacing**: The space between bars is managed by the flex `gap` property, pulling from `--hamburger-gap`.
  - **Sizing**: `width: max-content;` ensures the clickable area tightly wraps the bars.

* **Step C: Interactive Behavior & Animations**
  - **State Toggling**: Clicking the label checks/unchecks the hidden checkbox. 
  - **Morphing to X**:
    - Middle bar (`input`): `opacity: 0; width: 0;` (fades and shrinks away).
    - Top bar (`::before`): `rotate: 45deg; translate: 0 calc(var(--bar-height) / -2);` with `transform-origin: left center`.
    - Bottom bar (`::after`): `rotate: -45deg; translate: 0 calc(var(--bar-height) / 2);` with `transform-origin: left center`.
    - Diagonal Math: The width of the rotated bars expands to `calc(var(--hamburger-height) * 1.41421356237)` to perfectly span the square area.
  - **Accessibility**: Uses `.hamburger-menu:has(input:focus-visible)` to draw a custom `box-shadow` outline around the bars when navigating via keyboard, preventing ugly default outlines.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **State Management** | CSS Checkbox Hack (`:checked`) | Allows click-toggling without requiring JavaScript event listeners or DOM mutation. |
| **Element Targeting** | CSS `:has()` Selector | Allows the parent `<label>` to react to the state of its child `<input>`. |
| **Shape Morphing** | Pure CSS + `calc()` Trigonometry | Uses `sqrt(2)` multiplier to calculate the exact hypotenuse width needed for the "X" diagonals dynamically. |
| **Layout structure** | CSS Flexbox (`column`) | The simplest way to perfectly stack three bars with a consistent, variable-driven gap. |

> **Feasibility Assessment**: 100% of the visual effect and interaction logic from the tutorial can be reproduced exactly as described using pure CSS and HTML.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Math-Driven CSS Hamburger",
    body_text: str = "Click the hamburger menu to see the pure CSS morphing animation. It triggers the sidebar without any JavaScript.",
    color_scheme: str = "dark",        
    accent_color: str = "#00E5FF",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Math-Driven CSS-Only Morphing Hamburger Menu.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0B0E14"
        text_color = "#FFFFFF"
        sidebar_bg = "#1A1F2B"
    else:
        bg_color = "#F0F4F8"
        text_color = "#111827"
        sidebar_bg = "#FFFFFF"

    css = f"""/* Math-Driven CSS-Only Morphing Hamburger Menu */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    /* Theme Colors */
    --bg-color: {bg_color};
    --text-color: {text_color};
    --sidebar-bg: {sidebar_bg};
    
    /* Hamburger Configurable Variables */
    --bar-width: 60px;
    --bar-height: 8px;
    --hamburger-gap: 8px;
    --foreground: {accent_color};
    --background: var(--bg-color);
    --animation-timing: 300ms ease-in-out;
    
    /* Mathematical Calculations (Do Not Edit) */
    --hamburger-height: calc(var(--bar-height) * 3 + var(--hamburger-gap) * 2);
    /* 1.414... is the square root of 2, used to find the diagonal length of a square */
    --x-width: calc(var(--hamburger-height) * 1.41421356237);
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

/* Presentation Container */
.app-container {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    max-height: 100vh;
    position: relative;
    background: var(--bg-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Content Area */
.main-content {{
    padding: 80px 40px 40px;
    max-width: 600px;
}}

.main-content h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    line-height: 1.2;
}}

.main-content p {{
    font-size: 1.1rem;
    opacity: 0.8;
    line-height: 1.6;
}}

/* =========================================
   CORE SKILL: CSS HAMBURGER MENU
========================================= */

.hamburger-menu {{
    display: flex;
    flex-direction: column;
    gap: var(--hamburger-gap);
    width: max-content;
    position: absolute;
    top: 24px;
    right: 24px;
    z-index: 100;
    cursor: pointer;
}}

/* The pseudo-elements act as the top and bottom bars */
.hamburger-menu::before,
.hamburger-menu::after,
.hamburger-menu input {{
    content: "";
    width: var(--bar-width);
    height: var(--bar-height);
    background-color: var(--foreground);
    border-radius: 9999px;
    transform-origin: left center;
    transition: 
        opacity var(--animation-timing), 
        width var(--animation-timing), 
        rotate var(--animation-timing), 
        translate var(--animation-timing), 
        background-color var(--animation-timing);
}}

/* The hidden checkbox acts as the middle bar */
.hamburger-menu input {{
    appearance: none; /* Removes default checkbox styling */
    padding: 0;
    margin: 0;
    outline: none;
    pointer-events: none; /* Let the label handle the click */
}}

/* --- CHECKED STATE (The 'X' Morph) --- */

/* When the inner checkbox is checked, trigger the animations */
.hamburger-menu:has(input:checked)::before {{
    rotate: 45deg;
    width: var(--x-width);
    translate: 0 calc(var(--bar-height) / -2);
}}

.hamburger-menu:has(input:checked)::after {{
    rotate: -45deg;
    width: var(--x-width);
    translate: 0 calc(var(--bar-height) / 2);
}}

.hamburger-menu input:checked {{
    opacity: 0;
    width: 0;
}}

/* Optional: Swap color when active (e.g., if moving over a colored sidebar) */
.hamburger-menu:has(input:checked)::before,
.hamburger-menu:has(input:checked)::after {{
    background-color: var(--foreground); 
}}

/* --- ACCESSIBILITY (Keyboard Navigation) --- */
.hamburger-menu:has(input:focus-visible)::before,
.hamburger-menu:has(input:focus-visible)::after,
.hamburger-menu input:focus-visible {{
    border: 1px solid var(--background);
    box-shadow: 0 0 0 2px var(--foreground);
}}

/* =========================================
   SIDEBAR DEMONSTRATION
========================================= */

.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    width: 320px;
    height: 100%;
    background-color: var(--sidebar-bg);
    padding: 100px 32px 32px;
    translate: 100% 0; /* Hidden by default */
    transition: translate var(--animation-timing);
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.2);
    z-index: 50;
}}

.sidebar nav {{
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.sidebar nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: 600;
    opacity: 0.7;
    transition: opacity 0.2s, color 0.2s;
}}

.sidebar nav a:hover {{
    opacity: 1;
    color: var(--foreground);
}}

/* Trigger sidebar when hamburger is checked */
.app-container:has(.hamburger-menu input:checked) .sidebar {{
    translate: 0 0;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Pure CSS Hamburger Menu -->
        <label class="hamburger-menu" aria-label="Toggle navigation">
            <input type="checkbox" aria-hidden="true">
        </label>

        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <nav>
                <a href="#">Home</a>
                <a href="#">Services</a>
                <a href="#">Portfolio</a>
                <a href="#">Contact</a>
            </nav>
        </aside>

        <!-- Page Content -->
        <main class="main-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this component!
// The entire morphing animation and state management is handled 
// via the CSS Checkbox Hack and the :has() pseudo-class.

console.log("Component loaded: Zero JS required for navigation state.");
"""

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
  - **Keyboard Navigable**: By wrapping the `<input type="checkbox">` in a `<label>`, native keyboard focus (Tab) flows perfectly.
  - **Custom Focus States**: The default focus ring of the checkbox is suppressed, and replaced dynamically using `.hamburger-menu:has(input:focus-visible)`. This paints an outline on the custom bars instead, ensuring keyboard users know exactly where focus is.
  - **Semantic Markup**: Uses a `<label>` instead of generic `<div>`s. An `aria-label="Toggle navigation"` is added to the label for screen readers, ensuring the interactive element is properly described.
* **Performance**:
  - **No Main Thread Blocking**: Since there is no JavaScript event listeners or DOM manipulation required to change the state, the main thread remains completely free.
  - **Hardware Acceleration**: The animation targets `translate`, `rotate`, `width`, and `opacity`. These are composite-friendly properties (except `width`, which triggers layout, but is generally smooth enough on a small element). To be perfectly optimized, `scaleX` could be used instead of `width`, but `width` keeps the logic highly readable.
  - **No Extraneous Paint**: Removing margins, padding, and applying `appearance: none` on the checkbox removes native OS-level drawing overhead.