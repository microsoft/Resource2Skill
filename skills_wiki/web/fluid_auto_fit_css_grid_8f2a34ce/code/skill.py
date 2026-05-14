def create_component(
    output_dir: str,
    title_text: str = "Fluid Auto-Fit Grid",
    body_text: str = "Resize the viewport to see the cards automatically wrap and scale to fill the available space without any media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Auto-Fit CSS Grid layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#222429"
        border_color = "#4b525c"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
    else:
        bg_color = "#f9fafb"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"
        text_color = "#111827"
        text_muted = "#6b7280"

    # Generate dummy cards
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum {i}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Fluid Auto-Fit Grid Generated Component */
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

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    font-weight: 700;
}}

header p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* === CORE TECHNIQUE === */
.grid-container {{
    display: grid;
    /* 
      auto-fit: create as many columns as will fit in the container.
      minmax(300px, 1fr): columns must be at least 300px wide, 
      but can grow to 1 fraction of available space if there is leftover room.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px; /* Space between rows and columns */
    
    width: 100%;
    max-width: {width_px}px; /* Constrain max width based on requested params */
    margin: 0 auto;
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2.5em 2em;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    /* Subtle polish */
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.6;
}}

/* Ensure responsive preview within the requested height constraints */
@media (min-height: {height_px}px) {{
    body {{
        justify-content: center;
    }}
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

    <!-- The core grid wrapper -->
    <div class="grid-container" id="grid">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS approach — no layout JS needed.
// This script exists merely to demonstrate how you might dynamically add cards to test the grid flow.

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    
    // Optional: Log grid info to console
    console.log("Grid layout active. Resize window to see auto-fit in action.");
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
