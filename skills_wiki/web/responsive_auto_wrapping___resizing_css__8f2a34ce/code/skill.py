def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4a69bd",     # CSS hex color for a general accent, not directly used in cards in video but good for future
    width_px: int = 1200,              # Max width for the overall grid container
    height_px: int = 800,              # Min height for the body
    num_cards: int = 12,               # Number of cards to display
    card_min_width_px: int = 300,      # Minimum width for each card in the grid
    grid_gap_px: int = 15,             # Gap between grid items
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Wrapping & Resizing CSS Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "white"
        card_bg_color = "#222429"
        card_border_color = "rgb(75, 82, 92)"
    else: # light theme approximation
        bg_color = "#f8f9fa"
        text_color = "#212529"
        card_bg_color = "#ffffff"
        card_border_color = "#ced4da"

    # === CSS ===
    css = f"""/* Responsive Auto-Wrapping & Resizing CSS Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg-color: {card_bg_color};
    --card-border-color: {card_border_color};
    --accent-color: {accent_color}; /* General accent, not used on cards from video */
    --grid-max-width: {width_px}px;
    --grid-min-height: {height_px}px; /* for body */
    --card-min-width: {card_min_width_px}px;
    --grid-gap: {grid_gap_px}px;
}}

html {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--text-color);
}}

body {{
    background-color: var(--bg-color);
    padding: min(50px, 7%); /* Responsive padding as seen in video */
    min-height: 100vh;
    display: flex; /* Using flexbox on body to center the grid container */
    justify-content: center;
    align-items: flex-start; /* Align to top, not center, to allow scrolling for many cards */
}}

h1 {{
    margin: 30px 0;
    text-align: center;
    color: var(--text-color);
}}

.grid-wrapper {{
    max-width: var(--grid-max-width);
    width: 100%; /* Ensure it takes full width up to max */
}}

.grid-container {{
    display: grid;
    /* Core responsive grid magic: auto-fit for column count, minmax for item size */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center; /* Centers the grid if its total width is less than parent max-width */
}}

.card {{
    padding: 2em;
    border: 1px solid var(--card-border-color);
    border-radius: 10px;
    background-color: var(--card-bg-color);
    text-align: center;
    /* Ensure content inside cards is visible */
    color: var(--text-color);
}}

.card h2 {{
    margin-bottom: 0.5em;
    font-size: 1.5em;
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
    <div class="grid-wrapper">
        <h1>{title_text}</h1>
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for the core responsive grid functionality shown in the tutorial.
// This file is included for completeness.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Responsive Grid Loaded!');
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

