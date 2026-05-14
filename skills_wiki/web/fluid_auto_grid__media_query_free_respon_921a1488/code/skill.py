def create_component(
    output_dir: str,
    title_text: str = "Fluid Auto-Grid Layout",
    body_text: str = "Drag the bottom-right corner of this window to see the grid automatically re-flow. Try filtering items to see the difference between auto-fit and auto-fill.",
    color_scheme: str = "dark",
    accent_color: str = "#10b981",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        panel_bg = "#1e293b"
        card_bg = "#0f172a"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        border_color = "#334155"
    else:
        bg_color = "#f1f5f9"
        panel_bg = "#ffffff"
        card_bg = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        border_color = "#e2e8f0"

    css = f"""/* Fluid Auto-Grid Component */
:root {{
    --bg-window: {bg_color};
    --bg-panel: {panel_bg};
    --bg-card: {card_bg};
    --text-main: {text_primary};
    --text-muted: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    
    /* The core layout variable */
    --grid-min-col: 260px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000;
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
}}

/* Resizable Demo Window */
.demo-window {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    background-color: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    resize: both;
    overflow: auto;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Header & Controls */
header {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

h1 {{
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

p {{
    color: var(--text-muted);
    line-height: 1.5;
    max-width: 600px;
}}

.controls {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}}

button {{
    background: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

button.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}}

/* =========================================
   THE MAGIC GRID 
   ========================================= */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
       1. repeat(): Loops the column definition
       2. auto-fit: Creates as many columns as fit, collapses empty ones
       3. minmax(): Floor and ceiling size
       4. min(): The floor is 260px, UNLESS the container is smaller than 260px, then it's 100%
       5. 1fr: The ceiling allows items to stretch evenly
    */
    grid-template-columns: repeat(
        auto-fit, 
        minmax(min(var(--grid-min-col), 100%), 1fr)
    );
    
    align-content: start;
}}

/* Auto-fill mode class for demonstration */
.mushroom-grid.mode-autofill {{
    grid-template-columns: repeat(
        auto-fill, 
        minmax(min(var(--grid-min-col), 100%), 1fr)
    );
}}
/* ========================================= */

.card {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, border-color 0.2s ease, opacity 0.3s ease;
}}

.card.hidden {{
    display: none;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--text-muted);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-main);
}}

.tags {{
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}}

.tag.edible {{ background: rgba(16, 185, 129, 0.15); color: #10b981; }}
.tag.toxic {{ background: rgba(239, 68, 68, 0.15); color: #ef4444; }}
.tag.spring {{ background: rgba(59, 130, 246, 0.15); color: #3b82f6; }}
.tag.summer {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; }}

.card-body p {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.important-note {{
    margin-top: auto; /* pushes note to bottom if heights differ */
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--text-muted);
}}
.important-note strong {{
    color: var(--text-main);
}}

/* Scrollbar styling for the demo window */
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: var(--bg-panel); border-radius: 4px; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}
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

    <div class="demo-window">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            
            <div class="controls">
                <div class="button-group filter-group">
                    <button class="active" data-filter="all">Show All</button>
                    <button data-filter="spring">Spring Only</button>
                </div>
                <div class="button-group mode-group" style="margin-left: auto;">
                    <button class="active" data-mode="auto-fit">Mode: auto-fit (Stretch)</button>
                    <button data-mode="auto-fill">Mode: auto-fill (Gap)</button>
                </div>
            </div>
        </header>

        <main class="mushroom-grid" id="grid">
            <!-- Card 1 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Chanterelle</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag summer">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Golden-yellow, funnel-shaped mushroom with false gills running down the stem.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> Has toxic look-alikes.
                </div>
            </article>

            <!-- Card 2 -->
            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">Morel</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag spring">Spring</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Distinctive honeycomb-like cap structure attached directly to the stem.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> Must be cooked before eating.
                </div>
            </article>

            <!-- Card 3 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Death Cap</h2>
                    <div class="tags">
                        <span class="tag toxic">Toxic</span>
                        <span class="tag summer">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Pale green to white cap with white gills and a sac-like base at the bottom of the stem.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> Extremely toxic - study for safety.
                </div>
            </article>

            <!-- Card 4 -->
            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2 class="card-title">Oyster Mushroom</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag spring">Spring</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Fan-shaped caps growing in overlapping shelf-like clusters on dead wood.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> Great beginner mushroom.
                </div>
            </article>

            <!-- Card 5 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Lion's Mane</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag summer">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>White, shaggy appearance resembling a cascading waterfall of icicles.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> No toxic look-alikes.
                </div>
            </article>

             <!-- Card 6 -->
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2 class="card-title">Destroying Angel</h2>
                    <div class="tags">
                        <span class="tag toxic">Toxic</span>
                        <span class="tag summer">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Pure white mushroom with a sack-like base and a skirt-like ring on the stem.</p>
                </div>
                <div class="important-note">
                    <strong>Note:</strong> Deadly toxic.
                </div>
            </article>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const cards = document.querySelectorAll('.card');
    
    // Filtering logic to demonstrate how grid reflows
    const filterBtns = document.querySelectorAll('.filter-group button');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const filter = e.target.getAttribute('data-filter');
            
            cards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-season') === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    // Auto-fit vs Auto-fill toggle logic
    const modeBtns = document.querySelectorAll('.mode-group button');
    modeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active state
            modeBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const mode = e.target.getAttribute('data-mode');
            
            if (mode === 'auto-fill') {
                grid.classList.add('mode-autofill');
            } else {
                grid.classList.remove('mode-autofill');
            }
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
