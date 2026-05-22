def create_component(
    output_dir: str,
    title_text: str = "Mushroom Foraging Guide",
    body_text: str = "Filter the cards below and toggle the layout mode to see how CSS Grid handles dynamic content.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive Fluid Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        card_bg = "#1e1e1e"
        text_color = "#e0e0e0"
        text_muted = "#a0a0a0"
        border_color = "#333333"
    else:
        bg_color = "#f4f7f6"
        card_bg = "#ffffff"
        text_color = "#222222"
        text_muted = "#666666"
        border_color = "#e0e0e0"

    # === CSS ===
    css = f"""/* Auto-Responsive Fluid Grid */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --border-color: {border_color};
    
    /* Core Grid Variable */
    --grid-min-col-size: 280px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.5;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    /* Optional constraints based on requested sizing */
    min-height: {height_px}px; 
}}

.header {{
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}}

/* Controls UI */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
    justify-content: space-between;
}}

.filter-group, .toggle-group {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.btn {{
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.btn:hover {{
    border-color: var(--accent-color);
}}

.btn.active {{
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: #fff;
}}

/* =========================================
   CORE SKILL: THE FLUID GRID 
   ========================================= */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    /* Defaulting to auto-fit */
    grid-template-columns: repeat(
        auto-fit, 
        minmax(min(100%, var(--grid-min-col-size)), 1fr)
    );
    transition: all 0.3s ease;
}}

/* Modifier class for the auto-fill behavior */
.mushroom-grid.use-auto-fill {{
    grid-template-columns: repeat(
        auto-fill, 
        minmax(min(100%, var(--grid-min-col-size)), 1fr)
    );
}}
/* ========================================= */

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}}

.card.hidden {{
    display: none;
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}}

.tag {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}}

.tag.edible {{ background: rgba(76, 175, 80, 0.15); color: #4caf50; }}
.tag.toxic {{ background: rgba(244, 67, 54, 0.15); color: #f44336; }}
.tag.season {{ background: rgba(33, 150, 243, 0.15); color: #2196f3; }}

.card-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    flex-grow: 1;
}}

.card-footer {{
    background: rgba(0, 0, 0, 0.05);
    padding: 0.75rem;
    border-radius: 6px;
    font-size: 0.85rem;
    border-left: 3px solid var(--accent-color);
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
    <div class="app-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <div class="filter-group">
                <strong>Filter:</strong>
                <button class="btn active" data-filter="all">All</button>
                <button class="btn" data-filter="spring">Spring Only</button>
                <button class="btn" data-filter="edible">Edible</button>
            </div>
            <div class="toggle-group">
                <strong>Grid Mode:</strong>
                <button class="btn active" id="btn-fit">auto-fit</button>
                <button class="btn" id="btn-fill">auto-fill</button>
            </div>
        </div>

        <!-- The Responsive Grid -->
        <div class="mushroom-grid" id="main-grid">
            
            <div class="card" data-category="edible summer fall">
                <div class="card-header">
                    <h2 class="card-title">Chanterelle</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Golden-yellow, funnel-shaped mushroom with false gills. Has a fruity odor like apricots.</p>
                <div class="card-footer">
                    <strong>Important:</strong> Has toxic look-alikes.
                </div>
            </div>

            <div class="card" data-category="edible spring">
                <div class="card-header">
                    <h2 class="card-title">Morel</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Distinctive honeycomb-like cap structure. Found in wooded areas in early spring.</p>
                <div class="card-footer">
                    <strong>Important:</strong> Must be cooked before eating.
                </div>
            </div>

            <div class="card" data-category="toxic summer fall">
                <div class="card-header">
                    <h2 class="card-title">Death Cap</h2>
                </div>
                <div class="tags">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Pale green to white cap with white gills. Responsible for the majority of fatal mushroom poisonings.</p>
                <div class="card-footer" style="border-color: #f44336;">
                    <strong>Important:</strong> Extremely toxic.
                </div>
            </div>

            <div class="card" data-category="edible fall">
                <div class="card-header">
                    <h2 class="card-title">Lion's Mane</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Fall</span>
                </div>
                <p class="card-desc">White, shaggy appearance like a lion's mane. Known for its lobster-like taste.</p>
                <div class="card-footer">
                    <strong>Important:</strong> No toxic look-alikes.
                </div>
            </div>

            <div class="card" data-category="toxic spring">
                <div class="card-header">
                    <h2 class="card-title">False Morel</h2>
                </div>
                <div class="tags">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Brain-like, reddish-brown cap with irregular shape. Contains the toxin gyromitrin.</p>
                <div class="card-footer" style="border-color: #f44336;">
                    <strong>Important:</strong> Highly toxic.
                </div>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive logic to demonstrate fit vs fill
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('main-grid');
    const filterBtns = document.querySelectorAll('.filter-group .btn');
    const btnFit = document.getElementById('btn-fit');
    const btnFill = document.getElementById('btn-fill');
    const cards = document.querySelectorAll('.card');

    // Filtering Logic
    filterBtns.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');

            const filter = e.target.getAttribute('data-filter');

            cards.forEach(card => {{
                if (filter === 'all') {{
                    card.classList.remove('hidden');
                }} else {{
                    const categories = card.getAttribute('data-category');
                    if (categories.includes(filter)) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }}
            }});
        }});
    }});

    // Grid Layout Toggle Logic (auto-fit vs auto-fill)
    btnFit.addEventListener('click', () => {{
        btnFit.classList.add('active');
        btnFill.classList.remove('active');
        grid.classList.remove('use-auto-fill');
    }});

    btnFill.addEventListener('click', () => {{
        btnFill.classList.add('active');
        btnFit.classList.remove('active');
        grid.classList.add('use-auto-fill');
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
