# Full-Height Dashboard Grid Layout with Expandable Sidebar

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Height Dashboard Grid Layout with Expandable Sidebar

* **Core Visual Mechanism**: A classic admin or web-app dashboard layout structured entirely using CSS Grid's `grid-template-areas`. It creates a highly readable, semantic layout matrix (sidebar, header, main, footer). The key visual flair is an interactive sidebar that smoothly expands and collapses via a JavaScript class toggle, which animates the `grid-template-columns` property natively.
* **Why Use This Skill (Rationale)**: CSS Grid areas make 2D structural layouts trivial to read and modify. Instead of nesting multiple flexbox containers or using absolute positioning hacks for sidebars, the entire structural skeleton is defined in one place. Animating grid tracks (like `grid-template-columns`) allows for seamless, responsive resizing of the main content area alongside the sidebar.
* **Overall Applicability**: Core layout scaffolding for SaaS platforms, user dashboards, admin panels, documentation sites, and complex web applications. 
* **Value Addition**: Provides a robust, full-viewport skeleton that handles fixed-width (or dynamic) sidebars and auto-expanding main content areas cleanly. The CSS Grid layout prevents content overlap and ensures headers/footers respect the space of the sidebar automatically.
* **Browser Compatibility**: CSS Grid is universally supported in modern browsers. The ability to smoothly animate `grid-template-columns` is supported in all major modern browsers (Chrome 107+, Safari 16.4+, Firefox 66+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * Semantic HTML skeleton using `<aside>` (sidebar), `<header>`, `<main>`, and `<footer>`.
  * **Color Logic**: A distinct dark sidebar (e.g., `#1d1d29`) contrasted against a lighter main content background (`#f3f3f3`) with white surface cards (`#ffffff`). 
  * **Typographic Hierarchy**: System sans-serif fonts, ensuring the app feels native to the user's OS.
  * A circular floating button overlapping the border between the sidebar and the main content, acting as the toggle switch.

* **Step B: Layout & Compositional Style**
  * **Layout System**: CSS Grid defined on the parent container.
  * **Track Sizing**: Columns are set as `var(--sidebar-width, 5rem) 1fr`. Rows are `auto 1fr auto` (allowing header and footer to size to their content, while main fills the rest).
  * **Grid Areas Matrix**:
    ```css
    "sidebar header"
    "sidebar main"
    "sidebar footer"
    ```
  * Z-index layering: The toggle button uses absolute positioning (`inset`, `right: -0.75rem`) to pop halfway out of the sidebar, hovering over the main content track.

* **Step C: Interactive Behavior & Animations**
  * **JavaScript Toggle**: A simple event listener intercepts clicks on the resize button and toggles an `.sb-expand` class on the parent container.
  * **Grid Animation**: The parent container uses `transition: grid-template-columns 0.3s ease`. When `.sb-expand` is applied, a CSS variable `--sidebar-width` changes from `5rem` to `15rem`, smoothly pushing the main content to the right.
  * The toggle button chevron rotates 180 degrees via `transform: rotate()` to indicate the new state.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Macro Layout Skeleton** | CSS Grid (`grid-template-areas`) | Unmatched for creating readable, structured 2D matrices without nesting divs. |
| **Sidebar Resizing** | Native Grid Animation | Animating `grid-template-columns` handles the reflow of adjacent columns automatically without JS calculation. |
| **Hover/Click Interaction** | JavaScript DOM + CSS | JS simply toggles a class; CSS handles all visual states and transitions, keeping concerns separated. |
| **Content Arrangement** | Nested CSS Grid (`auto-fit`) | Used inside the main area to demonstrate how content cards elegantly reflow when the sidebar takes up more space. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Welcome to your control panel. Here is a summary of your recent activity.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#4f46e5",     # Indigo accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Full-Height Dashboard Grid Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        sidebar_color = "#020617"
        border_color = "#334155"
    else:
        bg_color = "#f1f5f9"
        surface_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        sidebar_color = "#1e293b"
        border_color = "#e2e8f0"

    # === CSS ===
    css = f"""/* Dashboard Layout Component */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --sidebar-color: {sidebar_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background to frame the component */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.dashboard-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    color: var(--text-color);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    
    /* Core Layout Engine */
    display: grid;
    --sidebar-width: 5rem;
    grid-template-columns: var(--sidebar-width) 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
    transition: grid-template-columns 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.dashboard-container.sb-expand {{
    --sidebar-width: 16rem;
}}

/* Sidebar Elements */
.sidebar {{
    grid-area: sidebar;
    background-color: var(--sidebar-color);
    color: #fff;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 0;
    z-index: 10;
}}

.dashboard-container.sb-expand .sidebar {{
    align-items: flex-start;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}}

.logo-icon {{
    font-size: 2rem;
    line-height: 1;
    margin-bottom: 3rem;
    color: var(--accent-color);
}}

.logo-text {{
    display: none;
    font-size: 1.25rem;
    font-weight: 700;
    margin-left: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.dashboard-container.sb-expand .logo-icon {{
    display: inline-flex;
    align-items: center;
}}

.dashboard-container.sb-expand .logo-text {{
    display: inline-block;
    opacity: 1;
}}

.nav-placeholder {{
    width: 2rem;
    height: 2rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    margin-bottom: 1rem;
}}

.dashboard-container.sb-expand .nav-placeholder {{
    width: 100%;
    height: 2.5rem;
}}

/* Resize Button */
.resize-btn {{
    position: absolute;
    top: 5rem;
    right: -0.75rem;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    background-color: var(--accent-color);
    color: #fff;
    border: 2px solid var(--sidebar-color);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: bold;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 20;
}}

.dashboard-container.sb-expand .resize-btn {{
    transform: rotate(180deg);
}}

.resize-btn:hover {{
    transform: scale(1.1);
}}
.dashboard-container.sb-expand .resize-btn:hover {{
    transform: rotate(180deg) scale(1.1);
}}

/* Main Structure Areas */
.header {{
    grid-area: header;
    background-color: var(--surface-color);
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
}}

.header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.main {{
    grid-area: main;
    padding: 2rem;
    overflow-y: auto;
}}

.main > p {{
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.6;
}}

.footer {{
    grid-area: footer;
    background-color: var(--surface-color);
    padding: 1rem 2rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.875rem;
    color: var(--text-muted);
}}

/* Nested Card Grid demonstrating layout reflow */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.card-title {{
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

.card-value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-container">
        
        <aside class="sidebar">
            <div class="logo-icon">⬡<span class="logo-text">Brand</span></div>
            <div class="nav-placeholder"></div>
            <div class="nav-placeholder"></div>
            <div class="nav-placeholder"></div>
            
            <button id="resize" class="resize-btn" title="Toggle Sidebar">❯</button>
        </aside>
        
        <header class="header">
            <h1>{safe_title}</h1>
        </header>
        
        <main class="main">
            <p>{safe_body}</p>
            
            <div class="card-grid">
                <div class="card">
                    <div class="card-title">Total Users</div>
                    <div class="card-value">5.6K</div>
                </div>
                <div class="card">
                    <div class="card-title">Revenue</div>
                    <div class="card-value">$10.5K</div>
                </div>
                <div class="card">
                    <div class="card-title">Active Tasks</div>
                    <div class="card-value">12</div>
                </div>
                <div class="card">
                    <div class="card-title">Pending</div>
                    <div class="card-value">70</div>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            &copy; 2024 Dashboard Grid Architecture
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dashboard Layout Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const resizeBtn = document.getElementById('resize');
    const container = document.querySelector('.dashboard-container');

    // Toggle the sidebar expansion class
    resizeBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        container.classList.toggle('sb-expand');
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

#### 3c. Verification Checklist
- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme` logic successfully generate dark/light themes?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the CSS grid area technique shown in the tutorial?

### 4. Accessibility & Performance Notes

* **Accessibility**:
  * Ensure the resize `<button>` has a descriptive `title` and `aria-label` for screen readers, as the icon (`❯`) is visual-only.
  * The main content area (`<main>`) handles internal scrolling, allowing users to scroll dashboard contents without losing the sticky navigation/header contexts.
  * Contrast ratios between sidebar text/icons and the dark sidebar background easily pass WCAG standards.
* **Performance**:
  * Animating `grid-template-columns` is slightly more computationally heavy than animating `transform` due to triggering layout/reflow steps in the rendering engine. However, for a single macroscopic layout container expanding on a click event (not continuous scroll), the visual payoff far outweighs the minor performance cost in modern browsers.
  * Will degrade perfectly: If a browser does not support animating `grid-template-columns`, the layout simply snaps instantly between collapsed and expanded states without breaking the page.