def create_component(
    output_dir: str,
    title_text: str = "Pure CSS Animated Honey Bee",
    body_text: str = "Created entirely with HTML and CSS shapes, no images or SVGs required.",
    color_scheme: str = "dark",
    accent_color: str = "#FFD700",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Animated Honey Bee effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#dc143c" # Crimson background matching the tutorial's distinct aesthetic
        text_color = "#ffffff"
        card_bg = "rgba(0, 0, 0, 0.2)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        card_bg = "rgba(255, 255, 255, 0.8)"

    # === CSS ===
    css = f"""/* Pure CSS Animated Honey Bee */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --card-bg: {card_bg};
    --bee-yellow: {accent_color};
    --bee-black: #111;
    --wing-color: rgba(173, 216, 230, 0.75);
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

.presentation-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 90vw;
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.header-text h1 {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}}

.header-text p {{
    font-size: 15px;
    opacity: 0.9;
    max-width: 400px;
    line-height: 1.5;
}}

.bee-wrapper {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}}

/* --- Core Bee Art & Animation --- */

.bee {{
    position: relative;
    width: 150px;
    height: 200px;
    /* Gentle vertical floating */
    animation: float 2.5s ease-in-out infinite;
}}

/* The main pill-shaped body */
.body {{
    position: absolute;
    width: 100%;
    height: 180px;
    background-color: var(--bee-yellow);
    border-radius: 75px;
    top: 10px;
    z-index: 2;
    overflow: hidden; /* crucial to clip the stripes to the body curve */
    box-shadow: inset -8px -8px 20px rgba(0, 0, 0, 0.15); /* Adds slight 3D volume */
}}

/* Black horizontal stripes */
.stripe {{
    position: absolute;
    width: 100%;
    height: 15px;
    background-color: var(--bee-black);
}}
.stripe:nth-child(1) {{ top: 100px; }}
.stripe:nth-child(2) {{ top: 130px; }}
.stripe:nth-child(3) {{ top: 160px; }}

/* Eyes */
.eye {{
    position: absolute;
    width: 14px;
    height: 14px;
    background-color: var(--bee-black);
    border-radius: 50%;
    top: 40px;
}}
.eye.left {{ left: 35px; }}
.eye.right {{ right: 35px; }}

/* Smiling Mouth */
.mouth {{
    position: absolute;
    width: 32px;
    height: 16px;
    background-color: #FFF;
    border-radius: 0 0 16px 16px; /* Semi-circle */
    top: 65px;
    left: 50%;
    transform: translateX(-50%);
}}

/* Antennae */
.antenna {{
    position: absolute;
    width: 4px;
    height: 30px;
    background-color: var(--bee-black);
    top: -15px;
    z-index: 1;
}}
.antenna.left {{
    left: 45px;
    transform: rotate(-25deg);
}}
.antenna.right {{
    right: 45px;
    transform: rotate(25deg);
}}
.antenna-tip {{
    position: absolute;
    width: 12px;
    height: 12px;
    background-color: var(--bee-black);
    border-radius: 50%;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
}}

/* Wings */
.wing {{
    position: absolute;
    width: 120px;
    height: 80px;
    background-color: var(--wing-color);
    top: 60px;
    z-index: 1; /* Placed behind the body */
}}

/* Asymmetrical petal shape using multi-value border-radius */
.wing.left {{
    left: -80px;
    border-radius: 100px 50px; 
    transform-origin: right center;
    animation: flap-left 0.12s ease-in-out infinite alternate;
}}
.wing.right {{
    right: -80px;
    border-radius: 50px 100px;
    transform-origin: left center;
    animation: flap-right 0.12s ease-in-out infinite alternate;
}}

/* --- Keyframes --- */

@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50%      {{ transform: translateY(-20px); }}
}}

@keyframes flap-left {{
    0%   {{ transform: rotate(-15deg); }}
    100% {{ transform: rotate(-55deg); }}
}}

@keyframes flap-right {{
    0%   {{ transform: rotate(15deg); }}
    100% {{ transform: rotate(55deg); }}
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
    <div class="presentation-container">
        
        <div class="bee-wrapper">
            <!-- Pure CSS Bee Component -->
            <div class="bee" aria-label="Animated Honey Bee">
                <div class="wing left"></div>
                <div class="wing right"></div>
                
                <div class="antenna left">
                    <div class="antenna-tip"></div>
                </div>
                <div class="antenna right">
                    <div class="antenna-tip"></div>
                </div>
                
                <div class="body">
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="mouth"></div>
                    <div class="stripe"></div>
                    <div class="stripe"></div>
                    <div class="stripe"></div>
                </div>
            </div>
        </div>

        <div class="header-text">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS Animated Art relies entirely on the browser's CSS rendering engine.
// No JavaScript is required for the floating or flapping animations!

document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Bee loaded. All animations are running natively via CSS @keyframes.");
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
