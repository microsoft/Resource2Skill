def create_component(
    output_dir: str,
    title_text: str = "Modern CSS Grid Capabilities",
    body_text: str = "Exploring explicit coordinate mapping, layered cells, and zero-media-query responsive flow.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., Violet)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing explicit and implicit CSS Grid layouts.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Adaptive Grid Architect Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

header.main-header {{
    text-align: left;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.5rem;
}}

header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 60ch;
    line-height: 1.5;
}}

/* === EXPLICIT GRID: Layering and Coordinates === */
.section-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.explicit-grid {{
    display: grid;
    /* 6 columns, equal width */
    grid-template-columns: repeat(6, 1fr);
    /* 4 rows, fixed height */
    grid-template-rows: repeat(4, 80px);
    gap: 1.5rem;
}}

.grid-panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 6px var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.grid-panel:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px var(--shadow);
}}

.panel-badge {{
    font-family: 'Courier New', monospace;
    font-size: 0.75rem;
    background: var(--bg);
    color: var(--text-muted);
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    border: 1px solid var(--border);
    align-self: flex-start;
    margin-bottom: auto;
}}

.panel-content h3 {{
    font-size: 1.4rem;
    margin-bottom: 0.25rem;
}}

.panel-content p {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

/* Mapping to explicit coordinates */
.panel-1 {{
    grid-area: 1 / 1 / 5 / 4; /* row-start / col-start / row-end / col-end */
    background: color-mix(in srgb, var(--accent) 8%, var(--surface));
    border-top: 4px solid var(--accent);
}}

.panel-2 {{
    /* Intentionally overlaps panel 1 and 3 */
    grid-area: 2 / 3 / 4 / 6; 
    z-index: 10;
    background: color-mix(in srgb, var(--accent) 70%, rgba(0,0,0,0.5));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.2);
}}

.panel-2 .panel-badge {{
    background: rgba(0,0,0,0.3);
    color: #fff;
    border-color: rgba(255,255,255,0.2);
}}

.panel-2 .panel-content p {{
    color: rgba(255,255,255,0.8);
}}

.panel-3 {{
    grid-area: 1 / 5 / 5 / 7;
}}

/* Responsive behavior for explicit grid */
@media (max-width: 900px) {{
    .explicit-grid {{
        grid-template-columns: 1fr;
        grid-template-rows: auto;
    }}
    .panel-1, .panel-2, .panel-3 {{
        grid-area: auto;
    }}
}}

/* === IMPLICIT GRID: Auto-fit fluid columns === */
.button-primary {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: opacity 0.2s;
}}

.button-primary:hover {{
    opacity: 0.9;
}}

.implicit-grid {{
    display: grid;
    /* THE MAGIC RESPONSIVE ALGORITHM */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    /* Automatically generated row height */
    grid-auto-rows: 140px; 
    gap: 1.5rem;
}}

.widget-card {{
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-muted);
    transition: all 0.3s ease;
    animation: scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}}

.widget-card:hover {{
    border-style: solid;
    border-color: var(--accent);
    color: var(--text);
    background: color-mix(in srgb, var(--accent) 5%, var(--surface));
}}

@keyframes scaleIn {{
    from {{ opacity: 0; transform: scale(0.9); }}
    to {{ opacity: 1; transform: scale(1); }}
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
    <div class="app-wrapper">
        <header class="main-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <section>
            <div class="section-title">
                <h2>1. Explicit Structure & Layering</h2>
            </div>
            <div class="explicit-grid">
                <article class="grid-panel panel-1">
                    <span class="panel-badge">grid-area: 1 / 1 / 5 / 4</span>
                    <div class="panel-content">
                        <h3>Main Overview</h3>
                        <p>Mapped specifically to coordinates.</p>
                    </div>
                </article>
                
                <article class="grid-panel panel-2">
                    <span class="panel-badge">grid-area: 2 / 3 / 4 / 6; z-index: 10</span>
                    <div class="panel-content">
                        <h3>Overlay Focus</h3>
                        <p>Natively overlaps without absolute positioning.</p>
                    </div>
                </article>

                <article class="grid-panel panel-3">
                    <span class="panel-badge">grid-area: 1 / 5 / 5 / 7</span>
                    <div class="panel-content">
                        <h3>Context Panel</h3>
                        <p>Flows around the explicit layout.</p>
                    </div>
                </article>
            </div>
        </section>

        <section>
            <div class="section-title">
                <h2>2. Implicit Fluid Responsiveness</h2>
                <button class="button-primary" id="addWidgetBtn">+ Add Widget</button>
            </div>
            <p style="color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">
                Powered by <code>grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))</code>. Resize browser to see reflow.
            </p>
            <div class="implicit-grid" id="widgetGrid">
                <div class="widget-card">Widget 1</div>
                <div class="widget-card">Widget 2</div>
                <div class="widget-card">Widget 3</div>
                <div class="widget-card">Widget 4</div>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Implicit Grid Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const addWidgetBtn = document.getElementById('addWidgetBtn');
    const widgetGrid = document.getElementById('widgetGrid');
    
    // Count existing widgets
    let widgetCount = widgetGrid.children.length;

    addWidgetBtn.addEventListener('click', () => {{
        widgetCount++;
        
        // Create new widget element
        const newWidget = document.createElement('div');
        newWidget.className = 'widget-card';
        newWidget.textContent = `Widget ${{widgetCount}}`;
        
        // Append to the implicit grid - CSS Grid handles the layout logic instantly
        widgetGrid.appendChild(newWidget);
        
        // Scroll to bottom smoothly if grid expands vertically
        window.scrollTo({{
            top: document.body.scrollHeight,
            behavior: 'smooth'
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
