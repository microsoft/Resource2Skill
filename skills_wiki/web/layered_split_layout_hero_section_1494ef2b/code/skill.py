def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "This layout uses intelligent flexbox spacing and layered CSS backgrounds to frame a central subject perfectly. A robust, editorial-style hero section.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.04)"
        quote_text_color = "#E2E8F0"
    else:
        bg_color = "#F8FAFC"
        text_color = "#0F172A"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        quote_text_color = "#334155"

    # === CSS ===
    css = f"""/* Layered Split-Layout Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-text: {quote_text_color};
    --accent-color: {accent_color};
    --pattern-color: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.widget-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background-color: var(--bg-color);
    
    /* The Magic: Layered Backgrounds */
    /* Layer 1 (Top): Transparent Portrait */
    /* Layer 2 (Bottom): Dotted Grid Pattern */
    background-image: 
        url('https://placehold.co/500x700/transparent/888888?text=Portrait\\nSubject'),
        radial-gradient(var(--pattern-color) 2px, transparent 2px);
    
    /* Portrait takes up 80% height, Pattern repeats every 30px */
    background-size: min(80%, 600px), 30px 30px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    position: relative;
    overflow: hidden;
    color: var(--text-color);
}}

.hero-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;
    padding: 0 60px;
    position: relative;
    z-index: 2;
}}

/* Left Column */
.main-intro {{
    max-width: 450px;
}}

.main-intro h1 {{
    font-size: clamp(40px, 5vw, 84px);
    font-weight: 900;
    line-height: 1.05;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 40px;
    opacity: 0.9;
}}

.btn-primary {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 14px 32px;
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: transform 0.2s ease, filter 0.2s ease;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    filter: brightness(1.15);
}}

/* Right Column */
.main-quotes {{
    max-width: 320px;
    /* Pushing it slightly up from vertical center matching video */
    transform: translateY(-20px); 
}}

.quote-block {{
    margin-bottom: 48px;
    padding-left: 24px;
    border-left: 4px solid var(--accent-color);
}}

.quote-block:last-child {{
    margin-bottom: 0;
}}

.quote-block p {{
    font-size: 16px;
    font-style: italic;
    line-height: 1.6;
    color: var(--quote-text);
    margin-bottom: 12px;
}}

.quote-block footer {{
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Responsive Graceful Degradation */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: space-evenly;
        text-align: center;
        padding: 40px 20px;
        background: radial-gradient(circle at center, rgba(var(--bg-color), 0.7) 0%, var(--bg-color) 80%);
    }}
    
    .main-intro, .main-quotes {{
        max-width: 100%;
        transform: translateY(0);
    }}
    
    .quote-block {{
        border-left: none;
        border-top: 3px solid var(--accent-color);
        padding-left: 0;
        padding-top: 16px;
        margin-bottom: 32px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="widget-container">
        <div class="hero-content">
            <!-- Left Side: Introduction -->
            <section class="main-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn-primary">My Work</a>
            </section>

            <!-- Right Side: Supporting Quotes -->
            <aside class="main-quotes">
                <div class="quote-block">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <footer>- Dr. Seuss</footer>
                </div>
                <div class="quote-block">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <footer>- Benjamin Franklin</footer>
                </div>
            </aside>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Layered Split-Layout Interactive Depth
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.widget-container');
    
    // Add subtle mouse-move parallax to the portrait layer
    container.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to center of container
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left - (rect.width / 2);
        const y = e.clientY - rect.top - (rect.height / 2);
        
        // Define movement intensity (lower number = less movement)
        const intensityX = 30; 
        const intensityY = 40;
        
        const moveX = (x / rect.width) * intensityX;
        const moveY = (y / rect.height) * intensityY;
        
        // Update background position. 
        // Base position is bottom (100%) center (50%).
        // We apply the offset to the first background layer (the portrait).
        // The second layer (the pattern) remains static 'center'.
        container.style.backgroundPosition = `calc(50% + ${moveX}px) calc(100% + ${moveY}px), center`;
    });
    
    // Reset position when mouse leaves
    container.addEventListener('mouseleave', () => {
        container.style.transition = 'background-position 0.5s ease-out';
        container.style.backgroundPosition = 'bottom center, center';
        
        setTimeout(() => {
            container.style.transition = 'none';
        }, 500);
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
