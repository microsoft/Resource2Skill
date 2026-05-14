def create_component(
    output_dir: str,
    title_text: str = "WELCOME\nTO MY FIRST\nWEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Format the title text to include HTML line breaks if newline characters are provided
    formatted_title = title_text.replace('\n', '<br>')

    # Theme variables
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.75)"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        btn_hover = "#a02a6d"
    else:
        bg_color = "#F4F7F6"
        text_color = "#1A253A"
        text_muted = "rgba(26, 37, 58, 0.75)"
        pattern_color = "rgba(0, 0, 0, 0.04)"
        btn_hover = "#a02a6d"

    # Secondary text from kwargs or defaults
    quote_1 = kwargs.get("quote_1", "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"\n\n- Dr. Seuss")
    quote_2 = kwargs.get("quote_2", "\"For the best return on your money, pour your purse into your head.\"\n\n- Benjamin Franklin")
    
    formatted_q1 = quote_1.replace('\n', '<br>')
    formatted_q2 = quote_2.replace('\n', '<br>')

    # === CSS ===
    css = f"""/* Asymmetric Split-Layout Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --accent-hover: {btn_hover};
    --pattern: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6rem;
    padding: 2rem;
    
    /* Procedural Pattern & Glow Background (replaces static images) */
    background-image: 
        radial-gradient(circle at center 80%, rgba(193, 53, 132, 0.15) 0%, transparent 50%),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern)), 
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern));
    background-size: 100% 100%, 30px 30px, 30px 30px;
    background-position: center bottom, 0 0, 15px 15px;
    background-repeat: no-repeat, repeat, repeat;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px rgba(0,0,0,0.2);
}}

/* Left Column: Main Intro */
.main-intro {{
    display: flex;
    flex-direction: column;
    max-width: 450px;
    z-index: 2;
    animation: fadeUp 0.8s ease-out forwards;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.05;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}}

.btn-primary {{
    display: inline-block;
    align-self: flex-start;
    background-color: var(--accent);
    color: #FFFFFF;
    text-decoration: none;
    padding: 14px 28px;
    font-weight: 800;
    text-transform: uppercase;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.btn-primary:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}}

/* Right Column: Secondary Quotes */
.main-quotes {{
    max-width: 380px;
    border-left: 4px solid var(--accent);
    padding-left: 2rem;
    z-index: 2;
    animation: fadeUp 0.8s ease-out 0.2s forwards;
    opacity: 0;
}}

.main-quotes p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    position: relative;
}}

/* Staggering the quotes via nth-child as done in the tutorial */
.main-quotes p:nth-child(2) {{
    margin-top: 3rem;
    padding-left: 2rem;
}}

/* Animations */
@keyframes fadeUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        gap: 4rem;
        height: auto;
        padding: 4rem 2rem;
    }}
    
    .main-intro {{
        max-width: 100%;
    }}
    
    .main-quotes {{
        margin-left: 0;
        max-width: 100%;
        padding-left: 1.5rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-container">
        
        <div class="main-intro">
            <h1>{formatted_title}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn-primary">My Work</a>
        </div>

        <div class="main-quotes">
            <p>{formatted_q1}</p>
            <p>{formatted_q2}</p>
        </div>

    </section>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Subtle parallax effect on mousemove to enhance the layered background feel
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-container');
    
    hero.addEventListener('mousemove', (e) => {
        const { width, height } = hero.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the container
        const x = (e.clientX / width) - 0.5;
        const y = (e.clientY / height) - 0.5;
        
        // Shift the radial gradient (glow) slightly in the opposite direction of the mouse
        const moveX = 50 - (x * 10);
        const moveY = 80 - (y * 10);
        
        hero.style.backgroundImage = `
            radial-gradient(circle at ${moveX}% ${moveY}%, rgba(193, 53, 132, 0.15) 0%, transparent 50%),
            linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern)), 
            linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern))
        `;
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
