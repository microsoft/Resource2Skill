def create_component(
    output_dir: str,
    title_text: str = "CSS Subgrid Alignment",
    body_text: str = "Notice how the buttons and paragraphs perfectly align across all cards, regardless of the text length inside them. Toggle the button below to see the difference.",
    color_scheme: str = "dark",        
    accent_color: str = "#00e5ff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Subgrid Aligned Card Deck.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#08060f"
        surface_color = "#161124"
        surface_hover = "#1d1630"
        text_color = "#f0f0f0"
        text_muted = "rgba(255, 255, 255, 0.7)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f4f5f8"
        surface_color = "#ffffff"
        surface_hover = "#f9fafb"
        text_color = "#0a0a0f"
        text_muted = "rgba(0, 0, 0, 0.6)"
        border_color = "rgba(0, 0, 0, 0.08)"

    css = f"""/* CSS Subgrid Alignment Component */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.main-header {{
    text-align: center;
    max-width: 800px;
    margin-bottom: 3rem;
}}

.main-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.main-header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2rem;
}}

/* Toggle Button Styling */
.controls {{
    display: flex;
    gap: 1rem;
    justify-content: center;
}}

.toggle-btn {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--accent);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.toggle-btn:hover, .toggle-btn.active {{
    background: var(--accent);
    color: #000;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
}}

/* == Core Subgrid Architecture == */
.card-wrapper {{
    display: grid;
    /* Responsive columns */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    width: 100%;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    transition: transform 0.3s ease, border-color 0.3s ease;
    
    /* SUBGRID MAGIC HERE */
    display: grid;
    grid-template-rows: subgrid;
    /* Span 3 rows in the parent grid (one for h2, one for p, one for button) */
    grid-row: span 3;
    /* Override inherited parent gap to standard component spacing */
    gap: 1.5rem; 
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.2);
    background: var(--surface-hover);
}}

.card h2 {{
    font-size: 1.5rem;
    line-height: 1.3;
    color: var(--text);
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.6;
    /* align-self controls how it sits inside its shared track */
    align-self: start; 
}}

.card button {{
    margin-top: auto;
    padding: 0.875rem;
    border-radius: 8px;
    border: none;
    background: rgba(255, 255, 255, 0.05);
    color: var(--accent);
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
}}

.card button:hover {{
    background: var(--accent);
    color: #000;
}}


/* == Legacy Layout (For Comparison Toggle) == */
.card-wrapper.legacy-layout .card {{
    /* Revert to standard flexbox behavior where internal items don't sync */
    display: flex;
    flex-direction: column;
    grid-row: auto; /* Remove span */
}}

.card-wrapper.legacy-layout .card p {{
    flex-grow: 1; /* Traditional hack to push button down, but misaligns paragraphs */
}}

/* Badges for visualization */
.badge {{
    display: inline-block;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: rgba(0, 229, 255, 0.1);
    color: var(--accent);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    font-weight: 700;
}}
"""

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
    
    <div class="main-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <div class="controls">
            <button id="toggle-btn" class="toggle-btn active">Using CSS Subgrid</button>
        </div>
    </div>

    <!-- The Grid Wrapper -->
    <div class="card-wrapper" id="grid-container">
        
        <!-- Card 1 -->
        <div class="card">
            <div>
                <span class="badge">Basic Layout</span>
                <h2>Custom Websites</h2>
            </div>
            <p>We design fast, modern, and responsive websites that help your business look professional on every device. Everything is built with scalability in mind.</p>
            <button>Learn More</button>
        </div>

        <!-- Card 2 -->
        <div class="card">
            <div>
                <span class="badge">Long Heading Variant</span>
                <h2>Full-Service Web Development & Architecture</h2>
            </div>
            <p>Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs.</p>
            <button>Discover Platform</button>
        </div>

        <!-- Card 3 -->
        <div class="card">
            <div>
                <span class="badge">Short Variant</span>
                <h2>SEO Optimization</h2>
            </div>
            <p>Slow site? Dropping rankings? We audit, optimize, and rebuild your foundation.</p>
            <button>Optimize Now</button>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.getElementById('toggle-btn');
    const gridContainer = document.getElementById('grid-container');

    let isSubgrid = true;

    toggleBtn.addEventListener('click', () => {{
        isSubgrid = !isSubgrid;
        
        if (isSubgrid) {{
            gridContainer.classList.remove('legacy-layout');
            toggleBtn.classList.add('active');
            toggleBtn.textContent = "Using CSS Subgrid";
        }} else {{
            gridContainer.classList.add('legacy-layout');
            toggleBtn.classList.remove('active');
            toggleBtn.textContent = "Using Legacy Flexbox";
        }}
    }});
}});
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
