def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Resize the browser to see the grid automatically reflow columns using auto-fit and minmax().",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fit Responsive CSS Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Optional kwargs configuration
    num_cards = kwargs.get("num_cards", 8)
    min_card_width = kwargs.get("min_card_width", 300)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"       # Deep dark blue/grey
        text_color = "#ffffff"
        text_muted = "#a0aab5"
        surface_color = "#222429"  # Elevated card color
        border_color = "#4b525c"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"

    # === CSS ===
    css = f"""/* Auto-Fit Responsive Grid — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 800px;
}}

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: var(--text-color);
}}

header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.5;
}}

/* THE CORE COMPONENT LAYOUT */
.grid-container {{
    display: grid;
    /* 
      1. auto-fit: place as many columns as fit the container 
      2. minmax: columns must be at least min_card_width wide
         but can grow (1fr) if there is extra space.
      Using min(100%, min_card_width) prevents overflow on very tiny screens.
    */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, {min_card_width}px), 1fr));
    gap: 20px;
    
    width: 100%;
    max-width: {width_px}px;
    
    /* Ensures grid centers nicely if container is wider than total max columns */
    justify-content: center; 
}}

/* Card Styling */
.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    /* Subtle hover effect to prove interactivity */
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-color);
    box-shadow: 0 10px 20px rgba(0,0,0, 0.1);
}}

.card h2 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-muted);
}}
"""

    # Generate dummy cards
    cards_html = ""
    for i in range(num_cards):
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum {i+1}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.</p>
        </div>"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>
    
    <!-- Component Start -->
    <div class="grid-container">
        {cards_html}
    </div>
    <!-- Component End -->
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Fit Responsive Grid
document.addEventListener('DOMContentLoaded', () => {{
    // The responsiveness is entirely handled natively by CSS Grid.
    // No JavaScript event listeners or resize observers are needed!
    console.log("Grid initialized successfully.");
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
