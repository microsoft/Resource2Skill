def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Component",
    body_text: str = "Resize the container using the bottom-right handle to see the grid automatically reflow without media queries.",
    color_scheme: str = "dark",
    accent_color: str = "#e74c3c",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fit Responsive CSS Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f5f5f5"
        surface_color = "#222429"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a1a"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # Generate CSS
    css = f"""/* Auto-Fit Responsive CSS Grid */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: 800px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.page-header p {{
    color: var(--accent-color);
    font-weight: 600;
}}

/* The Resizable Showcase Container */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    /* Adding resize so you can test the grid responsiveness directly */
    resize: both;
    overflow: auto;
    border: 2px dashed var(--accent-color);
    padding: 20px;
    border-radius: 12px;
    background: rgba(0,0,0,0.02);
}}

/* ================================================== */
/* THE CORE SKILL: CSS GRID WITH AUTO-FIT & MINMAX    */
/* ================================================== */
.grid-container {{
    display: grid;
    /* Auto-fit calculates columns dynamically. 
       Minmax ensures columns are at least 300px, but fill up to 1fr */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    width: 100%;
}}

.card {{
    background-color: var(--surface-color);
    padding: 2em;
    border: 1px solid var(--border-color);
    border-top: 3px solid var(--accent-color);
    border-radius: 10px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card p {{
    font-size: 0.9rem;
    line-height: 1.5;
    opacity: 0.8;
}}
"""

    # Generate Card HTML internally
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
            </div>"""

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- The Resizable Wrapper allowing desktop testing of grid reflow -->
    <div class="demo-wrapper">
        
        <!-- The Core Grid Container -->
        <div class="grid-container">
            {cards_html}
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # Generate JS (Empty, as this is a pure CSS solution, but file is provided for structural completeness)
    js = """// No JavaScript required for this responsive grid pattern!
// The layout logic is entirely handled by CSS Grid's auto-fit and minmax().
console.log("CSS Grid layout initialized.");
"""

    # Write files
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
