def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Relative Offset Split Hero' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_main = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        silhouette_color = "%23ffffff"
        silhouette_opacity = "0.15"
        pattern_color = "rgba(255,255,255,0.03)"
    else:
        bg_color = "#f0f4f8"
        text_main = "#111827"
        text_muted = "rgba(0, 0, 0, 0.7)"
        silhouette_color = "%23000000"
        silhouette_opacity = "0.10"
        pattern_color = "rgba(0,0,0,0.03)"

    # Base64 encoded SVG of a portrait silhouette for self-contained rendering
    svg_data = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E%3Cpath d='M100,400 C100,250 150,200 200,200 C250,200 300,250 300,400' fill='{silhouette_color}' fill-opacity='{silhouette_opacity}'/%3E%3Ccircle cx='200' cy='120' r='60' fill='{silhouette_color}' fill-opacity='{silhouette_opacity}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Relative Offset Split Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    /* Layered Background: Silhouette + Repeating Tech Pattern */
    background-image: 
        url("{svg_data}"),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color}),
        linear-gradient(45deg, {pattern_color} 25%, transparent 25%, transparent 75%, {pattern_color} 75%, {pattern_color});
    background-size: 
        65vh, 
        20px 20px, 
        20px 20px;
    background-position: 
        bottom center, 
        0 0, 
        10px 10px;
    background-repeat: 
        no-repeat, 
        repeat, 
        repeat;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    color: var(--text-main);
}}

/* -- Left Block (Intro) -- */
.main-intro {{
    /* The key mechanical layout choice: Offset from center */
    position: relative;
    right: 15%; 
    z-index: 2;
    max-width: 40%;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 5.5rem);
    line-height: 1.1;
    text-transform: uppercase;
    margin-bottom: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 30px;
    color: var(--text-muted);
    max-width: 400px;
}}

.main-intro a {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    padding: 14px 32px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.95rem;
    transition: transform 0.2s ease, filter 0.2s ease;
}}

.main-intro a:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* -- Right Block (Quotes) -- */
.main-quotes {{
    /* Pushed to the right to open the center stage */
    position: relative;
    left: 5%;
    z-index: 2;
    max-width: 30%;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 40px;
    color: var(--text-muted);
    font-style: italic;
}}

/* Stagger the second quote visually */
.main-quotes p:nth-child(2) {{
    margin-left: 60px;
}}

.quote-author {{
    display: block;
    margin-top: 12px;
    font-weight: 600;
    font-style: normal;
    color: var(--text-main);
}}

/* -- Graceful fallback for narrow containers -- */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        text-align: center;
        background-size: 40vh, 20px 20px, 20px 20px;
    }}
    .main-intro, .main-quotes {{
        position: static;
        max-width: 80%;
        margin: 20px 0;
    }}
    .main-intro p {{
        margin-left: auto;
        margin-right: auto;
    }}
    .main-quotes p {{
        text-align: left;
    }}
    .main-quotes p:nth-child(2) {{
        margin-left: 0; /* flatten the stagger on mobile */
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#work">My Work</a>
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

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required for this static structural pattern.
// Hover states and layout mechanics are handled entirely in CSS.
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
