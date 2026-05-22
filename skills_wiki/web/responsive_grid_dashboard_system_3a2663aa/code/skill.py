def create_component(
    output_dir: str,
    title_text: str = "Grid Architecture",
    body_text: str = "Responsive, dynamic dashboard using modern CSS Grid.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        border_color = "#334155"
        text_main = "#f8fafc"
        text_muted = "#94a3b8"
        hover_bg = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f1f5f9"
        surface_color = "#ffffff"
        border_color = "#cbd5e1"
        text_main = "#0f172a"
        text_muted = "#64748b"
        hover_bg = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Responsive Grid Dashboard System */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    padding: 1.5rem;
    container-type: inline-size;
}}

/* =========================================
   1. MACRO LAYOUT (Named Grid Areas)
   ========================================= */
.grid-dashboard {{
    display: grid;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
    grid-template-columns: 240px 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 1.5rem;
    height: 100%;
}}

.panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}}

.dashboard-header {{
    grid-area: header;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.dashboard-sidebar {{
    grid-area: sidebar;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.dashboard-footer {{
    grid-area: footer;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    color: var(--text-muted);
}}

.dashboard-content {{
    grid-area: main;
    overflow-y: auto;
    padding-right: 0.5rem;
}}

/* Custom Scrollbar */
.dashboard-content::-webkit-scrollbar {{ width: 6px; }}
.dashboard-content::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

/* =========================================
   2. MICRO LAYOUT (Auto-fit Fluid Grid)
   ========================================= */
.fluid-grid {{
    display: grid;
    /* The magic zero-media-query responsive rule */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    /* Implicit row sizing */
    grid-auto-rows: minmax(140px, auto);
    /* Fill empty spots caused by spanning */
    grid-auto-flow: dense;
    gap: 1.5rem;
}}

.card {{
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    cursor: pointer;
    animation: fadeUp 0.5s ease-out backwards;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

/* Grid Spanning */
.span-row {{ grid-row: span 2; }}

/* Container-aware Col Spanning */
@container (min-width: 600px) {{
    .span-col {{ grid-column: span 2; }}
    
    /* Interactive state */
    .card.expanded {{
        grid-column: span 2;
        grid-row: span 2;
        background: var(--hover-bg);
    }}
}}

/* =========================================
   3. GRID Z-INDEX LAYERING (No absolute pos)
   ========================================= */
.layered-card {{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    padding: 0; /* Let inner elements handle padding */
}}

.layered-card > * {{
    /* Both items occupy the exact same cell */
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.layered-card .base-content {{
    z-index: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.layered-badge {{
    z-index: 2;
    /* Grid alignment puts it in the corner */
    align-self: start;
    justify-self: end;
    /* Slight offset to overlap the corner */
    transform: translate(30%, -30%);
    
    background: var(--accent);
    color: #fff;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: 0 0 0 4px var(--bg); /* Cutout effect */
}}

/* Typography & Components */
h1, h2, h3 {{ font-weight: 600; line-height: 1.2; }}
.card-title {{ font-size: 1rem; color: var(--text-muted); }}
.card-stat {{ font-size: 2.5rem; font-weight: 700; color: var(--text); margin: 0.5rem 0; }}
.card-desc {{ font-size: 0.85rem; color: var(--text-muted); }}
.accent-text {{ color: var(--accent); }}

.nav-item {{
    padding: 12px 16px;
    border-radius: 8px;
    color: var(--text-muted);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.nav-item:hover {{ background: var(--hover-bg); color: var(--text); }}
.nav-item.active {{ background: var(--accent); color: #fff; }}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(15px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Container Query for Macro Layout Responsive Breakpoint */
@container (max-width: 800px) {{
    .grid-dashboard {{
        grid-template-areas:
            "header"
            "main"
            "footer";
        grid-template-columns: 1fr;
    }}
    .dashboard-sidebar {{ display: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="grid-dashboard">
            
            <!-- Dashboard Header -->
            <header class="dashboard-header panel">
                <h2>{title_text}</h2>
                <div class="card-desc">{body_text}</div>
            </header>
            
            <!-- Dashboard Sidebar -->
            <aside class="dashboard-sidebar panel">
                <div class="nav-item active">Overview</div>
                <div class="nav-item">Analytics</div>
                <div class="nav-item">Campaigns</div>
                <div class="nav-item">Settings</div>
            </aside>
            
            <!-- Dashboard Main Content (Fluid Grid) -->
            <main class="dashboard-content">
                <div class="fluid-grid">
                    
                    <div class="card panel span-row" style="animation-delay: 0.0s">
                        <h3 class="card-title">Active Users</h3>
                        <div class="card-stat">24.5k</div>
                        <div class="card-desc accent-text">↑ 14% vs last week</div>
                        <div style="flex-grow: 1; background: var(--hover-bg); border-radius: 8px; margin-top: 1rem;"></div>
                    </div>
                    
                    <!-- Grid Z-Index Layering Card -->
                    <div class="layered-card panel" style="animation-delay: 0.1s">
                        <div class="base-content">
                            <h3 class="card-title">Total Revenue</h3>
                            <div class="card-stat">$84,300</div>
                            <div class="card-desc">Current month</div>
                        </div>
                        <div class="layered-badge">New Record</div>
                    </div>
                    
                    <div class="card panel" style="animation-delay: 0.2s">
                        <h3 class="card-title">Server Status</h3>
                        <div class="card-stat" style="color: #10b981;">99.9%</div>
                        <div class="card-desc">All systems operational</div>
                    </div>

                    <div class="card panel span-col" style="animation-delay: 0.3s">
                        <h3 class="card-title">Network Traffic</h3>
                        <div class="card-stat">1.2 TB <span style="font-size: 1rem; color: var(--text-muted);">/ sec</span></div>
                        <div class="card-desc">Global routing active. Click me to test auto-flow: dense!</div>
                    </div>
                    
                    <div class="card panel" style="animation-delay: 0.4s">
                        <h3 class="card-title">Conversion Rate</h3>
                        <div class="card-stat">3.8%</div>
                        <div class="card-desc accent-text">↑ 0.5% vs last week</div>
                    </div>

                    <div class="card panel" style="animation-delay: 0.5s">
                        <h3 class="card-title">Bounce Rate</h3>
                        <div class="card-stat">42.1%</div>
                        <div class="card-desc">Holding steady</div>
                    </div>

                </div>
            </main>
            
            <!-- Dashboard Footer -->
            <footer class="dashboard-footer panel">
                &copy; 2024 CSS Grid Layout Architecture. Grid areas make layout declarative.
            </footer>
            
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Grid Dashboard Interactive Logic
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {{
        card.addEventListener('click', () => {{
            // Toggle the .expanded class
            // This leverages 'grid-auto-flow: dense' in the CSS.
            // As the card spans 2x2, the grid will automatically backfill 
            // the empty slots with smaller surrounding cards.
            card.classList.toggle('expanded');
        }});
    }});
}});
"""

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
