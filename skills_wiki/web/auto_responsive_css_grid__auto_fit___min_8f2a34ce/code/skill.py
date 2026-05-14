def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Resize the browser window to see the grid cards automatically wrap and resize using auto-fit and minmax().",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131314"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
        text_muted = "#aab2bd"
    else:
        bg_color = "#f4f5f7"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        text_muted = "#64748b"

    # Settings from tutorial
    min_column_width = "300px"
    grid_gap = "20px"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid — generated component */
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
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    /* Center the main container in the viewport for demonstration */
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: min(50px, 5vw);
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: var(--text);
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* == CORE SKILL PATTERN == */
.grid-container {{
    display: grid;
    /* repeat(auto-fit) creates as many columns as will fit in the container.
       minmax(300px, 1fr) ensures columns are at least 300px wide, but will grow evenly (1fr) to fill empty space.
       Using min(100%, 300px) instead of just 300px ensures it doesn't overflow on tiny mobile screens under 300px wide. */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, {min_column_width}), 1fr));
    gap: {grid_gap};
    justify-content: center;
}}

/* Card Styling */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 15px;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.4rem;
    color: var(--text);
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}
"""

    # === Generate dummy cards ===
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

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
    <div class="wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <!-- Grid Component -->
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Grid handles 100% of the responsiveness. 
// No JavaScript required for the layout calculation.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid initialized. Resize window to see auto-fit in action.");
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
