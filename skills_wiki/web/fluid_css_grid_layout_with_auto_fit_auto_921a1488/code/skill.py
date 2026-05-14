def create_component(
    output_dir: str,
    title_text: str = "Mushroom Field Guide",
    body_text: str = "Explore different species using a fluid, media-query-free grid. Use the controls to filter items and observe the difference between auto-fit and auto-fill.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#2ea043",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid CSS Grid Layout effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_primary = "#ffffff"
        text_secondary = "#a0a0a0"
        card_hover = "#2a2a2a"
    else:
        bg_color = "#f4f4f5"
        surface_color = "#ffffff"
        border_color = "#e4e4e7"
        text_primary = "#18181b"
        text_secondary = "#71717a"
        card_hover = "#f9f9fb"

    # === CSS ===
    css = f"""/* Fluid Grid Layout Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --card-hover: {card_hover};
    --grid-min-col-size: 250px;
}}

body {{
    font-family: system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    /* Height constraint for demo purposes */
    min-height: {height_px}px; 
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: left;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-secondary);
    line-height: 1.5;
    max-width: 600px;
}}

/* Controls UI */
.controls {{
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
    background: var(--surface);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}}

.control-group {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.control-group label {{
    font-weight: 600;
    font-size: 0.9rem;
}}

select, button {{
    background: var(--bg);
    color: var(--text-primary);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}}

select:hover, button:hover {{
    border-color: var(--accent);
}}

button.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}}

/* === The Core Grid Magic === */
.fluid-grid {{
    display: grid;
    gap: 1.5rem;
    /* Default behavior: auto-fit with overflow protection */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-min-col-size)), 1fr));
}}

/* Modifier for auto-fill demonstration */
.fluid-grid[data-layout-mode="auto-fill"] {{
    grid-template-columns: repeat(auto-fill, minmax(min(100%, var(--grid-min-col-size)), 1fr));
}}

/* Card Styles */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
}}

.card:hover {{
    transform: translateY(-2px);
    background-color: var(--card-hover);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.card[data-hidden="true"] {{
    display: none;
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 700;
}}

.badge {{
    background: rgba(46, 160, 67, 0.15); /* Accent tint */
    color: var(--accent);
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.card-desc {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1;
}}

.card-footer {{
    font-size: 0.85rem;
    padding-top: 1rem;
    border-top: 1px dashed var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.tag {{
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
}}
"""

    # === HTML ===
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
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <div class="control-group">
                <label>Grid Mode:</label>
                <select id="mode-select">
                    <option value="auto-fit">auto-fit (Stretches items to fill)</option>
                    <option value="auto-fill">auto-fill (Leaves empty gaps)</option>
                </select>
            </div>
            <div class="control-group">
                <label>Filter Season:</label>
                <button class="filter-btn active" data-season="all">All</button>
                <button class="filter-btn" data-season="spring">Spring</button>
                <button class="filter-btn" data-season="summer">Summer</button>
            </div>
        </div>

        <main class="fluid-grid" id="grid" data-layout-mode="auto-fit">
            
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Chanterelle</h2>
                    <span class="badge" style="color: #e3b341; background: rgba(227, 179, 65, 0.15)">Edible</span>
                </div>
                <p class="card-desc">Golden-yellow, funnel-shaped mushroom with false gills running down the stem.</p>
                <div class="card-footer">
                    <span class="tag">Summer</span>
                    <span class="tag">Deciduous Forests</span>
                </div>
            </article>

            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">Morel</h2>
                    <span class="badge">Edible</span>
                </div>
                <p class="card-desc">Distinctive honeycomb-like cap structure. Must be cooked thoroughly before eating.</p>
                <div class="card-footer">
                    <span class="tag">Spring</span>
                    <span class="tag">Elm/Ash Trees</span>
                </div>
            </article>

            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Death Cap</h2>
                    <span class="badge" style="color: #ff4d4d; background: rgba(255, 77, 77, 0.15)">Toxic</span>
                </div>
                <p class="card-desc">Pale green to white cap with white gills. Extremely toxic, responsible for most fatal poisonings.</p>
                <div class="card-footer">
                    <span class="tag">Summer</span>
                    <span class="tag">Oak Trees</span>
                </div>
            </article>

            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Chicken of the Woods</h2>
                    <span class="badge">Edible</span>
                </div>
                <p class="card-desc">Bright orange bracket fungus with yellow edges. Grows in overlapping clusters on living or dead trees.</p>
                <div class="card-footer">
                    <span class="tag">Summer</span>
                    <span class="tag">Hardwoods</span>
                </div>
            </article>

            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">False Morel</h2>
                    <span class="badge" style="color: #ff4d4d; background: rgba(255, 77, 77, 0.15)">Toxic</span>
                </div>
                <p class="card-desc">Brain-like, reddish-brown cap with irregular shape. Highly toxic, often confused with true morels.</p>
                <div class="card-footer">
                    <span class="tag">Spring</span>
                    <span class="tag">Coniferous Forests</span>
                </div>
            </article>

             <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Oyster Mushroom</h2>
                    <span class="badge">Edible</span>
                </div>
                <p class="card-desc">Fan-shaped caps growing in shelf-like clusters on dead wood. White to light brown.</p>
                <div class="card-footer">
                    <span class="tag">Summer</span>
                    <span class="tag">Dead Wood</span>
                </div>
            </article>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Grid Interactive Demo
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    const modeSelect = document.getElementById('mode-select');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');

    // Toggle between auto-fit and auto-fill
    modeSelect.addEventListener('change', (e) => {{
        grid.setAttribute('data-layout-mode', e.target.value);
    }});

    // Filter cards to demonstrate how layout adapts with fewer items
    filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            // Update active button state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const season = btn.getAttribute('data-season');

            // Hide/Show cards based on dataset
            cards.forEach(card => {{
                if (season === 'all' || card.getAttribute('data-season') === season) {{
                    card.removeAttribute('data-hidden');
                }} else {{
                    card.setAttribute('data-hidden', 'true');
                }}
            }});
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
