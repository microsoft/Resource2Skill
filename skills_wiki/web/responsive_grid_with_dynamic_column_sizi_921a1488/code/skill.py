def create_component(
    output_dir: str,
    title_text: str = "Get to know your mushrooms",
    card_data: list = None,
    color_scheme: str = "dark",  # "dark" or "light"
    min_col_size_px: int = 275,
    grid_gap_rem: float = 1.0,
    use_auto_fit: bool = False, # True for auto-fit, False for auto-fill
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Grid with Dynamic Column Sizing visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if card_data is None:
        card_data = [
            {"title": "Chanterelle", "notes": "Golden-yellow, funnel-shaped mushroom with false gills.", "tags": ["edible", "summer"]},
            {"title": "Morel", "notes": "Distinctive honeycomb-like cap structure.", "tags": ["edible", "spring"]},
            {"title": "Chicken of the Woods", "notes": "Bright orange bracket fungus with yellow edges.", "tags": ["edible", "summer"]},
            {"title": "Death Cap", "notes": "Pale green to white cap with white gills. Important notes: Extremely toxic - study for safety awareness.", "tags": ["toxic", "summer"]},
            {"title": "Oyster Mushroom", "notes": "Fan-shaped caps growing in clusters. Important notes: Great beginner mushroom, few look-alikes.", "tags": ["edible", "fall"]},
            {"title": "Lion's Mane", "notes": "White, shaggy appearance like a lion's mane. Important notes: No toxic look-alikes.", "tags": ["edible", "fall"]},
            {"title": "Destroying Angel", "notes": "Pure white mushroom with a sack-like base. Important notes: Deadly toxic - study for safety awareness.", "tags": ["toxic", "summer"]},
            {"title": "King Bolete", "notes": "Large brown cap with thick stem. Important notes: Learn to distinguish from similar species.", "tags": ["edible", "summer"]},
            {"title": "Shaggy Mane", "notes": "Golden-yellow, funnel-shaped mushroom with false gills. Important notes: Must be harvested and eaten quickly.", "tags": ["edible", "fall"]},
            {"title": "Maitake", "notes": "Brain-like, feathery clusters with overlapping grey-brown caps. Also known as Hen of the Woods - no toxic look-alikes.", "tags": ["edible", "fall"]},
            {"title": "False Morel", "notes": "Brain-like, reddish-brown cap with irregular shape. Important notes: Highly toxic - often confused with true morels.", "tags": ["toxic", "spring"]},
            {"title": "Matsutake", "notes": "White to tan brown cap with distinctive spicy aroma. Important notes: Verify identification - has toxic look-alikes.", "tags": ["edible", "fall"]},
        ]

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#2b2b2b"
        text_color = "#f0f0f0"
        card_bg = "#3a3a3a"
        tag_bg_edible = "#70b55f"
        tag_bg_toxic = "#e64a4b"
        tag_bg_summer = "#e6cc4b"
        tag_bg_spring = "#4b85e6"
        tag_bg_fall = "#8d4be6"
    else: # Light theme (simplified for demo)
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        tag_bg_edible = "#90ee90" # Light green
        tag_bg_toxic = "#ff6347" # Tomato red
        tag_bg_summer = "#ffd700" # Gold
        tag_bg_spring = "#87ceeb" # SkyBlue
        tag_bg_fall = "#dda0dd" # Plum

    repeat_keyword = "auto-fit" if use_auto_fit else "auto-fill"

    # === CSS ===
    css = f"""
        *, *::before, *::after {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg: {bg_color};
            --text-color: {text_color};
            --card-bg: {card_bg};
            --tag-bg-edible: {tag_bg_edible};
            --tag-bg-toxic: {tag_bg_toxic};
            --tag-bg-summer: {tag_bg_summer};
            --tag-bg-spring: {tag_bg_spring};
            --tag-bg-fall: {tag_bg_fall};
            --min-col-size: {min_col_size_px}px;
            --grid-gap: {grid_gap_rem}rem;
        }}

        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text-color);
            min-height: 100vh;
            padding: 2rem;
        }}

        h1 {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }}

        .filters {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .filters button {{
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 0.3rem;
            background-color: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            transition: background-color 0.2s ease-in-out;
        }}

        .filters button:hover,
        .filters button.active {{
            background-color: var(--tag-bg-edible); /* Use edible tag color as active indicator */
        }}

        .grid-auto-fill {{
            display: grid;
            grid-template-columns: repeat({repeat_keyword}, minmax(min(var(--min-col-size), 100%), 1fr));
            gap: var(--grid-gap);
            max-width: 1200px; /* Limit overall grid width for better presentation */
            margin: 0 auto;
        }}

        .card {{
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
            opacity: 1;
            transform: translateY(0);
        }}

        .card.hidden {{
            opacity: 0;
            transform: translateY(20px);
            position: absolute; /* Take out of flow to allow others to fill space */
            pointer-events: none;
            /* Adjust height to 0 to prevent empty space */
            height: 0; 
            overflow: hidden;
            padding-top: 0;
            padding-bottom: 0;
            margin-top: 0;
            margin-bottom: 0;
            transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out, height 0.5s ease-in-out, padding 0.5s ease-in-out, margin 0.5s ease-in-out;
        }}
        
        .card h2 {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }}

        .card p {{
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 1rem;
            color: var(--text-color);
        }}

        .card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .tag {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            padding: 0.3rem 0.6rem;
            border-radius: 0.3rem;
            color: var(--text-color);
        }}

        .tag.edible {{ background-color: var(--tag-bg-edible); }}
        .tag.toxic {{ background-color: var(--tag-bg-toxic); }}
        .tag.summer {{ background-color: var(--tag-bg-summer); }}
        .tag.spring {{ background-color: var(--tag-bg-spring); }}
        .tag.fall {{ background-color: var(--tag-bg-fall); }}
    """

    # === HTML ===
    cards_html = ""
    for i, card in enumerate(card_data):
        tags_html = "".join([f'<span class="tag {tag.lower()}">{tag}</span>' for tag in card["tags"]])
        cards_html += f"""
            <div class="card" data-id="card-{i}" data-tags="{','.join(card['tags'])}">
                <h2>{card["title"]}</h2>
                <p>{card["notes"]}</p>
                <div class="card-tags">
                    {tags_html}
                </div>
            </div>
        """

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
    <h1>{title_text}</h1>
    <div class="filters">
        <button data-filter-type="all" class="active">All</button>
        <button data-filter-type="season" data-filter-value="spring">Spring</button>
        <button data-filter-type="season" data-filter-value="summer">Summer</button>
        <button data-filter-type="season" data-filter-value="fall">Fall</button>
        <button data-filter-type="status" data-filter-value="edible">Edible</button>
        <button data-filter-type="status" data-filter-value="toxic">Toxic</button>
    </div>
    <div class="grid-auto-fill">
        {cards_html}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """
        document.addEventListener('DOMContentLoaded', () => {
            const grid = document.querySelector('.grid-auto-fill');
            const cards = Array.from(grid.querySelectorAll('.card'));
            const filterButtons = document.querySelectorAll('.filters button');

            let currentFilters = { season: 'all', status: 'all' };

            function applyFilters() {
                cards.forEach(card => {
                    const cardTags = card.dataset.tags.split(',');
                    const matchesSeason = currentFilters.season === 'all' || cardTags.includes(currentFilters.season);
                    const matchesStatus = currentFilters.status === 'all' || cardTags.includes(currentFilters.status);

                    if (matchesSeason && matchesStatus) {
                        card.classList.remove('hidden');
                        card.style.position = ''; // Restore position
                        card.style.height = '';   // Restore height
                        card.style.paddingTop = ''; // Restore padding
                        card.style.paddingBottom = '';
                        card.style.marginTop = ''; // Restore margin
                        card.style.marginBottom = '';
                    } else {
                        card.classList.add('hidden');
                        card.style.position = 'absolute'; // Take out of flow
                        card.style.height = '0'; // Collapse height
                        card.style.paddingTop = '0'; // Remove padding
                        card.style.paddingBottom = '0';
                        card.style.marginTop = '0'; // Remove margin
                        card.style.marginBottom = '0';
                    }
                });

                // Force reflow after position absolute to ensure smooth transition for remaining items
                // This is a common trick, but might not be strictly necessary with 'display: grid'
                void grid.offsetWidth; 
            }

            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');

                    const filterType = button.dataset.filterType;
                    const filterValue = button.dataset.filterValue || 'all';

                    if (filterType === 'all') {
                        currentFilters = { season: 'all', status: 'all' };
                    } else if (filterType === 'season') {
                        currentFilters.season = filterValue;
                    } else if (filterType === 'status') {
                        currentFilters.status = filterValue;
                    }
                    applyFilters();
                });
            });

            // Initial filter application (show all)
            applyFilters();
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

