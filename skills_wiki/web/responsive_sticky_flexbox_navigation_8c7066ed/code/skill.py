def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Flexbox Navigation visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1a1a2e"
        hover_text_color = "#111111"
    else:
        bg_color = "#f0f0f0"
        text_color = "#111111"
        surface_color = "#ffffff"
        hover_text_color = "#111111"

    # === CSS ===
    css = f"""/* Responsive Sticky Flexbox Navigation — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --hover-text: {hover_text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #333; /* Outer presentation background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

/* Navigation Styles */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--surface);
    color: var(--text);
    min-height: 70px;
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    /* Ensure the nav can wrap its children on mobile */
    flex-wrap: wrap; 
}}

.brand-logo {{
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    cursor: pointer;
}}

.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
}}

.nav-links li a {{
    display: block;
    padding: 10px 16px;
    text-decoration: none;
    color: var(--text);
    font-weight: 500;
    text-transform: uppercase;
    font-size: 14px;
    transition: all 0.2s ease-in-out;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

.nav-cta-button {{
    border: 2px solid var(--accent);
    border-radius: 4px;
    margin-left: 10px;
}}

/* Hamburger Menu Styles */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 30px;
    height: 21px;
    flex-direction: column;
    justify-content: space-between;
}}

.hamburger .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Mobile Responsiveness */
@media (max-width: 768px) {{
    .hamburger {{
        display: flex;
    }}
    
    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-direction: column;
        width: 100%;
        background-color: var(--surface);
        padding-bottom: 10px;
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
        padding: 15px;
    }}
    
    .nav-cta-button {{
        margin: 10px auto;
        width: 80%;
    }}
}}

/* Page Content Styles (for demonstration) */
.content {{
    padding: 40px;
    color: var(--text);
    max-width: 800px;
    margin: 0 auto;
}}

.content h1 {{
    margin-bottom: 16px;
    font-size: 32px;
}}

.scroll-spacer {{
    height: 150vh;
    margin-top: 50px;
    padding: 20px;
    border: 2px dashed var(--accent);
    opacity: 0.3;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    border-radius: 8px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Sticky Navigation Bar -->
        <nav class="navbar">
            <div class="brand-logo">{title_text}</div>
            
            <div class="hamburger" aria-label="Toggle Menu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
            
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#" class="nav-cta-button">Contact</a></li>
            </ul>
        </nav>

        <!-- Mock Page Content -->
        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            
            <div class="scroll-spacer">
                <p>Scroll down</p>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Flexbox Navigation — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle the mobile menu visibility
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
    }});

    // Optional: Close menu when a link is clicked (UX best practice)
    const links = document.querySelectorAll('.nav-links li a');
    links.forEach(link => {{
        link.addEventListener('click', () => {{
            if (window.innerWidth <= 768) {{
                navLinks.classList.remove('active');
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
