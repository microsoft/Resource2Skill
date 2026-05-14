def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Patterns",
    body_text: str = "Resize the browser to see the grid automatically adjust columns without media queries.",
    color_scheme: str = "dark",
    accent_color: str = "#6366f1",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # Cards generation
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <div class="card-icon" style="color: var(--accent);">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                </div>
                <h3 class="card-title">Grid Item {i}</h3>
                <p class="card-desc">This card automatically adapts its width based on the grid's minmax constraints.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit CSS Grid — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --min-col-width: 280px; /* The magic breakpoint value */
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 40px 20px;
    line-height: 1.5;
}}

.layout-wrapper {{
    width: 100%;
    max-width: var(--width);
}}

.header {{
    text-align: center;
    margin-bottom: 48px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.subtitle {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* === THE MAGIC GRID PATTERN === */
.auto-grid {{
    display: grid;
    /* This single line handles all responsive wrapping without media queries */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-col-width), 1fr));
    gap: 24px;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
    box-shadow: 0 4px 6px -1px var(--shadow), 0 2px 4px -2px var(--shadow);
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px var(--shadow), 0 4px 6px -4px var(--shadow);
    border-color: var(--accent);
}}

.card-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    margin-bottom: 8px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.6;
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
    <div class="layout-wrapper">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>
        
        <main class="auto-grid">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit CSS Grid — generated component
document.addEventListener('DOMContentLoaded', () => {{
    // The responsive behavior is natively handled by CSS Grid.
    // This JS file is included for potential future interactivity.
    
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {{
        card.addEventListener('click', () => {{
            const title = card.querySelector('.card-title').innerText;
            console.log(`Clicked on ${{title}}`);
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
