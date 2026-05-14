def create_component(
    output_dir: str,
    title_text: str = "Dashboard",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#0ea5e9",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid App Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        nav_bg = "#1e293b"
        sidebar_bg = "#1e293b"
        border_color = "#334155"
        footer_bg = "#020617"
        hover_bg = "rgba(14, 165, 233, 0.15)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        nav_bg = "#ffffff"
        sidebar_bg = "#ffffff"
        border_color = "#e2e8f0"
        footer_bg = "#f1f5f9"
        hover_bg = "rgba(14, 165, 233, 0.1)"

    # Generate dummy content to force scroll capability for testing sticky logic
    dummy_blocks = "\n".join(['<div class="dummy-block"></div>' for _ in range(8)])
    paragraphs = "\n".join([f"<p>{body_text}</p>" for _ in range(6)])

    # === CSS ===
    css = f"""/* Responsive App Layout — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --nav-bg: {nav_bg};
    --sidebar-bg: {sidebar_bg};
    --border: {border_color};
    --footer-bg: {footer_bg};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    
    --nav-height: 64px;
    --sidebar-width: 260px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* For component preview constraints */
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    margin: 0 auto;
    overflow-y: auto;
    overflow-x: hidden;
}}

/* Core CSS Grid Layout */
.app-layout {{
    display: grid;
    min-height: 100%;
    grid-template-columns: var(--sidebar-width) 1fr;
    grid-template-rows: var(--nav-height) 1fr auto;
    grid-template-areas:
        "navbar navbar"
        "sidebar main"
        "sidebar footer";
}}

/* Navbar Styling */
.navbar {{
    grid-area: navbar;
    position: sticky;
    top: 0;
    z-index: 50;
    background-color: var(--nav-bg);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.nav-brand {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--accent);
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    margin-left: 1.5rem;
    font-weight: 500;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.menu-toggle {{
    display: none;
    background: transparent;
    border: none;
    color: var(--text);
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: background-color 0.2s;
}}

.menu-toggle:hover {{
    background-color: var(--hover-bg);
}}

.menu-toggle svg {{
    width: 24px;
    height: 24px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}}

/* Sidebar Styling & Sticky Logic */
.sidebar {{
    grid-area: sidebar;
    position: sticky;
    top: var(--nav-height);
    /* Calculate height explicitly so it fills the viewport exactly, allowing sticky to slide correctly */
    height: calc(100vh - var(--nav-height));
    align-self: start;
    
    background-color: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 1.5rem 0;
    z-index: 40;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.sidebar-menu {{
    list-style: none;
}}

.sidebar-menu li a {{
    display: flex;
    align-items: center;
    padding: 0.875rem 1.5rem;
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
    border-left: 3px solid transparent;
}}

.sidebar-menu li a svg {{
    margin-right: 12px;
    opacity: 0.7;
    transition: opacity 0.2s;
}}

.sidebar-menu li a:hover,
.sidebar-menu li a.active {{
    background-color: var(--hover-bg);
    color: var(--accent);
    border-left-color: var(--accent);
}}

.sidebar-menu li a:hover svg,
.sidebar-menu li a.active svg {{
    opacity: 1;
}}

/* Main Content Styling */
.main-content {{
    grid-area: main;
    padding: 2rem 2.5rem;
}}

.main-content h1 {{
    margin-bottom: 1.5rem;
    font-size: 2rem;
    font-weight: 600;
}}

.main-content p {{
    margin-bottom: 1.25rem;
    line-height: 1.6;
    color: color-mix(in srgb, var(--text) 85%, transparent);
}}

/* Footer Styling */
.footer {{
    grid-area: footer;
    background-color: var(--footer-bg);
    border-top: 1px solid var(--border);
    padding: 1.5rem 2.5rem;
    text-align: center;
    font-size: 0.875rem;
    color: color-mix(in srgb, var(--text) 60%, transparent);
}}

/* Dummy visual blocks for scroll demonstration */
.dummy-blocks {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}}
.dummy-block {{
    height: 160px;
    background-color: var(--sidebar-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
}}

/* Responsive Breakpoint */
@media (max-width: 800px) {{
    .app-layout {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "navbar"
            "main"
            "footer";
    }}

    .menu-toggle {{
        display: block;
    }}

    .nav-links {{
        display: none;
    }}

    .sidebar {{
        position: fixed;
        top: var(--nav-height);
        left: 0;
        width: var(--sidebar-width);
        /* Hide off-canvas by default */
        transform: translateX(-100%);
        box-shadow: 4px 0 24px rgba(0,0,0,0.15);
    }}

    /* JS toggled class */
    .sidebar.show {{
        transform: translateX(0);
    }}
    
    .main-content {{
        padding: 1.5rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-layout">
        <!-- Sticky Navbar -->
        <nav class="navbar">
            <div class="nav-brand">
                <button class="menu-toggle" id="menuToggle" aria-label="Toggle Menu">
                    <svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"></path></svg>
                </button>
                <span>AppLogo</span>
            </div>
            <div class="nav-links">
                <a href="#">Overview</a>
                <a href="#">Activity</a>
                <a href="#">Support</a>
            </div>
        </nav>

        <!-- Sticky Sidebar -->
        <aside class="sidebar" id="sidebar">
            <ul class="sidebar-menu">
                <li>
                    <a href="#" class="active">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                        {title_text}
                    </a>
                </li>
                <li>
                    <a href="#">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                        Projects
                    </a>
                </li>
                <li>
                    <a href="#">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                        Team
                    </a>
                </li>
                <li>
                    <a href="#">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                        Settings
                    </a>
                </li>
            </ul>
        </aside>

        <!-- Main Fluid Area -->
        <main class="main-content">
            <h1>{title_text}</h1>
            {paragraphs}
            <div class="dummy-blocks">
                {dummy_blocks}
            </div>
        </main>

        <!-- Fluid Footer -->
        <footer class="footer">
            <p>&copy; 2024 AppLogo Inc. All rights reserved. CSS Grid App Layout Strategy.</p>
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Toggle Mobile Sidebar
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');

    if (sidebar && menuToggle) {{
        // Toggle 'show' class to trigger CSS transform
        menuToggle.addEventListener('click', () => {{
            sidebar.classList.toggle('show');
        }});
        
        // Optional UX: Close sidebar if clicking outside of it on mobile
        document.addEventListener('click', (e) => {{
            if (window.innerWidth <= 800) {{
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {{
                    sidebar.classList.remove('show');
                }}
            }}
        }});
    }}
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
