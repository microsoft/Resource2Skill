def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. This content block allows the container to overflow, demonstrating the sticky positioning of the header.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # Vibrant cyan from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a Responsive Sticky Navigation Bar.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        nav_bg = "#1a1f2e"
        text_color = "#94a3b8"
        nav_text = "#f8fafc"
        surface_color = "#1e293b"
    else:
        bg_color = "#f1f5f9"
        nav_bg = "#ffffff"
        text_color = "#475569"
        nav_text = "#0f172a"
        surface_color = "#e2e8f0"

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Body acts as a presentation backdrop */
body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
}}

/* The container acts as the device screen / browser viewport */
.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    border-radius: 8px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    
    /* Using Container Queries for robust component embedding */
    container-type: inline-size;
    container-name: layout;
}}

/* === Navigation Styles === */
.navbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    height: 80px;
    color: var(--nav-text);
}}

.logo h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    width: 34px;
    height: 34px;
    cursor: pointer;
    background: transparent;
    border: none;
}}

.hamburger .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--nav-text);
    border-radius: 4px;
    transition: all 0.2s ease;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li a {{
    display: block;
    padding: 30px 16px;
    color: var(--nav-text);
    text-decoration: none;
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 500;
    transition: background-color 0.15s ease, color 0.15s ease;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: #111; /* Enforce dark text on bright accent */
}}

/* CTA Button Specific Styling */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    margin-left: 16px;
    padding: 10px 24px !important;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
}}

/* === Content Styles for Scrolling Demo === */
.content {{
    padding: 60px 40px;
    min-height: 150vh; /* Force scrolling */
}}

.content h1 {{
    color: var(--nav-text);
    margin-bottom: 16px;
    font-size: 2.5rem;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 600px;
}}

.scroll-blocks {{
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.block {{
    height: 250px;
    background: var(--surface);
    border-radius: 12px;
}}

/* === Responsive Layout (Container Queries) === */
@container layout (max-width: 768px) {{
    .navbar {{
        flex-wrap: wrap; /* Allows links to drop below */
        padding: 0 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
        padding-bottom: 20px;
    }}

    /* Toggled via JavaScript */
    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links li a {{
        padding: 16px;
        text-align: center;
        font-size: 1rem;
    }}

    .nav-links li a:hover {{
        background-color: var(--surface);
        color: var(--accent);
    }}

    .nav-cta-button {{
        margin: 16px auto 0;
        width: max-content;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <nav class="navbar">
            <div class="logo">
                <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                </svg>
                <h3>{title_text}</h3>
            </div>
            
            <button class="hamburger" aria-label="Toggle Navigation">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </button>
            
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
            
            <div class="scroll-blocks">
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
            </div>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Drawer Toggle
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    let menuOpen = false;

    // Toggle menu state on click
    hamburger.addEventListener('click', () => {{
        menuOpen = !menuOpen;
        navLinks.classList.toggle('active');
        
        // Optional accessibility improvement: update aria-expanded
        hamburger.setAttribute('aria-expanded', menuOpen);
    }});

    // Close menu when clicking a link (improves mobile UX)
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {{
        link.addEventListener('click', () => {{
            if (menuOpen) {{
                navLinks.classList.remove('active');
                menuOpen = false;
                hamburger.setAttribute('aria-expanded', 'false');
            }}
        }});
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
