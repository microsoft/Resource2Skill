def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Drag the bottom-right corner of this container to resize it. Watch how the CSS Grid automatically recalculates the column count to fit the space perfectly—without a single media query.",
    color_scheme: str = "dark",
    accent_color: str = "#ec4899",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_border = "rgba(255, 255, 255, 0.1)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        text_muted = "#6b7280"
        surface_color = "#ffffff"
        surface_border = "rgba(0, 0, 0, 0.1)"
        surface_hover = "#f3f4f6"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-border: {surface_border};
    --surface-hover: {surface_hover};
    --shadow: {shadow_color};
    
    --card-min-width: 250px;
    --grid-gap: 1.5rem;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Interactive Demo Wrapper to showcase responsiveness */
.demo-wrapper {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    max-height: 90vh;
    resize: both;
    overflow: auto;
    background: var(--bg);
    border: 2px dashed var(--surface-border);
    border-radius: 16px;
    padding: 2rem;
    position: relative;
    box-shadow: 0 25px 50px -12px var(--shadow);
}}

/* Custom Scrollbar for Demo Wrapper */
.demo-wrapper::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
.demo-wrapper::-webkit-scrollbar-track {{
    background: transparent;
}}
.demo-wrapper::-webkit-scrollbar-thumb {{
    background: var(--surface-border);
    border-radius: 4px;
}}

.header {{
    margin-bottom: 2rem;
    max-width: 600px;
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* 
  =========================================
  THE MAGIC GRID TECHNIQUE
  =========================================
*/
.grid-container {{
    display: grid;
    /* 
      1. repeat(auto-fit): creates as many columns as fit the container
      2. minmax(): dictates the size rules for those columns
      3. min(100%, 250px): prevents overflow if container is narrower than 250px
      4. 1fr: allows columns to stretch and fill remaining space equally
    */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--card-min-width)), 1fr));
    gap: var(--grid-gap);
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s ease, 
                border-color 0.3s ease;
    cursor: default;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 24px var(--shadow);
    border-color: var(--accent);
    background: var(--surface-hover);
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.card-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--accent);
    font-weight: 700;
    font-size: 1.2rem;
    border: 1px solid var(--surface-border);
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* Visual indicator for resizing */
.resize-hint {{
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-size: 0.75rem;
    color: var(--text-muted);
    pointer-events: none;
    opacity: 0.6;
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
    <div class="demo-wrapper">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <!-- The Grid -->
        <div class="grid-container" id="dynamic-grid">
            <!-- Cards injected via JS -->
        </div>
        
        <div class="resize-hint">↘ Drag to resize</div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generate grid items dynamically to demonstrate the layout
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('dynamic-grid');
    const numCards = 8;
    
    for(let i = 1; i <= numCards; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-header">
                <div class="card-icon">${{i}}</div>
                <h3 class="card-title">Grid Item ${{i}}</h3>
            </div>
            <p class="card-desc">I am a flexible grid track. As the container resizes, I will stretch to fill space or wrap to a new line.</p>
        `;
        grid.appendChild(card);
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
