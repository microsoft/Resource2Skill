def create_component(
    output_dir: str,
    title_text: str = "Welcome to my website",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Flanking Hero Section effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_opacity = "0.05"
        portrait_color = "%23ffffff"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        pattern_opacity = "0.08"
        portrait_color = "%23000000"

    body_text = body_text or "Building digital experiences with modern web technologies. I craft responsive layouts, intuitive interactions, and clean code."

    # Data URI SVGs to make the component fully self-contained
    # 1. An abstract gradient silhouette anchored to the bottom
    portrait_svg = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 800'><defs><linearGradient id='grad' x1='0%' y1='0%' x2='0%' y2='100%'><stop offset='0%' stop-color='{portrait_color}' stop-opacity='0.25'/><stop offset='100%' stop-color='{portrait_color}' stop-opacity='0.0'/></linearGradient></defs><path d='M250,200 C190,200 150,260 150,340 C150,420 190,480 250,480 C310,480 350,420 350,340 C350,260 310,200 250,200 Z M60,800 C60,650 120,550 210,510 C230,500 270,500 290,510 C380,550 440,650 440,800 Z' fill='url(%23grad)'/></svg>"
    
    # 2. A subtle geometric dot pattern
    pattern_svg = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'><rect width='24' height='24' fill='none'/><circle cx='3' cy='3' r='1.5' fill='{portrait_color}' opacity='{pattern_opacity}'/></svg>"

    css = f"""/* Layered Flanking Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-container {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    max-height: 100vh;
    background-color: var(--bg);
    /* Multiple backgrounds: portrait on top of pattern */
    background-image: 
        url("{portrait_svg}"),
        url("{pattern_svg}");
    background-position: bottom center, center;
    background-size: auto 90%, 24px 24px;
    background-repeat: no-repeat, repeat;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15%; /* Creates the central void for the portrait */
    padding: 0 5%;
    position: relative;
    overflow: hidden;
    color: var(--text);
}}

/* Left Side: Heavy Introduction */
.main-intro {{
    flex: 1;
    max-width: 420px;
    z-index: 10;
    opacity: 0; /* Handled by JS */
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    opacity: 0.85;
}}

.btn-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 0.8rem 2rem;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.3s ease, transform 0.3s ease;
}}

.btn-cta:hover {{
    filter: brightness(1.15);
    transform: translateY(-3px);
}}

/* Right Side: Staggered Quotes */
.main-quotes {{
    flex: 1;
    max-width: 380px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
}}

.quote {{
    border-left: 4px solid var(--accent);
    padding-left: 1.5rem;
    opacity: 0; /* Handled by JS */
}}

/* Break the grid with an offset on the second quote */
.quote:nth-child(even) {{
    margin-left: 4rem;
}}

.quote p {{
    font-size: 1.05rem;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 0.75rem;
    opacity: 0.85;
}}

.quote small {{
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layered Flanking Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text.replace('\\n', '<br>')}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn-cta">My Work</a>
        </div>

        <div class="main-quotes">
            <div class="quote">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <small>— Dr. Seuss</small>
            </div>
            <div class="quote">
                <p>"An investment in knowledge pays the best interest."</p>
                <small>— Benjamin Franklin</small>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const intro = document.querySelector('.main-intro');
    const quotes = document.querySelectorAll('.quote');

    // Trigger staggered slide-in animations
    setTimeout(() => {
        intro.style.transition = 'opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)';
        intro.style.opacity = '1';
        intro.style.transform = 'translateX(0)';
    }, 100);

    // Initial state set here to avoid flash before JS runs
    intro.style.transform = 'translateX(-40px)';

    quotes.forEach((quote, index) => {
        quote.style.transform = 'translateX(40px)';
        
        setTimeout(() => {
            quote.style.transition = `opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) ${200 + (index * 200)}ms, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) ${200 + (index * 200)}ms`;
            quote.style.opacity = '1';
            quote.style.transform = 'translateX(0)';
        }, 100);
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
