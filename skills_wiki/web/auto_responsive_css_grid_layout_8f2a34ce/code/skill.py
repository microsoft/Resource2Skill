def create_component(
    output_dir: str,
    title_text: str = "Responsive CSS Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff", 
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid Layout.
    Includes a resizable wrapper to demonstrate the grid wrapping behavior directly.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        card_bg = "#222429"
        card_border = "rgb(75, 82, 92)"
        text_color = "#ffffff"
    else:
        bg_color = "#f0f2f5"
        card_bg = "#ffffff"
        card_border = "#e1e4e8"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --text-color: {text_color};
    --accent: {accent_color};
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 30px;
}}

/* 
  Interactive wrapper to demonstrate responsiveness 
  without needing to resize the browser window.
*/
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    resize: horizontal;
    overflow: auto;
    border: 2px dashed var(--card-border);
    padding: 20px;
    border-radius: 12px;
    background: rgba(0,0,0,0.2);
}}

/* === The Core Grid Implementation === */
.grid-container {{
    display: grid;
    /* 
      auto-fit: create as many columns as will fit in the container.
      minmax(300px, 1fr): column must be at least 300px, but can grow to fill space equally.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    justify-content: center;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    border-color: var(--accent);
}}

.card h2 {{
    margin-bottom: 15px;
    font-size: 1.25rem;
}}

.card p {{
    font-size: 0.9rem;
    line-height: 1.5;
    opacity: 0.85;
}}

/* Instruction tooltip styling */
.instruction {{
    font-size: 0.85rem;
    color: var(--accent);
    margin-bottom: 10px;
    text-align: center;
}}
"""

    # Generate multiple cards to populate the grid
    cards_html = ""
    for i in range(6):
        cards_html += f"""
            <div class="card">
                <h2>Card {i + 1}</h2>
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
    <div class="header">
        <h1>{title_text}</h1>
    </div>
    
    <div class="instruction">
        &#8596; Drag the bottom-right corner of the dashed box to resize and see the grid adapt!
    </div>

    <div class="demo-wrapper">
        <div class="grid-container">
            {cards_html}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for the grid layout! 
// CSS Grid handles all the responsive calculations natively.
console.log("CSS Grid layout initialized.");
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
