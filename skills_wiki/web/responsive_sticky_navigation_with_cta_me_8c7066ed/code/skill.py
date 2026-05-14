def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. This pattern provides continuous access to wayfinding without consuming permanent screen space as the user reads content.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent (cyan/teal from video)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        body_bg = "#121212"
        nav_bg = "#1e1e1e"
        text_color = "#ffffff"
        text_hover = "#111111"
        hamburger_color = "#ffffff"
    else:
        body_bg = "#f0f0f0"
        nav_bg = "#ffffff"
        text_color = "#111111"
        text_hover = "#ffffff"
        hamburger_color = "#111111"

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation — generated component */
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
    --hamburger: {hamburger_color};
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
    padding: 0 40px;
    background-color: var(--nav-bg);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    flex-wrap: wrap; /* Allows mobile menu to drop down */
}}

/* Logo Section */
.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 0;
}}

.logo svg {{
    width: 32px;
    height: 32px;
    fill: var(--text);
}}

.logo h3 {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 1px;
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li a {{
    display: block;
    text-decoration: none;
    color: var(--text);
    padding: 30px 20px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all 0.2s ease-in-out;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* CTA Button Specifics */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    padding: 10px 24px !important;
    margin-left: 20px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--text-hover) !important;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 34px;
    flex-direction: column;
    gap: 6px;
    padding: 20px 0;
}}

.hamburger .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--hamburger);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Main Content Placeholder */
main {{
    max-width: 800px;
    margin: 60px auto;
    padding: 0 20px;
    line-height: 1.6;
    font-size: 18px;
}}

/* Responsive Design - Mobile */
@media (max-width: 768px) {{
    nav {{
        padding: 0 20px;
    }}
    
    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Handled by JS */
        flex-basis: 100%;
        flex-direction: column;
        background-color: var(--nav-bg);
        border-top: 1px solid rgba(128, 128, 128, 0.1);
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-links li a {{
        padding: 20px;
        font-size: 18px;
    }}

    .nav-cta-button {{
        margin: 20px auto;
        width: fit-content;
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
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 22h20L12 2zm0 3.83L19.17 20H4.83L12 5.83z"/>
            </svg>
            <h3>{title_text}</h3>
        </div>
        
        <div class="hamburger" aria-label="Toggle navigation" role="button" tabindex="0">
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
        <br>
        <p>{body_text}</p>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <p>Keep scrolling to see the navigation bar stick to the top.</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Navigation — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    let menuOpen = false;

    // Toggle menu on click
    hamburger.addEventListener('click', () => {{
        if (!menuOpen) {{
            navLinks.style.display = 'flex';
            menuOpen = true;
        }} else {{
            navLinks.style.display = 'none';
            menuOpen = false;
        }}
    }});

    // Accessibility: Allow toggling with Enter key for keyboard users
    hamburger.addEventListener('keypress', (e) => {{
        if (e.key === 'Enter') {{
            hamburger.click();
        }}
    }});

    // Fix for resizing window: ensure menu displays correctly if scaled back up
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.style.display = ''; // Clear JS inline style to let CSS take over
            menuOpen = false;
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
