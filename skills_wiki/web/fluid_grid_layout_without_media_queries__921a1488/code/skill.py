def create_component(
    output_dir: str,
    title_text: str = "Responsive Mushroom Guide",
    body_text: str = "Filter items or resize your browser to see how the grid mathematically adapts without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4ade80",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    grid_mode: str = "auto-fit",       # "auto-fit" or "auto-fill"
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Grid Layout (auto-fit/auto-fill + minmax).

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1e1e24"
        text_color = "#e5e7eb"
        text_muted = "#9ca3af"
        surface_color = "#2a2a35"
        border_color = "rgba(255, 255, 255, 0.08)"
        tag_edible_bg = "rgba(74, 222, 128, 0.15)"
        tag_edible_fg = "#4ade80"
        tag_toxic_bg = "rgba(248, 113, 113, 0.15)"
        tag_toxic_fg = "#f87171"
        tag_season_bg = "rgba(96, 165, 250, 0.15)"
        tag_season_fg = "#60a5fa"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        tag_edible_bg = "rgba(21, 128, 61, 0.1)"
        tag_edible_fg = "#15803d"
        tag_toxic_bg = "rgba(185, 28, 28, 0.1)"
        tag_toxic_fg = "#b91c1c"
        tag_season_bg = "rgba(29, 78, 216, 0.1)"
        tag_season_fg = "#1d4ed8"

    # Data to populate the grid
    cards = [
        {"title": "Chanterelle", "type": "edible", "season": "Summer", "desc": "Golden-yellow, funnel-shaped mushroom with false gills. Has toxic look-alikes.", "note": "Learn proper identification."},
        {"title": "Death Cap", "type": "toxic", "season": "Summer", "desc": "Pale green to white cap with white gills. Highly toxic.", "note": "Study for safety awareness."},
        {"title": "Morel", "type": "edible", "season": "Spring", "desc": "Distinctive honeycomb-like cap structure.", "note": "Must be cooked before eating."},
        {"title": "Lion's Mane", "type": "edible", "season": "Fall", "desc": "White, shaggy appearance like a lion's mane.", "note": "No toxic look-alikes."},
        {"title": "Destroying Angel", "type": "toxic", "season": "Summer", "desc": "Pure white mushroom with a sack-like base.", "note": "Extremely toxic - deadly."},
        {"title": "Oyster Mushroom", "type": "edible", "season": "Fall", "desc": "Fan-shaped caps growing in overlapping clusters.", "note": "Great beginner mushroom."},
    ]

    cards_html = ""
    for card in cards:
        tag_type_class = "tag-edible" if card["type"] == "edible" else "tag-toxic"
        cards_html += f"""
        <div class="card" data-season="{card['season'].lower()}">
            <h3 class="card-title">{card['title']}</h3>
            <div class="card-tags">
                <span class="tag {tag_type_class}">{card['type']}</span>
                <span class="tag tag-season">{card['season']}</span>
            </div>
            <p class="card-desc">{card['desc']}</p>
            <div class="card-note">
                <strong>Important note:</strong> {card['note']}
            </div>
        </div>"""

    # === CSS ===
    css = f"""/* Fluid Grid Layout Component */
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
    --border: {border_color};
    
    --grid-min-col-size: 275px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    line-height: 1.5;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
}}

header {{
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

header p {{
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}}

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    background: var(--surface);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}}

select, button {{
    padding: 0.5rem 1rem;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    transition: border-color 0.2s;
}}

button {{
    background: var(--accent);
    color: #000;
    font-weight: 600;
    border: none;
}}

button:hover {{
    filter: brightness(1.1);
}}

select:focus, button:focus {{
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}}

/* ==================================================== */
/* Core Layout Mechanism: The Fluid Grid                */
/* ==================================================== */
.grid {{
    display: grid;
    gap: 1.5rem;
    /* 
      The Magic Formula:
      1. repeat(): Loops the pattern
      2. auto-fit/auto-fill: Dynamically creates tracks based on container width
      3. minmax(): Specifies the min/max limits for a track
      4. min(): Resolves the overflow bug! If viewport is < 275px, it caps at 100%
    */
    grid-template-columns: repeat({grid_mode}, minmax(min(var(--grid-min-col-size), 100%), 1fr));
    
    transition: all 0.4s ease;
}}
/* ==================================================== */

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}}

.card-tags {{
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
}}

.tag {{
    font-size: 0.7rem;
    padding: 0.15rem 0.6rem;
    border-radius: 9999px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.tag-edible {{ background: {tag_edible_bg}; color: {tag_edible_fg}; }}
.tag-toxic {{ background: {tag_toxic_bg}; color: {tag_toxic_fg}; }}
.tag-season {{ background: {tag_season_bg}; color: {tag_season_fg}; }}

.card-desc {{
    flex-grow: 1; /* Pushes note to the bottom */
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}}

.card-note {{
    font-size: 0.85rem;
    padding-top: 1rem;
    border-top: 1px dashed var(--border);
    color: var(--text);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            
            <div class="controls">
                <select id="grid-mode">
                    <option value="auto-fit" {"selected" if grid_mode == "auto-fit" else ""}>CSS Grid: auto-fit (stretches to fill space)</option>
                    <option value="auto-fill" {"selected" if grid_mode == "auto-fill" else ""}>CSS Grid: auto-fill (leaves empty columns)</option>
                </select>
                <button id="filter-btn" data-filtered="false">Filter: Show Spring items only</button>
            </div>
        </header>

        <main class="grid" id="main-grid">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Grid Interactivity
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('main-grid');
    const modeSelect = document.getElementById('grid-mode');
    const filterBtn = document.getElementById('filter-btn');
    const cards = document.querySelectorAll('.card');

    // Toggle between auto-fit and auto-fill dynamically
    modeSelect.addEventListener('change', (e) => {{
        const mode = e.target.value;
        grid.style.gridTemplateColumns = `repeat(${{mode}}, minmax(min(var(--grid-min-col-size), 100%), 1fr))`;
    }});

    // Filter items to demonstrate how auto-fit and auto-fill handle empty grid space
    filterBtn.addEventListener('click', (e) => {{
        const isFiltered = e.target.dataset.filtered === 'true';
        
        if (isFiltered) {{
            // Show all
            cards.forEach(card => card.style.display = 'flex');
            e.target.dataset.filtered = 'false';
            e.target.textContent = 'Filter: Show Spring items only';
        }} else {{
            // Show only spring items (results in just 1 card, creating empty space)
            cards.forEach(card => {{
                if (card.dataset.season === 'spring') {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            e.target.dataset.filtered = 'true';
            e.target.textContent = 'Filter: Show All';
        }}
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
