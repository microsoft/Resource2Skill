def create_component(
    output_dir: str,
    title_text: str = "Zero-Media-Query Grid",
    body_text: str = "Drag the bottom-right corner of the dotted container to resize it. Watch the grid automatically wrap and scale its columns.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Media-Query Auto-Fit CSS Grid effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f5f5f5"
        text_muted = "#a0a0a0"
        surface_color = "#1e1e1e"
        border_color = "#333333"
    else:
        bg_color = "#f8f9fa"
        text_color = "#212529"
        text_muted = "#6c757d"
        surface_color = "#ffffff"
        border_color = "#e9ecef"

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2 class="card-title">Lorem Ipsum {i}</h2>
                <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Zero-Media-Query Auto-Fit Grid — generated component */
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
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 3rem 1rem;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Interactive Resizable Wrapper to demonstrate grid behavior */
.resizable-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: 400px;
    margin: 0 auto;
    padding: 2rem;
    border: 2px dashed var(--accent);
    border-radius: 16px;
    
    /* CSS resize property allows user dragging to test responsiveness */
    resize: horizontal;
    overflow: hidden; /* Required for resize to work */
    background: rgba(0, 0, 0, 0.02);
}}

/* ========================================= */
/* CORE SKILL: The Auto-Fit CSS Grid Pattern */
/* ========================================= */
.grid-container {{
    display: grid;
    gap: 1.5rem; /* Space between rows and columns */
    /* 
       auto-fit: create as many columns as possible
       minmax(280px, 1fr): column must be at least 280px, but will grow to share remaining space
    */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-text {{
    color: var(--text-muted);
    font-size: 0.95rem;
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
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <!-- The wrapper allows manual resizing to test the grid without scaling the whole browser window -->
    <div class="resizable-wrapper">
        <div class="grid-container">
            {cards_html}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// No JavaScript required for this core layout effect!
// The responsiveness is entirely handled by the CSS Grid rendering engine.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid initialized. Try resizing the dashed container.");
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
