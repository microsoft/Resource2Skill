def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Split-Panel Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base64 SVGs to simulate the layered background imagery
    # 1. A placeholder cutout silhouette portrait (placed bottom center)
    svg_portrait = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cpath d='M200,800 C200,500 250,450 400,450 C550,450 600,500 600,800 Z' fill='rgba(0,0,0,0.3)'/%3E%3Ccircle cx='400' cy='320' r='110' fill='rgba(0,0,0,0.3)'/%3E%3C/svg%3E"
    
    # 2. A placeholder repeating dot pattern (placed over the whole background)
    svg_pattern = "data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='20' cy='20' r='2' fill='rgba(255,255,255,0.04)'/%3E%3C/svg%3E"

    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
    else:
        bg_color = "#F0F4F8"
        text_color = "#111827"
        svg_pattern = "data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='20' cy='20' r='2' fill='rgba(0,0,0,0.06)'/%3E%3C/svg%3E"
        svg_portrait = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cpath d='M200,800 C200,500 250,450 400,450 C550,450 600,500 600,800 Z' fill='rgba(0,0,0,0.08)'/%3E%3Ccircle cx='400' cy='320' r='110' fill='rgba(0,0,0,0.08)'/%3E%3C/svg%3E"

    css = f"""/* Layered Split-Panel Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
}}

.hero-section {{
    /* Using component width/height as a preview container context */
    width: 100%;
    min-height: {height_px}px;
    
    /* Core Visual Layering: Portrait on top, Pattern on bottom */
    background-image: url("{svg_portrait}"), url("{svg_pattern}");
    background-position: bottom center, top left;
    background-repeat: no-repeat, repeat;
    background-size: auto 90%, auto;
    
    /* Layout Framing: Pushing content to the sides */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 8vw;
}}

/* Left Column: Intro */
.main-intro {{
    flex: 0 1 450px;
    z-index: 2; /* Keeps text above imagery */
    padding-bottom: 5vh;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2rem;
    opacity: 0.9;
}}

/* CTA Button */
.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #FFFFFF;
    text-decoration: none;
    padding: 12px 32px;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    transition: filter 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    flex: 0 1 350px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

/* Blockquote Style Extraction */
.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
}}

.quote-block p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 0.5rem;
}}

.quote-block .author {{
    font-size: 0.9rem;
    opacity: 0.7;
    font-style: italic;
}}

/* Responsive Breakpoint */
@media (max-width: 900px) {{
    .hero-section {{
        flex-direction: column;
        justify-content: center;
        gap: 4rem;
        padding: 6rem 5vw;
        text-align: center;
        
        /* Fade portrait out to avoid unreadable text overlay on small screens */
        background-size: auto 40%, auto;
        background-position: bottom center, top left;
    }}
    
    .quote-block {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 1rem;
        text-align: left;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layered Split-Panel Hero</title>
    <!-- Google Fonts import per the original pattern -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-section">
        
        <!-- Left Flank: Main Introduction -->
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#work" class="cta-button">My Work</a>
        </section>

        <!-- Right Flank: Auxiliary Text / Quotes -->
        <section class="main-quotes">
            <div class="quote-block">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="author">- Dr. Seuss</span>
            </div>
            
            <div class="quote-block">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <span class="author">- Benjamin Franklin</span>
            </div>
        </section>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript is required for this purely structural/visual CSS layout pattern.
// Hover states and layouts are fully managed via the CSS rules.

console.log("Layered Split-Panel Hero Section successfully loaded.");
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
