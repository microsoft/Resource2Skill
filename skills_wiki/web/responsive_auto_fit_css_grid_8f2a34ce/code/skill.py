def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Drag the bottom right corner of the container to resize it. Watch how the CSS Grid automatically calculates the column count and wraps the cards perfectly without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#646cff",     # CSS hex color for accent
    width_px: int = 1000,              # Initial demo container width
    height_px: int = 700,              # Initial demo container height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        page_bg = "#121212"
        demo_bg = "#0f1115"
        card_bg = "#222429"
        text_color = "#ffffff"
        text_muted = "#a0aab8"
        border_color = "#3a3f47"
    else:
        page_bg = "#e9ecef"
        demo_bg = "#ffffff"
        card_bg = "#f8f9fa"
        text_color = "#1a1a2e"
        text_muted = "#6c757d"
        border_color = "#dee2e6"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — generated component */
:root {{
    --page-bg: {page_bg};
    --demo-bg: {demo_bg};
    --card-bg: {card_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    
    /* Core Grid Parameters */
    --min-card-width: 280px; 
    --grid-gap: 20px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* 
  Demo wrapper: Allows you to resize the container to see the 
  grid layout adapt without resizing the whole browser window.
*/
.demo-wrapper {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    background: var(--demo-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    
    /* Make the container resizable by the user */
    resize: both;
    overflow: auto;
    display: flex;
    flex-direction: column;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.5;
    max-width: 600px;
    margin: 0 auto;
}}

/* =========================================
   THE CORE SKILL: AUTO-FIT GRID
   ========================================= */
.grid-container {{
    display: grid;
    /* 
      1. repeat(auto-fit, ...): Creates as many columns as will fit in the container.
      2. minmax(280px, 1fr): Each column is AT LEAST 280px wide, but will stretch 
         equally (1fr) to fill any remaining horizontal space.
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: var(--grid-gap);
    width: 100%;
}}

/* Styling for individual cards */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.card p {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.6;
}}
"""

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

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
    <div class="demo-wrapper">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <!-- The Responsive Grid Component -->
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Component logic
document.addEventListener('DOMContentLoaded', () => {{
    // No JavaScript is required for the core layout!
    // CSS Grid handles the responsive mathematics natively.
    console.log("Grid initialized using CSS auto-fit and minmax().");
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
