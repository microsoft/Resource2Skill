def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY<br>FIRST WEBSITE",
    body_text: str = "I build engaging, high-performance web experiences. Focused on elegant code, beautiful design, and seamless user interactions.",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Layer Parallax Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        pattern_stroke = "rgba(255, 255, 255, 0.04)"
        portrait_fill = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        pattern_stroke = "rgba(0, 0, 0, 0.05)"
        portrait_fill = "rgba(0, 0, 0, 0.15)"

    # Standalone Base64 SVGs to replicate the tutorial's images
    svg_pattern = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M30 15v30M15 30h30' stroke='{pattern_stroke.replace(' ', '%20')}' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E"
    svg_portrait = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath d='M200 150 C 120 150 60 220 50 300 L 20 500 L 380 500 L 350 300 C 340 220 280 150 200 150 Z' fill='{portrait_fill.replace(' ', '%20')}'/%3E%3Ccircle cx='200' cy='110' r='70' fill='{portrait_fill.replace(' ', '%20')}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Dual-Layer Parallax Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Roboto', -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-container {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 4rem;
    
    /* The Core Technique: Layered Backgrounds */
    background-color: var(--bg-color);
    background-image: 
        url("{svg_portrait}"), /* Layer 1: Foreground Subject */
        url("{svg_pattern}");  /* Layer 2: Background Pattern */
    
    background-size: 
        auto 85%, /* Subject scale */
        60px 60px; /* Pattern scale */
        
    background-position: 
        bottom center, 
        center center;
        
    background-repeat: 
        no-repeat, 
        repeat;
        
    transition: background-position 0.1s ease-out;
}}

/* Flanking Content Modules */
.hero-left, .hero-quotes {{
    position: relative;
    z-index: 10;
    max-width: 400px;
    flex: 1;
}}

/* Typography & Accents */
.hero-left {{
    border-left: 4px solid var(--accent-color);
    padding-left: 2rem;
    padding-bottom: 1rem;
}}

.hero-left h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 800;
    text-transform: uppercase;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
}}

.hero-left p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 0.8rem 2rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}}

.cta-button:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

/* Right Side: Staggered Quotes */
.hero-quotes {{
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
    background: linear-gradient(90deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0) 100%);
    padding-top: 1rem;
    padding-bottom: 1rem;
    border-radius: 0 8px 8px 0;
}}

/* Stagger the second quote as seen in tutorial */
.quote-block:nth-child(2) {{
    margin-left: 3rem;
}}

.quote-block p {{
    font-size: 1.05rem;
    line-height: 1.5;
    margin-bottom: 0.8rem;
    font-style: italic;
}}

.quote-block cite {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* Responsive behavior */
@media (max-width: 960px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 3rem;
        padding: 4rem 2rem;
        background-position: bottom right -20%, center center;
        background-size: auto 50%, 60px 60px;
    }}
    .quote-block:nth-child(2) {{
        margin-left: 0;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dual-Layer Parallax Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-container">
        
        <!-- Left Flank: Intro Content -->
        <div class="hero-left">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">MY WORK</a>
        </div>

        <!-- Right Flank: Social Proof / Quotes -->
        <div class="hero-quotes">
            <div class="quote-block">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <cite>— Dr. Seuss</cite>
            </div>
            
            <div class="quote-block">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <cite>— Benjamin Franklin</cite>
            </div>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Parallax Effect for Multiple Backgrounds
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-container');
    
    // Only apply parallax on desktop devices to prevent scroll jank on touch
    if (window.matchMedia("(pointer: fine)").matches) {
        hero.addEventListener('mousemove', (e) => {
            // Calculate normalized cursor position (-0.5 to 0.5)
            const x = (e.clientX / window.innerWidth) - 0.5;
            const y = (e.clientY / window.innerHeight) - 0.5;

            // Shift foreground slightly, background more dramatically in opposite direction
            const fgOffsetX = x * 20; // max 10px shift
            const bgOffsetX = -x * 40; // max 20px shift
            const bgOffsetY = -y * 40;

            // Update background-position via CSS calc
            hero.style.backgroundPosition = `
                calc(50% + ${fgOffsetX}px) bottom, 
                calc(50% + ${bgOffsetX}px) calc(50% + ${bgOffsetY}px)
            `;
        });

        // Reset to center smoothly on mouse leave
        hero.addEventListener('mouseleave', () => {
            hero.style.backgroundPosition = 'bottom center, center center';
        });
    }
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
