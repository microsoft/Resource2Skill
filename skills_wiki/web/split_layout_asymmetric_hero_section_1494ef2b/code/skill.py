def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Asymmetric Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic mapping
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.8)"
        pattern_color = "rgba(255, 255, 255, 0.05)"
        portrait_color = "#111827"
    else:
        bg_color = "#F3F4F6"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.8)"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        portrait_color = "#D1D5DB"

    # CSS Generation
    css = f"""/* Split-Layout Asymmetric Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --pattern: {pattern_color};
    --portrait: {portrait_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    min-height: 600px;
    position: relative;
    background-image: radial-gradient(circle, var(--pattern) 2px, transparent 2.5px);
    background-size: 30px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
    overflow: hidden;
}}

/* Central Focal Image */
.hero-portrait {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    height: 85%;
    z-index: 1;
    fill: var(--portrait);
    transition: transform 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

/* Text Containers */
.main-intro, .main-quotes {{
    position: relative;
    z-index: 10;
    flex: 1;
    max-width: 400px;
}}

.main-intro {{
    padding-bottom: 8vh;
}}

.main-quotes {{
    padding-bottom: 8vh;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

/* Left Side: Headline & CTA */
.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    line-height: 1.1;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 20px;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 30px;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #fff;
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 700;
    text-decoration: none;
    text-transform: uppercase;
    transition: opacity 0.3s ease, transform 0.3s ease;
}}

.cta-button:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
}}

/* Right Side: Quotes */
.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    font-size: 16px;
    line-height: 1.6;
}}

.quote-block cite {{
    display: block;
    margin-top: 10px;
    font-style: normal;
    font-weight: 700;
    font-size: 14px;
}}

/* Asymmetric Offset from the Tutorial */
.main-quotes .quote-block:nth-child(2) {{
    margin-left: 100px;
}}

/* Entrance Animations */
.animate-hidden {{
    opacity: 0;
    transform: translateY(30px);
}}

.animate-reveal {{
    animation: slideUpFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

@keyframes slideUpFade {{
    0% {{ opacity: 0; transform: translateY(30px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 60px;
        padding-top: 60px;
        background-size: 20px 20px;
    }}
    .hero-portrait {{ opacity: 0.1; height: 60%; }}
    .quote-block {{ border-left: none; border-top: 4px solid var(--accent); padding-left: 0; padding-top: 20px; text-align: left; }}
    .main-quotes .quote-block:nth-child(2) {{ margin-left: 0; }}
}}
"""

    # HTML Generation
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <!-- Central SVG Portrait Cutout -->
        <svg class="hero-portrait animate-hidden" style="animation-delay: 0.1s;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" preserveAspectRatio="xMidYMax meet">
            <path d="M200 100 C140 100 110 150 110 210 C110 260 140 310 200 310 C260 310 290 260 290 210 C290 150 260 100 200 100 Z M90 350 C30 350 0 420 0 500 L0 600 L400 600 L400 500 C400 420 370 350 310 350 L90 350 Z" />
        </svg>

        <!-- Left Intro Block -->
        <div class="main-intro">
            <h1 class="animate-hidden" style="animation-delay: 0.2s;">{title_text}</h1>
            <p class="animate-hidden" style="animation-delay: 0.3s;">{body_text}</p>
            <a href="#" class="cta-button animate-hidden" style="animation-delay: 0.4s;">My Work</a>
        </div>

        <!-- Right Quotes Block -->
        <div class="main-quotes">
            <div class="quote-block animate-hidden" style="animation-delay: 0.5s;">
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <cite>- Dr. Seuss</cite>
            </div>
            <div class="quote-block animate-hidden" style="animation-delay: 0.6s;">
                "For the best return on your money, pour your purse into your head."
                <cite>- Benjamin Franklin</cite>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Generation
    js = """document.addEventListener('DOMContentLoaded', () => {
    // Simple entrance animation logic using Intersection Observer
    const elements = document.querySelectorAll('.animate-hidden');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-reveal');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(el => observer.observe(el));
});"""

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
