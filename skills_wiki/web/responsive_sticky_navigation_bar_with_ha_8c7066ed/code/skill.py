def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. This content area forces a scrollable viewport.",
    color_scheme: str = "light",        
    accent_color: str = "#39ffde",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#1e1e24"
        nav_text = "#ffffff"
        body_bg = "#121215"
        body_text = "#cccccc"
    else:
        nav_bg = "#ffffff"
        nav_text = "#111111"
        body_bg = "#222222" # Dark body for contrast as seen in the tutorial
        body_text = "#f0f0f0"

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --body-text: {body_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--body-bg);
    color: var(--body-text);
    position: relative;
    overflow-y: auto; /* Enable scrolling to demonstrate stickiness */
    overflow-x: hidden;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}}

/* --- Navigation Styles --- */
nav {{
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}}

.logo svg {{
    width: 24px;
    height: 24px;
    fill: var(--nav-text);
}}

.logo h3 {{
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li {{
    margin-left: 10px;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    padding: 8px 16px;
    transition: all 0.2s ease-in-out;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* CTA Button Specific Styling */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    margin-left: 10px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: #111 !important; /* Ensure high contrast against accent bg */
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    gap: 4px;
}}

.hamburger .bar {{
    width: 28px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Dummy Content for Scrolling */
.content {{
    padding: 60px 30px;
    min-height: 150vh; /* Forces container to scroll */
    background: linear-gradient(to bottom, var(--body-bg), #000);
}}

.content h1 {{
    margin-bottom: 20px;
    font-size: 2.5rem;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* --- Mobile Responsive Design --- */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex; /* Show toggle button */
    }}

    .nav-links {{
        display: none; /* Hide links by default */
        width: 100%;
        flex-direction: column;
        padding-top: 15px;
    }}

    /* Class toggled by JavaScript */
    .nav-links.active {{
        display: flex;
        animation: fadeInDown 0.3s ease forwards;
    }}

    .nav-links li {{
        width: 100%;
        margin-left: 0;
        text-align: center;
    }}

    .nav-links a {{
        display: block;
        padding: 15px 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
    }}

    .nav-cta-button {{
        margin: 15px auto;
        display: inline-block;
    }}
}}

@keyframes fadeInDown {{
    from {{ opacity: 0; transform: translateY(-10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Container acts as the simulated browser window -->
    <div class="container">
        
        <nav>
            <div class="logo">
                <svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 3.8l6.4 12.2H5.6L12 5.8z"/></svg>
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

        <div class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle mobile menu
    hamburger.addEventListener('click', () => {{
        // Toggling a class is much more robust than manipulating inline style.display
        // as it prevents layout bugs when resizing back to desktop width.
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger bars to 'X' (not explicitly in tutorial, but good practice)
        hamburger.classList.toggle('toggle');
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
