def create_component(
    output_dir: str,
    title_text: str = "This is Responsive!",
    body_text: str = "Resize the browser window to see the grid automatically adjust its columns without a single media query.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent/hover
    width_px: int = 1200,              # Max container width
    height_px: int = 800,              # Container min-height for preview
    card_count: int = 8,               # Number of cards to generate
    min_card_width: int = 300,         # The 'min' value in minmax()
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit CSS Grid effect.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape texts
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#ffffff"
        muted_text = "rgba(255, 255, 255, 0.7)"
        surface_color = "#222429"
        border_color = "rgb(75, 82, 92)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        muted_text = "rgba(0, 0, 0, 0.6)"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"

    # Generate dummy cards
    cards_html = ""
    for i in range(card_count):
        cards_html += f"""
        <article class="card">
            <h2>Lorem Ipsum {i+1}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </article>
        """

    # === CSS ===
    css = f"""/* Responsive Auto-Fit CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-color: {text_color};
    --muted-text: {muted_text};
    --border-color: {border_color};
    --accent-color: {accent_color};
    
    /* Grid Configuration */
    --min-card-width: {min_card_width}px;
    --grid-gap: 24px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    line-height: 1.5;
}}

header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 800px;
}}

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

header p {{
    color: var(--muted-text);
    font-size: 1.1rem;
}}

/* --- THE CORE PATTERN --- */
.grid-container {{
    display: grid;
    /* 
      auto-fit: create as many columns as will fit in the container
      minmax: columns must be at least var(--min-card-width), but can grow to 1fr to fill space
    */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center; /* Centers the grid if items max out container width */
    
    width: 100%;
    max-width: {width_px}px;
}}

/* Card Styling */
.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.card h2 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    font-size: 0.95rem;
    color: var(--muted-text);
}}

/* Interactive Hover State */
.card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent-color);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Grid Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>
    
    <main class="grid-container">
        {cards_html}
    </main>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit CSS Grid
// Note: This component is 100% CSS driven. No JavaScript is required for the responsive layout!
// This script is included for structural completion.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("CSS Grid layout initialized.");
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
