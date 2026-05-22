def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO<br>MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split Hero with Multi-Background Centerpiece' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#1a253a"
        pattern_color = "rgba(255, 255, 255, 0.05)"
        text_color = "#ffffff"
        text_muted = "#a0aec0"
        silhouette_color = "%230f172a" # URL encoded dark color
    else:
        bg_color = "#f8f9fa"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        text_color = "#1a202c"
        text_muted = "#4a5568"
        silhouette_color = "%23e2e8f0" # URL encoded light color

    # Generating a faux portrait silhouette using SVG data URI so the component is fully self-contained.
    portrait_svg = f"data:image/svg+xml;utf8,<svg viewBox='0 0 200 250' xmlns='http://www.w3.org/2000/svg'><path d='M100 110 C 130 110, 145 80, 145 50 C 145 20, 130 10, 100 10 C 70 10, 55 20, 55 50 C 55 80, 70 110, 100 110 Z M 20 250 C 20 180, 50 140, 100 140 C 150 140, 180 180, 180 250 Z' fill='{silhouette_color}'/></svg>"

    css = f"""/* Split Hero with Multi-Background Centerpiece */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --accent: {accent_color};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --pattern-color: {pattern_color};
}}

body {{
    font-family: 'Roboto', -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.hero-container {{
    position: relative;
    width: {width_px}px;
    max-width: 100vw;
    height: {height_px}px;
    
    /* MULTIPLE BACKGROUNDS: Top layer is silhouette, Bottom layer is dotted pattern */
    background-image: 
        url("{portrait_svg}"),
        radial-gradient(var(--pattern-color) 2px, transparent 2px);
    background-size: 70vh, 30px 30px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, 0 0;
    
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 8vh; /* Shift content slightly up */
}}

/* LEFT SIDE - Intro */
.main-intro {{
    position: relative;
    right: 15vw; /* Push away from the center portrait */
    max-width: 400px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: 64px;
    line-height: 1.1;
    margin-bottom: 20px;
    text-transform: uppercase;
    font-weight: 900;
}}

.main-intro p {{
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 30px;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* RIGHT SIDE - Quotes */
.main-quotes {{
    position: relative;
    left: 8vw; /* Push away from the center portrait */
    max-width: 350px;
    z-index: 10;
}}

.main-quotes .quote-box {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
}}

/* Stagger the layout for organic feel */
.main-quotes .quote-box:nth-child(2) {{
    margin-left: 80px;
}}

.quote-box p {{
    font-size: 15px;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 10px;
}}

.quote-box span.author {{
    display: block;
    font-size: 14px;
    font-weight: bold;
    color: var(--text-muted);
}}

/* Responsive adjustments */
@media (max-width: 1024px) {{
    .hero-container {{
        flex-direction: column;
        background-size: 50vh, 30px 30px;
        background-position: bottom -10vh center, 0 0;
        text-align: center;
    }}
    
    .main-intro, .main-quotes {{
        right: auto;
        left: auto;
        margin: 20px;
    }}
    
    .main-quotes .quote-box {{
        text-align: left;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Hero Pattern</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>

        <div class="main-quotes">
            <div class="quote-box">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="author">- Dr. Seuss</span>
            </div>
            <div class="quote-box">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <span class="author">- Benjamin Franklin</span>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS layout mechanism driven. Interactive behaviors can be initialized here if needed.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Split Hero Pattern initialized.');
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
