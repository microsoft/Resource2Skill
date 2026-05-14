import os

def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Responsive Layout Demo",
    body_text: str = "This demonstration showcases the power of CSS Grid for creating flexible and responsive layouts without needing media queries for basic reflow.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#6c63ff",  # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800, # This height is mostly for the *body* to show grid alignment. The grid-container itself will be auto height.
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the core CSS Grid responsive layout effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        text_color = "#e0e0e0"
        container_bg = "#2c2c44"
        item_bg = "#4a4a6e"
        item_border = accent_color
        item_accent_1_bg = "#8a82ff" # Lighter accent
        item_accent_2_bg = "#5a52d0" # Darker accent
        item_accent_3_bg = "#b0a9ff" # Even lighter accent
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        container_bg = "#e9ecef"
        item_bg = "#ffffff"
        item_border = accent_color
        item_accent_1_bg = "#908bff" # Lighter accent
        item_accent_2_bg = "#655ed8" # Darker accent
        item_accent_3_bg = "#c2beff" # Even lighter accent

    num_items = kwargs.get("num_grid_items", 8) # Default to 8 items for a good demo

    # === CSS ===
    css = f"""/* CSS Grid Responsive Layout Demo — generated component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --container-bg: {container_bg};
    --item-bg: {item_bg};
    --item-border: {item_border};
    --item-accent-1-bg: {item_accent_1_bg};
    --item-accent-2-bg: {item_accent_2_bg};
    --item-accent-3-bg: {item_accent_3_bg};
    --viewport-width: {width_px}px;
    --viewport-height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 20px;
    overflow-x: hidden; /* Prevent horizontal scroll on resize */
}}

h1 {{
    margin-bottom: 20px;
    color: var(--accent);
    text-align: center;
    font-size: 2.5em;
}}

p {{
    max-width: 800px;
    text-align: center;
    margin-bottom: 30px;
    line-height: 1.6;
    font-size: 1.1em;
}}

.grid-container {{
    display: grid;
    width: clamp(300px, 90vw, var(--viewport-width)); /* Responsive width */
    min-height: 400px; /* Minimum height for grid content */
    height: auto; /* Allow height to adjust based on content */
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Responsive columns */
    grid-auto-rows: minmax(100px, auto); /* Auto-height for implicit rows, min 100px */
    gap: 16px;
    background-color: var(--container-bg);
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);

    /* Align grid itself within the container (if grid is smaller than container's available space) */
    /* These would apply if grid-container had a fixed height/width larger than its content */
    /* justify-content: center; */
    /* align-content: start; */
}}

.grid-item {{
    background-color: var(--item-bg);
    border: 2px solid var(--item-border);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2em;
    font-weight: 700;
    color: var(--text);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;

    /* Align items within their cells (default is stretch) */
    justify-self: stretch;
    align-self: stretch;
}}

.grid-item:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}}

/* Specific item placements to demonstrate explicit control */
.item-1 {{
    grid-column: span 2; /* Span 2 columns */
    background-color: var(--item-accent-1-bg);
}}

.item-2 {{
    grid-row: span 2; /* Span 2 rows */
    background-color: var(--item-accent-2-bg);
}}

.item-3 {{
    /* Explicitly place item 3 to start at column line 3 and span 2 columns,
       and row line 1 and span 2 rows. This might overlap with auto-placed items */
    grid-column: 3 / span 2;
    grid-row: 1 / span 2;
    z-index: 1; /* Demonstrate layering */
    background-color: var(--item-accent-3-bg);
    transform: scale(1.05);
}}

/* Individual item alignment overrides within their cell */
.item-4 {{
    justify-self: end; /* Align to the end of its cell (row axis) */
    align-self: start; /* Align to the start of its cell (column axis) */
    background-color: var(--item-accent-1-bg);
}}

.item-5 {{
    justify-self: center; /* Align to the center of its cell (row axis) */
    align-self: end;     /* Align to the end of its cell (column axis) */
    background-color: var(--item-accent-2-bg);
}}
"""

    # Generate grid items HTML
    grid_items_html = ""
    # Ensure item-1 to item-5 are correctly identified for their specific CSS rules
    # regardless of the total num_items.
    for i in range(1, num_items + 1):
        grid_items_html += f'    <div class="grid-item item-{i}">{i}</div>\n'


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
    <p>{body_text}</p>
    <div class="grid-container">
{grid_items_html.strip()}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (empty as core grid features are CSS-driven) ===
    js = f"""// CSS Grid Responsive Layout Demo — no custom JavaScript for core grid features
document.addEventListener('DOMContentLoaded', () => {{
    // You can add interactive elements or dynamic content here if needed.
    console.log("CSS Grid demo loaded. Resize the browser window to see responsiveness.");
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
