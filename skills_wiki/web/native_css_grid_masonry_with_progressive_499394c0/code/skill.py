def create_component(
    output_dir: str,
    title_text: str = "Native CSS Masonry Grid",
    body_text: str = "A highly performant masonry layout using CSS Grid where supported, gracefully degrading to CSS Columns.",
    color_scheme: str = "light",
    accent_color: str = "#e63946",
    width_px: int = 1200,
    height_px: int = 800,
    column_count: int = 3,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f1115"
        text_color = "#f1f3f5"
        text_muted = "#aeb5bd"
        surface_color = "#1c1f26"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
        border = "1px solid rgba(255,255,255,0.05)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#212529"
        text_muted = "#6c757d"
        surface_color = "#ffffff"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
        border = "1px solid rgba(0,0,0,0.05)"

    # Generate dummy items with varying heights to showcase masonry packing
    item_heights = [120, 250, 180, 300, 150, 220, 190, 140, 280]
    items_html = ""
    for i, h in enumerate(item_heights):
        featured_class = " featured" if i == 1 else ""  # Make the second item featured to test spanning
        badge = '<span class="badge">Featured</span>' if i == 1 else ''
        items_html += f"""
        <div class="masonry-item{featured_class}">
            {badge}
            <div class="image-placeholder" style="height: {h}px;"></div>
            <h3 class="card-title">Grid Item {i+1}</h3>
            <p class="card-desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at porttitor sem.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Native CSS Masonry Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --accent: {accent_color};
    --border: {border};
    --shadow: {shadow};
    
    /* Configurable Grid Variables */
    --cols: {column_count};
    --gap: 24px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto 48px auto;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 16px;
    font-weight: 800;
    letter-spacing: -0.03em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.6;
}}

/* =========================================
   1. The Fallback: CSS Multiple Columns
========================================= */
.masonry-container {{
    max-width: {width_px}px;
    margin: 0 auto;
    
    /* Fallback properties */
    columns: var(--cols);
    column-gap: var(--gap);
}}

.masonry-item {{
    background: var(--surface);
    border-radius: 12px;
    padding: 20px;
    box-shadow: var(--shadow);
    border: var(--border);
    position: relative;
    
    /* Crucial for Column fallback: prevents item from snapping in half across columns */
    break-inside: avoid;
    
    /* Vertical spacing for column fallback */
    margin-bottom: var(--gap);
    
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.masonry-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15);
}}

/* =========================================
   2. Progressive Enhancement: Native Grid
========================================= */
@supports (grid-template-rows: masonry) {{
    .masonry-container {{
        /* Switch from columns to Grid */
        display: grid;
        grid-template-columns: repeat(var(--cols), 1fr);
        
        /* The Magic Property */
        grid-template-rows: masonry;
        
        /* Grid handles both row and column gaps */
        gap: var(--gap);
        
        /* Reset fallback properties */
        columns: auto;
    }}
    
    .masonry-item {{
        /* Grid gap handles spacing, remove fallback margin */
        margin-bottom: 0; 
    }}
    
    /* Spanning is uniquely easy in CSS Grid (does not work in Columns fallback) */
    .masonry-item.featured {{
        grid-column: span 2;
    }}
}}

/* Inner Card Styling */
.image-placeholder {{
    background: linear-gradient(135deg, rgba(128,128,128,0.1), rgba(128,128,128,0.2));
    border-radius: 8px;
    margin-bottom: 16px;
    width: 100%;
}}

.card-title {{
    font-size: 1.25rem;
    margin-bottom: 8px;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

.badge {{
    position: absolute;
    top: -10px;
    right: -10px;
    background: var(--accent);
    color: #fff;
    font-size: 0.75rem;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    z-index: 2;
}}

/* Simple Responsive Rules */
@media (max-width: 900px) {{
    :root {{
        --cols: 2;
    }}
    .masonry-item.featured {{
        grid-column: span 1; /* Disable spanning on smaller screens to prevent overflow */
    }}
}}

@media (max-width: 600px) {{
    :root {{
        --cols: 1;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main class="masonry-container">
        {items_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required for this layout!
// Native CSS Grid Masonry (and the CSS Columns fallback) handles 100% of the layout logic.

document.addEventListener('DOMContentLoaded', () => {
    // Check if the browser supports native masonry and log it for debug purposes
    const supportsMasonry = CSS.supports('grid-template-rows', 'masonry');
    if (supportsMasonry) {
        console.log("🚀 Awesome! Your browser supports native CSS Grid Masonry.");
    } else {
        console.log("ℹ️ Your browser is using the CSS Columns fallback layout.");
    }
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
