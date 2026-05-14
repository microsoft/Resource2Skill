def create_component(
    output_dir: str,
    title_text: str = "GridBox OS",
    body_text: str = "Responsive Dashboard Layout",
    color_scheme: str = "dark",
    accent_color: str = "#f43f5e",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid Dashboard layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_body = "#020617"       # Very dark slate for outer window
        bg_base = "#0f172a"       # App background
        bg_surface = "#1e293b"    # Card/Sidebar background
        bg_surface_hover = "#334155"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        border_color = "#334155"
    else:
        bg_body = "#e2e8f0"       
        bg_base = "#f8fafc"       
        bg_surface = "#ffffff"    
        bg_surface_hover = "#f1f5f9"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        border_color = "#cbd5e1"

    css = f"""/* Responsive CSS Grid Dashboard */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-body: {bg_body};
    --bg-base: {bg_base};
    --bg-surface: {bg_surface};
    --bg-surface-hover: {bg_surface_hover};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-body);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

/* A wrapper to act as the preview viewport */
.app-viewport {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    background: var(--bg-base);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25), 0 0 0 1px var(--border);
    overflow: hidden;
}}

/* ====================================================
   PATTERN 1: MACRO LAYOUT (Named Grid Areas)
==================================================== */
.dashboard-layout {{
    display: grid;
    height: 100%;
    grid-template-columns: 240px 1fr;
    grid-template-rows: 70px 1fr 50px;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
}}

.grid-sidebar {{
    grid-area: sidebar;
    background: var(--bg-surface);
    border-right: 1px solid var(--border);
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.grid-header {{
    grid-area: header;
    padding: 0 32px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border);
}}

.grid-main {{
    grid-area: main;
    padding: 32px;
    overflow-y: auto;
}}

.grid-footer {{
    grid-area: footer;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 32px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}}

/* ====================================================
   PATTERN 2: MICRO LAYOUT (Auto-Fit Responsive Grid)
==================================================== */
.auto-fit-grid {{
    display: grid;
    /* The magic formula for zero-media-query responsiveness */
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    grid-auto-rows: 160px; /* Default height for implicit rows */
    gap: 24px;
}}

/* ====================================================
   PATTERN 3: OVERLAPPING & SPANNING
==================================================== */
.card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* 1x1 grid for easy absolute-free overlapping */
    display: grid;
    grid-template-areas: "stack";
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
    border-color: var(--accent);
}}

/* Card Content Layer */
.card-content {{
    grid-area: stack; /* Assign to the single 1x1 cell */
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* Card Badge Layer (Overlaps without position: absolute) */
.card-badge {{
    grid-area: stack; /* Assign to the SAME cell */
    justify-self: end; /* Align right */
    align-self: start; /* Align top */
    margin: 16px;
    
    background: var(--accent);
    color: #fff;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 700;
    z-index: 2;
}}

/* Grid Span Demo */
.card-featured {{
    grid-column: span 2;
    grid-row: span 2;
}}

/* Typography Details */
h1 {{ font-size: 1.5rem; font-weight: 600; color: var(--text-primary); }}
h2 {{ font-size: 1.1rem; font-weight: 500; color: var(--text-primary); margin-bottom: 8px; }}
p {{ font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5; }}
.brand {{ font-size: 1.25rem; font-weight: 700; color: var(--accent); margin-bottom: 24px; }}

/* Responsive override for the macro layout only */
@media (max-width: 768px) {{
    .dashboard-layout {{
        grid-template-columns: 1fr;
        grid-template-rows: auto auto 1fr auto;
        grid-template-areas:
            "header"
            "sidebar"
            "main"
            "footer";
    }}
    .card-featured {{
        grid-column: span 1;
        grid-row: span 1;
    }}
}}
"""

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

    <div class="app-viewport">
        <div class="dashboard-layout">
            
            <!-- Sidebar Area -->
            <aside class="grid-sidebar">
                <div class="brand">⌘ {title_text}</div>
                <p>Overview</p>
                <p>Analytics</p>
                <p>Settings</p>
            </aside>

            <!-- Header Area -->
            <header class="grid-header">
                <h1>{body_text}</h1>
            </header>

            <!-- Main Content Area -->
            <main class="grid-main">
                
                <!-- Micro-layout: Responsive Grid without Media Queries -->
                <div class="auto-fit-grid">
                    
                    <!-- Spanning Card -->
                    <div class="card card-featured">
                        <div class="card-badge">LIVE</div>
                        <div class="card-content">
                            <h2>Featured Metric</h2>
                            <p>This element uses `grid-column: span 2` and `grid-row: span 2` to dominate the visual hierarchy.</p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-content">
                            <h2>Component 1</h2>
                            <p>Autofit handles wrapping gracefully.</p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-content">
                            <h2>Component 2</h2>
                            <p>1fr units distribute width equally.</p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-badge">+24%</div>
                        <div class="card-content">
                            <h2>Overlaps</h2>
                            <p>Grid layers the badge without absolute positioning.</p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-content">
                            <h2>Component 4</h2>
                            <p>Minimum width ensures readability.</p>
                        </div>
                    </div>

                </div>
            </main>

            <!-- Footer Area -->
            <footer class="grid-footer">
                <p>CSS Grid Pattern Extraction &copy; 2024</p>
            </footer>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// CSS Grid layout is highly declarative and requires zero JavaScript
// to maintain its responsiveness or overlapping properties.

document.addEventListener('DOMContentLoaded', () => {{
    console.log('{title_text} Layout Initialized successfully.');
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
