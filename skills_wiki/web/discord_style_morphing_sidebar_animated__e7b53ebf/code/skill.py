def create_component(
    output_dir: str,
    title_text: str = "Morphing Sidebar Navigation",
    body_text: str = "Hover over the icons on the left to experience the shape-morphing transition and animated tooltips.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3ba55d",     # Default is Discord-style green
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Discord-style Morphing Sidebar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on scheme ===
    if color_scheme == "dark":
        sidebar_bg = "#202225"
        icon_bg = "#36393f"
        icon_hover_text = "#ffffff"
        tooltip_bg = "#18191c"
        tooltip_text = "#ffffff"
        page_bg = "#2f3136"
        text_main = "#dcddde"
    else:
        sidebar_bg = "#e3e5e8"
        icon_bg = "#ffffff"
        icon_hover_text = "#ffffff"
        tooltip_bg = "#18191c"
        tooltip_text = "#ffffff"
        page_bg = "#f2f3f5"
        text_main = "#2e3338"

    # === CSS ===
    css = f"""/* Discord-Style Morphing Sidebar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --sidebar-bg: {sidebar_bg};
    --icon-bg: {icon_bg};
    --icon-color: {accent_color};
    --icon-hover-bg: {accent_color};
    --icon-hover-text: {icon_hover_text};
    --tooltip-bg: {tooltip_bg};
    --tooltip-text: {tooltip_text};
    --page-bg: {page_bg};
    --text-main: {text_main};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.app-window {{
    width: var(--width);
    height: var(--height);
    background: var(--page-bg);
    position: relative;
    display: flex;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    overflow: hidden;
    border-radius: 8px;
}}

/* Sidebar Layout */
.sidebar {{
    width: 72px;
    height: 100%;
    background-color: var(--sidebar-bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 12px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    z-index: 10;
}}

/* Morphing Icon Container */
.sidebar-item {{
    position: relative;
    width: 48px;
    height: 48px;
    margin-bottom: 12px;
    background-color: var(--icon-bg);
    color: var(--icon-color);
    border-radius: 50%; /* Starts as a circle */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    
    /* Smooth transition for shape, color, and background */
    transition: all 0.3s linear;
}}

/* Active/Hover State for Icon Container */
.sidebar-item:hover,
.sidebar-item.active {{
    border-radius: 16px; /* Morphs into a rounded square */
    background-color: var(--icon-hover-bg);
    color: var(--icon-hover-text);
}}

.sidebar-icon {{
    font-size: 20px;
    transition: color 0.3s linear;
}}

/* Separator Line */
.sidebar-separator {{
    height: 2px;
    width: 32px;
    background-color: var(--icon-bg);
    border-radius: 1px;
    margin: 4px 0 12px 0;
}}

/* Animated Tooltip */
.sidebar-tooltip {{
    position: absolute;
    left: 64px; /* Pushed outside the sidebar */
    background-color: var(--tooltip-bg);
    color: var(--tooltip-text);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    pointer-events: none; /* Prevents tooltip from blocking cursor */
    
    /* Animation initial state */
    transform: scale(0);
    transform-origin: left center;
    transition: transform 0.1s linear;
    z-index: 100;
}}

/* Tooltip Arrow */
.sidebar-tooltip::before {{
    content: '';
    position: absolute;
    top: 50%;
    right: 100%;
    transform: translateY(-50%);
    border-width: 5px;
    border-style: solid;
    border-color: transparent var(--tooltip-bg) transparent transparent;
}}

/* Show Tooltip on Parent Hover */
.sidebar-item:hover .sidebar-tooltip {{
    transform: scale(1);
}}

/* Main Content Area */
.content {{
    flex: 1;
    padding: 40px;
    overflow-y: auto;
}}

.content h1 {{
    font-size: 28px;
    margin-bottom: 16px;
    color: var(--text-main);
}}

.content p {{
    font-size: 16px;
    line-height: 1.6;
    opacity: 0.8;
}}
"""

    # === HTML ===
    # Escaping variables to prevent basic HTML breaking
    safe_title = title_text.replace("<", "&lt;").replace(">", "&gt;")
    safe_body = body_text.replace("<", "&lt;").replace(">", "&gt;")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <!-- FontAwesome for standard icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Inter Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-window">
        <!-- Sidebar Component -->
        <nav class="sidebar">
            <div class="sidebar-item" data-id="home">
                <i class="fa-brands fa-discord sidebar-icon"></i>
                <span class="sidebar-tooltip">Home</span>
            </div>
            
            <div class="sidebar-separator"></div>
            
            <div class="sidebar-item" data-id="fire">
                <i class="fa-solid fa-fire sidebar-icon"></i>
                <span class="sidebar-tooltip">Trending</span>
            </div>
            
            <div class="sidebar-item" data-id="plus">
                <i class="fa-solid fa-plus sidebar-icon"></i>
                <span class="sidebar-tooltip">Add Server</span>
            </div>
            
            <div class="sidebar-item" data-id="bolt">
                <i class="fa-solid fa-bolt sidebar-icon"></i>
                <span class="sidebar-tooltip">Quick Actions</span>
            </div>
            
            <div class="sidebar-item" data-id="download">
                <i class="fa-solid fa-download sidebar-icon"></i>
                <span class="sidebar-tooltip">Download Apps</span>
            </div>
        </nav>
        
        <!-- App Content -->
        <main class="content">
            <h1 id="page-title">{safe_title}</h1>
            <p id="page-content">{safe_body}</p>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sidebar interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const pageTitle = document.getElementById('page-title');
    
    // Optional: Add click behavior to show active states
    sidebarItems.forEach(item => {{
        item.addEventListener('click', () => {{
            // Remove active class from all
            sidebarItems.forEach(el => el.classList.remove('active'));
            
            // Add active class to clicked
            item.classList.add('active');
            
            // Update page content dynamically for demo purposes
            const tooltipText = item.querySelector('.sidebar-tooltip').textContent;
            pageTitle.textContent = tooltipText + ' Section';
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
