### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Glassmorphism Navbar & Overlay Drawer

* **Core Visual Mechanism**: A horizontally aligned flexbox navigation bar that elegantly collapses its desktop links on smaller viewports. It relies on a CSS `backdrop-filter: blur()` applied to an absolutely positioned sidebar drawer, creating a frosted-glass ("glassmorphism") effect that overlays the main content while allowing the page background to faintly show through. 
* **Why Use This Skill (Rationale)**: Maintaining an uncluttered UI on mobile devices is critical. By combining CSS Flexbox with Media/Container queries, you gracefully handle information density. The glassmorphism sidebar provides a high-end, native-app-like feel, allowing users to retain spatial context of the page they were viewing behind the blurred layer.
* **Overall Applicability**: Essential for SaaS landing pages, portfolio sites, dashboards, and almost any modern web layout that requires primary navigation that adapts across device sizes (desktop to mobile).
* **Value Addition**: Transforms a static list of links into an interactive, space-conscious menu system. The frosted overlay introduces a sense of depth (Z-axis layering), making the UI feel tactile and premium compared to flat, opaque background colors.
* **Browser Compatibility**: Broadly supported. `backdrop-filter` is supported in all modern browsers (requires `-webkit-` prefix for older Safari). The enhanced implementation provided below uses CSS `@container` queries to ensure the component adapts to its parent container's width, which is supported in modern browsers (Chrome 105+, Safari 16+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Constructs**: A semantic `<nav>` wrapper containing two unordered lists (`<ul>`)—one for the desktop horizontal view, one for the mobile sidebar drawer. 
  - **Color Logic**: Uses a semi-transparent background for the sidebar (`rgba(255, 255, 255, 0.4)` for light mode or `rgba(20, 20, 25, 0.6)` for dark mode) to ensure the blur effect is visible. 
  - **Typography**: Clean, sans-serif typography (e.g., Google's Inter or system UI fonts), using bold weights for the Logo/Brand element to establish hierarchy.
  - **CSS Properties**: The heavy lifting is done via `backdrop-filter: blur(12px)` for the glass effect, and `box-shadow` to create visual separation from the background. Inline SVGs inherit the current text color via `fill="currentColor"`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Flexbox. `justify-content: flex-end` groups links to the right, while applying `margin-right: auto` to the first child (Logo) automatically pushes it to the far left.
  - **Responsive Layers**: The sidebar escapes the document flow using absolute/fixed positioning, layered on top using `z-index`. 

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: A subtle background color shift on link hover provides tactile feedback.
  - **JavaScript Behavior**: Minimal vanilla JS is used to toggle the `display` state of the sidebar between `none` and `flex`.
  - **Responsive Triggers**: Container queries dictate state changes. At `<= 800px`, standard links hide and the menu icon appears. At `<= 400px`, the drawer expands from `250px` to `100%` width to maximize tap targets on small phones.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout | CSS Flexbox & Container Queries | `justify-content` and `auto` margins create dynamic spacing without hardcoded values. Container queries allow the component to be responsive to its bounding box. |
| Frosted Sidebar | CSS `backdrop-filter` | Native GPU-accelerated blur that creates the signature "glass" aesthetic over dynamic backgrounds. |
| Icons | Inline SVG | Ensures the component is entirely self-contained without needing to fetch external FontAwesome/Material asset libraries. |
| Drawer Toggle | Vanilla JS | A simple event-driven approach modifying the inline `display` style is highly performant and easy to read. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Resize the container to see the navbar collapse into a responsive hamburger menu. Click the menu to reveal the glassmorphism sidebar.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        nav_bg = "rgba(20, 20, 25, 0.95)"
        text_color = "#ffffff"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "rgba(20, 20, 25, 0.5)"
        # Complex gradient to show off the backdrop-filter blur
        body_bg = f"radial-gradient(circle at top right, {accent_color}40, transparent 40%), radial-gradient(circle at bottom left, {accent_color}40, transparent 40%), #0d111c"
    else:
        nav_bg = "rgba(255, 255, 255, 0.95)"
        text_color = "#111111"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        sidebar_bg = "rgba(255, 255, 255, 0.5)"
        body_bg = f"radial-gradient(circle at top right, {accent_color}30, transparent 40%), radial-gradient(circle at bottom left, {accent_color}30, transparent 40%), #f4f4f9"

    css = f"""/* Responsive Glassmorphism Navbar */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-bg: {sidebar_bg};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #111; /* Outer presentation background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Viewport frame acts as a simulated device screen */
.viewport-frame {{
    width: var(--width);
    height: var(--height);
    background: var(--body-bg);
    position: relative;
    overflow: hidden;
    container-type: inline-size;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    position: relative;
    z-index: 100;
}}

nav ul {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}}

nav li {{
    height: 60px;
}}

nav a {{
    height: 100%;
    padding: 0 24px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text);
    transition: background-color 0.2s ease;
    font-weight: 500;
}}

nav a:hover {{
    background-color: var(--hover-bg);
}}

/* Auto margin pushes the first item (Logo) to the far left */
nav li:first-child {{
    margin-right: auto;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

/* Sidebar Menu - Glassmorphism Drawer */
.sidebar {{
    position: absolute; /* Absolute relative to .viewport-frame */
    top: 0;
    right: 0;
    height: 100%;
    width: 280px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
    display: none; /* Toggled via JS */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
    justify-content: flex-start;
}}

.menu-button {{
    display: none;
}}

/* Main Content Styling */
.content {{
    padding: 4rem 3rem;
    color: var(--text);
    max-width: 800px;
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.content p {{
    font-size: 1.15rem;
    line-height: 1.7;
    opacity: 0.85;
}}

/* Container Queries for Responsiveness */
@container (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

@container (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

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
    <div class="viewport-frame">
        <nav>
            <!-- Mobile Sidebar Drawer -->
            <ul class="sidebar">
                <li onclick="hideSidebar()">
                    <a href="#" aria-label="Close Menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="28" viewBox="0 -960 960 960" width="28" fill="currentColor">
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
            <ul>
                <li><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button" onclick="showSidebar()">
                    <a href="#" aria-label="Open Menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="28" viewBox="0 -960 960 960" width="28" fill="currentColor">
                            <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Expose functions globally to act as event handlers for the inline HTML attributes
window.showSidebar = function() {
    const sidebar = document.querySelector('.sidebar');
    // Change display from none to flex to reveal the drawer
    sidebar.style.display = 'flex';
};

window.hideSidebar = function() {
    const sidebar = document.querySelector('.sidebar');
    // Hide the drawer
    sidebar.style.display = 'none';
};
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

#### 3c. Verification Checklist
- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs? (Google Fonts loaded)
- [x] Does the component respect the `width_px` and `height_px` parameters? (Implemented via a `.viewport-frame` wrapper using Container Queries so resizing perfectly triggers mobile layout)
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - `aria-label` attributes have been added to the SVG icon buttons so screen readers can correctly announce them as "Open Menu" and "Close Menu".
  - The SVGs utilize `fill="currentColor"`, ensuring they dynamically pass color contrast checks by matching the text styling rules of their parent elements.
* **Performance**: 
  - `backdrop-filter` is hardware-accelerated. However, utilizing it extensively on large, complex scrolling elements can cause minor repaints. Since it's limited to the navigation sidebar bounds, the performance impact is negligible.
  - The DOM query for toggling the sidebar is localized and only invoked strictly on user interaction. Using inline `display: none` to `display: flex` behaves instantly without relying on heavy animation frameworks.