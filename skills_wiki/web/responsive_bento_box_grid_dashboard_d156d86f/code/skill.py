def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Dashboard",
    body_text: str = "A fluid, asymmetrical bento-box layout driven by minmax() and fractional units.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#E94E77",     # CSS hex color for primary accent (pinkish red from video)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Box Grid pattern.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Safe escape for HTML content
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0B0C10"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.7)"
        surface_color = "#1F2833"
        grid_line_color = "rgba(255, 255, 255, 0.05)"
        shadow = "rgba(0, 0, 0, 0.4)"
        card_secondary = "#F2A900" # Yellow
        card_tertiary = "#2D82B7"  # Blue
    else:
        bg_color = "#F8F9FA"
        text_color = "#111111"
        text_muted = "rgba(0, 0, 0, 0.6)"
        surface_color = "#FFFFFF"
        grid_line_color = "rgba(0, 0, 0, 0.06)"
        shadow = "rgba(0, 0, 0, 0.08)"
        card_secondary = "#FCC046" # Lighter Yellow
        card_tertiary = "#4ECDC4"  # Teal/Blue

    # === CSS ===
    css = f"""/* Responsive Bento Box Grid */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --secondary: {card_secondary};
    --tertiary: {card_tertiary};
    --grid-line: {grid_line_color};
    --shadow: {shadow};
    --radius: 20px;
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    /* Blueprint/Technical grid background from the tutorial */
    background-image: 
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center center;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
    /* Ensure it takes up roughly the requested height if content permits */
    min-height: min(var(--height), 90vh);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* Core Grid Setup */
.bento-grid {{
    display: grid;
    /* The magic formula: responsive columns without media queries */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    grid-auto-rows: minmax(200px, auto);
    gap: 24px;
    width: 100%;
}}

/* Base Card Style */
.bento-card {{
    background: var(--surface);
    border-radius: var(--radius);
    padding: 32px;
    box-shadow: 0 8px 32px var(--shadow);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
}}

.bento-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px var(--shadow);
}}

/* Typographic Elements */
.bento-card h2, .bento-card h3 {{
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}}

.bento-card h2 {{ font-size: 2rem; }}
.bento-card h3 {{ font-size: 1.25rem; z-index: 2; }}

.bento-card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
    z-index: 2;
}}

.card-number {{
    position: absolute;
    top: 24px;
    left: 24px;
    font-size: 1rem;
    font-weight: 600;
    opacity: 0.5;
    background: rgba(0,0,0,0.1);
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
}}

/* Spanning Utility Classes */
.span-col-2 {{ grid-column: span 2; }}
.span-row-2 {{ grid-row: span 2; }}

/* Thematic Fills */
.bg-accent {{
    background: var(--accent);
    color: #fff;
}}
.bg-accent p {{ color: rgba(255,255,255,0.9); }}

.bg-secondary {{
    background: var(--secondary);
    color: #111;
}}
.bg-secondary .card-number {{ background: rgba(255,255,255,0.3); }}

.bg-tertiary {{
    background: var(--tertiary);
    color: #fff;
}}

/* Animation Initial State */
.bento-card {{
    opacity: 0;
    transform: translateY(30px);
}}

/* Responsive Breakpoints */
@media (max-width: 600px) {{
    /* Flatten the grid spans on small screens to prevent overflow */
    .span-col-2 {{ grid-column: span 1; }}
    .span-row-2 {{ grid-row: span 1; }}
    
    .bento-grid {{
        grid-template-columns: 1fr;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <main class="bento-grid">
            
            <!-- Hero Card: Spans 2 cols, 2 rows -->
            <article class="bento-card span-col-2 span-row-2 bg-accent">
                <div class="card-number">1</div>
                <h2>{safe_title}</h2>
                <p>{safe_body}</p>
            </article>

            <!-- Secondary Tall Card: Spans 1 col, 2 rows -->
            <article class="bento-card span-row-2 bg-secondary">
                <div class="card-number">2</div>
                <h3>Grid Auto Rows</h3>
                <p>Implicit grids dynamically adjust based on injected content height.</p>
            </article>

            <!-- Standard Card -->
            <article class="bento-card">
                <div class="card-number">3</div>
                <h3>Fractional Units</h3>
                <p>Distribute available space safely using 'fr'.</p>
            </article>

            <!-- Standard Card -->
            <article class="bento-card bg-tertiary">
                <div class="card-number">4</div>
                <h3>Grid Gap</h3>
                <p>Gutters between tracks.</p>
            </article>

            <!-- Wide Card: Spans 2 cols -->
            <article class="bento-card span-col-2">
                <div class="card-number">5</div>
                <h3>minmax() Function</h3>
                <p>Setting minimum boundaries while allowing maximum expansion creates inherently responsive designs without breakpoints.</p>
            </article>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entry animation for Bento Grid items
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    // Trigger animation frame by frame to ensure CSS transitions apply
    requestAnimationFrame(() => {{
        cards.forEach((card, index) => {{
            // Calculate delay based on DOM order
            const delay = index * 100; // 100ms per card
            
            setTimeout(() => {{
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }}, delay);
        }});
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
