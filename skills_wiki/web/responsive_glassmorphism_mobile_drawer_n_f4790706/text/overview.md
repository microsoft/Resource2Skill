### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Glassmorphism Mobile Drawer Navigation

* **Core Visual Mechanism**: This pattern features a sleek, slide-out mobile navigation drawer that utilizes a "frosted glass" aesthetic (`backdrop-filter: blur()`). Instead of an opaque solid color, the drawer uses a highly transparent background coupled with a strong blur effect, allowing the underlying page content to remain partially visible but out of focus. It transitions smoothly onto the screen using hardware-accelerated transforms (`translateX`).
* **Why Use This Skill (Rationale)**: The glassmorphism drawer solves the mobile navigation spatial constraint while maintaining user context. By allowing the background to blur through the menu, users don't feel like they've been transported to an entirely different page. It feels lightweight, modern, and spatially aware.
* **Overall Applicability**: Perfect for modern SaaS landing pages, portfolio sites, Web3/crypto interfaces, and any application leaning into a modern, airy, or "space" aesthetic. It's particularly effective when layered over rich, colorful photography, dynamic 3D scenes, or animated gradients.
* **Value Addition**: Compared to a standard solid-color toggle menu, this technique adds depth, tactile realism, and premium polish. The hardware-accelerated slide-in animation combined with the blur calculation makes the UI feel native and highly responsive.
* **Browser Compatibility**: The core visual (`backdrop-filter`) is supported in all modern browsers (Chrome 76+, Safari 9+, Firefox 103+, Edge 70+). A fallback solid or highly opaque background is required for legacy browsers that do not support the blur filter, achievable via the `@supports` CSS at-rule.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Semantic `<header>` containing a `<button>` (hamburger toggle) and a `<nav>` with a `<ul>` list of links.
  - **Color Logic**: Uses highly translucent backgrounds to drive the glass effect. For a dark theme, `rgba(255, 255, 255, 0.05)` to `0.1` works best.
  - **Typography**: Clean sans-serif, often tracked out (increased letter-spacing) and uppercase for primary navigation links to feel premium and structural.
  - **CSS Properties**: `backdrop-filter: blur(1rem)` is the star of the show.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox is used to align the items. On desktop, it uses `flex-direction: row`. On mobile, it switches to `flex-direction: column`.
  - **Positioning**: The mobile drawer relies on `position: fixed` to sit above the document flow. The `inset: 0 0 0 30%` shorthand is used to pin it to the top, bottom, and right, while leaving the left 30% of the screen uncovered to reveal the blurred page underneath.
  - **Responsive Spacing**: Modern CSS functions like `clamp()` are used for dynamic padding that scales with the viewport.

* **Step C: Interactive Behavior & Animations**
  - **State Management**: JavaScript is strictly used to toggle state via HTML attributes (`data-visible="true/false"` on the nav, and `aria-expanded="true/false"` on the button).
  - **Animation**: The drawer is hidden completely off-screen using `transform: translateX(100%)`. When `data-visible="true"`, it translates to `translateX(0%)`.
  - **Transitions**: `transition: transform 350ms ease-out` provides a snappy but smooth entrance.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Glassmorphism Overlay** | CSS `backdrop-filter` + `@supports` | Native browser blurring with GPU acceleration. Includes a solid background fallback for unsupported browsers. |
| **Drawer Layout** | CSS Fixed Positioning + `inset` | Ensures the drawer completely covers the right side of the viewport independently of document scroll. |
| **Slide Animation** | CSS `transform` + `transition` | Translating X coordinates avoids layout thrashing and ensures smooth 60fps animations on mobile devices. |
| **State Toggling** | JavaScript (Data Attributes) | Keeps JS decoupled from CSS. JS updates state (`data-visible`), CSS handles the visual reaction. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Explore the galaxy with our modern, glassmorphism mobile navigation drawer. Resize the window to see the responsive layout.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Mobile Drawer.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme properties
    if color_scheme == "dark":
        bg_base = "#0b0d17"
        text_color = "#ffffff"
        text_muted = "#d0d6f9"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        glass_border = "rgba(255, 255, 255, 0.1)"
        fallback_bg = "rgba(11, 13, 23, 0.95)"
        gradient_bg = "linear-gradient(135deg, #0b0d17 0%, #1a1525 100%)"
    else:
        bg_base = "#f0f2f5"
        text_color = "#0b0d17"
        text_muted = "#333333"
        glass_bg = "rgba(255, 255, 255, 0.6)"
        glass_border = "rgba(255, 255, 255, 0.8)"
        fallback_bg = "rgba(240, 242, 245, 0.95)"
        gradient_bg = "linear-gradient(135deg, #f0f2f5 0%, #e0e5ec 100%)"

    css = f"""/* Responsive Glassmorphism Mobile Drawer Navigation */
:root {{
    --clr-base: {bg_base};
    --clr-text: {text_color};
    --clr-muted: {text_muted};
    --clr-accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --fallback-bg: {fallback_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Resets */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--clr-text);
    background: {gradient_bg};
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Preview Container (Simulating a device/browser window) */
.preview-window {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-image: url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
}}

/* Layout Utility */
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

/* Header */
.primary-header {{
    align-items: center;
    justify-content: space-between;
    padding: 2rem clamp(1.5rem, 5vw, 3rem);
    position: relative;
    z-index: 1000; /* Ensure header sits above content */
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--clr-text);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.logo-circle {{
    width: 40px;
    height: 40px;
    background: var(--clr-text);
    border-radius: 50%;
    display: inline-block;
}}

/* Mobile Toggle Button */
.mobile-nav-toggle {{
    display: none;
    position: absolute;
    z-index: 9999;
    right: 2rem;
    top: 2rem;
    background: transparent;
    border: 0;
    cursor: pointer;
    width: 2rem;
    aspect-ratio: 1;
}}

.mobile-nav-toggle svg {{
    fill: var(--clr-text);
    width: 100%;
    height: 100%;
    transition: transform 0.3s ease;
}}

.icon-close {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-close {{
    display: block;
}}

/* Navigation */
.primary-navigation {{
    --gap: clamp(1.5rem, 5vw, 3rem);
    list-style: none;
    background: var(--fallback-bg);
}}

/* Glassmorphism progressive enhancement */
@supports (backdrop-filter: blur(1rem)) {{
    .primary-navigation {{
        background: var(--glass-bg);
        backdrop-filter: blur(1.5rem);
        border-left: 1px solid var(--glass-border);
    }}
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.9rem;
    display: block;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    color: var(--clr-accent);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-right: 0.5em;
    color: var(--clr-text);
    opacity: 0.6;
}}

/* Mobile Styles */
@media (max-width: 45em) {{
    .mobile-nav-toggle {{
        display: block;
    }}

    .primary-navigation {{
        flex-direction: column;
        position: absolute;
        z-index: 1000;
        inset: 0 0 0 30%; /* Start 30% from the left, cover rest */
        padding: clamp(6rem, 20vh, 10rem) 2rem;
        
        /* The Animation */
        transform: translateX(100%);
        transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0);
    }}
}}

/* Desktop Styles */
@media (min-width: 45em) {{
    .primary-navigation {{
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 7rem);
        /* Adding the glass styling to the desktop nav bar as well */
        background: var(--glass-bg);
        backdrop-filter: blur(1.5rem);
        border-left: 0;
    }}
    
    .primary-navigation span[aria-hidden="true"] {{
        display: none; /* Hide numbers on desktop for cleaner look */
    }}
}}

/* Hero Content */
.hero-content {{
    padding: clamp(2rem, 10vw, 6rem);
    max-width: 600px;
    position: relative;
    z-index: 1;
}}

.hero-subtitle {{
    text-transform: uppercase;
    letter-spacing: 4px;
    color: var(--clr-accent);
    font-size: 1.25rem;
    margin-bottom: 1rem;
}}

.hero-title {{
    font-size: clamp(3rem, 8vw, 6rem);
    line-height: 1.1;
    font-weight: 300;
    text-transform: uppercase;
    margin-bottom: 2rem;
}}

.hero-body {{
    color: var(--clr-muted);
    font-size: 1.125rem;
    line-height: 1.8;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="preview-window">
        <header class="primary-header flex">
            <a href="#" class="logo">
                <span class="logo-circle"></span>
                <span>{title_text}</span>
            </a>
            
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <!-- Hamburger Icon -->
                <svg class="icon-hamburger" viewBox="0 0 100 80" width="40" height="40">
                    <rect width="100" height="15"></rect>
                    <rect y="30" width="100" height="15"></rect>
                    <rect y="60" width="100" height="15"></rect>
                </svg>
                <!-- Close Icon -->
                <svg class="icon-close" viewBox="0 0 100 100" width="40" height="40">
                    <polygon points="100,10.6 89.4,0 50,39.4 10.6,0 0,10.6 39.4,50 0,89.4 10.6,100 50,60.6 89.4,100 100,89.4 60.6,50 "/>
                </svg>
            </button>

            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation flex">
                    <li><a href="#"><span aria-hidden="true">00</span>Home</a></li>
                    <li><a href="#"><span aria-hidden="true">01</span>Destination</a></li>
                    <li><a href="#"><span aria-hidden="true">02</span>Crew</a></li>
                    <li><a href="#"><span aria-hidden="true">03</span>Technology</a></li>
                </ul>
            </nav>
        </header>

        <main class="hero-content">
            <p class="hero-subtitle">So, you want to travel to</p>
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    // Toggle navigation drawer on click
    navToggle.addEventListener('click', () => {
        // Get the current state
        const visibility = nav.getAttribute('data-visible');
        
        // Toggle the states
        if (visibility === "false") {
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        } else {
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
        }
    });

    // Accessibility & UX Improvement: Close menu on hitting 'Escape'
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && nav.getAttribute('data-visible') === "true") {
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
            navToggle.focus(); // Return focus to the button
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

* **Accessibility (A11y)**: 
  * The toggle button effectively utilizes `aria-controls="primary-navigation"` to bind the button to the drawer semantically.
  * State tracking is fully exposed to screen readers via `aria-expanded="true/false"`.
  * The button text "Menu" is placed inside a visually hidden element (`.sr-only`), ensuring screen reader users hear what the button does instead of having it skipped because the visual icons are pure SVGs.
  * Decorative numbers ("00", "01") have `aria-hidden="true"` so screen readers will natively read just the link context ("Home", "Destination").
  * **Enhancement Added**: A keyboard listener triggers on "Escape" to close the menu and return focus to the toggle button, satisfying critical WCAG keyboard navigability requirements.
* **Performance**: 
  * Avoids manipulating CSS `left`, `right`, or `width` for the slide animation. Those trigger heavy browser layout recalculations. By using `transform: translateX()`, the browser moves the drawer exclusively on the GPU layer (Compositor), resulting in smooth 60fps animations.
  * The `backdrop-filter` is resource-intensive on low-end devices. Browsers that struggle generally turn it off natively, falling back gracefully to the opaque background color provided inside the `:root` variables.