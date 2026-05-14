import os

def create_component(
    output_dir: str,
    title_text: str = "Flexbox Navbar Variations",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#38bdf8",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    layout_type: int = 1, # 1, 2, 3, 4, 5 as per video variations
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Navbar Layouts visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_main_color = "#0f172a"
        text_white = "#ffffff"
        text_light_gray = "#e2e8f0"
        nav_bg_rgba = "rgba(255, 255, 255, 0.05)"
        border_rgba = "rgba(255, 255, 255, 0.1)"
        btn_text_color = "#0f172a" # dark blue for button text
    else: # Light scheme
        bg_main_color = "#f8f9fa"
        text_white = "#1a1a2e" # Dark text
        text_light_gray = "#555555"
        nav_bg_rgba = "rgba(0, 0, 0, 0.05)"
        border_rgba = "rgba(0, 0, 0, 0.1)"
        btn_text_color = "#ffffff" # White text for button

    # Specific hover accent color for button, as per video
    hover_accent_color = kwargs.get('hover_accent_color', '#00a9f3')

    # === HTML Structure and CSS overrides based on layout_type ===
    nav_content_html = ""
    nav_class_css = ""
    logo_css_override = ""
    nav_links_css_override = ""

    if layout_type == 1:
        # Layout 1: Logo Left, Nav Links Center, Button Right
        nav_content_html = f"""
            <div class="logo">CS Snippets</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        """
        nav_class_css = """
            display: flex;
            align-items: center;
            justify-content: space-between;
        """

    elif layout_type == 2:
        # Layout 2: Logo Left, Nav Links & Button Right
        nav_content_html = f"""
            <div class="logo">CS Snippets</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        """
        nav_class_css = """
            display: flex;
            align-items: center;
            justify-content: flex-end; /* Pushes everything to the right */
        """
        logo_css_override = """
            margin-right: auto; /* Pushes logo to the left, rest to the right */
        """
        nav_links_css_override = """
            margin-right: 30px; /* Space between links and button */
        """

    elif layout_type == 3:
        # Layout 3: Logo & Nav Links Left, Button Right
        nav_content_html = f"""
            <div class="nav-group">
                <div class="logo">CS Snippets</div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </div>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        """
        nav_class_css = """
            display: flex;
            align-items: center;
            justify-content: space-between;
        """
        # Additional CSS for .nav-group
        nav_group_css = """
            .nav-group {
                display: flex;
                align-items: center;
                gap: 2rem;
            }
        """
        # Add nav_group_css to the main css string later

    elif layout_type == 4:
        # Layout 4: Nav Links Left, Logo Center, Button Right
        nav_content_html = f"""
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="logo">CS Snippets</div>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        """
        nav_class_css = """
            display: flex;
            align-items: center;
            justify-content: space-between;
        """
        logo_css_override = """
            margin-right: 15rem; /* Pushes logo right, relative to nav-links */
        """

    elif layout_type == 5:
        # Layout 5: Nav Links Split, Logo Center, No Button
        nav_content_html = f"""
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">CS Snippets</div>
            <ul class="nav-links">
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
        """
        nav_class_css = """
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3rem; /* Gap between the three main items: links1, logo, links2 */
        """
        # Ensure logo_css_override is empty if it was set in a previous layout.
        logo_css_override = ""

    else:
        raise ValueError("Invalid layout_type. Choose 1, 2, 3, 4, or 5.")

    # === CSS ===
    css = f"""/* Flexbox Navbar Layouts — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: {bg_main_color};
    color: {text_white};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Aligns content to top initially */
    width: 100vw; /* Ensure body takes full viewport width */
    overflow-x: hidden; /* Prevent horizontal scroll */
}}

h2 {{
    text-align: center;
    padding: 2rem;
    color: {text_white}; /* Ensure h2 color matches body text */
}}

/* Navbar Container */
nav {{
    width: 100%;
    padding: 1rem 5%;
    background: {nav_bg_rgba};
    border-bottom: 1px solid {border_rgba};
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px); /* For Safari support */
    margin-bottom: 2rem;
    {nav_class_css}
}}

/* Logo */
.logo {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {accent_color};
    letter-spacing: 1px;
    {logo_css_override}
}}

/* Navigation Links */
.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
    {nav_links_css_override}
}}

.nav-links li a {{
    position: relative;
    font-size: 1.05rem;
    font-weight: 500;
    text-decoration: none;
    color: {text_light_gray};
    transition: 0.3s;
}}

.nav-links li a:hover {{
    color: {accent_color};
    text-shadow: 0 0 10px {accent_color};
}}

/* Buttons Container */
.btns {{
    display: flex;
}}

/* Button */
.btn {{
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    background: {accent_color};
    color: {btn_text_color};
    box-shadow: 0 0 15px {accent_color};
    border: none;
    cursor: pointer;
    transition: 0.3s;
}}

.btn:hover {{
    background: {hover_accent_color};
    box-shadow: 0 0 25px {hover_accent_color};
}}

"""
    # Add nav_group_css if layout_type is 3
    if layout_type == 3:
        css += nav_group_css


    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h2>Flexbox Navbar Variations</h2>
    <nav>
        {nav_content_html}
    </nav>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (empty as per tutorial) ===
    js = f"""// Flexbox Navbar Layouts — interactive behavior (no JavaScript required for these layouts)
document.addEventListener('DOMContentLoaded', () => {{
    // No specific JavaScript interactions are demonstrated for these static layouts.
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

