def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Resize the window or the container to see the navigation collapse into a mobile hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
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

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        nav_bg = "#1a1f33"
        hover_bg = "rgba(255, 255, 255, 0.08)"
        glass_bg = "rgba(13, 17, 28, 0.4)"
        glass_border = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        nav_bg = "#ffffff"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        glass_bg = "rgba(255, 255, 255, 0.3)"
        glass_border = "rgba(255, 255, 255, 0.4)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Sidebar Navigation — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --nav-bg: {nav_bg};
    --hover-bg: {hover_bg};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #2a2a2a; /* Outer canvas background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The component container simulates a device viewport */
.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background-color: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    
    /* Decorative background shapes to demonstrate the glass blur effect */
    background-image: 
        radial-gradient(circle at 15% 50%, var(--accent) 0%, transparent 20%),
        radial-gradient(circle at 85% 30%, var(--accent) 0%, transparent 25%);
}}

.navbar {{
    background-color: var(--nav-bg);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    position: relative;
    z-index: 10;
}}

.navbar ul {{
    list-style: none;
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: flex-end;
}}

.navbar li {{
    height: 60px;
}}

.navbar a {{
    height: 100%;
    padding: 0 24px;
    text-decoration: none;
    color: var(--text);
    display: flex;
    align-items: center;
    transition: background-color 0.2s ease, color 0.2s ease;
    font-weight: 500;
}}

.navbar a:hover {{
    background-color: var(--hover-bg);
}}

/* Pushes everything else to the right */
.logo {{
    margin-right: auto;
}}

.logo a {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.logo a:hover {{
    background-color: transparent;
    color: var(--accent);
}}

/* Sidebar Specific Styles */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 280px;
    background-color: var(--glass-bg);
    
    /* Glassmorphism magic */
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-left: 1px solid var(--glass-border);
    box-shadow: -5px 0 20px rgba(0,0,0,0.1);
    
    display: none; /* Toggled via JS */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    z-index: 999;
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
    justify-content: flex-start;
}}

/* SVG Icon alignment */
.navbar svg {{
    fill: currentColor;
    display: block;
}}

.main-content {{
    padding: 60px 40px;
    color: var(--text);
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.main-content h1 {{
    margin-bottom: 16px;
    font-size: 2.5rem;
    line-height: 1.2;
}}

.main-content p {{
    opacity: 0.8;
    line-height: 1.6;
}}

/* Responsive Breakpoints */
@media (min-width: 801px) {{
    .menu-button {{
        display: none;
    }}
}}

@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
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
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <!-- Sidebar Navigation (Hidden by default) -->
            <ul class="sidebar">
                <li class="close-button">
                    <a href="#" aria-label="Close menu">
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

            <!-- Horizontal Desktop Navigation -->
            <ul class="desktop-nav">
                <li class="logo"><a href="#">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button">
                    <a href="#" aria-label="Open menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26">
                            <path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main class="main-content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Glassmorphism Sidebar Navigation — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-button');
    const closeBtn = document.querySelector('.close-button');

    // Open sidebar
    menuBtn.addEventListener('click', (e) => {{
        e.preventDefault(); // Prevent jump to top of page
        sidebar.style.display = 'flex';
    }});

    // Close sidebar
    closeBtn.addEventListener('click', (e) => {{
        e.preventDefault(); // Prevent jump to top of page
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
