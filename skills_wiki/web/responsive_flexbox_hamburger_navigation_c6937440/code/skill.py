def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Resize the browser window to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#555555",     # Background color on hover
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Hamburger Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#333333"
        nav_text = "#ffffff"
        page_bg = "#f4f4f4"
        page_text = "#111111"
        hover_bg = accent_color if accent_color else "#555555"
    else:
        nav_bg = "#f8f9fa"
        nav_text = "#333333"
        page_bg = "#ffffff"
        page_text = "#111111"
        hover_bg = accent_color if accent_color else "#e2e6ea"

    # === CSS ===
    css = f"""/* Responsive Navbar Styles */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {page_bg};
    color: {page_text};
    /* Simulating requested dimensions for demonstration context */
    min-width: 320px;
}}

/* Navbar Container */
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
    font-weight: bold;
}}

/* Desktop Links */
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
    transition: background-color 0.2s ease;
}}

.navbar-links li a:hover {{
    background-color: {hover_bg};
}}

/* Mobile Toggle Button (Hidden on Desktop) */
.toggle-button {{
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: {nav_text};
    border-radius: 10px;
}}

/* Responsive Breakpoint */
@media (max-width: 600px) {{
    .toggle-button {{
        display: flex;
    }}

    .navbar-links {{
        display: none;
        width: 100%;
    }}

    .navbar {{
        flex-direction: column;
        align-items: flex-start;
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

    /* Class added via JavaScript */
    .navbar-links.active {{
        display: flex;
    }}
}}

/* Page Content */
.content {{
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="brand-title">{title_text}</div>
        
        <!-- Hamburger Button -->
        <a href="#" class="toggle-button" aria-label="Toggle navigation">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </a>
        
        <!-- Navigation Links -->
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
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navbar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent page jump on '#' link
        navbarLinks.classList.toggle('active');
    });
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
