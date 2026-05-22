### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Glassmorphism Navbar with Off-Canvas Sidebar

* **Core Visual Mechanism**: This pattern implements a clean, flexbox-driven horizontal navigation bar that gracefully collapses on smaller viewports. Instead of a standard dropdown, it introduces an off-canvas sidebar with a frosted-glass overlay (`backdrop-filter: blur()`). The semi-transparent glassmorphism creates spatial depth and layered hierarchy, allowing the user to faintly see the page content underneath.
* **Why Use This Skill (Rationale)**: Hiding secondary links behind a hamburger menu on mobile is standard UX practice, but implementing it as a sliding glass sidebar solves two problems: it provides large, touch-friendly hit areas for mobile users, and the transparency preserves the user's context (they don't feel like they've been taken to a completely new page).
* **Overall Applicability**: Universal component. Perfect for SaaS landing pages, portfolios, blogs, and administrative dashboards that require responsive design.
* **Value Addition**: Replaces abrupt `display: none/block` toggles with a smooth, hardware-accelerated slide-in animation. Container queries make the component hyper-resilient, meaning it responds to the width of its parent container rather than just the browser viewport.
* **Browser Compatibility**: Excellent. `backdrop-filter` is supported natively in all modern browsers (we include `-webkit-` for older Safari). Container queries (`@container`) are supported in all major browsers since late 2022.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color & Material Logic**: Solid, slightly elevated background for the top navbar. Translucent layer for the sidebar (e.g., `rgba(255, 255, 255, 0.5)` with `blur(12px)`) to mimic frosted glass. Text color uses high-contrast solids.
  - **Typography**: Sans-serif (Inter or system-ui), with the logo utilizing a bolder weight (`700`) to naturally establish hierarchy without requiring an image.
  - **Iconography**: Inline SVG icons (`currentColor`) ensure they automatically inherit the text color of the parent anchor tags, keeping hover states consistent.

* **Step B: Layout & Compositional Style**
  - **Horizontal Flow (Desktop)**: A single `<ul>` element styled with `display: flex`. The "Logo" list item uses `margin-right: auto` to elegantly push all subsequent links to the far right, eliminating the need for complex grid tracking or absolute positioning.
  - **Vertical Stack (Mobile)**: The sidebar `<ul>` swaps to `flex-direction: column`. Link anchors are expanded to `width: 100%` with padded boxes, creating highly accessible, full-bleed touch targets.
  - **Breakpoints**: 
    - `< 800px`: Hide desktop links, show hamburger menu.
    - `< 400px`: Expand the sliding sidebar from `250px` to `100%` width to maximize mobile screen usage.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Light background tint applied to anchor tags on hover, coupled with a subtle text color shift to the accent color.
  - **State Management**: JS is decoupled from HTML structure. An event listener toggles an `.active` class on the sidebar.
  - **Animation**: Instead of a jarring `display` swap, the sidebar uses `transform: translateX(100%)` to stay hidden off-screen, shifting to `translateX(0)` with a `0.3s cubic-bezier` transition for an organic slide-in feel.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Logic** | CSS Container Queries | `@container` allows the component to react to the `width_px` parameter contextually, rather than relying on the global window viewport. |
| **Navbar Spacing** | Flexbox + Auto Margin | `margin-right: auto` on the first element perfectly pins the logo to the left and links to the right. |
| **Sidebar Overlay** | CSS `backdrop-filter` | Native, performant rendering of the glassmorphism blur effect without external JS libraries. |
| **Off-canvas Animation** | CSS Transforms | Modifying `transform: translateX` is GPU-accelerated, ensuring 60fps sliding animations (unlike animating `width` or `margin`). |
| **Menu Icons** | Inline SVG | Lightweight, scalable, and dynamically inherits CSS colors via `fill="currentColor"`. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Responsive Glassmorphism Navigation",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a responsive glassmorphism navbar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg = "#111827"
        text_color = "#f9fafb"
        sidebar_bg = "rgba(17, 24, 39, 0.6)"
        hover_bg = "rgba(255, 255, 255, 0.1)"
    else:
        nav_bg = "#ffffff"
        text_color = "#1f2937"
        sidebar_bg = "rgba(255, 255, 255, 0.5)"
        hover_bg = "#f3f4f6"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text: {text_color};
    --sidebar-bg: {sidebar_bg};
    --hover-bg: {hover_bg};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #1a1a1a; /* Background for the iframe/browser body */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* The isolated preview container demonstrating responsiveness */
.preview-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
    
    /* Container Queries Setup */
    container-name: preview;
    container-type: inline-size;
    
    display: flex;
    flex-direction: column;
}}

/* === Main Navbar === */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 10;
}}

.desktop-nav {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}}

.desktop-nav li {{
    height: 60px;
}}

.desktop-nav a {{
    height: 100%;
    padding: 0 24px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text);
    transition: background-color 0.2s ease, color 0.2s ease;
    font-weight: 500;
}}

.desktop-nav a:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

/* Push everything else to the right */
.desktop-nav .logo {{
    margin-right: auto;
}}

.desktop-nav .logo a {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.desktop-nav .logo a:hover {{
    background-color: transparent;
    color: var(--text);
}}

/* === Off-Canvas Sidebar === */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: -10px 0 15px rgba(0, 0, 0, 0.1);
    
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    
    /* Sliding Animation */
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.sidebar.active {{
    transform: translateX(0);
}}

.sidebar li {{
    width: 100%;
    list-style: none;
}}

.sidebar a {{
    width: 100%;
    height: 60px;
    padding: 0 24px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text);
    transition: background-color 0.2s ease, color 0.2s ease;
    font-weight: 500;
}}

.sidebar a:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

/* === Responsive Breakpoints using Container Queries === */
.menu-button {{
    display: none;
}}

@container preview (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: flex;
    }}
}}

@container preview (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}

/* === Demo Content === */
.content {{
    flex: 1;
    padding: 4rem 2rem;
    color: #fff;
    overflow-y: auto;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 600px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        
        <nav aria-label="Main navigation">
            <!-- Off-Canvas Sidebar -->
            <ul class="sidebar" aria-hidden="true">
                <li class="close-button">
                    <a href="#" aria-label="Close menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26" fill="currentColor">
                            <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
                        </svg>
                    </a>
                </li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>

            <!-- Standard Desktop Navbar -->
            <ul class="desktop-nav">
                <li class="logo"><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button">
                    <a href="#" aria-label="Open menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26" fill="currentColor">
                            <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main class="content">
            <h1>{body_text}</h1>
            <p>This component utilizes container queries to demonstrate responsive behavior. Try adjusting the <code>width_px</code> parameter or rendering it in a smaller iframe to watch the navigation bar dynamically collapse into a glassmorphism sidebar menu.</p>
        </main>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Sidebar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-button a');
    const closeBtn = document.querySelector('.close-button a');

    // Open Sidebar
    menuBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.classList.add('active');
        sidebar.setAttribute('aria-hidden', 'false');
    });

    // Close Sidebar
    closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.classList.remove('active');
        sidebar.setAttribute('aria-hidden', 'true');
    });

    // Optional: Close sidebar when clicking outside of it
    document.addEventListener('click', (e) => {
        if (sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            !menuBtn.contains(e.target)) {
            sidebar.classList.remove('active');
            sidebar.setAttribute('aria-hidden', 'true');
        }
    });
});
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
  - `aria-label` tags were added to the icon-only buttons (Hamburger menu and Close menu) to ensure they are properly identified by screen readers.
  - The script dynamically manages the `aria-hidden` attribute on the sidebar container, informing screen readers when the menu context appears or disappears.
* **Performance**: 
  - Substituted the tutorial's `display: none` to `display: flex` JavaScript logic with a CSS class toggle (`.active`). This allows the sidebar to utilize `transform: translateX` for off-canvas movement, which is GPU-accelerated and eliminates layout jank.
  - Using `-webkit-backdrop-filter` alongside the standard syntax ensures the blur operation correctly triggers hardware compositing in WebKit-based browsers.