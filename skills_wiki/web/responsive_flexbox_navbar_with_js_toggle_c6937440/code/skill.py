def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Resize the window or iframe to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Navbar with Hamburger Menu.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        nav_bg = "#333333"
        nav_hover = "#555555"
        text_color = "#ffffff"
        page_bg = "#1a1a2e"
        page_text = "#f0f0f0"
    else:
        nav_bg = "#ffffff"
        nav_hover = "#f0f0f0"
        text_color = "#333333"
        page_bg = "#f4f4f9"
        page_text = "#333333"

    # === CSS ===
    css = f"""/* Responsive Navbar — generated component */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {page_bg};
    color: {page_text};
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Simulated Window Container for Demonstration */
.container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    background-color: {page_bg};
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
}}

/* Navbar Styles */
.navbar {{
    display: flex;
    position: relative;
    justify-content: space-between;
    align-items: center;
    background-color: {nav_bg};
    color: {text_color};
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}}

.brand-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0.5rem 1rem;
    color: {accent_color};
}}

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
    color: {text_color};
    padding: 1rem;
    font-weight: 500;
    transition: background-color 0.2s ease;
}}

.navbar-links li:hover {{
    background-color: {nav_hover};
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
    background: none;
    border: none;
    padding: 0;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: {text_color};
    border-radius: 10px;
    transition: all 0.3s ease;
}}

/* Page Content Styles */
.content {{
    padding: 2rem;
    text-align: center;
}}

/* Responsive Media Query */
/* Triggers when container is smaller than typical tablet size */
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
        padding: 0.75rem 1rem;
    }}

    /* The class added by JavaScript */
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
    <div class="container">
        <!-- Navigation Component -->
        <nav class="navbar">
            <div class="brand-title">{title_text}</div>
            
            <!-- Accessible Toggle Button -->
            <button class="toggle-button" aria-expanded="false" aria-controls="nav-menu" aria-label="Toggle navigation">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
            
            <div class="navbar-links" id="nav-menu">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
        </nav>
        
        <!-- Demonstration Content -->
        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
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

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            // Toggle the visual display of the menu
            navbarLinks.classList.toggle('active');
            
            // Update ARIA attributes for accessibility
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
