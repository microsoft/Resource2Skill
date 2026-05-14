def create_component(
    output_dir: str,
    title_text: str = "Pure CSS Mascot",
    body_text: str = "Look ma, no images! Drawn entirely with the CSS box model.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for the shirt
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Volumetric Character visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a192f"
        text_color = "#e6f1ff"
        stroke_color = "#000000"
        cloud_color = "rgba(255, 255, 255, 0.05)"
        shadow_dark = "rgba(0, 0, 0, 0.6)"
        shadow_light = "rgba(255, 255, 255, 0.15)"
        char_base = "#e0e0e0"
    else:
        bg_color = "#5ca2c6"
        text_color = "#ffffff"
        stroke_color = "#111111"
        cloud_color = "rgba(255, 255, 255, 0.3)"
        shadow_dark = "rgba(0, 0, 0, 0.2)"
        shadow_light = "rgba(255, 255, 255, 0.16)"
        char_base = "#ffffff"

    # === CSS ===
    css = f"""/* Pure CSS Volumetric Character — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --stroke: {stroke_color};
    --cloud: {cloud_color};
    --shadow-dark: {shadow_dark};
    --shadow-light: {shadow_light};
    --char-base: {char_base};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 20px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.1);
    background: linear-gradient(135deg, var(--bg), #00000033);
}}

/* Typography */
.content {{
    position: absolute;
    top: 40px;
    text-align: center;
    z-index: 20;
    width: 80%;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}}

p {{
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 400;
}}

/* Background Clouds using Multiple Box-Shadows */
.clouds {{
    position: absolute;
    width: 100px;
    height: 30px;
    background: transparent;
    border-radius: 50px;
    top: 20%;
    left: 10%;
    /* Drawing multiple clouds with a single div's box-shadow */
    box-shadow: 
        100px 50px 0 20px var(--cloud),
        250px -20px 0 10px var(--cloud),
        600px 100px 0 30px var(--cloud),
        -100px 200px 0 15px var(--cloud),
        800px 10px 0 25px var(--cloud);
    animation: drift 20s linear infinite alternate;
    z-index: 1;
}}

/* Character Container */
.character-container {{
    position: relative;
    width: 350px;
    height: 450px;
    z-index: 10;
    animation: float 3s ease-in-out infinite alternate;
    transform-origin: bottom center;
}}

/* Anatomy - Neck */
.neck {{
    position: absolute;
    width: 40px;
    height: 60px;
    background: var(--char-base);
    border: 10px solid var(--stroke);
    left: 50%;
    transform: translateX(-50%);
    top: 290px;
    z-index: 2;
}}

/* Anatomy - Body/Shirt */
.body-shape {{
    position: absolute;
    width: 180px;
    height: 90px;
    background: var(--accent);
    border: 10px solid var(--stroke);
    border-radius: 90px 90px 0 0; /* Pill shoulder shape */
    left: 50%;
    transform: translateX(-50%);
    top: 330px;
    z-index: 3;
    overflow: hidden;
}}

.body-shape::before {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 90px 90px 0 0;
    box-shadow: inset -15px 5px 0 2px var(--shadow-dark);
}}

/* Anatomy - Head */
.head {{
    position: absolute;
    width: 300px;
    height: 300px;
    background: var(--char-base);
    border-radius: 50%;
    border: 10px solid var(--stroke);
    left: 50%;
    transform: translateX(-50%);
    top: 20px;
    z-index: 4;
}}

/* Volumetric Head Shadow */
.head::before {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    /* Key shading trick from tutorial */
    box-shadow: inset -25px -10px 0 5px var(--shadow-dark);
    pointer-events: none;
    z-index: 10;
}}

/* Anatomy - Eyes */
.eye {{
    position: absolute;
    width: 100px;
    height: 100px;
    background: var(--stroke);
    border-radius: 50%;
    top: 70px;
}}

.eye.left {{ left: 35px; }}
.eye.right {{ right: 35px; }}

/* Eye Stroke Highlight */
.eye::before {{
    content: '';
    position: absolute;
    width: 24px;
    height: 24px;
    border: 5px solid var(--char-base);
    border-radius: 50%;
    top: 15px;
    left: 15px;
}}

/* Eye Volumetric Highlight */
.eye::after {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    box-shadow: inset -15px 5px 0 3px var(--shadow-light);
}}

/* Anatomy - Masked Mouth */
.mouth {{
    position: absolute;
    width: 140px;
    height: 140px;
    border: 10px solid var(--stroke);
    border-radius: 50%;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    /* Instead of messy overlay divs, use modern clip-path to trim the top half */
    clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%);
}}

/* Animations */
@keyframes float {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    100% {{ transform: translateY(-20px) rotate(1deg); }}
}}

@keyframes drift {{
    0% {{ transform: translateX(0px); }}
    100% {{ transform: translateX(-40px); }}
}}

/* Responsive Scaling */
@media (max-width: 600px) {{
    .character-container {{
        transform: scale(0.7);
        animation-name: float-mobile;
    }}
}}

@keyframes float-mobile {{
    0% {{ transform: scale(0.7) translateY(0px); }}
    100% {{ transform: scale(0.7) translateY(-20px); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="wrapper">
        <div class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="clouds" aria-hidden="true"></div>

        <!-- Semantic ARIA setup for CSS Art -->
        <div class="character-container" role="img" aria-label="An illustrated cartoon character created entirely with CSS">
            <div class="neck"></div>
            <div class="body-shape"></div>
            
            <div class="head">
                <div class="eye left"></div>
                <div class="eye right"></div>
                <div class="mouth"></div>
            </div>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS Character - Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const character = document.querySelector('.character-container');
    const wrapper = document.querySelector('.wrapper');

    // Add a subtle mouse-tracking parallax effect to compliment the CSS float
    wrapper.addEventListener('mousemove', (e) => {{
        // Check for reduced motion preference before applying JS animation
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        const x = (window.innerWidth / 2 - e.pageX) / 40;
        const y = (window.innerHeight / 2 - e.pageY) / 40;

        character.style.transform = `translate(${{-x}}px, ${{y}}px)`;
    }});

    wrapper.addEventListener('mouseleave', () => {{
        character.style.transform = `translate(0px, 0px)`;
        // The CSS @keyframes will smoothly take over again
    }});
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
