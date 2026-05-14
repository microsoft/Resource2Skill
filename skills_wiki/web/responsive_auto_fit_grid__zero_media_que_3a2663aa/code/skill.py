def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Resize the browser to see the grid automatically reflow without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Vibrant pink from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f3f4f6"
        surface_color = "#1f2937"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — generated component */
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
    --border: {border_color};
    --shadow: {shadow};
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
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text);
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text);
    opacity: 0.8;
    line-height: 1.6;
}}

/* === The Magic CSS Grid === */
.grid-container {{
    display: grid;
    /* This single line creates a responsive grid without media queries */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    width: 100%;
    max-width: var(--max-width);
}}

.grid-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
    min-height: 200px;
}}

.grid-item:hover {{
    transform: translateY(-5px);
    box-shadow: var(--shadow);
    border-color: var(--accent);
}}

.item-number {{
    background: var(--accent);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2rem;
}}

.item-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.item-desc {{
    font-size: 0.95rem;
    opacity: 0.7;
    line-height: 1.5;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </header>

    <!-- The grid container -->
    <main class="grid-container" id="grid">
        <!-- Grid items will be injected by JavaScript -->
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid — DOM Population
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const numCards = 8; // Number of cards to generate

    // Generate grid items dynamically
    for (let i = 1; i <= numCards; i++) {{
        const card = document.createElement('div');
        card.className = 'grid-item';
        
        card.innerHTML = `
            <div class="item-number">${{i}}</div>
            <h2 class="item-title">Grid Item ${{i}}</h2>
            <p class="item-desc">This card automatically adjusts its width based on the container size. It will never shrink below 280px.</p>
        `;
        
        gridContainer.appendChild(card);
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
