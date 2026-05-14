def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Welcome to your control panel. Here is a summary of your recent activity.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#4f46e5",     # Indigo accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Full-Height Dashboard Grid Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        sidebar_color = "#020617"
        border_color = "#334155"
    else:
        bg_color = "#f1f5f9"
        surface_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        sidebar_color = "#1e293b"
        border_color = "#e2e8f0"

    # === CSS ===
    css = f"""/* Dashboard Layout Component */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --sidebar-color: {sidebar_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background to frame the component */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.dashboard-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    color: var(--text-color);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    
    /* Core Layout Engine */
    display: grid;
    --sidebar-width: 5rem;
    grid-template-columns: var(--sidebar-width) 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
    transition: grid-template-columns 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.dashboard-container.sb-expand {{
    --sidebar-width: 16rem;
}}

/* Sidebar Elements */
.sidebar {{
    grid-area: sidebar;
    background-color: var(--sidebar-color);
    color: #fff;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 0;
    z-index: 10;
}}

.dashboard-container.sb-expand .sidebar {{
    align-items: flex-start;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}}

.logo-icon {{
    font-size: 2rem;
    line-height: 1;
    margin-bottom: 3rem;
    color: var(--accent-color);
}}

.logo-text {{
    display: none;
    font-size: 1.25rem;
    font-weight: 700;
    margin-left: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.dashboard-container.sb-expand .logo-icon {{
    display: inline-flex;
    align-items: center;
}}

.dashboard-container.sb-expand .logo-text {{
    display: inline-block;
    opacity: 1;
}}

.nav-placeholder {{
    width: 2rem;
    height: 2rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    margin-bottom: 1rem;
}}

.dashboard-container.sb-expand .nav-placeholder {{
    width: 100%;
    height: 2.5rem;
}}

/* Resize Button */
.resize-btn {{
    position: absolute;
    top: 5rem;
    right: -0.75rem;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    background-color: var(--accent-color);
    color: #fff;
    border: 2px solid var(--sidebar-color);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: bold;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 20;
}}

.dashboard-container.sb-expand .resize-btn {{
    transform: rotate(180deg);
}}

.resize-btn:hover {{
    transform: scale(1.1);
}}
.dashboard-container.sb-expand .resize-btn:hover {{
    transform: rotate(180deg) scale(1.1);
}}

/* Main Structure Areas */
.header {{
    grid-area: header;
    background-color: var(--surface-color);
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
}}

.header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.main {{
    grid-area: main;
    padding: 2rem;
    overflow-y: auto;
}}

.main > p {{
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.6;
}}

.footer {{
    grid-area: footer;
    background-color: var(--surface-color);
    padding: 1rem 2rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.875rem;
    color: var(--text-muted);
}}

/* Nested Card Grid demonstrating layout reflow */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.card-title {{
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

.card-value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-container">
        
        <aside class="sidebar">
            <div class="logo-icon">⬡<span class="logo-text">Brand</span></div>
            <div class="nav-placeholder"></div>
            <div class="nav-placeholder"></div>
            <div class="nav-placeholder"></div>
            
            <button id="resize" class="resize-btn" title="Toggle Sidebar">❯</button>
        </aside>
        
        <header class="header">
            <h1>{safe_title}</h1>
        </header>
        
        <main class="main">
            <p>{safe_body}</p>
            
            <div class="card-grid">
                <div class="card">
                    <div class="card-title">Total Users</div>
                    <div class="card-value">5.6K</div>
                </div>
                <div class="card">
                    <div class="card-title">Revenue</div>
                    <div class="card-value">$10.5K</div>
                </div>
                <div class="card">
                    <div class="card-title">Active Tasks</div>
                    <div class="card-value">12</div>
                </div>
                <div class="card">
                    <div class="card-title">Pending</div>
                    <div class="card-value">70</div>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            &copy; 2024 Dashboard Grid Architecture
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dashboard Layout Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const resizeBtn = document.getElementById('resize');
    const container = document.querySelector('.dashboard-container');

    // Toggle the sidebar expansion class
    resizeBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        container.classList.toggle('sb-expand');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
