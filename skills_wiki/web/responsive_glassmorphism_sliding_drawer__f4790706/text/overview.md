### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Glassmorphism Sliding Drawer Navigation

* **Core Visual Mechanism**: This pattern leverages a mobile-first sliding off-canvas drawer that seamlessly transitions into a spacious, inline flexbox navigation bar on larger screens. The defining aesthetic is a frosted-glass overlay (`backdrop-filter: blur()`) paired with semi-transparent backgrounds, creating a sense of depth and modernity. State transitions are governed by CSS transforms (`translateX(100%)`) for smooth, GPU-accelerated motion, tied to HTML `data-*` attributes updated via JavaScript.
* **Why Use This Skill (Rationale)**: Navigation is often the most critical interactive component of a site. This method solves the mobile-menu space constraint elegantly without feeling disjointed from the desktop experience. Using `backdrop-filter` maintains visual context of the page beneath the menu, preventing the user from feeling "lost" or taken to a completely new view.
* **Overall Applicability**: Ideal for visually rich websites—such as portfolios, SaaS landing pages, gaming hubs, or promotional sites (like the Space Tourism example)—where immersive background imagery or gradients should not be completely obscured by solid-color UI elements. 
* **Value Addition**: Compared to a standard block-level navigation, this technique adds a premium, "app-like" fluid feel. The accessibility features (`aria-controls`, `aria-expanded`, screen-reader-only text) ensure this visually appealing component remains fully usable for assistive technologies.
* **Browser Compatibility**: Requires modern browsers for `backdrop-filter` (supported in >90% of browsers globally; Safari requires prefix or specific flags in older versions, though widely supported now). `clamp()` and logical properties (`margin-inline-end`) are fully supported in modern engines.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Uses a semi-transparent surface color (e.g., `rgba(255, 255, 255, 0.05)`) over a dark or complex background to create the "glass" effect.
  - **Typographic Hierarchy**: High contrast sans-serif or condensed fonts. Menu items often prefixed with numbers (`00`, `01`, `02`) styled with a bolder weight (`font-weight: 700`) to create a technical, structured rhythm.
  - **Key CSS Properties**: `backdrop-filter: blur(1rem)` for the frosted glass; `display: flex` for horizontal/vertical alignment; `transform: translateX()` for the sliding mechanism.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Predominantly Flexbox (`display: flex`, `justify-content: space-between`).
  - **Spatial Feel**: Heavy use of whitespace, driven by CSS `gap` for item spacing and `clamp()` for fluid horizontal padding that scales with the viewport.
  - **Z-index Layering**: The mobile navigation toggle button sits at `z-index: 9999` (absolute/fixed) to guarantee it always overlays the sliding drawer, which operates on its own high z-index stacking context.

* **Step C: Interactive Behavior & Animations**
  - **State Machine**: Driven by `aria-expanded="true/false"` on the toggle button and `data-visible="true/false"` on the `<ul>` element.
  - **Motion**: The drawer slides in from the right. `transition: transform 350ms ease-out` provides a natural deceleration as the menu enters the viewport.
  - **JS Role**: Extremely minimal. JavaScript strictly toggles the string values of the data and aria attributes. CSS handles all the visual rendering of those states.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Frosted Glass Drawer** | CSS `backdrop-filter` | Native, performant blur effect that creates depth without needing duplicate canvas layers. |
| **Mobile Drawer Motion** | CSS `transform: translateX()` | GPU-accelerated property; avoids layout recalculation (reflow) during animation, preventing jank. |
| **Responsive Scaling** | CSS `clamp()`, Flexbox | `clamp()` provides fluid padding across screen sizes; Flexbox handles axis switching effortlessly. |
| **Menu Toggle Logic** | Vanilla JS + DOM Data Attributes | Keeps state firmly in the DOM (`data-visible`), creating a clean separation of concerns between JS (logic) and CSS (styling). |
| **Hamburger/Close Icon** | Inline SVG | Self-contained, scalable, and easy to swap states using CSS `display` based on the parent button's `aria-expanded` state. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Space Elements",
    body_text: str = "Explore the fluid frosted-glass navigation menu. Resize the browser to see the layout adapt, and click the menu toggle on mobile sizes.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Sliding Drawer Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_gradient = "radial-gradient(circle at bottom right, #1a0b2e, #0d111c, #000000)"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.6)"
        surface_color = "rgba(255, 255, 255, 0.05)"
        hover_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_gradient = "radial-gradient(circle at top left, #f0f4ff, #e5e9f0, #ffffff)"
        text_color = "#0b0c10"
        text_muted = "rgba(0, 0, 0, 0.5)"
        surface_color = "rgba(255, 255, 255, 0.6)"
        hover_bg = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navigation */
:root {{
    --clr-text: {text_color};
    --clr-muted: {text_muted};
    --clr-accent: {accent_color};
    --clr-surface: {surface_color};
    --clr-hover: {hover_bg};
    
    --ff-sans: 'Inter', system-ui, -apple-system, sans-serif;
    --ff-condensed: 'Oswald', sans-serif;
    
    --gap: 2rem;
}}

/* Reset */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body, h1, h2, h3, p, ul, li {{
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--ff-sans);
    background: {bg_gradient};
    color: var(--clr-text);
    min-height: 100vh;
    overflow-x: hidden; /* Prevent horizontal scroll from off-canvas menu */
    display: flex;
    flex-direction: column;
}}

/* Utility Classes */
.flex {{
    display: flex;
    gap: var(--gap, 1rem);
}}

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

/* Header Layout */
.primary-header {{
    align-items: center;
    justify-content: space-between;
    padding: 2rem;
    position: relative;
    z-index: 1000;
}}

.logo svg {{
    width: 48px;
    height: 48px;
    fill: var(--clr-text);
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: 0;
    cursor: pointer;
    position: absolute;
    z-index: 9999;
    right: 2rem;
    top: 2rem;
    padding: 0.5rem;
}}

.mobile-nav-toggle svg {{
    width: 24px;
    height: 24px;
    fill: var(--clr-text);
    transition: transform 0.3s ease;
}}

.mobile-nav-toggle .icon-close {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-close {{
    display: block;
}}

/* Primary Navigation Styles */
.primary-navigation {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    font-family: var(--ff-condensed);
    letter-spacing: 2px;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75em;
    padding: 0.5rem 0;
    position: relative;
}}

.primary-navigation a::after {{
    content: '';
    position: absolute;
    bottom: -0.5rem;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--clr-text);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease;
}}

.primary-navigation a:hover::after,
.primary-navigation a:focus::after {{
    transform: scaleX(1);
    transform-origin: left;
}}

.primary-navigation a span {{
    font-weight: 700;
    color: var(--clr-muted);
}}

/* Mobile specific styling */
@media (max-width: 45em) {{
    .primary-navigation {{
        --gap: 2em;
        position: fixed;
        inset: 0 0 0 30%; /* Drawer width: 70% of viewport */
        flex-direction: column;
        padding: min(20vh, 10rem) 2em;
        z-index: 1000;
        
        /* Glassmorphism */
        background: var(--clr-surface);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        
        /* Off-canvas setup */
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    /* Fallback for browsers that don't support backdrop-filter */
    @supports not (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: {bg_gradient};
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
    }}
}}

/* Desktop specific styling */
@media (min-width: 45em) {{
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 10rem);
        
        /* Glassmorphism Inline Header */
        background: var(--clr-surface);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
    }}
}}

/* Main Content Area */
main {{
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.hero-content {{
    max-width: 600px;
    text-align: center;
}}

.hero-content h1 {{
    font-size: clamp(2rem, 5vw, 4rem);
    font-family: var(--ff-condensed);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1rem;
}}

.hero-content h1 span {{
    color: var(--clr-accent);
}}

.hero-content p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--clr-muted);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="primary-header flex">
        <div class="logo">
            <!-- Mock Logo SVG -->
            <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="10 5" />
                <circle cx="24" cy="24" r="10" fill="currentColor"/>
            </svg>
        </div>

        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <rect y="4" width="24" height="3" rx="1.5"/>
                <rect y="11" width="24" height="3" rx="1.5"/>
                <rect y="18" width="24" height="3" rx="1.5"/>
            </svg>
            <!-- Close Icon -->
            <svg class="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" data-visible="false" class="primary-navigation flex">
                <li class="active"><a href="#"><span aria-hidden="true">00</span> Home</a></li>
                <li><a href="#"><span aria-hidden="true">01</span> Destination</a></li>
                <li><a href="#"><span aria-hidden="true">02</span> Crew</a></li>
                <li><a href="#"><span aria-hidden="true">03</span> Technology</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="hero-content">
            <h1>Explore <span>{title_text}</span></h1>
            <p>{body_text}</p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation State Management
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!primaryNav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Get the current state as a string from the custom data attribute
        const visibility = primaryNav.getAttribute('data-visible');

        // Toggle state based on the current value
        if (visibility === "false") {{
            primaryNav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
            primaryNav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the dynamic injection parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Are `title_text` and `body_text` appropriately mapped?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect (mobile side-drawer with blur, desktop inline nav)?

### 4. Accessibility & Performance Notes

* **Accessibility (A11y)**: 
  * The toggle `<button>` uses an inner `<span class="sr-only">` to ensure screen reader users hear "Menu" when focusing on the hamburger icon.
  * Structural numbers inside the navigation (`00`, `01`, etc.) use `aria-hidden="true"`. This prevents screen readers from obtrusively dictating "zero zero Home", reading just the relevant link text ("Home") instead.
  * The `aria-controls` attribute pairs the button functionally with the `id` of the unordered list. The `aria-expanded` updates dynamically via JS to actively communicate the drawer's visibility state.
* **Performance**: 
  * The drawer sliding effect is strictly driven by `transform: translateX()`, moving the element onto the GPU compositor thread and entirely bypassing layout reflows during the animation.
  * The `backdrop-filter` carries a small rendering penalty but is offset visually. We use `@supports` queries to fall back to a simpler background gradient block if the filter fails, ensuring graceful degradation. No un-throttled JS listeners are used.