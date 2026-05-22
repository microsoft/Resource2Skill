def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the navigation bar remain sticky at the top. Resize the browser window below 768px to see the mobile hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        nav_bg = "#222222"
        nav_text = "#ffffff"
        page_bg = "#111111"
        page_text = "#cccccc"
        hover_text = "#222222" # Dark text on accent bg for contrast
    else:
        nav_bg = "#ffffff"
        nav_text = "#111111"
        page_bg = "#f0f2f5"
        page_text = "#333333"
        hover_text = "#ffffff" # Light text on accent bg for contrast

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --hover-text: {hover_text};
    --page-bg: {page_bg};
    --page-text: {page_text};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--page-text);
    min-height: 200vh; /* Force scrolling to demonstrate sticky */
}}

/* Simulated Viewport wrapper for demo purposes if viewed in large frames */
.demo-viewport {{
    max-width: {width_px}px;
    margin: 0 auto;
    background: var(--page-bg);
    min-height: 100vh;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    position: relative;
}}

/* === Core Navigation Styles === */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    min-height: 70px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}}

.logo {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.5px;
    cursor: pointer;
}}

.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
}}

.nav-links li a {{
    text-decoration: none;
    color: var(--nav-text);
    padding: 12px 18px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    transition: all 0.2s ease-in-out;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

/* Call To Action Button Style */
.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    margin-left: 15px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    gap: 5px;
}}

.hamburger .bar {{
    width: 25px;
    height: 3px;
    background-color: var(--nav-text);
    transition: 0.3s;
}}

/* === Responsive Mobile Styles === */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap; /* Key mechanism to push links down */
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%; /* Take full width on new line */
        flex-direction: column;
        margin-top: 15px;
    }}

    /* Class toggled by JavaScript */
    .nav-links.active {{
        display: flex; 
    }}

    .nav-links li {{
        width: 100%;
        text-align: center;
    }}

    .nav-links li a {{
        display: block;
        padding: 15px;
    }}

    .nav-cta-button {{
        margin: 10px auto;
        width: max-content;
    }}
}}

/* Dummy Content */
.content {{
    padding: 60px 20px;
    line-height: 1.6;
    font-size: 1.1rem;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="demo-viewport">
        
        <!-- Navigation Component -->
        <nav>
            <div class="logo">{safe_title}</div>
            
            <div class="hamburger">
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

        <!-- Dummy Content to demonstrate sticky header -->
        <div class="content">
            <h1>Welcome to {safe_title}</h1>
            <br>
            <p>{safe_body}</p>
            <br><br><br><br><br><br><br><br><br><br><br><br>
            <p>Keep scrolling...</p>
            <br><br><br><br><br><br><br><br><br><br><br><br>
            <p>The navigation bar remains fixed at the top of the viewport.</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Menu Toggle
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu visibility on click
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
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
