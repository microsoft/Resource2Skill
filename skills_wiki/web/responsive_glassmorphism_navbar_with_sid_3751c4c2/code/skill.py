def create_component(
    output_dir: str,
    title_text: str = "Coding2go",
    body_text: str = "Experience the frosted glass sidebar by resizing this component below 800px width and clicking the hamburger icon.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        nav_bg = "#1a1a1a"
        text_color = "#ffffff"
        hover_bg = "#333333"
        sidebar_bg = "rgba(0, 0, 0, 0.4)"
        glass_border = "rgba(255, 255, 255, 0.05)"
    else:
        nav_bg = "#ffffff"
        text_color = "#1a1a1a"
        hover_bg = "#f0f0f0"
        sidebar_bg = "rgba(255, 255, 255, 0.25)"
        glass_border = "rgba(255, 255, 255, 0.4)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navbar */
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
    --glass-border: {glass_border};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #0f172a; /* Dark presentation background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.component-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    /* Rich background image to demonstrate the glassmorphism blur effect */
    background-image: url('https://images.unsplash.com/photo-1550439062-609e1531270e?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    position: relative;
    /* Create a containing block for fixed position children */
    transform: translateZ(0); 
    overflow: hidden;
    /* Modern container query for isolated responsiveness */
    container-type: inline-size;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
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
}}

/* Push the first item (Logo) to the far left */
nav li:first-child {{
    margin-right: auto;
}}

.logo {{
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--accent);
}}

/* --- Glassmorphism Sidebar --- */
.sidebar {{
    position: fixed;
    top: 0;
    right: 0;
    height: 100%; 
    width: 280px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-left: 1px solid var(--glass-border);
    box-shadow: -10px 0 30px rgba(0,0,0,0.15);
    display: none; /* Hidden by default */
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

.menu-button {{
    display: none; /* Hidden on desktop */
    cursor: pointer;
}}

/* Content styling to simulate a real page */
.hero-content {{
    padding: 4rem;
    color: #ffffff;
    text-shadow: 0 2px 8px rgba(0,0,0,0.6);
}}

.hero-content h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.hero-content p {{
    font-size: 1.2rem;
    max-width: 500px;
    line-height: 1.6;
}}

/* --- Responsive Container Queries --- */
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
    <div class="component-wrapper">
        <nav>
            <!-- Sidebar Drawer -->
            <ul class="sidebar">
                <li onclick="hideSidebar()" aria-label="Close menu" role="button" tabindex="0">
                    <a href="#">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor">
                            <path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/>
                        </svg>
                    </a>
                </li>
                <li><a href="#" class="logo">{title_text}</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>

            <!-- Desktop Navbar -->
            <ul>
                <li><a href="#" class="logo">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                
                <!-- Hamburger Menu Icon -->
                <li class="menu-button" onclick="showSidebar()" aria-label="Open menu" role="button" tabindex="0">
                    <a href="#">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor">
                            <path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>
        
        <!-- Main Page Content -->
        <main class="hero-content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Glassmorphism Navbar Logic

function showSidebar() {{
    const sidebar = document.querySelector('.sidebar');
    // Using flex to maintain the vertical column stacking logic
    sidebar.style.display = 'flex';
}}

function hideSidebar() {{
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'none';
}}
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
