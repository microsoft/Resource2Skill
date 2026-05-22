def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. Resize the window below 768px to see the mobile hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent (vibrant cyan/green by default)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Navigation Bar pattern.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        nav_bg = "#222222"
        text_color = "#ffffff"
        nav_text = "#f0f0f0"
        accent_text = "#111111" # Dark text on bright accent background
    else:
        bg_color = "#f4f4f4"
        nav_bg = "#ffffff"
        text_color = "#111111"
        nav_text = "#333333"
        accent_text = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar - Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --accent-text: {accent_text};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 200vh; /* Force scrolling to demonstrate sticky */
}}

/* Preview Container - Constrains width for accurate desktop/mobile testing */
.preview-container {{
    max-width: var(--max-width);
    margin: 0 auto;
    background: var(--bg);
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    min-height: 100vh;
    position: relative;
}}

/* === NAVIGATION BAR STYLES === */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
}}

.logo {{
    display: flex;
    align-items: center;
    height: 70px;
}}

.logo h3 {{
    font-size: 24px;
    font-weight: 700;
    color: var(--nav-text);
    cursor: pointer;
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
}}

.nav-links li a {{
    display: block;
    padding: 0 20px;
    line-height: 70px;
    color: var(--nav-text);
    text-decoration: none;
    text-transform: uppercase;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 150ms ease-in-out;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--accent-text);
}}

/* Special CTA Button */
.nav-cta-button {{
    border: 2px solid var(--accent);
    line-height: 38px !important;
    border-radius: 4px;
    margin-left: 15px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--accent-text) !important;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 34px;
}}

.hamburger .bar {{
    height: 4px;
    width: 100%;
    background-color: var(--nav-text);
    margin: 5px 0;
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Main Content Area */
.content {{
    padding: 60px 20px;
    text-align: center;
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.2rem;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}

/* === RESPONSIVE MOBILE STYLES === */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 0 20px;
    }}
    
    .logo {{
        height: 60px;
    }}

    .hamburger {{
        display: block; /* Show hamburger */
    }}

    .nav-links {{
        display: none; /* Hide links initially */
        flex-basis: 100%; /* Force to new line below logo/hamburger */
        flex-direction: column;
        width: 100%;
        padding-bottom: 15px;
    }}

    /* Class added via JS */
    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links li a {{
        text-align: center;
        line-height: 50px;
        padding: 0;
        border-radius: 4px;
        margin-bottom: 5px;
    }}
    
    .nav-cta-button {{
        margin-left: 0;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        
        <!-- Navigation Bar Component -->
        <nav>
            <div class="logo">
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger" aria-label="Toggle Navigation" role="button" tabindex="0">
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
        
        <!-- Page Content -->
        <div class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <br><br>
            <p style="opacity: 0.5">(Scroll down to see the sticky nav bar)</p>
        </div>
        
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    let menuOpen = false;

    // Toggle menu on hamburger click
    hamburger.addEventListener('click', () => {{
        if (!menuOpen) {{
            // Open menu
            navLinks.style.display = 'flex';
            menuOpen = true;
        }} else {{
            // Close menu
            navLinks.style.display = 'none';
            menuOpen = false;
        }}
    }});

    // Fix display states if window is resized past the mobile breakpoint
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            // Reset to desktop view
            navLinks.style.display = 'flex';
            menuOpen = false; 
        }} else if (!menuOpen) {{
            // Ensure it's hidden on mobile if state is closed
            navLinks.style.display = 'none';
        }}
    }});
    
    // Accessibility: Allow pressing Enter on the hamburger icon
    hamburger.addEventListener('keypress', (e) => {{
        if (e.key === 'Enter') {{
            hamburger.click();
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
