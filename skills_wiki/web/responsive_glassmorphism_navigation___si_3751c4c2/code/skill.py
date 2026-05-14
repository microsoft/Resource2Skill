def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Experience the power of responsive design and frosted glass overlays.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for hover accents
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navigation pattern.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#0f172a"
        text_color = "#f8f9fa"
        hover_bg = "#1e293b"
        sidebar_glass = "rgba(15, 23, 42, 0.6)"
    else:
        nav_bg = "#ffffff"
        text_color = "#1a1a2e"
        hover_bg = "#f1f5f9"
        sidebar_glass = "rgba(255, 255, 255, 0.25)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text: {text_color};
    --hover-bg: {hover_bg};
    --accent: {accent_color};
    --sidebar-glass: {sidebar_glass};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #1a1a1a;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    /* Simulated page background to demonstrate glassmorphism */
    background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80');
    background-size: cover;
    background-position: center;
    background-color: #333;
}}

/* --- Main Navigation Bar --- */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.1);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}}

nav ul {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}}

nav li {{
    height: 60px;
}}

nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text);
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

nav a:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

/* Push the logo to the far left */
nav li:first-child {{
    margin-right: auto;
}}

.logo {{
    font-weight: 700;
    font-size: 1.2rem;
}}

/* --- Sidebar Overlay --- */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px); /* Safari support */
    box-shadow: -10px 0 10px rgba(0, 0, 0, 0.1);
    display: none; /* Hidden by default via JS state */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
}}

.sidebar svg, nav svg {{
    fill: currentColor;
}}

/* --- Hero Content (Demonstrates Blur) --- */
.hero {{
    padding: 120px 40px 40px;
    color: #ffffff;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.25rem;
    max-width: 600px;
    line-height: 1.6;
}}

/* --- Responsive Breakpoints --- */

.menu-button {{
    display: none; /* Hidden on desktop */
}}

/* Tablet Breakpoint */
@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

/* Mobile Breakpoint */
@media (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

    # === HTML ===
    # Inline SVGs for Menu (hamburger) and Close (X)
    svg_menu = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>'
    svg_close = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>'

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
    <div class="app-wrapper">
        <nav>
            <!-- Sidebar Drawer -->
            <ul class="sidebar">
                <li class="close-button"><a href="#">{svg_close}</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            
            <!-- Main Horizontal Nav -->
            <ul class="main-nav">
                <li><a href="#" class="logo">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button"><a href="#">{svg_menu}</a></li>
            </ul>
        </nav>

        <main class="hero">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sidebar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-button a');
    const closeBtn = document.querySelector('.close-button a');

    // Open Sidebar
    menuBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.style.display = 'flex';
    }});

    // Close Sidebar
    closeBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.style.display = 'none';
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
