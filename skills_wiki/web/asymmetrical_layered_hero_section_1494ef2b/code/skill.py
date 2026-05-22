def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    cta_text: str = "MY WORK",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Layered Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base Text overrides mapping to tutorial defaults
    quote1_text = kwargs.get("quote1_text", '"The more that you read, the more things you will know. The more that you learn, the more places you\'ll go."<br><br>- Dr. Seuss')
    quote2_text = kwargs.get("quote2_text", '"For the best return on your money, pour your purse into your head."<br><br>- Benjamin Franklin')

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.04)"

    css = f"""/* Asymmetrical Layered Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --pattern: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Main Component Wrapper */
.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    background-color: var(--bg);
    
    /* Simulate layered background image and central portrait glow */
    background-image: 
        radial-gradient(circle at bottom center, color-mix(in srgb, var(--accent) 15%, transparent) 0%, transparent 65%),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern)),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern));
    background-size: 100% 100%, 40px 40px, 40px 40px;
    background-position: bottom center, 0 0, 20px 20px;
    
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    color: var(--text);
}}

/* Left Column: Introduction */
.hero-intro {{
    position: relative;
    right: 12%; /* Offset left to create central void */
    max-width: 420px;
    z-index: 10;
}}

.hero-intro h1 {{
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -1px;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-top: 1.5rem;
    opacity: 0.9;
}}

.hero-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 0.75rem 1.75rem;
    margin-top: 2rem;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 0.875rem;
    letter-spacing: 0.5px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.hero-cta:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Column: Quotes & Supporting Info */
.hero-quotes {{
    position: relative;
    left: 8%; /* Offset right */
    max-width: 360px;
    z-index: 10;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Staggered effect for the second quote */
.hero-quotes p:nth-child(2) {{
    margin-left: 4rem;
}}

/* Responsive Fallback */
@media (max-width: 960px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 4rem;
        padding-bottom: 4rem;
        height: auto;
        min-height: var(--height);
    }}
    
    .hero-intro, 
    .hero-quotes {{
        position: static;
        max-width: 600px;
        width: 90%;
        margin-bottom: 3rem;
    }}
    
    .hero-quotes p:nth-child(2) {{
        margin-left: 2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <div class="hero-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="hero-cta">{cta_text}</a>
        </div>

        <div class="hero-quotes">
            <p>{quote1_text}</p>
            <p>{quote2_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Asymmetrical Layered Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // Layout operates entirely on CSS Flexbox and Relative Positioning.
    // No JS strictly required for layout logic.
    console.log("Hero component loaded successfully.");
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
