def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "This is a responsive navbar. Resize the browser window to see the hamburger menu appear.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent/hover
    width_px: int = 1200,              # Component demo wrapper width
    height_px: int = 600,              # Component demo wrapper height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Navbar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#333333"
        nav_text = "#ffffff"
        hover_bg = "#555555"
        body_bg = "#1a1a1a"
        body_text_color = "#cccccc"
    else:
        nav_bg = "#f4f4f4"
        nav_text = "#333333"
        hover_bg = "#e0e0e0"
        body_bg = "#ffffff"
        body_text_color = "#333333"

    # === CSS ===
    css = f"""/* Responsive Navbar Generated Component */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --hover-bg: {hover_bg};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --body-text: {body_text_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--body-text);
    /* For demo constraints */
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding-top: 2rem;
}}

.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    border: 1px solid var(--hover-bg);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    background-color: var(--body-bg);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* Navbar Core */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    color: var(--nav-text);
}}

.brand-title {{
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0.5rem 1rem;
}}

/* Navbar Links Desktop */
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
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li a:hover,
.navbar-links li a:focus {{
    background-color: var(--hover-bg);
    color: var(--accent);
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
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--nav-text);
    border-radius: 10px;
    transition: background-color 0.2s ease;
}}

.toggle-button:hover .bar,
.toggle-button:focus .bar {{
    background-color: var(--accent);
}}

/* Main Content Area */
.content {{
    padding: 2rem;
    text-align: center;
}}

/* Responsive Breakpoint */
/* Using 600px instead of 400px for a more realistic modern mobile breakpoint */
@container demo-container (max-width: 600px) {{
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
        padding: 0.5rem 1rem;
    }}

    /* The JS triggered class */
    .navbar-links.active {{
        display: flex;
    }}
}}

/* Fallback Media Query if container queries aren't supported (or testing full window) */
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
        padding: 0.5rem 1rem;
    }}
    .navbar-links.active {{
        display: flex;
    }}
}}
"""

    # === HTML ===
    # I wrap it in a demo-wrapper with container-type so the responsive behavior 
    # can be tested without resizing the whole OS window if embedded.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <style>
        /* Define container for inner responsiveness demonstration */
        .demo-wrapper {{
            container-type: inline-size;
            container-name: demo-container;
        }}
    </style>
</head>
<body>

    <div class="demo-wrapper">
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
    js = f"""// Responsive Navbar Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            // Toggle the menu visibility
            navbarLinks.classList.toggle('active');
            
            // Update aria attribute for accessibility
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
