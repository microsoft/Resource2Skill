def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Resize the browser window to see the navbar collapse into a hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for hover states
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

    # === Derive theme colors ===
    if color_scheme == "dark":
        page_bg = "#121212"
        page_text = "#e0e0e0"
        nav_bg = "#333333"
        nav_text = "#ffffff"
        nav_hover = accent_color
    else:
        page_bg = "#f0f0f0"
        page_text = "#333333"
        nav_bg = "#ffffff"
        nav_text = "#333333"
        nav_hover = accent_color

    # === CSS ===
    css = f"""/* Responsive Flexbox Navbar */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-hover: {nav_hover};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
}}

/* Navbar Container */
.navbar {{
    display: flex;
    position: relative;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
}}

/* Brand/Title Area */
.brand-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0.5rem 1rem;
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
    padding: 1rem;
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li:hover a {{
    background-color: var(--nav-hover);
    color: #fff;
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
    cursor: pointer;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--nav-text);
    border-radius: 10px;
}}

/* Main Content Area (For demonstration) */
.content {{
    padding: 2rem;
    max-width: {width_px}px;
    margin: 0 auto;
    text-align: center;
}}

/* Responsive Breakpoint */
@media (max-width: 768px) {{
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

    .navbar-links ul li {{
        text-align: center;
    }}

    .navbar-links ul li a {{
        padding: .5rem 1rem;
    }}

    /* The class added by JavaScript to show the menu */
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
    <title>{title_text} - Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="brand-title">{title_text}</div>
        <a href="#" class="toggle-button">
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

    <div class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Flexbox Navbar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', (e) => {{
            e.preventDefault(); // Prevents the anchor tag from scrolling to top
            navbarLinks.classList.toggle('active');
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
