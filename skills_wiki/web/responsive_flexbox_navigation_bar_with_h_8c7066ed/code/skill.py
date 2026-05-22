def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. Resize the window to trigger the mobile hamburger menu.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for hover/CTA
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
        body_bg = "#111111"
        nav_bg = "#1a1a1a"
        text_color = "#ffffff"
        hover_text = "#111111" # Dark text on bright accent
    else:
        body_bg = "#f0f2f5"
        nav_bg = "#ffffff"
        text_color = "#111111"
        hover_text = "#111111"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --hover-text: {hover_text};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--text);
    min-height: 200vh; /* Force scrolling to demonstrate sticky nav */
}}

/* Navigation Container */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    flex-wrap: wrap;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
}}

/* Logo Area */
.logo {{
    display: flex;
    align-items: center;
    padding: 15px 0;
}}

.logo svg {{
    width: 40px;
    height: 40px;
}}

.logo h3 {{
    margin-left: 10px;
    color: var(--text);
    text-decoration: none;
    font-size: 24px;
    font-weight: 700;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links a {{
    display: block;
    padding: 25px 16px;
    color: var(--text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all ease-in-out 150ms;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

/* Call to Action Button */
.nav-cta-button {{
    padding: 10px 20px !important;
    margin-left: 16px;
    border: var(--accent) solid 2px;
    border-radius: 50px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 34px;
    padding: 10px 0;
}}

.hamburger .bar {{
    flex-basis: 100%;
    height: 3px;
    background-color: var(--text);
    margin: 4px 0;
    border-radius: 2px;
}}

/* Main Page Content for Demonstration */
main {{
    max-width: {width_px}px;
    margin: 60px auto;
    padding: 0 20px;
}}

main h1 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

main p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* === Mobile Responsive Design === */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex;
        flex-wrap: wrap;
    }}
    
    .nav-links {{
        display: none; /* Controlled by JS */
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
    }}
    
    .nav-links li {{
        width: 100%;
    }}
    
    .nav-links a {{
        text-align: center;
        font-size: 20px;
        padding: 20px 16px;
    }}
    
    .nav-cta-button {{
        margin-left: 0;
        border: none;
        border-radius: 0;
        margin-bottom: 10px;
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
    <nav>
        <div class="logo">
            <!-- Simple SVG Logo Placeholder -->
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="40" height="40" rx="8" fill="var(--text)"/>
                <circle cx="20" cy="20" r="12" fill="var(--nav-bg)"/>
            </svg>
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

    <main>
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    let menuOpen = false;

    // Toggle menu on click
    hamburger.addEventListener('click', () => {
        if (menuOpen === false) {
            navLinks.style.display = "block";
            menuOpen = true;
        } else {
            navLinks.style.display = "none";
            menuOpen = false;
        }
    });

    // Handle window resizing to prevent hidden links on desktop
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            navLinks.style.display = ''; // Clear inline styles
            menuOpen = false;
        } else {
            if (!menuOpen) {
                navLinks.style.display = 'none';
            }
        }
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
