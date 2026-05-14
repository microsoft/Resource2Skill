def create_component(
    output_dir: str,
    title_text: str = "Perfect Responsive Grid",
    body_text: str = "Drag the handle on the bottom-right of the dashed box to resize the container. Watch the grid mathematically reflow without a single media query.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_color = "#f5f5f5"
        text_muted = "#a3a3a3"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        border_color = "#e5e5e5"
        text_color = "#171717"
        text_muted = "#737373"

    # === CSS ===
    css = f"""/* Responsive Auto-Grid Component */
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
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    line-height: 1.5;
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Interactive Controls Panel */
.controls {{
    display: flex;
    gap: 2rem;
    padding: 1.25rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    flex-wrap: wrap;
}}

.control-group {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.control-group label {{
    font-weight: 500;
    font-size: 0.95rem;
}}

select, input[type="range"] {{
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem;
    border-radius: 4px;
    font-family: inherit;
    accent-color: var(--accent);
}}

/* Resizable Demo Container */
.resizer {{
    width: 100%;
    max-width: 100%;
    min-height: 400px;
    resize: horizontal;
    overflow: hidden;
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    background: var(--bg);
    position: relative;
}}

.resizer::after {{
    content: '↔ Drag to resize';
    position: absolute;
    bottom: 4px;
    right: 20px;
    font-size: 0.8rem;
    color: var(--text-muted);
    pointer-events: none;
}}

/* ========================================= */
/* THE CORE SKILL: THE RESPONSIVE AUTO-GRID  */
/* ========================================= */
.perfect-grid {{
    /* Variable for easy tweaking across different components */
    --grid-min-col-size: 260px;
    
    display: grid;
    gap: 1.25rem;
    
    /* 
      1. var(--grid-mode): Switches between auto-fill and auto-fit via JS for demo purposes.
      2. minmax(): Allows columns to grow (1fr) but not shrink below the minimum.
      3. min(size, 100%): The ultimate overflow protector for very small screens. 
    */
    grid-template-columns: repeat(
        var(--grid-mode, auto-fill), 
        minmax(min(var(--grid-min-col-size), 100%), 1fr)
    );
}}
/* ========================================= */

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 4px solid var(--accent);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}}

.tag {{
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--accent);
    border: 1px solid var(--accent);
}}

.card-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.4;
    flex-grow: 1;
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
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <div class="control-group">
                <label for="grid-mode">Grid Keyword:</label>
                <select id="grid-mode">
                    <option value="auto-fill">auto-fill (Best for filtering)</option>
                    <option value="auto-fit">auto-fit (Stretches few items)</option>
                </select>
            </div>
            <div class="control-group">
                <label for="item-count">Card Count: <span id="count-display">4</span></label>
                <input type="range" id="item-count" min="1" max="12" value="4">
            </div>
            <div class="control-group">
                <p style="font-size: 0.85rem; color: var(--text-muted); max-width: 300px; margin-left: auto;">
                    <em>Tip: Set cards to 2, then swap between auto-fill and auto-fit to see the difference.</em>
                </p>
            </div>
        </div>

        <div class="resizer">
            <div class="perfect-grid" id="grid-container">
                <!-- Cards injected via JS -->
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Logic to demonstrate grid capabilities
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid-container');
    const modeSelect = document.getElementById('grid-mode');
    const countSlider = document.getElementById('item-count');
    const countDisplay = document.getElementById('count-display');

    // Function to render dummy cards
    const renderCards = (count) => {{
        grid.innerHTML = '';
        for(let i = 0; i < count; i++) {{
            const card = document.createElement('div');
            card.className = 'card';
            
            // Randomize tag text slightly for realism
            const types = ['Component', 'Layout', 'Pattern'];
            const type = types[i % types.length];
            
            card.innerHTML = `
                <h3 class="card-title">Grid Element ${{i + 1}}</h3>
                <div class="tags">
                    <span class="tag">Responsive</span>
                    <span class="tag">${{type}}</span>
                </div>
                <p class="card-desc">This card automatically recalculates its width based on the container constraints, maintaining a minimum width without causing overflow.</p>
            `;
            grid.appendChild(card);
        }}
    }};

    // Change Grid Mode (auto-fill vs auto-fit)
    modeSelect.addEventListener('change', (e) => {{
        grid.style.setProperty('--grid-mode', e.target.value);
    }});

    // Change Number of Cards
    countSlider.addEventListener('input', (e) => {{
        const count = e.target.value;
        countDisplay.textContent = count;
        renderCards(count);
    }});

    // Initial Render
    renderCards(countSlider.value);
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
