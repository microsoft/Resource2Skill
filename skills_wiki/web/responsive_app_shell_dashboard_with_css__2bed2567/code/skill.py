def create_component(
    output_dir: str,
    title_text: str = "Welcome to the Dashboard",
    body_text: str = "This is the main content area. Resize the window to see the responsive behavior.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#3498db",     # CSS hex color for accent (e.g., active link)
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Dashboard Layout visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        sidebar_bg = "#1a1a2e"
        sidebar_text = "#ffffff"
        main_bg = "#16213e"
        main_text = "#e6e6e6"
        hover_bg = "rgba(255, 255, 255, 0.1)"
    else:
        sidebar_bg = "#2c3e50"
        sidebar_text = "#ffffff"
        main_bg = "#f4f6f8"
        main_text = "#333333"
        hover_bg = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Responsive App Shell Dashboard — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --sidebar-bg: {sidebar_bg};
    --sidebar-text: {sidebar_text};
    --main-bg: {main_bg};
    --main-text: {main_text};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #e0e0e0; /* Neutral background outside the component container */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The main application container */
.app-shell {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--main-bg);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border-radius: 8px;
    overflow: hidden;
    
    /* CORE CSS GRID LOGIC */
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: 100%;
    grid-template-areas: 'sidebar main';
}}

/* Sidebar specific styles */
.sidebar {{
    grid-area: sidebar;
    background-color: var(--sidebar-bg);
    color: var(--sidebar-text);
    padding: 24px 0;
    display: flex;
    flex-direction: column;
}}

.sidebar-header {{
    padding: 0 24px 24px 24px;
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 16px;
}}

.nav-list {{
    list-style: none;
}}

.nav-link {{
    display: block;
    padding: 12px 24px;
    color: var(--sidebar-text);
    text-decoration: none;
    font-size: 0.95rem;
    transition: background-color 0.2s ease, border-left 0.2s ease;
    border-left: 3px solid transparent;
}}

.nav-link:hover {{
    background-color: var(--hover-bg);
}}

.nav-link.active {{
    background-color: var(--hover-bg);
    border-left-color: var(--accent);
    font-weight: 500;
}}

/* Main content specific styles */
.main-content {{
    grid-area: main;
    background-color: var(--main-bg);
    color: var(--main-text);
    padding: 32px;
    overflow-y: auto;
}}

.main-content h1 {{
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 12px;
}}

.main-content p {{
    font-size: 1rem;
    line-height: 1.6;
    color: inherit;
    opacity: 0.8;
}}

/* RESPONSIVE LOGIC */
/* Simulating mobile view within the defined container width, or falling back to window width */
@media (max-width: 768px), (max-width: 1000px) and (max-aspect-ratio: 4/5) {{
    .app-shell {{
        /* Switch to stacked layout */
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr;
        grid-template-areas: 
            'sidebar'
            'main';
    }}
    
    .sidebar {{
        padding: 16px 0;
    }}
    
    .sidebar-header {{
        padding: 0 16px 16px 16px;
        margin-bottom: 8px;
    }}
    
    .nav-list {{
        display: flex;
        flex-wrap: wrap;
        padding: 0 8px;
    }}
    
    .nav-link {{
        padding: 8px 16px;
        border-left: none;
        border-bottom: 2px solid transparent;
        border-radius: 4px;
        margin-right: 4px;
    }}
    
    .nav-link.active {{
        border-left-color: transparent;
        border-bottom-color: var(--accent);
    }}
}}
"""

    # === HTML ===
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-shell">
        <aside class="sidebar">
            <div class="sidebar-header">
                Dashboard
            </div>
            <nav>
                <ul class="nav-list">
                    <li><a href="#" class="nav-link active">Home</a></li>
                    <li><a href="#" class="nav-link">Reports</a></li>
                    <li><a href="#" class="nav-link">Analytics</a></li>
                    <li><a href="#" class="nav-link">Settings</a></li>
                </ul>
            </nav>
        </aside>
        
        <main class="main-content">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Basic interactive behavior for sidebar links
document.addEventListener('DOMContentLoaded', () => {{
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault(); // Prevent jump to top
            
            // Remove active class from all
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked
            e.target.classList.add('active');
        }});
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
