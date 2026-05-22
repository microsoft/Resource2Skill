def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Resize the browser window to see the grid items automatically wrap and stretch to fill the available space, entirely without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive Fluid Grid Layout visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        text_muted = "#a0aab8"
        card_surface = "#222429"
        card_border = "rgb(75, 82, 92)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#121212"
        text_muted = "#555555"
        card_surface = "#ffffff"
        card_border = "#e0e4e8"

    # === CSS ===
    css = f"""/* Auto-Responsive Fluid Grid Layout — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --card-surface: {card_surface};
    --card-border: {card_border};
    --container-max-width: {width_px}px;
    --min-card-width: 300px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1rem;
}}

header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--accent-color);
}}

header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

.wrapper {{
    width: 100%;
    max-width: var(--container-max-width);
}}

/* === The Core Grid Technique === */
.grid-container {{
    display: grid;
    /* 
       auto-fit: adds as many columns as will fit based on min width 
       minmax: sets the absolute minimum width, and allows growing up to 1 fraction of remaining space
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: 20px;
    justify-content: center; /* Centers items if they don't stretch fully (e.g. fixed widths), but mostly acts as a fallback */
}}

/* Card Styling */
.card {{
    background-color: var(--card-surface);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-color);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}}

.card h2 {{
    font-size: 1.25rem;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <div class="wrapper">
        <div class="grid-container" id="grid">
            <!-- Cards will be injected by JavaScript to demonstrate flexibility -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Responsive Fluid Grid Layout — dynamic content generator
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    
    // Generate some placeholder content to populate the grid
    const numCards = 8;
    
    for (let i = 1; i <= numCards; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        const title = document.createElement('h2');
        title.textContent = `Card Item ${{i}}`;
        
        const text = document.createElement('p');
        text.textContent = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.';
        
        card.appendChild(title);
        card.appendChild(text);
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
