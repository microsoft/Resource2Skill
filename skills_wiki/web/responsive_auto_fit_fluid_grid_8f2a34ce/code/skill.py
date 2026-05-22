def create_component(
    output_dir: str,
    title_text: str = "Responsive Fluid Grid",
    body_text: str = "Resize the window to see the grid automatically adjust columns and stretch to fill available space.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#646cff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f0f0f0"
        muted_text = "#a0a0a0"
        card_bg = "#222429" # Based on tutorial visuals
        card_border = "#4b525c"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        muted_text = "#555555"
        card_bg = "#ffffff"
        card_border = "#e0e0e0"

    # Define some dummy content for the cards to demonstrate the grid
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
        <div class="card">
            <h2 class="card-title">Card Item {i}</h2>
            <p class="card-desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Fluid Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --muted-text: {muted_text};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}}

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: var(--accent);
}}

header p {{
    color: var(--muted-text);
    line-height: 1.6;
}}

/* === THE CORE SKILL: THE GRID === */
.grid-container {{
    width: 100%;
    max-width: {width_px}px; /* Constrain max width for ultra-wide screens */
    
    /* Grid Magic */
    display: grid;
    /* 
       auto-fit: create as many columns as will fit in the container
       minmax(300px, 1fr): Each column must be at least 300px. 
       If there is leftover space, distribute it equally (1fr) to all columns.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-content: center; /* Centers items if there's only a few and they don't fill the row */
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 32px 24px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    /* Subtle interaction enhancement */
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--muted-text);
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

    <main class="grid-container">
        {cards_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Fluid Grid
// This layout relies entirely on CSS Grid, so no JavaScript layout calculation is needed!
// This script is left empty intentionally to demonstrate that the fluidity is intrinsic to CSS.

document.addEventListener('DOMContentLoaded', () => {{
    console.log('Grid initialized. Resize the window to observe the CSS auto-fit and minmax behavior.');
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
