def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Masterclass",
    body_text: str = "This layout demonstrates macro structural mapping with grid areas, combined with a micro auto-fit grid that requires zero media queries for column wrapping.",
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
        outer_bg = "#000000"
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        surface_alt = "#0b1120"
        border_color = "#334155"
    else:
        outer_bg = "#cbd5e1"
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        surface_alt = "#f1f5f9"
        border_color = "#e2e8f0"

    css = f"""/* CSS Grid Architecture */
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
    --outer-bg: {outer_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--outer-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
    color: var(--text);
}}

/* === Macro Layout: Grid Areas === */
.app-shell {{
    display: grid;
    grid-template-areas:
        "header header"
        "aside main"
        "footer footer";
    grid-template-columns: 240px 1fr;
    grid-template-rows: 70px 1fr 50px;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    overflow: hidden;
}}

/* Header Region */
.shell-header {{
    grid-area: header;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: grid;
    align-items: center; /* Vertical centering */
    padding: 0 30px;
}}

.shell-header h2 {{
    font-weight: 600;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 12px;
}}

.shell-header h2::before {{
    content: '';
    display: block;
    width: 18px;
    height: 18px;
    background: var(--accent);
    border-radius: 4px;
    transform: rotate(15deg);
}}

/* Sidebar Region */
.shell-aside {{
    grid-area: aside;
    background: var(--surface-alt);
    border-right: 1px solid var(--border);
    padding: 30px 20px;
    display: grid;
    align-content: start; /* Pack items to top */
    gap: 12px;
}}

.nav-link {{
    padding: 12px 16px;
    border-radius: 8px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background 0.2s, color 0.2s;
    cursor: pointer;
    display: block;
}}

.nav-link:hover {{
    background: rgba(128, 128, 128, 0.1);
    color: var(--text);
}}

.nav-link.active {{
    background: var(--accent);
    color: #fff;
}}

/* Footer Region */
.shell-footer {{
    grid-area: footer;
    background: var(--surface);
    border-top: 1px solid var(--border);
    display: grid;
    align-items: center;
    justify-items: center; /* Horizontal centering */
    font-size: 0.85rem;
    color: var(--text-muted);
}}

/* Main Content Region */
.shell-main {{
    grid-area: main;
    padding: 40px;
    overflow-y: auto;
    background: var(--bg);
}}

.main-header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}}

.main-header p {{
    color: var(--text-muted);
    font-size: 1rem;
    line-height: 1.6;
    max-width: 600px;
}}

/* === Micro Layout: Auto-Fit Grid === */
.content-grid {{
    display: grid;
    /* Zero Media Queries required: columns wrap automatically */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-top: 36px;
}}

/* Standard Card */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    opacity: 0;
    transform: translateY(15px);
    transition: opacity 0.5s ease, transform 0.5s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}}

.card.loaded {{
    opacity: 1;
    transform: translateY(0);
}}

.card.loaded:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
    box-shadow: 0 12px 24px -8px rgba(0,0,0,0.3);
}}

.card h3 {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
}}

.card p {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

.card code {{
    background: var(--surface-alt);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    color: var(--accent);
    font-size: 0.85em;
}}

/* Feature: Full Width Spanning */
.full-width-card {{
    grid-column: 1 / -1; /* Spans from first grid line to the last grid line */
    background: linear-gradient(90deg, var(--surface), var(--surface-alt));
    border-left: 4px solid var(--accent);
}}

/* Feature: Grid Cell Stacking (Layering without Absolute Positioning) */
.layered-card {{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    padding: 0; /* Clear padding so background stretches */
    overflow: hidden;
}}

.layered-card > * {{
    /* Force all children into the exact same cell */
    grid-column: 1 / 2;
    grid-row: 1 / 2;
}}

.card-bg {{
    background: linear-gradient(135deg, var(--accent) 0%, transparent 100%);
    opacity: 0.15;
    z-index: 0;
}}

.layered-card .card-content {{
    padding: 24px;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.card-badge {{
    /* Grid alignment handles positioning natively */
    justify-self: end;
    align-self: start;
    z-index: 2;
    margin: 16px;
    background: var(--accent);
    color: #fff;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

/* Custom Scrollbar */
.shell-main::-webkit-scrollbar {{ width: 8px; }}
.shell-main::-webkit-scrollbar-track {{ background: transparent; }}
.shell-main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

/* Base macro fallback for very small viewports */
@media (max-width: 768px) {{
    .app-shell {{
        grid-template-areas:
            "header"
            "main"
            "footer";
        grid-template-columns: 1fr;
        grid-template-rows: 70px 1fr 50px;
    }}
    .shell-aside {{ display: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Grid Architecture</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-shell">
        <header class="shell-header">
            <h2>Grid Dashboard</h2>
        </header>
        
        <aside class="shell-aside">
            <a class="nav-link active">Overview</a>
            <a class="nav-link">Analytics</a>
            <a class="nav-link">Settings</a>
            <a class="nav-link">Deployments</a>
        </aside>
        
        <main class="shell-main">
            <div class="main-header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            
            <div class="content-grid">
                
                <div class="card">
                    <h3>Auto-Fit Grid</h3>
                    <p>This layout uses <code>repeat(auto-fit, minmax(220px, 1fr))</code> to create fluid column wrapping without any media queries.</p>
                </div>
                
                <div class="card layered-card">
                    <div class="card-bg"></div>
                    <div class="card-content">
                        <h3>Cell Stacking</h3>
                        <p>Both background and content share <code>grid-area: 1/1/2/2</code> for perfect layering without <code>position: absolute</code>.</p>
                    </div>
                    <div class="card-badge">Z-Index</div>
                </div>

                <div class="card full-width-card">
                    <div class="card-content">
                        <h3>Full Row Spanning</h3>
                        <p>Using <code>grid-column: 1 / -1</code> forces this item to stretch natively from the first grid line to the last dynamically created line.</p>
                    </div>
                </div>

                <div class="card">
                    <h3>Grid Alignment</h3>
                    <p>The header and footer regions utilize <code>align-items</code> and <code>justify-items</code> for frictionless vertical and horizontal centering.</p>
                </div>

                <div class="card">
                    <h3>Implicit Rows</h3>
                    <p>As you scale the window down, the grid automatically generates new implicit rows to house the wrapping content seamlessly.</p>
                </div>
                
            </div>
        </main>
        
        <footer class="shell-footer">
            <p>Built exclusively with Native CSS Grid Mechanics</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    // Stagger the entrance animation for grid items to highlight flow
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('loaded');
        }, 80 * index); // 80ms stagger delay per item
    });
});"""

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
