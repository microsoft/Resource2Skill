def create_component(
    output_dir: str,
    title_text: str = "Grid Master Dashboard",
    body_text: str = "A responsive Bento Box layout demonstrating advanced CSS Grid techniques without media queries.",
    color_scheme: str = "dark",
    accent_color: str = "#8a2be2",
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Box Grid System.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#f4f4f5"
        text_muted = "#a1a1aa"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Responsive Bento Grid System */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
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
    justify-content: center;
    align-items: center;
    padding: 2rem;
}}

.dashboard-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: left;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* === CORE SKILL: THE BENTO GRID === */
.bento-grid {{
    display: grid;
    /* Responsive without media queries: auto-fit + minmax */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    /* Dense flow fills empty gaps left by spanned items */
    grid-auto-flow: dense;
    gap: 1.25rem;
    /* Explicitly define row heights so spans look proportionate */
    grid-auto-rows: 240px; 
}}

/* Grid Item Base Styles */
.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    overflow: hidden;
    position: relative;
}}

.bento-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    border-color: var(--accent);
    background: var(--surface-hover);
}}

/* === SKILL: GRID SPANNING === */
.span-col-2 {{
    grid-column: span 2;
}}

.span-row-2 {{
    grid-row: span 2;
}}

/* Handle smaller screens gracefully where span 2 breaks the minmax constraints */
@media (max-width: 600px) {{
    .span-col-2 {{
        grid-column: span 1;
    }}
}}

/* === SKILL: INTERNAL GRID LAYERING (Z-INDEX TRICK) === */
.overlap-container {{
    display: grid;
    grid-template-areas: "stack";
    /* Override padding for full bleed */
    padding: 0; 
}}

.overlap-bg, .overlap-content {{
    /* Both occupy the exact same grid area */
    grid-area: stack; 
}}

.overlap-bg {{
    background: linear-gradient(135deg, var(--accent) 0%, transparent 100%);
    opacity: 0.15;
    z-index: 1;
}}

.overlap-content {{
    z-index: 2;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}

/* Typography inside cards */
.item-tag {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
    margin-bottom: auto;
    font-weight: 600;
}}

.item-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

h2.large-title {{
    font-size: 2.5rem;
    margin-top: auto;
}}

.item-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
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
    <div class="dashboard-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid">
            <!-- Hero Card: Spans 2 cols, 2 rows. Uses Grid overlapping -->
            <article class="bento-item span-col-2 span-row-2 overlap-container">
                <div class="overlap-bg"></div>
                <div class="overlap-content">
                    <span class="item-tag">Featured System</span>
                    <h2 class="item-title large-title">Implicit & Explicit Control</h2>
                    <p class="item-desc">Using overlapping grid areas, we can stack graphical elements and text directly on top of each other without absolute positioning.</p>
                </div>
            </article>

            <!-- Standard Card -->
            <article class="bento-item">
                <span class="item-tag">Fractional Units</span>
                <h2 class="item-title">1fr Magic</h2>
                <p class="item-desc">Distributes remaining available space equally among tracks.</p>
            </article>

            <!-- Tall Card: Spans 2 rows -->
            <article class="bento-item span-row-2">
                <span class="item-tag">Alignment</span>
                <h2 class="item-title">Justify & Align</h2>
                <p class="item-desc">Total 2D control over where items sit inside their designated cells using justify-items and align-items.</p>
            </article>

            <!-- Wide Card: Spans 2 cols -->
            <article class="bento-item span-col-2">
                <span class="item-tag">Responsiveness</span>
                <h2 class="item-title">Auto-Fit & MinMax</h2>
                <p class="item-desc">This layout mathematically recalculates columns based on container width. Resize the window to watch it reflow without breakpoints.</p>
            </article>

            <!-- Standard Card -->
            <article class="bento-item">
                <span class="item-tag">Gutters</span>
                <h2 class="item-title">Gap Property</h2>
                <p class="item-desc">Creates consistent spacing between grid tracks without margin math.</p>
            </article>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Bento Box Grid
// The core logic of this layout is handled entirely by CSS Grid.

document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-item');
    
    // Optional: Add a subtle entry animation
    cards.forEach((card, index) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {{
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease, box-shadow 0.3s ease, border-color 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }}, 100 * index); // Staggered delay
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
