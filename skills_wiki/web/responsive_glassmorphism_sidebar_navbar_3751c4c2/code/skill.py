def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "A clean, responsive navbar that morphs into a frosted-glass sidebar on mobile devices. Resize the container to see the transformation.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg = "#16161a"
        text_color = "#f0f0f0"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "rgba(15, 15, 20, 0.5)" # Semi-transparent dark
        shadow_color = "rgba(0, 0, 0, 0.5)"
        page_bg = "#0d111c"
    else:
        nav_bg = "#ffffff"
        text_color = "#1a1a1a"
        hover_bg = "#f0f0f0"
        sidebar_bg = "rgba(255, 255, 255, 0.3)" # Semi-transparent light
        shadow_color = "rgba(0, 0, 0, 0.1)"
        page_bg = "#f8f9fa"

    # SVGs for Icons
    menu_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26" fill="currentColor"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>'
    close_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 -960 960 960" width="26" fill="currentColor"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>'

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {page_bg};
    --nav-bg: {nav_bg};
    --text-color: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-bg: {sidebar_bg};
    --shadow-color: {shadow_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The isolated component frame */
.app-frame {{
    container-type: inline-size; /* Enables container queries */
    position: relative;
    width: var(--width);
    height: var(--height);
    background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80');
    background-size: cover;
    background-position: center;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
}}

/* Tint overlay for background image readability */
.app-frame::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 0;
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 5px var(--shadow-color);
    width: 100%;
    z-index: 10; /* Elevate nav above hero */
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
    padding: 0 24px;
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

.logo {{
    margin-right: auto;
}}

.logo a {{
    font-size: 1.3rem;
    font-weight: 700;
}}

.logo a:hover {{
    background-color: transparent;
}}

.menu-button {{
    display: none;
}}

/* Sidebar - Pre-staged but hidden */
.sidebar {{
    position: absolute; /* Absolute to the .app-frame */
    top: 0;
    right: 0;
    height: 100%;
    width: 280px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: -10px 0 20px var(--shadow-color);
    display: none; /* JS will toggle this to flex */
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
}}

.hero {{
    position: relative;
    z-index: 1;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
    color: #fff;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}}

.hero p {{
    font-size: 1.1rem;
    max-width: 600px;
    line-height: 1.6;
    opacity: 0.9;
}}

/* === Container Queries for Responsiveness === */
@container (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

@container (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

    # === HTML ===
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
    <div class="app-frame">
        <nav>
            <ul class="sidebar">
                <li id="close-btn"><a href="#">{close_svg}</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            <ul>
                <li class="logo"><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button" id="menu-btn"><a href="#">{menu_svg}</a></li>
            </ul>
        </nav>
        
        <main class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Sidebar toggling logic
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');

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
