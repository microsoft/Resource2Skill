def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Keep scrolling down to see the sticky navigation bar slide perfectly over the content.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sticky Responsive Flexbox Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on selection
    if color_scheme == "dark":
        bg_color = "#121212"
        nav_bg = "#1e1e1e"
        text_color = "#ffffff"
        nav_text = "#f0f0f0"
        surface_color = "#333333"
    else:
        bg_color = "#f4f4f5"
        nav_bg = "#ffffff"
        text_color = "#18181b"
        nav_text = "#111111"
        surface_color = "#e4e4e7"

    css = f"""/* Sticky Responsive Flexbox Navigation Bar */
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
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer dark area to frame the viewport */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The sandbox viewport mirroring a device screen */
.viewport-container {{
    container-type: inline-size;
    container-name: viewport;
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background: var(--bg);
    overflow-y: auto;
    position: relative;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}}

/* === Navigation Core Styles === */
.navbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    background-color: var(--nav-bg);
    border-bottom: 1px solid var(--surface);
}}

.logo {{
    display: flex;
    align-items: center;
    color: var(--nav-text);
    padding: 16px 0;
}}

.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    gap: 5px;
    padding: 8px;
}}

.hamburger .bar {{
    width: 26px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links a {{
    display: block;
    padding: 24px 16px;
    color: var(--nav-text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all 0.15s ease-in-out;
}}

/* Hover Effects */
.nav-links a:hover {{
    background-color: var(--accent);
    color: #111; /* Enforced dark text on bright accents */
}}

.nav-links .nav-cta-button {{
    margin-left: 16px;
    padding: 10px 24px;
    border: 2px solid var(--accent);
    border-radius: 50px;
    background: transparent;
}}

/* === Mock Page Content === */
.content {{
    padding: 60px 40px;
}}

.content h1 {{
    margin-bottom: 16px;
    font-size: 2.5rem;
}}

.spacer {{
    height: 1200px;
    margin-top: 40px;
    background: repeating-linear-gradient(
      45deg,
      transparent,
      transparent 20px,
      var(--surface) 20px,
      var(--surface) 40px
    );
    opacity: 0.3;
    border-radius: 8px;
}}

/* === Responsive Layout via Container Queries === */
@container viewport (max-width: 768px) {{
    .navbar {{
        flex-wrap: wrap;
        padding: 12px 20px;
    }}
    
    .hamburger {{
        display: flex;
    }}
    
    .nav-links {{
        display: none;
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
        padding-top: 10px;
        padding-bottom: 20px;
    }}
    
    .nav-links li {{
        width: 100%;
    }}
    
    .nav-links a {{
        text-align: center;
        padding: 16px;
        font-size: 16px;
    }}
    
    .cta-item {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}
    
    .nav-links .nav-cta-button {{
        margin-left: 0;
        margin-top: 16px;
    }}
}}

/* Fallback protection to ensure inline 'none' is overridden when resizing back to desktop */
@container viewport (min-width: 769px) {{
    .nav-links {{
        display: flex !important;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Sticky Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-container">
        
        <nav class="navbar">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px;">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                    <polyline points="2 17 12 22 22 17"></polyline>
                    <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger" aria-label="Toggle navigation" aria-expanded="false" role="button" tabindex="0">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li class="cta-item"><a class="nav-cta-button" href="#contact">Contact</a></li>
            </ul>
        </nav>
        
        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <div class="spacer"></div>
            <p>End of page.</p>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Vanilla JavaScript Menu Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // State variable mirroring the tutorial
    let menuOpen = false;

    // Handle click event for the hamburger menu
    hamburger.addEventListener('click', () => {{
        if (menuOpen === false) {{
            navLinks.style.display = 'block';
            menuOpen = true;
            hamburger.setAttribute('aria-expanded', 'true');
        }} else {{
            navLinks.style.display = 'none';
            menuOpen = false;
            hamburger.setAttribute('aria-expanded', 'false');
        }}
    }});

    // Accessibility: Allow keyboard triggering on the hamburger icon
    hamburger.addEventListener('keypress', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            hamburger.click();
        }}
    }});
}});
"""

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
