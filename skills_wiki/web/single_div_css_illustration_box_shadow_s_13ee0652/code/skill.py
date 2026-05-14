def create_component(
    output_dir: str,
    title_text: str = "CSS Art Mascot",
    body_text: str = "Drawn entirely with a single HTML element and CSS box-shadows.",
    color_scheme: str = "light",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Single-Div CSS Illustration visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive background based on scheme, but strictly preserve the character's colors
    # to ensure the optical blending illusion works perfectly.
    if color_scheme == "dark":
        bg_color = "#1a212b"
        text_color = "#ffffff"
    else:
        bg_color = "#95b7c0" # Original tutorial background
        text_color = "#1a1a2e"

    # Strict Character Palette
    face_color = "#fde7b6"
    ear_inner = "#c2704a"
    feature_color = "#5f1912"
    highlight = "#ffffff"

    # === CSS ===
    css = f"""/* Single-Div CSS Illustration — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    
    /* Character strict palette */
    --face: {face_color};
    --ear: {ear_inner};
    --feature: {feature_color};
    --highlight: {highlight};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

.text-content {{
    text-align: center;
    max-width: 600px;
    z-index: 10;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* === Core CSS Art Implementation === */
.teddy-wrapper {{
    position: relative;
    width: 250px;
    height: 250px;
    /* Optional scale adjustment for smaller heights */
    transform: scale(min(1, calc(var(--height) / 400)));
}}

.teddy {{
    background-color: var(--face);
    height: 250px;
    width: 250px;
    border-radius: 50%;
    position: absolute;
    top: 0;
    left: 0;
    /* Smooth hover effect to prove it's a live DOM element */
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}}

.teddy-wrapper:hover .teddy {{
    transform: scale(1.05) translateY(-10px);
}}

/* Muzzle vertical line drawn via gradient */
.teddy::before {{
    position: absolute;
    content: '';
    height: 120px;
    width: 150px;
    border-radius: 50%;
    top: 130px;
    left: 50px;
    background-image: linear-gradient(
        to right, 
        transparent 74px, 
        var(--feature) 74px, 
        var(--feature) 76px, 
        transparent 76px
    );
}}

/* 
  All facial features and ears are drawn by stamping box-shadows 
  from this single 30x30 invisible anchor element.
*/
.teddy::after {{
    position: absolute;
    content: '';
    height: 30px;
    width: 30px;
    border-radius: 50%;
    background-color: transparent;
    top: 180px;
    left: 110px;
    box-shadow:
        /* Eye reflections (White) */
        50px -105px 0 -8px var(--highlight),
        -50px -105px 0 -8px var(--highlight),
        38px -91px 0 -12px var(--highlight),
        -38px -91px 0 -12px var(--highlight),
        
        /* Main Eyes (Dark Brown) */
        -45px -100px 0 2px var(--feature),
        45px -100px 0 2px var(--feature),
        
        /* Nose */
        0 -40px 0 3px var(--feature),
        
        /* Open Mouth */
        0 17px 0 3px var(--feature),
        
        /* Inner Ears (Warm Brown) */
        -95px -180px 0 30px var(--ear),
        95px -180px 0 30px var(--ear),
        
        /* Outer Ears (Beige - blends flawlessly into the face) */
        -95px -180px 0 50px var(--face),
        95px -180px 0 50px var(--face);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- The entire character is contained in this single empty div -->
        <div class="teddy-wrapper">
            <div class="teddy"></div>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Single-Div CSS Illustration
// Visual rendering is purely CSS-driven.
// JavaScript can be used here to dynamically update CSS variables 
// if you wanted the character's eyes to follow the mouse, for example.

document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Art Component Loaded Successfully.");
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
