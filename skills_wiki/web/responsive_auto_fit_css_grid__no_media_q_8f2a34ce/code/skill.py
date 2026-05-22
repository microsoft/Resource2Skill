def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Resize the browser window to see the cards automatically wrap and adjust their widths seamlessly using CSS Grid auto-fit and minmax().",
    color_scheme: str = "dark",
    accent_color: str = "#4a90e2",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#16181d"
        text_color = "#f0f0f0"
        surface_color = "#222429"
        border_color = "rgba(255, 255, 255, 0.1)"
        muted_text = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        muted_text = "rgba(0, 0, 0, 0.6)"

    # Number of cards to generate for demonstration
    num_cards = kwargs.get("num_cards", 8)
    min_card_width = kwargs.get("min_card_width", "300px")

    # Generate Card HTML
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
            <div class="card">
                <h2 class="card-title">Lorem Ipsum {i+1}</h2>
                <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --muted: {muted_text};
    --min-card-width: {min_card_width};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 800px;
}}

.page-title {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.page-subtitle {{
    color: var(--muted);
    font-size: 1.1rem;
    line-height: 1.5;
}}

/* === THE CORE GRID LAYOUT === */
.grid-container {{
    width: 100%;
    max-width: 1400px; /* Optional: cap max width for ultrawide screens */
    
    /* Establish the grid */
    display: grid;
    
    /* 
      The Magic Formula:
      auto-fit: create as many columns as will fit.
      minmax: columns must be at least var(--min-card-width), but can grow to fill 1 fraction of free space.
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    
    /* Spacing between cards */
    gap: 20px;
}}

/* Card Styling */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    font-weight: 600;
}}

.card-text {{
    color: var(--muted);
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
        <h1 class="page-title">{title_text}</h1>
        <p class="page-subtitle">{body_text}</p>
    </header>

    <!-- Component Area -->
    <div class="grid-container">
{cards_html}
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid
// No JavaScript is required for this layout! 
// The magic happens entirely in CSS using grid-template-columns: repeat(auto-fit, minmax(...));

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid initialized purely with CSS.");
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
