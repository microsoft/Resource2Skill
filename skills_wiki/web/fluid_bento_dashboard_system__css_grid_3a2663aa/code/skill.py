def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Dashboard",
    body_text: str = "Resize the browser window to see the zero-media-query auto-fit grid in action.",
    color_scheme: str = "dark",
    accent_color: str = "#e83e8c",  # Vivid pink from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions mimicking the tutorial's technical/vibrant aesthetic
    if color_scheme == "dark":
        bg_color = "#0b0d17"
        text_color = "#ffffff"
        grid_line_color = "rgba(255, 255, 255, 0.1)"
        surface_primary = accent_color
        surface_secondary = "#00bfff" # Cyan
        surface_tertiary = "#ffc107"  # Yellow
        surface_empty = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        grid_line_color = "rgba(0, 0, 0, 0.1)"
        surface_primary = accent_color
        surface_secondary = "#0ea5e9"
        surface_tertiary = "#f59e0b"
        surface_empty = "rgba(0, 0, 0, 0.03)"

    css = f"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --grid-line: {grid_line_color};
    --accent-1: {surface_primary};
    --accent-2: {surface_secondary};
    --accent-3: {surface_tertiary};
    --surface-empty: {surface_empty};
    
    /* Configurable bounds */
    --max-w: {width_px}px;
    --min-h: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    
    /* Tutorial-style background dot pattern */
    background-image: radial-gradient(var(--grid-line) 1px, transparent 1px);
    background-size: 40px 40px;
}}

/* =========================================
   1. MACRO LAYOUT: Grid Template Areas
   ========================================= */
.app-shell {{
    width: 100%;
    max-width: var(--max-w);
    min-height: calc(var(--min-h) - 4rem);
    display: grid;
    gap: 16px;
    
    /* Explicit Grid Definition */
    grid-template-columns: 240px 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas: 
        "header header"
        "sidebar main"
        "footer footer";
        
    /* Blueprint aesthetic border */
    border: 2px dashed var(--grid-line);
    padding: 16px;
    border-radius: 12px;
    background: var(--bg);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Area Assignments */
.shell-header {{ grid-area: header; }}
.shell-sidebar {{ grid-area: sidebar; }}
.shell-main {{ grid-area: main; }}
.shell-footer {{ grid-area: footer; }}

/* Shell Block Styling */
.shell-block {{
    background: var(--surface-empty);
    border: 1px solid var(--grid-line);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.shell-header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.shell-header p {{
    color: var(--text);
    opacity: 0.7;
    font-size: 0.95rem;
}}

.code-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    opacity: 0.6;
    margin-bottom: auto;
    display: block;
}}

/* =========================================
   2. MICRO LAYOUT: Auto-Fit Fluid Grid
   ========================================= */
.bento-grid {{
    display: grid;
    gap: 16px;
    
    /* THE MAGIC LINE: Responsive without Media Queries */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    grid-auto-rows: 180px;
    
    /* Fills in empty spaces if items span differently */
    grid-auto-flow: dense; 
    
    /* Reset padding for the nested grid */
    padding: 0;
    background: transparent;
    border: none;
}}

/* Grid Items */
.bento-card {{
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease, filter 0.2s ease;
    cursor: pointer;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);
}}

.bento-card:hover {{
    transform: translateY(-4px);
    filter: brightness(1.1);
}}

.bento-card .code-label {{ color: rgba(255,255,255,0.8); margin-bottom: 0; }}
.bento-card h2 {{ font-size: 1.5rem; margin-top: auto; color: #fff; }}

/* Card Colors */
.card-primary {{ background: var(--accent-1); }}
.card-secondary {{ background: var(--accent-2); }}
.card-tertiary {{ background: var(--accent-3); }}
.card-empty {{ background: var(--surface-empty); border: 1px dashed var(--grid-line); }}

/* Spanning Elements */
.span-col-2 {{ grid-column: span 2; }}
.span-row-2 {{ grid-row: span 2; }}

/* =========================================
   3. RESPONSIVE OVERRIDE FOR MACRO LAYOUT
   ========================================= */
/* We use one media query here ONLY to stack the app shell sidebar. 
   The inner .bento-grid handles its own responsiveness natively. */
@media (max-width: 768px) {{
    .app-shell {{
        grid-template-columns: 1fr;
        grid-template-areas: 
            "header"
            "main"
            "sidebar"
            "footer";
    }}
    .span-col-2 {{ grid-column: span 1; }} /* Prevent horizontal overflow on small screens */
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

    <!-- CSS Grid "App Shell" using grid-template-areas -->
    <div class="app-shell">
        
        <header class="shell-block shell-header">
            <span class="code-label">grid-area: header;</span>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <aside class="shell-block shell-sidebar">
            <span class="code-label">grid-area: sidebar;</span>
        </aside>

        <!-- Nested fluid grid using auto-fit -->
        <main class="shell-main bento-grid">
            
            <div class="bento-card card-primary span-col-2 span-row-2">
                <span class="code-label">grid-column: span 2;<br>grid-row: span 2;</span>
                <h2>Hero Feature</h2>
            </div>
            
            <div class="bento-card card-secondary">
                <span class="code-label">auto-placed</span>
                <h2>Stat 1</h2>
            </div>
            
            <div class="bento-card card-tertiary">
                <span class="code-label">auto-placed</span>
                <h2>Stat 2</h2>
            </div>
            
            <div class="bento-card card-secondary span-col-2">
                <span class="code-label">grid-column: span 2;</span>
                <h2>Wide Widget</h2>
            </div>
            
            <div class="bento-card card-primary">
                <span class="code-label">auto-placed</span>
                <h2>Action</h2>
            </div>
            
            <div class="bento-card card-empty">
                <span class="code-label">auto-placed</span>
            </div>

        </main>
        
        <footer class="shell-block shell-footer">
            <span class="code-label">grid-area: footer;</span>
        </footer>

    </div>

    <script src="script.js"></script>
</body>
</html>
"""

    js = f"""// CSS Grid Fluid Dashboard
document.addEventListener('DOMContentLoaded', () => {{
    // The layout logic is handled entirely by CSS Grid.
    // JS is only used here to demonstrate dynamic content addition.
    
    const bentoGrid = document.querySelector('.bento-grid');
    
    // Example: Click an empty card to add a new auto-placed item
    const emptyCard = document.querySelector('.card-empty');
    if(emptyCard) {{
        emptyCard.addEventListener('click', () => {{
            const newCard = document.createElement('div');
            newCard.className = 'bento-card card-tertiary';
            newCard.innerHTML = `
                <span class="code-label">Dynamic auto-placed</span>
                <h2>New Item</h2>
            `;
            // Insert before the empty card placeholder
            bentoGrid.insertBefore(newCard, emptyCard);
        }});
    }}
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
