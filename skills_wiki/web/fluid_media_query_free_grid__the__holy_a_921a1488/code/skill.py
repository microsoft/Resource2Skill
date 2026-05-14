def create_component(
    output_dir: str,
    title_text: str = "Get to know your mushrooms",
    body_text: str = "A container-aware grid layout demonstrating auto-fit vs auto-fill without a single media query.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4caf50",     # CSS hex color for the "edible" accent tag
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Media-Query-Free Grid pattern.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_color = "#f0f0f0"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#f4f4f9"
        surface_color = "#ffffff"
        border_color = "#dddddd"
        text_color = "#111111"
        text_muted = "#666666"

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
            
            <div class="controls">
                <div class="control-group">
                    <label for="mode-select">Grid Algorithm:</label>
                    <select id="mode-select">
                        <option value="auto-fit">auto-fit (stretches to fill row)</option>
                        <option value="auto-fill">auto-fill (leaves empty columns)</option>
                    </select>
                </div>
                <div class="control-group">
                    <button id="add-btn">Add Card</button>
                    <button id="remove-btn" class="btn-secondary">Remove Card</button>
                </div>
            </div>
        </header>

        <!-- The core grid component -->
        <main class="mushroom-grid" data-mode="auto-fit" id="grid-container">
            <!-- Cards will be populated by JS -->
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Font & Reset */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    
    /* THE MAGIC VARIABLE - Minimum width of a card */
    --grid-min-col-size: 275px; 
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 60ch;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}}

/* Interactive Controls UI */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    background: var(--surface);
    padding: 1rem 1.5rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    align-items: center;
}}

.control-group {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

select, button {{
    font-family: inherit;
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
    cursor: pointer;
    transition: background 0.2s;
}}

button {{
    background: var(--text);
    color: var(--bg);
    font-weight: 500;
    border: none;
}}

button:hover {{ opacity: 0.9; transform: translateY(-1px); }}
button:active {{ transform: translateY(0); }}

button.btn-secondary {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
}}
button.btn-secondary:hover {{ background: var(--border); }}


/* ==================================================
   CORE DESIGN PATTERN: The Fluid Grid
   ================================================== */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
      1. repeat(auto-fit, ...): Makes as many columns as will fit.
      2. minmax(..., 1fr): Columns stretch evenly up to 1fr.
      3. min(275px, 100%): Columns are 275px wide, UNLESS the container is 
                           smaller than 275px (e.g. mobile), then it caps at 100% width.
    */
    grid-template-columns: repeat(auto-fit, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

/* Switch to auto-fill mode */
.mushroom-grid[data-mode="auto-fill"] {{
    grid-template-columns: repeat(auto-fill, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}


/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}}

.card-header {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.card-header h3 {{
    font-size: 1.35rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: var(--border);
    color: var(--text);
}}

.tag-accent {{
    background: var(--accent);
    color: #ffffff;
}}

.desc {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text);
}}

/* Pushes the notes to the bottom, ensuring equal height alignment across the grid row */
.card-notes {{
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.4;
}}

@keyframes popIn {{
    from {{ opacity: 0; transform: scale(0.95) translateY(10px); }}
    to {{ opacity: 1; transform: scale(1) translateY(0); }}
}}
"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid-container');
    const modeSelect = document.getElementById('mode-select');
    const addBtn = document.getElementById('add-btn');
    const removeBtn = document.getElementById('remove-btn');

    // Mushroom Data Pool to simulate realistic cards
    const mushrooms = [
        {{ name: "Chanterelle", desc: "Golden-yellow, funnel-shaped mushroom with false gills.", tag: "edible", note: "Has toxic look-alikes - learn proper identification." }},
        {{ name: "Death Cap", desc: "Pale green to white cap with white gills.", tag: "toxic", note: "Extremely toxic - study for safety awareness." }},
        {{ name: "Oyster Mushroom", desc: "Fan-shaped caps growing in clusters on dead wood.", tag: "edible", note: "Great beginner mushroom, few look-alikes." }},
        {{ name: "Lion's Mane", desc: "White, shaggy appearance like a lion's mane.", tag: "edible", note: "No toxic look-alikes. Excellent flavor." }},
        {{ name: "Destroying Angel", desc: "Pure white mushroom with a sack-like base.", tag: "toxic", note: "Deadly toxic - avoid if foraging." }},
    ];

    let cardCount = 0;

    // Listen for grid algorithm toggle
    modeSelect.addEventListener('change', (e) => {{
        grid.setAttribute('data-mode', e.target.value);
    }});

    // Helper to generate a realistic card
    function createCard(data) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        const isEdible = data.tag === 'edible';
        const tagClass = isEdible ? 'tag-accent' : '';
        const tagStyle = !isEdible ? 'background: #f44336; color: #fff;' : '';

        card.innerHTML = `
            <div class="card-header">
                <h3>${{data.name}}</h3>
                <div class="tags">
                    <span class="tag ${{tagClass}}" style="${{tagStyle}}">${{data.tag}}</span>
                    <span class="tag">Summer</span>
                </div>
            </div>
            <p class="desc">${{data.desc}}</p>
            <div class="card-notes">
                <strong>Important notes:</strong> ${{data.note}}
            </div>
        `;
        return card;
    }}

    // Add card logic
    addBtn.addEventListener('click', () => {{
        const data = mushrooms[cardCount % mushrooms.length];
        grid.appendChild(createCard(data));
        cardCount++;
    }});

    // Remove card logic
    removeBtn.addEventListener('click', () => {{
        if (grid.lastElementChild) {{
            grid.removeChild(grid.lastElementChild);
            cardCount--;
        }}
    }});

    // Pre-populate with 3 cards so the difference between auto-fit and auto-fill 
    // is immediately obvious on wide desktop screens.
    for(let i = 0; i < 3; i++) {{
        addBtn.click();
    }}
}});
"""

    # Write files
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
