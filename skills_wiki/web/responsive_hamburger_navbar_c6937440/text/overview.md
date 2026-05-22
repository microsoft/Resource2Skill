# Web Component Extraction: Responsive Hamburger Navbar

## 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Hamburger Navbar

* **Core Visual Mechanism**: The component leverages CSS Flexbox to distribute space between a brand logo and a navigation list. At a specific viewport width (the breakpoint), a media query (or container query) dynamically overrides the flex directions, transforming the horizontal list into a stacked vertical column. A CSS-drawn "hamburger" icon (three `span` bars) appears, acting as a toggle switch that injects an `.active` class via JavaScript to unhide the collapsed mobile menu.
* **Why Use This Skill (Rationale)**: Horizontal real estate is highly constrained on mobile devices. Standard inline navigation items become cluttered or illegible. This pattern solves the spacing issue by hiding secondary navigational items behind a recognizable icon, maintaining a clean header while preserving full navigational capability.
* **Overall Applicability**: This is a foundational web UI pattern. It is applicable to nearly every modern website, including SaaS landing pages, portfolios, blogs, e-commerce stores, and dashboards.
* **Value Addition**: It introduces graceful degradation for smaller screens. By avoiding external heavy libraries (like Bootstrap) for a simple menu toggle, it keeps the DOM lightweight and ensures the developer has total control over the stacking order, hover colors, and transition logic. 
* **Browser Compatibility**: The core Flexbox layout, absolute positioning, and JavaScript class toggling are universally supported in all modern and legacy browsers. (Note: The specific reproduction code below uses CSS Container Queries `@container` instead of `@media` to allow you to easily test the responsive breakpoint by resizing a preview window instead of resizing your entire browser. Container Queries are supported in all modern browsers updated since early 2023).

## 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Semantic `<nav>` container for accessibility, wrapping the brand text, the toggle button, and an unordered list `<ul>` of anchor `<a>` tags.
  - **Typography**: Clean sans-serif font (Inter) with distinct hierarchical sizing: `1.5rem` (24px) bold for the Brand Name, and `1rem` (16px) regular for links.
  - **Colors**: Defined by CSS variables. For a dark theme, a deep gray-blue background `#161b22`, offset by lighter text `#e6edf3` and an accent hover background `#00bfff`.
  - **Hamburger Icon**: Constructed purely with CSS. Three `span` elements, each `30px` wide and `3px` tall, flex-spaced inside a `21px` tall absolute container.

* **Step B: Layout & Compositional Style**
  - **Desktop (Default)**: `.navbar` uses `display: flex; justify-content: space-between; align-items: center;`. This anchors the brand name to the far left and the navigation list to the far right.
  - **Mobile (Collapsed)**: Below 600px, `.navbar` switches to `flex-direction: column` and `align-items: flex-start`. The `.toggle-button` becomes visible. The `.navbar-links` are hidden (`display: none`).
  - **Mobile (Expanded)**: When toggled, the `.navbar-links` gain `display: flex; flex-direction: column; width: 100%;`. Because `.navbar` is now a column, the links naturally stack beneath the brand title, pushing the rest of the page's document flow down.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Links feature a subtle background color and text color transition (`transition: background-color 0.2s ease, color 0.2s ease;`) to provide tactile feedback to mouse users.
  - **Click Interactions**: JavaScript listens for the `click` event on the hamburger button. It calls `classList.toggle('active')` on the links container to alternate between `display: none` and `display: flex`.

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Layout Switch** | CSS Container Queries | Replicates `@media` queries but allows the effect to trigger based on the size of a resizable parent `div`. This makes testing the breakpoint incredibly easy on large desktop monitors. |
| **Component Alignment** | CSS Flexbox | The most robust native CSS feature for handling 1D layouts and space-distribution (space-between) and easy axis-flipping (row to column). |
| **Menu Toggling** | JavaScript `classList` | Pure vanilla JS avoids overhead. Manipulating a class instead of inline styles keeps presentation logic strictly in CSS. |
| **Hamburger Graphic** | Pure CSS Shapes | Using 3 styled `<span>` elements avoids the need for external SVG or font-icon CDNs, ensuring absolute self-containment. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Resize this window horizontally using the bottom-right corner. When the container width drops below 600px, the horizontal navigation links collapse into a vertical hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#007BFF",     # CSS hex color for accent hover state
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Hamburger Navbar pattern.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d1117"
        nav_bg = "#161b22"
        text_color = "#e6edf3"
        surface_color = "rgba(255, 255, 255, 0.15)"
    else:
        bg_color = "#f6f8fa"
        nav_bg = "#ffffff"
        text_color = "#1f2328"
        surface_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Responsive Hamburger Navbar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --accent: {accent_color};
    --border: {surface_color};
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
    padding: 2rem;
}}

/* Resizable sandbox environment to demonstrate responsive behavior */
.preview-window {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow-y: auto;
    overflow-x: hidden;
    resize: horizontal; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    /* Container Query logic allows the navbar to react to this specific div's width */
    container-type: inline-size;
    container-name: navbar-container;
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--text);
    border-bottom: 1px solid var(--border);
    position: relative;
}}

.brand-title {{
    font-size: 1.5rem;
    margin: 1rem;
    font-weight: 600;
    letter-spacing: -0.5px;
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex;
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: var(--text);
    padding: 1.25rem 1.5rem;
    display: block;
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li a:hover {{
    background-color: var(--accent);
    color: #ffffff;
}}

.toggle-button {{
    position: absolute;
    top: 1.15rem; /* Vertically centered relative to the 56px navbar header height */
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    cursor: pointer;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--text);
    border-radius: 10px;
    transition: transform 0.2s ease, opacity 0.2s ease;
}}

.content {{
    padding: 2rem;
    line-height: 1.6;
}}

.content h1 {{
    margin-bottom: 1rem;
    font-size: 2rem;
}}

.content p {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* 
  Using @container instead of @media so it responds dynamically 
  to the user resizing the .preview-window frame 
*/
@container navbar-container (max-width: 600px) {{
    .toggle-button {{
        display: flex;
    }}

    .navbar-links {{
        display: none;
        width: 100%;
    }}

    .navbar {{
        flex-direction: column;
        align-items: flex-start;
    }}

    .navbar-links ul {{
        width: 100%;
        flex-direction: column;
    }}

    .navbar-links li {{
        text-align: center;
        border-top: 1px solid var(--border);
    }}

    .navbar-links li a {{
        padding: 1rem;
    }}

    /* The JS injection class to unhide the menu */
    .navbar-links.active {{
        display: flex;
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-window">
        
        <nav class="navbar" aria-label="Main Navigation">
            <div class="brand-title">{title_text}</div>
            
            <a href="#" class="toggle-button" aria-expanded="false" aria-label="Toggle navigation menu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </a>
            
            <div class="navbar-links">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
        </nav>

        <main class="content">
            <h1>Responsive Layout</h1>
            <p>{body_text}</p>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Hamburger Navbar — Interactive Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (!toggleButton || !navbarLinks) return;

    toggleButton.addEventListener('click', (e) => {{
        e.preventDefault(); // Prevents jumping to the top of the page due to href="#"
        
        // Toggle the visibility class
        navbarLinks.classList.toggle('active');
        
        // Update aria-expanded attribute for screen readers
        const isActive = navbarLinks.classList.contains('active');
        toggleButton.setAttribute('aria-expanded', isActive);
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

## 4. Accessibility & Performance Notes

* **Accessibility Enhancements**: 
  - Standard tutorials often overlook screen readers. The provided JS code dynamically updates the `aria-expanded` attribute on the hamburger toggle button. This ensures a screen reader user receives audio feedback that the menu state has changed.
  - The menu is wrapped in `<nav aria-label="Main Navigation">` to demarcate the landmark region correctly.
* **Performance**: This code is extremely performant. It does not observe window resizing via JavaScript (which causes heavy layout thrashing). Instead, it delegates all layout recalculation directly to the browser's native CSS rendering engine via Flexbox overrides and Container Queries. The DOM operations are strictly limited to string manipulation (`classList.toggle`) executed entirely on a discrete user click event.