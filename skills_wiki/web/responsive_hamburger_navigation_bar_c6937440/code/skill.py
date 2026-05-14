import os

def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    link_texts: list = None,
    color_scheme: str = "dark",        # "dark" or "light" for navbar colors
    body_bg_color: str = "#f0f0f0",    # Specific background color for the body
    width_px: int = 1200,              # Not directly used for component width, but for overall view
    height_px: int = 800,              # Not directly used for component height, but for overall view
    breakpoint_px: int = 400,          # Max-width for mobile layout breakpoint
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Navbar visual effect from the tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    if link_texts is None:
        link_texts = ["Home", "About", "Contact"]

    # === Derive navbar specific colors based on color_scheme ===
    if color_scheme == "dark":
        navbar_bg_color = "#333"
        navbar_text_color = "white"
        navbar_hover_bg_color = "#555"
        hamburger_bar_color = "white"
    else: # light scheme
        navbar_bg_color = "#f8f8f8"
        navbar_text_color = "#333"
        navbar_hover_bg_color = "#e0e0e0"
        hamburger_bar_color = "#333"


    # === CSS ===
    css = f"""/* Responsive Navbar — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background-color: {body_bg_color}; /* Consistent body background as seen in video output */
    min-height: 100vh; /* Ensure body takes full viewport height */
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {navbar_bg_color};
    color: {navbar_text_color};
    position: relative; /* For absolute positioning of toggle button */
    /* Padding is handled by children's margins/paddings as per video */
}}

.brand-title {{
    font-size: 1.5rem;
    margin: 0.5rem; /* Pushes content away from navbar edges */
    font-weight: 600;
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex; /* Horizontal links by default on desktop */
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: {navbar_text_color};
    padding: 1rem;
    display: block; /* Make entire padded area clickable */
    white-space: nowrap; /* Prevent links from wrapping */
    font-weight: 400;
}}

.navbar-links li a:hover {{
    background-color: {navbar_hover_bg_color};
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
    text-decoration: none; /* Anchor tag default underline */
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: {hamburger_bar_color};
    border-radius: 10px;
}}

/* Media Query for responsiveness */
@media (max-width: {breakpoint_px}px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start; /* Align children to the left */
        padding: 0; /* Reset global padding from larger screens if any */
    }}

    .toggle-button {{
        display: flex; /* Show hamburger button on mobile */
    }}

    .navbar-links {{
        display: none; /* Hide links by default on mobile */
        width: 100%;
    }}

    .navbar-links.active {{
        display: flex; /* Show links when active */
    }}

    .navbar-links ul {{
        width: 100%;
        flex-direction: column; /* Stack links vertically */
    }}

    .navbar-links li a {{
        text-align: center;
        padding: 0.5rem 1rem; /* Adjust padding for mobile layout */
    }}
}}
"""

    # Generate list items for HTML
    list_items_html = "\n".join([f'            <li><a href="#">{link}</a></li>' for link in link_texts])

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="brand-title">{title_text}</div>
        <a href="#" class="toggle-button" aria-expanded="false" aria-controls="navbarLinks">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </a>
        <div class="navbar-links" id="navbarLinks">
            <ul>
{list_items_html}
            </ul>
        </div>
    </nav>
    <script src="script.js" defer></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navbar — interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    if (toggleButton && navbarLinks) {
        toggleButton.addEventListener('click', () => {
            navbarLinks.classList.toggle('active');
            // Toggle aria-expanded attribute for accessibility
            const isExpanded = toggleButton.getAttribute('aria-expanded') === 'true';
            toggleButton.setAttribute('aria-expanded', !isExpanded);
        });
    }
});
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
