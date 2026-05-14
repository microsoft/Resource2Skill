def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split Hero with Centered Silhouette effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.04)"
        quote_text_color = "rgba(255, 255, 255, 0.85)"
    else:
        bg_color = "#F0F2F5"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.04)"
        quote_text_color = "rgba(26, 37, 58, 0.85)"

    # An SVG silhouette to substitute the portrait, base64/URL encoded for CSS
    svg_silhouette = "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath fill='{fill_color}' fill-opacity='0.08' d='M200 150c-30 0-55-25-55-55s25-55 55-55 55 25 55 55-25 55-55 55zm-80 50c-30 0-40 20-40 50v350h240V250c0-30-10-50-40-50h-80z'/%3E%3C/svg%3E".format(
        fill_color="%23FFFFFF" if color_scheme == "dark" else "%23000000"
    )

    # === CSS ===
    css = f"""/* Split Hero with Centered Silhouette — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --quote-text: {quote_text_color};
    --pattern: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-section {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background-color: var(--bg);
    
    /* The magic: Multiple layered backgrounds */
    /* Layer 1: Center Subject (Silhouette SVG) */
    /* Layer 2: Texture/Gradient environment */
    background-image: 
        url("data:image/svg+xml,{svg_silhouette}"),
        radial-gradient(circle at 50% 60%, var(--pattern) 0%, transparent 60%);
    background-position: bottom center, center;
    background-repeat: no-repeat, no-repeat;
    background-size: 75vh, cover;
    
    position: relative;
    display: flex;
    align-items: center;
    overflow: hidden;
}}

.hero-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 6vw;
    z-index: 10;
}}

/* === LEFT SIDE: INTRO === */
.main-intro {{
    max-width: 450px;
    transform: translateY(-4vh);
    animation: fadeInUp 1s ease-out forwards;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 96px);
    line-height: 1.1;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-bottom: 30px;
}}

.cta-btn {{
    display: block;
    width: fit-content;
    background-color: var(--accent);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-radius: 2px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-btn:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* === RIGHT SIDE: QUOTES === */
.main-quotes {{
    max-width: 400px;
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    transform: translateY(4vh);
    opacity: 0;
    animation: fadeInUp 1s ease-out 0.3s forwards;
}}

.main-quotes p {{
    font-size: 18px;
    line-height: 30px;
    color: var(--quote-text);
}}

.main-quotes p:first-child {{
    margin-bottom: 30px;
}}

/* Distinctive staggered indent for second quote */
.main-quotes p:nth-child(2) {{
    margin-left: clamp(20px, 4vw, 100px);
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(calc(var(--y-offset, 0) + 30px));
    }}
    to {{
        opacity: 1;
        transform: translateY(var(--y-offset, 0));
    }}
}}

.main-intro {{ --y-offset: -4vh; }}
.main-quotes {{ --y-offset: 4vh; }}

/* Responsive Stack */
@media (max-width: 1024px) {{
    .hero-section {{
        background-size: 50vh, cover;
        background-position: bottom -5vh center, center;
    }}
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 8vh;
        text-align: center;
        padding-top: 10vh;
    }}
    .main-intro, .main-quotes {{
        transform: translateY(0);
        max-width: 600px;
        --y-offset: 0;
    }}
    .main-intro {{ margin-top: 5vh; }}
    .main-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 24px;
        background: rgba(26, 37, 58, 0.5); /* contrast backdrop for mobile */
        border-radius: 8px;
        padding: 24px;
        backdrop-filter: blur(4px);
    }}
    .main-quotes p:nth-child(2) {{
        margin-left: 0;
    }}
    .cta-btn {{ margin: 30px auto 0 auto; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-section">
        <div class="hero-container">
            <!-- Left Side: Introduction -->
            <div class="main-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-btn">MY WORK</a>
            </div>

            <!-- Right Side: Supporting Quotes -->
            <div class="main-quotes">
                <p>
                    "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                    <br><br>
                    <em>- Dr. Seuss</em>
                </p>
                <p>
                    "For the best return on your money, pour your purse into your head."
                    <br><br>
                    <em>- Benjamin Franklin</em>
                </p>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JS required for this component.
// Layout and animations are fully handled by native CSS.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero Section Initialized.");
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
