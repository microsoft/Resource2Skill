def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1920,
    height_px: int = 1080,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Portrait Hero.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        silhouette_color = "#0f1626"
    else:
        bg_color = "#e9ecef"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "#ced4da"

    # SVG Data URIs for self-contained visual reproduction
    # 1. Subtle geometric pattern background
    pattern_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Cpath d='M20 0 L40 20 L20 40 L0 20 Z' fill='none' stroke='{pattern_color}' stroke-width='1'/%3E%3C/svg%3E"
    
    # 2. Placeholder portrait silhouette
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M200 120 C 160 120 130 150 130 190 C 130 230 160 260 200 260 C 240 260 270 230 270 190 C 270 150 240 120 200 120 Z M70 600 L70 500 C 70 400 120 330 200 330 C 280 330 330 400 330 500 L330 600 Z' fill='{silhouette_color}'/%3E%3C/svg%3E"

    css = f"""/* Split-Layout Portrait Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
}}

.hero-section {{
    position: relative;
    width: 100%;
    min-height: 100vh;
    /* Layer 1: Portrait (top), Layer 2: Pattern (bottom) */
    background-image: url("{portrait_svg}"), url("{pattern_svg}");
    background-position: bottom center, center;
    background-size: 75vh, 40px 40px;
    background-repeat: no-repeat, repeat;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15vw; /* Creates the central void for the portrait */
    padding: 0 5vw;
}}

/* Typography Defaults */
h1 {{
    font-size: clamp(3rem, 5vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Left Column */
.main-intro {{
    max-width: 450px;
    position: relative;
    /* Offset to fine-tune framing around portrait */
    bottom: 5vh;
    animation: fadeSlideUp 1s ease-out forwards;
}}

.main-intro p {{
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #fff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: transform 0.2s ease, opacity 0.2s ease;
}}

.btn:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

/* Right Column */
.main-quotes {{
    max-width: 380px;
    position: relative;
    /* Offset to create asymmetrical balance */
    top: 10vh;
    animation: fadeSlideUp 1s ease-out 0.2s forwards;
    opacity: 0;
}}

.main-quotes p {{
    font-size: 1rem;
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
    font-style: italic;
}}

/* Entrance Animation */
@keyframes fadeSlideUp {{
    0% {{
        opacity: 0;
        transform: translateY(30px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive Breakpoints */
@media (max-width: 1024px) {{
    .hero-section {{
        flex-direction: column;
        gap: 5vh;
        background-position: bottom right -10vw, center;
        background-size: 60vh, 40px 40px;
    }}
    
    .main-intro, .main-quotes {{
        top: 0;
        bottom: 0;
        max-width: 600px;
        background: rgba(0,0,0,0.4);
        padding: 2rem;
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Layout Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-section">
        <!-- Left Flank -->
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </section>

        <!-- Right Flank -->
        <section class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><br>— Dr. Seuss</p>
            <p>"For the best return on your money, pour your purse into your head."<br><br>— Benjamin Franklin</p>
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Optional: Add subtle parallax effect to the background on mousemove
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-section');
    
    hero.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Shift background slightly opposite to mouse movement
        // First bg is portrait (moves more), second is pattern (moves less)
        hero.style.backgroundPosition = `calc(50% - ${x}px) calc(100% - ${y}px), calc(50% - ${x/3}px) calc(50% - ${y/3}px)`;
    });

    // Reset on leave
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = 'bottom center, center';
        hero.style.transition = 'background-position 0.5s ease-out';
    });
    
    hero.addEventListener('mouseenter', () => {
        hero.style.transition = 'none';
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
