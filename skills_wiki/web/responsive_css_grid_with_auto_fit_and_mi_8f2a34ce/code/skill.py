def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#A0A0A0",  # CSS hex color for a subtle accent/border
    width_px: int = 1200,
    height_px: int = 800,
    min_card_width: int = 300, # Minimum width for each card before wrapping
    num_cards: int = 12, # Number of cards in the grid
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid with Auto-Fit and Min-Max Resizing visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0D0D14"  # Dark background
        h1_color = "#F0F0F0" # White for main title
        text_color = "#E0E0E0" # Off-white for card text
        card_bg_color = "#222429" # Dark gray for cards
        card_border_color = "rgb(75, 82, 92)" # Medium gray for card border
    else:
        bg_color = "#F8F9FA"  # Light background
        h1_color = "#343A40"  # Dark gray for main title
        text_color = "#495057" # Darker gray for card text
        card_bg_color = "#FFFFFF" # White for cards
        card_border_color = "#CED4DA" # Light gray for card border

    # Generate card HTML
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum</h2>
            <p>{body_text}</p>
        </div>
        """

    # === CSS ===
    css = f"""/* Responsive CSS Grid with Auto-Fit and Min-Max Resizing — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --h1-color: {h1_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg_color};
    --card-border: {card_border_color};
    --min-card-width: {min_card_width}px;
    --grid-gap: 15px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: min(50px, 7%); /* Responsive padding as seen in video setup */
    display: flex; /* Use flex to center the h1 and grid-container vertically */
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align to start but allow content to push down */
}}

h1 {{
    margin-bottom: 30px;
    color: var(--h1-color);
    text-align: center;
    font-size: 2.5em;
}}

.grid-container {{
    display: grid;
    /* Core responsive grid magic */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center; /* Center the grid items within the container if there's leftover space */
    width: 100%; /* Take full width of parent padding */
    max-width: {width_px}px; /* Constrain max width for desktop view */
    /* Optional: border for debugging as seen in video, commented out for final clean look */
    /* border: 1px solid red; */
}}

.card {{
    padding: 2em;
    border: 1px solid var(--card-border);
    border-radius: 10px;
    background-color: var(--card-bg);
    text-align: center;
    /* Ensure cards have a flex-basis to work with minmax(300px, 1fr) */
    min-width: var(--min-card-width);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.card h2 {{
    color: var(--h1-color); /* Same color as main title */
    margin-bottom: 1em;
    font-size: 1.5em;
}}

.card p {{
    font-size: 0.9em;
    line-height: 1.6;
}}
"""

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
    <div class="grid-container">
        {cards_html}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive CSS Grid with Auto-Fit and Min-Max Resizing — interactive behavior
// This component's core responsiveness is managed purely by CSS Grid properties.
// No JavaScript is required for the demonstrated layout and resizing behavior.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Responsive Grid component loaded.');
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

