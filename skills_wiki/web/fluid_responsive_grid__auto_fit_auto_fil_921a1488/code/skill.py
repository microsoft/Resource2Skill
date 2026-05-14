def create_component(
    output_dir: str,
    title_text: str = "Fluid Responsive Grid",
    body_text: str = "Resize the browser or container to see the grid adapt automatically. Add/remove cards to see the difference between auto-fit and auto-fill.",
    color_scheme: str = "dark",        
    accent_color: str = "#10b981",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Responsive Grid technique.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
        card_border = "#334155"
        control_bg = "#0b1120"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        card_bg = "#ffffff"
        card_border = "#cbd5e1"
        control_bg = "#e2e8f0"

    css = f"""/* Fluid Responsive Grid */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent-color: {accent_color};
    --control-bg: {control_bg};
    --grid-min-col-size: 250px;
    --grid-mode: auto-fit; /* Toggled via JS to demonstrate auto-fill */
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
}}

header {{
    text-align: center;
    max-width: 800px;
    margin-bottom: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: var(--accent-color);
}}

p {{
    opacity: 0.8;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}}

.controls {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    background: var(--control-bg);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--card-border);
    flex-wrap: wrap;
}}

button {{
    background: var(--card-bg);
    color: var(--text-color);
    border: 1px solid var(--card-border);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
}}

button:hover {{
    border-color: var(--accent-color);
    color: var(--accent-color);
}}

label {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-weight: 500;
}}

/* === Resizable Demo Container === */
.resize-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px // 2}px;
    resize: horizontal;
    overflow: hidden;
    border: 2px dashed var(--card-border);
    border-radius: 12px;
    padding: 2rem;
    background: var(--control-bg);
    margin: 0 auto;
}}

/* === The Magic Grid CSS === */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    
    /* 
     * Core Technique:
     * 1. repeat(auto-fit, ...) -> create as many columns as possible.
     * 2. minmax(..., 1fr)      -> columns must be at least X, but can grow to fill space (1fr).
     * 3. min(250px, 100%)      -> prevents overflow if container is narrower than 250px.
     */
    grid-template-columns: repeat(
        var(--grid-mode), 
        minmax(min(var(--grid-min-col-size), 100%), 1fr)
    );
}}

/* Card Styling */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-color);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}}

.card-tag {{
    align-self: flex-start;
    background: var(--accent-color);
    color: #fff;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}}

.card-title {{
    font-size: 1.25rem;
    margin-top: 0.5rem;
}}

.card-desc {{
    font-size: 0.9rem;
    opacity: 0.7;
    line-height: 1.5;
}}
"""

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
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <div class="controls">
            <label>
                <input type="radio" name="gridMode" value="auto-fit" checked> auto-fit (stretches)
            </label>
            <label>
                <input type="radio" name="gridMode" value="auto-fill"> auto-fill (leaves gaps)
            </label>
            <button id="add-btn">+ Add Card</button>
            <button id="remove-btn">- Remove Card</button>
        </div>
    </header>

    <div class="resize-container" title="Drag the bottom right corner to resize horizontally">
        <div class="mushroom-grid" id="grid">
            <!-- Cards generated by JS -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Fluid Responsive Grid Interactive Script
document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const addBtn = document.getElementById('add-btn');
    const removeBtn = document.getElementById('remove-btn');
    const radios = document.querySelectorAll('input[name="gridMode"]');
    
    let cardCount = 3; // Start with few cards to demonstrate fit vs fill easily

    const createCard = (id) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <span class="card-tag">Item ${id}</span>
            <h3 class="card-title">Responsive Item</h3>
            <p class="card-desc">This card will adapt its width fluidly based on the grid constraints.</p>
        `;
        return card;
    };

    const renderCards = () => {
        grid.innerHTML = '';
        for (let i = 1; i <= cardCount; i++) {
            grid.appendChild(createCard(i));
        }
    };

    // Toggle between auto-fit and auto-fill by changing CSS custom property
    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            document.documentElement.style.setProperty('--grid-mode', e.target.value);
        });
    });

    addBtn.addEventListener('click', () => {
        cardCount++;
        renderCards();
    });

    removeBtn.addEventListener('click', () => {
        if (cardCount > 1) {
            cardCount--;
            renderCards();
        }
    });

    // Initial render
    renderCards();
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
