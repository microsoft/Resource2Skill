def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. Resize the window to test the mobile flex-wrap hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent (e.g., cyan)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flex-Wrap Navbar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        surface_color = "#1a1f36"
        text_color = "#f0f0f0"
        text_hover = "#111111" # Dark text ensures contrast on bright accent colors
    else:
        bg_color = "#f0f0f0"
        surface_color = "#ffffff"
        text_color = "#111111"
        text_hover = "#111111"

    # === CSS ===
    css = f"""/* Responsive Flex-Wrap Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --accent: {accent_color};
    --text-hover: {text_hover};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
}}

/* -- Navbar Core -- */
.navbar {{
    position: sticky;
    top: 0;
    background-color: var(--surface);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
    flex-wrap: wrap; /* CRITICAL: allows mobile menu to wrap to next line */
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}}

/* -- Logo -- */
.logo a {{
    color: var(--text);
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: 700;
    padding: 20px 0;
    display: block;
}}

/* -- Desktop Links -- */
.nav-links {{
    list-style: none;
    display: flex;
    align-items: center;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 24px 20px;
    display: block;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* -- CTA Button Styling -- */
.nav-cta-button {{
    margin-left: 10px;
}}

.nav-cta-button a {{
    border: 2px solid var(--accent);
    border-radius: 50px;
    padding: 10px 24px;
    margin-left: 10px;
}}

.nav-cta-button a:hover {{
    background-color: var(--accent);
    color: var(--text-hover);
}}

/* -- Hamburger Icon (Hidden on Desktop) -- */
.hamburger {{
    display: none;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 10px;
}}

.hamburger .bar {{
    display: block;
    width: 28px;
    height: 3px;
    margin: 5px auto;
    background-color: var(--text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* -- Responsive Mobile Adjustments -- */
@media (max-width: 768px) {{
    .hamburger {{
        display: block; /* Show hamburger */
    }}
    
    .nav-links {{
        display: none; /* Hide links by default */
        flex-direction: column;
        width: 100%;
        flex-basis: 100%; /* CRITICAL: Forces the links to wrap below the header */
        padding-bottom: 20px;
    }}
    
    .nav-links.active {{
        display: flex; /* Shown when JS toggles class */
    }}
    
    .nav-links a {{
        text-align: center;
        padding: 15px;
        font-size: 1.1rem;
    }}
    
    .nav-cta-button {{
        margin: 15px 0 0 0;
        text-align: center;
    }}
    
    .nav-cta-button a {{
        margin: 0 auto;
        display: inline-block;
    }}
}}

/* -- Page Content -- */
.content {{
    padding: 60px 5%;
    max-width: var(--max-width);
    margin: 0 auto;
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}

.dummy-scroll {{
    height: 150vh;
    background: linear-gradient(to bottom, var(--surface), transparent);
    margin-top: 40px;
    border-radius: 12px;
    opacity: 0.3;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Semantic Nav Element -->
    <nav class="navbar" aria-label="Main Navigation">
        
        <div class="logo">
            <a href="#">{title_text}</a>
        </div>
        
        <!-- Accessible Button for Hamburger -->
        <button class="hamburger" aria-expanded="false" aria-controls="nav-menu" aria-label="Toggle navigation menu">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </button>
        
        <ul id="nav-menu" class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li class="nav-cta-button"><a href="#contact">Contact</a></li>
        </ul>
        
    </nav>

    <!-- Main Content Context -->
    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
        <div class="dummy-scroll"></div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar Interactivity
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {{
        // Toggle the active class which changes display from none to flex
        const isActive = navLinks.classList.toggle('active');
        
        // Update ARIA accessibility attribute based on state
        hamburger.setAttribute('aria-expanded', isActive);
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
