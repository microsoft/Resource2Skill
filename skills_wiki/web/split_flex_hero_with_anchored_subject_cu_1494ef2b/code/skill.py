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
    Create a web component reproducing the Split-Flex Hero pattern.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        quote_text_color = "rgba(255, 255, 255, 0.8)"
    else:
        bg_color = "#F0F4F8"
        text_color = "#111827"
        quote_text_color = "rgba(17, 24, 39, 0.8)"

    # Generate a procedural SVG silhouette for the central subject
    silhouette_svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'>
        <path fill='{text_color}' opacity='0.1' d='M100,600 C100,450 140,380 200,380 C260,380 300,450 300,600 Z' />
        <circle fill='{text_color}' opacity='0.1' cx='200' cy='280' r='70' />
    </svg>"""
    encoded_silhouette = "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(silhouette_svg)

    # Generate a subtle background pattern
    pattern_svg = f"""<svg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'>
        <path d='M20 20h20v20H20zM0 0h20v20H0z' fill='{text_color}' fill-opacity='0.02' fill-rule='evenodd'/>
    </svg>"""
    encoded_pattern = "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(pattern_svg)

    # === CSS ===
    css = f"""/* Split-Flex Hero with Anchored Subject Cutout */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Main Component Wrapper */
.hero-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    /* Multiple backgrounds: Top layer is the portrait, bottom layer is the repeating pattern */
    background-image: url('{encoded_silhouette}'), url('{encoded_pattern}');
    background-size: 70vh, auto;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}}

/* Left Column: Introduction */
.main-intro {{
    position: relative;
    right: 15vh; /* Pushes content leftwards, making space for the center portrait */
    padding-bottom: 8vh;
    max-width: 450px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: 72px;
    line-height: 1.1;
    color: var(--text-color);
    text-transform: uppercase;
    font-weight: 900;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-color);
    margin-bottom: 32px;
}}

.btn {{
    display: block;
    width: fit-content;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: opacity 0.2s ease, transform 0.2s ease;
}}

.btn:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
}}

/* Right Column: Secondary Quotes */
.main-quotes {{
    position: relative;
    left: 4vh; /* Pushes content rightwards */
    padding-bottom: 8vh;
    max-width: 320px;
    z-index: 10;
}}

.main-quotes p {{
    font-size: 16px;
    line-height: 1.6;
    color: var(--quote-color);
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin: 40px 0;
}}

/* Stagger the second quote for visual interest */
.main-quotes p:nth-child(2) {{
    margin-left: 60px;
}}

.quote-author {{
    display: block;
    font-weight: 700;
    margin-top: 8px;
    color: var(--text-color);
}}

/* Basic Responsiveness for smaller embedded views */
@media (max-width: 900px) {{
    .main-intro {{ right: 5vh; max-width: 350px; }}
    .main-intro h1 {{ font-size: 48px; }}
    .main-quotes {{ left: 0; max-width: 280px; display: none; /* hide secondary on small to keep focus */ }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">MY WORK</a>
        </div>

        <div class="main-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>
                "An investment in knowledge pays the best interest."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interaction logic for Hero Section
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn');
    
    // Simple click ripple effect on the CTA button
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = 'translateY(-2px)';
        }, 150);
    });
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
