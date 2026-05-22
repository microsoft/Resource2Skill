def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "The more that you read, the more things you will know. The more that you learn, the more places you'll go.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Focus Hero Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme variables
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_color = "#ffffff"
        btn_text = "#ffffff"
        bg_pattern_fill = "rgba(0,0,0,0.15)"
        fg_subject_fill = "rgba(255,255,255,0.03)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        btn_text = "#ffffff"
        bg_pattern_fill = "rgba(0,0,0,0.03)"
        fg_subject_fill = "rgba(0,0,0,0.05)"

    # SVG Data URIs for offline-capable backgrounds
    # 1. Pattern (background)
    svg_pattern = f"""<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M0,0 L20,20 L0,40 Z' fill='{bg_pattern_fill}'/></svg>"""
    import urllib.parse
    pattern_url = f"data:image/svg+xml;utf8,{urllib.parse.quote(svg_pattern)}"

    # 2. Subject Cutout (foreground)
    svg_subject = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><path d='M50,200 C50,110 80,70 100,70 C120,70 150,110 150,200 Z' fill='{fg_subject_fill}'/><circle cx='100' cy='45' r='25' fill='{fg_subject_fill}'/></svg>"""
    subject_url = f"data:image/svg+xml;utf8,{urllib.parse.quote(svg_subject)}"

    # === CSS ===
    css = f"""/* Split-Focus Hero Layout */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --btn-text: {btn_text};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-wrapper {{
    width: var(--container-width);
    height: var(--container-height);
    max-width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
    padding-bottom: 8vh; /* Slight upward shift */
    
    /* Core Pattern: Layered Multiple Backgrounds */
    background-image: 
        url("{subject_url}"), 
        url("{pattern_url}");
    background-size: 
        80vh, 
        40px 40px;
    background-repeat: 
        no-repeat, 
        repeat;
    background-position: 
        bottom center, 
        center;
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 12vw; /* Push away from center void */
    max-width: 400px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.btn-primary {{
    display: inline-block;
    background-color: var(--accent-color);
    color: var(--btn-text);
    text-decoration: none;
    padding: 12px 28px;
    font-size: 0.875rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-top: 1rem;
    transition: opacity 0.2s ease, transform 0.2s ease;
}}

.btn-primary:hover {{
    opacity: 0.85;
    transform: translateY(-2px);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 8vw; /* Push away from center void */
    max-width: 360px;
    z-index: 10;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 2.5rem;
}}

.quote-block p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 0.75rem;
    font-style: italic;
}}

.quote-block small {{
    font-size: 0.875rem;
    font-weight: 600;
    opacity: 0.8;
}}

/* Staggered Rhythm logic from tutorial */
.quote-block:nth-child(2) {{
    margin-left: 60px;
}}

/* Responsive Fallback */
@media (max-width: 1000px) {{
    .hero-wrapper {{
        flex-direction: column;
        height: auto;
        min-height: var(--container-height);
        background-size: 50vh, 40px 40px;
        padding: 4rem 2rem;
    }}
    .main-intro, .main-quotes {{
        position: static;
        width: 100%;
        max-width: 600px;
        margin: 2rem 0;
        text-align: center;
    }}
    .quote-block {{
        text-align: left;
    }}
    .quote-block:nth-child(2) {{
        margin-left: 0;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Extract</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        
        <!-- Left Side -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <a href="#" class="btn-primary">My Work</a>
        </div>

        <!-- Right Side -->
        <div class="main-quotes">
            <div class="quote-block">
                <p>"{body_text}"</p>
                <small>- Dr. Seuss</small>
            </div>
            <div class="quote-block">
                <p>"An investment in knowledge pays the best interest."</p>
                <small>- Benjamin Franklin</small>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS implementation based on tutorial logic.
// JS included for future intersection observer extensions if needed.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero section loaded successfully.");
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
        "files": files
    }
