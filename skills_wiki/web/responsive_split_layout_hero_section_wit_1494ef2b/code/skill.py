def create_component(
    output_dir: str,
    title_text: str = "Welcome<br>to my first<br>website",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        surface_color = "rgba(255, 255, 255, 0.05)"
        svg_fill = "ffffff"
    else:
        bg_color = "#E5E9F0"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.06)"
        svg_fill = "000000"

    # A self-contained SVG silhouette to mimic the portrait background image in the tutorial
    svg_data = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'><circle cx='100' cy='80' r='50' fill='%23{svg_fill}' opacity='0.15'/><path d='M20 300 C20 180, 180 180, 180 300 Z' fill='%23{svg_fill}' opacity='0.15'/></svg>"

    # === CSS ===
    css = f"""/* Responsive Split-Layout Hero Section */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* Mock Header for layout context */
.site-header {{
    height: 60px;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    background-color: var(--bg);
    border-bottom: 1px solid var(--surface);
    z-index: 1000;
    display: flex;
    align-items: center;
    padding: 0 40px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.hero-main {{
    margin-top: 60px;
    height: calc(100vh - 60px);
    min-height: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    /* Layer 1: Geometric Pattern */
    background-image: radial-gradient(circle at 10px 10px, var(--surface) 2px, transparent 0);
    background-size: 30px 30px;
    background-position: top left;
}}

/* Layer 2: Center Portrait Placeholder */
.hero-main::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 70vh;
    height: 70vh;
    background-image: url("{svg_data}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: bottom center;
    z-index: 1;
    pointer-events: none;
}}

.main-intro {{
    position: relative;
    right: 12vw;
    width: 100%;
    max-width: 450px;
    z-index: 2;
    padding-bottom: 8vh;
}}

.main-intro h1 {{
    font-size: clamp(40px, 6vw, 96px);
    line-height: 1.1;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: 30px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 40px;
    opacity: 0.9;
}}

.main-intro a.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 16px 32px;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.main-intro a.btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

.main-quotes {{
    position: relative;
    left: 4vw;
    width: 100%;
    max-width: 380px;
    z-index: 2;
    padding-bottom: 4vh;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.7;
    font-style: italic;
}}

.main-quotes p strong {{
    display: block;
    margin-top: 10px;
    font-style: normal;
    font-size: 14px;
    opacity: 0.7;
}}

/* The Core Technique: Staggering siblings without extra classes */
.main-quotes p:nth-child(2) {{
    margin-left: 80px;
}}

/* Responsive Graceful Degradation */
@media (max-width: 1024px) {{
    .hero-main {{
        flex-direction: column;
        padding: 40px 20px;
        height: auto;
        min-height: 100vh;
    }}
    
    .hero-main::after {{
        opacity: 0.3; /* Push placeholder further back visually */
        width: 100vw;
    }}

    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        margin-bottom: 40px;
        max-width: 100%;
        padding-bottom: 0;
    }}

    .main-quotes p:nth-child(2) {{
        margin-left: 40px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="site-header">
        Brand Logo
    </header>

    <main class="hero-main">
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>
        
        <div class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <strong>- Dr. Seuss</strong>
            </p>
            <p>"For the best return on your money, pour your purse into your head."
                <strong>- Benjamin Franklin</strong>
            </p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Split-Layout Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // The core layout is driven purely by CSS Flexbox and Viewport calculation.
    // JS is reserved for interactive enhancements if added later.
    console.log("Hero Section loaded successfully.");
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
