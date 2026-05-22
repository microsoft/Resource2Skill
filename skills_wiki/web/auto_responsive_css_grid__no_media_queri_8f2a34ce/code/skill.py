def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Resize the browser window to see the grid automatically wrap and resize its items without media queries.",
    color_scheme: str = "dark",        
    accent_color: str = "rgb(75, 82, 92)", 
    width_px: int = 1200,
    height_px: int = 800, # Used for max-width of container
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        surface_color = "#222429"
        border_color = accent_color
        muted_text = "#a0aab2"
    else:
        bg_color = "#f4f4f9"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = accent_color if accent_color != "rgb(75, 82, 92)" else "#d1d5db"
        muted_text = "#6b7280"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid */
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
    --muted: {muted_text};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

header p {{
    color: var(--muted);
    line-height: 1.5;
}}

/* --- THE CORE TECHNIQUE --- */
.grid-container {{
    width: 100%;
    max-width: var(--max-width);
    
    /* 1. Define as Grid */
    display: grid;
    
    /* 2. The Magic Line:
       - repeat(): Repeat the column definition
       - auto-fit: Fit as many columns as possible before wrapping
       - minmax(300px, 1fr): Each column is AT LEAST 300px wide, and AT MOST 1 fraction of available space
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    
    /* 3. Spacing */
    gap: 20px;
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--muted);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main class="grid-container" id="grid-container">
        <!-- Cards injected via JS for demonstration -->
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generate dummy content to demonstrate the grid
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('grid-container');
    const cardCount = 8; // Change this to test with more/fewer items

    const dummyText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.";

    for (let i = 1; i <= cardCount; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        card.innerHTML = `
            <h2>Lorem Ipsum</h2>
            <p>${{dummyText}}</p>
        `;
        
        container.appendChild(card);
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
