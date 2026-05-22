def create_component(
    output_dir: str,
    title_text: str = "Welcome to my<br>first website",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisl non dolor scelerisque efficitur.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Center-Subject Split-Layout Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and SVG assets based on color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        # Darker silhouette for dark theme
        silhouette_color = "%230d1421" 
        pattern_color = "%23ffffff"
        pattern_opacity = "0.03"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        # Lighter silhouette for light theme
        silhouette_color = "%23e2e8f0" 
        pattern_color = "%23000000"
        pattern_opacity = "0.03"

    # SVG Pattern Data URI
    svg_pattern = f"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2z' fill='{pattern_color}' fill-opacity='{pattern_opacity}' fill-rule='evenodd'/%3E%3C/svg%3E"
    
    # SVG Portrait Silhouette Data URI
    svg_portrait = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath d='M200 50c-40 0-70 30-70 70s30 70 70 70 70-30 70-70-30-70-70-70zm-90 160c-40 0-80 20-80 60v230h340v-230c0-40-40-60-80-60H110z' fill='{silhouette_color}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Center-Subject Split-Layout Hero — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
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
}}

/* Main Hero Container */
.hero-main {{
    width: 100%;
    min-height: var(--container-height);
    /* Dual Backgrounds: Portrait on top, Pattern on bottom */
    background-image: 
        url("{svg_portrait}"),
        url("{svg_pattern}");
    background-position: bottom center, center;
    background-repeat: no-repeat, repeat;
    background-size: min(70vh, 500px), auto;
    
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 15vw; /* Pushes content left from center */
    max-width: 400px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(2rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Always white text on accent button */
    padding: 12px 24px;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: filter 0.3s ease;
}}

.btn:hover {{
    filter: brightness(1.2);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 10vw; /* Pushes content right from center */
    max-width: 350px;
    z-index: 10;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
    margin-bottom: 2.5rem;
}}

.quote-block p.quote-text {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 0.5rem;
}}

.quote-block p.quote-author {{
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-muted);
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: flex-start;
        padding: 4rem 2rem;
        background-position: bottom center, center;
        background-size: min(40vh, 300px), auto;
    }}
    
    .main-intro, .main-quotes {{
        position: static;
        right: auto;
        left: auto;
        max-width: 100%;
        text-align: center;
        margin-bottom: 3rem;
    }}
    
    .quote-block {{
        text-align: left;
        margin: 0 auto 2rem auto;
        max-width: 400px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Layout Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-main">
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>
        
        <div class="main-quotes">
            <div class="quote-block">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            <div class="quote-block">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Center-Subject Split-Layout Hero
// Interaction logic can be added here (e.g., parallax effects on scroll)
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero component loaded successfully.");
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
