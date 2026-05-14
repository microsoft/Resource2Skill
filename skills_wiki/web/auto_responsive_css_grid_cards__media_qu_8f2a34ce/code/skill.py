def create_component(
    output_dir: str,
    title_text: str = "Responsive CSS Grid",
    body_text: str = "Resize the browser window to see the grid automatically wrap and stretch items without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
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

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#1f2937"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"

    # === HTML Card Generation ===
    cards_html = ""
    for i in range(12):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid Cards */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header p {{
    opacity: 0.8;
    line-height: 1.5;
}}

.grid-container {{
    /* Limit max width to specified parameter for presentation */
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    
    /* THE CORE GRID LOGIC */
    display: grid;
    gap: 15px;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

/* Adding a subtle hover effect for polish */
.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card h2 {{
    margin-bottom: 15px;
    font-size: 1.25rem;
}}

.card p {{
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.8;
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
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="grid-container">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Responsive CSS Grid Cards
// This layout is handled entirely by CSS Grid. 
// No JavaScript math is required to calculate columns or widths!
console.log("Grid layout initialized perfectly via CSS.");
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
