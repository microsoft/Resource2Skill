def create_component(
    output_dir: str,
    title_text: str = "Grid Lanes Gallery",
    body_text: str = "A fluid, masonry-style layout simulating the upcoming CSS display: grid-lanes specification.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Grid Lanes (Masonry) Layout visual effect.
    """
    import os
    import random

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # Generate random heights for cards to simulate Masonry content
    card_heights = [random.randint(150, 450) for _ in range(16)]

    # === CSS ===
    css = f"""/* Grid Lanes (Masonry) — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --lane-gap: 24px;
    --row-height: 10px; /* Fine-grained base grid for packing */
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
    justify-content: center;
    padding: 40px 20px;
    overflow-y: auto;
    overflow-x: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
}}

header {{
    margin-bottom: 40px;
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}}

/* 
 * GRID LANES IMPLEMENTATION 
 * Polyfilling the upcoming `display: grid-lanes` spec 
 */
.grid-lanes {{
    display: grid;
    /* Responsive lanes based on minimum width */
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    /* Tiny row height acts as our vertical resolution */
    grid-auto-rows: var(--row-height);
    /* Only horizontal gap applied here; vertical gap is handled by the JS span logic */
    column-gap: var(--lane-gap);
    align-items: start;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 4px 6px -1px var(--shadow), 0 2px 4px -2px var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 20px -5px var(--shadow), 0 8px 10px -6px var(--shadow);
}}

.card-content {{
    padding: 24px;
    display: flex;
    flex-direction: column;
    height: 100%;
}}

.card-tag {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
    align-self: flex-start;
}}

.card h3 {{
    font-size: 1.25rem;
    margin-bottom: 8px;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* Visual placeholder for media/images */
.card-media {{
    width: 100%;
    background: linear-gradient(135deg, var(--border), transparent);
    border-bottom: 1px solid var(--border);
}}
"""

    # === HTML ===
    cards_html = ""
    for i, h in enumerate(card_heights):
        media_height = h - 150 if h > 200 else 0
        media_html = f'<div class="card-media" style="height: {media_height}px;"></div>' if media_height > 0 else ""
        cards_html += f"""
        <article class="card">
            {media_html}
            <div class="card-content">
                <span class="card-tag">Item {i+1}</span>
                <h3>Lane Entry {i+1}</h3>
                <p>Dynamic content naturally flowing into vertical columns, adapting to the height required.</p>
            </div>
        </article>"""

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
    <div class="wrapper">
        <header>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <main class="grid-lanes" id="masonry-grid">
            {cards_html}
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Grid Lanes (Masonry) — dynamic packing logic
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('masonry-grid');
    const items = grid.querySelectorAll('.card');

    function layoutGridLanes() {{
        // Read CSS variables
        const computedStyle = window.getComputedStyle(grid);
        const rowHeight = parseInt(computedStyle.getPropertyValue('grid-auto-rows')) || 10;
        const gap = parseInt(computedStyle.getPropertyValue('--lane-gap')) || 24;

        items.forEach(item => {{
            // Reset span to get natural height
            item.style.gridRowEnd = 'auto';
            
            // Calculate height of the element
            const contentHeight = item.getBoundingClientRect().height;
            
            // Calculate how many rows it needs to span (+ lane gap for vertical spacing)
            const rowSpan = Math.ceil((contentHeight + gap) / rowHeight);
            
            // Apply the span to tuck it tightly into the lane
            item.style.gridRowEnd = `span ${{rowSpan}}`;
        }});
    }}

    // Initial layout
    layoutGridLanes();

    // Ensure layout holds when images load (if we had images) or viewport resizes
    window.addEventListener('resize', layoutGridLanes);
    
    // Optional: ResizeObserver for robust layout updates if inner content changes
    const resizeObserver = new ResizeObserver(() => {{
        layoutGridLanes();
    }});
    resizeObserver.observe(grid);
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
