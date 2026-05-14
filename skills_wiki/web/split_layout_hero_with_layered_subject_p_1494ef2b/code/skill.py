def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584", 
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Hero with Layered Subject Portrait.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base64 SVG of a male silhouette portrait (to ensure the layering effect works standalone)
    portrait_svg = "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath fill='%230f1724' d='M100 500c0-80 30-150 70-180-20-20-30-50-30-90 0-60 20-100 60-100s60 40 60 100c0 40-10 70-30 90 40 30 70 100 70 180H100z'/%3E%3C/svg%3E"

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        quote_text_color = "#D1D5DB"
    else:
        bg_color = "#F3F4F6"
        text_color = "#111827"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        quote_text_color = "#4B5563"
        portrait_svg = portrait_svg.replace("%230f1724", "%23d1d5db") # Lighter silhouette for light theme

    css = f"""/* Split-Layout Hero Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-text: {quote_text_color};
    --accent-color: {accent_color};
    --pattern-color: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    overflow: hidden;
    background-color: var(--bg-color);
    
    /* The Core Visual Mechanism: Layered Backgrounds */
    /* 1. Subject Portrait (Bottom Center) */
    /* 2. Geometric Pattern (Repeating Grid simulated with radial-gradient) */
    background-image: 
        url("{portrait_svg}"),
        radial-gradient(var(--pattern-color) 2px, transparent 2px),
        radial-gradient(var(--pattern-color) 2px, transparent 2px);
    background-position: 
        bottom center,
        0 0,
        20px 20px;
    background-size: 
        65% auto, /* Portrait scale */
        40px 40px, /* Pattern scale */
        40px 40px;
    background-repeat: 
        no-repeat,
        repeat,
        repeat;
        
    /* Layout */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
}}

/* Left Column: Intro */
.main-intro {{
    width: 35%;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(2rem, 4vw, 4.5rem);
    line-height: 1.1;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--text-color);
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--quote-text);
    margin-bottom: 30px;
}}

.cta-btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 0.9rem;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-btn:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* Right Column: Quotes */
.main-quotes {{
    width: 35%;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-box {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
}}

/* Staggered Indentation Effect from Tutorial */
.quote-box:nth-child(2) {{
    margin-left: 80px;
}}

.quote-text {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--quote-text);
    font-style: italic;
    margin-bottom: 10px;
}}

.quote-author {{
    font-size: 0.9rem;
    font-weight: bold;
    color: var(--text-color);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 40px;
        padding: 40px 5%;
        background-position: bottom right -20%, 0 0, 20px 20px;
        background-size: 80% auto, 40px 40px, 40px 40px;
    }}
    .main-intro, .main-quotes {{ width: 100%; }}
    .quote-box:nth-child(2) {{ margin-left: 40px; }}
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
    <main class="hero-container" id="hero">
        
        <!-- Left Side: Introduction -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-btn">My Work</a>
        </div>

        <!-- Right Side: Supporting Quotes -->
        <div class="main-quotes">
            <div class="quote-box">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            
            <div class="quote-box">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Optional Parallax Enhancement for Background Layers
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.getElementById('hero');
    
    hero.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const xPos = (clientX / window.innerWidth - 0.5) * 20; // Subtle 20px shift
        const yPos = (clientY / window.innerHeight - 0.5) * 20;
        
        // Target background position: 
        // Portrait (bottom center, shift slightly)
        // Pattern 1 (shift moderately)
        // Pattern 2 (shift strongly for depth)
        hero.style.backgroundPosition = `
            calc(50% + ${xPos * 0.5}px) bottom,
            ${xPos}px ${yPos}px,
            calc(20px + ${xPos * 1.5}px) calc(20px + ${yPos * 1.5}px)
        `;
    });
    
    hero.addEventListener('mouseleave', () => {
        // Reset on mouse leave
        hero.style.backgroundPosition = 'bottom center, 0 0, 20px 20px';
        hero.style.transition = 'background-position 0.5s ease-out';
    });
    
    hero.addEventListener('mouseenter', () => {
        // Remove transition to allow instant tracking
        hero.style.transition = 'none';
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
