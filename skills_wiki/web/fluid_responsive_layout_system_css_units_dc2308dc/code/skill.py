def create_component(
    output_dir: str,
    title_text: str = "Mastering CSS Units",
    body_text: str = "A fluid, responsive layout built entirely by choosing the right unit for the job: VH for viewports, REM for typography, % for grids, EM for proportional components, and PX for fixed assets.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Responsive Layout System.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Fluid Responsive Layout System — generated component */
:root {{
    /* Base typography setup for REM calculations */
    font-size: 16px; 
    
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
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
    overflow-x: hidden;
}}

/* 
  1. VIEWPORT UNITS (vh, vw)
  Used for macro-layout. 100vh ensures the hero section takes up exactly 
  100% of the screen height, regardless of the device.
*/
.hero {{
    min-height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem 5%; /* Fallback padding */
    position: relative;
}}

/* 
  2. REM UNITS (Root EM)
  Used for typography. 1rem = 16px (based on root). 
  Scales perfectly if user zooms or changes default browser font size.
*/
.hero h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem); /* Responsive typography using REM and VW */
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1rem;
    max-width: 800px;
}}

.hero p {{
    font-size: 1.125rem; /* 18px equivalent */
    color: var(--text-muted);
    max-width: 600px;
    margin-bottom: 3rem;
}}

/* 
  3. PERCENTAGES (%)
  Used for fluid containers and grid layouts relative to their parent.
*/
.features-grid {{
    width: 90%; /* Fluid width relative to screen */
    max-width: 1200px;
    display: flex;
    flex-wrap: wrap;
    gap: 2%; /* Percentage gap */
    justify-content: center;
}}

/* 
  4. EM UNITS (Element EM)
  Used for proportional scaling inside components. 
  If you change the .card font-size, the padding and gap scale automatically.
*/
.card {{
    background: var(--card-bg);
    width: 31%; /* Percentage layout */
    min-width: 300px;
    margin-bottom: 2rem;
    
    font-size: 1rem; /* Base size for this component */
    padding: 2.5em; /* 2.5 x 16px = 40px padding. Relative to card font-size */
    
    border-radius: 12px;
    border: 1px solid var(--border);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}}

/* 
  5. PX UNITS (Pixels)
  Used STRICTLY for elements that must NOT distort or change size, 
  like borders and branded icons.
*/
.card-icon {{
    width: 48px;  /* Absolute unit */
    height: 48px; /* Absolute unit */
    background: rgba(139, 92, 246, 0.1);
    color: var(--accent);
    border-radius: 8px; /* Fixed radius */
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5em; /* EM for relative spacing */
}}

.card-icon svg {{
    width: 24px; /* Fixed icon size */
    height: 24px;
}}

.card h2 {{
    font-size: 1.5rem; /* REM */
    margin-bottom: 0.75em; /* EM relative to h2 font size */
}}

.card p {{
    font-size: 1rem;
    color: var(--text-muted);
}}

/* Badge uses EM to scale perfectly with text */
.badge {{
    display: inline-block;
    padding: 0.4em 0.8em;
    background: var(--accent);
    color: white;
    font-size: 0.875rem;
    font-weight: 600;
    border-radius: 100px;
    margin-bottom: 1.5em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Mobile adjustments */
@media (max-width: 900px) {{
    .card {{
        width: 48%;
    }}
}}

@media (max-width: 600px) {{
    .card {{
        width: 100%;
    }}
    .hero {{
        padding-top: 4rem;
        padding-bottom: 4rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero">
        <span class="badge">Responsive Design</span>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        
        <div class="features-grid">
            <!-- Card 1: Demonstrates REM, EM, and PX -->
            <div class="card">
                <div class="card-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
                </div>
                <h2>Absolute Scale (PX)</h2>
                <p>The icon above is exactly 48px by 48px. Pixels are perfect for logos and icons that should never squish or stretch.</p>
            </div>

            <!-- Card 2 -->
            <div class="card">
                <div class="card-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
                </div>
                <h2>Relative Text (REM)</h2>
                <p>This text uses REM units. It reads the browser's default font size to ensure maximum accessibility for all users.</p>
            </div>

            <!-- Card 3 -->
            <div class="card">
                <div class="card-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                </div>
                <h2>Proportional (EM & %)</h2>
                <p>This card takes up 30% of its parent container. Its internal padding uses EM, so it scales if the card's font size changes.</p>
            </div>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Helper script to dynamically show the viewport size to demonstrate fluid resizing
document.addEventListener('DOMContentLoaded', () => {{
    const hero = document.querySelector('.hero');
    
    // Create an indicator element
    const indicator = document.createElement('div');
    indicator.style.position = 'absolute';
    indicator.style.top = '1rem';
    indicator.style.right = '1rem';
    indicator.style.background = 'rgba(0,0,0,0.5)';
    indicator.style.color = '#fff';
    indicator.style.padding = '0.5rem 1rem';
    indicator.style.borderRadius = '20px';
    indicator.style.fontSize = '0.875rem';
    indicator.style.fontFamily = 'monospace';
    indicator.style.backdropFilter = 'blur(4px)';
    indicator.style.zIndex = '100';
    
    hero.appendChild(indicator);

    function updateSize() {{
        indicator.textContent = `Viewport: ${{window.innerWidth}}px × ${{window.innerHeight}}px`;
    }}

    window.addEventListener('resize', updateSize);
    updateSize();
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
