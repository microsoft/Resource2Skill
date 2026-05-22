def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Drag the handle on the bottom right of the container to test the fluid auto-fit grid mechanics.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#15161a" 
        text_color = "#ffffff"
        text_muted = "#a0aab5"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#1a1a2e"
        text_muted = "#5c6ac4"
        surface_color = "#ffffff"
        border_color = "#dfe3e8"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit CSS Grid Cards */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 800px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.5;
}}

/* 
 * INTERACTIVE WRAPPER 
 * (Added so you can resize the container and see the grid wrap) 
 */
.resize-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: 400px;
    padding: 20px;
    border: 2px dashed var(--border);
    border-radius: 12px;
    resize: horizontal;
    overflow: hidden;
    position: relative;
    background: rgba(0,0,0,0.1);
}}

.resize-wrapper::after {{
    content: "↔ Drag to resize";
    position: absolute;
    bottom: 5px;
    right: 25px;
    font-size: 0.8rem;
    color: var(--text-muted);
    pointer-events: none;
}}

/* =========================================
 * CORE SKILL: THE RESPONSIVE AUTO-FIT GRID 
 * ========================================= */
.grid-container {{
    display: grid;
    /* The Magic Line:
       1. auto-fit: Creates as many columns as will fit.
       2. minmax(300px, 1fr): Cards drop to a new line if they hit 300px, 
          otherwise they grow equally to fill the space.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-content: center; /* Centers the grid tracks if max-width is reached */
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2.5em 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 15px;
    color: var(--text);
}}

.card p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}
"""

    # Generate 7 cards to ensure at least one orphan exists in a 3-column or 4-column setup
    cards_html = ""
    for i in range(1, 8):
        cards_html += f"""
            <article class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </article>"""

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
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <div class="resize-wrapper">
        <main class="grid-container">
            {cards_html}
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Grid handles all the responsiveness natively.
// No JavaScript is required for the auto-fit minmax calculation!
console.log("Grid initialized without JS layout dependencies.");
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
