def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "I'm building my first portfolio. This layout frames a central subject using flexbox and multi-layered CSS backgrounds to create depth and editorial style.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Central Subject Split-Content Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        quote_text = "#e0e5ec"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        silhouette_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f6f9"
        text_color = "#111827"
        quote_text = "#4b5563"
        pattern_color = "rgba(0, 0, 0, 0.03)"
        silhouette_color = "rgba(0, 0, 0, 0.1)"

    # SVG Data URI for a generic person silhouette placeholder
    silhouette_svg = f"""data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><path fill="{silhouette_color.replace('#', '%23')}" d="M100 130c27.6 0 50-22.4 50-50S127.6 30 100 30 50 52.4 50 80s22.4 50 50 50zm-60 140v-20c0-33.1 26.9-60 60-60h0c33.1 0 60 26.9 60 60v20H40z"/></svg>"""

    # === CSS ===
    css = f"""/* Central Subject Split-Content Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text};
    --accent-color: {accent_color};
    --accent-hover: {accent_color}dd;
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
    /* Emulate a full screen view based on provided dimensions */
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-main {{
    /* Layout */
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    position: relative;
    
    /* Layered Background: Subject Placeholder on top of Geometric Pattern */
    background-image: 
        url('{silhouette_svg}'),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color}),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color});
    background-size: 
        70vh, 
        60px 60px, 
        60px 60px;
    background-position: 
        bottom center, 
        0 0, 
        30px 30px;
    background-repeat: 
        no-repeat, 
        repeat, 
        repeat;
}}

/* --- Left Side: Intro --- */
.main-intro {{
    /* Core technique: nudge left to dodge the central subject */
    position: relative;
    right: 12vw;
    z-index: 2;
    max-width: 450px;
}}

.main-intro h1 {{
    /* Responsive typography scaling while preserving the massive feel */
    font-size: clamp(3rem, 6vw, 96px);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-bottom: 30px;
}}

.main-intro a {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background-color 0.2s ease;
}}

.main-intro a:hover {{
    background-color: var(--accent-hover);
}}

/* --- Right Side: Quotes --- */
.main-quotes {{
    /* Core technique: nudge right to dodge central subject */
    position: relative;
    left: 8vw;
    padding-bottom: 8vh; /* Slight vertical offset */
    z-index: 2;
    max-width: 350px;
    
    /* Left accent bar */
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
}}

.main-quotes p {{
    font-size: 16px;
    line-height: 26px;
    color: var(--quote-color);
    margin-bottom: 24px;
    font-style: italic;
}}

/* Editorial shift for the second paragraph */
.main-quotes p:nth-child(2) {{
    margin-left: 60px;
}}

.main-quotes strong {{
    display: block;
    font-style: normal;
    margin-top: 8px;
    font-size: 14px;
    color: var(--text-color);
}}

/* Basic Responsive Fallback for smaller screens */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        text-align: center;
        padding: 40px;
        background-position: bottom center, 0 0, 30px 30px;
        background-size: 40vh, 60px 60px, 60px 60px;
    }}
    
    .main-intro, .main-quotes {{
        position: static;
        right: auto;
        left: auto;
        max-width: 100%;
    }}
    
    .main-quotes {{
        margin-top: 50vh; /* Make room for subject */
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 20px;
        padding-bottom: 0;
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
    <title>Hero Layout Pattern</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-main">
        
        <div class="main-intro">
            <h1>{title_text.replace(chr(10), '<br>')}</h1>
            <p>{body_text}</p>
            <a href="#">My Work</a>
        </div>

        <div class="main-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <strong>- Dr. Seuss</strong>
            </p>
            <p>
                "For the best return on your money, pour your purse into your head."
                <strong>- Benjamin Franklin</strong>
            </p>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JS required for this pure CSS layout technique.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Central Subject Split-Content Hero initialized.");
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
