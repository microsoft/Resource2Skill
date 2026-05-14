def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Resize the window to see the grid wrap without media queries. Use the controls to test auto-fill vs auto-fit.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80", 
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Responsive CSS Grid technique.
    Demonstrates the difference between auto-fill and auto-fit using minmax() and min().
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        surface_hover = "#2a2a2a"
        text_primary = "#ffffff"
        text_secondary = "#a1a1aa"
        border_color = "#3f3f46"
    else:
        bg_color = "#f4f4f5"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        text_primary = "#18181b"
        text_secondary = "#52525b"
        border_color = "#e4e4e7"

    # === CSS ===
    css = f"""/* Fluid Responsive Grid Component */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --surface-hover: {surface_hover};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --accent-color: {accent_color};
    
    /* Core Grid Variables */
    --grid-min-size: 275px;
    --grid-mode: auto-fill; /* Can toggle to auto-fit via JS */
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
}}

header {{
    margin-bottom: 2rem;
    text-align: center;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

p.subtitle {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
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
    border-radius: 0.75rem;
    justify-content: center;
    align-items: center;
}}

button, select {{
    background-color: var(--bg-color);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.9rem;
    font-family: inherit;
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
}}

button:hover, select:hover {{
    border-color: var(--accent-color);
    background-color: var(--surface-hover);
}}

/* --- THE MAGIC GRID --- */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
       THE CORE TECHNIQUE:
       1. repeat(var(--grid-mode), ...): Uses auto-fill or auto-fit.
       2. minmax(..., 1fr): Cards stretch to fill space (1fr) but never shrink below the minimum.
       3. min(var(--grid-min-size), 100%): The absolute minimum is 275px, UNLESS the screen is narrower than 275px (e.g. 200px), then it uses 100% of the screen. Prevents horizontal overflow.
    */
    grid-template-columns: repeat(
        var(--grid-mode), 
        minmax(min(var(--grid-min-size), 100%), 1fr)
    );
}}

/* --- Card Styles --- */
.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 0.75rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
    /* Optional: subtle animation when cards mount */
    animation: fadeIn 0.3s ease-out;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    border-color: var(--accent-color);
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
    background-color: var(--bg-color);
    color: var(--accent-color);
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    border: 1px solid var(--border-color);
}}

.card-desc {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1;
}}

.important-note {{
    background-color: rgba(255, 255, 255, 0.03);
    padding: 0.75rem;
    border-radius: 0.5rem;
    border-left: 3px solid var(--accent-color);
    font-size: 0.85rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <header>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <div class="controls">
            <button id="add-btn">Add Card</button>
            <button id="remove-btn">Remove Card</button>
            
            <div style="width: 1px; height: 24px; background: var(--border-color); margin: 0 0.5rem;"></div>
            
            <label for="mode-select" style="font-size: 0.9rem; font-weight: 600;">Grid Behavior:</label>
            <select id="mode-select">
                <option value="auto-fill">auto-fill (Leaves blank space, cards stay natural size)</option>
                <option value="auto-fit">auto-fit (Collapses blank space, stretches cards to fill)</option>
            </select>
        </div>

        <!-- The Grid Container -->
        <div class="mushroom-grid" id="grid">
            <!-- Initial content generated by JS -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    const modeSelect = document.getElementById('mode-select');
    const addBtn = document.getElementById('add-btn');
    const removeBtn = document.getElementById('remove-btn');

    let cardCount = 0;

    // Dummy data for card generation
    const contentData = [
        {{ title: "Chanterelle", badge: "Edible", desc: "Golden-yellow, funnel-shaped mushroom with false gills.", note: "Has toxic look-alikes - learn proper identification." }},
        {{ title: "Morel", badge: "Spring", desc: "Distinctive honeycomb-like cap structure.", note: "Must be cooked before eating." }},
        {{ title: "Death Cap", badge: "Toxic", desc: "Pale green to white cap with white gills.", note: "Extremely toxic - study for safety awareness." }},
        {{ title: "Lion's Mane", badge: "Edible", desc: "White, shaggy appearance like a lion's mane.", note: "No toxic look-alikes." }},
        {{ title: "Chicken of the Woods", badge: "Edible", desc: "Bright orange bracket fungus with yellow edges.", note: "Avoid if growing on certain tree species." }}
    ];

    // Function to toggle auto-fill vs auto-fit via CSS Variable
    modeSelect.addEventListener('change', (e) => {{
        grid.style.setProperty('--grid-mode', e.target.value);
    }});

    // Function to create a card element
    function createCard() {{
        const data = contentData[cardCount % contentData.length];
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-header">
                <div class="card-title">${{data.title}} #${{cardCount + 1}}</div>
                <div class="badge">${{data.badge}}</div>
            </div>
            <div class="card-desc">${{data.desc}}</div>
            <div class="important-note">
                <strong>Important note:</strong> ${{data.note}}
            </div>
        `;
        return card;
    }}

    // Add card interaction
    addBtn.addEventListener('click', () => {{
        grid.appendChild(createCard());
        cardCount++;
    }});

    // Remove card interaction
    removeBtn.addEventListener('click', () => {{
        if (grid.lastChild) {{
            grid.removeChild(grid.lastChild);
            cardCount--;
        }}
    }});

    // Initialize with 4 cards to show off the grid layout
    for(let i=0; i<4; i++) {{
        addBtn.click();
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
