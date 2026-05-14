def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO<br>MY FIRST<br>WEBSITE",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Portrait Hero Section.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # === Theme Derivation ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        svg_fill = "%23ffffff"
        svg_opacity = "0.06"
        pattern_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1A253A"
        text_muted = "rgba(26, 37, 58, 0.7)"
        svg_fill = "%23000000"
        svg_opacity = "0.04"
        pattern_color = "rgba(0, 0, 0, 0.08)"

    # SVG Silhouette Data URI
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M20,600 C20,350 100,280 200,280 C300,280 380,350 380,600 Z' fill='{svg_fill}' fill-opacity='{svg_opacity}'/%3E%3Ccircle cx='200' cy='150' r='90' fill='{svg_fill}' fill-opacity='{svg_opacity}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Split-Content Portrait Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --pattern-color: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    background-color: var(--bg-color);
    /* Layer 1: Portrait Silhouette, Layer 2: Dotted Pattern */
    background-image: 
        url("{portrait_svg}"),
        radial-gradient(var(--pattern-color) 1.5px, transparent 1.5px);
    background-size: 
        auto 85%, 
        24px 24px;
    background-position: 
        50% 100%, 
        center center;
    background-repeat: 
        no-repeat, 
        repeat;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}}

.hero-content {{
    width: 100%;
    max-width: 1200px;
    padding: 0 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 2;
    pointer-events: none; /* Let background clicks pass through */
}}

.hero-content > * {{
    pointer-events: auto; /* Re-enable clicks on text/buttons */
}}

/* Left Column: Intro */
.hero-intro {{
    flex: 0 1 450px;
    opacity: 0;
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.hero-intro h1 {{
    font-size: clamp(40px, 5.5vw, 76px);
    line-height: 1.05;
    font-weight: 800;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: -0.02em;
}}

.hero-intro > p {{
    font-size: 16px;
    line-height: 1.7;
    color: var(--text-muted);
    margin-bottom: 40px;
    max-width: 90%;
}}

.cta-btn {{
    display: inline-block;
    padding: 14px 36px;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 2px;
    transition: all 0.3s ease;
}}

.cta-btn:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

/* Right Column: Quotes */
.hero-quotes {{
    flex: 0 1 350px;
    display: flex;
    flex-direction: column;
    gap: 48px;
    opacity: 0;
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
}}

.quote-item {{
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
}}

.quote-item p {{
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 12px;
    font-style: italic;
    color: var(--text-muted);
}}

.quote-item .author {{
    font-size: 14px;
    font-weight: 700;
    color: var(--accent-color);
    text-transform: uppercase;
    letter-spacing: 0.02em;
}}

/* Animations */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive Graceful Degradation */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 60px;
    }}
    .hero-intro, .hero-quotes {{
        flex: 1 1 auto;
        width: 100%;
        max-width: 600px;
    }}
    .hero-intro > p {{
        margin: 0 auto 30px auto;
    }}
    .quote-item {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 16px;
    }}
    .hero-wrapper {{
        background-position: 50% 120%, center center; /* push portrait lower */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        <div class="hero-content">
            <div class="hero-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-btn">My Work</a>
            </div>
            
            <div class="hero-quotes">
                <div class="quote-item">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <span class="author">- Dr. Seuss</span>
                </div>
                <div class="quote-item">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <span class="author">- Benjamin Franklin</span>
                </div>
            </div>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-wrapper');
    
    // Parallax effect mapped to mouse movement
    hero.addEventListener('mousemove', (e) => {
        // Calculate cursor position relative to the center of the wrapper
        const rect = hero.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        
        // Multipliers define the intensity of the parallax shift
        const shiftX = x * 30; // Max 15px shift
        const shiftY = y * 15; // Max 7.5px shift
        
        // Update background position dynamically
        // Layer 1 (Portrait) moves, Layer 2 (Pattern) stays fixed
        hero.style.backgroundPosition = `calc(50% + ${shiftX}px) calc(100% + ${shiftY}px), center center`;
    });

    // Reset position when mouse leaves the section
    hero.addEventListener('mouseleave', () => {
        hero.style.transition = 'background-position 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
        hero.style.backgroundPosition = '50% 100%, center center';
        
        // Remove transition after it completes to restore raw mouse tracking responsiveness
        setTimeout(() => {
            hero.style.transition = 'none';
        }, 500);
    });
});
"""

    # === Write Files ===
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
        "files": files
    }
