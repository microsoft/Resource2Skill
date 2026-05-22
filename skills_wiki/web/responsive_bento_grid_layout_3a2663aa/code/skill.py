def create_component(
    output_dir: str,
    title_text: str = "Bento Grid Dashboard",
    body_text: str = "A responsive CSS Grid layout using auto-fit, minmax(), and implicit spanning without breakpoints.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme derivation
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "#334155"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3)"
        hover_shadow = "0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)"
        hover_shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.05)"

    css = f"""/* Responsive Bento Grid Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
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
    align-items: center;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background: var(--bg);
    overflow-y: auto;
    overflow-x: hidden;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

/* Header */
.app-header {{
    text-align: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}}

.app-header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.app-header p {{
    color: var(--text-muted);
    font-size: 1rem;
}}

/* === CORE TECHNIQUE: Responsive Grid === */
.bento-grid {{
    display: grid;
    /* auto-fit + minmax creates responsive columns without media queries.
       min(240px, 100%) ensures the column doesn't overflow on screens smaller than 240px */
    grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr));
    /* Implicit rows take a minimum of 180px, but expand to fit content */
    grid-auto-rows: minmax(180px, auto);
    /* dense flow fills in gaps left by spanning items */
    grid-auto-flow: dense;
    gap: 1.5rem;
}}

/* Base Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: var(--hover-shadow);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--accent);
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* === Spanning Techniques === */
.card--tall {{
    grid-row: span 2;
}}

/* Use a simple media query to prevent wide cards from blowing out small mobile screens */
@media (min-width: 550px) {{
    .card--wide {{
        grid-column: span 2;
    }}
    .card--hero {{
        grid-column: span 2;
        grid-row: span 2;
    }}
}}

/* === Layering with Grid (No Position Absolute) === */
.card--layered {{
    display: grid;
    /* Single implicit cell */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    padding: 0; /* Remove padding to allow bg to stretch */
    overflow: hidden;
}}

.card--layered .layer-bg {{
    /* Span full grid */
    grid-area: 1 / 1 / -1 / -1;
    background: linear-gradient(135deg, var(--accent), transparent);
    opacity: 0.15;
    z-index: 1;
}}

.card--layered .layer-img {{
    grid-area: 1 / 1 / -1 / -1;
    z-index: 2;
    justify-self: end;
    align-self: start;
    font-size: 4rem;
    opacity: 0.5;
    transform: translate(20px, -20px);
}}

.card--layered .layer-content {{
    grid-area: 1 / 1 / -1 / -1;
    z-index: 3;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}

/* === Alignment Properties === */
.card--align {{
    display: grid;
}}

.align-box {{
    /* Aligning the item inside its grid cell */
    justify-self: center;
    align-self: center;
    background: var(--accent);
    color: #fff;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}}

/* Scrollbar styling for container */
.app-container::-webkit-scrollbar {{ width: 8px; }}
.app-container::-webkit-scrollbar-track {{ background: var(--bg); }}
.app-container::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}
"""

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
    <div class="app-container">
        <header class="app-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid">
            
            <!-- Hero Card: Spans 2x2 on larger screens -->
            <div class="card card--hero">
                <h2 class="card-title">Responsive auto-fit</h2>
                <p class="card-desc">This layout uses <code>repeat(auto-fit, minmax(240px, 1fr))</code>. The browser calculates how many columns fit automatically. No media queries are needed for the column logic!</p>
            </div>

            <!-- Standard Card -->
            <div class="card">
                <h2 class="card-title">Standard 1x1</h2>
                <p class="card-desc">Just a regular card taking up a single implicit grid cell. The row height is set via <code>grid-auto-rows: minmax(180px, auto)</code>.</p>
            </div>

            <!-- Tall Card -->
            <div class="card card--tall">
                <h2 class="card-title">Vertical Span</h2>
                <p class="card-desc">Using <code>grid-row: span 2</code> makes this card stretch across two rows vertically. Grid auto-flow dense ensures empty spaces around it get filled.</p>
            </div>

            <!-- Layered Card -->
            <div class="card card--layered card--wide">
                <div class="layer-bg"></div>
                <div class="layer-img">✨</div>
                <div class="layer-content">
                    <h2 class="card-title" style="color: inherit;">Grid Layering</h2>
                    <p class="card-desc" style="color: inherit; opacity: 0.9;">Elements are overlapped using <code>grid-area: 1 / 1 / -1 / -1</code> and z-index, entirely avoiding absolute positioning.</p>
                </div>
            </div>

            <!-- Alignment Card -->
            <div class="card card--align">
                <div class="align-box">justify-self: center</div>
            </div>

            <!-- Standard Card -->
            <div class="card">
                <h2 class="card-title">Implicit Grid</h2>
                <p class="card-desc">If you add more items than explicit tracks, the implicit grid handles them seamlessly.</p>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Responsive Bento Grid
document.addEventListener('DOMContentLoaded', () => {
    // Layout and responsiveness are handled entirely by CSS Grid.
    console.log("Grid initialized. Try resizing the container to see auto-fit in action.");
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
