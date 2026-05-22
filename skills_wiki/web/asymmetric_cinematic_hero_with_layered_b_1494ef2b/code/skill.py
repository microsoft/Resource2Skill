def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Some placeholder text here to demonstrate the visual layout, indicating what the site is about and providing context.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Cinematic Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A" # Dark slate blue from tutorial
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.7)"
    else:
        bg_color = "#F4F7F6"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"

    # CSS Content
    css = f"""/* Asymmetric Cinematic Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The main hero viewport */
.hero-section {{
    position: relative;
    width: 100%;
    max-width: var(--comp-width);
    height: var(--comp-height);
    background-color: var(--bg-color);
    /* Subtle repeating dot pattern */
    background-image: radial-gradient(var(--text-muted) 1px, transparent 1px);
    background-size: 24px 24px;
    background-position: 0 0;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

/* Central Silhouette (replacing the portrait image for self-containment) */
.hero-section::before {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: clamp(300px, 40vw, 500px);
    height: 70vh;
    max-height: 80%;
    background: linear-gradient(to top, var(--bg-color) 0%, var(--accent-color) 100%);
    opacity: 0.15;
    border-radius: 250px 250px 0 0;
    z-index: 1;
    pointer-events: none;
}}

/* Inner constraint wrapper */
.hero-content {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0 5vw;
    gap: 4rem;
}}

/* Left side: Heavy typography */
.hero-intro {{
    flex: 1;
    max-width: 550px;
}}

.hero-intro h1 {{
    color: var(--text-color);
    font-size: clamp(3rem, 6vw, 6rem); /* Scales from 48px to 96px */
    line-height: 1.1;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.hero-intro p {{
    color: var(--text-color);
    font-size: 1.125rem; /* 18px */
    line-height: 1.6;
    margin-bottom: 2.5rem;
}}

.cta-btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #fff;
    text-decoration: none;
    padding: 14px 32px;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.3s ease, transform 0.3s ease;
}}

.cta-btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right side: Offset Quotes */
.hero-quotes {{
    flex: 0 1 400px;
    border-left: 4px solid var(--accent-color);
    padding-left: 2rem;
}}

.quote-block {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 2.5rem;
}}

.quote-block strong {{
    display: block;
    margin-top: 0.5rem;
    color: var(--text-color);
    font-weight: 500;
}}

/* Asymmetric offset for the second quote */
.quote-block.offset {{
    margin-left: 3.5rem;
    margin-bottom: 0;
}}

/* Responsive breakdown */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 3rem;
    }}
    
    .hero-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 2rem;
    }}
    
    .quote-block.offset {{
        margin-left: 0;
    }}
}}
"""

    # HTML Content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Pattern</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-section">
        <div class="hero-content">
            
            <div class="hero-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-btn">My Work</a>
            </div>

            <div class="hero-quotes">
                <p class="quote-block">
                    "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                    <strong>— Dr. Seuss</strong>
                </p>
                <p class="quote-block offset">
                    "For the best return on your money, pour your purse into your head."
                    <strong>— Benjamin Franklin</strong>
                </p>
            </div>

        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>
"""

    # JS Content (Empty for this CSS-driven layout, provided for completeness)
    js = """// No JavaScript required for this purely structural and aesthetic layout.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Hero loaded successfully.');
});
"""

    # Write files
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
