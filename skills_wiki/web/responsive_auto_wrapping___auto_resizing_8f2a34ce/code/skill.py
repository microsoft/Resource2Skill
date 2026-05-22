def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#d600b3",  # CSS hex color for accent - changed to a vibrant pink/purple
    width_px: int = 1200,
    height_px: int = 800, # height not strictly used for grid, but for overall container size if needed.
    min_column_width_px: int = 300, # Minimum width for each grid column/card
    grid_gap_px: int = 15, # Gap between grid items
    num_cards: int = 12, # Number of cards in the grid
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Wrapping & Auto-Resizing CSS Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)" # From video: rgb(13, 13, 20) -> #0D0D14
        text_color = "white"
        card_bg_color = "#222429"
        card_border_color = "rgb(75, 82, 92)"
    else: # light theme
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg_color = "#ffffff"
        card_border_color = "#ced4da"

    # === CSS ===
    css = f"""/* Responsive Auto-Wrapping & Auto-Resizing CSS Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg_color};
    --card-border: {card_border_color};
    --min-column-width: {min_column_width_px}px;
    --grid-gap: {grid_gap_px}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: min(50px, 7%); /* Adjust padding dynamically */
    display: flex; /* Use flex to center the grid-container itself */
    justify-content: center;
    align-items: flex-start; /* Align grid container to top */
    overflow-x: hidden; /* Prevent horizontal scroll for small screen sizes */
}}

h1 {{
    margin-bottom: 30px;
    text-align: center;
}}

.grid-container {{
    display: grid;
    /* Core responsive logic: auto-fit columns, min width 300px, max width 1 fraction */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-column-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center; /* Centers the grid items within the container if total width allows for gaps */
    width: 100%; /* Ensure grid container takes full width to allow auto-fit to work */
    max-width: {width_px}px; /* Constrain grid container max width */
}}

.card {{
    padding: 2em;
    border: 1px solid var(--card-border);
    border-radius: 10px;
    background-color: var(--card-bg);
    text-align: center;
    min-height: 200px; /* Added for visual consistency of card height */
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center content vertically within card */
    align-items: center; /* Center content horizontally within card */
}}

.card h2 {{
    margin-bottom: 0.5em;
    color: var(--accent); /* Use accent color for card titles */
}}

.card p {{
    font-size: 0.9em;
    line-height: 1.5;
}}
"""

    # === HTML ===
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum</h2>
            <p>{body_text}</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{title_text}!</h1>
    <div class="grid-container">
        {cards_html}
    </div>
</body>
</html>"""

    # === JavaScript (empty as no interactive behavior is demonstrated) ===
    js = ""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        # Only write script.js if it has content, otherwise skip
        if fname == "script.js" and not content.strip():
            continue

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

