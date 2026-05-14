def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Resize the window to see the grid automatically adjust its columns without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive Grid visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d0d14" # rgb(13, 13, 20) from tutorial
        text_color = "#f0f0f0"
        surface_color = "#222429"
        border_color = "rgba(75, 82, 92, 0.6)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow = "rgba(0, 0, 0, 0.08)"

    # Number of cards to generate
    card_count = kwargs.get("card_count", 6)
    
    # Generate HTML for grid items
    cards_html = ""
    for i in range(card_count):
        cards_html += f"""
        <div class="card">
            <h2 class="card-title">Lorem Ipsum</h2>
            <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

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
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --card-min-width: 300px; /* Crucial constraint from tutorial */
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    /* Simulate tutorial padding */
    padding: min(50px, 7%);
    display: flex;
    justify-content: center;
    align-items: flex-start;
}}

.container {{
    width: 100%;
    max-width: var(--width);
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
}}

.header h1 {{
    font-size: 2.2rem;
    margin-bottom: 10px;
}}

.header p {{
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}}

/* THE CORE SKILL: Auto-Fit MinMax Grid */
.grid-container {{
    display: grid;
    /* Auto-fit adds as many columns as fit. Minmax ensures they are at least 300px but can expand (1fr) */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: 20px;
    justify-content: center;
}}

.card {{
    background-color: var(--surface);
    padding: 2em;
    border: 1px solid var(--border);
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px var(--shadow);
    border-color: var(--accent);
}}

.card-title {{
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 1.4rem;
    font-weight: 600;
}}

.card-text {{
    font-size: 0.95rem;
    line-height: 1.6;
    opacity: 0.75;
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
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="grid-container">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Responsive Grid 
// Layout is handled entirely by CSS Grid. No JavaScript calculation required.
console.log("Grid layout initialized cleanly via CSS Grid auto-fit property.");
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
