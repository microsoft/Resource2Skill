def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. Resize the window to see the responsive mobile menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # Teal accent from the tutorial
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

    # Derive theme colors
    if color_scheme == "dark":
        body_bg = "#111111"
        nav_bg = "#222222"
        text_color = "#ffffff"
        nav_text = "#ffffff"
        hamburger_color = "#ffffff"
    else:
        body_bg = "#f0f2f5"
        nav_bg = "#ffffff"
        text_color = "#333333"
        nav_text = "#111111"
        hamburger_color = "#111111"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar Component */
:root {{
    --body-bg: {body_bg};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --hamburger: {hamburger_color};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--text);
    min-height: 200vh; /* Forced height to demonstrate sticky scrolling */
}}

/* Navigation Bar */
nav {{
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    background-color: var(--nav-bg);
    padding: 15px 30px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}}

/* Logo / Brand */
.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 24px;
    font-weight: 700;
    color: var(--nav-text);
    text-decoration: none;
}}

.logo svg {{
    width: 30px;
    height: 30px;
    fill: var(--nav-text);
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
    gap: 25px;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: color 0.2s ease-in-out;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* CTA Button Styling */
.nav-cta-button {{
    border: 2px solid var(--accent);
    padding: 10px 20px;
    border-radius: 50px;
    transition: all 0.2s ease-in-out;
}}

.nav-links a.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--nav-bg);
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
}}

.hamburger .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--hamburger);
    border-radius: 3px;
    transition: all 0.3s ease-in-out;
}}

/* Main Content Area */
.content {{
    max-width: {width_px}px;
    margin: 60px auto;
    padding: 0 30px;
    line-height: 1.6;
}}

.content h1 {{
    margin-bottom: 20px;
    font-size: 2.5rem;
}}

/* Responsive Design - Mobile */
@media (max-width: 768px) {{
    nav {{
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
        padding-bottom: 10px;
        gap: 15px;
    }}

    /* Class added via JavaScript */
    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-cta-button {{
        display: inline-block;
        margin-top: 10px;
    }}
    
    /* Hamburger Animation to X */
    .hamburger.is-active .bar:nth-child(1) {{
        transform: translateY(9px) rotate(45deg);
    }}
    .hamburger.is-active .bar:nth-child(2) {{
        opacity: 0;
    }}
    .hamburger.is-active .bar:nth-child(3) {{
        transform: translateY(-9px) rotate(-45deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <a href="#" class="logo">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 22h20L12 2zm0 3.8l7.2 14.2H4.8L12 5.8z"/>
            </svg>
            {title_text}
        </a>

        <div class="hamburger" aria-label="Toggle Menu" aria-expanded="false">
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

    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <br><br><br><br><br>
        <p><em>(Keep scrolling to observe the sticky position of the navigation bar...)</em></p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navigation Behavior
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        // Toggle the dropdown menu visibility
        navLinks.classList.toggle('active');
        
        // Toggle the hamburger icon animation state
        hamburger.classList.toggle('is-active');
        
        // Update ARIA attribute for accessibility
        const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
        hamburger.setAttribute('aria-expanded', !isExpanded);
    });
});
"""

    # Write files to disk
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
