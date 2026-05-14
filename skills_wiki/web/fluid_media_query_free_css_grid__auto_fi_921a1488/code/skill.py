def create_component(
    output_dir: str,
    title_text: str = "Mushroom Guide",
    body_text: str = "Explore our responsive, media-query-free card grid.",
    color_scheme: str = "dark",        
    accent_color: str = "#4ade80",     
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Media-Query-Free CSS Grid effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#242424"
        text_primary = "#ffffff"
        text_secondary = "#a3a3a3"
        border_color = "#333333"
        tag_edible_bg = "rgba(74, 222, 128, 0.15)"
        tag_edible_text = "#4ade80"
        tag_toxic_bg = "rgba(248, 113, 113, 0.15)"
        tag_toxic_text = "#f87171"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        text_primary = "#171717"
        text_secondary = "#525252"
        border_color = "#e5e5e5"
        tag_edible_bg = "rgba(34, 197, 94, 0.15)"
        tag_edible_text = "#166534"
        tag_toxic_bg = "rgba(239, 68, 68, 0.15)"
        tag_toxic_text = "#991b1b"

    # === CSS ===
    css = f"""/* Fluid Media-Query-Free CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    
    /* Grid Variables */
    --grid-gap: 1.5rem;
    --grid-min-col-size: 275px; /* The threshold for column wrapping */
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
}}

.layout-wrapper {{
    width: 100%;
    max-width: {width_px}px;
}}

header {{
    margin-bottom: 2.5rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.subtitle {{
    color: var(--text-secondary);
    font-size: 1.125rem;
}}

/* THE MAGIC GRID PATTERN */
.fluid-grid {{
    display: grid;
    gap: var(--grid-gap);
    /* 
      1. auto-fill: creates empty column tracks to prevent stretching if few items exist
      2. minmax: sets the floor and ceiling for column width
      3. min(var, 100%): if the screen is narrower than the min size, it snaps to 100% to prevent overflow
    */
    grid-template-columns: repeat(
        auto-fill, 
        minmax(min(var(--grid-min-col-size), 100%), 1fr)
    );
}}

/* Card Styling */
.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 0.75rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.tag.edible {{
    background-color: {tag_edible_bg};
    color: {tag_edible_text};
}}

.tag.toxic {{
    background-color: {tag_toxic_bg};
    color: {tag_toxic_text};
}}

.card-description {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1; /* Pushes notes to the bottom if descriptions vary in length */
}}

.card-notes {{
    background-color: rgba(0,0,0,0.1);
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.875rem;
    color: var(--text-secondary);
    border-left: 3px solid {accent_color};
}}

/* For light mode notes background adjustment */
@media (prefers-color-scheme: light) {{
    .card-notes {{
        background-color: rgba(0,0,0,0.03);
    }}
}}
"""

    # === HTML ===
    # Generating some dummy data to illustrate the grid wrapping
    cards_data = [
        {"title": "Chanterelle", "type": "edible", "desc": "Golden-yellow, funnel-shaped mushroom with false gills.", "note": "Has toxic look-alikes - learn proper identification."},
        {"title": "Death Cap", "type": "toxic", "desc": "Pale green to white cap with white gills. Found under oak trees.", "note": "Extremely toxic - study for safety awareness."},
        {"title": "Morel", "type": "edible", "desc": "Distinctive honeycomb-like cap structure.", "note": "Must be cooked before eating."},
        {"title": "Destroying Angel", "type": "toxic", "desc": "Pure white mushroom with a sack-like base (volva).", "note": "Deadly toxic - study for safety awareness."},
        {"title": "Chicken of the Woods", "type": "edible", "desc": "Bright orange bracket fungus with yellow edges.", "note": "Avoid if growing on certain tree species."},
        {"title": "False Morel", "type": "toxic", "desc": "Brain-like, reddish-brown cap with irregular shape.", "note": "Highly toxic - often confused with true morels."}
    ]

    cards_html = ""
    for card in cards_data:
        cards_html += f"""
            <article class="card">
                <div class="card-header">
                    <h2 class="card-title">{card['title']}</h2>
                    <div class="tags">
                        <span class="tag {card['type']}">{card['type']}</span>
                    </div>
                </div>
                <p class="card-description">{card['desc']}</p>
                <div class="card-notes">
                    <strong>Important:</strong> {card['note']}
                </div>
            </article>"""

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
    <div class="layout-wrapper">
        <header>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <!-- The Fluid Grid Component -->
        <main class="fluid-grid" id="grid">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Media-Query-Free Grid
// The layout is handled entirely by CSS Grid. 
// This script allows you to toggle between auto-fill and auto-fit to observe the difference.

document.addEventListener('DOMContentLoaded', () => {{
    // Optional: Add a double click listener to the body to toggle layout modes for demonstration
    const grid = document.getElementById('grid');
    let isAutoFill = true;

    document.body.addEventListener('dblclick', () => {{
        isAutoFill = !isAutoFill;
        const mode = isAutoFill ? 'auto-fill' : 'auto-fit';
        
        // Dynamically update the CSS property
        grid.style.gridTemplateColumns = `repeat(${{mode}}, minmax(min(var(--grid-min-col-size), 100%), 1fr))`;
        
        console.log(`Grid switched to: ${{mode}}`);
        
        // If there were a visual toast notification, we would fire it here
        // "auto-fit" will stretch remaining cards if some are removed/filtered.
        // "auto-fill" will leave empty spaces, maintaining card widths.
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
