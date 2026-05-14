def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Navigation Bar visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#1a1a1a"
        nav_text = "#f0f0f0"
        body_bg = "#0a0a0a"
        hover_bg = "rgba(255, 255, 255, 0.05)"
    else:
        nav_bg = "#ffffff"
        nav_text = "#111111"
        body_bg = "#222222" # Tutorial used dark body with light nav
        hover_bg = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Flexbox Navigation Bar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --body-bg: {body_bg};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #333; /* Dark outer background for preview contrast */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Container simulating a device screen or browser window */
.preview-window {{
    width: var(--width);
    height: var(--height);
    background: var(--body-bg);
    overflow-y: auto;
    position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border-radius: 8px;
}}

/* === Navigation Styles === */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    min-height: 80px;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    flex-wrap: wrap; /* Allows wrapping on mobile */
}}

.logo {{
    display: flex;
    align-items: center;
}}

.logo h3 {{
    color: var(--nav-text);
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    justify-content: space-around;
    height: 24px;
    width: 30px;
}}

.hamburger .bar {{
    width: 100%;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li {{
    margin-left: 20px;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--nav-text);
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 15px;
    border-radius: 4px;
    transition: all 0.2s ease-in-out;
}}

.nav-links a:hover {{
    background-color: var(--hover-bg);
}}

/* CTA Button Styling */
.nav-links .nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    padding: 10px 24px;
    margin-left: 10px;
}}

.nav-links .nav-cta-button:hover {{
    background-color: var(--accent);
    color: #111; /* Always dark text on neon background for contrast */
}}

/* Dummy content to demonstrate scrolling */
.content {{
    padding: 60px 40px;
    color: #fff;
    min-height: 150vh;
}}

.content h1 {{
    font-size: 48px;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 18px;
    line-height: 1.6;
    opacity: 0.8;
}}

/* === Mobile Responsive Design === */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-direction: column;
        width: 100%;
        padding-bottom: 20px;
    }}

    /* Class added by JavaScript */
    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        margin: 10px 0;
        width: 100%;
        text-align: center;
    }}

    .nav-links a {{
        display: block;
        font-size: 16px;
        padding: 15px;
    }}
    
    .nav-links .nav-cta-button {{
        margin-left: 0;
        display: inline-block;
        margin-top: 10px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-window">
        <nav>
            <div class="logo">
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#cases">Cases</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact" class="nav-cta-button">Contact</a></li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <p style="margin-top: 40px; color: var(--accent);">
                Resize the preview window (or browser) below 768px width to see the mobile hamburger menu in action.
            </p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Flexbox Navigation Bar — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu visibility on mobile
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger bars into an 'X' (Left out to stay true to tutorial's visual, 
        // but can be added via CSS tracking the .active state on the parent)
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
