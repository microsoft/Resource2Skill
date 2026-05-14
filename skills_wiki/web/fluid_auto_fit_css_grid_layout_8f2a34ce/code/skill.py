def create_component(
    output_dir: str,
    title_text: str = "This is Responsive!",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Auto-Fit CSS Grid Layout visual effect.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user inputs for HTML safety
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = "#4b525c"
        demo_border = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        surface_color = "#ffffff"
        border_color = "#d4d4d8"
        demo_border = "rgba(0, 0, 0, 0.2)"

    # Generate grid items (9 items to clearly show multi-row wrapping)
    grid_items_html = ""
    for i in range(1, 10):
        grid_items_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>{safe_body}</p>
            </div>"""

    # === CSS ===
    css = f"""/* Fluid Auto-Fit CSS Grid Layout — generated component */
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
    --demo-border: {demo_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.page-title {{
    margin-bottom: 30px;
    font-size: 2.5rem;
    text-align: center;
}}

/* A wrapper to allow manual resizing to demonstrate the auto-fit grid */
.demo-resizer {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    resize: horizontal; /* Allows user to drag and resize the container */
    overflow: auto;
    border: 2px dashed var(--demo-border);
    padding: 20px;
    background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 10px,
        rgba(128, 128, 128, 0.03) 10px,
        rgba(128, 128, 128, 0.03) 20px
    );
}}

.demo-instruction {{
    text-align: center;
    font-size: 0.9rem;
    color: var(--accent);
    margin-bottom: 20px;
    font-weight: 600;
}}

/* THE CORE GRID MECHANISM */
.grid-container {{
    display: grid;
    /* 
      auto-fit: Creates as many columns as will fit in the container.
      minmax(300px, 1fr): Each column is at least 300px. 
      If there is extra space, they grow equally (1fr). 
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    
    /* Centers the grid within its container if it maxes out */
    justify-content: center; 
}}

.card {{
    padding: 2em;
    border: 1px solid var(--border);
    border-radius: 10px;
    background-color: var(--surface);
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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

/* Custom Scrollbar for the resizer */
.demo-resizer::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
.demo-resizer::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 4px;
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 class="page-title">{safe_title}</h1>
    
    <div class="demo-resizer">
        <p class="demo-instruction">↘ Drag the bottom-right corner of this box to see the grid automatically reflow!</p>
        
        <div class="grid-container">
            {grid_items_html}
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Auto-Fit CSS Grid Layout — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // Pure CSS handles the grid logic. 
    // Console log to verify initialization.
    console.log("Grid component loaded. Resize the container to see auto-fit and minmax in action.");
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
