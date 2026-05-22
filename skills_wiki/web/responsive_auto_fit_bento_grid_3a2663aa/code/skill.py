def create_component(
    output_dir: str,
    title_text: str = "Responsive Bento Grid",
    body_text: str = "Resize the browser window to see the grid automatically reflow using auto-fit and minmax().",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # CSS hex color for accent (pink to match tutorial vibe)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Bento Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0b0f19" # Deep dark from video
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(30, 41, 59, 0.6)"
        surface_hover = "rgba(30, 41, 59, 0.9)"
        border_color = "rgba(255, 255, 255, 0.08)"
        border_hover = accent_color
    else:
        bg_color = "#f0f2f5"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        surface_hover = "#f8fafc"
        border_color = "rgba(0, 0, 0, 0.08)"
        border_hover = accent_color

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Bento Grid — generated component */
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
    --surface-hover: {surface_hover};
    --border: {border_color};
    --border-hover: {border_hover};
    
    /* Configurable container dimensions */
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
    overflow-x: hidden;
}}

header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

p.subtitle {{
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.6;
}}

/* Core Grid Layout Mechanism */
.grid-container {{
    width: 100%;
    max-width: var(--max-width);
    
    /* The Magic Sauce */
    display: grid;
    gap: 1.5rem;
    
    /* Automatically creates columns at least 250px wide, 
       stretching equally to fill remaining space */
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    
    /* Sets a uniform height for implicit rows */
    grid-auto-rows: 220px;
    
    /* Forces smaller items to backfill gaps left by spanning items */
    grid-auto-flow: dense;
}}

/* Grid Item Styling */
.grid-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                border-color 0.3s ease, 
                box-shadow 0.3s ease;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}}

.grid-item:hover {{
    transform: translateY(-4px);
    border-color: var(--border-hover);
    background: var(--surface-hover);
    box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.2);
}}

/* Bento Box Modifiers */
/* On smaller screens, minmax forces a wrap so span 2 might overflow if not clamped, 
   but grid handles this gracefully or we use a simple media query for safety */
@media (min-width: 600px) {{
    .span-col-2 {{
        grid-column: span 2;
    }}
    .span-row-2 {{
        grid-row: span 2;
    }}
    .span-both {{
        grid-column: span 2;
        grid-row: span 2;
    }}
}}

/* Internal Item Content */
.item-number {{
    position: absolute;
    top: 1rem;
    left: 1.5rem;
    font-size: 3rem;
    font-weight: 800;
    opacity: 0.1;
    color: var(--text);
}}

.item-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--accent);
}}

.item-desc {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* Custom decorations based on tutorial visuals */
.grid-item::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 0;
    background: var(--accent);
    transition: height 0.3s ease;
}}

.grid-item:hover::before {{
    height: 100%;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p class="subtitle">{body_text}</p>
    </header>

    <main class="grid-container">
        <!-- Spans 2 columns -->
        <article class="grid-item span-col-2">
            <span class="item-number">01</span>
            <h2 class="item-title">auto-fit</h2>
            <p class="item-desc">Creates as many columns as will fit into the container. Drops elements to the next line when there isn't enough space.</p>
        </article>

        <!-- Standard size -->
        <article class="grid-item">
            <span class="item-number">02</span>
            <h2 class="item-title">minmax()</h2>
            <p class="item-desc">Sets a dynamic track size with a floor (250px) and a ceiling (1fr).</p>
        </article>

        <!-- Spans 2 rows -->
        <article class="grid-item span-row-2">
            <span class="item-number">03</span>
            <h2 class="item-title">Vertical Span</h2>
            <p class="item-desc">Using grid-row: span 2 allows this item to break the horizontal uniformity, creating a classic Bento aesthetic.</p>
        </article>

        <!-- Spans both -->
        <article class="grid-item span-both">
            <span class="item-number">04</span>
            <h2 class="item-title">Hero Feature</h2>
            <p class="item-desc">Spanning multiple rows and columns establishes a focal point within the dense grid layout.</p>
        </article>

        <!-- Standard size -->
        <article class="grid-item">
            <span class="item-number">05</span>
            <h2 class="item-title">1fr Unit</h2>
            <p class="item-desc">Distributes remaining available space equally among tracks.</p>
        </article>

        <!-- Standard size -->
        <article class="grid-item">
            <span class="item-number">06</span>
            <h2 class="item-title">Implicit Rows</h2>
            <p class="item-desc">grid-auto-rows ensures newly wrapped items inherit a specific height automatically.</p>
        </article>
        
        <!-- Standard size -->
        <article class="grid-item">
            <span class="item-number">07</span>
            <h2 class="item-title">Dense Flow</h2>
            <p class="item-desc">Notice how smaller items backfill gaps created by larger spanning components.</p>
        </article>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Bento Grid
document.addEventListener('DOMContentLoaded', () => {{
    // The responsive reflow is handled entirely by CSS Grid.
    // We log the grid computed properties for demonstration purposes.
    const gridContainer = document.querySelector('.grid-container');
    
    window.addEventListener('resize', () => {{
        const computedStyle = window.getComputedStyle(gridContainer);
        const columnCount = computedStyle.gridTemplateColumns.split(' ').length;
        console.log(`Current active columns: ${{columnCount}}`);
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
