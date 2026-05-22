def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Masterclass",
    body_text: str = "Experience the power of auto-fit vs auto-fill without a single media query.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid CSS Grid Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user inputs
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#2a2a2a"
        text_color = "#e0e0e0"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "#64748b"

    # === CSS ===
    css = f"""/* Fluid CSS Grid Layout Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    
    /* The core variable governing the grid's wrapping behavior */
    --grid-min-col-size: 275px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.5rem;
}}

h1 {{
    font-size: 2.25rem;
    margin-bottom: 0.5rem;
}}

p.subtitle {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Interactive Controls */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    border: 1px solid var(--border);
}}

.filter-group {{
    display: flex;
    gap: 0.5rem;
}}

button {{
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
}}

button:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

button.active {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
}}

.toggle-group {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-muted);
    cursor: pointer;
}}

input[type="checkbox"] {{
    accent-color: var(--accent);
    width: 1rem;
    height: 1rem;
    cursor: pointer;
}}

/* =========================================
   THE MAGIC GRID STYLES
========================================= */
.fluid-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
       THE MAGIC FORMULA:
       1. repeat(auto-fit, ...): Make as many columns as fit. If items are few, stretch them.
       2. minmax(..., 1fr): Ensure columns are at least X size, but share remaining space equally.
       3. min(var(--size), 100%): The absolute minimum is the requested size, UNLESS the container 
          itself is smaller than that size, in which case default to 100% to prevent overflow.
    */
    grid-template-columns: repeat(auto-fit, minmax(min(var(--grid-min-col-size), 100%), 1fr));
    
    /* Smooth height transitions when filtering */
    transition: all 0.3s ease;
}}

/* When switched to auto-fill mode */
.fluid-grid.use-fill {{
    /* auto-fill creates empty grid tracks, preventing items from stretching to fill the row */
    grid-template-columns: repeat(auto-fill, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

/* Card Styles */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.3s ease, transform 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    border-color: var(--accent);
}}

.card.hidden {{
    display: none;
}}

.card-header h2 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.tag.primary {{
    background: rgba(74, 222, 128, 0.15); /* Accent color tint */
    color: var(--accent);
}}

.tag.secondary {{
    background: var(--bg);
    color: var(--text-muted);
    border: 1px solid var(--border);
}}

.card-body p {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-muted);
}}
"""

    # Generate some dummy content matching the video's context
    items = [
        {"title": "Chanterelle", "type": "spring", "desc": "Golden, funnel-shaped mushroom with false gills. highly sought after."},
        {"title": "Morel", "type": "spring", "desc": "Distinctive honeycomb-like cap structure. Must be cooked before eating."},
        {"title": "Chicken of the Woods", "type": "summer", "desc": "Bright orange bracket fungus with yellow edges. Tastes remarkable."},
        {"title": "Death Cap", "type": "summer", "desc": "Pale green to white cap with white gills. Extremely toxic, study for safety."},
        {"title": "Oyster Mushroom", "type": "fall", "desc": "Fan-shaped caps growing in overlapping clusters. Great for beginners."},
        {"title": "Lion's Mane", "type": "fall", "desc": "White, shaggy appearance like a lion's mane. Known for its look-alike safety."},
        {"title": "Destroying Angel", "type": "summer", "desc": "Pure white mushroom with a sack-like base. Deadly toxic."},
        {"title": "King Bolete", "type": "fall", "desc": "Large brown cap with thick stem. Learn to distinguish from similar species."}
    ]

    cards_html = ""
    for item in items:
        cards_html += f"""
        <article class="card" data-category="{item['type']}">
            <div class="card-header">
                <h2>{item['title']}</h2>
                <div class="tags">
                    <span class="tag primary">{item['type']}</span>
                    <span class="tag secondary">Fungi</span>
                </div>
            </div>
            <div class="card-body">
                <p>{item['desc']}</p>
            </div>
        </article>"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="app-container">
        <header>
            <h1>{safe_title}</h1>
            <p class="subtitle">{safe_body}</p>
        </header>

        <section class="controls">
            <div class="filter-group">
                <button class="active" data-filter="all">All Seasons</button>
                <button data-filter="spring">Spring</button>
                <button data-filter="summer">Summer</button>
                <button data-filter="fall">Fall</button>
            </div>
            <label class="toggle-group">
                <input type="checkbox" id="mode-toggle">
                Use <strong>auto-fill</strong> instead of <strong>auto-fit</strong>
            </label>
        </section>

        <section class="fluid-grid" id="grid">
            {cards_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const filterBtns = document.querySelectorAll('.filter-group button');
    const cards = document.querySelectorAll('.card');
    const toggleCheckbox = document.getElementById('mode-toggle');
    const grid = document.getElementById('grid');

    // Filter Logic
    filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            // Show/Hide cards
            cards.forEach(card => {{
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }});
    }});

    // Auto-fit vs Auto-fill layout switch logic
    toggleCheckbox.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            grid.classList.add('use-fill');
        }} else {{
            grid.classList.remove('use-fill');
        }}
    }});
}});
"""

    # Write files
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
