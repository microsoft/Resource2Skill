def create_component(
    output_dir: str,
    title_text: str = "Fluid Auto-Fit Grid",
    body_text: str = "Drag the handle on the bottom-right of the container to resize it and watch the grid recalculate automatically.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        surface_hover = "#f1f5f9"

    card_min_width = 250
    grid_gap = 20

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid */
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
    --surface-hover: {surface_hover};
    --border: {border_color};
    --card-min-width: {card_min_width}px;
    --grid-gap: {grid_gap}px;
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
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.5;
}}

/* Resizable wrapper to demonstrate the grid fluidity without resizing the browser window */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    resize: horizontal;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 2rem;
    border: 2px dashed var(--border);
    border-radius: 12px;
    position: relative;
    background: radial-gradient(circle at top right, rgba(0,0,0,0.02), transparent);
}}

.demo-wrapper::-webkit-resizer {{
    border: 3px solid var(--accent);
    background: var(--accent);
    box-shadow: 0 0 10px var(--accent);
}}

/* THE CORE SKILL: Responsive CSS Grid */
.grid-container {{
    display: grid;
    /* This single line creates the responsive wrapping behavior */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center;
}}

/* Card Styling */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.card:hover {{
    background-color: var(--surface-hover);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: var(--text);
}}

.card p {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* Status indicator for the demo */
.status-bar {{
    position: absolute;
    top: 0.5rem;
    right: 1rem;
    font-family: monospace;
    font-size: 0.85rem;
    color: var(--accent);
    background: var(--bg);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    border: 1px solid var(--border);
}}
"""

    # Generate Card HTML blocks
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
            <div class="card">
                <h2>Lorem Ipsum {i}</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed.</p>
            </div>"""

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

    <div class="demo-wrapper" id="resizable-container">
        <div class="status-bar" id="status-display">Width: {width_px}px | Columns: -</div>
        <div class="grid-container" id="grid">
            {cards_html}
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Grid - Demonstration Logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('resizable-container');
    const statusDisplay = document.getElementById('status-display');
    const grid = document.getElementById('grid');

    // Observe changes to the container's width to demonstrate dynamic wrapping
    if(container && statusDisplay && grid) {{
        const observer = new ResizeObserver(entries => {{
            for (let entry of entries) {{
                const width = Math.round(entry.contentRect.width);
                
                // Dynamically calculate how many columns are currently rendered
                // by checking the grid-template-columns computed style
                const computedStyle = window.getComputedStyle(grid);
                const columnsCount = computedStyle.getPropertyValue('grid-template-columns').split(' ').length;
                
                statusDisplay.textContent = `Width: ${{width}}px | Columns: ${{columnsCount}}`;
            }}
        }});
        
        // Start observing
        observer.observe(container);
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
