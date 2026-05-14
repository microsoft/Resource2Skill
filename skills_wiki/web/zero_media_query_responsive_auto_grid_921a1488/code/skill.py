def create_component(
    output_dir: str,
    title_text: str = "Mushroom Reference Guide",
    body_text: str = "Explore our responsive grid. Toggle the layout mode and filter to see how auto-fit and auto-fill react to varying content amounts.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        surface_hover = "#2a2a2a"
        text_color = "#f0f0f0"
        text_muted = "#a0a0a0"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f5f7"
        surface_color = "#ffffff"
        surface_hover = "#f8f9fa"
        text_color = "#1a1a1a"
        text_muted = "#666666"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Zero-Media-Query Grid Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --text: {text_color};
    --text-muted: {text_muted};
    --border: {border_color};
    --accent: {accent_color};
    --toxic: #ef5350;
    
    /* Configurable Grid Property */
    --grid-mode: auto-fit;
    --min-col-size: 275px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
}}

.header {{
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.5;
    max-width: 600px;
    margin-bottom: 1.5rem;
}}

/* Controls UI */
.controls {{
    display: flex;
    gap: 1.5rem;
    align-items: center;
    background: var(--surface);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    margin-bottom: 2rem;
    flex-wrap: wrap;
}}

.control-group {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.control-group label {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-right: 0.5rem;
}}

button, select {{
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}}

button.active, button:hover {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}}

/* THE CORE GRID PATTERN */
.mushroom-grid {{
    display: grid;
    /* 
       1. repeat(var(--grid-mode), ...) toggles between auto-fit and auto-fill 
       2. minmax(...) sets lower and upper bounds
       3. min(275px, 100%) prevents horizontal overflow on screens narrower than 275px
    */
    grid-template-columns: repeat(var(--grid-mode), minmax(min(var(--min-col-size), 100%), 1fr));
    gap: 1.5rem;
    align-items: start;
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
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                opacity 0.3s ease;
    height: 100%;
}}

.card.hidden {{
    display: none;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    background: var(--surface-hover);
    border-color: rgba(255, 255, 255, 0.2);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    line-height: 1.2;
}}

.tag-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.tag {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}}

.tag.edible {{ background: rgba(76, 175, 80, 0.15); color: var(--accent); }}
.tag.toxic {{ background: rgba(239, 83, 80, 0.15); color: var(--toxic); }}
.tag.season {{ background: rgba(255, 255, 255, 0.1); color: var(--text-muted); border: 1px solid var(--border); }}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
    flex-grow: 1;
}}

.card-notes {{
    background: rgba(0,0,0,0.2);
    padding: 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    border-left: 3px solid var(--accent);
}}
.card.toxic-card .card-notes {{
    border-left-color: var(--toxic);
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
    <main class="app-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <div class="control-group">
                <label>Grid Mode:</label>
                <select id="grid-mode-select">
                    <option value="auto-fit">auto-fit (Stretches to fill)</option>
                    <option value="auto-fill">auto-fill (Leaves blank space)</option>
                </select>
            </div>
            <div class="control-group">
                <label>Filter Season:</label>
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="spring">Spring</button>
                <button class="filter-btn" data-filter="summer">Summer</button>
            </div>
        </div>

        <div class="mushroom-grid" id="grid">
            <!-- Card 1 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Chanterelle</h2>
                </div>
                <div class="tag-list">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Golden-yellow, funnel-shaped mushroom with false gills running down the stem.</p>
                <div class="card-notes">
                    <strong>Important:</strong> Has toxic look-alikes - learn proper identification.
                </div>
            </article>

            <!-- Card 2 -->
            <article class="card toxic-card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">False Morel</h2>
                </div>
                <div class="tag-list">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Brain-like, reddish-brown cap with irregular shape. Highly dangerous raw.</p>
                <div class="card-notes">
                    <strong>Important:</strong> Highly toxic - often confused with true morels.
                </div>
            </article>

            <!-- Card 3 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Chicken of the Woods</h2>
                </div>
                <div class="tag-list">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Bright orange bracket fungus with yellow edges. Tastes surprisingly like chicken.</p>
                <div class="card-notes">
                    <strong>Important:</strong> Avoid if growing on certain tree species like Eucalyptus.
                </div>
            </article>

            <!-- Card 4 -->
            <article class="card toxic-card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Death Cap</h2>
                </div>
                <div class="tag-list">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Pale green to white cap with white gills and a distinct base sac.</p>
                <div class="card-notes">
                    <strong>Important:</strong> Extremely toxic - study strictly for safety awareness.
                </div>
            </article>
            
            <!-- Card 5 -->
            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">Morel</h2>
                </div>
                <div class="tag-list">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Distinctive honeycomb-like cap structure with a hollow interior.</p>
                <div class="card-notes">
                    <strong>Important:</strong> Must be cooked before eating.
                </div>
            </article>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const modeSelect = document.getElementById('grid-mode-select');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');

    // 1. Toggle between auto-fit and auto-fill using CSS variables
    modeSelect.addEventListener('change', (e) => {
        // We set the CSS variable on the root, which updates the grid dynamically
        document.documentElement.style.setProperty('--grid-mode', e.target.value);
    });

    // 2. Filter logic to demonstrate why auto-fill is useful when items are removed
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active button state
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');

            const filter = e.target.getAttribute('data-filter');

            // Filter cards
            cards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-season') === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
});
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
