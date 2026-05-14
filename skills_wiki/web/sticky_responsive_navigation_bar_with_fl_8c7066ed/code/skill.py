def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent (teal)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation Bar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        body_bg = "#0d111c"
        nav_bg = "#1a1f33"
        text_color = "#f0f0f0"
        text_muted = "#a0aabf"
        hamburger_color = "#ffffff"
    else:
        body_bg = "#f0f2f5"
        nav_bg = "#ffffff"
        text_color = "#111111"
        text_muted = "#555555"
        hamburger_color = "#111111"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar - Generated Component */
/* Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --hamburger: {hamburger_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--text);
    min-height: 200vh; /* Forced height to demonstrate sticky behavior */
    overflow-x: hidden;
}}

/* Navigation Bar Base */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    padding: 0 40px;
    min-height: 80px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}}

/* Logo Section */
.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, var(--accent), #a2ff00);
    border-radius: 8px;
}}

.logo h3 {{
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.5px;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    gap: 32px;
}}

.nav-links li a {{
    text-decoration: none;
    color: var(--text);
    font-size: 16px;
    font-weight: 500;
    text-transform: uppercase;
    transition: color 0.2s ease-in-out;
}}

.nav-links li a:hover {{
    color: var(--accent);
}}

/* Call to Action Button */
.nav-cta-button {{
    padding: 10px 24px;
    border: 2px solid var(--accent);
    border-radius: 50px;
    background-color: transparent;
    transition: all 0.3s ease-in-out !important;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: #111 !important; /* Force dark text on accent background for contrast */
}}

/* Hamburger Menu (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    gap: 5px;
}}

.hamburger .bar {{
    width: 30px;
    height: 3px;
    background-color: var(--hamburger);
    border-radius: 3px;
    transition: all 0.3s ease;
}}

/* Main Content Area */
main {{
    max-width: var(--width);
    margin: 100px auto;
    padding: 0 40px;
}}

h1.page-title {{
    font-size: 48px;
    margin-bottom: 20px;
}}

p.page-content {{
    font-size: 18px;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 600px;
}}

/* Responsive Design - Mobile */
@media (max-width: 768px) {{
    nav {{
        padding: 20px;
        flex-wrap: wrap; /* Crucial for dropping links to the next line */
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Toggled via JS */
        flex-direction: column;
        flex-basis: 100%; /* Forces links to span full width below logo */
        width: 100%;
        padding-top: 20px;
        gap: 20px;
    }}

    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-links li a {{
        display: block;
        padding: 10px 0;
        font-size: 18px;
    }}
    
    .nav-cta-button {{
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
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#contact" class="nav-cta-button">Contact</a></li>
        </ul>
    </nav>

    <main id="home">
        <h1 class="page-title">Welcome to {title_text}</h1>
        <p class="page-content">{body_text} Shrink the browser window width below 768px to see the hamburger menu appear and flex-wrap layout kick in.</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    let menuOpen = false;

    // Toggle menu visibility
    hamburger.addEventListener('click', () => {{
        if (!menuOpen) {{
            // Using inline styling to mirror transcript's explicit block/none instructions
            navLinks.style.display = 'flex'; 
            menuOpen = true;
        }} else {{
            navLinks.style.display = 'none';
            menuOpen = false;
        }}
    }});

    // Handle window resize cleanly
    // If user resizes back to desktop, ensure menu becomes visible again
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.style.display = 'flex';
            menuOpen = false; // Reset state for mobile
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
