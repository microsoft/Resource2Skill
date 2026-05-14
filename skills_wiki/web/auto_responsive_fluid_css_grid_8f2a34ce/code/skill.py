def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Resize your browser window to see the cards wrap and scale fluidly without any media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive Fluid CSS Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        text_color = "#ffffff"
        card_bg = "#222429"
        card_border = "#4b525c"
        text_muted = "#a0aab5"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        card_bg = "#ffffff"
        card_border = "#e5e7eb"
        text_muted = "#6b7280"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
    --min-card-width: 300px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
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
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 1.1rem;
}}

/* THE CORE SKILL: Auto-Responsive Grid */
.grid-container {{
    display: grid;
    /* 
       auto-fit: Add as many columns as possible.
       minmax: Columns must be at least 300px, but will expand (1fr) to fill remaining space.
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: 1.5rem; /* Space between rows and columns */
    
    width: 100%;
    max-width: {width_px}px; /* Prevent it from getting too absurdly wide on ultra-wides */
    
    /* Optional: Center items if there's leftover space and max-width is hit */
    justify-content: center;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.card-icon {{
    font-size: 2rem;
    color: var(--accent);
    margin-bottom: 1rem;
}}
"""

    # Generate 8 cards to demonstrate the wrapping behavior
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
        <div class="card">
            <div class="card-icon">✦</div>
            <h2>Lorem Ipsum {i}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed.</p>
        </div>"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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
    js = f"""// Auto-Responsive Grid — No JS required for layout!
// The layout is handled entirely by CSS Grid (repeat, auto-fit, minmax).
// This script is intentionally left sparse as proof of the CSS Grid's power.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("CSS Grid layout initialized.");
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
