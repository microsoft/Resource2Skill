def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "A showcase of creative development, visual design, and interactive web experiences.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Content Flex Hero with Center Subject' visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        silhouette_color = "%230d1320" # URL encoded dark blue/black
        pattern_color = "rgba(255, 255, 255, 0.03)"
        quote_opacity = "0.85"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        silhouette_color = "%23cbd5e1" # URL encoded slate grey
        pattern_color = "rgba(0, 0, 0, 0.04)"
        quote_opacity = "0.75"

    # SVG Silhouette (URL Encoded for background-image)
    svg_bg = f"data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M200 150c-40 0-70-30-70-70s30-70 70-70 70 30 70 70-30 70-70 70zm-120 450v-100c0-60 40-120 120-120h0c80 0 120 60 120 120v100H80z' fill='{silhouette_color}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Split-Content Flex Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

body {{
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Roboto', sans-serif;
}}

.hero-wrapper {{
    width: var(--comp-width);
    height: var(--comp-height);
    background-color: var(--bg-color);
    
    /* Layer 1: Bottom-anchored portrait (SVG silhouette) */
    /* Layer 2: Repeating dot pattern */
    background-image: 
        url("{svg_bg}"),
        radial-gradient(circle at center, {pattern_color} 2px, transparent 2px);
    background-size: 70%, 24px 24px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
    color: var(--text-color);
}}

/* The Flex-Pull Layout */
.main-intro {{
    position: relative;
    right: 12%; /* Pulls left from center */
    padding-bottom: 5%;
    max-width: 420px;
    z-index: 10;
}}

.main-quotes {{
    position: relative;
    left: 8%; /* Pushes right from center */
    padding-bottom: 5%;
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
    max-width: 320px;
    z-index: 10;
}}

/* Typography */
.main-intro h1 {{
    font-size: 64px;
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    opacity: 0.9;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    margin-top: 32px;
    text-decoration: none;
    font-size: 16px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background-color 0.2s ease, transform 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Quotes Styling & Staggering */
.main-quotes p {{
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 24px;
    opacity: {quote_opacity};
}}

.main-quotes p:last-child {{
    margin-bottom: 0;
}}

.main-quotes p:nth-child(2) {{
    /* Stagger the second quote as seen in the tutorial */
    margin-left: 32px;
}}

.author {{
    display: block;
    margin-top: 8px;
    font-weight: 700;
    font-size: 14px;
    opacity: 0.7;
}}

/* Basic fallback for small containers */
@media (max-width: 900px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 40px;
        background-position: bottom right -10%, center;
        background-size: 50%, 24px 24px;
    }}
    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        width: 80%;
        margin-bottom: 40px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Left Side: Introduction -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <!-- Right Side: Supporting Quotes -->
        <div class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="author">- Dr. Seuss</span>
            </p>
            <p>"For the best return on your money, pour your purse into your head."
                <span class="author">- Benjamin Franklin</span>
            </p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JS required for this CSS layout technique.
// Added simple hover ripple effect logging for demonstration.
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn');
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Call to action triggered!');
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
