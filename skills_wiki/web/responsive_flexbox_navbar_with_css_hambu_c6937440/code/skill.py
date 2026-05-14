def create_component(
    output_dir: str,
    title_text: str = "DevSimplified",
    body_text: str = "Resize your browser window to see the responsive navbar in action.",
    color_scheme: str = "dark",        
    accent_color: str = "#555555",     
    width_px: int = 1000,
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

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        page_bg = "#121212"
        page_text = "#ffffff"
        nav_bg = "#333333"
        nav_text = "#ffffff"
        nav_hover = accent_color if accent_color else "#555555"
    else:
        page_bg = "#f4f4f9"
        page_text = "#333333"
        nav_bg = "#ffffff"
        nav_text = "#333333"
        nav_hover = accent_color if accent_color else "#e0e0e0"
        
    border_color = "rgba(0,0,0,0.1)" if color_scheme == "light" else "rgba(255,255,255,0.1)"

    # === CSS ===
    css = f"""/* Responsive Flexbox Navbar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-hover: {nav_hover};
    --border-color: {border_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
}}

/* Viewport Container for demonstration purposes */
.viewport-container {{
    max-width: {width_px}px;
    height: {height_px}px;
    margin: 2rem auto;
    background-color: var(--page-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

/* Navbar Core Styles */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    border-bottom: 1px solid var(--border-color);
}}

.brand-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0.5rem 1rem;
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
    text-decoration: none;
    color: var(--nav-text);
    padding: 1rem;
    display: block;
    transition: background-color 0.2s ease;
}}

.navbar-links li:hover {{
    background-color: var(--nav-hover);
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

/* Main Content Area */
.main-content {{
    padding: 2rem;
    text-align: center;
}}

/* Responsive Container Queries (Simulating Media Queries within the component) */
@container (max-width: 600px) {{
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

    /* JS Toggle Class */
    .navbar-links.active {{
        display: flex;
    }}
}}

/* We use a container query so the component works exactly as expected when injected 
   into specific widths, regardless of the user's overall browser window size. */
.viewport-container {{
    container-type: inline-size;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="viewport-container">
        <!-- Navigation Bar -->
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

        <!-- Page Content -->
        <main class="main-content">
            <h1>Welcome to {title_text}</h1>
            <p style="margin-top: 1rem; opacity: 0.8;">{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    // Toggle the 'active' class on click
    toggleButton.addEventListener('click', (e) => {{
        e.preventDefault(); // Prevent jump to top of page
        navbarLinks.classList.toggle('active');
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
