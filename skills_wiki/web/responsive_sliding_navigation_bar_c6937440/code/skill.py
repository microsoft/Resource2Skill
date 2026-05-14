def create_component(
    output_dir: str,
    brand_name: str = "Brand Name",
    links: list = None,
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00bfff",  # CSS hex color for accent - not directly used in this specific navbar but included for consistency
    width_px: int = 1200,
    height_px: int = 800,
    breakpoint_px: int = 600, # Max-width for mobile layout
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sliding Navigation Bar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if links is None:
        links = ["Home", "About", "Contact"]

    # === Derive theme colors from color_scheme ===
    # For this specific navbar, colors are fixed as per tutorial, accent_color is not used.
    # bg_color = "#0d111c" if color_scheme == "dark" else "#f8f9fa"
    # text_color = "#f0f0f0" if color_scheme == "dark" else "#1a1a2e"
    navbar_bg = "#333333"
    navbar_text = "#ffffff"
    navbar_hover_bg = "#555555"

    # === CSS ===
    css = f"""/* Responsive Sliding Navigation Bar — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: #f0f0f0; /* Neutral background for the page content */
    margin: 0;
    padding: 0;
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {navbar_bg};
    color: {navbar_text};
    height: 60px; /* Fixed height for the navbar */
    padding: 0 1rem;
}}

.brand-title {{
    font-size: 1.5rem;
    margin: 0.5rem;
}}

.navbar-links {{
    display: flex; /* Desktop: links visible, horizontal */
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex; /* Desktop: links are horizontal */
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: {navbar_text};
    padding: 1rem;
    display: block; /* Makes the whole LI clickable */
}}

.navbar-links li a:hover {{
    background-color: {navbar_hover_bg};
}}

.toggle-button {{
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    display: none; /* Hidden by default on desktop */
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    cursor: pointer;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: {navbar_text};
    border-radius: 10px;
}}

/* Mobile Styles */
@media (max-width: {breakpoint_px}px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start;
        padding: 0;
        height: auto; /* Allow height to adjust */
    }}

    .brand-title {{
        margin-left: 1rem; /* Adjust brand title margin for mobile */
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }}

    .navbar-links {{
        width: 100%;
        display: none; /* Hidden by default on mobile */
        flex-direction: column; /* Links stacked vertically */
    }}

    .navbar-links.active {{
        display: flex; /* Display when active */
    }}

    .navbar-links ul {{
        flex-direction: column;
        width: 100%;
    }}

    .navbar-links li {{
        text-align: center;
    }}

    .navbar-links li a {{
        padding: 0.5rem 1rem; /* Adjust padding for mobile links */
    }}

    .toggle-button {{
        display: flex; /* Visible on mobile */
    }}
}}
"""

    # === HTML ===
    link_items_html = "\n".join(
        [f'            <li><a href="#">{link}</a></li>' for link in links]
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand_name} - Responsive Navbar</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="brand-title">{brand_name}</div>
        <a href="#" class="toggle-button">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </a>
        <div class="navbar-links">
            <ul>
{link_items_html}
            </ul>
        </div>
    </nav>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sliding Navigation Bar — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {{
        toggleButton.addEventListener('click', () => {{
            navbarLinks.classList.toggle('active');
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

