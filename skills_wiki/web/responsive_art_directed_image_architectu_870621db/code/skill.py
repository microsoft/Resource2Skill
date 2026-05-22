def create_component(
    output_dir: str,
    title_text: str = "Responsive Image Architecture",
    body_text: str = "Resize your browser window to see the browser dynamically swap image assets based on viewport width, layout size, and pixel density.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing Responsive Images with <picture>, srcset, and sizes.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "#1e293b"
        border_color = "#334155"
        ph_bg = "1e293b"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        ph_bg = "e2e8f0"

    ph_txt = accent_color.lstrip('#')

    # CSS
    css = f"""/* Responsive Images Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    padding-bottom: 6rem; /* space for debug panel */
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.section-title {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}}

/* Base responsive image styling */
img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    display: block;
}}

/* Layout for Pattern 2 (sizes example) */
.gallery-grid {{
    display: grid;
    grid-template-columns: 1fr; /* 100vw context */
    gap: 1.5rem;
}}

@media (min-width: 600px) {{
    .gallery-grid {{
        grid-template-columns: repeat(2, 1fr); /* 50vw context */
    }}
}}

@media (min-width: 1024px) {{
    .gallery-grid {{
        grid-template-columns: repeat(3, 1fr); /* 33vw context */
    }}
}}

/* Floating Debug Panel */
.debug-panel {{
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(8px);
    color: #fff;
    padding: 1rem 1.5rem;
    border-radius: 50px;
    font-family: monospace;
    font-size: 0.9rem;
    display: flex;
    gap: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    z-index: 100;
    border: 1px solid var(--accent);
}}

.debug-item span {{
    color: var(--accent);
    font-weight: bold;
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Pattern 1: Art Direction with <picture> -->
        <section>
            <h2 class="section-title">Pattern 1: Art Direction (The &lt;picture&gt; element)</h2>
            <p style="margin-bottom: 1rem; opacity: 0.8;">Forces a specific aspect ratio/crop based on device width.</p>
            <div class="card">
                <picture>
                    <!-- Desktop: Ultra-wide crop -->
                    <source media="(min-width: 1024px)" srcset="https://placehold.co/1200x300/{ph_bg}/{ph_txt}.png?text=Desktop+Crop+(21:9)">
                    
                    <!-- Tablet: Standard landscape crop -->
                    <source media="(min-width: 600px)" srcset="https://placehold.co/800x500/{ph_bg}/{ph_txt}.png?text=Tablet+Crop+(16:10)">
                    
                    <!-- Mobile / Fallback: Portrait crop -->
                    <img id="hero-img" src="https://placehold.co/600x800/{ph_bg}/{ph_txt}.png?text=Mobile+Crop+(3:4)" alt="Art directed hero image">
                </picture>
            </div>
        </section>

        <!-- Pattern 2: Resolution Switching with srcset & sizes -->
        <section>
            <h2 class="section-title">Pattern 2: Resolution Switching (srcset + sizes)</h2>
            <p style="margin-bottom: 1rem; opacity: 0.8;">The browser calculates CSS layout width and screen density, automatically picking the most efficient file size.</p>
            <div class="card gallery-grid">
                <!-- 
                  The 'sizes' attribute perfectly matches the CSS Grid rules:
                  < 600px: 1 column (takes up ~100vw)
                  600px - 1024px: 2 columns (takes up ~50vw)
                  > 1024px: 3 columns (takes up ~33vw)
                -->
                <img id="fluid-img" 
                     src="https://placehold.co/400x300/{ph_bg}/{ph_txt}.png?text=Fallback+400w" 
                     srcset="
                        https://placehold.co/400x300/{ph_bg}/{ph_txt}.png?text=File:+400w 400w,
                        https://placehold.co/800x600/{ph_bg}/{ph_txt}.png?text=File:+800w 800w,
                        https://placehold.co/1200x900/{ph_bg}/{ph_txt}.png?text=File:+1200w 1200w,
                        https://placehold.co/1600x1200/{ph_bg}/{ph_txt}.png?text=File:+1600w 1600w
                     "
                     sizes="(max-width: 599px) 100vw, (max-width: 1023px) 50vw, 33vw"
                     alt="Fluid gallery image"
                     loading="lazy">
                
                <img src="https://placehold.co/800x600/{ph_bg}/{ph_txt}.png?text=Static+Dummy" alt="Dummy">
                <img src="https://placehold.co/800x600/{ph_bg}/{ph_txt}.png?text=Static+Dummy" alt="Dummy">
            </div>
        </section>
    </div>

    <!-- Debug UI to visualize the native browser behavior -->
    <div class="debug-panel">
        <div class="debug-item">Viewport: <span id="out-vw">--</span></div>
        <div class="debug-item">Hero File: <span id="out-hero">--</span></div>
        <div class="debug-item">Gallery File: <span id="out-fluid">--</span></div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript
    js = f"""// JS is ONLY used here to visualize the browser's native internal choices.
// The actual image swapping is happening 100% natively in HTML/C++ engine.

document.addEventListener('DOMContentLoaded', () => {{
    const heroImg = document.getElementById('hero-img');
    const fluidImg = document.getElementById('fluid-img');
    
    const outVw = document.getElementById('out-vw');
    const outHero = document.getElementById('out-hero');
    const outFluid = document.getElementById('out-fluid');

    function extractDimensions(url) {{
        if (!url) return 'Unknown';
        const match = url.match(/[0-9]+x[0-9]+/);
        return match ? match[0] : 'Fallback';
    }}

    function updateDebugPanel() {{
        outVw.textContent = window.innerWidth + 'px';
        
        // currentSrc contains the URL of the image the browser ACTUALLY downloaded
        outHero.textContent = extractDimensions(heroImg.currentSrc);
        outFluid.textContent = extractDimensions(fluidImg.currentSrc);
    }}

    // Update on load and resize
    window.addEventListener('resize', updateDebugPanel);
    
    // Images might change currentSrc after load based on network/caching
    heroImg.addEventListener('load', updateDebugPanel);
    fluidImg.addEventListener('load', updateDebugPanel);
    
    // Initial call
    updateDebugPanel();
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
