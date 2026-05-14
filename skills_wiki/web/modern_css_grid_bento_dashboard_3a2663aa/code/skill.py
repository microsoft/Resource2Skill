def create_component(
    output_dir: str,
    title_text: str = "Grid Master Dashboard",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern CSS Grid Bento Dashboard.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    body_text = body_text or "Learn how to build powerful two-dimensional layouts utilizing auto-fit grids, template areas, and layer stacking without absolute positioning."

    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        border_color = "#334155"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#64748b"

    css = f"""/* Modern CSS Grid Dashboard */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_primary};
    --text-sec: {text_secondary};
    --accent: {accent_color};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000; /* Outer canvas */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.widget-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: 100vh;
    container-type: inline-size;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background: var(--bg);
    color: var(--text);
}}

/* === 1. Macro Layout: Grid Template Areas === */
.dashboard-layout {{
    display: grid;
    height: 100%;
    grid-template-columns: 260px 1fr;
    grid-template-rows: 70px 1fr auto;
    grid-template-areas:
        "header header"
        "sidebar main"
        "sidebar footer";
}}

.header {{
    grid-area: header;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    background: var(--bg);
    z-index: 10;
}}

.sidebar {{
    grid-area: sidebar;
    border-right: 1px solid var(--border);
    background: var(--surface);
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.main-content {{
    grid-area: main;
    overflow-y: auto;
    padding: 2rem;
    background: var(--bg);
}}

.footer {{
    grid-area: footer;
    border-top: 1px solid var(--border);
    padding: 1rem 2rem;
    color: var(--text-sec);
    font-size: 0.875rem;
}}

/* Header & Sidebar Internals */
.logo {{ font-size: 1.5rem; font-weight: 700; letter-spacing: -0.5px; }}
.logo span {{ color: var(--accent); }}
.user-profile {{ width: 40px; height: 40px; border-radius: 50%; background: var(--accent); }}

.nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 8px;
    color: var(--text-sec);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}}
.nav-item:hover {{ background: rgba(150, 150, 150, 0.1); color: var(--text); }}
.nav-item.active {{ background: var(--accent); color: #fff; }}
.nav-item svg {{ width: 20px; height: 20px; }}

/* === 2. Grid Layering Trick (No Absolute Positioning) === */
.layered-card {{
    display: grid;
    /* 1x1 grid cell */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 16px;
    overflow: hidden;
    min-height: 280px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid var(--border);
}}

.layered-card > * {{
    /* Pin all children to the exact same cell */
    grid-area: 1 / 1 / -1 / -1;
}}

.layered-card .bg-layer {{
    background: linear-gradient(135deg, var(--accent), #000000);
    z-index: 1;
}}

.layered-card .pattern-layer {{
    background-image: radial-gradient(rgba(255,255,255,0.15) 2px, transparent 2px);
    background-size: 24px 24px;
    z-index: 2;
}}

.layered-card .content-layer {{
    z-index: 3;
    padding: 3rem;
    /* Grid alignment inside the cell */
    align-self: end;
    justify-self: start;
    color: #ffffff;
}}

.content-layer h2 {{ font-size: 2.5rem; margin-bottom: 0.5rem; line-height: 1.1; letter-spacing: -1px; }}
.content-layer p {{ font-size: 1.1rem; opacity: 0.9; max-width: 600px; line-height: 1.5; }}

/* === 3. Micro Layout: Auto-Fit Zero-MQ Grid === */
.auto-grid {{
    display: grid;
    /* The magic responsive line */
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
}}
.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}}

.card-title {{ font-size: 0.875rem; color: var(--text-sec); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
.card-value {{ font-size: 2.25rem; font-weight: 700; color: var(--text); }}

/* Mini Grid for Charts */
.card-chart {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    align-items: end; /* Align bars to bottom */
    gap: 6px;
    height: 45px;
    margin-top: 1.5rem;
}}
.chart-bar {{
    background: var(--accent);
    border-radius: 3px 3px 0 0;
    opacity: 0.85;
    transition: height 0.5s ease-out;
}}

/* Container Query for Macro Layout collapse */
@container (max-width: 800px) {{
    .dashboard-layout {{
        grid-template-areas:
            "header"
            "main"
            "footer";
        grid-template-columns: 1fr;
    }}
    .sidebar {{ display: none; }}
    .content-layer h2 {{ font-size: 1.8rem; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        <div class="dashboard-layout">
            
            <header class="header">
                <div class="logo">Grid<span>Master</span></div>
                <div class="user-profile"></div>
            </header>
            
            <aside class="sidebar">
                <div class="nav-item active">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                    Overview
                </div>
                <div class="nav-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"></path><path d="M3 5v14a2 2 0 0 0 2 2h16v-5H5a2 2 0 0 0 0 4h16"></path></svg>
                    Transactions
                </div>
                <div class="nav-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                    Analytics
                </div>
            </aside>
            
            <main class="main-content">
                
                <!-- Grid Layering Example -->
                <div class="layered-card">
                    <div class="bg-layer"></div>
                    <div class="pattern-layer"></div>
                    <div class="content-layer">
                        <h2>{title_text}</h2>
                        <p>{body_text}</p>
                    </div>
                </div>

                <!-- Auto-Fit Grid Example -->
                <div class="auto-grid" id="data-grid">
                    <!-- JavaScript will populate cards here -->
                </div>

            </main>
            
            <footer class="footer">
                <p>&copy; 2024 Powered by CSS Grid</p>
            </footer>
            
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Populate Auto-Fit Grid with Demo Data
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('data-grid');
    
    const cardData = [
        {{ title: 'Total Revenue', value: '$84,592' }},
        {{ title: 'Active Users', value: '4,209' }},
        {{ title: 'Conversion Rate', value: '6.4%' }},
        {{ title: 'Server Uptime', value: '99.9%' }}
    ];

    cardData.forEach(data => {{
        const card = document.createElement('div');
        card.className = 'card';
        
        // Generate random heights for the mini grid chart
        let barsHtml = '';
        for(let i=0; i<7; i++) {{
            const height = Math.floor(Math.random() * 70) + 30; // 30% to 100%
            barsHtml += `<div class="chart-bar" style="height: 0%" data-target="${{height}}"></div>`;
        }}

        card.innerHTML = `
            <div class="card-title">${{data.title}}</div>
            <div class="card-value">${{data.value}}</div>
            <div class="card-chart">
                ${{barsHtml}}
            </div>
        `;
        
        grid.appendChild(card);
    }});

    // Simple animation for the grid charts
    setTimeout(() => {{
        document.querySelectorAll('.chart-bar').forEach(bar => {{
            bar.style.height = bar.getAttribute('data-target') + '%';
        }});
    }}, 100);
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
