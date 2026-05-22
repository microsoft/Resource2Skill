def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Card Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        card_bg = "#222429"
        border_color = "#4b525c"
        text_muted = "#a0aab8"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        card_bg = "#ffffff"
        border_color = "#e5e7eb"
        text_muted = "#6b7280"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --border-color: {border_color};
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
    margin-bottom: 40px;
    max-width: 800px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* 
  To demonstrate the responsiveness effectively, the wrapper has horizontal resize enabled.
  Drag the bottom-right corner of the container to see the grid adapt!
*/
.demo-wrapper {{
    width: 100%;
    max-width: var(--container-width);
    /* Adding resize so the user can easily test the responsive behavior without resizing the whole browser window */
    resize: horizontal;
    overflow: auto;
    border: 1px dashed var(--border-color);
    padding: 20px;
    border-radius: 12px;
}}

/* =========================================
   CORE SKILL: CSS GRID AUTO-FIT MINMAX
   ========================================= */
.grid-container {{
    display: grid;
    /* The magic line: create as many columns as fit, min 300px wide, max 1 fraction of space */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-content: center; /* Centers the grid if items hit max limits */
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2em;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    color: var(--text-color);
}}

.card p {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}
"""

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
        <p>Drag the bottom right corner of the dashed box to resize the container and watch the grid automatically reflow without any media queries.</p>
    </header>

    <div class="demo-wrapper">
        <div class="grid-container" id="grid">
            <!-- Cards will be populated by JavaScript for demonstration purposes -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const bodyText = `{body_text}`;
    
    // Generate 8 cards to clearly demonstrate the grid wrapping behavior
    const numberOfCards = 8;
    
    for (let i = 1; i <= numberOfCards; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        const title = document.createElement('h2');
        title.textContent = `Card Lorem Ipsum ${{i}}`;
        
        const paragraph = document.createElement('p');
        paragraph.textContent = bodyText;
        
        card.appendChild(title);
        card.appendChild(paragraph);
        gridContainer.appendChild(card);
    }}
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
