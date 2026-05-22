def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    cta_text: str = "MY WORK",
    quote_1: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"<br><br>- Dr. Seuss",
    quote_2: str = "\"For the best return on your money, pour your purse into your head.\"<br><br>- Benjamin Franklin",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Layered-Background Flexbox Hero.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        hero_overlay = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#F0F2F5"
        text_color = "#111827"
        pattern_color = "rgba(0, 0, 0, 0.03)"
        hero_overlay = "rgba(0, 0, 0, 0.08)"

    # Base64/URL encoded SVGs for standalone background layers
    # 1. A generic tech pattern
    pattern_svg = f"data:image/svg+xml,%3Csvg width='20' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h20v20H0z' fill='none'/%3E%3Cpath d='M2 2h4v4H2zM14 14h4v4h-4z' fill='{pattern_color.replace(' ', '').replace(',', '%2C')}'/%3E%3C/svg%3E"
    
    # 2. A central human-like silhouette/graphic placeholder
    hero_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath fill='{hero_overlay.replace(' ', '').replace(',', '%2C')}' d='M200 50c-55 0-100 45-100 100 0 53 41 96 93 99-52 14-99 53-120 110-18 47-23 102-23 150v91h300v-91c0-48-5-103-23-150-21-57-68-96-120-110 52-3 93-46 93-99 0-55-45-100-100-100z'/%3E%3C/svg%3E"

    css = f"""/* Asymmetrical Layered-Background Flexbox Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Outer page background */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Main Container Wrapper */
.hero-container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background-color: var(--bg-color);
    color: var(--text-color);
    position: relative;
    overflow: hidden;
    
    /* The Core Technique: Layered Backgrounds */
    background-image: 
        url("{hero_svg}"), 
        url("{pattern_svg}");
    background-size: 
        70%, /* Scales hero graphic relative to container width */
        20px 20px; /* Repeating pattern size */
    background-position: 
        bottom center, 
        0 0;
    background-repeat: 
        no-repeat, 
        repeat;

    /* Layout */
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Left Block: Introduction */
.main-intro {{
    position: relative;
    right: 12%; /* Shifts block left from center */
    padding-bottom: 8%; /* Adjusts vertical center of gravity */
    z-index: 2;
    max-width: 450px;
}}

.main-intro h1 {{
    font-size: 96px;
    line-height: 106px;
    font-weight: 900;
    text-transform: uppercase;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-top: 15px;
}}

.cta-button {{
    display: block;
    width: fit-content;
    background-color: var(--accent);
    color: #FFF;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: bold;
    padding: 12px 24px;
    margin-top: 30px;
    border-radius: 2px;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* Right Block: Staggered Quotes */
.main-quotes {{
    position: relative;
    left: 4%; /* Shifts block right from center */
    padding-bottom: 8%;
    z-index: 2;
}}

.main-quotes p {{
    font-size: 16px;
    line-height: 28px;
    max-width: 320px;
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin: 40px 0;
    font-style: italic;
}}

/* The Core Technique: Staggering */
.main-quotes p:nth-child(2) {{
    margin-left: 100px;
}}

/* Responsive Graceful Degradation */
@media (max-width: 1000px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        background-size: 90%, 20px 20px;
        padding: 40px;
    }}
    .main-intro, .main-quotes {{
        position: static;
        padding: 0;
        max-width: 100%;
    }}
    .main-intro {{ margin-bottom: 40px; }}
    .main-intro h1 {{
        font-size: 56px;
        line-height: 64px;
    }}
    .main-quotes p:nth-child(2) {{
        margin-left: 40px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">{cta_text}</a>
        </div>

        <div class="main-quotes">
            <p>{quote_1}</p>
            <p>{quote_2}</p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS implementation. No JavaScript required for core visual functionality.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Hero section initialized.');
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
