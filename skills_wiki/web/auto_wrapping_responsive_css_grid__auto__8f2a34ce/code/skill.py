def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Magic",
    body_text: str = "Drag the bottom-right corner of the container below to see the grid automatically wrap and resize its columns.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Wrapping CSS Grid pattern.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        text_muted = "#a0aabf"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgb(209, 213, 219)"

    # Generate dummy cards
    cards_html = ""
    for i in range(1, 8):
        cards_html += f"""
            <div class="card">
                <h2>Card {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Auto-Wrapping Responsive Grid Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
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
    max-width: 800px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Interactive wrapper to demonstrate fluid resizing */
.preview-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    resize: horizontal; /* Allows user to drag and resize to test responsiveness */
    overflow: hidden;
    border: 2px dashed var(--accent-color);
    padding: 20px;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.2);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}}

/* ========================================= */
/* THE CORE SKILL: CSS GRID AUTO-FIT         */
/* ========================================= */
.grid-container {{
    display: grid;
    /* 
       auto-fit: Add as many columns as possible
       minmax: Columns must be at least 250px, but flex to 1fr if space permits
    */
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    
    /* Allow scrolling inside the preview wrapper */
    height: 100%;
    overflow-y: auto;
    padding-right: 10px;
}}

/* Custom scrollbar for the preview */
.grid-container::-webkit-scrollbar {{
    width: 8px;
}}
.grid-container::-webkit-scrollbar-track {{
    background: transparent;
}}
.grid-container::-webkit-scrollbar-thumb {{
    background: var(--border-color);
    border-radius: 4px;
}}

.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    border-color: var(--accent-color);
}}

.card h2 {{
    margin-bottom: 1rem;
    font-size: 1.5rem;
    color: var(--text-color);
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.5;
    font-size: 0.95rem;
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
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- The resizable window to showcase the grid reflow -->
    <div class="preview-wrapper">
        <div class="grid-container">
            {cards_html}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for the grid responsiveness.
// The CSS Grid repeat(auto-fit, minmax()) property handles all layout calculations natively.
console.log("Grid is running entirely on pure CSS.");
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
