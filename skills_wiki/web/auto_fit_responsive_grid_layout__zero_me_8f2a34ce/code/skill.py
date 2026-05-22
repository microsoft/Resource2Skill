def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Drag the handle on the bottom-right of the dotted container to see the grid reflow instantly.",
    color_scheme: str = "dark",
    accent_color: str = "#6366f1",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fit Responsive Grid layout.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        text_color = "#f0f0f0"
        card_bg = "#222429"
        card_border = "#4b525c"
        text_muted = "#a1a1aa"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        card_bg = "#ffffff"
        card_border = "#e4e4e7"
        text_muted = "#52525b"

    # === CSS ===
    css = f"""/* Auto-Fit Responsive Grid — generated component */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Interactive Resizable Wrapper (For demonstration purposes) */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: 400px;
    padding: 2rem;
    border: 2px dashed var(--card-border);
    border-radius: 16px;
    resize: horizontal; /* Allows user to drag and test responsiveness */
    overflow: auto;     /* Required for resize to work */
    background: rgba(0, 0, 0, 0.02);
}}

/* === CORE GRID CSS === */
.grid-container {{
    display: grid;
    /* 
       The core logic:
       auto-fit: Add as many columns as fit the container.
       minmax: Each column is minimum 280px wide (down to 100% on extreme small screens), 
               and maximum 1fr (takes up remaining space evenly).
    */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: 1.5rem;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}}

.card h2 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.card p {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
}}
"""

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
            <article class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed.</p>
            </article>"""

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
    
    <div class="demo-wrapper">
        <div class="grid-container">
            {cards_html}
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Fit Responsive Grid 
// Note: This layout is achieved 100% with CSS. 
// No JavaScript is required for the grid reflowing behavior.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid layout initialized. Try resizing the dotted container!");
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
