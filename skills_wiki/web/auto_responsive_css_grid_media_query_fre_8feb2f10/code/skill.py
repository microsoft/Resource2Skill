def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Resize the browser window to see the grid seamlessly adapt without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 100,               # Using 100% width internally, this parameter serves as reference container max-width if needed
    height_px: int = 800,
    item_count: int = 9,               # Number of cards to generate
    min_col_width: int = 300,          # The minimum width of a grid item before it wraps
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"          # Video: rgb(13, 13, 20)
        text_color = "#ffffff"
        card_bg = "#222429"           # Video: #222429
        border_color = "#4b525c"      # Video: rgb(75, 82, 92)
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        border_color = "#d1d5db"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg: {card_bg};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --min-col-width: {min_col_width}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: clamp(20px, 5vw, 50px); /* Responsive padding around container */
}}

.page-header {{
    text-align: center;
    margin-bottom: 40px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.page-header p {{
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

/* === The Core Grid Magic === */
.grid-container {{
    display: grid;
    /* 
      1. auto-fit: Create as many columns as will fit.
      2. minmax(300px, 1fr): Columns must be at least 300px wide. 
         If there's extra space, stretch them evenly (1fr) to fill it. 
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-col-width), 1fr));
    gap: 15px;
    
    max-width: 1400px; /* Optional constraint to prevent excessive stretching on ultrawides */
    margin: 0 auto;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    
    /* Subtle interaction */
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-color);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    opacity: 0.8;
}}
"""

    # === JavaScript (for populating dynamic cards) ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('responsive-grid');
    const itemCount = {item_count};
    
    // Generate cards dynamically
    for (let i = 1; i <= itemCount; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        card.innerHTML = `
            <h2>Card Title ${{i}}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        `;
        
        gridContainer.appendChild(card);
    }}
}});
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main>
        <!-- The container that holds the responsive grid -->
        <div id="responsive-grid" class="grid-container">
            <!-- Cards will be injected here by script.js -->
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

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
