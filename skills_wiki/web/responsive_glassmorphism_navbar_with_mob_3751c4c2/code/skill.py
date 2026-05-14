def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "A responsive, glassmorphic navigation bar that adapts gracefully from desktop to mobile views.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors to ensure proper contrast and glassmorphism transparency
    if color_scheme == "dark":
        nav_bg = "rgba(13, 17, 28, 0.85)"
        text_color = "#f0f0f0"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_glass = "rgba(13, 17, 28, 0.6)"
        # A vivid gradient background to demonstrate the frosted glass blur
        bg_pattern = "radial-gradient(circle at top right, #2a2a4a 0%, #0d111c 100%)"
        body_bg = "#000"
    else:
        nav_bg = "rgba(255, 255, 255, 0.85)"
        text_color = "#1a1a2e"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        sidebar_glass = "rgba(255, 255, 255, 0.4)"
        # A soft gradient background for light mode
        bg_pattern = "radial-gradient(circle at top right, #e6eeff 0%, #f8f9fa 100%)"
        body_bg = "#ccc"

    # SVG Icons (Standardized clean paths matching the tutorial's intent)
    icon_menu = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>"""
    icon_close = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>"""

    css = f"""/* Responsive Navbar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text-color: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-glass: {sidebar_glass};
    --accent: {accent_color};
    --bg-pattern: {bg_pattern};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: {body_bg};
}}

/* The mock viewport acts as our "device screen" container */
.mock-viewport {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background: var(--bg-pattern);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    /* Container Queries enable true component-level responsiveness */
    container-type: inline-size;
    container-name: viewport;
}}

nav {{
    background-color: var(--nav-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    position: relative;
    z-index: 10;
}}

nav ul {{
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
}}

nav li {{
    height: 50px;
}}

nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text-color);
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

nav a:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

/* Pushes everything else to the right */
.logo {{
    margin-right: auto;
    font-weight: 700;
    font-size: 1.15rem;
    letter-spacing: -0.5px;
}}

.menu-button {{
    display: none;
}}

/* The Glassmorphism Side Drawer */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: -10px 0 25px rgba(0, 0, 0, 0.1);
    display: none; /* Toggled via JS */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
    justify-content: flex-start;
}}

.content {{
    padding: 60px 40px;
    color: var(--text-color);
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}}

.content h1 {{
    margin-bottom: 16px;
    font-size: 2.5rem;
}}

.content p {{
    font-size: 1.1rem;
    opacity: 0.8;
    line-height: 1.6;
}}

/* Responsive Breakpoints using Container Queries */
@container viewport (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

@container viewport (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

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
    <div class="mock-viewport">
        <nav>
            <!-- Mobile Sidebar Drawer -->
            <ul class="sidebar">
                <li class="close-button"><a href="#">{icon_close}</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            
            <!-- Standard Desktop Navbar -->
            <ul class="main-nav">
                <li class="logo"><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button"><a href="#">{icon_menu}</a></li>
            </ul>
        </nav>
        
        <!-- Page Context to demonstrate glassmorphism -->
        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Responsive Navbar Interactive Logic
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-button');
    const closeBtn = document.querySelector('.close-button');

    // Open sidebar
    menuBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.style.display = 'flex';
    });

    // Close sidebar
    closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.style.display = 'none';
    });
});
"""

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
