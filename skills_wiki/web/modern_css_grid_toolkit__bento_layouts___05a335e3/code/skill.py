def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Mastery",
    body_text: str = "Exploring the power of asymmetric Bento layouts, fluid auto-wrapping, and grid stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#0ea5e9",     # Primary accent color (indigo/blue)
    width_px: int = 1200,
    height_px: int = 800,              # Used as a min-height for the demo wrapper
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Bento Grid and Auto-wrapping fluid layouts.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Derivation ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        text_muted = "#94a3b8"        # Slate 400
        surface_color = "#1e293b"     # Slate 800
        surface_hover = "#334155"     # Slate 700
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8fafc"          # Slate 50
        text_color = "#0f172a"        # Slate 900
        text_muted = "#64748b"        # Slate 500
        surface_color = "#ffffff"     # White
        surface_hover = "#f1f5f9"     # Slate 100
        border_color = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Modern CSS Grid Toolkit — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --accent: {accent_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
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
    line-height: 1.6;
    min-height: var(--min-height);
    padding: 3rem 1.5rem;
}}

.container {{
    max-width: var(--max-width);
    margin: 0 auto;
}}

.header {{
    margin-bottom: 3rem;
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}}

.section-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}}

/* =========================================
   1. Asymmetric Bento Grid
   Uses grid-template-areas for exact placement
   ========================================= */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* Desktop layout: 4 columns, 2 rows */
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, minmax(220px, auto));
    grid-template-areas:
        "box1 box1 box2 box3"
        "box1 box1 box4 box5";
    margin-bottom: 5rem;
}}

.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.25rem;
    padding: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
}}

.bento-item:not(.box1):hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    background: var(--surface-hover);
}}

.bento-item h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.bento-item p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

code {{
    background: rgba(128, 128, 128, 0.15);
    padding: 0.1rem 0.4rem;
    border-radius: 0.25rem;
    font-family: monospace;
    font-size: 0.85em;
}}

/* Assigning explicit areas */
.box1 {{ grid-area: box1; }}
.box2 {{ grid-area: box2; }}
.box3 {{ grid-area: box3; }}
.box4 {{ grid-area: box4; }}
.box5 {{ grid-area: box5; }}

/* Grid Stacking Technique for Hero Box */
.box1 {{
    display: grid;
    padding: 0; /* Remove padding so bg spans fully */
    border: none;
}}

.box1 > * {{
    /* Both children occupy the exact same grid cell */
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.box1-bg {{
    background: linear-gradient(135deg, var(--accent), #8b5cf6);
    width: 100%;
    height: 100%;
    opacity: 0.95;
    transition: transform 0.5s ease;
}}

.box1:hover .box1-bg {{
    transform: scale(1.05);
}}

.box1-content {{
    padding: 2rem;
    align-self: end; /* Align content to the bottom */
    z-index: 2;
    color: #ffffff;
}}

.box1-content p {{
    color: rgba(255, 255, 255, 0.9);
}}

.box1-content code {{
    background: rgba(0,0,0,0.3);
}}

/* Responsive Bento Matrix Redefinitions */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, minmax(200px, auto));
        grid-template-areas:
            "box1 box1 box2"
            "box1 box1 box3"
            "box4 box5 box5";
    }}
}}

@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas:
            "box1"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
    .box1 {{ min-height: 300px; }}
}}

/* =========================================
   2. Auto-Wrapping Fluid Grid
   Uses auto-fit and minmax for fluid wrapping
   ========================================= */
.auto-grid {{
    display: grid;
    gap: 1.5rem;
    /* The magic formula for responsive grids without media queries */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}}

.auto-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 2.5rem 1.5rem;
    text-align: center;
    transition: transform 0.3s ease, border-color 0.3s ease;
    /* Inner alignment via grid */
    display: grid;
    place-items: center;
    gap: 0.5rem;
}}

.auto-item:hover {{
    transform: scale(1.02);
    border-color: var(--accent);
}}

.circle-icon {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(14, 165, 233, 0.1);
    color: var(--accent);
    display: grid;
    place-items: center;
    margin-bottom: 0.5rem;
    font-weight: bold;
    font-size: 1.2rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <h2 class="section-title">1. Asymmetric "Bento" Grid</h2>
        <div class="bento-grid">
            <div class="bento-item box1">
                <!-- Layer 1: Background -->
                <div class="box1-bg"></div>
                <!-- Layer 2: Content (Stacked via Grid) -->
                <div class="box1-content">
                    <h3>Hero Layout Stacking</h3>
                    <p>Using <code>grid-column: 1/-1</code> to overlay text on a background without absolute positioning.</p>
                </div>
            </div>
            <div class="bento-item box2">
                <h3>Grid Areas</h3>
                <p>Mapped explicitly via CSS strings.</p>
            </div>
            <div class="bento-item box3">
                <h3>Visual Weight</h3>
                <p>Draws attention logically.</p>
            </div>
            <div class="bento-item box4">
                <h3>Reflows</h3>
                <p>Changes shape on tablet & mobile.</p>
            </div>
            <div class="bento-item box5">
                <h3>Versatility</h3>
                <p>Perfect for SaaS features & portfolios.</p>
            </div>
        </div>

        <h2 class="section-title">2. Auto-Wrapping Fluid Grid</h2>
        <div class="auto-grid">
            <div class="auto-item">
                <div class="circle-icon">1</div>
                <h3>auto-fit</h3>
                <p>Fills available columns.</p>
            </div>
            <div class="auto-item">
                <div class="circle-icon">2</div>
                <h3>minmax()</h3>
                <p>Enforces a 260px minimum width.</p>
            </div>
            <div class="auto-item">
                <div class="circle-icon">3</div>
                <h3>Fluid Resize</h3>
                <p>Expands using <code>1fr</code>.</p>
            </div>
            <div class="auto-item">
                <div class="circle-icon">4</div>
                <h3>Zero Media Queries</h3>
                <p>Wraps automatically.</p>
            </div>
            <div class="auto-item">
                <div class="circle-icon">5</div>
                <h3>place-items</h3>
                <p>Perfect inner centering.</p>
            </div>
            <div class="auto-item">
                <div class="circle-icon">6</div>
                <h3>Scalability</h3>
                <p>Handles infinite items gracefully.</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # Minimal JS needed as these layout paradigms are pure CSS.
    # Adding a small visual effect to log grid layout changes for educational observation.
    js = f"""// Modern CSS Grid Toolkit
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Grid components loaded perfectly.");
    
    // Optional: Add subtle entry animations
    const items = document.querySelectorAll('.bento-item, .auto-item');
    items.forEach((item, index) => {{
        item.style.opacity = '0';
        item.style.transform = 'translateY(15px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {{
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
            
            // Re-apply hover transitions after entry animation completes
            setTimeout(() => {{
                item.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease, border-color 0.3s ease';
            }}, 500);
        }}, 100 * (index % 6));
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
