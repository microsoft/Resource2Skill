def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    quote1_text: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"<br><br>- Dr. Seuss",
    quote2_text: str = "\"For the best return on your money, pour your purse into your head.\"<br><br>- Benjamin Franklin",
    cta_text: str = "MY WORK",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Split-Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        bg_alt = "#2A354A"
        text_main = "#ffffff"
        text_muted = "#e2e8f0"
    else:
        bg_color = "#f0f2f5"
        bg_alt = "#e4e6ea"
        text_main = "#1A253A"
        text_muted = "#4a5568"

    # We use a base64 encoded SVG portrait silhouette so the component functions entirely standalone
    # while still matching the layered background logic of the tutorial.
    svg_fill = bg_alt.replace("#", "%23")
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'%3E%3Ccircle cx='200' cy='150' r='75' fill='{svg_fill}'/%3E%3Cpath d='M80,400 Q80,240 200,240 Q320,240 320,400' fill='{svg_fill}'/%3E%3C/svg%3E"

    css = f"""/* Flexbox Split-Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --bg-alt: {bg_alt};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000; /* Outer page canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-viewport {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    /* Layered Backgrounds: Portrait on top, Radial Gradient behind */
    background-image: 
        url("{portrait_svg}"),
        radial-gradient(circle at center, var(--bg-alt) 0%, var(--bg) 100%);
    background-size: min(500px, calc(var(--height) * 0.8)), cover;
    background-repeat: no-repeat, no-repeat;
    background-position: bottom center, center;
    
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* This gap pushes the columns outward, framing the central background portrait */
    gap: max(40px, calc(var(--width) * 0.18));
    padding: 0 4%;
}}

/* Left Column */
.main-intro {{
    position: relative;
    max-width: 380px;
    z-index: 10;
    /* Optical vertical balance over the portrait */
    transform: translateY(-8%);
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, calc(var(--width) * 0.05), 4rem);
    line-height: 1.05;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--text-main);
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.main-intro .cta-btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff; /* fixed white to ensure CTA contrast */
    text-decoration: none;
    padding: 0.75rem 1.5rem;
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    transition: filter 0.2s ease;
}}

.main-intro .cta-btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column */
.main-quotes {{
    position: relative;
    max-width: 320px;
    z-index: 10;
    transform: translateY(-8%);
}}

.main-quotes p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
}}

/* Staggered block effect */
.main-quotes p:nth-child(2) {{
    margin-left: 3.5rem;
    margin-bottom: 0;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flexbox Split-Hero Section</title>
    <!-- Google Fonts: Roboto -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-viewport">
        <!-- Left content column -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-btn">{cta_text}</a>
        </div>
        
        <!-- Right content column -->
        <div class="main-quotes">
            <p>{quote1_text}</p>
            <p>{quote2_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JavaScript required for this purely structural CSS flexbox pattern.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Flexbox Split-Hero Initialized.");
});
"""

    # Write files
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
