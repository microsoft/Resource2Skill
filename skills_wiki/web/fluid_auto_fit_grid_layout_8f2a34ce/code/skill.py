def create_component(
    output_dir: str,
    title_text: str = "This is Responsive!",
    body_text: str = "Resize the container to see the grid automatically wrap and scale.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4facfe",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    card_count: int = 6,               # Number of cards to generate
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Auto-Fit Grid Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "white"
        card_bg = "#222429"
        card_border = "rgb(75, 82, 92)"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f4f4f8"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        card_border = "#e0e0e0"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === Generate Card HTML ===
    cards_html = ""
    for i in range(card_count):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum {i+1}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Fluid Auto-Fit Grid Layout — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
}}

/* A resizable container to demonstrate the effect without resizing the whole browser window */
.wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    resize: horizontal; /* Allow manual resizing for testing */
    padding: 20px;
    border: 2px dashed var(--card-border);
    border-radius: 12px;
}}

.header-block {{
    text-align: center;
    margin-bottom: 40px;
}}

.header-block h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header-block p {{
    color: var(--accent);
    font-weight: 600;
}}

/* THE CORE COMPONENT LOGIC */
.grid-container {{
    display: grid;
    /* The magic line: Fits as many 300px columns as possible, stretches them to fill gaps */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
    gap: 15px;
    justify-content: center; /* Centers the grid block if there's leftover space */
    width: 100%;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    box-shadow: 0 4px 15px var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 15px;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px var(--shadow);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    opacity: 0.85;
}}
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
    <div class="wrapper">
        <div class="header-block">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Auto-Fit Grid Layout — utility script
document.addEventListener('DOMContentLoaded', () => {{
    // The grid is 100% CSS-driven. 
    // This JS simply logs the current grid capacity for educational/debug purposes.
    const grid = document.querySelector('.grid-container');
    const wrapper = document.querySelector('.wrapper');
    
    const updateGridInfo = () => {{
        const columns = window.getComputedStyle(grid).getPropertyValue('grid-template-columns');
        const numColumns = columns.split(' ').length;
        console.log(`Grid is currently displaying ${{numColumns}} column(s) within ${{wrapper.clientWidth}}px`);
    }};

    // Observe resizing of the wrapper
    const observer = new ResizeObserver(updateGridInfo);
    observer.observe(wrapper);
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
