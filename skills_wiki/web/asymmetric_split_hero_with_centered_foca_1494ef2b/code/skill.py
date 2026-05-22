def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1440,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Split Hero design pattern.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic based on the tutorial's aesthetic
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_color = "#ffffff"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        silhouette_color = "rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#e2e8f0"
        text_color = "#1a202c"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "rgba(0, 0, 0, 0.1)"

    # Base64 encoded SVGs for self-contained visual fidelity (Texture pattern & Center Portrait Placeholder)
    svg_pattern = f"data:image/svg+xml;utf8,<svg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'><path d='M20 0L40 20L20 40L0 20Z' fill='{pattern_color}' fill-rule='evenodd'/></svg>"
    svg_portrait = f"data:image/svg+xml;utf8,<svg width='400' height='600' viewBox='0 0 400 600' xmlns='http://www.w3.org/2000/svg'><circle cx='200' cy='180' r='90' fill='{silhouette_color}'/><path d='M60 600 C 60 380, 340 380, 340 600 Z' fill='{silhouette_color}'/></svg>"

    css = f"""/* Asymmetric Split Hero Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: #0d1117; /* Darker backdrop for the framed container */
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background-color: var(--bg-color);
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 25%; /* Pushes columns apart to frame the center */
    padding: 0 5%;
    
    /* Layered backgrounds: Portrait on top, repeating pattern below */
    background-image: 
        url("{svg_portrait}"),
        url("{svg_pattern}");
    background-position: 
        bottom center,
        center;
    background-size: 
        auto 85%, /* Scales portrait appropriately */
        40px 40px;
    background-repeat: 
        no-repeat,
        repeat;
}}

/* Left Column: Intro */
.main-intro {{
    flex: 1;
    max-width: 450px;
    z-index: 2; /* Ensure text sits above backgrounds */
    margin-bottom: 5vh; /* Slight vertical offset based on video */
}}

.main-intro h1 {{
    font-size: 4rem; /* Scaled slightly from 96px for generic container fit */
    line-height: 1.1;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-bottom: 32px;
    opacity: 0.9;
}}

.main-intro a.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Forces white text on buttons */
    text-decoration: none;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    transition: filter 0.2s ease;
}}

.main-intro a.cta-button:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    flex: 1;
    max-width: 350px;
    z-index: 2;
    margin-bottom: 5vh;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.6;
    font-style: italic;
    opacity: 0.9;
}}

/* Editorial Asymmetry Offset */
.main-quotes p:nth-child(2) {{
    margin-left: 80px;
}}

.quote-author {{
    display: block;
    margin-top: 12px;
    font-style: normal;
    font-weight: 600;
    color: var(--accent-color);
}}

/* Responsive fallbacks */
@media (max-width: 1024px) {{
    .hero-container {{
        gap: 5%;
    }}
    .main-intro h1 {{ font-size: 3rem; }}
    .main-quotes p:nth-child(2) {{ margin-left: 40px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Reproduction</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </section>

        <section class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><span class="quote-author">- Dr. Seuss</span></p>
            <p>"For the best return on your money, pour your purse into your head."<br><span class="quote-author">- Benjamin Franklin</span></p>
        </section>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic (Empty for pure CSS layout)
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero section loaded.");
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
