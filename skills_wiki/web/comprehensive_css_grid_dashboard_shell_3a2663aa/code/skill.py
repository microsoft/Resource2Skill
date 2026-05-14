def create_component(
    output_dir: str,
    title_text: str = "GridMaster Dashboard",
    body_text: str = "A comprehensive demonstration of CSS Grid features.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_alt = "rgba(255, 255, 255, 0.02)"
        border_color = "rgba(255, 255, 255, 0.08)"
        text_color = "#f8f9fa"
        text_muted = "rgba(255, 255, 255, 0.5)"
    else:
        bg_color = "#f1f3f5"
        surface_color = "#ffffff"
        surface_alt = "#f8f9fa"
        border_color = "rgba(0, 0, 0, 0.08)"
        text_color = "#121212"
        text_muted = "rgba(0, 0, 0, 0.5)"

    # === CSS ===
    css = f"""/* Comprehensive CSS Grid Layout */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-alt: {surface_alt};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
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
    padding: 1rem;
}}

/* 1. Macro Layout: explicit areas */
.app-layout {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    
    display: grid;
    grid-template-columns: 240px 1fr;
    grid-template-rows: 64px 1fr 48px;
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
}}

.header {{
    grid-area: header;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.logo span {{
    color: var(--accent);
}}

/* Feature: Explicit Placement & Alignment */
.floating-badge {{
    grid-area: header;
    justify-self: end;
    align-self: center;
    background: var(--accent);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: bold;
    text-transform: uppercase;
    margin-right: 1.5rem;
}}

.sidebar {{
    grid-area: sidebar;
    background: var(--surface-alt);
    border-right: 1px solid var(--border);
    padding: 1.5rem;
}}

.nav-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.nav-item {{
    padding: 0.6rem 1rem;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s;
}}

.nav-item:hover {{
    background: var(--surface);
    color: var(--text);
}}

.nav-item.active {{
    background: var(--accent);
    color: white;
}}

.footer {{
    grid-area: footer;
    background: var(--surface);
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    color: var(--text-muted);
}}

.main-content {{
    grid-area: main;
    overflow-y: auto;
    padding: 2rem;
}}

.header-text {{
    margin-bottom: 2rem;
}}

.header-text h2 {{
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.header-text p {{
    color: var(--text-muted);
    font-size: 1rem;
}}

/* 2. Micro Layout: Zero-media-query auto-fit grid */
.widget-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    grid-auto-rows: 150px;
    gap: 1.25rem;
    grid-auto-flow: dense;
}}

.widget {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
}}

.widget:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}}

.widget h3 {{
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
}}

.widget p {{
    color: var(--text-muted);
    font-size: 0.9rem;
}}

/* Feature: Spanning */
.widget-wide {{
    grid-column: span 2;
}}

.widget-tall {{
    grid-row: span 2;
}}

/* Feature: Explicit Alignment within a cell */
.widget-aligned {{
    display: grid;
    place-items: center;
    text-align: center;
}}

.widget-aligned .icon {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

/* Feature: Z-axis Layering via Grid Lines */
.widget-layered {{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    padding: 0;
    border: none;
    overflow: hidden;
    color: white;
}}

.widget-layered > * {{
    /* Places all direct children perfectly overlapping in the single grid cell */
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.layer-bg {{
    background: linear-gradient(135deg, var(--accent) 0%, #ff007f 100%);
    opacity: 0.85;
    z-index: 1;
    transition: transform 0.5s ease;
}}

.widget-layered:hover .layer-bg {{
    transform: scale(1.05);
}}

.layer-content {{
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem;
}}

.layer-content h3 {{
    font-size: 1.4rem;
}}

/* Responsive Overrides */
@media (max-width: 800px) {{
    .app-layout {{
        grid-template-columns: 1fr;
        grid-template-rows: 64px auto 1fr 48px;
        grid-template-areas:
            "header"
            "sidebar"
            "main"
            "footer";
    }}
    
    .sidebar {{
        border-right: none;
        border-bottom: 1px solid var(--border);
    }}
    
    .nav-list {{
        flex-direction: row;
        flex-wrap: wrap;
    }}
}}

@media (max-width: 550px) {{
    /* Prevent spanning widgets from blowing out the auto-fit columns on tiny screens */
    .widget-wide, .widget-tall {{
        grid-column: span 1;
        grid-row: span 1;
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
        <header class="header">
            <div class="logo">Grid<span>Master</span></div>
        </header>
        
        <!-- Explicit Grid Area Placed Element -->
        <div class="floating-badge">Pro</div>
        
        <aside class="sidebar">
            <ul class="nav-list" role="navigation">
                <li class="nav-item active" aria-current="page" tabindex="0">Overview</li>
                <li class="nav-item" tabindex="0">Analytics</li>
                <li class="nav-item" tabindex="0">Settings</li>
            </ul>
        </aside>
        
        <main class="main-content">
            <div class="header-text">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>
            
            <div class="widget-grid">
                
                <!-- Layering & Spanning Demo -->
                <div class="widget widget-wide widget-layered">
                    <div class="layer-bg"></div>
                    <div class="layer-content">
                        <h3>Layered Layout</h3>
                        <p>Overlapping using 1 / -1</p>
                    </div>
                </div>
                
                <!-- Spanning Demo -->
                <div class="widget widget-tall">
                    <h3>Tall Widget</h3>
                    <p>grid-row: span 2</p>
                </div>
                
                <!-- Explicit Alignment Demo -->
                <div class="widget widget-aligned">
                    <div class="icon">📦</div>
                    <h3>Centered</h3>
                    <p>place-items: center</p>
                </div>
                
                <!-- Standard Auto-fit Demo -->
                <div class="widget">
                    <h3>Auto Grid 1</h3>
                    <p>Flows naturally</p>
                </div>
                
                <div class="widget">
                    <h3>Auto Grid 2</h3>
                    <p>Resizes seamlessly</p>
                </div>
                
                <div class="widget widget-wide">
                    <h3>Wide Widget</h3>
                    <p>grid-column: span 2</p>
                </div>
                
            </div>
        </main>
        
        <footer class="footer">
            Designed with core CSS Grid mechanics
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Minimal interaction to demonstrate a living component
document.addEventListener('DOMContentLoaded', () => {{
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {{
        item.addEventListener('click', () => {{
            // Remove active states
            navItems.forEach(nav => {{
                nav.classList.remove('active');
                nav.removeAttribute('aria-current');
            }});
            
            // Add active state to clicked item
            item.classList.add('active');
            item.setAttribute('aria-current', 'page');
        }});
        
        // Allow keyboard navigation for accessibility
        item.addEventListener('keydown', (e) => {{
            if(e.key === 'Enter' || e.key === ' ') {{
                e.preventDefault();
                item.click();
            }}
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
