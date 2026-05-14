def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Demo",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",
    accent_color: str = "#4b525c",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        surface_color = "#222429"
        text_color = "#ffffff"
        text_muted = "#cccccc"
        border_color = accent_color
    else:
        bg_color = "#f0f2f5"
        surface_color = "#ffffff"
        text_color = "#1a1a1a"
        text_muted = "#555555"
        border_color = "#d1d5db"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --border: {border_color};
    --accent: #3b82f6;
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

.header-container {{
    text-align: center;
    margin-bottom: 40px;
}}

/* 
  Resizable Wrapper for Demonstration 
  (Allows testing the responsive layout without resizing the whole window)
*/
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-width: 320px;
    padding: 20px;
    border: 2px dashed rgba(128, 128, 128, 0.3);
    border-radius: 12px;
    resize: horizontal; /* Interactive resizing handle */
    overflow: auto;
    background: rgba(0,0,0,0.2);
}}

.demo-label {{
    text-align: right;
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 10px;
    font-style: italic;
}}

/* ========================================= */
/* THE CORE SKILL: Responsive Auto-Fit Grid  */
/* ========================================= */
.grid-container {{
    display: grid;
    /* 
       The Magic Formula:
       auto-fit: create as many columns as will fit.
       minmax(300px, 1fr): columns must be at least 300px wide, 
                           but stretch (1fr) to fill remaining space.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px; /* Spacing between rows and columns */
}}

/* Card Styling to match tutorial */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    border-color: var(--accent);
}}

.card h2 {{
    margin-bottom: 10px;
    font-size: 1.25rem;
    color: var(--text);
}}

.card p {{
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--text-muted);
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
    <div class="header-container">
        <h1>{title_text}</h1>
        <p style="margin-top: 8px; color: var(--text-muted);">Drag the bottom-right corner of the dashed box to see the grid auto-wrap.</p>
    </div>

    <div class="demo-wrapper">
        <div class="demo-label">↕ Drag corner to resize container</div>
        
        <!-- The Grid Container -->
        <div class="grid-container" id="grid">
            <!-- Cards will be injected here by script.js -->
        </div>
    </div>

    <script src="script.js"></script>
    <script>
        // Data injected from Python generator
        window.componentData = {{
            bodyText: "{body_text}"
        }};
    </script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Inject mock data to populate the responsive grid
document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid');
    const bodyText = window.componentData.bodyText;
    
    // Generate 9 placeholder cards to show multiple rows wrapping
    const cardCount = 9;
    
    let htmlContent = '';
    
    for (let i = 1; i <= cardCount; i++) {
        htmlContent += `
            <div class="card">
                <h2>Lorem Ipsum ${i}</h2>
                <p>${bodyText}</p>
            </div>
        `;
    }
    
    gridContainer.innerHTML = htmlContent;
});
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
