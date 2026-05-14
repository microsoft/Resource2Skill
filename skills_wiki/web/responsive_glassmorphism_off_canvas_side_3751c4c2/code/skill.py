def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Resize the browser to see the responsive glassmorphism sidebar in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent logo
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Sidebar Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#1a1a1a"
        text_color = "#ffffff"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "rgba(26, 26, 26, 0.4)"
        # Vibrant background so the blur effect is highly visible
        body_bg = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)" 
    else:
        nav_bg = "#ffffff"
        text_color = "#111111"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        sidebar_bg = "rgba(255, 255, 255, 0.2)"
        body_bg = "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navbar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}}

:root {{
    --nav-bg: {nav_bg};
    --text-color: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-bg: {sidebar_bg};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background: {body_bg};
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.viewport-container {{
    width: var(--width);
    height: var(--height);
    background: {body_bg};
    position: relative;
    overflow-x: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    border-radius: 8px;
}}

/* Top Navigation Bar */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.1);
    width: 100%;
}}

nav ul {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
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
    transition: background-color 0.2s ease;
}}

nav a:hover {{
    background-color: var(--hover-bg);
}}

/* Push logo to the left */
.nav-links li:first-child {{
    margin-right: auto;
}}
.nav-links li:first-child a {{
    font-weight: 700;
    color: var(--accent);
    font-size: 1.1rem;
}}

/* Sidebar (Off-canvas menu) */
.sidebar {{
    position: absolute; /* Using absolute inside our relative component container instead of fixed */
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: -10px 0 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    
    /* Animation enhancement over the tutorial */
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.sidebar.active {{
    transform: translateX(0);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
}}

.menu-button {{
    display: none;
}}

/* SVG Icon Coloring */
nav svg {{
    fill: var(--text-color);
}}

/* Main Content Area */
main {{
    padding: 80px 40px;
    color: {text_color};
    text-align: center;
}}

main h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}}

/* Responsive Breakpoints */
@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

@media (max-width: 400px) {{
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
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Viewport Container mimics the browser window for component display -->
    <div class="viewport-container">
        
        <nav>
            <!-- Sidebar / Off-canvas Menu -->
            <ul class="sidebar" id="sidebar">
                <li>
                    <a href="#" id="close-btn" aria-label="Close menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26">
                            <path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/>
                        </svg>
                    </a>
                </li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>

            <!-- Top Navbar -->
            <ul class="nav-links">
                <li><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button" id="open-btn">
                    <a href="#" aria-label="Open menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26">
                            <path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sidebar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.getElementById('sidebar');
    const openBtn = document.getElementById('open-btn');
    const closeBtn = document.getElementById('close-btn');

    // Open sidebar
    openBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.classList.add('active');
    }});

    // Close sidebar
    closeBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.classList.remove('active');
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
