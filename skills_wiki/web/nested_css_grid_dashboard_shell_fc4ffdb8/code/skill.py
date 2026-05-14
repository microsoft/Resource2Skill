def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Welcome back. Here is your daily summary and analytics breakdown.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Nested CSS Grid Dashboard Shell.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        sidebar_bg = "#0f172a"
        header_bg = "#1e293b"
        main_bg = "#020617"
        card_bg = "#1e293b"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        border_color = "#334155"
    else:
        sidebar_bg = "#1c1f23"
        header_bg = "#ffffff"
        main_bg = "#e2e8f0"
        card_bg = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        border_color = "#cbd5e1"

    # === CSS ===
    css = f"""/* Nested CSS Grid Dashboard Shell */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --sidebar-bg: {sidebar_bg};
    --header-bg: {header_bg};
    --main-bg: {main_bg};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Backdrop if component is smaller than viewport */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Macro Layout: Application Shell */
.app-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--main-bg);
    
    display: grid;
    grid-template-columns: 280px 1fr;
    grid-template-rows: 70px 1fr;
    grid-template-areas:
        "sidebar header"
        "sidebar main";
    
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Shell Components */
.sidebar {{
    grid-area: sidebar;
    background: var(--sidebar-bg);
    color: #fff;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 32px;
}}

.logo {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 12px;
}}

.logo::before {{
    content: '';
    display: block;
    width: 24px;
    height: 24px;
    background: var(--accent);
    border-radius: 6px;
}}

.nav-placeholder {{
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.nav-item {{
    height: 32px;
    background: rgba(255,255,255,0.05);
    border-radius: 6px;
    width: 80%;
}}

.header {{
    grid-area: header;
    background: var(--header-bg);
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    color: var(--text-primary);
}}

.header h2 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

/* Micro Layout: Nested Main Grid */
.main-content {{
    grid-area: main;
    padding: 32px;
    overflow-y: auto;
    
    /* Inner Grid setup */
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 24px;
    
    /* The Magic: Asymmetric Bento Box Mapping */
    grid-template-areas:
        "c1 c2 c3"
        "c4 c4 c5"
        "c4 c4 c6";
}}

/* Card Elements */
.card {{
    background: var(--card-bg);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid var(--border);
    color: var(--text-primary);
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}}

.card-title {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.card-value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
}}

/* Assigning specific cards to their designated areas */
.card:nth-child(1) {{ grid-area: c1; }}
.card:nth-child(2) {{ grid-area: c2; }}
.card:nth-child(3) {{ grid-area: c3; }}
.card:nth-child(4) {{ grid-area: c4; background: linear-gradient(135deg, var(--card-bg), rgba(59, 130, 246, 0.05)); }}
.card:nth-child(5) {{ grid-area: c5; }}
.card:nth-child(6) {{ grid-area: c6; }}

/* Inside the large card to make it look like a chart placeholder */
.chart-placeholder {{
    flex: 1;
    background: repeating-linear-gradient(
        45deg,
        rgba(0,0,0,0.02),
        rgba(0,0,0,0.02) 10px,
        rgba(0,0,0,0.04) 10px,
        rgba(0,0,0,0.04) 20px
    );
    border-radius: 8px;
    border: 1px dashed var(--border);
    margin-top: auto;
    min-height: 150px;
}}

/* Responsive Breakpoint */
@media (max-width: 925px) {{
    .app-container {{
        /* Shift Macro Layout to stacked */
        grid-template-columns: 1fr;
        grid-template-rows: 60px 60px 1fr;
        grid-template-areas:
            "header"
            "sidebar"
            "main";
        height: auto;
        min-height: 100vh;
    }}
    
    .sidebar {{
        flex-direction: row;
        padding: 0 20px;
        align-items: center;
        justify-content: space-between;
    }}
    
    .nav-placeholder {{ display: none; }}
    
    .main-content {{
        /* Shift Micro Layout to single column */
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas: none; /* Clear the visual map */
        padding: 20px;
    }}
    
    .card {{
        /* Override explicit placements to allow natural stacking */
        grid-area: auto !important; 
        min-height: 200px; /* Ensure they have body when stacked */
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
    <div class="app-container">
        
        <header class="header">
            <h2>{title_text}</h2>
            <div style="font-size: 0.875rem; color: var(--text-secondary);">{body_text}</div>
        </header>
        
        <aside class="sidebar">
            <div class="logo">AppDash</div>
            <div class="nav-placeholder">
                <div class="nav-item" style="background: var(--accent);"></div>
                <div class="nav-item"></div>
                <div class="nav-item"></div>
                <div class="nav-item"></div>
            </div>
        </aside>
        
        <main class="main-content">
            <!-- Card 1 (grid-area: c1) -->
            <div class="card">
                <div class="card-title">Daily Users</div>
                <div class="card-value">24,591</div>
            </div>
            
            <!-- Card 2 (grid-area: c2) -->
            <div class="card">
                <div class="card-title">Conversion</div>
                <div class="card-value">4.2%</div>
            </div>
            
            <!-- Card 3 (grid-area: c3) -->
            <div class="card">
                <div class="card-title">Bounce Rate</div>
                <div class="card-value">42.8%</div>
            </div>
            
            <!-- Card 4 (grid-area: c4) - The Large Span Card -->
            <div class="card">
                <div class="card-title">Revenue Overview (Spans 2x2)</div>
                <div class="card-value">$124,500</div>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">Interactive layout mapped purely via grid-template-areas.</p>
                <div class="chart-placeholder"></div>
            </div>
            
            <!-- Card 5 (grid-area: c5) -->
            <div class="card">
                <div class="card-title">Avg Session</div>
                <div class="card-value">2m 14s</div>
            </div>
            
            <!-- Card 6 (grid-area: c6) -->
            <div class="card">
                <div class="card-title">Active Now</div>
                <div class="card-value" style="color: var(--accent);">1,204</div>
            </div>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Nested CSS Grid Dashboard Shell
// Layout logic is handled entirely by CSS Grid.
// This script is ready for future interactive enhancements (e.g. updating the chart data).

document.addEventListener('DOMContentLoaded', () => {{
    console.log('Dashboard layout initialized.');
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
