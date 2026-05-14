def create_component(
    output_dir: str,
    title_text: str = "Grid Mastery Dashboard",
    body_text: str = "A comprehensive layout demonstrating macro and micro grid architectures.",
    color_scheme: str = "dark",
    accent_color: str = "#e91e63",     # Pink from tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid Dashboard.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors matching the tutorial's vibrant-on-dark style
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        surface_color = "#1a2235"
        surface_highlight = "#232d45"
        text_color = "#f8fafc"
        muted_color = "#94a3b8"
        border_color = "#334155"
        grid_line = "rgba(255, 255, 255, 0.05)"
        glass_bg = "rgba(26, 34, 53, 0.6)"
    else:
        bg_color = "#f1f5f9"
        surface_color = "#ffffff"
        surface_highlight = "#e2e8f0"
        text_color = "#0f172a"
        muted_color = "#64748b"
        border_color = "#cbd5e1"
        grid_line = "rgba(0, 0, 0, 0.05)"
        glass_bg = "rgba(255, 255, 255, 0.6)"

    secondary_color = kwargs.get("secondary_color", "#00bcd4") # Cyan
    warning_color = kwargs.get("warning_color", "#ffeb3b")     # Yellow

    css = f"""/* Responsive CSS Grid Dashboard */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-highlight: {surface_highlight};
    --text: {text_color};
    --muted: {muted_color};
    --border: {border_color};
    --grid-line: {grid_line};
    --glass: {glass_bg};
    
    --accent: {accent_color};
    --secondary: {secondary_color};
    --warning: {warning_color};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    overflow: hidden;
    position: relative;
}}

/* === Macro Layout: The Application Shell === */
.dashboard-layout {{
    display: grid;
    grid-template-areas:
        "header header"
        "sidebar main";
    grid-template-columns: 280px 1fr;
    grid-template-rows: 80px 1fr;
    gap: 1.5rem;
    height: 100%;
    padding: 1.5rem;
}}

.dashboard-header {{
    grid-area: header;
    background: var(--surface);
    border-radius: 1rem;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 2rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}}

.dashboard-header h1 {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
}}

#toggle-grid {{
    margin-left: auto;
    background: var(--surface-highlight);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.6rem 1.2rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.2s ease;
}}

#toggle-grid:hover {{
    background: var(--border);
}}

.dashboard-sidebar {{
    grid-area: sidebar;
    background: var(--surface);
    border-radius: 1rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}}

.dashboard-sidebar h3 {{
    font-size: 1.1rem;
    color: var(--accent);
    margin-bottom: 0.75rem;
}}

.dashboard-sidebar p {{
    color: var(--muted);
    font-size: 0.95rem;
    line-height: 1.6;
}}

.align-showcase {{
    margin-top: auto;
    background: var(--bg);
    border-radius: 0.75rem;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border: 1px dashed var(--border);
    min-height: 160px;
    position: relative;
    padding: 1rem;
}}

.align-showcase::after {{
    content: "grid cell (1fr x 1fr)";
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    font-size: 0.75rem;
    color: var(--muted);
    font-family: monospace;
}}

.align-box {{
    /* Demonstrates internal cell alignment */
    justify-self: end;
    align-self: end;
    background: var(--warning);
    color: #000;
    font-weight: 700;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    z-index: 2;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}}

/* === Micro Layout: The Bento Grid === */
.dashboard-main {{
    grid-area: main;
    background: var(--bg);
    border-radius: 1rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    overflow-y: auto;
    
    /* Background Grid Pattern imitating the tutorial UI */
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center top;
    box-shadow: inset 0 2px 20px rgba(0,0,0,0.02);
}}

.dashboard-main::-webkit-scrollbar {{ width: 6px; }}
.dashboard-main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

.bento-grid {{
    display: grid;
    /* The magic auto-fit responsive formula */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    grid-auto-rows: 200px;
    grid-auto-flow: dense;
    gap: 1.5rem;
}}

.card {{
    background: var(--surface);
    border-radius: 1rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s, border-color 0.2s;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -3px rgba(0,0,0,0.1);
    border-color: var(--secondary);
}}

.card h3 {{
    font-size: 1.15rem;
    margin-bottom: 0.75rem;
    color: var(--text);
}}

.card p {{
    color: var(--muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

code {{
    background: var(--surface-highlight);
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-family: monospace;
    font-size: 0.85rem;
    color: var(--secondary);
    display: inline-block;
    margin-top: 0.5rem;
}}

/* Spanning Classes */
.card-col-span-2 {{ grid-column: span 2; }}
.card-row-span-2 {{ grid-row: span 2; }}

.accent-card {{
    border-color: var(--secondary);
    background: linear-gradient(135deg, var(--surface), rgba(0, 188, 212, 0.05));
}}
.accent-card h3 {{ color: var(--secondary); }}

/* === Complex Explicit Overlap Showcase === */
.card-overlap {{
    padding: 0;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 1fr);
    background: transparent;
    border: none;
    box-shadow: none;
}}

.card-overlap:hover {{
    transform: none;
    border-color: transparent;
    box-shadow: none;
}}

.overlap-bg {{
    /* Explicit line numbers: row-start / col-start / row-end / col-end */
    grid-area: 1 / 1 / 4 / 4;
    background: linear-gradient(135deg, var(--accent), var(--secondary));
    border-radius: 1rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}}

.overlap-content {{
    /* Overlaps the background element naturally using grid tracks */
    grid-area: 2 / 2 / 5 / 5;
    background: var(--glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 1rem;
    z-index: 10;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

/* === Interactive State: Grid Outlines === */
.dashboard-main.show-outlines .card {{
    border: 2px dashed var(--accent);
    background: rgba(233, 30, 99, 0.03);
    box-shadow: none;
}}
.dashboard-main.show-outlines .card > * {{
    opacity: 0.8;
}}

/* === Responsive Breakpoints === */
@media (max-width: 900px) {{
    .dashboard-layout {{
        grid-template-areas:
            "header"
            "main"
            "sidebar";
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr auto;
    }}
}}

@media (max-width: 650px) {{
    .card-col-span-2 {{ grid-column: span 1; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="dashboard-layout">
            
            <header class="dashboard-header">
                <h1>{title_text}</h1>
                <button id="toggle-grid">Toggle Grid View</button>
            </header>
            
            <aside class="dashboard-sidebar">
                <div class="sidebar-info">
                    <h3>Grid Concepts</h3>
                    <p>{body_text}</p>
                </div>
                
                <!-- Alignment Showcase -->
                <div class="align-showcase">
                    <div class="align-box">align-self: end</div>
                </div>
            </aside>
            
            <main class="dashboard-main">
                <div class="bento-grid">
                    
                    <div class="card card-col-span-2 accent-card">
                        <h3>Responsive Auto-fit</h3>
                        <p>Fluid columns mapping to container width without media queries.</p>
                        <code>repeat(auto-fit, minmax(260px, 1fr))</code>
                    </div>
                    
                    <div class="card card-row-span-2">
                        <h3>Row Spanning</h3>
                        <p>Stretches vertically across defined tracks.</p>
                        <code>grid-row: span 2</code>
                        <p style="margin-top:1rem;">Empty gaps are efficiently backfilled using <code>grid-auto-flow: dense</code>.</p>
                    </div>
                    
                    <div class="card card-overlap">
                        <div class="overlap-bg"></div>
                        <div class="overlap-content">
                            <h3>Explicit Overlap</h3>
                            <p>Layered cleanly using precise track coordinates.</p>
                            <code>grid-area: 2 / 2 / 5 / 5</code>
                        </div>
                    </div>
                    
                    <div class="card basic-card">
                        <h3>Implicit Grid</h3>
                        <p>Items added beyond explicit definitions generate rows automatically.</p>
                    </div>
                    
                    <div class="card basic-card">
                        <h3>Fractional Units</h3>
                        <p>Distributes remaining spatial availability using the <code>1fr</code> unit.</p>
                    </div>
                    
                </div>
            </main>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Interactive Grid Visualizer Toggle
document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.getElementById('toggle-grid');
    const mainContent = document.querySelector('.dashboard-main');
    
    toggleBtn.addEventListener('click', () => {{
        // Toggles the class that applies dashed borders to grid items
        mainContent.classList.toggle('show-outlines');
        
        // Update button visual state
        if (mainContent.classList.contains('show-outlines')) {{
            toggleBtn.style.background = 'var(--accent)';
            toggleBtn.style.color = '#fff';
            toggleBtn.style.borderColor = 'var(--accent)';
            toggleBtn.textContent = 'Hide Grid View';
        }} else {{
            toggleBtn.style.background = 'var(--surface-highlight)';
            toggleBtn.style.color = 'var(--text)';
            toggleBtn.style.borderColor = 'var(--border)';
            toggleBtn.textContent = 'Toggle Grid View';
        }}
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
