def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Resize the container to see the navbar collapse into a responsive hamburger menu. Click the menu to reveal the glassmorphism sidebar.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        nav_bg = "rgba(20, 20, 25, 0.95)"
        text_color = "#ffffff"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "rgba(20, 20, 25, 0.5)"
        # Complex gradient to show off the backdrop-filter blur
        body_bg = f"radial-gradient(circle at top right, {accent_color}40, transparent 40%), radial-gradient(circle at bottom left, {accent_color}40, transparent 40%), #0d111c"
    else:
        nav_bg = "rgba(255, 255, 255, 0.95)"
        text_color = "#111111"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        sidebar_bg = "rgba(255, 255, 255, 0.5)"
        body_bg = f"radial-gradient(circle at top right, {accent_color}30, transparent 40%), radial-gradient(circle at bottom left, {accent_color}30, transparent 40%), #f4f4f9"

    css = f"""/* Responsive Glassmorphism Navbar */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-bg: {sidebar_bg};
    --accent: {accent_color};
    --body-bg: {body_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #111; /* Outer presentation background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Viewport frame acts as a simulated device screen */
.viewport-frame {{
    width: var(--width);
    height: var(--height);
    background: var(--body-bg);
    position: relative;
    overflow: hidden;
    container-type: inline-size;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    position: relative;
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
    padding: 0 24px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text);
    transition: background-color 0.2s ease;
    font-weight: 500;
}}

nav a:hover {{
    background-color: var(--hover-bg);
}}

/* Auto margin pushes the first item (Logo) to the far left */
nav li:first-child {{
    margin-right: auto;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

/* Sidebar Menu - Glassmorphism Drawer */
.sidebar {{
    position: absolute; /* Absolute relative to .viewport-frame */
    top: 0;
    right: 0;
    height: 100%;
    width: 280px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
    display: none; /* Toggled via JS */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
    justify-content: flex-start;
}}

.menu-button {{
    display: none;
}}

/* Main Content Styling */
.content {{
    padding: 4rem 3rem;
    color: var(--text);
    max-width: 800px;
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.content p {{
    font-size: 1.15rem;
    line-height: 1.7;
    opacity: 0.85;
}}

/* Container Queries for Responsiveness */
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
    <div class="viewport-frame">
        <nav>
            <!-- Mobile Sidebar Drawer -->
            <ul class="sidebar">
                <li onclick="hideSidebar()">
                    <a href="#" aria-label="Close Menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="28" viewBox="0 -960 960 960" width="28" fill="currentColor">
                            <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
                        </svg>
                    </a>
                </li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            
            <!-- Standard Desktop Navbar -->
            <ul>
                <li><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button" onclick="showSidebar()">
                    <a href="#" aria-label="Open Menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="28" viewBox="0 -960 960 960" width="28" fill="currentColor">
                            <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Expose functions globally to act as event handlers for the inline HTML attributes
window.showSidebar = function() {
    const sidebar = document.querySelector('.sidebar');
    // Change display from none to flex to reveal the drawer
    sidebar.style.display = 'flex';
};

window.hideSidebar = function() {
    const sidebar = document.querySelector('.sidebar');
    // Hide the drawer
    sidebar.style.display = 'none';
};
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
