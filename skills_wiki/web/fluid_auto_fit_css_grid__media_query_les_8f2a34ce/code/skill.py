def create_component(
    output_dir: str,
    title_text: str = "Fluid Grid Layout",
    body_text: str = "Drag the bottom-right corner of the container below to resize it. Watch how the grid automatically adapts, wrapping cards and maintaining strict column alignment without a single media query.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1100,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Auto-Fit CSS Grid layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        card_bg = "#222429"
        text_main = "#ffffff"
        text_muted = "#a0aab2"
        border_color = "#3a3f47"
        demo_bg = "#15161b"
    else:
        bg_color = "#f8f9fa"
        card_bg = "#ffffff"
        text_main = "#1a1d20"
        text_muted = "#5c6b7a"
        border_color = "#e1e4e8"
        demo_bg = "#eaedf1"

    # === CSS ===
    css = f"""/* Fluid Auto-Fit CSS Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --demo-bg: {demo_bg};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.page-header {{
    text-align: center;
    max-width: 800px;
    margin-bottom: 40px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 16px;
}}

.page-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* Resizable wrapper purely for demonstration purposes */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    background-color: var(--demo-bg);
    border: 2px dashed var(--border-color);
    border-radius: 16px;
    padding: 30px;
    overflow: auto;
    resize: horizontal; /* Allows user to drag and test responsiveness */
    position: relative;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}}

.demo-wrapper::after {{
    content: '↔ Drag to resize';
    position: absolute;
    bottom: 10px;
    right: 25px;
    font-size: 0.8rem;
    color: var(--text-muted);
    pointer-events: none;
}}

/* =========================================
   CORE SKILL: FLUID AUTO-FIT GRID
   ========================================= */
.grid-container {{
    display: grid;
    /* 
       The magic formula: 
       1. auto-fit: Create as many columns as will fit.
       2. minmax(280px, 1fr): Columns must be at least 280px. 
          If there's extra space, divide it equally (1fr).
    */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    width: 100%;
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 32px 24px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: var(--accent-color);
}}

.card h2 {{
    font-size: 1.25rem;
    color: var(--text-main);
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.card-accent-bar {{
    width: 40px;
    height: 4px;
    background-color: var(--accent-color);
    border-radius: 2px;
    margin: 0 auto;
}}
"""

    # === HTML ===
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <div class="card-accent-bar"></div>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

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

    <div class="demo-wrapper">
        <div class="grid-container">
            {cards_html}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Auto-Fit CSS Grid 
// No JavaScript is required for the grid reflow algorithm! 
// CSS Grid handles the responsive math natively via repeat(auto-fit, minmax(...)).

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid loaded. Try resizing the demo container!");
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
