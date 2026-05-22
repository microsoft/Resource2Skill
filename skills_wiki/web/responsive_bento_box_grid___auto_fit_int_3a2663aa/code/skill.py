def create_component(
    output_dir: str,
    title_text: str = "Bento Grid System",
    body_text: str = "A fully responsive, fluid layout utilizing CSS Grid auto-fit, minmax(), and fractional units to naturally reflow without complex media queries.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Box Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        text_muted = "#8b949e"
        surface_color = "rgba(255, 255, 255, 0.02)"
        surface_hover = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.06)"
        border_hover = "rgba(255, 255, 255, 0.15)"
        spotlight_color = "rgba(255, 255, 255, 0.06)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#1a1a2e"
        text_muted = "#5c6573"
        surface_color = "#ffffff"
        surface_hover = "#fdfdfd"
        border_color = "rgba(0, 0, 0, 0.06)"
        border_hover = "rgba(0, 0, 0, 0.12)"
        spotlight_color = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Bento Grid System */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
    --spotlight: {spotlight_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    /* Subtle Blueprint Grid Background */
    background-image: 
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: -1px -1px;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    position: relative;
}}

.bento-grid {{
    display: grid;
    /* The core responsive magic: */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    grid-auto-rows: minmax(220px, auto);
    grid-auto-flow: dense;
    gap: 1.5rem;
    width: 100%;
}}

.bento-item {{
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), 
                border-color 0.4s ease, 
                box-shadow 0.4s ease, 
                background 0.4s ease;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}}

/* Dynamic Hover Effect */
.bento-item:hover {{
    transform: translateY(-6px);
    border-color: var(--border-hover);
    background: var(--surface-hover);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}}

/* JS Spotlight Overlay */
.bento-item::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(
        800px circle at var(--mouse-x, 0) var(--mouse-y, 0), 
        var(--spotlight), 
        transparent 40%
    );
    z-index: 1;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s ease;
}}

.bento-grid:hover .bento-item::before {{
    opacity: 1;
}}

/* Content z-index so text stays above spotlight */
.item-content {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
}}

/* Typography */
.tag {{
    align-self: flex-start;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1.5rem;
}}

.bento-item h3 {{
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    line-height: 1.2;
}}

.bento-item p {{
    color: var(--text-muted);
    font-size: 1rem;
    line-height: 1.6;
}}

/* Explicit Spanning System */
.bento-item.large {{
    grid-column: span 2;
    grid-row: span 2;
    background: linear-gradient(145deg, var(--surface), transparent);
}}

.bento-item.large .title {{
    font-size: 2.75rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.1;
    letter-spacing: -0.03em;
}}

.bento-item.large .body-text {{
    font-size: 1.15rem;
    max-width: 90%;
}}

.bento-item.wide {{
    grid-column: span 2;
}}

.bento-item.tall {{
    grid-row: span 2;
}}

/* Graphic Visualizations */
.meta-visual {{
    margin-top: auto;
    padding-top: 2rem;
    position: relative;
}}

.grid-illustration {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    opacity: 0.8;
    transition: transform 0.4s ease;
}}

.bento-item.large:hover .grid-illustration {{
    transform: scale(1.02);
}}

.g-box {{
    height: 48px;
    border-radius: 8px;
    background: var(--border);
}}

.g-box.filled {{ background: var(--accent); }}
.g-box.span-2 {{ grid-column: span 2; }}

.fr-visual {{
    display: flex;
    gap: 0.5rem;
    height: 36px;
    width: 100%;
}}

.fr-bar {{
    background: transparent;
    border: 1px dashed var(--accent);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--accent);
}}

.fr-bar.filled {{
    background: var(--accent);
    color: var(--bg);
    border-style: solid;
}}

.align-visual {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    height: 120px;
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 0.5rem;
}}

.dot {{
    width: 12px;
    height: 12px;
    background: var(--border-hover);
    border-radius: 50%;
}}

/* Fallback for smaller screens to prevent span overflows */
@media (max-width: 768px) {{
    .bento-item.large,
    .bento-item.wide {{
        grid-column: 1 / -1;
    }}
    .bento-item.large {{
        grid-row: span 1;
    }}
    .bento-item.large .title {{
        font-size: 2rem;
    }}
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
    <div class="container">
        <div class="bento-grid">
            
            <!-- Hero Spanning Item -->
            <div class="bento-item large">
                <div class="item-content">
                    <div class="tag">Auto-Fit CSS Grid</div>
                    <h1 class="title">{title_text}</h1>
                    <p class="body-text">{body_text}</p>
                    
                    <div class="meta-visual">
                        <div class="grid-illustration">
                            <div class="g-box filled span-2"></div>
                            <div class="g-box"></div>
                            <div class="g-box"></div>
                            <div class="g-box"></div>
                            <div class="g-box filled span-2"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Wide Item -->
            <div class="bento-item wide">
                <div class="item-content">
                    <h3>Implicit Tracks & Flow</h3>
                    <p>Using <code>grid-auto-rows</code> and <code>grid-auto-flow: dense</code>, items naturally backfill gaps and generate new rows instantly.</p>
                </div>
            </div>

            <!-- Tall Item -->
            <div class="bento-item tall">
                <div class="item-content">
                    <h3>Fractional Dynamics</h3>
                    <p>The <code>1fr</code> unit dynamically calculates and distributes leftover available space equitably.</p>
                    <div class="meta-visual">
                        <div class="fr-visual">
                            <div class="fr-bar" style="flex: 1;">1fr</div>
                            <div class="fr-bar filled" style="flex: 2;">2fr</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Standard Items -->
            <div class="bento-item">
                <div class="item-content">
                    <h3>Alignment Axes</h3>
                    <p>Control exact placement inside cells.</p>
                    <div class="meta-visual">
                        <div class="align-visual">
                            <div class="dot" style="align-self: start; justify-self: start;"></div>
                            <div class="dot" style="align-self: center; justify-self: center; background: var(--accent); transform: scale(1.5);"></div>
                            <div class="dot" style="align-self: end; justify-self: end;"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bento-item">
                <div class="item-content">
                    <h3>Explicit Spans</h3>
                    <p>Break the mold by declaring <code>grid-column: span X</code> to span multiple defined tracks.</p>
                </div>
            </div>

            <div class="bento-item wide">
                <div class="item-content" style="flex-direction: row; align-items: center; justify-content: space-between;">
                    <div>
                        <h3>Zero Media Queries</h3>
                        <p>Fluidly wraps elements via `minmax()` boundaries.</p>
                    </div>
                    <div style="font-size: 2rem; opacity: 0.8;">⚙️</div>
                </div>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Spotlight tracking for Bento items
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.querySelector('.bento-grid');
    const items = document.querySelectorAll('.bento-item');

    // Attach event listener to the grid container
    grid.addEventListener('mousemove', (e) => {{
        // Update variables for each item to track relative mouse position
        items.forEach(item => {{
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Set CSS custom properties
            item.style.setProperty('--mouse-x', `${{x}}px`);
            item.style.setProperty('--mouse-y', `${{y}}px`);
        }});
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
