def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "A deep dive into web design, extracting core visual patterns and building reusable components for the modern web.",
    quote_1: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"",
    quote_1_author: str = "- Dr. Seuss",
    quote_2: str = "\"For the best return on your money, pour your purse into your head.\"",
    quote_2_author: str = "- Benjamin Franklin",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Background Split Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_color = "#ffffff"
        silhouette_color = "#212f4a" # Slightly lighter than bg
        pattern_color = "ffffff"
        pattern_opacity = "0.03"
    else:
        bg_color = "#f0f4f8"
        text_color = "#111827"
        silhouette_color = "#e2e8f0"
        pattern_color = "000000"
        pattern_opacity = "0.03"

    # URL encode SVG colors for data URIs
    sil_enc = urllib.parse.quote(silhouette_color)

    # Inline SVG for the geometric background pattern
    pattern_svg = f"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23{pattern_color}' fill-opacity='{pattern_opacity}' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E"
    
    # Inline SVG acting as the generic cutout person/subject
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M50,600 C50,400 120,320 200,320 C280,320 350,400 350,600 Z' fill='{sil_enc}'/%3E%3Ccircle cx='200' cy='200' r='90' fill='{sil_enc}'/%3E%3C/svg%3E"

    css = f"""/* Dual-Background Split Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;800&display=swap');

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
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    min-height: 600px;
    position: relative;
    overflow: hidden;
    
    /* Center the flex layout */
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* Layered Backgrounds: Subject (Top), Pattern (Bottom) */
    background-color: var(--bg-color);
    background-image: url("{portrait_svg}"), url("{pattern_svg}");
    background-size: 75vh, 40px 40px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 12vw; /* Push outward from center */
    max-width: 450px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(48px, 5.5vw, 96px);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-weight: 800;
    text-transform: uppercase;
    margin-top: 30px;
    letter-spacing: 1px;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 12vw; /* Push outward from center */
    max-width: 400px;
    z-index: 10;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.8;
}}

/* Stagger the second quote */
.main-quotes p:nth-child(2) {{
    margin-left: 100px;
}}

/* Responsive Adjustments */
@media (max-width: 1100px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: center;
        background-position: bottom right -10vw, center;
        padding: 40px;
    }}
    
    .main-intro, .main-quotes {{
        position: static;
        max-width: 600px;
        width: 100%;
    }}
    
    .main-intro {{
        margin-bottom: 60px;
    }}
    
    .main-quotes p:nth-child(2) {{
        margin-left: 40px; /* Reduce stagger on smaller screens */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        
        <!-- Left Content -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <!-- Right Content -->
        <div class="main-quotes">
            <p>{quote_1}<br><br>{quote_1_author}</p>
            <p>{quote_2}<br><br>{quote_2_author}</p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for the core visual layout and relative offset mechanics.
console.log("Hero layout loaded successfully.");
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
