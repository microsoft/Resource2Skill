def create_component(
    output_dir: str,
    title_text: str = "CSsnippets",
    links_primary: list = None,
    links_secondary: list = None, # For type-5 split links
    button_text: str = "Login",
    navbar_type: str = "type-1",  # "type-1", "type-2", "type-3", "type-4", "type-5"
    color_scheme: str = "dark",  # Only "dark" is demonstrated in the video
    accent_color: str = "#4ade80", # Vibrant green, as seen in the video's examples
    width_px: int = 1200, # This defines the visual width of the component wrapper
    height_px: int = 800, # This defines the visual height of the component wrapper
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Responsive Navbar Variations visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if links_primary is None:
        links_primary = ["Home", "Services", "Portfolio", "About"]
    if links_secondary is None:
        links_secondary = ["Portfolio", "About"] # Default for type-5

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color_light = "#e2e8f0"
        text_color_dark = "#0f172a"
        navbar_bg_rgba = "rgba(255, 255, 255, 0.05)"
        navbar_border_rgba = "rgba(255, 255, 255, 0.1)"
    else: # Light scheme - not explicitly covered in video, but for parameter flexibility
        bg_color = "#f8f9fa"
        text_color_light = "#1a1a2e"
        text_color_dark = "#f8f9fa"
        navbar_bg_rgba = "rgba(0, 0, 0, 0.05)"
        navbar_border_rgba = "rgba(0, 0, 0, 0.1)"

    # Generate a slightly darker/more intense accent for hover effect
    def darken_color(hex_color, percent):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * (1 - percent)) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

    accent_color_hover = darken_color(accent_color, 0.2)


    # === HTML Structure based on navbar_type ===
    nav_links_html_primary = "\n".join([f'            <li><a href="#">{link}</a></li>' for link in links_primary])
    nav_links_html_secondary = "\n".join([f'            <li><a href="#">{link}</a></li>' for link in links_secondary])

    html_content = ""
    if navbar_type == "type-1":
        html_content = f"""
        <div class="logo">{title_text}</div>
        <ul class="nav-links">
{nav_links_html_primary}
        </ul>
        <div class="btns">
            <button class="btn">{button_text}</button>
        </div>
        """
    elif navbar_type == "type-2":
        html_content = f"""
        <div class="logo">{title_text}</div>
        <ul class="nav-links">
{nav_links_html_primary}
        </ul>
        <div class="btns">
            <button class="btn">{button_text}</button>
        </div>
        """
    elif navbar_type == "type-3":
        html_content = f"""
        <div class="nav-group">
            <div class="logo">{title_text}</div>
            <ul class="nav-links">
{nav_links_html_primary}
            </ul>
        </div>
        <div class="btns">
            <button class="btn">{button_text}</button>
        </div>
        """
    elif navbar_type == "type-4":
        html_content = f"""
        <ul class="nav-links">
{nav_links_html_primary}
        </ul>
        <div class="logo">{title_text}</div>
        <div class="btns">
            <button class="btn">{button_text}</button>
        </div>
        """
    elif navbar_type == "type-5":
        html_content = f"""
        <ul class="nav-links">
{nav_links_html_primary}
        </ul>
        <div class="logo">{title_text}</div>
        <ul class="nav-links">
{nav_links_html_secondary}
        </ul>
        """
    else:
        raise ValueError(f"Unknown navbar_type: {navbar_type}")

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-dark: {bg_color};
    --text-light: {text_color_light};
    --text-dark: {text_color_dark};
    --accent: {accent_color};
    --accent-hover: {accent_color_hover};
    --navbar-bg: {navbar_bg_rgba};
    --navbar-border: {navbar_border_rgba};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-dark);
    color: var(--text-light);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Aligns navbar to the top */
    overflow-x: hidden; /* Prevent horizontal scroll */
    padding: 2rem 0; /* Add some vertical padding around the navbar */
}}

.wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    /* This wrapper is to simulate the overall content area for the navbar to be on */
}}

nav.navbar {{
    width: 100%;
    padding: 1rem 5%;
    background: var(--navbar-bg);
    border-bottom: 1px solid var(--navbar-border);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px); /* For Safari support */
    /* margin-bottom: 2rem; */ /* Removed for cleaner component display */
    display: flex;
    align-items: center;
}}

.logo {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

.nav-links li a {{
    position: relative;
    font-size: 1.05rem;
    font-weight: 500;
    text-decoration: none;
    color: var(--text-light);
    transition: 0.3s;
}}

.nav-links li a:hover {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent);
}}

.btns {{
    display: flex;
}}

.btn {{
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    background: var(--accent);
    color: var(--text-dark);
    box-shadow: 0 0 15px var(--accent);
    border: none;
    cursor: pointer;
    transition: 0.3s;
    outline: none; /* Remove focus outline */
}}

.btn:hover {{
    background: var(--accent-hover);
    box-shadow: 0 0 25px var(--accent-hover);
}}

/* --- Navbar Type Specific Styles --- */

/* Type 1: Logo left, Links center, Button right */
.navbar.type-1 {{
    justify-content: space-between;
}}

/* Type 2: Logo left, Links and Button right */
.navbar.type-2 {{
    justify-content: flex-end;
}}
.navbar.type-2 .logo {{
    margin-right: auto;
}}
.navbar.type-2 .nav-links {{
    margin-right: 30px; /* Space between links and button */
}}

/* Type 3: Logo and Links left (grouped), Button right */
.navbar.type-3 {{
    justify-content: space-between;
}}
.navbar.type-3 .nav-group {{
    display: flex;
    align-items: center;
    gap: 2rem; /* Gap between logo and nav-links */
}}

/* Type 4: Links left, Logo center, Button right */
.navbar.type-4 {{
    justify-content: space-between;
}}
.navbar.type-4 .logo {{
    /* This margin-right helps to visually center the logo in the tutorial video */
    margin-right: 15rem; /* Adjust based on desired visual centering */
}}

/* Type 5: Links left, Logo center, Links right (no button) */
.navbar.type-5 {{
    justify-content: center;
    gap: 3rem; /* Gap between first nav-links, logo, and second nav-links */
}}
.navbar.type-5 .nav-links:first-of-type {{
    margin-right: 0; /* Clear margin from Type 2 if applied */
}}
"""

    # === JavaScript ===
    js = """// No JavaScript is required for the core visual and layout effects.
// This file is included for completeness.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Navbar variations loaded.");
});
"""

    # === Write files ===
    files = []
    # Create an outer wrapper div to contain the navbar if width_px/height_px define the viewport
    # However, the tutorial demonstrates the navbar itself taking 100% width, so the wrapper is less critical.
    # I'll include a wrapper for context and ensure it respects the specified dimensions for the *component display area*.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flexbox Navbar Variations - {navbar_type.replace('-', ' ').title()}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper" style="width: {width_px}px; height: {height_px}px; background-color: {bg_color}; display: flex; justify-content: center; align-items: flex-start;">
        <nav class="navbar {navbar_type}">
            {html_content.strip()}
        </nav>
    </div>
    <script src="script.js"></script>
</body>
</html>"""


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

