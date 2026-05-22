def create_component(
    output_dir: str,
    title_text: str = "Modern CSS Layout Strategy",
    body_text: str = "Grid for strict 1D structure. Flexbox for organic 2D wrapping.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Intentional 1D vs 2D Layouts visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "#1e293b"
        border_color = "#334155"
        sub_text = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        sub_text = "#475569"

    # === CSS ===
    css = f"""/* Intentional 1D vs 2D Layouts — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --sub-text: {sub_text};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    line-height: 1.5;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

header {{
    text-align: center;
    margin-bottom: 1rem;
}}

header h1 {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

header p {{
    color: var(--sub-text);
    font-size: 1.125rem;
}}

.section-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}}

.section-header h2 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.section-header p {{
    color: var(--sub-text);
    font-size: 0.9rem;
    margin-top: 0.25rem;
}}

.btn {{
    background: var(--surface);
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn:hover {{
    background: var(--accent);
    color: #ffffff;
}}

/* =========================================
   SKILL PATTERN 1: The Strict 1D Grid
   ========================================= */
.grid-layout {{
    display: grid;
    gap: 1.25rem;
}}

/* On larger screens, force auto-flow into equal width columns */
@media (min-width: 650px) {{
    .grid-layout {{
        grid-auto-flow: column;
        grid-auto-columns: 1fr;
    }}
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 4px solid var(--accent);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}}

.card h3 {{
    font-size: 1.125rem;
    margin-bottom: 0.5rem;
}}

.card p {{
    color: var(--sub-text);
    font-size: 0.9rem;
}}


/* =========================================
   SKILL PATTERN 2: The Intrinsic 2D Flexbox
   ========================================= */
.flex-layout {{
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap; /* The core wrapping behavior */
}}

.pill {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1.25rem;
    border-radius: 9999px; /* Pill shape */
    font-size: 0.9rem;
    font-weight: 500;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    white-space: nowrap;
    transition: border-color 0.2s ease;
}}

.pill:hover {{
    border-color: var(--accent);
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
    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Grid Demonstration -->
        <section>
            <div class="section-header">
                <div>
                    <h2>1D Layout (CSS Grid)</h2>
                    <p>Parent controls layout: grid-auto-flow: column; grid-auto-columns: 1fr;</p>
                </div>
                <button id="add-grid-btn" class="btn">+ Add Card</button>
            </div>
            <div class="grid-layout" id="grid-container">
                <div class="card">
                    <h3>Analytics</h3>
                    <p>Equal width columns automatically enforced by the parent container.</p>
                </div>
                <div class="card">
                    <h3>Performance</h3>
                    <p>No need for flex: 1 on children.</p>
                </div>
                <div class="card">
                    <h3>Security</h3>
                    <p>Adding more cards equally distributes the available space.</p>
                </div>
            </div>
        </section>

        <!-- Flexbox Demonstration -->
        <section>
            <div class="section-header">
                <div>
                    <h2>2D Layout (CSS Flexbox)</h2>
                    <p>Content controls sizing: flex-wrap: wrap;</p>
                </div>
                <button id="add-flex-btn" class="btn">+ Add Tag</button>
            </div>
            <div class="flex-layout" id="flex-container">
                <div class="pill">Responsive</div>
                <div class="pill">Fluid</div>
                <div class="pill">Dynamic Sizing</div>
                <div class="pill">CSS</div>
                <div class="pill">Intrinsic Length</div>
                <div class="pill">Wraps Naturally</div>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic demonstration of Grid vs Flexbox behaviors
document.addEventListener('DOMContentLoaded', () => {{
    
    // Grid Logic
    const gridContainer = document.getElementById('grid-container');
    const addGridBtn = document.getElementById('add-grid-btn');
    let gridCounter = 3;

    addGridBtn.addEventListener('click', () => {{
        gridCounter++;
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>Card ${{gridCounter}}</h3>
            <p>Automatically squeezed equally by the Grid auto-flow algorithm.</p>
        `;
        gridContainer.appendChild(card);
    }});

    // Flexbox Logic
    const flexContainer = document.getElementById('flex-container');
    const addFlexBtn = document.getElementById('add-flex-btn');
    const tags = ["Algorithm", "UI/UX", "Frontend", "Architecture", "Organic", "Scale", "Very Long Content Tag"];

    addFlexBtn.addEventListener('click', () => {{
        const word = tags[Math.floor(Math.random() * tags.length)];
        const pill = document.createElement('div');
        pill.className = 'pill';
        pill.textContent = word;
        flexContainer.appendChild(pill);
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
