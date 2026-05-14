def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid Cards.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        page_bg = "#0d0d14"
        card_bg = "#222429"
        text_primary = "#ffffff"
        text_secondary = "#a0aab8"
        border_color = "#373a43"
    else:
        page_bg = "#f3f4f6"
        card_bg = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        border_color = "#e5e7eb"

    # HTML content generation - generating 8 cards to clearly show wrapping and the last row
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <div class="card">
                <h2 class="card-title">Lorem Ipsum {i}</h2>
                <p class="card-body">{body_text}</p>
            </div>"""

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid Cards */
:root {{
    --page-bg: {page_bg};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --accent: {accent_color};
    --base-width: {width_px}px;
    --base-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
}}

/* Resizable Demo Wrapper - allows dragging to see the responsive effect locally */
.demo-wrapper {{
    width: 100%;
    max-width: var(--base-width);
    min-height: 50vh;
    padding: 1rem;
    resize: horizontal; /* Interactive resizing */
    overflow: hidden;
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    position: relative;
    background: rgba(0,0,0,0.02);
}}

.demo-wrapper::after {{
    content: '↔ Drag to resize & test grid';
    position: absolute;
    bottom: 8px;
    right: 24px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    pointer-events: none;
}}

/* --- THE CORE GRID TECHNIQUE --- */
.grid-container {{
    display: grid;
    /* This is the magic line from the tutorial */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    /* Centers the grid columns if they don't stretch the full width */
    justify-content: center; 
    width: 100%;
}}

/* Card Styling */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 200px;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-primary);
}}

.card-body {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-secondary);
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
    <div class="header">
        <h1>{title_text}</h1>
        <p>A fluid, responsive grid layout without media queries using <code>auto-fit</code> and <code>minmax()</code>.</p>
    </div>

    <!-- Drag the bottom right corner of this wrapper to see the cards wrap perfectly -->
    <div class="demo-wrapper">
        <div class="grid-container">
{cards_html}
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid Cards
document.addEventListener('DOMContentLoaded', () => {{
    // The core layout is powered entirely by CSS Grid.
    // No JavaScript resize listeners are required for this layout technique to work.
    
    const wrapper = document.querySelector('.demo-wrapper');
    const cards = document.querySelectorAll('.card');

    // Optional: Add a slight entrance animation to showcase the grid loading
    cards.forEach((card, index) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {{
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            
            // Reset transition for hover effects after entrance
            setTimeout(() => {{
                card.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease';
            }}, 600);
        }}, 100 * index); // Staggered delay
    }});
}});
"""

    # Write files
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
