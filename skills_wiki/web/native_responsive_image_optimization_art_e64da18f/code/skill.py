def create_component(
    output_dir: str,
    title_text: str = "Responsive Images Demo",
    body_text: str = "Resize your browser window to see the browser intelligently swap image sources based on viewport width.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1000,
    height_px: int = 1200,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f8fafc"
        muted_text = "#94a3b8"
        border_color = "#334155"
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        muted_text = "#64748b"
        border_color = "#e2e8f0"

    css = f"""/* Native Responsive Image Component */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_color};
    --text-muted: {muted_text};
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
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.6;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

.container {{
    max-width: {width_px}px;
    width: 100%;
}}

header {{
    margin-bottom: 3rem;
    text-align: center;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.description {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
}}

.demo-section {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}}

.demo-section h2 {{
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.demo-section p {{
    color: var(--text-muted);
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
}}

/* The critical CSS for responsive images */
.responsive-img {{
    width: 100%;
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    display: block;
    /* Optional visual flair */
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}}

.responsive-img:hover {{
    transform: scale(1.01);
}}

code {{
    background: rgba(128, 128, 128, 0.15);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9em;
    color: var(--accent);
}}
"""

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
    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p class="description">{body_text}</p>
        </header>

        <!-- Example 1: Resolution Switching -->
        <section class="demo-section">
            <h2>1. Resolution Switching <code>(srcset & sizes)</code></h2>
            <p>Provides the browser with multiple resolutions of the same image. Open DevTools, disable cache, and resize the window to see the browser fetch the appropriately sized file.</p>
            
            <!-- 
              Logic: 
              - Up to 600px viewport, expect image to take up ~100vw. Browser picks the 480w image.
              - Up to 1024px viewport, expect image to be ~800px wide. Browser picks the 800w image.
              - Larger viewports, image is constrained by max-width, use the 1200w image.
            -->
            <img class="responsive-img"
                 src="https://placehold.co/1200x600/10b981/ffffff?text=Desktop+(1200w)" 
                 srcset="
                    https://placehold.co/480x320/ef4444/ffffff?text=Mobile+(480w) 480w,
                    https://placehold.co/800x500/3b82f6/ffffff?text=Tablet+(800w) 800w,
                    https://placehold.co/1200x600/10b981/ffffff?text=Desktop+(1200w) 1200w
                 "
                 sizes="(max-width: 600px) 100vw, (max-width: 1024px) 800px, 1000px"
                 alt="A placeholder demonstrating resolution switching">
        </section>

        <!-- Example 2: Art Direction -->
        <section class="demo-section">
            <h2>2. Art Direction <code>(&lt;picture&gt;)</code></h2>
            <p>Forces the browser to use entirely different image crops based on strict media queries. Notice how the aspect ratio completely changes below 768px.</p>
            
            <!-- 
              Logic:
              - Below 768px, force load the tall portrait crop.
              - 768px and above, load the wide landscape crop.
            -->
            <picture>
                <source media="(max-width: 768px)" srcset="https://placehold.co/600x800/8b5cf6/ffffff?text=Portrait+Crop+(Mobile)">
                <source media="(min-width: 769px)" srcset="https://placehold.co/1200x400/f59e0b/ffffff?text=Landscape+Crop+(Desktop)">
                
                <!-- Fallback for older browsers -->
                <img class="responsive-img" 
                     src="https://placehold.co/1200x400/f59e0b/ffffff?text=Landscape+Crop+(Desktop)" 
                     alt="A placeholder demonstrating art direction with different aspect ratios">
            </picture>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Native Responsive Image Component
// No JavaScript is required for responsive images! 
// The browser's HTML parser and rendering engine handle srcset, sizes, and picture logic automatically.

document.addEventListener('DOMContentLoaded', () => {
    console.log("Responsive images initialized. Try resizing your browser window with DevTools open (Cache Disabled) to observe network requests.");
});
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
