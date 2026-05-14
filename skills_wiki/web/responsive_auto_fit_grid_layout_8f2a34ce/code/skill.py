def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
        slider_track = "#333"
    else:
        bg_color = "#f4f4f5"
        text_color = "#1a1a1a"
        surface_color = "#ffffff"
        border_color = "#d1d5db"
        slider_track = "#e5e7eb"

    # Settings
    card_count = 6
    card_min_width = 300
    gap_size = 15

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — generated component */
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
    --slider-track: {slider_track};
    --width-max: {width_px}px;
    --card-min-width: {card_min_width}px;
    --grid-gap: {gap_size}px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: min(50px, 5%);
    display: flex;
    flex-direction: column;
    align-items: center;
}}

header {{
    text-align: center;
    margin-bottom: 40px;
    width: 100%;
    max-width: var(--width-max);
}}

h1 {{
    margin-bottom: 10px;
    font-size: 2.5rem;
}}

.header-subtitle {{
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}}

/* Interactive Demo Controls */
.demo-controls {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    padding: 15px 25px;
    border-radius: 10px;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    gap: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}}

.demo-controls input[type="range"] {{
    -webkit-appearance: none;
    width: 200px;
    background: transparent;
}}

.demo-controls input[type="range"]::-webkit-slider-thumb {{
    -webkit-appearance: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: var(--accent);
    cursor: pointer;
    margin-top: -6px;
}}

.demo-controls input[type="range"]::-webkit-slider-runnable-track {{
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: var(--slider-track);
    border-radius: 2px;
}}

.width-display {{
    font-family: monospace;
    font-size: 1.1rem;
    color: var(--accent);
    font-weight: bold;
    min-width: 70px;
}}

/* =========================================
   CORE GRID MAGIC
   ========================================= */
.grid-container {{
    display: grid;
    /* The magic formula: dynamically create columns based on min width, and let them stretch (1fr) */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center;
    
    /* Layout constraints for demonstration */
    width: 100%;
    max-width: var(--width-max);
    margin: 0 auto;
    
    /* Smooth transition to show reflow nicely during slider adjustment */
    transition: width 0.1s ease-out;
}}

/* Card Styles */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-top: 4px solid var(--border);
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    border-top-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.6;
    opacity: 0.8;
}}
"""

    # === HTML ===
    cards_html = ""
    for i in range(card_count):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum</h2>
            <p>{body_text}</p>
        </div>"""

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
    <header>
        <h1>{title_text}</h1>
        <p class="header-subtitle">Resize the slider below to see the CSS Grid <code>repeat(auto-fit, minmax(300px, 1fr))</code> algorithm dynamically recalculate columns and wrap elements.</p>
    </header>

    <div class="demo-controls">
        <label for="width-slider"><strong>Container Width:</strong></label>
        <input type="range" id="width-slider" min="320" max="{width_px}" value="{width_px}">
        <span id="width-display" class="width-display">{width_px}px</span>
    </div>

    <!-- The Reusable Component -->
    <div class="grid-container" id="grid-demo">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Grid Demo Logic
document.addEventListener('DOMContentLoaded', () => {{
    const slider = document.getElementById('width-slider');
    const display = document.getElementById('width-display');
    const gridContainer = document.getElementById('grid-demo');

    // Update grid container width based on slider input to demonstrate auto-fit
    slider.addEventListener('input', (e) => {{
        const currentWidth = e.target.value;
        gridContainer.style.maxWidth = currentWidth + 'px';
        display.textContent = currentWidth + 'px';
    }});
    
    // Initial sync
    const initialWidth = slider.value;
    gridContainer.style.maxWidth = initialWidth + 'px';
    display.textContent = initialWidth + 'px';
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
