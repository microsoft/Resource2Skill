def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "This layout balances strong, aggressive typography on the left with asymmetric, supportive social proof on the right.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        quote_text_color = "rgba(255, 255, 255, 0.85)"
        accent_hover = "#9e2f6e"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        quote_text_color = "rgba(26, 37, 58, 0.85)"
        accent_hover = "#a1276b"

    # === CSS ===
    css = f"""/* Split-Layout Typography Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent-color: {accent_color};
    --accent-hover: {accent_hover};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Hero Main Container */
.hero-main {{
    width: 100%;
    max-width: var(--container-width);
    min-height: var(--container-height);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    position: relative;
    gap: 4rem;
}}

/* Background Simulation (Replacing Local Images) */
.hero-main::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    /* Simulate a repeating pattern and a central glow (portrait substitute) */
    background-image: 
        radial-gradient(circle at 50% 100%, rgba(193, 53, 132, 0.15) 0%, transparent 60%),
        repeating-linear-gradient(45deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 2px, transparent 2px, transparent 12px);
    background-size: 100% 100%, 24px 24px;
    z-index: 0;
    pointer-events: none;
}}

/* Main Intro (Left Column) */
.main-intro {{
    flex: 1.2;
    position: relative;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    max-width: 90%;
    margin-bottom: 2.5rem;
    color: var(--quote-color);
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #FFFFFF;
    text-decoration: none;
    padding: 14px 32px;
    font-weight: 600;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}}

/* Main Quotes (Right Column) */
.main-quotes {{
    flex: 0.8;
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.quote {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--quote-color);
    font-style: italic;
}}

.quote-author {{
    display: block;
    margin-top: 0.75rem;
    font-weight: 600;
    font-style: normal;
    color: var(--text-color);
}}

/* The Core Technique: Offsetting the nth-child */
.quote:nth-child(2) {{
    margin-left: 4rem; /* Pushes the second item outward */
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: center;
        gap: 4rem;
        padding-top: 6rem;
        padding-bottom: 6rem;
    }}
    .main-intro, .main-quotes {{
        flex: 1;
        width: 100%;
    }}
    .quote:nth-child(2) {{
        margin-left: 2rem;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-main">
        <!-- Left Side: Intro -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>

        <!-- Right Side: Quotes -->
        <div class="main-quotes">
            <p class="quote">
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p class="quote">
                "An investment in knowledge always pays the best interest."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Split-Layout Typography Hero
document.addEventListener('DOMContentLoaded', () => {
    // Component is primarily CSS-driven. 
    // JS can be utilized here to add entrance animations if desired.
    const intro = document.querySelector('.main-intro');
    const quotes = document.querySelectorAll('.quote');
    
    // Optional basic fade-in effect implementation
    intro.style.opacity = '0';
    intro.style.transform = 'translateY(20px)';
    intro.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    
    setTimeout(() => {
        intro.style.opacity = '1';
        intro.style.transform = 'translateY(0)';
    }, 100);

    quotes.forEach((quote, index) => {
        quote.style.opacity = '0';
        quote.style.transform = 'translateX(20px)';
        quote.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            quote.style.opacity = '1';
            quote.style.transform = 'translateX(0)';
        }, 300 + (index * 200));
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
