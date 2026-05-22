def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Resize the browser window to see the columns automatically wrap and adjust.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        text_muted = "#a1a1aa"
        card_bg = "#222222"
        card_border = "#333333"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        text_muted = "#52525b"
        card_bg = "#ffffff"
        card_border = "#e4e4e7"

    # Generate dummy cards
    cards_html = ""
    for i in range(6):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — generated component */
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
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.page-header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* --- Core Visual Effect: Auto-Fit Grid --- */
.grid-container {{
    width: 100%;
    max-width: var(--max-width);
    display: grid;
    /* The magic formula: fit as many 300px columns as possible, stretch remaining space */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    justify-content: center;
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.6;
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
    <header class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <!-- The Grid Container -->
    <main class="grid-container">
        {cards_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid — interaction logic
// Note: The core layout requires zero JavaScript. CSS Grid handles all resizing natively.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid component loaded. Resize the window to see auto-fit in action.");
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
