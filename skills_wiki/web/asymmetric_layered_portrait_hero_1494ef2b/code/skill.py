def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "This layout uses CSS flexbox and dual-layered backgrounds to create depth. The text floats above a central subject anchored to the bottom of the viewport.",
    color_scheme: str = "dark",        
    accent_color: str = "#c13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Layered Portrait Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1a253a"
        pattern_color = "#22304a"
        text_color = "#ffffff"
        accent_hover = "#9e2f6e"
        silhouette_fill = "%230d1424" # URL encoded #0d1424
    else:
        bg_color = "#f4f6f9"
        pattern_color = "#e2e8f0"
        text_color = "#1a253a"
        accent_hover = "#a1276a"
        silhouette_fill = "%23cbd5e1" # URL encoded #cbd5e1

    # Generate a robust SVG silhouette placeholder as a data URI to simulate the portrait
    svg_portrait = f"data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath fill='{silhouette_fill}' d='M100 500c0-100 50-150 100-150s100 50 100 150H100zM200 100a80 80 0 1 0 0 160 80 80 0 0 0 0-160z'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Asymmetric Layered Portrait Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --pattern: {pattern_color};
    --text: {text_color};
    --accent: {accent_color};
    --accent-hover: {accent_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Optional grid background fallback if not doing the hero container */
}}

.hero-main {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    background-color: var(--bg);
    
    /* Dual Background Layering: Portrait on top, dotted pattern behind */
    background-image: 
        url("{svg_portrait}"),
        radial-gradient(var(--pattern) 3px, transparent 3.5px);
        
    /* Scale portrait to 70% of container height, pattern repeats every 30px */
    background-size: 
        70%, 
        30px 30px;
        
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4vw;
    gap: 2rem;
    overflow: hidden;
}}

/* Ensure text content stays above background images */
.main-intro, .main-quotes {{
    z-index: 2;
    flex: 1;
    max-width: 400px;
}}

/* Left Column Styling */
.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 96px); /* Fluid scaling based on tutorial's 96px */
    line-height: 1.05;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-bottom: 2rem;
}}

.main-intro a.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #fff;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 18px;
    padding: 12px 24px;
    transition: background-color 0.2s ease;
}}

.main-intro a.cta-button:hover {{
    background-color: var(--accent-hover);
}}

/* Right Column Styling */
.main-quotes {{
    /* Push the quotes down slightly as per tutorial design */
    padding-top: 10vh;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 18px;
    line-height: 30px;
    background: rgba(0,0,0,0.2); /* Slight readable backdrop for contrast */
    padding-top: 10px;
    padding-bottom: 10px;
    border-radius: 0 8px 8px 0;
    backdrop-filter: blur(4px);
}}

/* Asymmetric Offset */
.main-quotes p:nth-child(2) {{
    margin-left: 80px;
}}

/* Author styling */
.quote-author {{
    display: block;
    margin-top: 10px;
    font-weight: bold;
    color: var(--accent);
}}

@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: center;
        background-position: bottom 20% center, center;
        background-size: 50%, 30px 30px;
        height: auto;
        min-height: var(--height);
    }}
    .main-intro, .main-quotes {{
        max-width: 100%;
        text-align: center;
    }}
    .main-quotes p {{
        border-left: none;
        border-bottom: 4px solid var(--accent);
        border-radius: 8px 8px 0 0;
    }}
    .main-quotes p:nth-child(2) {{
        margin-left: 0;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-main">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>

        <div class="main-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>
                "An investment in knowledge pays the best interest."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Optional: Add subtle parallax to the background pattern on mouse move
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-main');
    
    hero.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        // Slightly shift the background pattern, keeping the portrait centered
        // Format: portrait X Y, pattern X Y
        hero.style.backgroundPosition = `bottom center, calc(50% + ${x * 10}px) calc(50% + ${y * 10}px)`;
    });
});
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
