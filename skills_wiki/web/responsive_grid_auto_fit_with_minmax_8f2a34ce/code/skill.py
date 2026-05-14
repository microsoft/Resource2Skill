def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Patterns",
    body_text: str = "Resize the window to see the grid automatically adjust. No media queries required.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    min_col_width_px: int = 300,
    card_count: int = 8,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Grid Auto-Fit visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f0f0f0"
        text_muted = "#a0a0a0"
        card_bg = "#222429"
        card_border = "#3a3c42"
    else:
        bg_color = "#f4f5f7"
        text_color = "#1a1a2e"
        text_muted = "#5a5a6e"
        card_bg = "#ffffff"
        card_border = "#e0e0e0"

    # Generate dummy cards
    cards_html = ""
    for i in range(1, card_count + 1):
        cards_html += f"""
        <div class="card">
            <h2 class="card-title">Lorem Ipsum {i}</h2>
            <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Responsive Grid Auto-Fit — generated component */
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
    --card-bg: {card_bg};
    --card-border: {card_border};
    --min-col-width: {min_col_width_px}px;
    --max-container-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* === Core Grid Magic === */
.grid-container {{
    width: 100%;
    max-width: var(--max-container-width);
    
    /* The core technique: */
    display: grid;
    /* min(100%, ...) ensures it doesn't break on extremely narrow screens */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--min-col-width)), 1fr));
    gap: 1.5rem;
    
    /* Centers items if the container is wider than the max possible span */
    justify-content: center; 
}}

.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
}}

.card-text {{
    font-size: 0.95rem;
    line-height: 1.6;
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
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>
    
    <main class="grid-container">
        {cards_html}
    </main>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Grid Auto-Fit
// No JavaScript required for the layout engine!
// CSS Grid handles 100% of the responsiveness.

document.addEventListener('DOMContentLoaded', () => {
    console.log("Grid initialized successfully.");
});
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
