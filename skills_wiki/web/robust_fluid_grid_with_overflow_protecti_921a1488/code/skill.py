def create_component(
    output_dir: str,
    title_text: str = "Get to know your mushrooms",
    body_text: str = "A responsive grid demonstrating auto-fill with minmax and overflow protection.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Robust Fluid Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#18181b"          # Zinc 900
        text_color = "#f4f4f5"        # Zinc 100
        text_muted = "#a1a1aa"        # Zinc 400
        surface_color = "#27272a"     # Zinc 800
        surface_hover = "#3f3f46"     # Zinc 700
        border_color = "#3f3f46"
        tag_bg_1 = "rgba(74, 222, 128, 0.15)" # Green tint
        tag_text_1 = "#4ade80"
        tag_bg_2 = "rgba(248, 113, 113, 0.15)" # Red tint
        tag_text_2 = "#f87171"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        border_color = "#e4e4e7"
        tag_bg_1 = "rgba(22, 163, 74, 0.1)"
        tag_text_1 = "#16a34a"
        tag_bg_2 = "rgba(220, 38, 38, 0.1)"
        tag_text_2 = "#dc2626"

    # === CSS ===
    css = f"""/* Robust Fluid Grid — generated component */
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
    
    /* Configurable Grid Property */
    --grid-min-col-size: 275px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px; /* Constrain max width for presentation */
}}

header {{
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}}

header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* ========================================================
   THE CORE GRID PATTERN 
   ======================================================== */
.fluid-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
       1. repeat(auto-fill, ...): Create as many columns as fit. If items are removed, keep empty tracks so remaining items don't stretch.
       2. minmax(..., 1fr): Columns stretch to fill row, but have a minimum size.
       3. min(100%, var(--grid-min-col-size)): 
          Try to be at least the pixel value. BUT if the container itself 
          is smaller than that pixel value (e.g. mobile screen), cap the 
          minimum width at 100% of the container to prevent horizontal overflow.
    */
    grid-template-columns: repeat(
        auto-fill, 
        minmax(min(100%, var(--grid-min-col-size)), 1fr)
    );
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, background-color 0.2s ease;
    cursor: default;
}}

.card:hover {{
    transform: translateY(-2px);
    background: var(--surface-hover);
}}

.card-header {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.05em;
}}

.tag.edible {{
    background-color: {tag_bg_1};
    color: {tag_text_1};
}}

.tag.toxic {{
    background-color: {tag_bg_2};
    color: {tag_text_2};
}}

.tag.season {{
    background-color: rgba(161, 161, 170, 0.15);
    color: var(--text-muted);
}}

.card-body p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.card-footer {{
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.85rem;
}}

.card-footer span {{
    font-weight: 600;
    color: var(--text);
}}

/* Filter controls demo */
.controls {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}}

button:hover, button.active {{
    background: var(--text);
    color: var(--bg);
}}
"""

    # Data for generating cards
    mushrooms = [
        {"name": "Chanterelle", "tags": [("edible", "Edible"), ("season", "Summer")], "desc": "Golden-yellow, funnel-shaped mushroom with false gills.", "note": "Has toxic look-alikes - learn proper identification."},
        {"name": "Death Cap", "tags": [("toxic", "Toxic"), ("season", "Summer")], "desc": "Pale green to white cap with white gills.", "note": "Extremely toxic - study for safety awareness."},
        {"name": "Morel", "tags": [("edible", "Edible"), ("season", "Spring")], "desc": "Distinctive honeycomb-like cap structure.", "note": "Must be cooked before eating."},
        {"name": "Oyster Mushroom", "tags": [("edible", "Edible"), ("season", "Fall")], "desc": "Fan-shaped caps growing in clusters.", "note": "Great beginner mushroom, few look-alikes."},
        {"name": "Chicken of the Woods", "tags": [("edible", "Edible"), ("season", "Fall")], "desc": "Bright orange bracket fungus with yellow edges.", "note": "Avoid if growing on certain tree species."},
        {"name": "Destroying Angel", "tags": [("toxic", "Toxic"), ("season", "Summer")], "desc": "Pure white mushroom with a sack-like base.", "note": "Deadly toxic - study for safety awareness."},
        {"name": "Lion's Mane", "tags": [("edible", "Edible"), ("season", "Fall")], "desc": "White, shaggy appearance like a lion's mane.", "note": "No toxic look-alikes."},
        {"name": "False Morel", "tags": [("toxic", "Toxic"), ("season", "Spring")], "desc": "Brain-like, reddish-brown cap with irregular shape.", "note": "Highly toxic - often confused with true morels."}
    ]

    cards_html = ""
    for m in mushrooms:
        tags_html = "".join([f'<span class="tag {t[0]}">{t[1]}</span>' for t in m["tags"]])
        cards_html += f"""
            <article class="card" data-season="{m["tags"][1][0].lower()}">
                <div class="card-header">
                    <h2 class="card-title">{m["name"]}</h2>
                    <div class="tags">
                        {tags_html}
                    </div>
                </div>
                <div class="card-body">
                    <p>{m["desc"]}</p>
                </div>
                <div class="card-footer">
                    <p><span>Important notes:</span> {m["note"]}</p>
                </div>
            </article>"""

    # === HTML ===
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
    <div class="app-wrapper">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <button class="active" data-filter="all">Show All</button>
            <button data-filter="spring">Spring</button>
            <button data-filter="summer">Summer</button>
        </div>

        <!-- THE FLUID GRID -->
        <main class="fluid-grid" id="grid">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Script to demonstrate why auto-fill is better than auto-fit when filtering
document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('.controls button');
    const cards = document.querySelectorAll('.card');

    buttons.forEach(button => {{
        button.addEventListener('click', () => {{
            // Update active state
            buttons.forEach(b => b.classList.remove('active'));
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            // Filter cards
            cards.forEach(card => {{
                if (filter === 'all' || card.getAttribute('data-season') === filter) {{
                    card.style.display = 'flex'; // Restore grid item
                }} else {{
                    card.style.display = 'none'; // Remove from grid flow
                }}
            }});
            
            /* 
               Notice how when you filter to "Spring" (only 2 items), 
               the cards DO NOT stretch to fill the entire screen width.
               This is because we used 'auto-fill' in our CSS Grid instead 
               of 'auto-fit'. 'auto-fill' preserves the empty grid tracks!
            */
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
