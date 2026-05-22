def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Resize the browser to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent/hover
    width_px: int = 1000,              # Used here to simulate a container width
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Hamburger Navbar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Allow custom nav links to be passed in, otherwise default to standard ones
    nav_links = kwargs.get("nav_links", ["Home", "About", "Services", "Contact"])
    breakpoint_px = kwargs.get("breakpoint_px", 600) # Width at which hamburger appears

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        page_bg = "#121212"
        nav_bg = "#333333"
        nav_text = "#ffffff"
        nav_hover = "#555555"
    else:
        page_bg = "#e0e0e0"
        nav_bg = "#ffffff"
        nav_text = "#333333"
        nav_hover = "#f0f0f0"

    # Overriding hover with accent color if desired
    # For this specific tutorial's aesthetic, we stick to the muted hover, but 
    # we can use the accent color for active/focus states or bottom borders.
    
    # Generate HTML list items
    li_elements = "\n                ".join(
        [f'<li><a href="#">{link}</a></li>' for link in nav_links]
    )

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
    color: {nav_text};
    min-height: 100vh;
}}

.preview-container {{
    max-width: {width_px}px;
    margin: 0 auto;
    background-color: {page_bg};
    min-height: {height_px}px;
    border: 1px solid #ccc; /* Just to visualize the bounds */
    overflow-x: hidden;
}}

/* Navbar Styles */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {nav_bg};
    color: {nav_text};
}}

.brand-title {{
    font-size: 1.5rem;
    margin: 0.5rem;
    font-weight: 600;
}}

.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex;
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: {nav_text};
    padding: 1rem;
    display: block;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.navbar-links li:hover {{
    background-color: {nav_hover};
}}

/* Toggle Button (Hamburger) Styles */
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
    background-color: {nav_text};
    border-radius: 10px;
}}

/* Main Content Area */
.content {{
    padding: 2rem;
    color: {nav_bg}; /* Contrast against page background */
}}
.content h1 {{ margin-top: 0; }}

/* Responsive Breakpoint */
@media (max-width: {breakpoint_px}px) {{
    .navbar {{
        flex-direction: column;
        align-items: flex-start;
        position: relative;
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

    .navbar-links ul li {{
        text-align: center;
    }}

    .navbar-links ul li a {{
        padding: 0.5rem 1rem;
    }}

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
    <title>{title_text} - Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        <!-- Navbar -->
        <nav class="navbar">
            <div class="brand-title">{title_text}</div>
            
            <button class="toggle-button" aria-label="Toggle navigation" aria-expanded="false">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
            
            <div class="navbar-links">
                <ul>
                    {li_elements}
                </ul>
            </div>
        </nav>

        <!-- Page Content -->
        <main class="content">
            <h1>Welcome</h1>
            <p>{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', () => {{
        // Toggle the active class to show/hide the menu
        const isActive = navbarLinks.classList.toggle('active');
        
        // Update ARIA expanded state for accessibility
        toggleButton.setAttribute('aria-expanded', isActive);
    }});
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
