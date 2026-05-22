def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY SITE",
    body_text: str = "A showcase of creative development and visual design. Building experiences that blend aesthetics with functionality.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Layout Hero with Central Void' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Establish theme colors based on scheme
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.85)"
        pattern_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#111827"
        text_muted = "rgba(0, 0, 0, 0.7)"
        pattern_color = "rgba(0, 0, 0, 0.04)"

    css = f"""/* Split-Layout Hero CSS */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap');

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --pattern-color: {pattern_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Container mapping to requested dimensions */
.hero-wrapper {{
    width: var(--container-width);
    height: var(--container-height);
    max-width: 100vw;
    background-color: var(--bg-color);
    
    /* Simulate the layered background (pattern + central light/subject) */
    background-image: 
        radial-gradient(ellipse at bottom center, var(--pattern-color) 0%, transparent 60%),
        linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color)),
        linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color));
    background-size: 100% 100%, 40px 40px, 40px 40px;
    background-position: center, 0 0, 20px 20px;
    
    color: var(--text-color);
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* The central "void" placeholder - simulates the portrait image from the tutorial */
.hero-subject-silhouette {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 400px;
    height: 80%;
    background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
    border-radius: 200px 200px 0 0;
    opacity: 0.3;
    pointer-events: none;
    z-index: 1;
}}

/* Main Flex Layout for content */
.hero-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1400px;
    padding: 0 4rem;
    z-index: 2; /* Keep text above the background subject */
}}

/* Left Column - Intro */
.main-intro {{
    flex: 0 1 500px;
    /* Pushing it slightly out from the center as done in the video */
    position: relative;
    right: 2vw; 
    padding-bottom: 4vh;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    line-height: 1.05;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    color: var(--text-muted);
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Button text is always white */
    text-decoration: none;
    padding: 12px 32px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.875rem;
    transition: filter 0.2s ease, transform 0.2s ease;
    width: fit-content;
}}

.cta-button:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* Right Column - Quotes */
.main-quotes {{
    flex: 0 1 350px;
    /* Pushing it slightly out to the right */
    position: relative;
    left: 2vw;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
    margin: 2.5rem 0;
}}

.quote-block p {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}}

.quote-block cite {{
    font-size: 0.875rem;
    font-weight: 700;
    font-style: normal;
    color: var(--text-color);
}}

/* Staggering the quotes for an editorial look */
.quote-block:nth-child(2) {{
    margin-left: 80px;
}}

/* Responsive behavior */
@media (max-width: 968px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        gap: 4rem;
        padding: 2rem;
    }}
    
    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        flex: 1 1 auto;
        width: 100%;
        max-width: 600px;
        text-align: center;
    }}
    
    .quote-block {{
        text-align: left; /* Keep quote text left-aligned despite container centering */
    }}
    
    .quote-block:nth-child(2) {{
        margin-left: 40px;
    }}
    
    .hero-subject-silhouette {{
        opacity: 0.1; /* Fade out more on mobile to prevent text clash */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Layout Hero Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <!-- Visual placeholder representing the portrait image from the tutorial -->
        <div class="hero-subject-silhouette"></div>
        
        <main class="hero-content">
            
            <div class="main-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-button">My Work</a>
            </div>

            <div class="main-quotes">
                <div class="quote-block">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <cite>- Dr. Seuss</cite>
                </div>
                
                <div class="quote-block">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <cite>- Benjamin Franklin</cite>
                </div>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic for CTA hover effect tracking (optional enhancement)
document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.cta-button');
    
    button.addEventListener('mousedown', () => {
        button.style.transform = 'scale(0.95)';
    });
    
    button.addEventListener('mouseup', () => {
        button.style.transform = 'translateY(-2px)';
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = '';
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
