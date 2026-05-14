def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Masterclass",
    body_text: str = "Resize the window to see auto-fit and minmax() in action without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#E63946",     # Tutorial's signature pink/red
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing advanced CSS Grid layouts.
    Combines Grid Template Areas (for macro layout) and Auto-Fit/MinMax (for micro layout).
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0B0D17"         # Deep dark background
        container_bg = "#1A1D2D"     # Slightly lighter for the main container
        text_color = "#FFFFFF"
        text_muted = "rgba(255,255,255,0.7)"
        border_color = "rgba(255,255,255,0.1)"
    else:
        bg_color = "#F0F2F5"         # Soft light gray
        container_bg = "#FFFFFF"
        text_color = "#111827"
        text_muted = "rgba(0,0,0,0.6)"
        border_color = "rgba(0,0,0,0.1)"

    # === CSS ===
    css = f"""/* Fluid CSS Grid Layout — generated component */
:root {{
    --bg: {bg_color};
    --container-bg: {container_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --max-width: {width_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: var(--max-width);
}}

.page-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
}}

.page-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* MACRO LAYOUT: CSS Grid Template Areas */
.app-shell {{
    width: 100%;
    max-width: var(--max-width);
    /* The core height behavior */
    min-height: 600px;
    background: var(--border); /* Acts as grid lines visible through gaps */
    border: 2px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    
    /* Grid Magic Here */
    display: grid;
    gap: 4px; /* Creates the wireframe aesthetic */
    
    /* Defines 3 rows and 2 columns */
    grid-template-rows: 80px 1fr 60px;
    grid-template-columns: 250px 1fr;
    
    /* Drawing the map */
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
}}

/* Assigning elements to the named areas */
.area-header {{ grid-area: header; }}
.area-sidebar {{ grid-area: sidebar; }}
.area-main {{ grid-area: main; }}
.area-footer {{ grid-area: footer; }}

/* Base styling for all outer grid items */
.shell-item {{
    background: var(--container-bg);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}}

.shell-item h2 {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 1rem;
}}

/* MICRO LAYOUT: Auto-fit Responsive Grid (No Media Queries) */
.fluid-grid {{
    /* Nested Grid Magic Here */
    display: grid;
    gap: 1rem;
    
    /* 
       auto-fit: create as many columns as will fit in the container
       minmax(200px, 1fr): columns are at least 200px, but share remaining space equally 
    */
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    
    /* implicit row sizing */
    grid-auto-rows: 150px; 
    
    width: 100%;
}}

.fluid-card {{
    background: var(--accent);
    color: white;
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    font-weight: 600;
    font-size: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}}

.fluid-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px rgba(0,0,0,0.2);
}}

/* Adding the tutorial's item number aesthetic */
.fluid-card::before {{
    content: attr(data-index);
    position: absolute;
    top: 1rem;
    left: 1rem;
    font-size: 1rem;
    background: rgba(255,255,255,0.2);
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}}

/* Optional: Layering example using explicit grid coordinates */
.fluid-card.spanner {{
    /* Spans 2 columns if space permits (breaks gracefully due to grid flow) */
    /* grid-column: span 2; */
    background: rgba(255,255,255,0.1);
    border: 2px dashed var(--accent);
    color: var(--accent);
}}

/* Responsive adjustment ONLY for the macro app-shell */
@media (max-width: 768px) {{
    .app-shell {{
        grid-template-columns: 1fr;
        grid-template-rows: auto auto 1fr auto;
        grid-template-areas:
            "header"
            "sidebar"
            "main"
            "footer";
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <p style="margin-top:0.5rem; font-family:monospace; color:var(--accent);" id="dimension-readout">Width: ...</p>
    </header>

    <div class="app-shell">
        <header class="shell-item area-header">
            <h2>Header</h2>
            <p>grid-area: header;</p>
        </header>
        
        <aside class="shell-item area-sidebar">
            <h2>Sidebar</h2>
            <p>grid-area: sidebar;</p>
        </aside>
        
        <main class="shell-item area-main">
            <h2>Main / Fluid Grid</h2>
            
            <div class="fluid-grid">
                <div class="fluid-card" data-index="1">Item</div>
                <div class="fluid-card" data-index="2">Item</div>
                <div class="fluid-card" data-index="3">Item</div>
                <div class="fluid-card spanner" data-index="4">Item</div>
                <div class="fluid-card" data-index="5">Item</div>
                <div class="fluid-card" data-index="6">Item</div>
            </div>
            
        </main>
        
        <footer class="shell-item area-footer">
            <h2>Footer</h2>
            <p>grid-area: footer;</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Fluid CSS Grid Layout — dynamic readout
document.addEventListener('DOMContentLoaded', () => {
    const readout = document.getElementById('dimension-readout');
    const mainGrid = document.querySelector('.fluid-grid');
    
    // Use ResizeObserver to watch the specific grid container
    const observer = new ResizeObserver(entries => {
        for (let entry of entries) {
            const width = Math.round(entry.contentRect.width);
            readout.textContent = `Main Container Width: ${width}px | auto-fit wrapping`;
        }
    });
    
    if (mainGrid) {
        observer.observe(mainGrid);
    }
});
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
