def create_component(
    output_dir: str,
    title_text: str = "WELCOME\nTO MY FIRST\nWEBSITE",
    body_text: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"\n\n- Dr. Seuss",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Typography Layered Hero Section.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import base64

    os.makedirs(output_dir, exist_ok=True)

    # Format text for HTML
    title_html = title_text.replace('\n', '<br>')
    body_html = body_text.replace('\n', '<br>')

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_fill = "#ffffff"
        pattern_opacity = "0.05"
        portrait_fill = "#ffffff"
    else:
        bg_color = "#F4F7F6"
        text_color = "#111827"
        pattern_fill = "#000000"
        pattern_opacity = "0.04"
        portrait_fill = "#000000"

    # Base64 encode SVGs to avoid CORS/loading issues and allow dynamic theme colors
    def get_b64_svg(svg_string):
        b64 = base64.b64encode(svg_string.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{b64}"

    # Repeating background pattern
    pattern_raw = f"""<svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'><g fill='none' fill-rule='evenodd'><g fill='{pattern_fill}' fill-opacity='{pattern_opacity}'><path d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/></g></g></svg>"""
    
    # Transparent portrait silhouette placeholder
    portrait_raw = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'><path fill='{portrait_fill}' opacity='0.12' d='M100,40 A45,45 0 1,0 100,130 A45,45 0 1,0 100,40 Z M30,300 C30,170 170,170 170,300 Z' /></svg>"""

    pattern_url = get_b64_svg(pattern_raw)
    portrait_url = get_b64_svg(portrait_raw)

    # === CSS ===
    css = f"""/* Split-Typography Layered Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-container {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    max-height: 100vh;
    background-color: var(--bg-color);
    position: relative;
    overflow: hidden;
    
    /* 
       Multiple backgrounds:
       1st image (portrait) sits on top, sized to 85% height of the container, pinned bottom center.
       2nd image (pattern) sits behind, repeating across the container.
    */
    background-image: 
        url("{portrait_url}"),
        url("{pattern_url}");
    background-size: auto 85%, auto;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, 0 0;
}}

.hero-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;
    padding: 0 8%;
    /* Ensures text remains layered above the background images */
    position: relative;
    z-index: 10;
}}

.main-intro {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 45%;
    /* JS animation hook */
    opacity: 0; 
}}

.title {{
    font-size: clamp(2.5rem, 5.5vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    color: var(--text-color);
    margin-bottom: 2rem;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 1rem 2.5rem;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 1rem;
    letter-spacing: 0.05em;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

.main-quotes {{
    max-width: 32%;
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
    /* JS animation hook */
    opacity: 0;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-color);
    opacity: 0.85;
}}

/* Responsive Graceful Degradation */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        gap: 3rem;
        text-align: center;
    }}
    .main-intro, .main-quotes {{
        max-width: 90%;
        align-items: center;
    }}
    .main-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 1.5rem;
    }}
    .hero-container {{
        background-size: auto 60%, auto;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        <div class="hero-content">
            
            <section class="main-intro">
                <h1 class="title">{title_html}</h1>
                <a href="#work" class="btn">My Work</a>
            </section>

            <section class="main-quotes">
                <p class="body-text">{body_html}</p>
            </section>

        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Split-Typography Entrance Animation
document.addEventListener('DOMContentLoaded', () => {{
    const introBlock = document.querySelector('.main-intro');
    const quoteBlock = document.querySelector('.main-quotes');

    // Prepare initial transformed states
    introBlock.style.transform = 'translateX(-40px)';
    quoteBlock.style.transform = 'translateX(40px)';

    // Define transition properties
    const transitionRule = 'opacity 0.8s cubic-bezier(0.25, 1, 0.5, 1), transform 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
    
    introBlock.style.transition = transitionRule;
    quoteBlock.style.transition = transitionRule;
    quoteBlock.style.transitionDelay = '0.15s'; // Stagger the entrance

    // Trigger animations
    requestAnimationFrame(() => {{
        requestAnimationFrame(() => {{
            introBlock.style.opacity = '1';
            introBlock.style.transform = 'translateX(0)';
            
            quoteBlock.style.opacity = '1';
            quoteBlock.style.transform = 'translateX(0)';
        }});
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
