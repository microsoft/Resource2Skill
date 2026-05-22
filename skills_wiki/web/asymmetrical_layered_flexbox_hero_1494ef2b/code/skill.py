def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY<br>FIRST WEBSITE",
    body_text: str = "A demonstration of layered background compositing, asymmetrical flexbox alignment, and interactive depth techniques.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Layered Flexbox Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#151b29"
        text_color = "#ffffff"
        header_bg = "#ffffff"
        header_text = "#000000"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#e5e7eb"
        text_color = "#111827"
        header_bg = "#111827"
        header_text = "#ffffff"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # Inline SVG for the portrait silhouette to ensure self-containment
    svg_portrait = "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E%3Cpath fill='{}' d='M200 60c-38.66 0-70 31.34-70 70s31.34 70 70 70 70-31.34 70-70-31.34-70-70-70zm0 160c-77.32 0-140 62.68-140 140v20h280v-20c0-77.32-62.68-140-140-140z'/%3E%3C/svg%3E".format("%23222" if color_scheme == "dark" else "%23ccc")

    css = f"""/* Asymmetrical Layered Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --header-bg: {header_bg};
    --header-text: {header_text};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.browser-window {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Mock Header for layout context */
.site-header {{
    position: absolute;
    top: 0;
    width: 100%;
    height: 60px;
    background-color: var(--header-bg);
    color: var(--header-text);
    display: flex;
    align-items: center;
    padding: 0 40px;
    font-weight: 600;
    z-index: 1000;
}}

/* Main Hero Setup */
.hero-section {{
    width: 100%;
    height: calc(100% - 60px);
    margin-top: 60px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* The Layering Technique: Portrait over Pattern */
    background-image: 
        url("data:image/svg+xml,{svg_portrait}"),
        radial-gradient(var(--surface) 3px, transparent 3px);
    background-size: 
        55vh, /* Portrait size */
        30px 30px; /* Pattern scale */
    background-position: 
        50% 100%, /* Portrait anchored bottom center */
        center;
    background-repeat: 
        no-repeat,
        repeat;
}}

/* Asymmetrical Layout Logic */
.hero-intro {{
    position: relative;
    right: 80px; /* Push left manually */
    max-width: 450px;
    padding-bottom: 40px;
}}

.hero-intro h1 {{
    font-size: 72px;
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: 20px;
}}

.hero-intro p {{
    font-size: 16px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #fff;
    text-decoration: none;
    padding: 14px 28px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.2);
}}

/* Quotes Staggering Logic */
.hero-quotes {{
    position: relative;
    left: 40px; /* Push right manually */
    max-width: 320px;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

/* The stagger effect */
.hero-quotes p:nth-child(2) {{
    margin-left: 80px;
}}

.quote-author {{
    display: block;
    margin-top: 10px;
    font-weight: 700;
    font-size: 14px;
    opacity: 1;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asymmetrical Layered Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="browser-window">
        <header class="site-header">
            LOGO
        </header>
        
        <main class="hero-section" id="hero">
            <div class="hero-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">My Work</a>
            </div>
            
            <div class="hero-quotes">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span></p>
                
                <p>"For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span></p>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Parallax interaction for the layered background
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.getElementById('hero');
    
    // Listen for mouse movements on the hero section
    hero.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to the center of the element
        const rect = hero.getBoundingClientRect();
        const xPos = (e.clientX - rect.left) / rect.width - 0.5;
        
        // Shift the background position. 
        // We only target the first background (the portrait), leaving the pattern static.
        // Base position is 50% X, 100% Y. We apply a subtle offset multiplier (e.g., -30px).
        const offsetX = 50 + (xPos * -6);
        
        hero.style.backgroundPosition = `${offsetX}% 100%, center`;
    });
    
    // Reset position when mouse leaves
    hero.addEventListener('mouseleave', () => {
        hero.style.transition = 'background-position 0.5s ease-out';
        hero.style.backgroundPosition = '50% 100%, center';
        
        setTimeout(() => {
            hero.style.transition = 'none';
        }, 500);
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
