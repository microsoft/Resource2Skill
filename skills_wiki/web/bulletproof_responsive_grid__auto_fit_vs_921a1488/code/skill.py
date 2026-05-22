def create_component(
    output_dir: str,
    title_text: str = "CSS Grid: Auto-Fit vs Auto-Fill",
    body_text: str = "Resize the container below to see how the grid calculates columns automatically. Toggle between modes to see how empty tracks are handled.",
    color_scheme: str = "dark",
    accent_color: str = "#3498db",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the bulletproof responsive grid pattern.
    Includes an interactive UI to resize the container and toggle between auto-fit and auto-fill.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f0f11"
        surface_color = "#1c1c1f"
        border_color = "#2d2d33"
        text_primary = "#f3f3f4"
        text_secondary = "#a0a0a8"
    else:
        bg_color = "#f4f4f5"
        surface_color = "#ffffff"
        border_color = "#e4e4e7"
        text_primary = "#18181b"
        text_secondary = "#71717a"

    css = f"""/* Bulletproof CSS Grid Component */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    
    /* The core grid variables */
    --grid-mode: auto-fit;
    --grid-min-col: 240px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
}}

.app-container {{
    max-width: {width_px}px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-secondary);
    line-height: 1.5;
}}

/* Control Panel */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    align-items: center;
    justify-content: space-between;
}}

.control-group {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

select, button {{
    background: var(--bg);
    color: var(--text-primary);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
}}

select:hover, button:hover {{
    border-color: var(--accent);
}}

button:active {{
    background: var(--border);
}}

/* Resizable Demo Container */
.demo-wrapper {{
    width: 100%;
    background: var(--bg);
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 1rem;
    /* This allows the user to drag and resize the container */
    resize: horizontal;
    overflow: hidden;
    min-width: 280px; /* Test the mobile bounds */
    max-width: 100%;
    min-height: {height_px}px;
}}

.demo-wrapper::after {{
    content: "↔ Drag corner to resize container";
    display: block;
    text-align: right;
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 1rem;
    pointer-events: none;
}}

/* THE MAGIC GRID */
.grid {{
    display: grid;
    gap: 1rem;
    /* 
      1. var(--grid-mode): Switches between auto-fit and auto-fill
      2. min(var(--grid-min-col), 100%): Prevents overflow if container < 240px
      3. 1fr: Stretches to fill remaining space
    */
    grid-template-columns: repeat(
        var(--grid-mode), 
        minmax(min(var(--grid-min-col), 100%), 1fr)
    );
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s;
    /* View Transition Name for smooth DOM addition/removal (modern browsers) */
    view-transition-name: card-var; 
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: var(--border);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}}

.tag-season {{ background: rgba(52, 152, 219, 0.15); color: #3498db; }}
.tag-edible {{ background: rgba(46, 204, 113, 0.15); color: #2ecc71; }}
.tag-toxic {{ background: rgba(231, 76, 60, 0.15); color: #e74c3c; }}

.card-desc {{
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.5;
    flex-grow: 1;
}}
"""

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
    <div class="app-container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="controls">
            <div class="control-group">
                <label for="mode-select" style="font-size: 0.9rem; font-weight: 600;">Keyword:</label>
                <select id="mode-select">
                    <option value="auto-fit">auto-fit (Stretch items to fill empty tracks)</option>
                    <option value="auto-fill">auto-fill (Leave empty tracks at min-width)</option>
                </select>
            </div>
            <div class="control-group">
                <button id="btn-remove">- Remove Card</button>
                <span id="card-count" style="font-weight: 600; font-variant-numeric: tabular-nums;">4 Cards</span>
                <button id="btn-add">+ Add Card</button>
            </div>
        </div>

        <div class="demo-wrapper">
            <div class="grid" id="grid">
                <!-- Cards will be injected by JS -->
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const modeSelect = document.getElementById('mode-select');
    const btnAdd = document.getElementById('btn-add');
    const btnRemove = document.getElementById('btn-remove');
    const cardCountLabel = document.getElementById('card-count');

    const mushrooms = [
        { name: "Chanterelle", season: "Summer", type: "edible", desc: "Golden-yellow, funnel-shaped mushroom with false gills. Avoid if growing on specific trees." },
        { name: "Morel", season: "Spring", type: "edible", desc: "Distinctive honeycomb-like cap structure. Must be cooked before eating." },
        { name: "Death Cap", season: "Fall", type: "toxic", desc: "Pale green to white cap with white gills. Extremely toxic - study for safety awareness." },
        { name: "Lion's Mane", season: "Fall", type: "edible", desc: "White, shaggy appearance like a lion's mane. Great beginner mushroom, no toxic look-alikes." },
        { name: "Chicken of the Woods", season: "Summer", type: "edible", desc: "Bright orange bracket fungus with yellow edges. Tastes surprisingly like chicken." },
        { name: "Destroying Angel", season: "Summer", type: "toxic", desc: "Pure white mushroom with a sack-like base. Deadly toxic - avoid at all costs." }
    ];

    let currentCards = 0;

    function createCardHTML(data) {
        const tagClass = data.type === 'edible' ? 'tag-edible' : 'tag-toxic';
        return `
            <div class="card-header">
                <h3 class="card-title">${data.name}</h3>
            </div>
            <div class="tags">
                <span class="tag tag-season">${data.season}</span>
                <span class="tag ${tagClass}">${data.type}</span>
            </div>
            <p class="card-desc">${data.desc}</p>
        `;
    }

    function addCard() {
        if (currentCards >= mushrooms.length * 2) return; // Cap for demo
        
        const data = mushrooms[currentCards % mushrooms.length];
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = createCardHTML(data);
        
        // Use View Transitions if available for smooth insertion
        if (document.startViewTransition) {
            document.startViewTransition(() => grid.appendChild(card));
        } else {
            grid.appendChild(card);
        }
        
        currentCards++;
        updateCount();
    }

    function removeCard() {
        if (currentCards <= 1) return; // Keep at least 1
        
        const lastCard = grid.lastElementChild;
        
        if (document.startViewTransition) {
            document.startViewTransition(() => grid.removeChild(lastCard));
        } else {
            grid.removeChild(lastCard);
        }
        
        currentCards--;
        updateCount();
    }

    function updateCount() {
        cardCountLabel.textContent = `${currentCards} Card${currentCards !== 1 ? 's' : ''}`;
    }

    // Change Grid Mode (auto-fit vs auto-fill)
    modeSelect.addEventListener('change', (e) => {
        grid.style.setProperty('--grid-mode', e.target.value);
    });

    btnAdd.addEventListener('click', addCard);
    btnRemove.addEventListener('click', removeCard);

    // Initialize with 4 cards to show 1 empty slot on a wide screen with auto-fill
    for(let i = 0; i < 4; i++) {
        addCard();
    }
});
"""

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
