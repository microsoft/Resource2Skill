def create_component(
    output_dir: str,
    title_text: str = "Layout Engines: Flexbox vs Grid",
    body_text: str = "Notice how both methods keep the cards equal in height and push the buttons to the bottom, regardless of content length.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     # Flexbox Accent (Cyan)
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox vs Grid 3-Card layout comparison.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#0f0f13" # Deep dark purple/black from video
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_hover = "rgba(255, 255, 255, 0.06)"
        grid_accent = "#ff4bfb" # Pink/Magenta for grid to match video
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        text_muted = "rgba(0, 0, 0, 0.6)"
        surface_color = "#ffffff"
        surface_hover = "#fdfdfd"
        grid_accent = "#d900c7" 

    flex_accent = accent_color

    css = f"""/* Robust 3-Card Comparison Layout */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --flex-accent: {flex_accent};
    --grid-accent: {grid_accent};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1.5;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    /* Auto height to allow content to dictate space, but respect min boundaries */
    min-height: calc(var(--height) * 0.8); 
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 1.5rem auto;
}}

.toggle-btn {{
    background: transparent;
    border: 1px solid var(--text-muted);
    color: var(--text);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.9rem;
    transition: all 0.2s;
}}

.toggle-btn:hover {{
    background: var(--surface);
    border-color: var(--text);
}}

.section-title {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
}}

.flex-title {{ color: var(--flex-accent); }}
.grid-title {{ color: var(--grid-accent); }}

/* Shared Card Styles */
.card {{
    background: var(--surface);
    padding: 2rem;
    border-radius: 12px;
    border-top: 4px solid;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, background 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    background: var(--surface-hover);
}}

.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}}

.btn {{
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 0.75rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s;
}}

.btn:hover {{ opacity: 0.8; }}

/* --- CORE SKILL: FLEXBOX IMPLEMENTATION --- */
.flex-container {{
    display: flex;
    gap: 1.5rem;
}}

.flex-card {{
    border-color: var(--flex-accent);
    /* 1. Ensure cards share equal width */
    flex: 1; 
    /* 2. Make the card itself a flex container */
    display: flex;
    flex-direction: column;
}}

.flex-card p {{
    /* 3. Tell the paragraph to absorb all empty vertical space */
    flex-grow: 1;
}}

.flex-card .btn {{
    background-color: var(--flex-accent);
    color: #000;
}}

/* --- CORE SKILL: GRID IMPLEMENTATION --- */
.grid-container {{
    display: grid;
    /* 1. Define equal width columns */
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}}

.grid-card {{
    border-color: var(--grid-accent);
    /* 2. Make the card a grid container */
    display: grid;
    /* 3. Define rows: Auto height for Title, 1fr (remaining space) for Text, Auto height for Button */
    grid-template-rows: auto 1fr auto;
}}

.grid-card p {{
    /* Margin reset required because grid handles the spacing internally */
    margin-bottom: 1.5rem; 
}}

.grid-card .btn {{
    background-color: var(--grid-accent);
    color: #fff;
}}

/* Structural Debugging Classes */
body.debug-mode .card {{
    outline: 2px dashed rgba(255,255,255,0.3);
    outline-offset: -2px;
}}
body.debug-mode .card > * {{
    outline: 1px solid rgba(255, 0, 0, 0.5);
    background: rgba(255, 0, 0, 0.05);
}}

/* Responsive */
@media (max-width: 900px) {{
    .flex-container {{ flex-direction: column; }}
    .grid-container {{ grid-template-columns: 1fr; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <button class="toggle-btn" id="debugToggle">Toggle Structural View</button>
        </header>

        <!-- FLEXBOX SECTION -->
        <section>
            <h2 class="section-title flex-title">Flexbox Layout</h2>
            <div class="flex-container">
                <div class="card flex-card">
                    <h3>Card 1</h3>
                    <p>Short description. Just a few words here.</p>
                    <a href="#" class="btn">Button</a>
                </div>
                <div class="card flex-card">
                    <h3>Card 2</h3>
                    <p>Medium description. This paragraph contains slightly more text to demonstrate how the layout handles uneven content across the siblings.</p>
                    <a href="#" class="btn">Button</a>
                </div>
                <div class="card flex-card">
                    <h3>Card 3</h3>
                    <p>Long description. This is the longest paragraph in the row. Because this card expands the height of the entire row, the layouts of the other two cards must intelligently distribute their empty space so their buttons align perfectly at the bottom with this one.</p>
                    <a href="#" class="btn">Button</a>
                </div>
            </div>
        </section>

        <!-- GRID SECTION -->
        <section>
            <h2 class="section-title grid-title">Grid Layout</h2>
            <div class="grid-container">
                <div class="card grid-card">
                    <h3>Card 1</h3>
                    <p>Short description. Just a few words here.</p>
                    <a href="#" class="btn">Button</a>
                </div>
                <div class="card grid-card">
                    <h3>Card 2</h3>
                    <p>Medium description. This paragraph contains slightly more text to demonstrate how the layout handles uneven content across the siblings.</p>
                    <a href="#" class="btn">Button</a>
                </div>
                <div class="card grid-card">
                    <h3>Card 3</h3>
                    <p>Long description. This is the longest paragraph in the row. Because this card expands the height of the entire row, the layouts of the other two cards must intelligently distribute their empty space so their buttons align perfectly at the bottom with this one.</p>
                    <a href="#" class="btn">Button</a>
                </div>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Toggle structural debug view to visualize how Flexbox and Grid calculate space
document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.getElementById('debugToggle');
    
    toggleBtn.addEventListener('click', () => {{
        document.body.classList.toggle('debug-mode');
        
        if (document.body.classList.contains('debug-mode')) {{
            toggleBtn.textContent = "Disable Structural View";
            toggleBtn.style.background = "rgba(255,0,0,0.2)";
            toggleBtn.style.borderColor = "red";
        }} else {{
            toggleBtn.textContent = "Toggle Structural View";
            toggleBtn.style.background = "transparent";
            toggleBtn.style.borderColor = "var(--text-muted)";
        }}
    }});
}});
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
