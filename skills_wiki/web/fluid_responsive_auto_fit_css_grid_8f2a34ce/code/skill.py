def create_component(
    output_dir: str,
    title_text: str = "Responsive CSS Grid",
    body_text: str = "Resize the browser to see the fluid auto-fit behavior.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1200,
    height_px: int = 800,
    num_cards: int = 9,
    min_card_width_px: int = 300,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#131314"
        text_color = "#ffffff"
        text_muted = "#a0aab4"
        card_bg = "#222429"
        card_border = "#3a3f47"
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        text_muted = "#4b5563"
        card_bg = "#ffffff"
        card_border = "#e5e7eb"

    # Generate Card HTML
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
        <div class="card">
            <h2 class="card-title">Lorem Ipsum {i+1}</h2>
            <p class="card-desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Fluid Responsive Auto-Fit CSS Grid */
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
    --card-border: {card_border};
    --accent: {accent_color};
    --min-card-width: {min_card_width_px}px;
    
    /* Layout properties */
    --grid-gap: 20px;
    --container-max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* === CORE GRID PATTERN === */
.grid-container {{
    display: grid;
    /* 
       The magic formula:
       - auto-fit: fit as many columns as possible
       - minmax(X, 1fr): column must be at least X wide, max 1 fraction of free space
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: var(--grid-gap);
    
    /* Optional: Center the grid if there's leftover space on the sides */
    justify-content: center;
    
    width: 100%;
    max-width: var(--container-max-width);
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-muted);
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
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    
    <div class="grid-container">
        {cards_html}
    </div>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required! 
// The fluid responsiveness is entirely handled by CSS Grid's auto-fit and minmax functions.
console.log("Grid layout is purely CSS-driven.");
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
