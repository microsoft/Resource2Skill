def create_component(
    output_dir: str,
    title_text: str = "Responsive Navbar",
    logo_text: str = "Coding2go",
    nav_links: list = None,
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent - not heavily used in original, mainly for contrast
    width_px: int = 1200,
    height_px: int = 800,
    background_image_url: str = "https://images.unsplash.com/photo-1549692520-acc6669e2fde?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Responsive Glassmorphism Navigation Bar" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if nav_links is None:
        nav_links = ["Blog", "Products", "About", "Forum", "Login"]

    # --- SVG Icons from Google Material Symbols ---
    # Hamburger menu icon
    menu_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26"><path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/></svg>"""
    # Close icon
    close_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231Z"/></svg>"""

    # --- Generate navigation list items ---
    desktop_nav_items_html = f'<li class="logo-item"><a href="#">{logo_text}</a></li>'
    for link_text in nav_links:
        desktop_nav_items_html += f'<li class="hideOnMobile"><a href="#">{link_text}</a></li>'
    desktop_nav_items_html += f'<li class="menu-button" onclick="showSidebar()"><a href="#">{menu_icon_svg}</a></li>'

    sidebar_nav_items_html = f'<li onclick="hideSidebar()"><a href="#">{close_icon_svg}</a></li>'
    for link_text in nav_links:
        sidebar_nav_items_html += f'<li><a href="#">{link_text}</a></li>'
        
    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg_color = "#333333"
        nav_text_color = "#f0f0f0"
        nav_hover_bg = "#555555"
        sidebar_bg_rgba = "rgba(0, 0, 0, 0.2)"
        box_shadow_color = "rgba(255, 255, 255, 0.1)"
    else: # light (as per video)
        nav_bg_color = "#ffffff"
        nav_text_color = "#000000"
        nav_hover_bg = "#f0f0f0"
        sidebar_bg_rgba = "rgba(255, 255, 255, 0.2)"
        box_shadow_color = "rgba(0, 0, 0, 0.1)" # Used for nav bar
        box_shadow_sidebar_color = "rgba(0, 0, 0, 0.1)" # Used for sidebar (negative x for left shadow)

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navigation Bar — generated component */
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-image: url('{background_image_url}');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}}

nav {{
    background-color: {nav_bg_color};
    box-shadow: 3px 3px 5px {box_shadow_color};
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
}}

nav ul {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}}

nav li {{
    height: 50px;
}}

nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: {nav_text_color};
}}

nav a:hover {{
    background-color: {nav_hover_bg};
}}

nav li:first-child {{
    margin-right: auto; /* Pushes the logo to the left */
}}

/* Sidebar specific styles */
.sidebar {{
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 250px;
    z-index: 999;
    background-color: {sidebar_bg_rgba}; /* Semi-transparent white */
    backdrop-filter: blur(10px); /* Frosted glass effect */
    box-shadow: -10px 0 10px {box_shadow_sidebar_color}; /* Shadow on left side */
    display: none; /* Hidden by default, shown by JS on mobile */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}}

.sidebar li {{
    width: 100%;
    height: 50px; /* Each sidebar item has fixed height */
}}

.sidebar a {{
    width: 100%; /* Links fill the width of sidebar items */
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: {nav_text_color};
}}

.sidebar a:hover {{
    background-color: {nav_hover_bg};
}}

/* Responsive adjustments */
/* Hide desktop navigation links and show menu button on screens <= 800px */
@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block; /* Show hamburger menu icon */
    }}
}}

/* For very small screens, make sidebar full width */
@media (max-width: 400px) {{
    .sidebar {{
        width: 100%;
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
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            {desktop_nav_items_html}
        </ul>
    </nav>
    <ul class="sidebar">
        {sidebar_nav_items_html}
    </ul>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Glassmorphism Navigation Bar — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');

    window.showSidebar = function() {{
        sidebar.style.display = 'flex';
    }};

    window.hideSidebar = function() {{
        sidebar.style.display = 'none';
    }};

    // Ensure sidebar is hidden initially on desktop, or shown/hidden based on media query
    function handleResize() {{
        if (window.innerWidth > 800) {{
            sidebar.style.display = 'none'; // Hide sidebar on larger screens
        }} else if (sidebar.style.display !== 'flex') {{
            // If on mobile size and not already open, ensure it's hidden
            sidebar.style.display = 'none'; 
        }}
    }}

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check on load
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

