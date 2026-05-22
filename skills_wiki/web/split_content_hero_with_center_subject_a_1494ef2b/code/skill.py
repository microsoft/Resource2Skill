def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Content Hero with Center Subject' visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors to maintain contrast
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        subtext_color = "rgba(255, 255, 255, 0.8)"
        pattern_color = "rgba(255, 255, 255, 0.05)"
        silhouette_color = "rgba(0, 0, 0, 0.4)"
        btn_text = "#FFFFFF"
    else:
        bg_color = "#F0F2F5"
        text_color = "#111827"
        subtext_color = "rgba(0, 0, 0, 0.7)"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "rgba(0, 0, 0, 0.1)"
        btn_text = "#FFFFFF"

    # Inline SVGs for pure CSS background layers (using rgba to avoid URL hex encoding issues)
    svg_subject = f"<svg width='400' height='600' viewBox='0 0 400 600' xmlns='http://www.w3.org/2000/svg'><path d='M50 600 C50 400 150 350 200 350 C250 350 350 400 350 600 Z' fill='{silhouette_color}'/><circle cx='200' cy='250' r='80' fill='{silhouette_color}'/></svg>"
    svg_pattern = f"<svg width='40' height='40' xmlns='http://www.w3.org/2000/svg'><circle cx='20' cy='20' r='2' fill='{pattern_color}'/></svg>"

    css = f"""/* Split-Content Hero Styles */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Main Hero Container */
.hero {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    
    /* Layer 1: Center Subject, Layer 2: Repeating Grid */
    background-image: 
        url("data:image/svg+xml;utf8,{svg_subject}"),
        url("data:image/svg+xml;utf8,{svg_pattern}");
    background-size: min(70vh, 500px), 40px 40px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    /* Core Layout Technique */
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding-bottom: 8vh; /* Lift content slightly */
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 12vw; /* Push away from center */
    width: 400px;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 6rem); /* Scales down gracefully */
    line-height: 1.1;
    color: var(--text);
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--subtext);
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: var(--btn-text);
    padding: 14px 28px;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    transition: filter 0.3s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 8vw; /* Push away from center */
    width: 350px;
    z-index: 2;
}}

.quote-box {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--subtext);
}}

/* Offset the second quote for visual interest (as done in tutorial) */
.quote-box:nth-child(2) {{
    margin-left: 80px;
}}

/* Responsive Fallback for smaller iframes/screens */
@media (max-width: 900px) {{
    .hero {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 10vh;
        background-position: bottom -100px center, center;
    }}
    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        width: 85%;
        margin-bottom: 40px;
    }}
    .main-quotes .quote-box:nth-child(2) {{
        margin-left: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <div class="main-quotes">
            <p class="quote-box">
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><br>- Dr. Seuss
            </p>
            <p class="quote-box">
                "For the best return on your money, pour your purse into your head."<br><br>- Benjamin Franklin
            </p>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero');
    
    // Add subtle parallax to the background images on mouse move
    // This adds a modern touch while respecting the CSS layout
    hero.addEventListener('mousemove', (e) => {
        // Calculate offset based on mouse position relative to center
        const xOffset = (window.innerWidth / 2 - e.pageX) / 80;
        const yOffset = (window.innerHeight / 2 - e.pageY) / 80;
        
        // Apply parallax only to the subject (Layer 1), keep the pattern static (Layer 2)
        // Background positions: Layer 1 (bottom center), Layer 2 (center)
        hero.style.backgroundPosition = `calc(50% + ${xOffset}px) calc(100% + ${yOffset}px), center`;
    });
    
    // Reset position on mouse leave
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = `bottom center, center`;
    });
});"""

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
