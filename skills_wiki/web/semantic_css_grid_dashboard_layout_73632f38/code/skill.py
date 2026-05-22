def create_component(
    output_dir: str,
    title_text: str = "Grid Dashboard",
    body_text: str = "Semantic layout using grid-template-areas",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#d95c3c",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the semantic CSS Grid template areas layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1a1f2e"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Semantic CSS Grid Dashboard — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.app-intro {{
    text-align: center;
    margin-bottom: 10px;
}}

.app-intro h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
}}

.app-intro p {{
    opacity: 0.7;
    font-size: 1rem;
}}

/* Core Grid Layout Implementation */
.grid-container {{
    flex: 1;
    display: grid;
    /* 2 columns: left is 2 fractions, right is 1 fraction */
    grid-template-columns: 2fr 1fr;
    /* 3 rows: Header (auto), Content (fills remaining space), Footer (auto) */
    grid-template-rows: 80px 1fr 80px;
    /* Mapping the layout visually */
    grid-template-areas: 
        "header header"
        "content sidebar"
        "footer footer";
    gap: 20px; /* Space between grid items */
}}

/* Assigning HTML elements to their respective Grid Areas */
.grid-header  {{ grid-area: header; }}
.grid-content {{ grid-area: content; }}
.grid-sidebar {{ grid-area: sidebar; }}
.grid-footer  {{ grid-area: footer; }}

/* Stylistic treatments for the grid items */
.grid-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 1.25rem;
    font-weight: 600;
    box-shadow: 0 4px 6px var(--shadow);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}}

/* Top accent bar for visual flair */
.grid-item::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--border);
    transition: background 0.3s ease;
}}

.grid-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px var(--shadow);
    border-color: var(--accent);
}}

.grid-item:hover::before {{
    background: var(--accent);
}}

.item-label {{
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 0.85rem;
    opacity: 0.6;
    margin-top: 8px;
    font-weight: 500;
}}

/* Responsive behavior: stack vertically on small screens */
@media (max-width: 768px) {{
    .app-wrapper {{
        height: auto;
        min-height: var(--height);
    }}
    .grid-container {{
        grid-template-columns: 1fr;
        grid-template-rows: auto auto auto auto;
        grid-template-areas: 
            "header"
            "content"
            "sidebar"
            "footer";
    }}
    .grid-content {{
        min-height: 300px; /* ensure content has height when stacked */
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="app-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <!-- CSS Grid Container -->
        <div class="grid-container">
            <header class="grid-item grid-header">
                <div>Header</div>
                <div class="item-label">Spans 2 columns</div>
            </header>
            
            <main class="grid-item grid-content">
                <div>Main Content</div>
                <div class="item-label">Takes 2fr width</div>
            </main>
            
            <aside class="grid-item grid-sidebar">
                <div>Sidebar</div>
                <div class="item-label">Takes 1fr width</div>
            </aside>
            
            <footer class="grid-item grid-footer">
                <div>Footer</div>
                <div class="item-label">Spans 2 columns</div>
            </footer>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Semantic CSS Grid Layout
document.addEventListener('DOMContentLoaded', () => {{
    // The layout is purely CSS driven.
    // JS is added here just for simple interaction feedback.
    
    const gridItems = document.querySelectorAll('.grid-item');
    
    gridItems.forEach(item => {{
        item.addEventListener('click', () => {{
            const originalBorder = item.style.borderColor;
            // Provide a quick click ripple/flash effect
            item.style.transform = 'scale(0.98)';
            item.style.borderColor = 'var(--accent)';
            
            setTimeout(() => {{
                item.style.transform = '';
                item.style.borderColor = originalBorder;
            }}, 150);
        }});
    }});
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
