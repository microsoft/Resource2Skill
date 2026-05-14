def create_component(
    output_dir: str,
    title_text: str = "Responsive Navbar",
    body_text: str = "", # In this tutorial, body_text is effectively the background image
    color_scheme: str = "light", # "dark" or "light"
    accent_color: str = "#000000", # Default black for icons/text as per video
    width_px: int = 1200, # This defines the initial viewport width for testing, component is responsive
    height_px: int = 800, # This defines the initial viewport height for testing, component is responsive
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar with Sliding Sidebar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # --- Theme colors ---
    if color_scheme == "dark":
        nav_bg_color = "#333333" # Darker nav for contrast
        text_color = "#f0f0f0"
        sidebar_bg_color_rgba = "rgba(0, 0, 0, 0.4)" # Darker translucent
        hover_color = "#444444"
    else: # light (as per video)
        nav_bg_color = "#ffffff"
        text_color = "#000000"
        sidebar_bg_color_rgba = "rgba(255, 255, 255, 0.2)" # Lighter translucent
        hover_color = "#f0f0f0"
    
    # Background image URL (from video tutorial description)
    background_image_url = "https://raw.githubusercontent.com/Coding2GO/responsive-navbar/main/laptop.jpg"

    # --- CSS ---
    css = f"""/* Responsive Glassmorphism Navbar with Sliding Sidebar — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    min-height: 100vh;
    font-family: 'Segoe UI', 'Inter', system-ui, -apple-system, sans-serif;
    background-image: url('{background_image_url}');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}}

/* Main Navigation Bar */
nav {{
    background-color: {nav_bg_color};
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.1);
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
}}

nav ul {{
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    padding: 0 15px; /* Added padding to nav ul as seen in video */
}}

nav li {{
    height: 50px;
}}

/* Logo link */
nav li:first-child {{
    margin-right: auto; /* Pushes logo to the left */
}}

nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: {text_color};
    font-weight: 600;
}}

nav a:hover {{
    background-color: {hover_color};
}}

/* Sidebar specific styles */
.sidebar {{
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 250px;
    z-index: 999; /* Below main nav but above content */
    background-color: {sidebar_bg_color_rgba};
    backdrop-filter: blur(10px);
    box-shadow: -10px 0 10px rgba(0, 0, 0, 0.1);
    display: none; /* Hidden by default */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}}

.sidebar li {{
    width: 100%;
    height: 50px; /* Matching main nav link height */
}}

.sidebar a {{
    width: 100%;
    padding: 0 30px; /* Matching main nav link padding */
    text-decoration: none;
    display: flex;
    align-items: center;
    color: {text_color};
    font-weight: 600;
}}

.sidebar li:first-child {{
    margin-left: auto; /* Pushes close icon to the right within sidebar header area */
}}

/* Responsive behavior */

/* Hide desktop links and show menu button on screens smaller than 800px */
@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block; /* Show hamburger button */
    }}
}}

/* Make sidebar full width on screens smaller than 400px */
@media (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

    # --- HTML ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="#">{title_text}</a></li> {/* This will display "Coding2go" or whatever title_text is */}
            <li class="hideOnMobile"><a href="#">Blog</a></li>
            <li class="hideOnMobile"><a href="#">Products</a></li>
            <li class="hideOnMobile"><a href="#">About</a></li>
            <li class="hideOnMobile"><a href="#">Forum</a></li>
            <li class="hideOnMobile"><a href="#">Login</a></li>
            <li class="menu-button" onclick="showSidebar()">
                <a href="#">
                    <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="{accent_color}"><path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/></svg>
                </a>
            </li>
        </ul>
    </nav>

    <ul class="sidebar">
        <li onclick="hideSidebar()">
            <a href="#">
                <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="{accent_color}"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>
            </a>
        </li>
        <li><a href="#">Blog</a></li>
        <li><a href="#">Products</a></li>
        <li><a href="#">About</a></li>
        <li><a href="#">Forum</a></li>
        <li><a href="#">Login</a></li>
    </ul>

    <script src="script.js"></script>
</body>
</html>"""

    # --- JavaScript ---
    js = f"""// Responsive Glassmorphism Navbar with Sliding Sidebar — interactive behavior
function showSidebar() {{
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {{
        sidebar.style.display = 'flex';
    }}
}}

function hideSidebar() {{
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {{
        sidebar.style.display = 'none';
    }}
}}
"""

    # --- Write files ---
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

