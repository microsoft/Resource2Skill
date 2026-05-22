def create_component(
    output_dir: str,
    title_text: str = "Animated Menu Tutorial",
    body_text: str = "Click the hamburger icon in the top right to reveal the off-screen navigation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6F86FF",     # CSS hex color for accent (e.g. the hamburger bars)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Morphing Hamburger & Off-Screen Slide Menu.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        nav_bg = "#161b22"
        menu_bg = "#222531"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        nav_bg = "#ffffff"
        menu_bg = "#e9ecef"

    # === CSS ===
    css = f"""/* Animated Hamburger & Off-screen Menu — generated component */
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
    --menu-bg: {menu_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Viewport Container (Simulating the window for demonstration) */
.viewport-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 8px;
}}

/* Navbar */
nav {{
    padding: 1rem 2rem;
    display: flex;
    background-color: var(--nav-bg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    text-decoration: none;
    line-height: 50px; /* Align with hamburger */
}}

/* Main Content Area */
main {{
    padding: 3rem 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* ===============================
   OFF-SCREEN MENU STYLES
   =============================== */
.off-screen-menu {{
    background-color: var(--menu-bg);
    height: 100%; /* Constrained to container for demo, normally 100vh */
    width: 100%;
    max-width: 450px;
    position: absolute; /* Using absolute for container demo, normally fixed */
    top: 0;
    right: -450px; /* Hidden by default */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: right .3s ease;
    z-index: 999;
}}

.off-screen-menu.active {{
    right: 0;
}}

.off-screen-menu ul {{
    list-style: none;
    text-align: center;
}}

.off-screen-menu li {{
    margin: 2rem 0;
}}

.off-screen-menu a {{
    color: var(--text);
    text-decoration: none;
    font-size: 3rem;
    font-weight: 600;
    transition: color 0.2s ease;
}}

.off-screen-menu a:hover {{
    color: var(--accent);
}}

/* ===============================
   HAMBURGER TOGGLE STYLES
   =============================== */
.ham-menu {{
    height: 50px;
    width: 50px;
    margin-left: auto;
    position: relative;
    cursor: pointer;
    z-index: 1000; /* Stays above the sliding menu */
}}

.ham-menu span {{
    height: 5px;
    width: 100%;
    background-color: var(--accent);
    border-radius: 25px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    transition: .3s ease;
}}

/* Default Positions */
.ham-menu span:nth-child(1) {{
    top: 25%;
}}
.ham-menu span:nth-child(2) {{
    top: 50%;
}}
.ham-menu span:nth-child(3) {{
    top: 75%;
}}

/* Active/Open Morphing Positions */
.ham-menu.active span:nth-child(1) {{
    top: 50%;
    transform: translate(-50%, -50%) rotate(45deg);
}}
.ham-menu.active span:nth-child(2) {{
    opacity: 0;
}}
.ham-menu.active span:nth-child(3) {{
    top: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="viewport-container">
        
        <!-- Off-Screen Navigation Menu -->
        <div class="off-screen-menu" id="nav-menu" role="dialog" aria-hidden="true">
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>

        <!-- Main Navbar -->
        <nav>
            <a href="#" class="logo">Brand.</a>
            <div class="ham-menu" role="button" aria-expanded="false" aria-controls="nav-menu" tabindex="0" aria-label="Toggle Navigation">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>

        <!-- Main Body Content -->
        <main>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Hamburger & Off-screen Menu — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamMenu = document.querySelector('.ham-menu');
    const offScreenMenu = document.querySelector('.off-screen-menu');

    // Function to toggle menu states
    const toggleMenu = () => {{
        const isActive = hamMenu.classList.toggle('active');
        offScreenMenu.classList.toggle('active');
        
        // Update accessibility attributes
        hamMenu.setAttribute('aria-expanded', isActive);
        offScreenMenu.setAttribute('aria-hidden', !isActive);
    }};

    // Mouse click event
    hamMenu.addEventListener('click', toggleMenu);

    // Keyboard accessibility (Enter or Space key)
    hamMenu.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            toggleMenu();
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
