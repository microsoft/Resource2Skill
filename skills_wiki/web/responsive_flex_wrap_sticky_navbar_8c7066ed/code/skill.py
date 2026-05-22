def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. Resize the window to test the mobile hamburger menu.",
    color_scheme: str = "light",        # "dark" or "light" controls the BODY background, navbar remains contrasting
    accent_color: str = "#39ffde",     # CSS hex color for accent/CTA
    width_px: int = 100%,
    height_px: int = 100,              # Height of the viewport/container to demo scrolling
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flex-Wrap Sticky Navbar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        body_bg = "#222222"
        body_text_color = "#f0f0f0"
        nav_bg = "#111111"
        nav_text = "#ffffff"
        hamburger_color = "#ffffff"
    else:
        body_bg = "#f4f4f4"
        body_text_color = "#333333"
        nav_bg = "#ffffff"
        nav_text = "#111111"
        hamburger_color = "#111111"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar - Generated Component */
:root {{
    --body-bg: {body_bg};
    --body-text: {body_text_color};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --hamburger: {hamburger_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--body-bg);
    color: var(--body-text);
    min-height: 200vh; /* Extra height to demonstrate sticky scrolling */
}}

/* Navbar Core Styles */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap; /* Crucial for mobile stacking */
    padding: 0 40px;
    background-color: var(--nav-bg);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
    min-height: 70px;
}}

/* Logo */
.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--nav-text);
}}

.logo svg {{
    width: 30px;
    height: 30px;
    fill: var(--nav-text);
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li a {{
    display: block;
    padding: 25px 16px;
    color: var(--nav-text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    transition: all ease-in-out 150ms;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: #111; /* Ensure contrast on hover */
}}

/* Call To Action Button */
.nav-cta-button {{
    padding: 10px 20px !important;
    margin-left: 16px;
    border: solid 2px var(--accent);
    border-radius: 50px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: #111 !important;
}}

/* Hamburger Menu Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 30px;
    height: 20px;
    flex-direction: column;
    justify-content: space-between;
}}

.hamburger .bar {{
    flex-basis: 100%;
    height: 3px;
    background-color: var(--hamburger);
    border-radius: 2px;
}}

/* Page Content */
.content-wrapper {{
    max-width: 800px;
    margin: 60px auto;
    padding: 0 20px;
    line-height: 1.6;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    nav {{
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile, toggled by JS */
        flex-basis: 100%; /* Forces menu to wrap below logo/hamburger */
        flex-direction: column;
        padding-top: 15px;
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-links li a {{
        padding: 15px;
    }}

    .nav-cta-button {{
        margin-left: 0;
        margin-top: 10px;
        margin-bottom: 15px;
        display: inline-block;
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <div class="logo">
            <!-- Simple placeholder geometric logo -->
            <svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/></svg>
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

    <div class="content-wrapper">
        <h1>Welcome to {title_text}</h1>
        <p style="margin-top: 20px;">{body_text}</p>
        
        <div style="margin-top: 60px; padding: 40px; background: rgba(128,128,128,0.1); border-radius: 8px;">
            <h3>Keep scrolling...</h3>
            <p style="margin-top: 10px; opacity: 0.7;">Notice how the navigation bar stays pinned to the top of the screen thanks to <code>position: sticky</code>.</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // State tracker for mobile menu
    let menuOpen = false;

    hamburger.addEventListener('click', () => {{
        if (!menuOpen) {{
            // Open the menu
            navLinks.style.display = 'flex';
            menuOpen = true;
        }} else {{
            // Close the menu
            navLinks.style.display = 'none';
            menuOpen = false;
        }}
    }});

    // Optional: Reset inline styles if window is resized back to desktop
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.style.display = ''; // Clear inline styles to let CSS take over
            menuOpen = false;
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
