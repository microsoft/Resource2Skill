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
