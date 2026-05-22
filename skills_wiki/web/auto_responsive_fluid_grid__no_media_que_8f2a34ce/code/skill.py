def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Resize the browser window to see the cards automatically wrap and scale using CSS Grid.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent (e.g., blue)
    width_px: int = 1200,              # Max container width
    height_px: int = 800,              # Min viewport height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid pattern.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f9fafb"
        subtext_color = "#9ca3af"
        surface_color = "#1f2937"
        border_color = "rgba(255, 255, 255, 0.1)"
        hover_shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        subtext_color = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        hover_shadow = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --hover-shadow: {hover_shadow};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    line-height: 1.5;
}}

.page-header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 600px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.page-header p {{
    color: var(--subtext);
    font-size: 1.125rem;
}}

/* =========================================
   CORE SKILL: THE AUTO-RESPONSIVE GRID
   ========================================= */
.grid-container {{
    display: grid;
    /* repeat(auto-fit, ...) calculates how many columns can fit.
       minmax(300px, 1fr) ensures columns are at least 300px wide,
       but will stretch (1fr) to fill remaining space. */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    width: 100%;
    max-width: var(--max-width);
}}

/* Card Styling */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px var(--hover-shadow);
    border-color: var(--accent);
}}

.card-icon {{
    width: 48px;
    height: 48px;
    background-color: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    font-size: 24px;
}}

.card h2 {{
    font-size: 1.25rem;
    margin-bottom: 12px;
    font-weight: 600;
}}

.card p {{
    color: var(--subtext);
    font-size: 0.95rem;
    flex-grow: 1; /* Pushes button to bottom if card heights vary */
    margin-bottom: 20px;
}}

.card-footer {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--accent);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: auto;
}}

.card-footer::after {{
    content: '→';
    transition: transform 0.2s ease;
}}

.card:hover .card-footer::after {{
    transform: translateX(4px);
}}
"""

    # Escape text to prevent basic HTML injection
    import html as html_escape
    safe_title = html_escape.escape(title_text)
    safe_body = html_escape.escape(body_text)

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="page-header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>

    <!-- The Grid Container -->
    <div class="grid-container" id="grid-root">
        <!-- Cards will be injected here via JavaScript for demonstration purposes -->
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Auto-Responsive Grid — dynamic content injection
document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-root');
    
    // Sample data to populate the grid
    const cardsData = [
        { title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate." },
        { title: "Responsive Layouts", content: "Never write a media query for your grid columns again. The browser calculates the optimal fit based on the minmax function." },
        { title: "Performance First", content: "Using native CSS Grid is heavily optimized by modern browsers, resulting in zero jank and layout shifting compared to JS resize listeners." },
        { title: "Flexible Content", content: "Grid items can have variable height content, but the row will automatically stretch the shorter items to match the tallest item." },
        { title: "Gap Integration", content: "The CSS gap property applies perfect gutters between columns and rows without margin collapsing issues." },
        { title: "Intrinsic Design", content: "Design from the inside out. Let elements dictate their required space, ensuring content is never squeezed beyond readability." }
    ];

    // Generate HTML for each card and append to container
    cardsData.forEach(data => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-icon">✧</div>
            <h2>${data.title}</h2>
            <p>${data.content}</p>
            <div class="card-footer">Learn more</div>
        `;
        gridContainer.appendChild(card);
    });
});
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
