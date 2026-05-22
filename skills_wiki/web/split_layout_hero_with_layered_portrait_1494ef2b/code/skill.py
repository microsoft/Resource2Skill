def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived colors
    bg_base = "#1a253a" if color_scheme == "dark" else "#e0e5ec"
    text_main = "#ffffff" if color_scheme == "dark" else "#111111"
    text_muted = "rgba(255, 255, 255, 0.85)" if color_scheme == "dark" else "rgba(0, 0, 0, 0.75)"
    btn_bg = "#9e2f6e"
    btn_hover = "#6b1f4a"

    # SVG Avatar acting as the cut-out portrait
    portrait_url = "https://api.dicebear.com/7.x/open-peeps/svg?seed=Felix&backgroundColor=transparent&pose=standing"

    css = f"""/* Split-Layout Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');

:root {{
    --bg-base: {bg_base};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg-base);
    
    /* Layered Backgrounds: Portrait over a radial pattern */
    background-image: 
        url('{portrait_url}'),
        radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0.2) 100%);
    background-size: 
        auto 85%, /* Portrait height */
        cover;    /* Pattern covers everything */
    background-position: 
        bottom center, 
        center;
    background-repeat: no-repeat;
    
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 6vw;
    overflow: hidden;
}}

/* Left Column: Intro */
.main-intro {{
    max-width: 500px;
    z-index: 10;
    padding-bottom: 8vh;
}}

.main-intro h1 {{
    font-size: clamp(48px, 6vw, 96px);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-main);
    margin-bottom: 30px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    color: var(--text-muted);
    margin-bottom: 40px;
}}

.btn-work {{
    display: inline-block;
    background-color: var(--btn-bg);
    color: #fff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: background-color 0.2s ease;
}}

.btn-work:hover {{
    background-color: var(--btn-hover);
}}

/* Right Column: Quotes */
.main-quotes {{
    max-width: 450px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
}}

.quote-block:nth-child(2) {{
    margin-left: 80px; /* Staggered offset mimicking the tutorial */
}}

.quote-text {{
    font-size: 16px;
    line-height: 28px;
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 15px;
}}

.quote-author {{
    font-size: 14px;
    font-weight: 600;
    color: var(--text-main);
}}

/* Responsive Adjustments */
@media (max-width: 1024px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 60px;
        background-position: bottom right -20%, center;
        background-size: auto 60%, cover;
        padding: 40px 5vw;
        align-items: flex-start;
    }}
    .main-intro, .main-quotes {{
        max-width: 100%;
        background: rgba(26, 37, 58, 0.7); /* ensure readable text over image */
        padding: 20px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
    }}
    .quote-block:nth-child(2) {{
        margin-left: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Left Side: Main Introduction -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn-work">My Work</a>
        </div>

        <!-- Right Side: Secondary Quotes -->
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

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Split-Layout Hero interactions
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add subtle parallax effect to the backgrounds on mouse move
    const hero = document.querySelector('.hero-container');
    
    hero.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth - e.pageX * 2) / 90;
        const y = (window.innerHeight - e.pageY * 2) / 90;
        
        // Slightly shift the background image position
        hero.style.backgroundPosition = `calc(50% + ${x}px) calc(100% + ${y}px), center`;
    });
    
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = `bottom center, center`;
    });
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
