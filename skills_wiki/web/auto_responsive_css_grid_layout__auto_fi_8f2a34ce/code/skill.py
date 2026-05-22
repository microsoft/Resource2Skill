def create_component(
    output_dir: str,
    title_text: str = "Responsive CSS Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4b525c",     # CSS hex color for card borders/hover
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the auto-responsive CSS Grid layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#131314"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = accent_color  # Default from video is a dark gray
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    /* Center the container on the screen for demonstration */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

header {{
    text-align: center;
    margin-bottom: 40px;
}}

/* THE CORE SKILL: Auto-responsive Grid */
.grid-container {{
    display: grid;
    /* 
       auto-fit: adds as many columns as will fit.
       minmax(300px, 1fr): columns must be at least 300px wide, 
       but will stretch (1fr) to fill remaining space.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-content: center;
    
    width: 100%;
    /* Constrain max width for ultra-wide monitors */
    max-width: {width_px}px; 
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out;
}}

.card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
}}

.card h2 {{
    margin-bottom: 15px;
    font-size: 1.25rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    opacity: 0.8;
}}
"""

    # === Generate Card HTML Snippets ===
    # Generating 6 cards to effectively demonstrate the wrapping behavior
    cards_html = ""
    for i in range(6):
        cards_html += f"""
        <article class="card">
            <h2>Card Title {i + 1}</h2>
            <p>{body_text}</p>
        </article>"""

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
    <header>
        <h1>{title_text}</h1>
    </header>
    
    <main class="grid-container">
        {cards_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// This grid layout is entirely handled by CSS. 
// No JavaScript is required to calculate column widths or wrapping logic.
console.log("Grid layout initialized via CSS.");
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
