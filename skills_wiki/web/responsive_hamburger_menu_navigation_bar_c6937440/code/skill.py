def create_component(
    output_dir: str,
    brand_name: str = "Brand Name",
    links: list = None,
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00bfff",  # Not directly used as per tutorial, but kept for consistency
    width_px: int = 1200,
    height_px: int = 800,  # Note: Height here refers to the overall container, not fixed navbar height.
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Hamburger Menu Navigation Bar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if links is None:
        links = ["Home", "About", "Contact"]

    # === Derive theme colors from color_scheme ===
    # The tutorial uses fixed colors, not strictly a scheme, but adapting the structure.
    navbar_bg_color = "#333333"
    text_color = "#ffffff"
    link_hover_bg = "#555555"

    # === CSS ===
    css = f"""/* Responsive Hamburger Menu Navigation Bar — generated component */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif; /* Adjusted to common sans-serif */
    background-color: #f0f0f0; /* Default background for content area */
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {navbar_bg_color};
    color: {text_color};
}}

.brand-title {{
    font-size: 1.5rem;
    margin: .5rem;
}}

.navbar-links {{
    height: 100%;
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex; /* Horizontal display for desktop */
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: {text_color};
    padding: 1rem;
    display: block; /* Make links block for padding */
}}

.navbar-links li:hover {{
    background-color: {link_hover_bg};
}}

.toggle-button {{
    position: absolute;
    top: .75rem;
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
    background-color: {text_color};
    border-radius: 10px;
}}

/* === Media Query for Mobile (max-width: 400px from tutorial) === */
@media (max-width: 400px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start; /* Align brand name to left */
    }}

    .toggle-button {{
        display: flex; /* Show hamburger button on mobile */
    }}

    .navbar-links {{
        display: none; /* Hide navigation links by default on mobile */
        width: 100%; /* Take full width when displayed */
    }}

    .navbar-links ul {{
        flex-direction: column; /* Stack links vertically */
        width: 100%; /* Take full width */
    }}
    
    .navbar-links li a {{
        text-align: center;
        padding: .5rem 1rem;
    }}
    
    /* When 'active' class is added by JS, display the links */
    .navbar-links.active {{
        display: flex;
        flex-direction: column; /* Ensure links stack vertically when active */
    }}
}}
"""

    # === HTML ===
    link_items_html = "\n".join([f'<li><a href="#">{link}</a></li>' for link in links])
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Navbar</title>
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
    js = f"""// Responsive Hamburger Menu Navigation Bar — interactive behavior
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

