def create_component(
    output_dir: str,
    title_text: str = "Responsive Minmax Grid",
    body_text: str = "Resize the browser window to see the grid automatically wrap and scale using CSS Grid's auto-fit and minmax() functions. No media queries required.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4a90e2",     # CSS hex color for accent
    width_px: int = 1200,              # Max container width
    height_px: int = 800,              # Minimum container height
    card_count: int = 6,               # Number of cards to generate
    min_col_width: int = 300,          # Minimum width of a grid card
    gap_px: int = 20,                  # Gap between grid items
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fitting Fluid CSS Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        text_color = "#ffffff"
        body_text_color = "#a0aab5"
        surface_color = "#222429"
        border_color = "#4b525c"
        hover_surface = "#2a2d33"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        body_text_color = "#4b5563"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"
        hover_surface = "#f9fafb"

    # Generate the cards HTML
    cards_html = ""
    for i in range(card_count):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Auto-Fitting Fluid CSS Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {body_text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {hover_surface};
    --border: {border_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
    --min-col-width: {min_col_width}px;
    --grid-gap: {gap_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: min(50px, 7vw);
}}

/* Main wrapper to respect width constraint */
.wrapper {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Typography */
.header-area {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}}

.header-area h1 {{
    font-size: 2.5rem;
    margin-bottom: 15px;
    color: var(--text);
}}

.header-area p {{
    font-size: 1.1rem;
    line-height: 1.5;
    color: var(--text-muted);
}}

/* 
 * THE CORE SKILL: THE MINMAX GRID 
 * This automatically fits as many columns as possible that are at least 
 * var(--min-col-width) wide, and stretches them equally (1fr) to fill remaining space.
 */
.grid-container {{
    width: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(var(--min-col-width), 1fr));
    gap: var(--grid-gap);
}}

/* Card Styling */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.card:hover {{
    transform: translateY(-4px);
    background-color: var(--surface-hover);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text);
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

/* Highlighted accent text */
.accent {{
    color: var(--accent);
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
    <div class="wrapper">
        <div class="header-area">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <!-- The Core Grid Component -->
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Fitting Fluid CSS Grid — Optional Interactive Enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.querySelector('.grid-container');
    const cards = document.querySelectorAll('.card');

    // Add a simple entrance animation to demonstrate grid item rendering
    cards.forEach((card, index) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {{
            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            
            // Restore hover transition after entrance animation completes
            setTimeout(() => {{
                card.style.transition = 'transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease';
            }}, 400);
            
        }}, index * 100); // Stagger entrance
    }});
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
