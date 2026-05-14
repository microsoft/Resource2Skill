def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split Flexbox Hero with Layered Background Portrait' layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and SVG fills ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        svg_fill = "%23ffffff"
        pattern_opacity = "0.03"
        portrait_opacity = "0.08"
    else:
        bg_color = "#f4f7f6"
        text_color = "#111827"
        svg_fill = "%23000000"
        pattern_opacity = "0.04"
        portrait_opacity = "0.06"

    # SVG Data URIs to ensure self-contained rendering
    # 1. Silhouette portrait for foreground
    portrait_svg = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><path d='M200 220c-44.1 0-80-35.9-80-80s35.9-80 80-80 80 35.9 80 80-35.9 80-80 80zm-120 180v-40c0-66.3 53.7-120 120-120s120 53.7 120 120v40H80z' fill='{svg_fill}' fill-opacity='{portrait_opacity}'/></svg>"
    # 2. Geometric pattern for background
    pattern_svg = f"data:image/svg+xml;utf8,<svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'><g fill='none' fill-rule='evenodd'><g fill='{svg_fill}' fill-opacity='{pattern_opacity}'><path d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/></g></g></svg>"

    # === CSS ===
    css = f"""/* Split Flexbox Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
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
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    color: var(--text-color);
    position: relative;
    overflow: hidden;
    
    /* MULTIPLE BACKGROUNDS: Portrait on top of geometric pattern */
    background-image: 
        url("{portrait_svg}"), 
        url("{pattern_svg}");
    background-position: bottom center, center;
    background-size: 60%, auto;
    background-repeat: no-repeat, repeat;
    
    /* Layout */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 40px 6vw;
}}

/* === Left Column: Intro === */
.main-intro {{
    position: relative;
    max-width: 420px;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    opacity: 0.9;
    margin-bottom: 36px;
}}

.btn-work {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 14px 32px;
    font-size: 16px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.btn-work:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* === Right Column: Quotes === */
.main-quotes {{
    position: relative;
    max-width: 380px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
}}

.quote-block p {{
    font-size: 16px;
    line-height: 28px;
    opacity: 0.85;
}}

/* The signature stagger effect from the tutorial */
.quote-block:nth-child(2) {{
    margin-left: 60px;
}}

/* Animation classes applied via JS */
.fade-up {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.fade-up.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 60px;
        background-size: 80%, auto;
        padding-top: 80px;
        padding-bottom: 80px;
        overflow-y: auto;
    }}

    .main-intro, .main-quotes {{
        max-width: 100%;
    }}

    .quote-block {{
        text-align: left;
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 16px;
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
    <title>Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-container">
        
        <!-- Left Side -->
        <div class="main-intro">
            <h1 class="fade-up">{title_text}</h1>
            <p class="fade-up">{body_text}</p>
            <a href="#" class="btn-work fade-up">My Work</a>
        </div>

        <!-- Right Side -->
        <div class="main-quotes">
            <div class="quote-block fade-up">
                <p>"The more that you read, the more<br>things you will know. The more that<br>you learn, the more places you'll go."<br><br>- Dr. Seuss</p>
            </div>
            
            <div class="quote-block fade-up">
                <p>"For the best return on your<br>money, pour your purse<br>into your head."<br><br>- Benjamin Franklin</p>
            </div>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entrance animation logic
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Determine stagger delay based on DOM order
                const elements = Array.from(document.querySelectorAll('.fade-up'));
                const index = elements.indexOf(entry.target);
                
                // Apply a slight delay to each subsequent element
                entry.target.style.transitionDelay = `${{index * 0.15}}s`;
                entry.target.classList.add('visible');
                
                // Stop observing once animated
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    const animatedElements = document.querySelectorAll('.fade-up');
    animatedElements.forEach(el => observer.observe(el));
}});
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
