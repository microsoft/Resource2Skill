def create_component(
    output_dir: str,
    title_text: str = "Zero-Media-Query Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#131316"
        container_bg = "transparent"
        card_bg = "#222429"
        card_border = "#3a3d45"
        text_primary = "#ffffff"
        text_secondary = "#9ca3af"
    else:
        bg_color = "#f3f4f6"
        container_bg = "transparent"
        card_bg = "#ffffff"
        card_border = "#e5e7eb"
        text_primary = "#111827"
        text_secondary = "#4b5563"

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2 class="card-title">Card {i}</h2>
                <p class="card-text">{body_text}</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid Component */
:root {{
    --bg-color: {bg_color};
    --container-bg: {container_bg};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    
    /* Configurable constraints passed from Python */
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    /* Optional: constrain to height_px if strictly desired, though grids usually want to flow naturally */
}}

.page-title {{
    margin-bottom: 40px;
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    color: var(--text-primary);
}}

/* ========================================================= */
/* THE CORE SKILL: Zero-Media-Query Grid Container           */
/* ========================================================= */
.grid-container {{
    display: grid;
    /* 
       repeat(): apply a pattern
       auto-fit: place as many columns as fit, collapse empty ones
       minmax(): card must be at least 300px, but can grow to fill 1 fraction of available space 
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    
    /* Container constraints */
    width: 100%;
    max-width: var(--comp-width);
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 30px 25px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.card-text {{
    font-size: 1rem;
    line-height: 1.5;
    color: var(--text-secondary);
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
    <h1 class="page-title">{title_text}</h1>
    
    <!-- Grid Container -->
    <div class="grid-container">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// The core mechanic of this component is handled entirely by CSS Grid.
// No JavaScript is required for the responsive resizing or reflowing.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid initialized. Resize the window to observe auto-fit in action.");
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
