def create_component(
    output_dir: str,
    title_text: str = "Our hero heading",
    body_text: str = "This is just placeholder text. Don't be alarmed, this is just here to fill up space since your finalized copy isn't ready yet. Once we have your content finalized, we'll replace this placeholder text with your real content.",
    color_scheme: str = "light",
    accent_color: str = "#0ea5e9",
    width_px: int = 1200,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#020617"
        text_color = "#f8fafc"
        surface_color = "#0f172a"
        surface_border = "#1e293b"
        text_muted = "#94a3b8"
    else:
        bg_color = "#ffffff"
        text_color = "#0f172a"
        surface_color = "#f8fafc"
        surface_border = "#e2e8f0"
        text_muted = "#475569"

    css = f"""/* CSS Grid Bleed Layout (Split Hero) */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-border: {surface_border};
    
    /* Grid Configuration */
    --content-max-width: {width_px}px;
    --padding-inline: clamp(1rem, 5vw, 2rem);
    --split-ratio: 0.5; /* 0.5 = 50/50 split. 0.4 = 40/60 split */
    --hero-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* 
  The "Content Grid" Pattern
  Creates a 4-column grid. The middle two columns equal the max-width of the site.
  The outer two columns act as flexible margins that extend to the screen edge.
*/
.split-hero {{
    display: grid;
    grid-template-columns:
        [full-start] minmax(var(--padding-inline), 1fr)
        [content-start] minmax(0, calc(var(--content-max-width) * var(--split-ratio)))
        [center] minmax(0, calc(var(--content-max-width) * (1 - var(--split-ratio)))) [content-end]
        minmax(var(--padding-inline), 1fr) [full-end];
    
    min-height: var(--hero-height);
    background-color: var(--surface);
}}

/* Default Layout: Text Left, Image Right */
.split-hero .hero-content {{
    grid-column: content-start / center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 1.5rem;
    padding-block: 4rem;
    padding-right: clamp(2rem, 6vw, 4rem); /* Acts as the gap between text and image */
    transition: padding 0.3s ease;
}}

.split-hero .hero-media {{
    grid-column: center / full-end;
    height: 100%;
    position: relative;
    overflow: hidden;
}}

.split-hero .hero-media img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.5s ease;
}}

.split-hero .hero-media:hover img {{
    transform: scale(1.03);
}}

/* Flipped Layout: Image Left, Text Right */
.split-hero.flipped .hero-content {{
    grid-column: center / content-end;
    padding-right: 0;
    padding-left: clamp(2rem, 6vw, 4rem);
}}

.split-hero.flipped .hero-media {{
    grid-column: full-start / center;
}}

/* Typography & Elements */
.title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.lead {{
    font-size: clamp(1rem, 2vw, 1.125rem);
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 45ch;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.875rem 1.75rem;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    font-weight: 500;
    border-radius: 0.375rem;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
}}

.btn:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}}

/* Interactive Demo Controls Panel (Builder UI Simulation) */
.demo-controls {{
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--bg);
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    z-index: 100;
    border: 1px solid var(--surface-border);
    min-width: 250px;
}}

.demo-controls h3 {{
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: -0.5rem;
}}

.control-group {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.875rem;
}}

.control-group-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

input[type=range] {{
    width: 100%;
    cursor: pointer;
    accent-color: var(--accent);
}}

/* Responsive Breakpoint */
@media (max-width: 768px) {{
    .split-hero {{
        --split-ratio: 1; /* Reset logic for clean single column */
        grid-template-columns:
            [full-start] minmax(var(--padding-inline), 1fr)
            [content-start center] minmax(0, var(--content-max-width)) [content-end]
            minmax(var(--padding-inline), 1fr) [full-end];
        grid-template-rows: auto auto;
    }}
    
    .split-hero .hero-content,
    .split-hero.flipped .hero-content {{
        grid-column: content-start / content-end;
        grid-row: 1;
        padding-inline: 0;
        padding-bottom: 3rem;
    }}
    
    .split-hero .hero-media,
    .split-hero.flipped .hero-media {{
        /* On mobile, let the image bleed edge-to-edge horizontally */
        grid-column: full-start / full-end; 
        grid-row: 2;
        min-height: 400px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Split Hero Component -->
    <section class="split-hero" id="hero-instance">
        <div class="hero-content">
            <h1 class="title">{title_text}</h1>
            <p class="lead">{body_text}</p>
            <a href="#" class="btn">Call to action</a>
        </div>
        <div class="hero-media">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1400&q=80" alt="Hero portrait model showcasing fashion">
        </div>
    </section>

    <!-- Builder Simulation UI (Not part of core component, for demo purposes) -->
    <div class="demo-controls">
        <h3>Layout Controls</h3>
        <div class="control-group">
            <div class="control-group-row">
                <label>Flip Sides</label>
                <button class="btn" id="toggle-flip" style="padding: 0.25rem 0.75rem; font-size: 0.75rem;">Toggle</button>
            </div>
        </div>
        <div class="control-group">
            <div class="control-group-row">
                <label>Split Ratio</label>
                <span id="ratio-val" style="font-weight:bold; color:var(--accent);">50 / 50</span>
            </div>
            <input type="range" id="ratio-slider" min="0.3" max="0.7" step="0.05" value="0.5">
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Component Logic & Builder Controls Simulation
document.addEventListener('DOMContentLoaded', () => {{
    const hero = document.getElementById('hero-instance');
    const toggleBtn = document.getElementById('toggle-flip');
    const ratioSlider = document.getElementById('ratio-slider');
    const ratioValDisplay = document.getElementById('ratio-val');

    // Toggle Left/Right layout orientation
    toggleBtn.addEventListener('click', () => {{
        hero.classList.toggle('flipped');
    }});

    // Dynamically adjust the CSS Grid split ratio
    ratioSlider.addEventListener('input', (e) => {{
        const val = parseFloat(e.target.value);
        
        // Update CSS Custom Property driving the grid columns
        hero.style.setProperty('--split-ratio', val);
        
        // Update UI Display
        const leftPercent = Math.round(val * 100);
        const rightPercent = Math.round((1 - val) * 100);
        
        // Account for flip state in label
        if (hero.classList.contains('flipped')) {{
            ratioValDisplay.innerText = `${{rightPercent}} / ${{leftPercent}}`;
        }} else {{
            ratioValDisplay.innerText = `${{leftPercent}} / ${{rightPercent}}`;
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
