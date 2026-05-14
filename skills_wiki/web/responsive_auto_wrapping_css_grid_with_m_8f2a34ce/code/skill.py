def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#ff0000",  # CSS hex color for accent (used for debug border in video)
    width_px: int = 1200,
    height_px: int = 800,
    num_cards: int = 12,
    min_card_width_px: int = 300, # Minimum width for each card
    gap_px: int = 15, # Gap between grid items
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Wrapping CSS Grid with Minmax Sizing.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        h1_color = "#f0f0f0"
        card_bg_color = "#222429"
        card_border_color = "rgb(75, 82, 92)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        h1_color = "#1a1a2e"
        card_bg_color = "rgba(0, 0, 0, 0.04)"
        card_border_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: {text_color};
    text-align: center;
}}

body {{
    padding: min(50px, 7%);
    background-color: {bg_color};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}}

h1 {{
    margin-bottom: 30px;
    color: {h1_color};
}}

.grid-container {{
    display: grid;
    /* This is the core responsive grid logic */
    grid-template-columns: repeat(auto-fit, minmax({min_card_width_px}px, 1fr));
    gap: {gap_px}px;
    justify-content: center; /* Centers the grid within its container */
    max-width: {width_px}px; /* Constrain grid container width for demonstration */
    border: 1px solid {accent_color}; /* Visual boundary for the grid container */
}}

.card {{
    padding: 2em;
    border: 1px solid {card_border_color};
    border-radius: 10px;
    background-color: {card_bg_color};
    text-align: center;
    /* Ensure card content does not overflow and respects min-width */
    overflow: hidden;
    min-width: {min_card_width_px}px;
}}

.card h2 {{
    margin-bottom: 0.5em;
    color: {text_color};
}}

.card p {{
    font-size: 0.9em;
    line-height: 1.5;
    color: {text_color};
}}
"""

    # Generate card elements
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum</h2>
            <p>{body_text}</p>
        </div>"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{title_text}</h1>
    <div class="grid-container">{cards_html}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Wrapping CSS Grid with Minmax Sizing - No specific JS interaction needed for this core pattern.
document.addEventListener('DOMContentLoaded', () => {{
    console.log('Responsive Grid Loaded');
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

