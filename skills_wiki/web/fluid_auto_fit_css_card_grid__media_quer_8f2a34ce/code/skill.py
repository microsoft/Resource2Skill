def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Components",
    body_text: str = "Resize the browser to see the auto-fit grid in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent borders/hovers
    width_px: int = 1200,              # Max container width
    height_px: int = 800,              # Minimum container height
    card_min_width: int = 300,         # The critical minmax value from the video
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Auto-Fit CSS Card Grid.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"
        text_color = "#ffffff"
        card_bg = "#222429"
        card_border = "rgb(75, 82, 92)"
        text_muted = "#a0aab8"
    else:
        bg_color = "#f4f5f7"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        text_muted = "#64748b"

    # === CSS ===
    css = f"""/* Fluid Auto-Fit CSS Card Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
    --card-min-width: {card_min_width}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: var(--min-height);
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 800px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* The Core Grid Technique from the tutorial */
.grid-container {{
    display: grid;
    /* This single line replaces media queries! */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: 20px;
    justify-content: center;
    
    width: 100%;
    max-width: var(--max-width);
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 15px;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-muted);
}}
"""

    # === HTML ===
    cards_html = ""
    for i in range(1, 9):  # Generate 8 cards to clearly show wrapping behavior
        cards_html += f"""
        <div class="card">
            <h2>Lorem Ipsum {i}</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta.</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    
    <div class="grid-container">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Auto-Fit CSS Card Grid
// No JavaScript is strictly required for the CSS Grid layout to function.
// This script is included for demonstration of component mount.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid container mounted. Try resizing the window to see auto-fit in action.");
    
    // Optional: Add entrance animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {{
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }}, 100 * index); // Staggered delay
        
        // Remove inline transition after entrance so hover effect works properly
        setTimeout(() => {{
            card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease';
        }}, 100 * index + 500);
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
