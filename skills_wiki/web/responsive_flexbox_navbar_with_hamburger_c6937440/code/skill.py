def create_component(
    output_dir: str,
    title_text: str = "DevSimplified",
    body_text: str = "Resize the browser window to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for brand accent
    width_px: int = 800,               # Set below 768 to force mobile view instantly
    height_px: int = 600,
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
        nav_bg = "#333333"
        nav_text = "#ffffff"
        nav_hover = "#555555"
        body_bg = "#f4f4f9"
        body_text = "#1a1a1a"
    else:
        nav_bg = "#ffffff"
        nav_text = "#333333"
        nav_hover = "#e0e0e0"
        body_bg = "#1a1a2e"
        body_text = "#f0f0f0"

    # === CSS ===
    css = f"""/* Responsive Navbar — generated component */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-hover: {nav_hover};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --body-text: {body_text};
}}

body {{
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--body-bg);
    color: var(--body-text);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Mock browser window constraint for testing purposes */
.mock-browser {{
    width: {width_px}px;
    height: {height_px}px;
    background: #ffffff;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    border-radius: 8px;
    overflow-x: hidden;
    overflow-y: auto;
    position: relative;
    border: 1px solid #ccc;
}}

/* =========================================
   NAVBAR STYLES
   ========================================= */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
}}

.brand-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0.5rem 1rem;
    color: var(--accent);
}}

.navbar-links {{
    height: 100%;
}}

.navbar-links ul {{
    display: flex;
    margin: 0;
    padding: 0;
    list-style: none;
}}

.navbar-links li a {{
    display: block;
    text-decoration: none;
    color: var(--nav-text);
    padding: 1rem;
    transition: background-color 0.2s ease;
}}

.navbar-links li a:hover {{
    background-color: var(--nav-hover);
}}

/* Hamburger Menu Button */
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
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--nav-text);
    border-radius: 10px;
}}

/* Page Content */
.content {{
    padding: 2rem;
    text-align: center;
    color: #333;
}}

/* =========================================
   MEDIA QUERIES (Mobile View)
   ========================================= */
/* Triggering at 768px (standard tablet/mobile breakpoint) */
/* Note: Container Queries (@container) would be better here for the mock-browser, 
   but standard @media is used to perfectly match the tutorial's logic. 
   If width_px < 768, you will see the mobile view immediately. */
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
        padding: 0.75rem 1rem;
    }}

    /* The JS Toggle Class */
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
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Container acts as a mock viewport to demonstrate responsiveness based on requested dimensions -->
    <div class="mock-browser">
        
        <!-- NAVBAR COMPONENT -->
        <nav class="navbar">
            <div class="brand-title">{title_text}</div>
            
            <button class="toggle-button" aria-label="Toggle navigation" aria-expanded="false">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
            
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
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar - Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            // Toggle the CSS class that changes display: none to display: flex
            navbarLinks.classList.toggle('active');
            
            // Accessibility update
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
