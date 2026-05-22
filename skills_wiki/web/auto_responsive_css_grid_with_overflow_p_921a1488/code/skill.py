def create_component(
    output_dir: str,
    title_text: str = "Mushroom Reference Guide",
    body_text: str = "Filter the cards below and toggle the Grid Mode. Notice how 'auto-fill' preserves card sizes when few items are visible, while 'auto-fit' awkwardly stretches them.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_color = "#f5f5f5"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        border_color = "#e0e0e0"
        text_color = "#1a1a2e"
        text_muted = "#666666"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --grid-min-col-size: 275px;
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem 1rem;
    line-height: 1.5;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
}}

header {{
    margin-bottom: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 65ch;
}}

.controls-wrapper {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}}

.filters {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.filter-btn {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.filter-btn:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

.filter-btn.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: {bg_color};
}}

.grid-mode-control {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--surface);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}}

.grid-mode-control label {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}}

.grid-mode-control select {{
    background: transparent;
    color: var(--text);
    border: none;
    font-family: inherit;
    font-size: 0.95rem;
    cursor: pointer;
    outline: none;
}}

/* =========================================
   THE CORE TECHNIQUE
   ========================================= */
.grid-container {{
    display: grid;
    gap: 1.5rem;
    
    /* 
      1. auto-fill: Keeps column sizes rigid and creates empty tracks, preventing stretching
      2. minmax: Sets the bounds for the columns
      3. min(275px, 100%): Ensures columns don't overflow viewports smaller than 275px 
    */
    grid-template-columns: repeat(auto-fill, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

.grid-container.mode-fit {{
    grid-template-columns: repeat(auto-fit, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

/* Card Styling */
.card {{
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: color-mix(in srgb, var(--accent) 50%, transparent);
}}

.card-tag {{
    align-self: flex-start;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    margin-bottom: 1.25rem;
}}

.card-title {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    flex-grow: 1;
}}
"""

    # === HTML ===
    # Generate mock card data
    categories = ["spring", "summer", "autumn"]
    labels = ["Spring", "Summer", "Autumn"]
    
    cards_html = ""
    for i in range(1, 10):
        idx = i % 3
        cat = categories[idx]
        label = labels[idx]
        cards_html += f"""
        <div class="card" data-category="{cat}">
            <span class="card-tag">{label}</span>
            <h3 class="card-title">Grid Item {i}</h3>
            <p class="card-desc">This responsive item will adapt to the grid mathematically. Try filtering down to just a few items to see how the layout reacts.</p>
        </div>"""

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
    <div class="container">
        <header>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="controls-wrapper">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="spring">Spring</button>
                <button class="filter-btn" data-filter="summer">Summer</button>
                <button class="filter-btn" data-filter="autumn">Autumn</button>
            </div>

            <div class="grid-mode-control">
                <label for="mode-select">Behavior</label>
                <select id="mode-select">
                    <option value="auto-fill">auto-fill (Rigid Columns)</option>
                    <option value="auto-fit">auto-fit (Stretching Columns)</option>
                </select>
            </div>
        </div>

        <div class="grid-container" id="card-grid">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const filters = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');
    const modeSelect = document.getElementById('mode-select');
    const grid = document.getElementById('card-grid');

    // Filter Logic
    filters.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filters.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filterValue = btn.dataset.filter;
            
            // Toggle visibility. CSS grid auto-collapses 'display: none' elements
            cards.forEach(card => {
                if (filterValue === 'all' || card.dataset.category === filterValue) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Toggle grid behavior between auto-fill and auto-fit to demonstrate the tutorial concept
    modeSelect.addEventListener('change', (e) => {
        if (e.target.value === 'auto-fit') {
            grid.classList.add('mode-fit');
        } else {
            grid.classList.remove('mode-fit');
        }
    });
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
