def create_component(
    output_dir: str,
    title_text: str = "Get to know your mushrooms",
    min_col_size_px: int = 275,
    gap_rem: float = 1.0,
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#4caf50",  # Primary accent color (edible tag)
    width_px: int = 1200,
    height_px: int = 800,
    initial_grid_mode: str = "auto-fill", # "auto-fill" or "auto-fit"
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid with Dynamic Columns and Overflow Protection visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#2d2d2d"
        card_bg_color = "#3e3e3e"
        text_color = "#f0f0f0"
        header_bg_color = "#2d2d2d" # For consistency with main bg
    else:
        bg_color = "#f8f9fa"
        card_bg_color = "#ffffff"
        text_color = "#1a1a2e"
        header_bg_color = "#f8f9fa"

    # Example card data (can be dynamically filtered by JS in a full application)
    card_data = [
        {"title": "Chanterelle", "notes": "Golden-yellow, funnel-shaped mushroom with false gills", "tags": [("edible", "#8bc34a"), ("summer", "#8bc34a")]},
        {"title": "Morel", "notes": "Distinctive honeycomb-like cap structure", "tags": [("ededible", "#8bc34a"), ("spring", "#00bcd4")]},
        {"title": "Chicken of the Woods", "notes": "Bright orange bracket fungus with yellow edges", "tags": [("edible", "#8bc34a"), ("summer", "#8bc34a")]},
        {"title": "Death Cap", "notes": "Pale green to white cap with white gills", "tags": [("toxic", "#f44336"), ("summer", "#8bc34a")]},
        {"title": "Oyster Mushroom", "notes": "Fan-shaped caps growing in clusters", "tags": [("edible", "#8bc34a"), ("fall", "#ffc107")]},
        {"title": "Lion's Mane", "notes": "White, shaggy appearance like a lion's mane", "tags": [("edible", "#8bc34a")]},
        {"title": "Destroying Angel", "notes": "Pure white mushroom with a sack-like base", "tags": [("toxic", "#f44336"), ("summer", "#8bc34a")]},
        {"title": "King Bolete", "notes": "Large brown cap with thick stem", "tags": [("edible", "#8bc34a"), ("summer", "#8bc34a")]},
        {"title": "Shaggy Mane", "notes": "Golden-yellow, funnel-shaped mushroom with false gills", "tags": [("edible", "#8bc34a")]},
        {"title": "Maitake", "notes": "Large, feathery clusters with overlapping grey-brown caps", "tags": [("edible", "#8bc34a"), ("fall", "#ffc107")]},
        {"title": "False Morel", "notes": "Brain-like, reddish-brown cap with irregular shape", "tags": [("toxic", "#f44336"), ("spring", "#00bcd4")]},
        {"title": "Matsutake", "notes": "White to tan brown cap with distinct spicy aroma", "tags": [("edible", "#8bc34a"), ("fall", "#ffc107")]},
    ]

    card_html_list = []
    for i, card in enumerate(card_data):
        tags_html = "".join([f'<span class="tag" style="background-color: {tag_color};">{tag_name.upper()}</span>' for tag_name, tag_color in card["tags"]])
        card_html_list.append(f"""
        <div class="card" data-season="{card['tags'][0][0] if card['tags'] else ''}" data-type="{card['tags'][1][0] if len(card['tags']) > 1 else card['tags'][0][0] if card['tags'] else ''}">
            <h3 class="card-title">{card['title']}</h3>
            <div class="tag-list">{tags_html}</div>
            <p class="card-notes">{card['notes']}</p>
        </div>
        """)
    
    cards_html = "\n".join(card_html_list)

    # === CSS ===
    css = f"""
/* Responsive CSS Grid with Dynamic Columns and Overflow Protection — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg_color};
    --text: {text_color};
    --header-bg: {header_bg_color};
    --min-col-size: {min_col_size_px}px;
    --grid-gap: {gap_rem}rem;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 2rem;
}}

.header {{
    background-color: var(--header-bg);
    padding: 1.5rem 0;
    width: 100%;
    text-align: center;
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text);
}}

.filters {{
    margin-bottom: 2rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}}

.filter-button, .select-wrapper select {{
    background-color: var(--card-bg);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s, border-color 0.2s;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    padding-right: 2.5rem; /* Space for arrow */
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23f0f0f0%22%20d%3D%22M287%20197.974l-116.8-116.8c-4.16-4.16-9.62-6.25-15.08-6.25s-10.92%202.09-15.08%206.25L5.4%20197.974c-4.16%204.16-6.25%209.62-6.25%2015.08s2.09%2010.92%206.25%2015.08c4.16%204.16%209.62%206.25%2015.08%206.25h255.44c4.16%200%209.62-2.09%2015.08-6.25s6.25-9.62%206.25-15.08c0-5.46-2.09-10.92-6.25-15.08z%22%2F%3E%3C%2Fsvg%3E');
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 0.8rem;
}

.select-wrapper {{
    position: relative;
}}

.filter-button:hover, .select-wrapper select:hover {{
    background-color: rgba(255, 255, 255, 0.1);
    border-color: var(--accent);
}}
.filter-button.active, .select-wrapper select:focus {{
    background-color: var(--accent);
    border-color: var(--accent);
    color: white;
    outline: none;
}}


.grid-auto-fill {{
    display: grid;
    /* Core responsive grid magic */
    grid-template-columns: repeat(var(--grid-mode, auto-fill), minmax(min(var(--min-col-size), 100%), 1fr));
    gap: var(--grid-gap);
    width: 100%;
    max-width: {width_px}px; /* Constrain max width for demo */
}}

.grid-auto-fit {{
    grid-template-columns: repeat(auto-fit, minmax(min(var(--min-col-size), 100%), 1fr));
}}

.card {{
    background-color: var(--card-bg);
    padding: 15px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    color: var(--text);
    min-height: 150px;
    transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}}

.card-title {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.tag-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 0.8rem;
}}

.tag {{
    font-size: 0.7rem;
    font-weight: 500;
    padding: 3px 8px;
    border-radius: 4px;
    color: white;
    text-transform: uppercase;
    white-space: nowrap;
}}

.card-notes {{
    font-size: 0.9rem;
    line-height: 1.4;
    flex-grow: 1; /* Allow notes to take up remaining space */
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
    </div>
    <div class="filters">
        <div class="select-wrapper">
            <select id="season-filter">
                <option value="all">Season: All</option>
                <option value="spring">Spring</option>
                <option value="summer">Summer</option>
                <option value="fall">Fall</option>
            </select>
        </div>
        <div class="select-wrapper">
            <select id="type-filter">
                <option value="all">Type: All</option>
                <option value="edible">Edible</option>
                <option value="toxic">Toxic</option>
                <option value="none">None</option>
            </select>
        </div>
        <div class="select-wrapper">
            <select id="grid-mode-selector">
                <option value="auto-fill" {'selected' if initial_grid_mode == 'auto-fill' else ''}>Grid Mode: Auto-Fill</option>
                <option value="auto-fit" {'selected' if initial_grid_mode == 'auto-fit' else ''}>Grid Mode: Auto-Fit</option>
            </select>
        </div>
    </div>
    <div id="mushroom-grid" class="grid-auto-fill">
        {cards_html}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
// Responsive CSS Grid with Dynamic Columns and Overflow Protection — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const mushroomGrid = document.getElementById('mushroom-grid');
    const seasonFilter = document.getElementById('season-filter');
    const typeFilter = document.getElementById('type-filter');
    const gridModeSelector = document.getElementById('grid-mode-selector');
    const cards = Array.from(mushroomGrid.querySelectorAll('.card'));

    // Set initial grid mode based on parameter
    mushroomGrid.style.setProperty('--grid-mode', gridModeSelector.value);

    const applyFilters = () => {{
        const selectedSeason = seasonFilter.value;
        const selectedType = typeFilter.value;

        cards.forEach(card => {{
            const cardSeason = card.dataset.season;
            const cardType = card.dataset.type;

            const matchesSeason = selectedSeason === 'all' || cardSeason === selectedSeason;
            const matchesType = selectedType === 'all' || cardType === selectedType;

            if (matchesSeason && matchesType) {{
                card.style.display = 'flex';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }} else {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {{
                    card.style.display = 'none';
                }}, 300); // Match CSS transition duration
            }}
        }});
    }};

    seasonFilter.addEventListener('change', applyFilters);
    typeFilter.addEventListener('change', applyFilters);
    gridModeSelector.addEventListener('change', (event) => {{
        mushroomGrid.style.setProperty('--grid-mode', event.target.value);
    }});

    // Apply filters on initial load
    applyFilters();
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

