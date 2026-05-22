def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Portrait-Centric Split-Content Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on video styling
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        quote_text_color = "#E2E8F0"
    else:
        bg_color = "#F8FAFC"
        text_color = "#0F172A"
        quote_text_color = "#334155"

    # SVG Data URIs for self-contained reproduction
    # 1. A subtle geometric pattern for the background
    pattern_svg = "data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2z' fill='rgba(0,0,0,0.05)' fill-rule='evenodd'/%3E%3C/svg%3E"
    
    # 2. A generic portrait silhouette to represent the central subject
    portrait_svg = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath fill='rgba(0,0,0,0.4)' d='M200 250c-44.18 0-80-35.82-80-80s35.82-80 80-80 80 35.82 80 80-35.82 80-80 80zm-120 250c0-88.37 71.63-160 160-160h-80c88.37 0 160 71.63 160 160H80z'/%3E%3C/svg%3E"

    css = f"""/* Portrait-Centric Split-Content Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent-color: {accent_color};
    /* Calculate a darker hover state dynamically using color-mix if supported, or fallback to opacity */
    --accent-hover: {accent_color}cc; 
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', 'Inter', system-ui, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* The main bounded container reproducing the video's viewport */
.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    background-color: var(--bg-color);
    
    /* Multiple backgrounds: Portrait on top, Pattern on bottom */
    background-image: 
        url("{portrait_svg}"),
        url("{pattern_svg}");
    background-position: 
        bottom center,
        center;
    background-size: 
        60% auto, /* Portrait size */
        40px 40px; /* Pattern size */
    background-repeat: 
        no-repeat,
        repeat;
        
    /* Flex layout pushes content to left and right */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 8%;
    overflow: hidden;
    color: var(--text-color);
}}

/* Left Column: Main Introduction */
.main-intro {{
    flex: 0 1 400px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 900;
    line-height: 1.05;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    color: var(--quote-color);
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 12px 28px;
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: background-color 0.3s ease;
}}

.btn:hover {{
    background-color: var(--accent-hover);
}}

/* Right Column: Quotes */
.main-quotes {{
    flex: 0 1 350px;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    z-index: 10;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
}}

.quote-text {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    color: var(--quote-color);
    margin-bottom: 1rem;
}}

.quote-author {{
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-color);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 3rem;
        padding: 4rem 8%;
        text-align: center;
        background-position: bottom right -20%, center;
        background-size: 80% auto, 40px 40px;
    }}
    
    .main-intro h1 {{
        font-size: 2.5rem;
    }}
    
    .main-quotes {{
        gap: 2rem;
    }}
    
    .quote-block {{
        text-align: left;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-container">
        
        <!-- Left Side Content -->
        <div class="main-intro">
            <h1>{title_text.replace(" ", "<br>")}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <!-- Right Side Quotes -->
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

    js = """// Simple interaction: Add a subtle entrance animation to the content
document.addEventListener('DOMContentLoaded', () => {
    const intro = document.querySelector('.main-intro');
    const quotes = document.querySelectorAll('.quote-block');
    
    // Initial states
    intro.style.opacity = '0';
    intro.style.transform = 'translateY(20px)';
    intro.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    
    quotes.forEach((q, i) => {
        q.style.opacity = '0';
        q.style.transform = 'translateX(20px)';
        q.style.transition = `opacity 0.8s ease ${i * 0.2 + 0.3}s, transform 0.8s ease ${i * 0.2 + 0.3}s`;
    });
    
    // Trigger animation
    setTimeout(() => {
        intro.style.opacity = '1';
        intro.style.transform = 'translateY(0)';
        
        quotes.forEach(q => {
            q.style.opacity = '1';
            q.style.transform = 'translateX(0)';
        });
    }, 100);
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
