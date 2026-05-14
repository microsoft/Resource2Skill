def create_component(
    output_dir: str,
    title_text: str = "This is Responsive!",
    body_text: str = "Resize the dotted container box from the bottom right corner to see the grid automatically adjust and wrap.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Auto-Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    # Escape HTML inputs to prevent XSS
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        card_bg = "#222429"
        card_border = "rgb(75, 82, 92)"
        wrapper_bg = "rgba(255, 255, 255, 0.02)"
    else:
        bg_color = "#f4f4f9"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        card_border = "#d1d5db"
        wrapper_bg = "rgba(0, 0, 0, 0.02)"

    # Generate mock cards based on tutorial content
    mock_cards = ""
    for _ in range(6):
        mock_cards += f"""
            <div class="card">
                <h2>Lorem Ipsum</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive CSS Auto-Grid Layout — generated component */
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
    --wrapper-bg: {wrapper_bg};
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--accent);
    font-weight: 600;
}}

/* Interactive wrapper to demonstrate resizing */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    min-height: 400px;
    resize: both;
    overflow: auto;
    background-color: var(--wrapper-bg);
    border: 2px dashed var(--accent);
    border-radius: 12px;
    padding: 30px;
    position: relative;
}}

.demo-wrapper::after {{
    content: "↘ Drag to resize";
    position: absolute;
    bottom: 5px;
    right: 15px;
    font-size: 0.8rem;
    color: var(--accent);
    opacity: 0.7;
    pointer-events: none;
}}

/* === Core Skill: The Auto-Grid === */
.grid-container {{
    display: grid;
    /* This is the magic line. Auto-fit creates columns. Minmax ensures they don't crush. */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    justify-content: center;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    border-color: var(--accent);
}}

.card h2 {{
    margin-bottom: 15px;
    font-size: 1.5rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </div>

    <!-- The demo-wrapper allows manual resizing to test the grid -->
    <div class="demo-wrapper">
        <div class="grid-container">
            {mock_cards}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive CSS Auto-Grid Layout
document.addEventListener('DOMContentLoaded', () => {{
    const demoWrapper = document.querySelector('.demo-wrapper');
    
    // Optional: Log width changes to demonstrate no media queries are firing
    let resizeObserver = new ResizeObserver(entries => {{
        for (let entry of entries) {{
            console.log(`Container resized to: ${{entry.contentRect.width}}px`);
            // The CSS Grid handles the internal reflow entirely natively!
        }}
    }});
    
    if (demoWrapper) {{
        resizeObserver.observe(demoWrapper);
    }}
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
