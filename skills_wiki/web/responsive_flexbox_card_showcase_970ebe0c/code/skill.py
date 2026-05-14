def create_component(
    output_dir: str,
    title_text: str = "CSS Flexbox Interactive Showcase",
    body_text: str = "Use the controls below to manipulate the flex container properties in real-time. Resize your browser to see flex-wrap in action.",
    color_scheme: str = "dark",
    accent_color: str = "#0071FF",  # Video's specific shade of blue
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing an interactive CSS Flexbox showcase.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)
    
    # Safe text escaping
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0b0e14"
        container_bg = "#151b23"
        text_primary = "#ffffff"
        text_secondary = "#8b949e"
        border_color = "rgba(255, 255, 255, 0.15)"
        card_bg = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f6f8fa"
        container_bg = "#ffffff"
        text_primary = "#1f2328"
        text_secondary = "#656d76"
        border_color = "rgba(0, 0, 0, 0.15)"
        card_bg = "rgba(0, 0, 0, 0.02)"

    # === CSS ===
    css = f"""/* Flexbox Interactive Showcase */
:root {{
    --bg-color: {bg_color};
    --container-bg: {container_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --card-bg: {card_bg};
    --accent: {accent_color};
    --max-width: {width_px}px;
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

header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: 800px;
}}

header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

header p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* Controls Section */
.controls {{
    background: var(--container-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
}}

.control-group {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex-grow: 1;
}}

.control-group label {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
}}

.button-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

button {{
    background: var(--card-bg);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.9rem;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--border-color);
}}

button.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}}

/* Flex Container Frame (Mimicking the video's presentation) */
.flex-frame {{
    width: 100%;
    max-width: var(--max-width);
    min-height: {height_px // 2}px;
    background: var(--container-bg);
    border: 4px solid var(--border-color); /* Bold border from video */
    border-radius: 8px;
    padding: 1.5rem;
    overflow: hidden;
}}

/* THE ACTUAL FLEX CONTAINER */
.flex-container {{
    display: flex;
    gap: 20px; /* Video default */
    flex-wrap: wrap; /* Video default */
    justify-content: flex-start;
    align-items: stretch;
    height: 100%;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* Flex Items (Cards) */
.flex-item {{
    background: var(--card-bg);
    border: 2px solid var(--accent); /* Accent border from video */
    border-radius: 8px;
    padding: 2rem;
    flex: 1 1 250px; /* Grow, Shrink, Basis */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.flex-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 113, 255, 0.15);
}}

.flex-item h2 {{
    font-size: 1.25rem;
    color: var(--text-primary);
}}

.flex-item p {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1; /* Pushes button to bottom */
}}

.flex-item .item-btn {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 0.75rem;
    border-radius: 4px;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    width: 100%;
    transition: filter 0.2s;
}}

.flex-item .item-btn:hover {{
    filter: brightness(1.2);
}}

/* Specific helper classes for height to demonstrate align-items */
.flex-item:nth-child(2) {{ min-height: 250px; }}
.flex-item:nth-child(4) {{ min-height: 280px; }}

@media (max-width: 768px) {{
    body {{ padding: 1rem; }}
    .controls {{ flex-direction: column; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>

    <section class="controls">
        <div class="control-group">
            <label>Flex Direction</label>
            <div class="button-row">
                <button data-prop="flexDirection" data-val="row" class="active">row</button>
                <button data-prop="flexDirection" data-val="column">column</button>
                <button data-prop="flexDirection" data-val="row-reverse">row-reverse</button>
            </div>
        </div>
        
        <div class="control-group">
            <label>Justify Content</label>
            <div class="button-row">
                <button data-prop="justifyContent" data-val="flex-start" class="active">flex-start</button>
                <button data-prop="justifyContent" data-val="center">center</button>
                <button data-prop="justifyContent" data-val="flex-end">flex-end</button>
                <button data-prop="justifyContent" data-val="space-between">space-between</button>
                <button data-prop="justifyContent" data-val="space-evenly">space-evenly</button>
            </div>
        </div>

        <div class="control-group">
            <label>Align Items</label>
            <div class="button-row">
                <button data-prop="alignItems" data-val="stretch" class="active">stretch</button>
                <button data-prop="alignItems" data-val="flex-start">flex-start</button>
                <button data-prop="alignItems" data-val="center">center</button>
                <button data-prop="alignItems" data-val="flex-end">flex-end</button>
            </div>
        </div>
        
        <div class="control-group">
            <label>Flex Wrap</label>
            <div class="button-row">
                <button data-prop="flexWrap" data-val="wrap" class="active">wrap</button>
                <button data-prop="flexWrap" data-val="nowrap">nowrap</button>
            </div>
        </div>
    </section>

    <section class="flex-frame">
        <div class="flex-container" id="flexBox">
            <article class="flex-item">
                <h2>Layout Flexibility</h2>
                <p>Flexbox allows items to grow and shrink dynamically. Resize the browser to see these boxes stack.</p>
                <a href="#" class="item-btn">Learn More</a>
            </article>
            <article class="flex-item">
                <h2>Alignment Mastery</h2>
                <p>No more vertical alignment hacks. Use <code>align-items</code> and <code>justify-content</code>.</p>
                <a href="#" class="item-btn">Learn More</a>
            </article>
            <article class="flex-item">
                <h2>Consistent Gaps</h2>
                <p>The <code>gap</code> property creates perfect spacing between elements without relying on margins.</p>
                <a href="#" class="item-btn">Learn More</a>
            </article>
            <article class="flex-item">
                <h2>Source Order Independence</h2>
                <p>Use <code>row-reverse</code> or <code>column-reverse</code> to visually alter layouts without touching HTML.</p>
                <a href="#" class="item-btn">Learn More</a>
            </article>
            <article class="flex-item">
                <h2>Fluid Proportions</h2>
                <p>Combining <code>flex-basis</code> and <code>flex-grow</code> yields mathematically perfect fluid grids.</p>
                <a href="#" class="item-btn">Learn More</a>
            </article>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Flexbox Interactive Controller
document.addEventListener('DOMContentLoaded', () => {
    const flexContainer = document.getElementById('flexBox');
    const buttons = document.querySelectorAll('.controls button');

    buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const property = e.target.getAttribute('data-prop');
            const value = e.target.getAttribute('data-val');

            // Apply the CSS property to the container
            flexContainer.style[property] = value;

            // Handle active state styling for buttons in the same group
            const group = e.target.closest('.button-row');
            group.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
        });
    });
});"""

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
