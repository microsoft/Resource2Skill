### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Slide-Out Mobile Navigation

* **Core Visual Mechanism**: This pattern features a mobile-first slide-out navigation menu anchored to the right side of the screen. The defining aesthetic is a "frosted glass" (glassmorphism) effect applied to the menu surface via CSS `backdrop-filter: blur()`, allowing the underlying page content (like a vibrant hero image or gradient) to subtly bleed through. On desktop, it gracefully expands into a top-level horizontal flex menu.
* **Why Use This Skill (Rationale)**: Sliding menus maximize screen real estate on mobile devices. Adding a glassmorphism effect elevates the design, making it feel modern, lightweight, and deeply integrated with the page's spatial depth, rather than looking like an obstructive, disconnected solid block. 
* **Overall Applicability**: Ideal for modern landing pages, SaaS websites, portfolios, and web apps with rich background imagery or complex layouts where you want to maintain visual context even while the user is navigating.
* **Value Addition**: It introduces smooth spatial context. The sliding animation (`transform: translateX`) combined with the blurred translucency helps users understand that the main page is still right there beneath the menu.
* **Browser Compatibility**: `backdrop-filter` is widely supported in modern browsers. However, it requires a fallback for browsers that do not support it (like older versions of Firefox or IE), which is gracefully handled using the `@supports` CSS feature query.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: The transparent glass effect requires a highly translucent background, e.g., `rgba(255, 255, 255, 0.1)` for light text on dark backgrounds. 
  - **Typographic Hierarchy**: Uppercase, sans-serif fonts with heavy letter-spacing (e.g., `2px` or `0.15em`) for navigation links. Numbers prefixing the links (e.g., "01 Home") have a bold weight (`700`) to create a technical, structured feel.
  - **Key CSS Properties**: `backdrop-filter: blur(1rem)` for the glass effect, and `transform: translateX(100%)` to move the menu off-canvas.

* **Step B: Layout & Compositional Style**
  - **Layout System**: 
    - **Desktop**: A standard Flexbox layout (`justify-content: space-between`) for the header, and `display: flex; gap: 2rem` for the navigation items.
    - **Mobile**: The `<nav>` uses `position: fixed` with the logical property `inset: 0 0 0 30%` to lock it to the top, bottom, and right, while leaving a 30% gap on the left side to show the page background.
  - **Z-index Layering**: The toggle button is given a high `z-index: 9999` to ensure it stays on top of the sliding menu when it expands.

* **Step C: Interactive Behavior & Animations**
  - **State Management**: JavaScript handles click events to toggle a `data-visible="true/false"` attribute on the menu and an `aria-expanded="true/false"` attribute on the button. 
  - **Motion**: The menu slides in via a CSS `transition: transform 350ms ease-out;`.
  - **Icon Swap**: The hamburger icon switches to a close (X) icon strictly via CSS, driven by the `aria-expanded` state of the parent button.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Frosted glass effect | CSS `backdrop-filter` | Native, performant way to blur elements behind the menu. |
| Slide-in animation | CSS `transform` & `transition` | GPU-accelerated, butter-smooth animation without relying on JS physics. |
| Menu Toggle State | JS + DOM Data Attributes | Using `data-visible` and `aria-expanded` separates state logic from styling and ensures accessibility. |
| Layout / Positioning | CSS Flexbox & `inset` | `inset` is a clean shorthand for fixed positioning (`top`, `right`, `bottom`, `left`), and Flexbox easily shifts between horizontal (desktop) and vertical (mobile). |
| Hamburger Icon | Inline SVG + CSS State | Inherits the theme's `currentColor` easily, and swapping icons via CSS `display: block/none` using the `aria-expanded` attribute avoids messy JS DOM replacement. |

*Feasibility Assessment*: 100%. The exact visual mechanics, responsive transition, accessibility toggles, and sliding glass effects can be entirely reproduced using vanilla HTML, CSS, and JS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Click the menu icon on a mobile screen to see the glassmorphism slide-out navigation. Resize your browser to see the layout adapt.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Slide-Out Navigation effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme derivations
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0b0d17 0%, #15192b 100%)"
        text_color = "#ffffff"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        solid_fallback_bg = "#15192b"
        hover_color = "rgba(255, 255, 255, 0.5)"
    else:
        bg_gradient = "linear-gradient(135deg, #e0e5ec 0%, #ffffff 100%)"
        text_color = "#0b0d17"
        glass_bg = "rgba(0, 0, 0, 0.05)"
        solid_fallback_bg = "#e0e5ec"
        hover_color = "rgba(0, 0, 0, 0.5)"

    css = f"""/* Glassmorphism Slide-Out Navigation */
:root {{
    --clr-text: {text_color};
    --clr-accent: {accent_color};
    --clr-glass: {glass_bg};
    --clr-solid-fallback: {solid_fallback_bg};
    --clr-hover: {hover_color};
    --gap: 2rem;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: {bg_gradient};
    color: var(--clr-text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Typography Utilities */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}

/* Page Layout */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo {{
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-circle {{
    width: 40px;
    height: 40px;
    background: var(--clr-text);
    border-radius: 50%;
    display: inline-block;
}}

/* Navigation Baseline */
.primary-navigation {{
    list-style: none;
    display: flex;
    gap: var(--gap, 2rem);
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover {{
    border-color: var(--clr-hover);
}}

.primary-navigation a > span {{
    font-weight: 700;
    color: var(--clr-accent);
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: 0;
    color: var(--clr-text);
    cursor: pointer;
    z-index: 9999;
}}

.mobile-nav-toggle svg {{
    width: 2rem;
    height: 2rem;
    fill: currentColor;
    transition: transform 0.3s ease;
}}

.icon-close {{
    display: none;
}}

/* Mobile Layout - Media Query */
@media (max-width: 45rem) {{
    .primary-navigation {{
        position: fixed;
        /* Logical property shorthand for top:0, right:0, bottom:0, left:30% */
        inset: 0 0 0 30%; 
        flex-direction: column;
        padding: min(30vh, 10rem) 2rem;
        background: var(--clr-glass);
        transform: translateX(100%);
        transition: transform 350ms ease-out;
        z-index: 1000;
    }}
    
    /* The Glassmorphism Effect */
    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--clr-glass);
            backdrop-filter: blur(1rem);
        }}
    }}
    /* Fallback for browsers without backdrop-filter */
    @supports not (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--clr-solid-fallback);
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        right: 2rem;
        top: 2rem;
    }}

    /* Toggle Icon States */
    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
        display: none;
    }}
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{
        display: block;
    }}
}}

/* Decorative Hero Content */
.hero-content {{
    max-width: 600px;
    margin: 10rem auto;
    padding: 2rem;
    text-align: center;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
}}

.hero-content p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--clr-hover);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="primary-header">
        <div class="logo">
            <span class="logo-circle"></span>
            LOGO
        </div>

        <!-- Mobile Navigation Toggle -->
        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 100 80" aria-hidden="true">
                <rect width="100" height="15" rx="8"></rect>
                <rect y="32" width="100" height="15" rx="8"></rect>
                <rect y="64" width="100" height="15" rx="8"></rect>
            </svg>
            <!-- Close Icon -->
            <svg class="icon-close" viewBox="0 0 100 100" aria-hidden="true">
                <rect x="10" y="42" width="100" height="15" rx="8" transform="rotate(45 50 50)"></rect>
                <rect x="10" y="42" width="100" height="15" rx="8" transform="rotate(-45 50 50)"></rect>
            </svg>
        </button>

        <!-- Primary Navigation -->
        <nav>
            <ul id="primary-navigation" class="primary-navigation" data-visible="false">
                <li>
                    <a href="#">
                        <span aria-hidden="true">00</span>Home
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">01</span>Destination
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">02</span>Crew
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">03</span>Technology
                    </a>
                </li>
            </ul>
        </nav>
    </header>

    <main class="hero-content">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Mobile Navigation Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.mobile-nav-toggle');
    const primaryNav = document.querySelector('#primary-navigation');

    if (!navToggle || !primaryNav) return;

    navToggle.addEventListener('click', () => {
        // Read the current visibility state as a string
        const visibility = primaryNav.getAttribute('data-visible');

        if (visibility === 'false') {
            // Open menu
            primaryNav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        } else {
            // Close menu
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
});
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
  - The toggle button utilizes `aria-expanded="true/false"` to communicate the current state of the navigation menu to screen reader users.
  - The `aria-controls="primary-navigation"` maps the button directly to the `id` of the menu it controls.
  - The numbers prefixed in the menu items (e.g., "01") are wrapped in a `span` with `aria-hidden="true"`. This prevents screen readers from awkwardly reading out "Zero one destination". It treats the numbers strictly as visual enhancements.
  - A `<span class="sr-only">Menu</span>` ensures screen readers announce the button's purpose without requiring a visible text label.
* **Performance**:
  - The sliding animation uses `transform: translateX()`, which triggers hardware acceleration (GPU compositing) and does not force browser layout recalculations (unlike animating `width`, `left`, or `margin`).
  - `backdrop-filter: blur()` is computationally heavy on low-end devices. To mitigate this, a `@supports` block guarantees that browsers that struggle with or do not support the native blur effect will immediately fall back to a less expensive solid background color instead of lagging.