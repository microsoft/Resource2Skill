def create_component(
    output_dir: str,
    title_text: str = "Flexbox Engine Demo",
    body_text: str = "Interact with the controls to see how Flexbox properties dynamically alter layout, alignment, and space distribution.",
    color_scheme: str = "dark",        
    accent_color: str = "#ec4899",     
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create an interactive web component reproducing the Flexbox Layout Engine.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        surface_color = "#1e293b"     # Slate 800
        card_bg = "#334155"           # Slate 700
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"          # Slate 50
        text_color = "#0f172a"        # Slate 900
        surface_color = "#ffffff"     # White
        card_bg = "#f1f5f9"           # Slate 100
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Flexbox Engine Demo — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --card-bg: {card_bg};
    --border: {border_color};
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
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header-section {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text);
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

/* Controls UI */
.controls-panel {{
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    align-items: center;
}}

button {{
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-weight: 500;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--card-bg);
    border-color: var(--accent);
}}

button.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}}

/* THE FLEXBOX CONTAINER */
.flex-sandbox {{
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    min-height: 400px;
    
    /* Default Flex Properties */
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: stretch;
    gap: 1.5rem;
    
    transition: all 0.4s ease;
}}

/* THE FLEX ITEMS */
.flex-item {{
    background: var(--card-bg);
    border-top: 4px solid var(--accent);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease, flex-grow 0.3s ease;
    
    /* Intrinsic sizing: Grow to share space, shrink if squeezed, base size 200px */
    flex: 1 1 200px;
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 120px;
}}

.flex-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}}

.item-title {{
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}}

.item-code {{
    font-family: monospace;
    font-size: 0.85rem;
    opacity: 0.7;
    background: var(--bg);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
    width: fit-content;
}}

/* Demonstrating Item-Specific Properties */
.flex-item.featured {{
    flex-grow: 2; /* Takes up twice as much available space */
    border-top-color: #10b981; /* Emerald green to distinguish */
}}
.flex-item.featured .item-code {{ color: #10b981; }}

.flex-item.align-diff {{
    align-self: center; /* Overrides container's align-items */
    border-top-color: #f59e0b; /* Amber to distinguish */
}}
.flex-item.align-diff .item-code {{ color: #f59e0b; }}
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
        <header class="header-section">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <nav class="controls-panel">
            <strong>Direction:</strong>
            <button data-prop="flexDirection" data-val="row" class="active">row</button>
            <button data-prop="flexDirection" data-val="column">column</button>
            
            <strong style="margin-left: 1rem;">Justify:</strong>
            <button data-prop="justifyContent" data-val="flex-start" class="active">start</button>
            <button data-prop="justifyContent" data-val="center">center</button>
            <button data-prop="justifyContent" data-val="space-between">space-between</button>
            <button data-prop="justifyContent" data-val="space-evenly">space-evenly</button>
        </nav>

        <main class="flex-sandbox" id="sandbox">
            <div class="flex-item">
                <div class="item-title">Item 1</div>
                <div class="item-code">flex: 1 1 200px;</div>
            </div>
            
            <div class="flex-item">
                <div class="item-title">Item 2</div>
                <div class="item-code">flex: 1 1 200px;</div>
            </div>
            
            <div class="flex-item featured">
                <div class="item-title">Item 3 (Featured)</div>
                <div class="item-code">flex-grow: 2;</div>
            </div>
            
            <div class="flex-item align-diff">
                <div class="item-title">Item 4 (Offset)</div>
                <div class="item-code">align-self: center;</div>
            </div>
            
            <div class="flex-item">
                <div class="item-title">Item 5</div>
                <div class="item-code">flex: 1 1 200px;</div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Flexbox Interactive Controller
document.addEventListener('DOMContentLoaded', () => {{
    const sandbox = document.getElementById('sandbox');
    const buttons = document.querySelectorAll('button[data-prop]');

    buttons.forEach(btn => {{
        btn.addEventListener('click', () => {{
            const prop = btn.getAttribute('data-prop');
            const val = btn.getAttribute('data-val');
            
            // Apply CSS property to container
            sandbox.style[prop] = val;
            
            // Manage active states for UI
            document.querySelectorAll(`button[data-prop="${{prop}}"]`).forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
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
