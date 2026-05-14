# High-level Design Pattern Extraction

> **Skill Name**: Responsive Sticky Flexbox Navigation Bar

* **Core Visual Mechanism**: A top-aligned navigation bar that remains fixed to the viewport as the user scrolls (`position: sticky`). It utilizes CSS Flexbox for horizontal alignment of the brand logo and navigation links. On mobile viewports (via CSS Media Queries), the layout seamlessly collapses: the horizontal links are hidden, a hamburger icon appears, and JavaScript enables toggling a vertical, full-width menu that pushes down from the header.
* **Why Use This Skill (Rationale)**: Navigation is the anchor of user experience. This pattern solves the problem of fitting multiple navigation items on small screens without cluttering the interface. Using `position: sticky` ensures the menu is always accessible without forcing the user to scroll back to the top, which increases engagement and ease of use.
* **Overall Applicability**: Virtually every modern website requires a responsive navigation bar. This pattern is foundational for SaaS landing pages, portfolios, blogs, and corporate websites.
* **Value Addition**: Compared to basic static links, this pattern provides structural hierarchy, preserves screen real estate on mobile devices, and creates a polished, app-like interaction via the interactive hamburger menu and hover states. 
* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS Grid/Flexbox, `position: sticky`, and vanilla JavaScript DOM manipulation. No external dependencies are required.

# Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Semantic `<nav>` container holding a `.logo` div, a `.hamburger` toggle div (composed of three `.bar` spans), and a `<ul>` for the `.nav-links`.
  - **Color Logic**: High contrast between the navigation bar background and text. A distinct accent color (e.g., `#39ffde`) is used for hover states and call-to-action (CTA) button borders to draw the eye.
  - **Typography**: Clean, sans-serif typography (e.g., 'Inter' or 'Roboto') with uppercase formatting for menu items to establish a clear UI hierarchy.
  - **Key CSS Properties**: `position: sticky`, `top: 0`, `flex-wrap: wrap`, `transition`.

* **Step B: Layout & Compositional Style**
  - **Desktop Layout**: Uses `display: flex; justify-content: space-between; align-items: center;` to push the logo to the far left and the links to the far right.
  - **Mobile Layout**: At `max-width: 768px`, the `.nav-links` are hidden (`display: none`). When active, they switch to `display: flex; flex-direction: column;`, taking up `width: 100%`. The flex container's `flex-wrap: wrap` property allows this 100% width element to naturally fall below the logo and hamburger icon.
  - **Z-Index Layering**: The navigation bar is given a high `z-index` (e.g., `1000`) to ensure it always overlays page content during scrolling.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Links change background color to the accent color, utilizing a smooth `transition: all 0.2s ease-in-out` for a polished feel.
  - **Mobile Toggle**: A vanilla JavaScript click event listener on the hamburger icon toggles an `.active` class on the `.nav-links` container, which overrides the mobile `display: none` with `display: flex`. (Note: Using a class toggle is more robust than the inline `style.display` manipulation shown in the video, as it prevents display bugs when resizing the browser window from mobile back to desktop).

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Sticky Header** | CSS `position: sticky` | Native CSS solution that behaves like `relative` until the scroll threshold is met, then acts like `fixed`. |
| **Responsive Layout** | CSS Flexbox & Media Queries | `justify-content: space-between` perfectly handles the desktop layout, while `flex-wrap` and `flex-direction: column` effortlessly reflow the layout for mobile. |
| **Mobile Menu Toggle** | Vanilla JS (Class Toggle) | Lightweight and performant. Toggling a CSS class (`.active`) cleanly separates logic from styling, avoiding inline style conflicts. |
| **Hamburger Icon** | Pure CSS Shapes | Created using three generic `<div>` elements styled as thin bars. Avoids the need for external SVG or font icon requests. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent hover states
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Flexbox Navigation Bar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#222222"
        nav_bg = "#111111"
        text_color = "#ffffff"
        accent_text = "#111111" # Dark text on bright accent background
    else:
        bg_color = "#f4f4f4"
        nav_bg = "#ffffff"
        text_color = "#111111"
        accent_text = "#111111" 

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation Bar — generated component */
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
    --accent-text: {accent_text};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* Set min-height to allow scrolling to test sticky nav */
    min-height: 200vh; 
    overflow-x: hidden;
}}

/* --- Navigation Container --- */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    flex-wrap: wrap; /* Allows mobile menu to drop below logo */
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    min-height: 70px;
    background-color: var(--nav-bg);
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

/* --- Logo Section --- */
.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}}

.logo h3 {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.5px;
}}

/* --- Hamburger Menu Icon (Hidden on Desktop) --- */
.hamburger {{
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    cursor: pointer;
}}

.hamburger .bar {{
    width: 100%;
    height: 3px;
    background-color: var(--text);
    border-radius: 3px;
    transition: all 0.3s ease;
}}

/* --- Navigation Links --- */
.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
}}

.nav-links li a {{
    text-decoration: none;
    color: var(--text);
    padding: 10px 16px;
    display: block;
    text-transform: uppercase;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
    border-radius: 4px;
}}

/* Hover effect for all links */
.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--accent-text);
}}

/* Special styling for Call-To-Action button */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px !important;
    margin-left: 10px;
}}

/* --- Page Content Placeholder --- */
.content {{
    padding: 60px 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 20px;
    line-height: 1.2;
}}

.content p {{
    font-size: 1.2rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* =========================================
   Mobile Responsiveness
   ========================================= */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex; /* Show hamburger icon */
    }}
    
    .nav-links {{
        display: none; /* Hide horizontal links by default */
        width: 100%; /* Force to full width so flex-wrap pushes it down */
        flex-direction: column;
        padding-top: 15px;
        padding-bottom: 15px;
    }}
    
    /* Class toggled by JavaScript */
    .nav-links.active {{
        display: flex; 
    }}
    
    .nav-links li {{
        width: 100%;
        text-align: center;
    }}
    
    .nav-links li a {{
        padding: 15px;
        border-radius: 0;
    }}
    
    .nav-cta-button {{
        margin-left: 0;
        margin-top: 10px;
        display: inline-block;
        width: auto;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <nav class="navbar">
        <div class="logo">
            <!-- Simple SVG Logo Placeholder -->
            <svg width="28" height="28" viewBox="0 0 24 24" fill="var(--text)">
                <path d="M12 2L2 22h20L12 2zm0 3.8l6.2 12.2H5.8L12 5.8z"/>
            </svg>
            <h3>{title_text}</h3>
        </div>
        
        <div class="hamburger">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        
        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact" class="nav-cta-button">Contact</a></li>
        </ul>
    </nav>

    <div class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <p style="margin-top: 40px; font-size: 0.9rem; opacity: 0.5;">
            (Scroll down to observe the sticky navigation effect, and resize the browser below 768px to see the mobile menu toggle.)
        </p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Navigation Bar — interactive behavior

document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle the mobile menu
    // We use classList.toggle instead of inline style.display for better reliability
    // when a user resizes the window back to desktop size while the menu is open.
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
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