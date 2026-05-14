def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "I'm a digital designer and developer focusing on crafting clean, user-centric experiences. I believe in the power of minimalism and functional design.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Content Profile Hero' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#1A1A24" # Deep navy/gray
        text_primary = "#FFFFFF"
        text_secondary = "#A0AEC0"
        pattern_color = "rgba(255, 255, 255, 0.04)"
        silhouette_color = "rgba(255, 255, 255, 0.07)"
    else:
        bg_color = "#F7FAFC"
        text_primary = "#1A202C"
        text_secondary = "#4A5568"
        pattern_color = "rgba(0, 0, 0, 0.04)"
        silhouette_color = "rgba(0, 0, 0, 0.07)"

    # URL-encode the hex color for SVG data URI
    encoded_silhouette = silhouette_color.replace('rgba(', 'rgba%28').replace(',', '%2C').replace(')', '%29').replace(' ', '')
    encoded_pattern = pattern_color.replace('rgba(', 'rgba%28').replace(',', '%2C').replace(')', '%29').replace(' ', '')

    css = f"""/* Split-Content Profile Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* 
       Layered Background: 
       1. Top layer: Central portrait placeholder (SVG silhouette)
       2. Bottom layer: Repeating tech/cube pattern (SVG pattern)
    */
    background-image: 
        url('data:image/svg+xml;utf8,<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><path d="M100 100c-16.6 0-30-13.4-30-30s13.4-30 30-30 30 13.4 30 30-13.4 30-30 30zm-45 80c0-24.9 20.1-45 45-45s45 20.1 45 45H55z" fill="{encoded_silhouette}"/></svg>'),
        url('data:image/svg+xml;utf8,<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M20 0l20 20-20 20L0 20z" fill="{encoded_pattern}" fill-rule="evenodd"/></svg>');
    background-position: bottom center, 0 0;
    background-size: auto 85%, 40px 40px;
    background-repeat: no-repeat, repeat;
    padding: 2rem;
}}

.hero-layout {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    width: 100%;
    gap: 2rem;
    z-index: 10;
}}

/* --- Left Column: Intro --- */
.hero-intro {{
    flex: 1 1 350px;
    max-width: 450px;
    /* Pushed up slightly to create asymmetry */
    transform: translateY(-3rem);
}}

.hero-intro h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 900;
    text-transform: uppercase;
    line-height: 1.05;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.hero-intro > p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 2rem;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 0.875rem 2rem;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.875rem;
    letter-spacing: 1px;
    transition: filter 0.3s ease, transform 0.3s ease;
}}

.cta-button:hover {{
    filter: brightness(1.2);
    transform: translateY(-2px);
}}

/* --- Center Spacer for Portrait --- */
.hero-spacer {{
    flex: 0 0 auto;
    width: clamp(200px, 20vw, 350px);
}}

/* --- Right Column: Quotes --- */
.hero-quotes {{
    flex: 1 1 350px;
    max-width: 400px;
    /* Pushed down slightly to create asymmetry */
    transform: translateY(3rem);
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
}}

/* Staggered layout: Indent the second quote */
.quote-block:nth-child(2) {{
    margin-left: 3.5rem;
}}

.quote-block p {{
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 0.5rem;
    font-style: italic;
}}

.quote-block cite {{
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-secondary);
    font-style: normal;
}}

/* Responsive Design */
@media (max-width: 1024px) {{
    .hero-spacer {{
        display: none; /* Hide spacer on smaller screens */
    }}
    .hero-container {{
        background-position: center center, 0 0;
        background-size: auto 60%, 40px 40px;
    }}
    .hero-intro, .hero-quotes {{
        transform: translateY(0);
        background: rgba(var(--bg-color), 0.8);
        backdrop-filter: blur(4px);
        padding: 1.5rem;
        border-radius: 8px;
    }}
    .quote-block:nth-child(2) {{
        margin-left: 1.5rem; /* Reduce stagger on small screens */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Profile Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-container">
        <div class="hero-layout">
            
            <!-- Left Side: Introduction -->
            <div class="hero-intro">
                <h1>{title_text.replace(chr(10), '<br>')}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-button">My Work</a>
            </div>

            <!-- Center Spacer (Allows background portrait to show through) -->
            <div class="hero-spacer"></div>

            <!-- Right Side: Quotes -->
            <div class="hero-quotes">
                <blockquote class="quote-block">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <cite>— Dr. Seuss</cite>
                </blockquote>
                
                <blockquote class="quote-block">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <cite>— Benjamin Franklin</cite>
                </blockquote>
            </div>

        </div>
    </section>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic (Reserved for future expansion, e.g., scroll parallax)
document.addEventListener('DOMContentLoaded', () => {
    // Component is heavily CSS-driven. 
    // JavaScript can be added here for scroll-triggered fades or parallax background movement.
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
