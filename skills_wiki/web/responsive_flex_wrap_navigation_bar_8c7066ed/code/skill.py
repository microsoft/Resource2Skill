def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. Resize the window below 768px to interact with the mobile hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flex-Wrap Navigation Bar.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        page_bg = "#121212"
        nav_bg = "#1e1e1e"
        nav_text = "#ffffff"
        border_color = "rgba(255, 255, 255, 0.1)"
        hover_bg = "rgba(255, 255, 255, 0.05)"
    else:
        page_bg = "#f4f4f9"
        nav_bg = "#ffffff"
        nav_text = "#111111"
        border_color = "rgba(0, 0, 0, 0.1)"
        hover_bg = "rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* Responsive Flex-Wrap Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --border: {border_color};
    --hover: {hover_bg};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--nav-text);
    min-height: 200vh; /* Forced height to demonstrate sticky scrolling */
}}

/* Navigation Container */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    flex-wrap: wrap; /* CRITICAL for mobile push-down */
    justify-content: space-between;
    align-items: center;
    padding: 16px 32px;
    background-color: var(--nav-bg);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    z-index: 1000;
    border-bottom: 1px solid var(--border);
}}

/* Logo Section */
.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}}

.logo svg {{
    color: var(--accent);
}}

.logo h3 {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

/* Hamburger Icon */
.hamburger {{
    display: none;
    flex-direction: column;
    gap: 6px;
    cursor: pointer;
    padding: 8px;
}}

.hamburger .bar {{
    width: 28px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 3px;
    transition: all 0.3s ease;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    gap: 8px;
}}

.nav-links li a {{
    text-decoration: none;
    color: var(--nav-text);
    font-size: 15px;
    font-weight: 500;
    padding: 10px 16px;
    border-radius: 6px;
    transition: all 0.2s ease;
}}

.nav-links li a:hover {{
    background-color: var(--hover);
    color: var(--accent);
}}

/* CTA Button Specific Styles */
.nav-links li a.nav-cta-button {{
    border: 2px solid var(--accent);
    color: var(--accent);
    margin-left: 12px;
    padding: 8px 20px;
    border-radius: 50px;
}}

.nav-links li a.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--page-bg) !important;
}}

/* Main Content Area */
main.content {{
    max-width: {width_px}px;
    margin: 60px auto;
    padding: 0 32px;
    line-height: 1.6;
}}

main.content h1 {{
    font-size: 3rem;
    margin-bottom: 16px;
}}

main.content p {{
    font-size: 1.125rem;
    opacity: 0.8;
}}

/* === Responsive Mobile Design === */
@media (max-width: 768px) {{
    nav {{
        padding: 16px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%; /* Pushes to a new row because nav has flex-wrap: wrap */
        flex-direction: column;
        align-items: stretch;
        margin-top: 16px;
        gap: 0;
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links li a {{
        display: block;
        text-align: center;
        padding: 16px;
        border-radius: 0;
        border-top: 1px solid var(--border);
    }}

    .nav-links li a.nav-cta-button {{
        margin: 16px 0 0 0;
        border-radius: 6px;
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
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
                <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            <h3>{title_text}</h3>
        </div>
        
        <div class="hamburger" id="hamburger-menu">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>

        <ul class="nav-links" id="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li><a class="nav-cta-button" href="#contact">Contact</a></li>
        </ul>
    </nav>

    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.getElementById('hamburger-menu');
    const navLinks = document.getElementById('nav-links');
    let menuOpen = false;

    // Toggle menu visibility on hamburger click
    hamburger.addEventListener('click', () => {{
        menuOpen = !menuOpen;
        if (menuOpen) {{
            navLinks.style.display = 'flex';
        }} else {{
            navLinks.style.display = 'none';
        }}
    }});

    // Reset styles on window resize to prevent layout breaking
    // if users scale from mobile back to desktop while menu is closed
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.style.display = 'flex';
            menuOpen = false;
        }} else if (!menuOpen) {{
            navLinks.style.display = 'none';
        }}
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
