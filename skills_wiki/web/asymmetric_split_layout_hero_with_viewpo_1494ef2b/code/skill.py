def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Split-Layout Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#F4F6F8"
        text_color = "#111827"
        pattern_color = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Asymmetric Split-Layout Hero */
:root {{
    --site-bg: {bg_color};
    --site-text: {text_color};
    --site-accent: {accent_color};
    /* Calculate a darker hover state based on opacity */
    --site-accent-hover: color-mix(in srgb, var(--site-accent) 80%, black);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--site-bg);
    color: var(--site-text);
    overflow-x: hidden;
}}

/* 
  The main container utilizes layered backgrounds to mimic the video's setup.
  Layer 1: Radial gradient simulating the central subject/portrait.
  Layer 2 & 3: Linear gradients creating a repeating geometric pattern.
*/
.hero-main {{
    width: 100%;
    /* Set to exact height for reproduction environment, typically 100vh */
    height: {height_px}px; 
    min-height: 100vh;
    
    background-image: 
        radial-gradient(ellipse at bottom center, color-mix(in srgb, var(--site-accent) 20%, transparent) 0%, transparent 50%),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color}),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color});
    background-size: 
        100vw 70vh,
        20px 20px, 
        20px 20px;
    background-position: 
        bottom center,
        0 0, 
        10px 10px;
    background-repeat: 
        no-repeat,
        repeat, 
        repeat;

    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding-bottom: 8vh;
}}

/* Horizontal offsets tied to viewport height */
.main-intro {{
    position: relative;
    right: 20vh; 
    z-index: 10;
}}

.main-quotes {{
    position: relative;
    left: 4vh;
    z-index: 10;
}}

/* Typography & Element Styling */
.main-intro h1 {{
    font-size: clamp(48px, 8vh, 96px);
    line-height: 1.1;
    font-weight: 900;
    text-transform: uppercase;
    max-width: 500px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    max-width: 400px;
    margin-top: 30px;
}}

.main-intro a {{
    display: inline-block;
    background-color: var(--site-accent);
    color: #ffffff;
    text-decoration: none;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 30px;
    transition: background-color 0.3s ease;
}}

.main-intro a:hover {{
    background-color: var(--site-accent-hover);
}}

.main-quotes p {{
    border-left: 4px solid var(--site-accent);
    padding-left: 20px;
    font-size: 18px;
    line-height: 30px;
    max-width: 320px;
    margin-bottom: 40px;
    font-style: italic;
}}

.main-quotes .author {{
    display: block;
    margin-top: 10px;
    font-weight: bold;
    font-size: 16px;
    font-style: normal;
}}

/* Stagger effect for the quotes */
.main-quotes div:nth-child(2) p {{
    margin-left: 100px;
}}

/* Responsive fallback */
@media (max-width: 1024px) {{
    .hero-main {{
        flex-direction: column;
        text-align: center;
        padding: 40px 20px;
    }}
    .main-intro, .main-quotes {{
        right: auto;
        left: auto;
    }}
    .main-quotes div:nth-child(2) p {{
        margin-left: 0;
    }}
    .main-intro p, .main-intro h1, .main-quotes p {{
        max-width: 100%;
    }}
    .main-quotes {{
        margin-top: 60px;
    }}
    .main-quotes p {{
        border-left: none;
        border-top: 4px solid var(--site-accent);
        padding-left: 0;
        padding-top: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Layout Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-main">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#">My Work</a>
        </div>

        <div class="main-quotes">
            <div>
                <p>
                    "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                    <span class="author">- Dr. Seuss</span>
                </p>
            </div>
            <div>
                <p>
                    "For the best return on your money, pour your purse into your head."
                    <span class="author">- Benjamin Franklin</span>
                </p>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript is strictly necessary for this static layout, 
// as the responsive and alignment mechanics are purely handled via CSS Flexbox and Viewport units.
console.log("Hero layout initialized.");
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
