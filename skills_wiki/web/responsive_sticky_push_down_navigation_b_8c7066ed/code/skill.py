def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation effect in action. Notice how the menu remains at the top of the viewport. Resize the window below 768px to see the flex-wrap mobile menu approach.",
    color_scheme: str = "light",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Push-Down Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors (Matching the high-contrast aesthetic of the tutorial)
    if color_scheme == "dark":
        body_bg = "#121212"
        body_text = "#e0e0e0"
        nav_bg = "#1f1f1f"
        nav_text = "#ffffff"
    else:
        body_bg = "#222222"      # Tutorial uses a dark body even for default
        body_text = "#ffffff"
        nav_bg = "#ffffff"       # White nav bar
        nav_text = "#111111"

    # === CSS ===
    css = f"""/* Responsive Sticky Push-Down Navigation Bar */
:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --body-text: {body_text};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--body-text);
    /* Extra height to demonstrate sticky scrolling */
    min-height: 200vh; 
    overflow-x: hidden;
}}

/* Navbar Container */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap; /* Crucial for mobile menu wrapping */
    background-color: var(--nav-bg);
    color: var(--nav-text);
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}}

/* Logo Section */
.logo {{
    display: flex;
    align-items: center;
    height: 70px;
    padding-left: 20px;
}}

.logo svg {{
    margin-right: 10px;
    color: var(--nav-text);
}}

.logo h3 {{
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 20px;
    font-weight: 700;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    justify-content: space-between;
    width: 34px;
    height: 24px;
    margin-right: 20px;
}}

.hamburger .bar {{
    width: 100%;
    height: 4px;
    background-color: var(--nav-text);
    border-radius: 2px;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    margin: 0;
}}

.nav-links li a {{
    display: block;
    padding: 25px 16px;
    color: var(--nav-text);
    text-decoration: none;
    font-size: 16px;
    font-weight: 500;
    text-transform: uppercase;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
}}

/* Call To Action Button */
.nav-cta-button {{
    margin: 0 20px 0 10px;
    padding: 10px 20px !important;
    border: 2px solid var(--accent);
    border-radius: 50px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--nav-text);
}}

/* Main Content Area */
.content {{
    padding: 60px 20px;
    max-width: {width_px}px;
    margin: 0 auto;
    line-height: 1.6;
}}

.content h1 {{
    margin-bottom: 20px;
    font-size: 2.5rem;
}}

.content p {{
    font-size: 1.1rem;
    color: #a0a0a0;
}}

/* --- Responsive Breakpoint --- */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex; /* Show hamburger */
    }}

    .nav-links {{
        display: none; /* Hide horizontal menu */
        flex-basis: 100%; /* Force menu onto a new line below the logo/hamburger */
        flex-direction: column;
        width: 100%;
    }}

    /* Toggled via JavaScript */
    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-links li a {{
        padding: 15px 0;
    }}

    .nav-cta-button {{
        margin: 15px auto 25px auto;
        display: inline-block;
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
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="navbar">
        <div class="logo">
            <!-- Example generic shape to represent the logo -->
            <svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
            </svg>
            <h3>{title_text}</h3>
        </div>
        
        <div class="hamburger" aria-label="Toggle Navigation">
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
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Push-Down Navigation Bar
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle mobile menu
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
    }});

    // Ensure menu resets properly if window is resized past the mobile breakpoint
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.classList.remove('active');
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
