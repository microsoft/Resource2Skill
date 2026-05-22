def create_component(
    output_dir: str,
    title_text: str = "Active Nav",
    body_text: str = "Click the links above to see the active state change dynamically.",
    color_scheme: str = "light",
    accent_color: str = "#000000",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Active Navigation Indicator.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Resolve colors based on scheme
    if color_scheme == "dark":
        text_color = "#f0f0f0"
        nav_bg = "rgba(0, 0, 0, 0.6)"
        hero_bg = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=2000" # Darker mountain/nature alternative
        active_text = "#ffffff"
    else:
        text_color = "#111111"
        nav_bg = "rgba(255, 255, 255, 0.8)"
        hero_bg = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2000" # Bright mountain peak
        active_text = "#ffffff"

    # === CSS ===
    css = f"""/* Vanilla JS Active Nav Indicator */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --text-default: {text_color};
    --text-active: {active_text};
    --nav-bg: {nav_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #333;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background: url('{hero_bg}') center/cover no-repeat;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    overflow: hidden;
}}

header {{
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 1.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}}

nav ul {{
    display: flex;
    list-style-type: none;
    justify-content: center;
    gap: 2rem;
}}

nav li a {{
    color: var(--text-default);
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 500;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
}}

/* Active State Styling */
nav li a.active {{
    background-color: var(--accent);
    color: var(--text-active);
}}

nav li a:hover:not(.active) {{
    opacity: 0.6;
}}

.content-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-title-box {{
    background: var(--nav-bg);
    backdrop-filter: blur(8px);
    padding: 3rem 6rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.page-title {{
    font-size: 5rem;
    font-weight: 800;
    color: var(--text-default);
    letter-spacing: -2px;
    margin-bottom: 1rem;
}}

.page-body {{
    font-size: 1.1rem;
    color: var(--text-default);
    opacity: 0.8;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#blog">Blog</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>

        <main class="content-area">
            <div class="page-title-box">
                <h1 class="page-title">Home</h1>
                <p class="page-body">{body_text}</p>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Dynamic Active Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    function setActivePage() {{
        // 1. Identify the current page.
        // NOTE: The tutorial uses `window.location.pathname` for multi-page sites.
        // For this single-file interactive demo, we use `window.location.hash` 
        // so you can click links and test the logic locally without a server.
        let activePage = window.location.hash || '#home';

        // 2. Select all navigation links
        const navLinks = document.querySelectorAll('nav a');

        // 3. Iterate over each link
        navLinks.forEach(link => {{
            
            // Clear existing active classes (necessary for this single-page simulation)
            link.classList.remove('active');

            // 4. Check if the link's href includes our current page identifier
            if (link.href.includes(activePage)) {{
                // 5. Apply the active styling class
                link.classList.add('active');
            }}
        }});

        // --- Demo specific: Update the visual UI card to reflect the "page change" ---
        const titleEl = document.querySelector('.page-title');
        if (titleEl) {{
            const pageName = activePage.replace('#', '');
            titleEl.textContent = pageName.charAt(0).toUpperCase() + pageName.slice(1);
        }}
    }}

    // Run immediately on page load
    setActivePage();

    // Re-run when the hash changes to simulate navigating to a new page
    window.addEventListener('hashchange', setActivePage);
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
