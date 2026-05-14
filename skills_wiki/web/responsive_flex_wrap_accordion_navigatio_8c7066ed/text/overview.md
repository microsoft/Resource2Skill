### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Flex-Wrap Accordion Navigation Bar

* **Core Visual Mechanism**: This pattern uses CSS Flexbox (`display: flex` combined with `flex-wrap: wrap`) on the main `<nav>` element. On desktop, elements sit side-by-side. On mobile devices, the navigation links container is given `flex-basis: 100%`, forcing it to "wrap" onto a new line directly below the logo and hamburger icon. JavaScript is then used to toggle its visibility, creating an accordion-like expanding menu without relying on absolute positioning.
* **Why Use This Skill (Rationale)**: Traditional mobile menus often require absolute positioning, fixed overlays, or CSS translations which can cause z-index issues or scroll-locking headaches. The flex-wrap method keeps the menu strictly within the document flow, gracefully pushing page content down when opened. It's clean, robust, and minimizes CSS complexity.
* **Overall Applicability**: Highly suitable for SaaS landing pages, corporate websites, portfolios, and blogs where a reliable, sticky top-navigation is required across all device sizes.
* **Value Addition**: Provides a seamless transition between desktop and mobile states using native browser layout algorithms. The `position: sticky` addition ensures the navigation is always accessible without obscuring content when at the top of the page.
* **Browser Compatibility**: Fully supported in all modern browsers (CSS Flexbox, `position: sticky`, `classList` API). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A high-contrast split. A solid background for the navbar (e.g., `#ffffff` or `#1a1f36`) with contrasting text (`#111111` or `#f0f0f0`). Hover states and Call-to-Action (CTA) borders utilize a vibrant, recognizable accent color (e.g., `#39ffde` cyan).
  - **Typography**: Clean, sans-serif web font (Inter or Roboto) heavily utilizing uppercase transforms (`text-transform: uppercase`) and medium font weights (`500`) for navigation links to create a strong visual hierarchy.
  - **The Hamburger Icon**: Built purely out of HTML elements (typically `<span>` or `<div>`) styled with fixed heights, widths, and background colors to represent the three bars, avoiding the need for external icon font assets.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main `<nav>` uses `justify-content: space-between` to push the logo to the far left and the menu/hamburger to the far right.
  - **Mobile Layout Injection**: At `max-width: 768px`, the `.nav-links` container is switched to `flex-direction: column` and assigned `flex-basis: 100%`. Because the parent `<nav>` has `flex-wrap: wrap`, this forces the links to occupy the entire next "row" within the navbar.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Desktop links have a blocky hover effect (`padding: 25px 20px`) where the background color fills the vertical space of the navbar, transitioning smoothly (`transition: all 0.2s`).
  - **JavaScript State**: A simple JS event listener attaches to the hamburger menu, toggling an `active` class on the links container which changes it from `display: none` to `display: flex`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout Swap | CSS Flexbox (`flex-wrap` + `flex-basis`) | Cleanest native way to force elements to a new row on mobile without breaking document flow or using `position: absolute`. |
| Sticky Header | CSS `position: sticky` | Native, performant way to keep the navbar at the top of the viewport during scrolling without JS scroll listeners. |
| Hamburger Icon | Pure CSS lines | Eliminates external dependencies (like Font Awesome) ensuring the component is entirely self-contained. |
| Menu Toggle | JS `classList.toggle` | Modern, clean alternative to the tutorial's inline `style.display` manipulation, separating logic from styling. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. Resize the window to test the mobile flex-wrap hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent (e.g., cyan)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flex-Wrap Navbar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        surface_color = "#1a1f36"
        text_color = "#f0f0f0"
        text_hover = "#111111" # Dark text ensures contrast on bright accent colors
    else:
        bg_color = "#f0f0f0"
        surface_color = "#ffffff"
        text_color = "#111111"
        text_hover = "#111111"

    # === CSS ===
    css = f"""/* Responsive Flex-Wrap Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --accent: {accent_color};
    --text-hover: {text_hover};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
}}

/* -- Navbar Core -- */
.navbar {{
    position: sticky;
    top: 0;
    background-color: var(--surface);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
    flex-wrap: wrap; /* CRITICAL: allows mobile menu to wrap to next line */
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}}

/* -- Logo -- */
.logo a {{
    color: var(--text);
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: 700;
    padding: 20px 0;
    display: block;
}}

/* -- Desktop Links -- */
.nav-links {{
    list-style: none;
    display: flex;
    align-items: center;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 24px 20px;
    display: block;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* -- CTA Button Styling -- */
.nav-cta-button {{
    margin-left: 10px;
}}

.nav-cta-button a {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    padding: 10px 24px;
    margin-left: 10px;
}}

.nav-cta-button a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* -- Hamburger Icon (Hidden on Desktop) -- */
.hamburger {{
    display: none;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 10px;
}}

.hamburger .bar {{
    display: block;
    width: 28px;
    height: 3px;
    margin: 5px auto;
    background-color: var(--text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* -- Responsive Mobile Adjustments -- */
@media (max-width: 768px) {{
    .hamburger {{
        display: block; /* Show hamburger */
    }}
    
    .nav-links {{
        display: none; /* Hide links by default */
        flex-direction: column;
        width: 100%;
        flex-basis: 100%; /* CRITICAL: Forces the links to wrap below the header */
        padding-bottom: 20px;
    }}
    
    .nav-links.active {{
        display: flex; /* Shown when JS toggles class */
    }}
    
    .nav-links a {{
        text-align: center;
        padding: 15px;
        font-size: 1.1rem;
    }}
    
    .nav-cta-button {{
        margin: 15px 0 0 0;
        text-align: center;
    }}
    
    .nav-cta-button a {{
        margin: 0 auto;
        display: inline-block;
    }}
}}

/* -- Page Content -- */
.content {{
    padding: 60px 5%;
    max-width: var(--max-width);
    margin: 0 auto;
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}

.dummy-scroll {{
    height: 150vh;
    background: linear-gradient(to bottom, var(--surface), transparent);
    margin-top: 40px;
    border-radius: 12px;
    opacity: 0.3;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Semantic Nav Element -->
    <nav class="navbar" aria-label="Main Navigation">
        
        <div class="logo">
            <a href="#">{title_text}</a>
        </div>
        
        <!-- Accessible Button for Hamburger -->
        <button class="hamburger" aria-expanded="false" aria-controls="nav-menu" aria-label="Toggle navigation menu">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </button>
        
        <ul id="nav-menu" class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li class="nav-cta-button"><a href="#contact">Contact</a></li>
        </ul>
        
    </nav>

    <!-- Main Content Context -->
    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <div class="dummy-scroll"></div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar Interactivity
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {{
        // Toggle the active class which changes display from none to flex
        const isActive = navLinks.classList.toggle('active');
        
        // Update ARIA accessibility attribute based on state
        hamburger.setAttribute('aria-expanded', isActive);
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

* **Accessibility Enhancements (Beyond Tutorial)**: 
  * The tutorial utilized a `<div>` for the hamburger menu. The reproduction code upgrades this to a semantic `<button>` to ensure it is keyboard-focusable and reachable via Tab navigation.
  * Added `aria-label`, `aria-controls`, and dynamic `aria-expanded` attributes in the JavaScript so screen readers accurately announce when the mobile menu is opened or closed.
  * Ensures that when the bright accent color is hovered, the text color changes to a deep, dark value (`#111111`) to guarantee WCAG compliant contrast ratios.
* **Performance**: This method is highly performant. `position: sticky` runs entirely on the browser's compositor thread, eliminating scroll jank. Toggling the CSS class for the menu is instantaneous, avoiding expensive height calculations or JavaScript animations. Using Flexbox for layout minimizes complex recalculations.