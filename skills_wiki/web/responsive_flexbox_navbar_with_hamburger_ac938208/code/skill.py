def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Welcome to our responsive website.",
    color_scheme: str = "dark",        # "dark" or "light" navbar theme
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
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg = "#333333"
        nav_text = "#ffffff"
        nav_hover = accent_color
        body_bg = "#f4f4f4"
        body_text_color = "#333333"
    else:
        nav_bg = "#ffffff"
        nav_text = "#333333"
        nav_hover = accent_color
        body_bg = "#1a1a1a"
        body_text_color = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Flexbox Navbar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-hover: {nav_hover};
    --body-bg: {body_bg};
    --body-text: {body_text_color};
    --preview-width: {width_px}px;
    --preview-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--body-bg);
    color: var(--body-text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Preview Container simulating a device screen */
.device-container {{
    width: 100%;
    max-width: var(--preview-width);
    height: var(--preview-height);
    background: white;
    border: 1px solid #ddd;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}}

/* === NAVBAR CORE STYLES === */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    position: relative;
}}

.brand-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0.5rem 1rem;
    cursor: pointer;
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex;
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: var(--nav-text);
    padding: 1rem;
    display: block;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li:hover {{
    background-color: var(--nav-hover);
}}

/* Make text darker if hover background is very light (simplistic contrast fix) */
.navbar-links li:hover a {{
    color: { '#ffffff' if color_scheme == 'light' else nav_text }; 
}}

/* === HAMBURGER BUTTON === */
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

/* === PAGE CONTENT === */
.hero {{
    padding: 4rem 2rem;
    text-align: center;
    flex-grow: 1;
    background: var(--body-bg);
}}

.hero h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

/* === RESPONSIVE DESIGN (MOBILE) === */
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
    }}

    /* Class added by JavaScript */
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
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Device container is used to restrict max-width to the preview dimensions -->
    <div class="device-container">
        
        <nav class="navbar">
            <div class="brand-title">{safe_title}</div>
            
            <button class="toggle-button" aria-label="Toggle navigation" aria-expanded="false">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
            
            <div class="navbar-links">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
        </nav>

        <main class="hero">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
            <p style="margin-top: 2rem; font-size: 0.9rem; color: gray;">
                (Resize the window or preview container below 600px to see the hamburger menu in action)
            </p>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Flexbox Navbar — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            // Toggle the display of the links
            navbarLinks.classList.toggle('active');
            
            // Update accessibility attribute
            const isExpanded = toggleButton.getAttribute('aria-expanded') === 'true';
            toggleButton.setAttribute('aria-expanded', !isExpanded);
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
