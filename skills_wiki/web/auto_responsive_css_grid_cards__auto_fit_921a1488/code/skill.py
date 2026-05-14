def create_component(
    output_dir: str,
    title_text: str = "Responsive Card Grid",
    body_text: str = "Resize the browser to see the grid reflow automatically. Toggle between auto-fit and auto-fill to observe how empty space is handled when there are fewer items.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Grid auto-fit/minmax responsive layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        surface_hover = "#2a2a2a"
        text_primary = "#f5f5f5"
        text_secondary = "#a0a0a0"
        border_color = "#333333"
    else:
        bg_color = "#f4f7f6"
        surface_color = "#ffffff"
        surface_hover = "#f9f9f9"
        text_primary = "#2c3e50"
        text_secondary = "#7f8c8d"
        border_color = "#e0e0e0"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --surface-hover: {surface_hover};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --border-color: {border_color};
    
    --card-min-width: 280px; /* The threshold for reflowing */
    --grid-gap: 1.5rem;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
}}

header {{
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

p.desc {{
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 800px;
}}

/* --- Control Panel --- */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    align-items: center;
}}

.control-group {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

button {{
    background-color: var(--surface-hover);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
}}

button:hover {{
    background-color: var(--border-color);
}}

button.primary {{
    background-color: var(--accent-color);
    color: #fff;
    border: none;
}}

button.primary:hover {{
    filter: brightness(1.1);
}}

.radio-group {{
    display: flex;
    background: var(--bg-color);
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}}

.radio-group label {{
    padding: 0.5rem 1rem;
    cursor: pointer;
    background: transparent;
    transition: background 0.2s;
    font-size: 0.9rem;
    font-weight: 600;
}}

.radio-group input[type="radio"] {{
    display: none;
}}

.radio-group label:has(input:checked) {{
    background: var(--accent-color);
    color: white;
}}


/* --- THE CORE GRID MAGIC --- */
.auto-grid {{
    display: grid;
    gap: var(--grid-gap);
    /* Default to auto-fit. 
       min(var(--card-min-width), 100%) prevents horizontal overflow on tiny screens 
    */
    grid-template-columns: repeat(auto-fit, minmax(min(var(--card-min-width), 100%), 1fr));
    
    /* Animation for layout changes */
    transition: all 0.3s ease;
}}

/* Variant demonstrating auto-fill */
.auto-grid.use-auto-fill {{
    grid-template-columns: repeat(auto-fill, minmax(min(var(--card-min-width), 100%), 1fr));
}}


/* --- Card Styling --- */
.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeIn 0.4s ease-out forwards;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.badge {{
    background-color: rgba(76, 175, 80, 0.15); /* Tinted accent */
    color: var(--accent-color);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.card-body {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1; /* Pushes footer down */
}}

.card-footer {{
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-primary);
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: scale(0.95); }}
    to {{ opacity: 1; transform: scale(1); }}
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
        <header>
            <h1>{title_text}</h1>
            <p class="desc">{body_text}</p>
        </header>

        <section class="controls">
            <div class="control-group">
                <span style="font-weight: 600; font-size: 0.9rem;">Grid Mode:</span>
                <div class="radio-group">
                    <label>
                        <input type="radio" name="grid-mode" value="auto-fit" checked> auto-fit
                    </label>
                    <label>
                        <input type="radio" name="grid-mode" value="auto-fill"> auto-fill
                    </label>
                </div>
            </div>
            
            <div class="control-group" style="margin-left: auto;">
                <button id="btn-remove">Remove Card</button>
                <button id="btn-add" class="primary">Add Card</button>
            </div>
        </section>

        <!-- The Responsive Grid -->
        <main class="auto-grid" id="main-grid">
            <!-- Cards will be injected by JS -->
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('main-grid');
    const btnAdd = document.getElementById('btn-add');
    const btnRemove = document.getElementById('btn-remove');
    const modeRadios = document.querySelectorAll('input[name="grid-mode"]');
    
    let cardCount = 0;

    // Sample data
    const itemNames = ["Chanterelle", "Morel", "Chicken of the Woods", "Death Cap", "Oyster Mushroom", "Lion's Mane"];
    const tags = ["Edible", "Spring", "Summer", "Toxic", "Fall", "Medicinal"];

    function createCard() {{
        cardCount++;
        const card = document.createElement('article');
        card.className = 'card';
        
        const title = itemNames[cardCount % itemNames.length];
        const tag = tags[cardCount % tags.length];
        const tagColor = tag === "Toxic" ? "#f44336" : "var(--accent-color)";
        const tagBg = tag === "Toxic" ? "rgba(244, 67, 54, 0.15)" : "";

        card.innerHTML = `
            <div class="card-header">
                <h2 class="card-title">${{title}} ${{cardCount}}</h2>
                <span class="badge" style="color: ${{tagColor}}; background-color: ${{tagBg || ''}}">${{tag}}</span>
            </div>
            <div class="card-body">
                <p>This is a dynamically generated card demonstrating the fluid CSS grid. Notice how it fits within the established minmax boundaries.</p>
            </div>
            <div class="card-footer">
                Important notes: Reference item #${{Math.floor(Math.random() * 1000)}}
            </div>
        `;
        return card;
    }}

    // Initial load: Add 4 cards (enough to show wrapping but leave space on wide screens)
    for(let i=0; i<4; i++) {{
        grid.appendChild(createCard());
    }}

    // Add card interaction
    btnAdd.addEventListener('click', () => {{
        grid.appendChild(createCard());
    }});

    // Remove card interaction
    btnRemove.addEventListener('click', () => {{
        if (grid.lastElementChild) {{
            grid.removeChild(grid.lastElementChild);
        }}
    }});

    // Toggle between auto-fit and auto-fill
    modeRadios.forEach(radio => {{
        radio.addEventListener('change', (e) => {{
            if (e.target.value === 'auto-fill') {{
                grid.classList.add('use-auto-fill');
            }} else {{
                grid.classList.remove('use-auto-fill');
            }}
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
