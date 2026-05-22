def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # Vibrant cyan from the tutorial
    width_px: int = 1000,              # Window width preview limit
    height_px: int = 800,              # Window height preview limit
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Hamburger Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        body_bg = "#222222"
        nav_bg = "#111111"
        text_color = "#ffffff"
        text_hover = "#111111"
    else:
        body_bg = "#f0f0f0"
        nav_bg = "#ffffff"
        text_color = "#111111"
        text_hover = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar - CSS Reset & Variables */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --text-hover: {text_hover};
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
    background-color: var(--nav-bg);
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    flex-wrap: wrap; /* Allows dropdown to wrap below the logo */
}}

/* Logo */
.logo {{
    display: flex;
    align-items: center;
    height: 60px;
}}

.logo h3 {{
    font-size: 24px;
    color: var(--text);
    cursor: pointer;
}}

/* Navigation Links (Desktop) */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li a {{
    display: block;
    padding: 20px 16px;
    color: var(--text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all ease-in-out 150ms;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* Call To Action Button */
.nav-cta-button {{
    margin-left: 16px;
    padding: 10px 18px !important;
    border: 2px solid var(--accent);
    border-radius: 50px;
    color: var(--accent) !important;
}}

.nav-cta-button:hover {{
    background-color: var(--accent) !important;
    color: var(--text-hover) !important;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 34px;
    flex-direction: column;
    gap: 4px;
}}

.hamburger .bar {{
    flex-basis: 100%;
    height: 4px;
    background-color: var(--text);
    border-radius: 2px;
}}

/* Demo Content Area */
.content {{
    padding: 40px 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    line-height: 1.6;
}}

.content h1 {{
    margin-bottom: 20px;
    font-size: 2.5rem;
}}

/* ==== Responsive Design ==== */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex; /* Show hamburger */
    }}
    
    .nav-links {{
        display: none; /* Hidden by default on mobile, toggled via JS */
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
        padding-bottom: 20px;
    }}
    
    .nav-links li {{
        width: 100%;
        text-align: center;
    }}
    
    .nav-cta-button {{
        margin-left: 0;
        margin-top: 10px;
        display: inline-block;
        width: max-content;
    }}
}}

/* Desktop resize fallback to ensure menu stays visible if JS hid it */
@media (min-width: 769px) {{
    .nav-links {{
        display: flex !important;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Navigation Bar -->
    <nav>
        <div class="logo">
            <h3>{title_text}</h3>
        </div>
        
        <!-- Hamburger Menu Icon -->
        <div class="hamburger">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        
        <!-- Navigation Links -->
        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li><a class="nav-cta-button" href="#contact">Contact</a></li>
        </ul>
    </nav>

    <!-- Main Content -->
    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <p style="margin-top: 50vh; opacity: 0.5;">Keep scrolling to test sticky behavior...</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // State tracker for mobile menu
    let menuOpen = false;

    // Toggle logic
    hamburger.addEventListener('click', () => {
        if (menuOpen === false) {
            navLinks.style.display = "flex";
            menuOpen = true;
        } else {
            navLinks.style.display = "none";
            menuOpen = false;
        }
    });

    // Optional: Close menu when a link is clicked (useful for single page apps/smooth scrolling)
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navLinks.style.display = "none";
                menuOpen = false;
            }
        });
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
