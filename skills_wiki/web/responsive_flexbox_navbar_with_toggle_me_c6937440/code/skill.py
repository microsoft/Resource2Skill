def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Resize the browser window to see the responsive navbar collapse into a hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for hover states/accents
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Navbar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg = "#1f2937"
        nav_text = "#f9fafb"
        page_bg = "#111827"
        page_text = "#d1d5db"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        bar_color = "#f9fafb"
    else:
        nav_bg = "#ffffff"
        nav_text = "#111827"
        page_bg = "#f3f4f6"
        page_text = "#4b5563"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        bar_color = "#111827"

    # === CSS ===
    css = f"""/* Responsive Flexbox Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --page-bg: {page_bg};
    --page-text: {page_text};
    --hover-bg: {hover_bg};
    --accent: {accent_color};
    --bar-color: {bar_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
}}

/* Navbar Container */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

/* Brand Logo/Title */
.brand-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0.5rem 1rem;
    text-decoration: none;
    color: var(--nav-text);
}}

/* Navigation Links */
.navbar-links {{
    height: 100%;
}}

.navbar-links ul {{
    display: flex;
    margin: 0;
    padding: 0;
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    display: block;
    text-decoration: none;
    color: var(--nav-text);
    padding: 1rem 1.5rem;
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li a:hover,
.navbar-links li a:focus {{
    background-color: var(--hover-bg);
    color: var(--accent);
    outline: none;
}}

/* Hamburger Toggle Button */
.toggle-button {{
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 10;
}}

/* Screen reader only text for accessibility */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--bar-color);
    border-radius: 10px;
    transition: all 0.3s ease;
}}

/* Page Content Formatting */
.content {{
    padding: 3rem 2rem;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    line-height: 1.6;
}}

/* --- Responsive Media Query --- */
/* Breakpoint at 600px for mobile layout */
@media (max-width: 600px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start;
    }}

    .toggle-button {{
        display: flex;
    }}

    .navbar-links {{
        display: none;
        width: 100%;
    }}

    .navbar-links ul {{
        width: 100%;
        flex-direction: column;
    }}

    .navbar-links li {{
        text-align: center;
    }}

    .navbar-links li a {{
        padding: 1rem;
        border-top: 1px solid rgba(128,128,128, 0.1);
    }}

    /* JS Toggled Class */
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
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="navbar">
        <a href="#" class="brand-title">{title_text}</a>
        
        <!-- Accessible Button instead of anchor tag -->
        <button class="toggle-button" aria-expanded="false" aria-controls="primary-navigation">
            <span class="sr-only">Menu</span>
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </button>

        <div class="navbar-links" id="primary-navigation">
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>
    </nav>

    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            (If viewing in a large window, drag the edge to make it narrower than 600px)
        </p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            // Toggle the display class on the links container
            navbarLinks.classList.toggle('active');
            
            // Update aria-expanded for screen readers
            const isExpanded = navbarLinks.classList.contains('active');
            toggleButton.setAttribute('aria-expanded', isExpanded);
        }});
    }}
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
