def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Scroll down to see the sticky glassmorphism navbar and sidebar in action.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent hover
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar & Sidebar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "rgba(13, 17, 28, 0.95)"
        text_color = "#f0f0f0"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "rgba(13, 17, 28, 0.4)"
        page_bg = "#0d111c"
        shadow_color = "rgba(0, 0, 0, 0.5)"
        overlay_bg = "rgba(0, 0, 0, 0.6)"
    else:
        nav_bg = "rgba(255, 255, 255, 0.95)"
        text_color = "#1a1a2e"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        sidebar_bg = "rgba(255, 255, 255, 0.3)"
        page_bg = "#f0f2f5"
        shadow_color = "rgba(0, 0, 0, 0.1)"
        overlay_bg = "rgba(255, 255, 255, 0.6)"

    # SVG Icons
    menu_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor"><path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/></svg>'
    close_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>'

    # === CSS ===
    css = f"""/* Responsive Navbar & Sidebar Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text: {text_color};
    --hover-bg: {hover_bg};
    --sidebar-bg: {sidebar_bg};
    --page-bg: {page_bg};
    --shadow: {shadow_color};
    --accent: {accent_color};
    --overlay: {overlay_bg};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Simulator acts as the viewport for our component */
.device-simulator {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    background-color: var(--page-bg);
    background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80');
    background-size: cover;
    background-position: center;
    position: relative;
    overflow-x: hidden;
    overflow-y: auto;
    
    /* Crucial: traps `position: fixed` elements inside this simulator */
    transform: translateZ(0); 
    container-type: inline-size;
}}

/* Tint overlay to ensure text contrast against the image */
.device-simulator::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: var(--overlay);
    z-index: 1;
    pointer-events: none;
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 10px var(--shadow);
    position: sticky;
    top: 0;
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

/* Pushes everything else to the right */
nav .logo {{
    margin-right: auto;
}}

nav .logo a {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

nav .logo a:hover {{
    background-color: transparent;
    color: var(--text);
}}

/* Mobile Sidebar Styling */
.sidebar {{
    position: fixed;
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: -10px 0 20px var(--shadow);
    display: none;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    animation: slideIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}}

@keyframes slideIn {{
    from {{ transform: translateX(100%); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
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

/* Main content layer */
main {{
    position: relative;
    z-index: 2;
    padding: 40px;
    color: var(--text);
}}

main h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

main p {{
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 600px;
}}

.skeleton-content {{
    height: 250px;
    background: var(--hover-bg);
    backdrop-filter: blur(4px);
    border: 1px solid var(--sidebar-bg);
    border-radius: 12px;
    margin-top: 2rem;
}}

/* Responsiveness using Container Queries relative to simulator */
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
    <title>{title_text} - Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="device-simulator">
        <nav>
            <!-- Mobile Sidebar Panel -->
            <ul class="sidebar">
                <li class="close-button"><a href="#">{close_svg}</a></li>
                <li><a href="#">Home</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            
            <!-- Standard Navbar -->
            <ul class="main-nav">
                <li class="logo"><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Home</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button"><a href="#">{menu_svg}</a></li>
            </ul>
        </nav>

        <main>
            <h1>Discover Seamless Routing</h1>
            <p>{body_text}</p>
            <div class="skeleton-content"></div>
            <div class="skeleton-content"></div>
            <div class="skeleton-content"></div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navbar interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-button');
    const closeBtn = document.querySelector('.close-button');

    // Show sidebar
    menuBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        // Changing display to flex reveals the element and triggers the CSS slideIn animation
        sidebar.style.display = 'flex';
    }});

    // Hide sidebar
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
