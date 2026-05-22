def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "I build interactive, immersive web experiences designed to capture attention and deliver value.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#c13584",     # CSS hex color for accent (Magenta)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Focal Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        pattern_opacity = "0.05"
        svg_color = "%23ffffff" # URL encoded #ffffff
        accent_hover = "#9e2f6e"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1A253A"
        pattern_opacity = "0.08"
        svg_color = "%231A253A" # URL encoded #1A253A
        accent_hover = "#a02a6d"

    # Self-contained SVG backgrounds (Pattern and Abstract Portrait Avatar)
    pattern_svg = f"data:image/svg+xml;utf8,<svg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'><path d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2z' fill='{svg_color}' fill-opacity='{pattern_opacity}' fill-rule='evenodd'/></svg>"
    
    avatar_svg = f"data:image/svg+xml;utf8,<svg width='300' height='400' viewBox='0 0 24 24' fill='none' stroke='{svg_color}' stroke-width='0.5' stroke-linecap='round' stroke-linejoin='round' xmlns='http://www.w3.org/2000/svg'><path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'></path><circle cx='12' cy='7' r='4'></circle></svg>"

    # === CSS ===
    css = f"""/* Split-Focal Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --accent-hover: {accent_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    
    /* 
      Multiple Backgrounds:
      1st: The focal subject (Avatar SVG), anchored bottom center.
      2nd: The repeating pattern SVG.
    */
    background-image: 
        url("{avatar_svg}"),
        url("{pattern_svg}");
    background-size: 60vh, 40px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center center;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15vw; /* Creates the negative space for the focal subject */
    padding: 0 5vw;
}}

/* Left Column: Main Intro */
.main-intro {{
    max-width: 420px;
    padding-bottom: 8vh; /* Lift content above the subject's base */
    position: relative;
    z-index: 10;
    opacity: 0;
    animation: fadeInUp 0.8s ease-out forwards;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    opacity: 0.9;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Always white for contrast against accent */
    padding: 14px 28px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}}

/* Right Column: Secondary Text / Quotes */
.main-quotes {{
    max-width: 320px;
    padding-bottom: 8vh;
    padding-left: 1.5rem;
    border-left: 4px solid var(--accent-color);
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
    position: relative;
    z-index: 10;
    opacity: 0;
    animation: fadeInUp 0.8s ease-out 0.3s forwards; /* Staggered load */
}}

.quote-block p.quote-text {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    opacity: 0.85;
    margin-bottom: 0.5rem;
}}

.quote-block p.quote-author {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--accent-color);
}}

/* Load-in Animation */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive Degradation */
@media (max-width: 960px) {{
    .hero-container {{
        flex-direction: column;
        gap: 3rem;
        height: auto;
        min-height: var(--height);
        padding: 4rem 2rem;
        background-position: bottom right -20%, center center; /* Shift avatar out of the way */
        background-size: 50vh, 40px;
    }}
    
    .main-intro, .main-quotes {{
        padding-bottom: 0;
        max-width: 100%;
    }}

    .main-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 1.5rem;
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        <!-- Left Focal Content -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>
        
        <!-- Right Focal Content -->
        <div class="main-quotes">
            <div class="quote-block">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            <div class="quote-block">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Optional: Add subtle parallax to the background on mousemove
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.hero-container');
    
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Shift background position slightly for depth effect
        container.style.backgroundPosition = `calc(50% + ${x}px) bottom, calc(50% + ${x * 0.5}px) calc(50% + ${y * 0.5}px)`;
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
