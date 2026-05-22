def create_component(
    output_dir: str,
    title_text: str = "Adaptive Bento Grid",
    body_text: str = "A modern, asymmetric layout pattern utilizing CSS grid-template-areas and grid-stacking for responsive, tactile design.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Adaptive Bento Grid Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base Colors
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_bg = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.08)"
        glow_color = f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.15)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_bg = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.08)"
        glow_color = f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.12)"

    css = f"""/* Adaptive Bento Grid Layout */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_bg};
    --border: {border_color};
    --glow: {glow_color};
    --max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.header h1 span {{
    color: var(--accent);
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 1.1rem;
}}

/* --- Core Grid Layout --- */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    gap: 1.5rem;
    /* 4 Column Baseline Setup */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(280px, auto);
    /* Visual ASCII Mapping */
    grid-template-areas:
        "hero hero sec-top sec-top"
        "hero hero sec-bot-l sec-bot-r";
}}

/* --- Cards Styling --- */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease;
}}

/* Glow Effect Base */
.bento-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(800px circle at var(--mouse-x, 0) var(--mouse-y, 0), var(--glow), transparent 40%);
    opacity: 0;
    transition: opacity 0.5s ease;
    z-index: 0;
    pointer-events: none;
}}

.bento-grid:hover .bento-card::before {{
    opacity: 1;
}}

.bento-card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
}}

.bento-card > * {{
    z-index: 1; /* Keep content above the glow */
}}

.bento-card h3 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.bento-card p {{
    color: var(--text-muted);
    line-height: 1.5;
}}

/* --- Area Assignments --- */
.card-hero {{
    grid-area: hero;
    /* Implement Grid Stacking inside the Hero card */
    display: grid;
    padding: 0;
}}

.card-hero .content-layer, 
.card-hero .bg-layer {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.card-hero .bg-layer {{
    background: linear-gradient(135deg, var(--surface) 0%, var(--glow) 100%);
    opacity: 0.3;
    border-radius: 24px;
}}

.card-hero .content-layer {{
    padding: 3rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}

.card-hero h3 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.card-sec-top {{
    grid-area: sec-top;
    justify-content: center;
}}

.card-sec-bot-l {{
    grid-area: sec-bot-l;
}}

.card-sec-bot-r {{
    grid-area: sec-bot-r;
}}

.icon-wrapper {{
    height: 48px;
    width: 48px;
    background: rgba(139, 92, 246, 0.1);
    color: var(--accent);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
}}

/* --- Responsive Reflows --- */

/* Tablet: Move to a 2-column or adjusted 3-column layout */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "sec-top sec-top"
            "sec-bot-l sec-bot-r";
    }}
}}

/* Mobile: Single Column Stack */
@media (max-width: 640px) {{
    .bento-grid {{
        display: flex;
        flex-direction: column;
    }}
    .card-hero h3 {{
        font-size: 1.8rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{title_text.replace(title_text.split()[-1], f"<span>{title_text.split()[-1]}</span>")}</h1>
        <p>{body_text}</p>
    </header>

    <main class="bento-grid" id="bento">
        <!-- Hero Card utilizing Grid Stacking -->
        <article class="bento-card card-hero">
            <div class="bg-layer"></div>
            <div class="content-layer">
                <div class="icon-wrapper">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                </div>
                <h3>Grid Stacking</h3>
                <p>This layout uses CSS Grid overlay mechanics (grid-column: 1 / -1) to layer background gradients and text without brittle absolute positioning.</p>
            </div>
        </article>

        <!-- Top Secondary Card -->
        <article class="bento-card card-sec-top">
            <div class="icon-wrapper">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h7"/></svg>
            </div>
            <h3>Template Areas</h3>
            <p>Layout mapped via intuitive ASCII-like strings. Rearranging this grid across breakpoints only requires altering a single string per media query.</p>
        </article>

        <!-- Bottom Left Card -->
        <article class="bento-card card-sec-bot-l">
            <h3>Responsive</h3>
            <p>Automatic reflowing adapts the layout flawlessly from desktop down to mobile dimensions.</p>
        </article>

        <!-- Bottom Right Card -->
        <article class="bento-card card-sec-bot-r">
            <h3>Interactive</h3>
            <p>Move your cursor. JS tracks coordinates to map a smooth, localized radial glow over the grid cells.</p>
        </article>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Cursor Glow Tracking logic for the Bento Grid
document.addEventListener('DOMContentLoaded', () => {{
    const bentoContainer = document.getElementById('bento');
    const cards = document.querySelectorAll('.bento-card');

    // Update custom properties on mousemove
    bentoContainer.addEventListener('mousemove', (e) => {{
        for(const card of cards) {{
            const rect = card.getBoundingClientRect();
            
            // Calculate mouse position relative to each card
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Set CSS variables for the radial-gradient position
            card.style.setProperty('--mouse-x', `${{x}}px`);
            card.style.setProperty('--mouse-y', `${{y}}px`);
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
