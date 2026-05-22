def create_component(
    output_dir: str,
    title_text: str = "Meet Pippo",
    body_text: str = "A pure CSS character. Click him to say hello!",
    color_scheme: str = "dark",
    accent_color: str = "#579AE8",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Character Illustration.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
    else:
        bg_color = "#eef2f5"
        text_color = "#1a1a2e"

    css = f"""/* Pure CSS Character Illustration — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    
    /* Character Palette */
    --bird-yellow: #FCE454;
    --bird-dark: #1A1A1A;
    --bird-orange: #FF8A00;
    --bird-orange-dark: #D35400;
    --bird-blush: #FF2458;
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
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
}}

.text-content {{
    text-align: center;
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

/* === PURE CSS BIRD === */
.bird-wrapper {{
    position: relative;
    width: 200px;
    height: 230px;
    animation: bob 2.5s infinite ease-in-out;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}}

/* Animation classes */
.bird-wrapper.jumping {{
    animation: jump 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

/* Cap */
.bird-cap {{
    position: absolute;
    top: 0; left: 0;
    width: 200px; height: 110px;
    background: var(--accent);
    border-radius: 100px 100px 0 0;
    z-index: 3;
}}

.bird-cap-peak {{
    position: absolute;
    top: 110px; left: 50px;
    width: 0; height: 0;
    border-left: 50px solid transparent;
    border-right: 50px solid transparent;
    border-top: 40px solid var(--accent);
    z-index: 3;
}}

/* Cap Spots */
.spot {{
    position: absolute;
    background: var(--bird-dark);
    border-radius: 50%;
    z-index: 4;
}}
.spot-1 {{ width: 28px; height: 28px; top: 25px; left: 45px; }}
.spot-2 {{ width: 32px; height: 32px; top: 20px; left: 125px; }}
.spot-3 {{ width: 24px; height: 24px; top: 70px; left: 88px; }}

/* Face */
.bird-face {{
    position: absolute;
    top: 50px; left: 10px;
    width: 180px; height: 150px;
    background: var(--bird-yellow);
    border-radius: 50%;
    z-index: 2;
}}

/* Eyes */
.eye {{
    position: absolute;
    top: 130px;
    width: 28px; height: 28px;
    background: var(--bird-dark);
    border-radius: 50%;
    z-index: 4;
}}
.eye-left {{ left: 40px; }}
.eye-right {{ left: 132px; }}

.iris {{
    position: absolute;
    top: 4px; left: 4px;
    width: 10px; height: 10px;
    background: white;
    border-radius: 50%;
}}

/* Blush */
.blush {{
    position: absolute;
    top: 160px;
    width: 24px; height: 24px;
    background: var(--bird-blush);
    border-radius: 50%;
    filter: blur(6px);
    z-index: 3;
    opacity: 0.65;
}}
.blush-left {{ left: 24px; }}
.blush-right {{ left: 152px; }}

/* Beak */
.beak {{
    position: absolute;
    top: 160px; left: 75px;
    width: 50px; height: 30px;
    z-index: 5;
}}
.beak-top {{
    position: absolute;
    top: 0; left: 0;
    width: 50px; height: 20px;
    background: var(--bird-orange);
    border-radius: 50%;
    border: 2px solid var(--bird-orange-dark);
}}
.beak-bottom {{
    position: absolute;
    top: 10px; left: 10px;
    width: 30px; height: 16px;
    background: var(--bird-orange-dark);
    border-radius: 50%;
    border: 2px solid var(--bird-orange-dark);
    z-index: -1;
}}

/* Wings */
.wing {{
    position: absolute;
    top: 130px;
    width: 60px; height: 60px;
    background: var(--bird-yellow);
    z-index: 1; /* Behind face, above feet */
}}
.wing-left {{
    left: -10px;
    border-radius: 220px 0 220px 0;
    transform-origin: top right;
    animation: flap-left 1.2s infinite ease-in-out;
}}
.wing-right {{
    left: 150px;
    border-radius: 0 220px 0 220px;
    transform-origin: top left;
    animation: flap-right 1.2s infinite ease-in-out;
}}

/* Feet */
.foot {{
    position: absolute;
    top: 195px;
    width: 30px; height: 38px;
    background: var(--bird-orange-dark);
    /* Creates a 3-toed webbed foot using coordinates */
    clip-path: polygon(66% 0, 100% 79%, 75% 79%, 52% 100%, 26% 79%, 3% 80%, 34% 0);
    z-index: 0;
}}
.foot-left {{ left: 54px; transform: rotate(10deg); }}
.foot-right {{ left: 116px; transform: rotate(-10deg); }}


/* === Keyframe Animations === */
@keyframes bob {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(12px); }}
}}

@keyframes flap-left {{
    0%, 100% {{ transform: rotate(0deg); }}
    50% {{ transform: rotate(-35deg); }}
}}

@keyframes flap-right {{
    0%, 100% {{ transform: rotate(0deg); }}
    50% {{ transform: rotate(35deg); }}
}}

@keyframes jump {{
    0% {{ transform: translateY(12px) scaleY(0.9); }}
    40% {{ transform: translateY(-50px) scaleY(1.05); }}
    80% {{ transform: translateY(5px) scaleY(0.95); }}
    100% {{ transform: translateY(0px) scaleY(1); }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- PURE CSS CHARACTER -->
        <div class="bird-wrapper" id="pippo">
            
            <div class="wing wing-left"></div>
            <div class="wing wing-right"></div>
            
            <div class="foot foot-left"></div>
            <div class="foot foot-right"></div>
            
            <div class="bird-face"></div>
            
            <div class="bird-cap"></div>
            <div class="bird-cap-peak"></div>
            
            <div class="spot spot-1"></div>
            <div class="spot spot-2"></div>
            <div class="spot spot-3"></div>
            
            <div class="eye eye-left">
                <div class="iris"></div>
            </div>
            <div class="eye eye-right">
                <div class="iris"></div>
            </div>
            
            <div class="blush blush-left"></div>
            <div class="blush blush-right"></div>
            
            <div class="beak">
                <div class="beak-bottom"></div>
                <div class="beak-top"></div>
            </div>
            
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Pure CSS Character Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const bird = document.getElementById('pippo');
    let isJumping = false;

    // Trigger jump animation on click
    bird.addEventListener('click', () => {{
        if (isJumping) return;
        isJumping = true;
        
        // Remove idle bobbing to apply jump
        bird.style.animation = 'none';
        bird.offsetHeight; // trigger browser reflow
        
        // Add jump class
        bird.classList.add('jumping');
        
        // Restore idle animation after jump completes
        setTimeout(() => {{
            bird.classList.remove('jumping');
            bird.style.animation = ''; // restores stylesheet animation
            isJumping = false;
        }}, 500); // matches the 0.5s duration in CSS
    }});
}});
"""

    # Write files
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
