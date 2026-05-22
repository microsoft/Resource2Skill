def create_component(
    output_dir: str,
    title_text: str = "Coding2go",
    body_text: str = "Resize the window to see the responsive glassmorphism sidebar in action.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent/hover
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphic Responsive Sidebar Navigation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        nav_bg = "#1e293b"
        text_color = "#f8fafc"
        sidebar_bg = "rgba(30, 41, 59, 0.6)"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f1f5f9"
        nav_bg = "#ffffff"
        text_color = "#0f172a"
        sidebar_bg = "rgba(255, 255, 255, 0.3)"
        hover_bg = "#f1f5f9"
        shadow = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Glassmorphic Responsive Sidebar Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --accent: {accent_color};
    --sidebar-bg: {sidebar_bg};
    --hover-bg: {hover_bg};
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    /* Simulated background to show off the glassmorphism */
    background-image: radial-gradient(circle at 15% 50%, rgba(0, 191, 255, 0.15), transparent 25%), 
                      radial-gradient(circle at 85% 30%, rgba(255, 0, 255, 0.1), transparent 25%);
}}

.preview-container {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding-top: 100px;
    text-align: center;
}}

/* Main Navigation Bar */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 10px var(--shadow);
    position: fixed;
    top: 0;
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

nav a svg {{
    fill: currentColor;
}}

/* Push first item (Logo) to the left */
nav li:first-child {{
    margin-right: auto;
    font-weight: 700;
    font-size: 1.2rem;
}}

/* Glassmorphic Sidebar */
.sidebar {{
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 250px;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: -10px 0 20px var(--shadow);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    z-index: 999;
    /* Upgraded from raw display block/none to smooth transform */
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
}}

.sidebar.active {{
    transform: translateX(0);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
    padding: 0 30px;
}}

/* Hide Menu Button on Desktop */
.menu-button {{
    display: none;
}}

/* Media Queries for Responsiveness */
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
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <!-- Sidebar Menu (Hidden by default) -->
        <ul class="sidebar" id="sidebar">
            <li id="close-btn">
                <a href="#" aria-label="Close menu">
                    <svg viewBox="0 0 24 24" width="26" height="26"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                </a>
            </li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Products</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Forum</a></li>
            <li><a href="#">Login</a></li>
        </ul>

        <!-- Main Desktop Menu -->
        <ul>
            <li><a href="#">{title_text}</a></li>
            <li class="hideOnMobile"><a href="#">Blog</a></li>
            <li class="hideOnMobile"><a href="#">Products</a></li>
            <li class="hideOnMobile"><a href="#">About</a></li>
            <li class="hideOnMobile"><a href="#">Forum</a></li>
            <li class="hideOnMobile"><a href="#">Login</a></li>
            <li class="menu-button" id="open-btn">
                <a href="#" aria-label="Open menu">
                    <svg viewBox="0 0 24 24" width="26" height="26"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
                </a>
            </li>
        </ul>
    </nav>

    <div class="preview-container">
        <h1>{title_text} Navigation Concept</h1>
        <p>{body_text}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Navigation Bar Sidebar Logic
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

    // Optional: Close sidebar when clicking outside of it
    document.addEventListener('click', (e) => {{
        if (sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            !openBtn.contains(e.target)) {{
            sidebar.classList.remove('active');
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
