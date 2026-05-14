def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Hero layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base colors derived from tutorial
    if color_scheme == "dark":
        bg_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.15)"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.85)"
    else:
        bg_color = "#E2E6ED"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        text_color = "#1A253A"
        text_muted = "rgba(26, 37, 58, 0.85)"

    # Quotes for the right-hand side
    quote_1 = '"The more that you read, the more things you will know. The more that you learn, the more places you\'ll go."<br><br>- Dr. Seuss'
    quote_2 = '"For the best return on your money, pour your purse into your head."<br><br>- Benjamin Franklin'

    css = f"""/* Split-Content Hero — Generated Component */
:root {{
    --bg-color: {bg_color};
    --pattern-color: {pattern_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #0d0d0d;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Main Component Wrapper */
.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    /* CSS Geometric Pattern mimicking the video */
    background-image: 
        repeating-linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color)),
        repeating-linear-gradient(45deg, var(--pattern-color) 25%, var(--bg-color) 25%, var(--bg-color) 75%, var(--pattern-color) 75%, var(--pattern-color));
    background-position: 0 0, 20px 20px;
    background-size: 40px 40px;
    
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
    box-shadow: 0 25px 50px rgba(0,0,0,0.5);
}}

/* The Central Portrait / Centerpiece */
.hero-centerpiece {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 45%;
    height: 85%;
    /* Abstract placeholder replacing the specific portrait PNG to ensure reproducibility */
    background: radial-gradient(ellipse at top, var(--text-muted) 0%, transparent 60%),
                linear-gradient(to top, #000 0%, transparent 80%);
    border-radius: 200px 200px 0 0;
    z-index: 1;
    pointer-events: none;
    transition: transform 0.1s ease-out;
}}

/* Foreground Content Layers */
.main-intro, .main-quotes {{
    z-index: 2;
    position: relative;
    color: var(--text-main);
    display: flex;
    flex-direction: column;
}}

/* Left Pane: Intro */
.main-intro {{
    max-width: 40%;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
    max-width: 85%;
}}

.cta-button {{
    display: inline-block;
    width: fit-content;
    background-color: var(--accent);
    color: #FFF;
    text-decoration: none;
    padding: 12px 28px;
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Pane: Quotes */
.main-quotes {{
    max-width: 35%;
}}

.quote {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 2.5rem;
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

/* Staggering the second quote as shown in the tutorial */
.quote:nth-child(2) {{
    margin-left: 40px;
}}

/* Responsive Adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: flex-start;
        padding: 40px 5%;
        overflow-y: auto;
    }}
    .hero-centerpiece {{
        opacity: 0.15; /* Push to background on mobile */
        width: 100%;
        height: 50%;
    }}
    .main-intro, .main-quotes {{
        max-width: 100%;
        text-align: center;
        align-items: center;
    }}
    .quote {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 15px;
    }}
    .quote:nth-child(2) {{
        margin-left: 0;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container" id="hero">
        <!-- Abstract centerpiece simulating the layered portrait -->
        <div class="hero-centerpiece" id="centerpiece"></div>
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">My Work</a>
        </div>
        
        <div class="main-quotes">
            <p class="quote">{quote_1}</p>
            <p class="quote">{quote_2}</p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Subtle Parallax Effect to enhance depth of the layered layout
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.getElementById('hero');
    const centerpiece = document.getElementById('centerpiece');

    if (!hero || !centerpiece) return;

    hero.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to container center
        const rect = hero.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        
        // Calculate offset (constrain movement range to subtle shifts)
        const mouseX = e.clientX - centerX;
        const shiftX = (mouseX * -0.05); // Negative value moves object opposite to mouse
        
        // Apply transform. The base CSS has translateX(-50%) to keep it centered.
        centerpiece.style.transform = `translateX(calc(-50% + ${shiftX}px))`;
    });

    hero.addEventListener('mouseleave', () => {
        // Reset to default on mouse leave
        centerpiece.style.transform = `translateX(-50%)`;
    });
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
