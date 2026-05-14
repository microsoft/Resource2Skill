def create_component(
    output_dir: str,
    title_text: str = "Responsive Art Direction",
    body_text: str = "Resize your browser window to see the image adapt. The browser natively switches between different crops and resolutions based on the viewport width.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Picture Element visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1a2235"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        
    # Strip '#' for the placehold.co URL generation
    surface_hex = surface_color.replace("#", "")
    accent_hex = accent_color.replace("#", "")

    # === CSS ===
    css = f"""/* Responsive Art Direction — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    max-width: var(--max-width);
    width: 100%;
    background: var(--surface);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}}

.title {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text);
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    color: var(--text);
    opacity: 0.8;
    max-width: 800px;
}}

.hero-figure {{
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    background: var(--bg);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

/* The critical CSS rule for fluid responsive images */
.responsive-image {{
    display: block;
    width: 100%;
    height: auto;
    object-fit: cover;
}}

figcaption {{
    padding: 1.25rem;
    text-align: center;
    font-size: 0.875rem;
    background: var(--bg);
    color: var(--text);
    opacity: 0.7;
}}

code {{
    background: rgba(128, 128, 128, 0.15);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: 'Menlo', 'Monaco', monospace;
    color: var(--accent);
}}

/* Dynamic Viewport Badge */
.size-display {{
    position: fixed;
    top: 24px;
    right: 24px;
    background: var(--surface);
    color: var(--text);
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.875rem;
    z-index: 1000;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

.size-display span {{
    color: var(--accent);
    font-weight: 700;
}}

@media (max-width: 600px) {{
    body {{ padding: 1rem; }}
    .container {{ padding: 1.5rem; }}
    .title {{ font-size: 1.75rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <figure class="hero-figure">
            <!-- 
              The <picture> element evaluates <source> tags from top to bottom. 
              The first media query that returns true is selected.
            -->
            <picture>
                <!-- Mobile: Art directed crop (1:1 Square) with Retina display support -->
                <source media="(max-width: 500px)" 
                        srcset="https://placehold.co/500x500/{surface_hex}/{accent_hex}?text=Mobile+Crop+(Square)+1x 1x, 
                                https://placehold.co/1000x1000/{surface_hex}/{accent_hex}?text=Mobile+Retina+(Square)+2x 2x">
                
                <!-- Tablet: Medium size (3:2 Aspect Ratio) -->
                <source media="(max-width: 900px)" 
                        srcset="https://placehold.co/900x600/{surface_hex}/{accent_hex}?text=Tablet+View+(3:2)">
                        
                <!-- Desktop: Wide landscape (2:1 Aspect Ratio) -->
                <source media="(min-width: 901px)" 
                        srcset="https://placehold.co/1600x800/{surface_hex}/{accent_hex}?text=Desktop+View+(2:1)">
                        
                <!-- Fallback: Standard IMG tag. This is required and also acts as the baseline default -->
                <img src="https://placehold.co/1600x800/{surface_hex}/{accent_hex}?text=Desktop+View+(2:1)" 
                     alt="A dynamically responsive demonstration placeholder" 
                     class="responsive-image"
                     loading="lazy">
            </picture>
            <figcaption>
                The image above physically changes its source file as you scale the window past 900px and 500px boundaries.
            </figcaption>
        </figure>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Art Direction — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    // Create a dynamic badge to show the user the current window width
    // This helps visualize exactly when the <picture> element switches sources
    const sizeDisplay = document.createElement('div');
    sizeDisplay.className = 'size-display';
    document.body.appendChild(sizeDisplay);

    function updateSize() {{
        sizeDisplay.innerHTML = `Viewport width: <span>${{window.innerWidth}}px</span>`;
    }}
    
    // Listen for resize events
    window.addEventListener('resize', () => {{
        // Use requestAnimationFrame to throttle resize events slightly for performance
        window.requestAnimationFrame(updateSize);
    }});
    
    // Initial call
    updateSize();
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
