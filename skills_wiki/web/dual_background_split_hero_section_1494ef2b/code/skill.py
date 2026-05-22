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
    Create a web component reproducing the Dual-Background Split Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#111827" 
        text_color = "#f9fafb"
        text_muted = "#9ca3af"
        # Hex codes encoded for SVG Data URI
        silhouette_color = "%231f2937" 
        pattern_color = "rgba(255,255,255,0.03)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        silhouette_color = "%23e2e8f0"
        pattern_color = "rgba(0,0,0,0.04)"

    # Self-contained SVG assets
    svg_pattern = f'<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg"><path d="M0 40L40 0" stroke="{pattern_color}" stroke-width="2"/></svg>'
    svg_portrait = f'<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg"><circle cx="200" cy="120" r="80" fill="{silhouette_color}" /><path d="M60 400 Q 60 220 200 220 Q 340 220 340 400" fill="{silhouette_color}" /></svg>'

    # === CSS ===
    css = f"""/* Dual-Background Split Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg);
    color: var(--text-main);
}}

/* The Core Technique: Dual Background Images */
.hero-section {{
    min-height: var(--height);
    width: 100%;
    /* Layer 1: Foreground Portrait, Layer 2: Background Pattern */
    background-image: 
        url('data:image/svg+xml;utf8,{svg_portrait}'),
        url('data:image/svg+xml;utf8,{svg_pattern}');
    background-position: 
        bottom center, 
        center;
    background-repeat: 
        no-repeat, 
        repeat;
    background-size: 
        auto 75vh, /* Scales the portrait to viewport height */
        40px 40px;
    
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4rem 8vw;
    position: relative;
    overflow: hidden;
}}

/* Left Column */
.main-intro {{
    max-width: 420px;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.05;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 12px 28px;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Column */
.main-quotes {{
    max-width: 350px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 1.5rem;
}}

.quote-block p {{
    font-size: 1.05rem;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 0.75rem;
}}

.quote-block cite {{
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-muted);
    font-style: normal;
}}

/* Responsive behavior */
@media (max-width: 960px) {{
    .hero-section {{
        flex-direction: column;
        justify-content: center;
        gap: 4rem;
        /* Shift background portrait right to accommodate stacked text */
        background-position: bottom -5% right -20%, center;
        background-size: auto 50vh, 40px 40px;
        padding: 6rem 5vw;
    }}

    .main-intro, .main-quotes {{
        max-width: 600px;
        width: 100%;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Hero Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-section">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>

        <div class="main-quotes">
            <blockquote class="quote-block">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <cite>- Dr. Seuss</cite>
            </blockquote>
            
            <blockquote class="quote-block">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <cite>- Benjamin Franklin</cite>
            </blockquote>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interaction logic (Optional for this CSS-heavy layout)
document.addEventListener('DOMContentLoaded', () => {
    // Subtle entry animation for text elements
    const elements = document.querySelectorAll('.main-intro, .quote-block');
    elements.forEach((el, index) => {
        el.animate([
            { opacity: 0, transform: 'translateY(20px)' },
            { opacity: 1, transform: 'translateY(0)' }
        ], {
            duration: 800,
            easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
            fill: 'forwards',
            delay: index * 200
        });
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
