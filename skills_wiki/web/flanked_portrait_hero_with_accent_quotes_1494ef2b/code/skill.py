def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#c13584",     # Authentic magenta from tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flanked Portrait Hero layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1a253a"  # Tutorial specific dark blue
        text_color = "#ffffff"
        pattern_color = "rgba(255, 255, 255, 0.04)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#1a253a"
        pattern_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Flanked Portrait Hero Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --pattern: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', 'Inter', system-ui, sans-serif;
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    position: relative;
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    background-color: var(--bg);
    background-image: radial-gradient(circle at center, var(--pattern) 2px, transparent 2px);
    background-size: 24px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 6vw;
    overflow: hidden;
    color: var(--text);
}}

/* Central Masked Portrait */
.hero-portrait {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 38%;
    max-width: 450px;
    height: 85%;
    /* Using a placeholder portrait image */
    background-image: url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80');
    background-size: cover;
    background-position: top center;
    border-radius: 300px 300px 0 0;
    
    /* Fades out the bottom of the image into the background */
    -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    
    z-index: 1;
    filter: grayscale(15%) contrast(1.1);
}}

/* Left Column: Intro */
.hero-intro {{
    position: relative;
    z-index: 2;
    max-width: 380px;
    padding-bottom: 5vh; /* Slight upward shift */
}}

.hero-intro h1 {{
    font-size: clamp(2.5rem, 5.5vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3); /* Ensure legibility if overlapping image */
}}

.hero-intro p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.9;
    margin-bottom: 2.5rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}}

.hero-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff; /* Hardcoded white for contrast on accent */
    text-decoration: none;
    padding: 0.8rem 2rem;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 3px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.hero-cta:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* Right Column: Quotes */
.hero-quotes {{
    position: relative;
    z-index: 2;
    max-width: 320px;
    padding-bottom: 5vh;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
    font-size: 0.95rem;
    line-height: 1.7;
    opacity: 0.9;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}}

/* Staggered Layout for second quote */
.hero-quotes p:nth-child(2) {{
    margin-left: 3.5rem;
}}

.quote-author {{
    display: block;
    margin-top: 1rem;
    font-style: italic;
    opacity: 0.8;
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        padding: 4rem 2rem;
        height: auto;
        min-height: var(--height);
    }}
    .hero-portrait {{
        opacity: 0.15;
        width: 80%;
        height: 60%;
        border-radius: 200px 200px 0 0;
    }}
    .hero-intro, .hero-quotes {{
        max-width: 100%;
        padding-bottom: 2rem;
    }}
    .hero-quotes p:nth-child(2) {{
        margin-left: 2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Central Image Layer -->
        <div class="hero-portrait"></div>
        
        <!-- Left Content -->
        <div class="hero-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="hero-cta">MY WORK</a>
        </div>
        
        <!-- Right Content -->
        <div class="hero-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>
                "For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic (empty by default for structural hero)
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero layout loaded and ready.");
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
