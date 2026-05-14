def create_component(
    output_dir: str,
    title_text: str = "Get to know your mushrooms",
    body_text: str = "A responsive grid demonstrating auto-fit vs auto-fill.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80", 
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid Engine.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#161618"
        card_bg = "#222224"
        text_primary = "#f3f4f6"
        text_secondary = "#9ca3af"
        border_color = "#374151"
        tag_bg = "#1f2937"
    else:
        bg_color = "#f9fafb"
        card_bg = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        border_color = "#e5e7eb"
        tag_bg = "#f3f4f6"

    css = f"""/* Responsive Grid Engine CSS */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --border-color: {border_color};
    --tag-bg: {tag_bg};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.5;
    padding: 2rem;
    display: flex;
    justify-content: center;
    min-height: 100vh;
}}

.main-wrapper {{
    width: 100%;
    max-width: {width_px}px;
}}

header {{
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

p.subtitle {{
    color: var(--text-secondary);
    margin-bottom: 2rem;
}}

/* Controls */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
    align-items: center;
    background: var(--card-bg);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}}

.control-group {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.control-label {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 0.5rem;
}}

button {{
    background: var(--tag-bg);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

button:hover {{
    border-color: var(--text-secondary);
}}

button.active {{
    background: var(--accent-color);
    color: #000;
    border-color: var(--accent-color);
}}

/* === THE CORE GRID ENGINE === */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
       Variables for the grid engine:
       --min-col-size sets the preferred minimum width of a card.
       --placement toggles between auto-fit and auto-fill.
    */
    --min-col-size: 275px;
    --placement: auto-fill; /* Defaulting to auto-fill for filtering */
    
    grid-template-columns: repeat(
        var(--placement), 
        minmax(min(var(--min-col-size), 100%), 1fr)
    );
}}

/* Cards */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}}

.card.hidden {{
    display: none;
}}

.card-header h2 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    background: var(--tag-bg);
    color: var(--accent-color);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.tag.toxic {{ color: #ef4444; }}
.tag.edible {{ color: #4ade80; }}

.card-body p {{
    font-size: 0.95rem;
    color: var(--text-secondary);
}}

.important-note {{
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.875rem;
}}

.important-note strong {{
    color: var(--text-primary);
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
    <div class="main-wrapper">
        <header>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <div class="controls">
            <div class="control-group">
                <span class="control-label">Layout Engine:</span>
                <button class="toggle-btn active" data-placement="auto-fill">auto-fill (Best for filters)</button>
                <button class="toggle-btn" data-placement="auto-fit">auto-fit (Stretches items)</button>
            </div>
            <div class="control-group" style="margin-left: auto;">
                <span class="control-label">Filter Season:</span>
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="spring">Spring</button>
                <button class="filter-btn" data-filter="summer">Summer</button>
            </div>
        </div>

        <main class="mushroom-grid" id="grid">
            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2>Chanterelle</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Golden-yellow, funnel-shaped mushroom with false gills.</p>
                </div>
                <div class="important-note">
                    <strong>Important notes:</strong> Has toxic look-alikes.
                </div>
            </article>

            <article class="card" data-season="spring">
                <div class="card-header">
                    <h2>Morel</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag">Spring</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Distinctive honeycomb-like cap structure. Found near dead elms.</p>
                </div>
                <div class="important-note">
                    <strong>Important notes:</strong> Must be cooked before eating.
                </div>
            </article>

            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2>Chicken of the Woods</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Bright orange bracket fungus with yellow edges. Tastes like chicken.</p>
                </div>
                <div class="important-note">
                    <strong>Important notes:</strong> Avoid if growing on conifers.
                </div>
            </article>

            <article class="card" data-season="summer">
                <div class="card-header">
                    <h2>Death Cap</h2>
                    <div class="tags">
                        <span class="tag toxic">Toxic</span>
                        <span class="tag">Summer</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Pale green to white cap with white gills. Extremely dangerous.</p>
                </div>
                <div class="important-note">
                    <strong>Important notes:</strong> Extremely toxic - study for safety awareness.
                </div>
            </article>

            <article class="card" data-season="all">
                <div class="card-header">
                    <h2>Oyster Mushroom</h2>
                    <div class="tags">
                        <span class="tag edible">Edible</span>
                        <span class="tag">All Year</span>
                    </div>
                </div>
                <div class="card-body">
                    <p>Fan-shaped caps growing in overlapping clusters on deciduous wood.</p>
                </div>
                <div class="important-note">
                    <strong>Important notes:</strong> Great beginner mushroom.
                </div>
            </article>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const cards = document.querySelectorAll('.card');

    // Handle Layout Engine Toggle (auto-fit vs auto-fill)
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state UI
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update CSS Variable on the grid container
            const placement = btn.getAttribute('data-placement');
            grid.style.setProperty('--placement', placement);
        });
    });

    // Handle Item Filtering
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state UI
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Filter logic
            const filter = btn.getAttribute('data-filter');
            
            cards.forEach(card => {
                const season = card.getAttribute('data-season');
                if (filter === 'all' || season === filter || season === 'all') {
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
