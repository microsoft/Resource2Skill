def create_component(
    output_dir: str,
    title_text: str = "Welcome<br>To My First<br>Website",
    body_text: str = "We extract the essence of web design patterns and distill them into reusable code.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584", 
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Layered Hero layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base themes
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        # Dark grid pattern
        pattern_color = "rgba(0, 0, 0, 0.2)"
        silhouette_color = "%23ffffff" # URL encoded hex
        silhouette_opacity = "0.05"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        text_muted = "rgba(0, 0, 0, 0.7)"
        # Light grid pattern
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "%23000000" # URL encoded hex
        silhouette_opacity = "0.05"

    # SVG Data URI for the foreground portrait/subject to ensure self-contained execution
    # This creates a stylistic, abstract bust/silhouette
    svg_portrait = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><path d='M200 200c-44.18 0-80-35.82-80-80s35.82-80 80-80 80 35.82 80 80-35.82 80-80 80zm-120 200v-40c0-66.27 53.73-120 120-120h0c66.27 0 120 53.73 120 120v40H80z' fill='{silhouette_color}' fill-opacity='{silhouette_opacity}'/></svg>"

    css = f"""/* Split-Content Layered Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* The Core Hero Pattern */
.hero-main {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    
    /* Dual Background Logic: 
       Layer 1 (Top): The Portrait/Subject anchored bottom center
       Layer 2 (Bottom): The repeating texture/pattern */
    background-image: 
        url("{svg_portrait}"),
        radial-gradient({pattern_color} 2px, transparent 2px);
        
    background-position: bottom center, 0 0;
    /* Scale the portrait using viewport height, repeat the pattern */
    background-size: 70vh, 32px 32px;
    background-repeat: no-repeat, repeat;
    
    /* Layout */
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4rem;
    overflow: hidden;
}}

/* Left Pane: Primary Intro */
.main-intro {{
    flex: 1;
    max-width: 450px;
    z-index: 2; /* Ensure text sits above the background layers */
}}

.main-intro h1 {{
    font-size: 56px;
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 32px;
}}

.cta-button {{
    display: inline-block;
    padding: 14px 32px;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 14px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Pane: Secondary Quotes/Context */
.main-quotes {{
    flex: 1;
    max-width: 380px;
    z-index: 2;
}}

/* Visual Anchor/Divider Strategy */
.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 24px;
    margin-bottom: 32px;
}}

.quote-block:last-child {{
    margin-bottom: 0;
    margin-left: 40px; /* Offset the second block for staggered editorial look */
}}

.quote-text {{
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 12px;
    font-style: italic;
}}

.quote-author {{
    font-size: 14px;
    font-weight: 700;
    color: var(--text-muted);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: center;
        gap: 4rem;
        text-align: center;
        background-position: center center, 0 0;
        background-size: 60vh, 32px 32px;
    }}
    
    .quote-block {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 24px;
    }}
    
    .quote-block:last-child {{
        margin-left: 0;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Content Hero Pattern</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,700;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-main">
        
        <!-- Left Side: Primary Content -->
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#work" class="cta-button">My Work</a>
        </section>

        <!-- Right Side: Secondary Content (Quotes) -->
        <section class="main-quotes">
            <div class="quote-block">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            
            <div class="quote-block">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </section>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JavaScript required for this core CSS pattern.
// Hover states and parallax-like layering are handled entirely via CSS backgrounds and flexbox flow.
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
