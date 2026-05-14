def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "This layout uses multiple CSS backgrounds to layer a subject over a textured canvas. The split flexbox design naturally frames the focal point.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Column Layered Background Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        quote_text_color = "rgba(255, 255, 255, 0.85)"
        pattern_color = "%23141d2e" # URL encoded #141d2e
        portrait_color = "%230d131c" # URL encoded silhouette color
    else:
        bg_color = "#E2E8F0"
        text_color = "#1E293B"
        quote_text_color = "rgba(30, 41, 59, 0.85)"
        pattern_color = "%23cbd5e1"
        portrait_color = "%2394a3b8"

    # SVG Data URIs for self-contained assets
    # 1. Repeating geometric pattern
    svg_pattern = f"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='{pattern_color}' fill-opacity='1' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E"
    
    # 2. Generic person silhouette portrait (Bottom-aligned)
    svg_portrait = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath fill='{portrait_color}' d='M200 50c-40 0-70 30-70 75s30 85 70 85 70-40 70-85-30-75-70-75zm-90 180c-45 0-80 40-80 90v180h340V320c0-50-35-90-80-90H110z'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Dual-Column Layered Background Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    position: relative;
    background-color: var(--bg-color);
    
    /* MULTIPLE BACKGROUNDS: Foreground subject stacked over Background pattern */
    background-image: 
        url("{svg_portrait}"), 
        url("{svg_pattern}");
    
    /* Foreground scales to 75% height, pattern repeats */
    background-size: 
        auto 75%, 
        40px 40px;
    
    /* Foreground anchored bottom center, pattern fills */
    background-position: 
        bottom center, 
        top left;
    
    background-repeat: 
        no-repeat, 
        repeat;
        
    /* Layout */
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8vw;
    padding: 0 4vw;
    overflow: hidden;
}}

/* === LEFT COLUMN: INTRO === */
.main-intro {{
    position: relative;
    flex: 1;
    max-width: 450px;
    /* Pushed slightly left to clear the central portrait */
    transform: translateX(-2vw);
    z-index: 2;
}}

.main-intro h1 {{
    color: var(--text-color);
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 900;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    color: var(--text-color);
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2rem;
}}

.btn-accent {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.btn-accent:hover {{
    filter: brightness(1.2);
    transform: translateY(-2px);
}}

/* === RIGHT COLUMN: QUOTES === */
.main-quotes {{
    position: relative;
    flex: 1;
    max-width: 400px;
    z-index: 2;
}}

.main-quotes p {{
    color: var(--quote-color);
    font-size: 1rem;
    line-height: 1.6;
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 2.5rem;
    font-style: italic;
}}

/* The staggered offset effect from the tutorial */
.main-quotes p:nth-child(even) {{
    margin-left: 80px;
}}

.quote-author {{
    display: block;
    margin-top: 10px;
    font-weight: 700;
    font-style: normal;
    color: var(--text-color);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        text-align: center;
        gap: 2rem;
        /* Dim portrait on mobile to ensure text readability */
        background-image: 
            linear-gradient(rgba(26, 37, 58, 0.8), rgba(26, 37, 58, 0.8)),
            url("{svg_portrait}"), 
            url("{svg_pattern}");
    }}
    
    .main-intro {{ transform: none; max-width: 600px; }}
    
    .main-quotes p {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 15px;
        text-align: center;
    }}
    
    .main-quotes p:nth-child(even) {{
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
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn-accent">My Work</a>
        </div>

        <div class="main-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>
                "For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JS required for this pure CSS layout pattern.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Dual-Column Layered Hero initialized.");
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
