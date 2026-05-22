### 1. High-level Design Pattern Extraction

> **Skill Name**: Accessible Glassmorphic Off-Canvas Navigation

* **Core Visual Mechanism**: A responsive navigation system that seamlessly morphs from a frosted-glass, slide-out hamburger menu on mobile devices into an inline, glass-backed top navigation bar on larger screens. It uses `backdrop-filter` to create depth and spatial context, layering over background imagery.
* **Why Use This Skill (Rationale)**: Mobile screen real estate is precious. Sliding an off-canvas menu into view allows users to focus purely on content. Integrating frosted glass (`backdrop-filter`) prevents the menu from feeling entirely disconnected from the page content beneath it. Furthermore, utilizing ARIA attributes (`aria-expanded`, `aria-controls`) makes the interactive toggle transparent to assistive technologies.
* **Overall Applicability**: This is the gold standard for hero sections, landing pages, and web applications that feature rich background imagery or complex gradients, where you want the navigation to feel integrated and premium rather than boxed out in a solid header.
* **Browser Compatibility**: Uses `backdrop-filter` which is widely supported, but gracefully falls back to a more opaque background color using `@supports` for older browsers. The reproduction leverages **Container Queries** (`@container`) to map the responsive changes to the component's width itself, making it highly reusable in modular layouts.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Dependent on theme. It typically layers a deep base with a highly translucent surface. For a dark theme: `rgba(255, 255, 255, 0.05)` for the glass effect, coupled with a `blur(1rem)` backdrop filter. A fallback color like `rgba(11, 13, 23, 0.95)` is specified.
  - **Typography**: Heavily relies on uppercase sans-serif text (`text-transform: uppercase`, `letter-spacing: 2px`) for a clean, modern, editorial aesthetic. Nav items are enumerated (00, 01, 02...) with the numbers in a bolder weight to establish visual rhythm.
  - **Icons**: SVG-based hamburger and close icons that visually swap based on the toggle state.

* **Step B: Layout & Compositional Style**
  - **Mobile Layout**: The `<ul>` navigation is taken out of normal flow using absolute/fixed positioning (`inset: 0 0 0 30%`), pinning it to the top, right, and bottom, while leaving the left 30% open to indicate the page still exists underneath.
  - **Desktop Layout**: Using Flexbox, it transitions into a standard horizontal layout (`flex-direction: row`) with a fluid gap (`clamp()`).
  - **Container Queries**: Drives the transition between mobile and desktop states without relying on the window size, making the component truly portable.

* **Step C: Interactive Behavior & Animations**
  - **JavaScript State**: A click listener on the toggle button reads and updates HTML data attributes (`data-visible="true/false"`) and accessibility attributes (`aria-expanded`).
  - **Animation**: The mobile menu slides in via CSS `transform: translateX(100%)` to `translateX(0%)` with a `350ms ease-out` transition.
  - **Hover Effects**: Links feature a sleek scale-up underline effect using the `::after` pseudo-element with `transform: scaleX()` tied to the hover state.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Toggle | Container Queries (`@container`) | Allows the navigation to shift from mobile to desktop styling based on the container width instead of viewport width, ensuring component reusability. |
| Glassmorphism | CSS `backdrop-filter` + `@supports` | Native hardware-accelerated blur that blends with the content underneath. Feature queries provide a solid-color fallback for maximum reliability. |
| Off-canvas Animation | CSS `transform: translateX` | Extremely performant, GPU-accelerated sliding motion that avoids layout recalculation jitter. |
| State Management | JS manipulating `data-` attributes | Decouples styling from logic. The CSS responds to the explicit data state (`data-visible`) rather than class toggling. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Let's face it; if you want to go to space, you might as well genuinely go to outer space and not hover kind of on the edge of it. Well sit back, and relax because we'll give you a truly out of this world experience!",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Accessible Glassmorphic Off-Canvas Navigation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Establish Theme
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0b0d17 0%, #1a1a2e 100%)"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        glass_fallback = "rgba(11, 13, 23, 0.95)"
    else:
        bg_gradient = "linear-gradient(135deg, #e6e9f0 0%, #eef1f5 100%)"
        text_color = "#0b0d17"
        surface_color = "rgba(255, 255, 255, 0.4)"
        glass_fallback = "rgba(255, 255, 255, 0.95)"

    # HTML Content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Glass Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Bellefair&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="outer-wrapper">
        <div class="viewport">
            
            <header class="primary-header">
                <div class="logo">
                    <svg viewBox="0 0 48 48" width="48" height="48">
                        <circle cx="24" cy="24" r="24" fill="var(--text)"/>
                        <path d="M24 12 L36 36 L12 36 Z" fill="var(--bg)"/>
                    </svg>
                </div>
                
                <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                    <span class="sr-only">Menu</span>
                    <svg class="icon-hamburger" viewBox="0 0 100 80" width="24" height="24">
                        <rect width="100" height="15" rx="8" fill="currentColor"></rect>
                        <rect y="32" width="100" height="15" rx="8" fill="currentColor"></rect>
                        <rect y="65" width="100" height="15" rx="8" fill="currentColor"></rect>
                    </svg>
                    <svg class="icon-close" viewBox="0 0 100 100" width="24" height="24">
                        <line x1="15" y1="15" x2="85" y2="85" stroke="currentColor" stroke-width="15" stroke-linecap="round"/>
                        <line x1="85" y1="15" x2="15" y2="85" stroke="currentColor" stroke-width="15" stroke-linecap="round"/>
                    </svg>
                </button>

                <nav>
                    <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                        <li class="active"><a href="#"><span aria-hidden="true">00</span>Home</a></li>
                        <li><a href="#"><span aria-hidden="true">01</span>Destination</a></li>
                        <li><a href="#"><span aria-hidden="true">02</span>Crew</a></li>
                        <li><a href="#"><span aria-hidden="true">03</span>Technology</a></li>
                    </ul>
                </nav>
            </header>

            <main class="hero-section">
                <div class="hero-content">
                    <p class="subtitle">So, you want to travel to</p>
                    <h1 class="title">{title_text}</h1>
                    <p class="body-text">{body_text}</p>
                </div>
                <div class="hero-action">
                    <button class="cta-button">Explore</button>
                </div>
            </main>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # CSS Content
    css = f"""/* Responsive Glass Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_gradient};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --glass-fallback: {glass_fallback};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Barlow Condensed', sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
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

/* Environment Bounds */
.outer-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    background: var(--bg);
    overflow: hidden;
}}

.viewport {{
    container-type: inline-size;
    width: 100%;
    height: 100%;
    position: relative;
    color: var(--text);
    display: flex;
    flex-direction: column;
}}

/* Header & Base Nav Styling */
.primary-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: clamp(1.5rem, 5cqw, 3rem);
}}

.logo {{
    z-index: 9999;
}}

.primary-navigation {{
    display: flex;
    list-style: none;
    margin: 0;
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1.1rem;
    display: block;
    padding-block: 0.5rem;
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-inline-end: 0.75em;
}}

/* Nav Underline Hover Effect */
.primary-navigation a {{
    position: relative;
}}

.primary-navigation a::after {{
    content: '';
    position: absolute;
    bottom: -0.25rem;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--accent);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease;
}}

.primary-navigation a:hover::after,
.primary-navigation a:focus-visible::after {{
    transform: scaleX(1);
    transform-origin: left;
}}

.primary-navigation li.active a::after {{
    transform: scaleX(1);
    background: var(--text);
}}


/* Mobile First Container Query */
@container (max-width: 45rem) {{
    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        z-index: 9999;
        right: clamp(1.5rem, 5cqw, 3rem);
        top: clamp(1.5rem, 5cqw, 3rem);
        background: transparent;
        border: 0;
        cursor: pointer;
        color: var(--text);
    }}

    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; }}
    .mobile-nav-toggle[aria-expanded="false"] .icon-hamburger {{ display: block; }}
    .mobile-nav-toggle[aria-expanded="false"] .icon-close {{ display: none; }}

    .primary-navigation {{
        position: absolute;
        z-index: 1000;
        inset: 0 0 0 30%;
        flex-direction: column;
        gap: 2rem;
        padding: min(30cqh, 10rem) 2rem;
        background: var(--glass-fallback);
        transform: translateX(100%);
        transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--surface);
            backdrop-filter: blur(1.5rem);
            -webkit-backdrop-filter: blur(1.5rem);
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}
}}

/* Desktop Container Query */
@container (min-width: 45.001rem) {{
    .mobile-nav-toggle {{
        display: none;
    }}

    .primary-navigation {{
        flex-direction: row;
        gap: clamp(1.5rem, 4cqw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(2rem, 5cqw, 5rem);
        background: var(--glass-fallback);
    }}

    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--surface);
            backdrop-filter: blur(1.5rem);
            -webkit-backdrop-filter: blur(1.5rem);
        }}
    }}
}}

/* Decorative Hero Section */
.hero-section {{
    flex: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-around;
    padding: clamp(2rem, 5cqw, 8rem);
    gap: 4rem;
}}

.hero-content {{
    max-width: 450px;
}}

.subtitle {{
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 4px;
    opacity: 0.8;
    color: var(--accent);
}}

.title {{
    font-family: 'Bellefair', serif;
    font-size: clamp(5rem, 12cqw, 9rem);
    text-transform: uppercase;
    line-height: 1.1;
    margin-block: 1rem;
}}

.body-text {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}

.cta-button {{
    font-family: 'Bellefair', serif;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    border: none;
    background: var(--text);
    color: #0b0d17;
    font-size: 2rem;
    text-transform: uppercase;
    cursor: pointer;
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease;
}}

.cta-button::before {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 100%; height: 100%;
    background: var(--text);
    border-radius: 50%;
    z-index: -1;
    opacity: 0.1;
    transition: transform 0.4s ease;
}}

.cta-button:hover::before {{
    transform: translate(-50%, -50%) scale(1.5);
}}
"""

    # JS Content
    js = f"""// Accessibility & State Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const navToggle = document.querySelector('.mobile-nav-toggle');
    const primaryNav = document.querySelector('#primary-navigation');

    if (!navToggle || !primaryNav) return;

    navToggle.addEventListener('click', () => {{
        // Read explicit state from custom data attribute
        const isVisible = primaryNav.getAttribute('data-visible');

        if (isVisible === 'false') {{
            primaryNav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        }} else {{
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
        }}
    }});
}});
"""

    # Write files
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