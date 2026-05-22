def create_component(
    output_dir: str,
    title_text: str = "GridMaster Dashboard",
    body_text: str = "Responsive CSS Grid architecture utilizing areas, auto-fit tracks, and overlapping cells.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent (e.g., blue)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid App Shell & Auto-Fit Gallery.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        surface_border = "#334155"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        surface_color = "#ffffff"
        surface_border = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "#64748b"

    # Parse accent color for RGB usage (needed for opacity layers)
    accent_hex = accent_color.lstrip('#')
    if len(accent_hex) == 3:
        accent_hex = ''.join(c + c for c in accent_hex)
    accent_r, accent_g, accent_b = tuple(int(accent_hex[i:i+2], 16) for i in (0, 2, 4))

    # === CSS ===
    css = f"""/* CSS Grid Layout Patterns */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-border: {surface_border};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --accent-rgb: {accent_r}, {accent_g}, {accent_b};
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
    padding: 20px;
}}

/* =========================================
   1. MACRO LAYOUT: CSS Grid App Shell
========================================= */
.app-shell {{
    display: grid;
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: calc(100vh - 40px);
    
    /* Defines the structural map of the app */
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
        
    /* Track sizing */
    grid-template-rows: 64px 1fr 48px;
    grid-template-columns: 240px 1fr;
    
    /* The Gap Border Trick: The gap reveals the parent's background color, 
       creating clean 1px borders between all grid areas automatically */
    gap: 1px; 
    background-color: var(--surface-border);
    border: 1px solid var(--surface-border);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Map elements to their respective areas */
.header {{ grid-area: header; }}
.sidebar {{ grid-area: sidebar; }}
.main {{ grid-area: main; overflow-y: auto; overflow-x: hidden; }}
.footer {{ grid-area: footer; }}

/* Fill cells with surface color to complete the border trick */
.header, .sidebar, .main, .footer {{
    background-color: var(--surface);
}}

/* Shell Component Styling */
.header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.sidebar {{
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.menu-item {{
    padding: 10px 16px;
    border-radius: 6px;
    color: var(--text-muted);
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.menu-item:hover, .menu-item.active {{
    background-color: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
}}

.main {{
    padding: 32px;
    background-color: var(--bg); /* Override surface for depth */
}}

.footer {{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    color: var(--text-muted);
}}

/* =========================================
   2. MICRO LAYOUT: Responsive Auto-Fit Grid
========================================= */
.auto-grid {{
    display: grid;
    /* The ultimate fluid pattern: automatically creates as many columns 
       as will fit, at a minimum of 220px, stretching to fill remainder (1fr) */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-top: 32px;
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 10px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

/* =========================================
   3. GRID LAYERING DEMO
========================================= */
.card-layer-demo {{
    display: grid;
    /* Create a single shared area */
    grid-template-areas: "overlap"; 
    height: 120px;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 8px;
    border: 1px solid var(--surface-border);
    background-color: var(--bg);
}}

/* Assign multiple elements to the exact same area */
.layer-bg {{
    grid-area: overlap;
    background: linear-gradient(135deg, var(--accent) 0%, transparent 100%);
    opacity: 0.15;
}}

.layer-img {{
    grid-area: overlap;
    background-image: repeating-linear-gradient(45deg, var(--surface-border) 0, var(--surface-border) 2px, transparent 2px, transparent 12px);
    opacity: 0.3;
}}

.layer-content {{
    grid-area: overlap;
    place-self: center; /* Grid shorthand for align-self & justify-self */
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--accent);
    z-index: 10;
}}

/* Typographic & Icon Styles */
h1 {{ font-size: 1.8rem; font-weight: 700; color: var(--text); letter-spacing: -0.5px; }}
h3 {{ font-size: 1.1rem; font-weight: 600; color: var(--text); }}
p {{ line-height: 1.6; }}
.text-muted {{ color: var(--text-muted); font-size: 0.95rem; }}
.accent-text {{ color: var(--accent); }}

.card-icon {{
    font-size: 1.5rem;
    height: 48px;
    width: 48px;
    display: grid;
    place-items: center; /* Quick alignment */
    background: rgba(var(--accent-rgb), 0.1);
    border-radius: 8px;
    margin-bottom: 8px;
}}

/* =========================================
   4. RESPONSIVE FALLBACKS
========================================= */
@media (max-width: 768px) {{
    .app-shell {{
        /* Rearrange the macro-layout for mobile view */
        grid-template-areas:
            "header"
            "main"
            "sidebar"
            "footer";
        grid-template-rows: 64px 1fr auto 48px;
        grid-template-columns: 1fr;
    }}
    
    .sidebar {{
        flex-direction: row;
        overflow-x: auto;
        padding: 12px 16px;
        border-right: none;
        border-top: 1px solid var(--surface-border);
    }}
    
    .menu-item {{
        white-space: nowrap;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-shell">
        <header class="header">
            <div class="logo"><span class="accent-text">Grid</span>Master</div>
        </header>
        
        <aside class="sidebar">
            <div class="menu-item active">Grid Overview</div>
            <div class="menu-item">Track Sizing</div>
            <div class="menu-item">Alignment</div>
            <div class="menu-item">Implicit Grids</div>
        </aside>
        
        <main class="main">
            <div class="main-header">
                <h1 class="title">{title_text}</h1>
                <p class="text-muted" style="margin-top: 8px;">{body_text}</p>
            </div>
            
            <div class="auto-grid">
                <!-- Card 1 -->
                <div class="card">
                    <div class="card-icon">🗺️</div>
                    <h3>Grid Areas</h3>
                    <p class="text-muted">Macro-layout uses named areas (header, sidebar, main, footer) to map the UI structure cleanly.</p>
                </div>
                
                <!-- Card 2 -->
                <div class="card">
                    <div class="card-layer-demo">
                        <div class="layer-img"></div>
                        <div class="layer-bg"></div>
                        <div class="layer-content">Grid Stacking</div>
                    </div>
                    <h3>Layering Items</h3>
                    <p class="text-muted">Place multiple elements in the same grid cell using <code>grid-area</code>. No absolute positioning needed.</p>
                </div>
                
                <!-- Card 3 -->
                <div class="card">
                    <div class="card-icon">🪄</div>
                    <h3>Auto-Fit Magic</h3>
                    <p class="text-muted">This gallery utilizes <code>repeat(auto-fit, minmax(...))</code>. Cards reflow automatically without media queries.</p>
                </div>
                
                <!-- Card 4 -->
                <div class="card">
                    <div class="card-icon">📏</div>
                    <h3>Fractional Units</h3>
                    <p class="text-muted">Columns are sized using <code>1fr</code>, dynamically taking up a specific fraction of the available free space.</p>
                </div>
                
                <!-- Card 5 -->
                <div class="card">
                    <div class="card-icon">🎯</div>
                    <h3>Alignment Controls</h3>
                    <p class="text-muted">Achieve precise positioning using <code>place-items</code> or <code>place-self</code> to center elements along both axes instantly.</p>
                </div>
                
                <!-- Card 6 -->
                <div class="card">
                    <div class="card-icon">✨</div>
                    <h3>Grid Gap</h3>
                    <p class="text-muted">Create consistent spacing between elements using the <code>gap</code> property. Say goodbye to complex margin math.</p>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            <p>Responsive CSS Grid App Shell Pattern</p>
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Simple interaction for the Sidebar menu state
document.addEventListener('DOMContentLoaded', () => {{
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {{
        item.addEventListener('click', () => {{
            // Remove active class from all
            menuItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            item.classList.add('active');
        }});
    }});
}});
"""

    # Write files
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
