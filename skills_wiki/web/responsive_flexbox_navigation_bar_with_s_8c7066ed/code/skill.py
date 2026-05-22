def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        nav_bg = "#ffffff"       # High contrast nav bar as seen in the tutorial
        nav_text = "#111111"
        text_color = "#f0f0f0"
        accent_contrast = "#111111"
    else:
        bg_color = "#f0f0f0"
        nav_bg = "#111111"
        nav_text = "#ffffff"
        text_color = "#333333"
        accent_contrast = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --accent-contrast: {accent_contrast};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    /* Extra height to demonstrate position: sticky */
    min-height: 200vh; 
}}

/* Navigation Container */
nav {{
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: var(--nav-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

/* Logo */
.logo {{
    display: flex;
    align-items: center;
    padding: 20px 0;
    color: var(--nav-text);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--nav-text);
    border-radius: 4px;
    margin-right: 12px;
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li {{
    margin: 0 5px;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--nav-text);
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    transition: all 0.2s ease-in-out;
    border-radius: 4px;
}}

.nav-links a:hover:not(.nav-cta-button) {{
    background-color: rgba(150, 150, 150, 0.1);
    color: var(--accent);
}}

/* CTA Button specifically styled */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px !important;
    margin-left: 10px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--accent-contrast) !important;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    padding: 10px 0;
}}

.hamburger .bar {{
    width: 30px;
    height: 3px;
    background-color: var(--nav-text);
    margin: 6px 0;
    border-radius: 2px;
    transition: 0.3s;
}}

/* Main Content Area */
.hero-content {{
    padding: 80px 40px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}

.hero-content h1 {{
    font-size: 3rem;
    margin-bottom: 20px;
}}

/* Mobile Responsive Adjustments */
@media (max-width: 768px) {{
    nav {{
        padding: 0 20px;
        flex-wrap: wrap; /* Crucial for pushing links to next row */
    }}

    .hamburger {{
        display: block;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-direction: column;
        flex-basis: 100%; /* Forces the ul to take full width and break line */
        width: 100%;
        padding-bottom: 20px;
    }}

    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
        margin: 5px 0;
    }}

    .nav-links a {{
        display: block;
        padding: 15px;
    }}

    .nav-cta-button {{
        margin-left: 0;
        margin-top: 10px;
        display: inline-block;
        width: max-content;
        margin-left: auto;
        margin-right: auto;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="logo">
            <div class="logo-icon"></div>
            <h3>{title_text}</h3>
        </div>
        
        <div class="hamburger">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        
        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Cases</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#" class="nav-cta-button">Contact</a></li>
        </ul>
    </nav>

    <main class="hero-content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <br><br>
        <p style="opacity: 0.6">Try resizing the window to less than 768px wide to see the hamburger menu appear, and scroll down to observe the sticky header.</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Menu Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {{
        hamburger.addEventListener('click', () => {{
            // Toggle the 'active' class to show/hide the menu on mobile
            navLinks.classList.toggle('active');
            
            // Optional: Animate hamburger into an 'X'
            hamburger.classList.toggle('is-active');
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
