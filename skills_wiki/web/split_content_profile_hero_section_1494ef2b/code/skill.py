def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY<br>FIRST WEBSITE",
    body_text: str = "I am a frontend developer focused on creating clean, engaging, and responsive user experiences.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#C13584",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Profile Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert newlines to HTML breaks if provided instead of <br>
    title_text = title_text.replace("\n", "<br>")

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.04)"
        silhouette_fill = "%23ffffff"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_fill = "%23000000"

    # Hover color (slightly darker by adjusting opacity for simplicity in this script, 
    # though true color math is better in production)
    accent_hover = f"{accent_color}dd" 

    css = f"""/* Split-Content Profile Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --accent-hover: {accent_hover};
    --pattern-color: {pattern_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-wrapper {{
    width: 100%;
    height: var(--container-height);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-color);
}}

/* Dotted background pattern */
.hero-wrapper::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(var(--pattern-color) 1.5px, transparent 1.5px);
    background-size: 24px 24px;
    z-index: 0;
}}

/* Central Anchor (Simulating the cut-out portrait) */
.hero-portrait {{
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 450px;
    height: 85%;
    /* Using an SVG silhouette as a robust placeholder for the portrait image */
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 250"><path fill="{silhouette_fill}" opacity="0.08" d="M100,20 C65,20 45,45 45,80 C45,115 65,135 100,135 C135,135 155,115 155,80 C155,45 135,20 100,20 Z M15,250 C15,180 45,155 100,155 C155,155 185,180 185,250 Z"/></svg>');
    background-size: contain;
    background-position: bottom center;
    background-repeat: no-repeat;
    z-index: 1;
    pointer-events: none;
}}

.hero-content {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: var(--container-width);
    padding: 0 40px;
    gap: 20px;
}}

/* Left Column: Intro */
.hero-intro {{
    flex: 1;
    max-width: 480px;
}}

.hero-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: 24px;
    letter-spacing: -1px;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 32px;
    opacity: 0.9;
    max-width: 90%;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 28px;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.875rem;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.btn:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}}

/* Right Column: Quotes */
.hero-quotes {{
    flex: 1;
    max-width: 380px;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
}}

/* Staggering the second quote as done in the tutorial */
.quote:nth-child(2) {{
    transform: translateX(40px);
}}

.quote p {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    opacity: 0.9;
    margin-bottom: 12px;
}}

.quote .author {{
    display: block;
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--accent-color);
}}

/* Responsive behavior */
@media (max-width: 960px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 60px;
    }}
    
    .hero-intro, .hero-quotes {{
        max-width: 600px;
    }}
    
    .hero-intro p {{
        margin: 0 auto 32px auto;
    }}
    
    .quote {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 20px;
        text-align: center;
    }}
    
    .quote:nth-child(2) {{
        transform: translateX(0);
    }}
    
    .hero-portrait {{
        opacity: 0.3; /* Fade back so text is readable if overlapping */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        <!-- Abstract Silhouette representing the portrait -->
        <div class="hero-portrait"></div>

        <div class="hero-content">
            <!-- Left Side: Introduction -->
            <div class="hero-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">MY WORK</a>
            </div>

            <!-- Right Side: Quotes -->
            <div class="hero-quotes">
                <div class="quote">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <span class="author">— Dr. Seuss</span>
                </div>
                <div class="quote">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <span class="author">— Benjamin Franklin</span>
                </div>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JavaScript required for this static layout pattern.
// Smooth scrolling or entrance animations could be added here in the future.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Hero section loaded.');
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
