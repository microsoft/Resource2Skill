def create_component(
    output_dir: str,
    title_text: str = "Launch Countdown",
    body_text: str = "Systems online. Awaiting final deployment sequence.",
    color_scheme: str = "dark",
    accent_color: str = "#333333",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Mechanical Flip Clock effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* 3D Mechanical Flip Clock */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
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
    padding: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 300;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
    text-align: center;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.7;
    margin-bottom: 3rem;
    text-align: center;
}}

/* Clock Layout */
.clock-container {{
    display: flex;
    gap: 1.5rem;
}}

.flip-unit {{
    --unit-w: 130px;
    --unit-h: 180px;
    --half-h: calc(var(--unit-h) / 2);
    
    position: relative;
    width: var(--unit-w);
    height: var(--unit-h);
    font-size: calc(var(--unit-h) * 0.75);
    line-height: var(--unit-h);
    font-weight: 700;
    text-align: center;
    perspective: 800px;
    border-radius: 12px;
    background-color: #111; /* Hidden background */
    box-shadow: 0 20px 40px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(255,255,255,0.1);
}}

/* The Mechanical Split Gap */
.flip-unit::after {{
    content: "";
    position: absolute;
    top: calc(var(--half-h) - 1px);
    left: 0;
    width: 100%;
    height: 2px;
    background: #000;
    z-index: 10;
}}

.card {{
    position: absolute;
    left: 0;
    width: 100%;
    height: var(--half-h);
    background: var(--accent);
    color: #ffffff;
    overflow: hidden;
    border-radius: 12px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}}

.card.top, .card.flap-top {{
    top: 0;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    transform-origin: bottom;
}}

.card.bottom, .card.flap-bottom {{
    bottom: 0;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    transform-origin: top;
}}

.card span {{
    position: absolute;
    left: 0;
    width: 100%;
    height: var(--unit-h);
    line-height: var(--unit-h);
    text-align: center;
    z-index: 2;
}}

.card.top span, .card.flap-top span {{
    top: 0;
}}

.card.bottom span, .card.flap-bottom span {{
    top: calc(var(--half-h) * -1);
}}

/* Shading / Lighting Overlays */
.card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: #000;
    opacity: 0;
    z-index: 3;
}}

/* 3D Flap States */
.flap-top {{
    z-index: 5;
    transform: rotateX(0deg);
    backface-visibility: hidden;
}}

.flap-bottom {{
    z-index: 5;
    transform: rotateX(90deg);
    backface-visibility: hidden;
}}

.top {{ z-index: 1; }}
.bottom {{ z-index: 1; }}

/* Animations */
.flap-top.animating {{
    animation: flipTop 0.25s ease-in forwards;
}}
.flap-top.animating::before {{
    animation: darkenTop 0.25s ease-in forwards;
}}

.flap-bottom.animating {{
    animation: flipBottom 0.25s ease-out 0.25s forwards;
}}
.flap-bottom::before {{
    opacity: 0.6; /* Starts shadowed while pointing out */
}}
.flap-bottom.animating::before {{
    animation: lightenBottom 0.25s ease-out 0.25s forwards;
}}

@keyframes flipTop {{
    0% {{ transform: rotateX(0deg); }}
    100% {{ transform: rotateX(-90deg); }}
}}

@keyframes flipBottom {{
    0% {{ transform: rotateX(90deg); }}
    100% {{ transform: rotateX(0deg); }}
}}

@keyframes darkenTop {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 0.6; }}
}}

@keyframes lightenBottom {{
    0% {{ opacity: 0.6; }}
    100% {{ opacity: 0; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <div class="clock-container">
            <!-- Tens Digit -->
            <div class="flip-unit" id="tens">
                <div class="card top"><span>1</span></div>
                <div class="card bottom"><span>1</span></div>
                <div class="card flap-top"><span>1</span></div>
                <div class="card flap-bottom"><span>1</span></div>
            </div>
            <!-- Ones Digit -->
            <div class="flip-unit" id="ones">
                <div class="card top"><span>2</span></div>
                <div class="card bottom"><span>2</span></div>
                <div class="card flap-top"><span>2</span></div>
                <div class="card flap-bottom"><span>2</span></div>
            </div>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Mechanical Flip Clock Controller

document.addEventListener('DOMContentLoaded', () => {{
    let currentCount = 12; // Starting number matching the initial DOM state

    // Coordinates the precise timing of DOM state swaps and CSS animations
    function updateDigit(unitId, currentVal, nextVal) {{
        const unit = document.getElementById(unitId);
        if (!unit) return;

        const topNextSpan = unit.querySelector('.top span');
        const bottomCurrSpan = unit.querySelector('.bottom span');
        const flapTopSpan = unit.querySelector('.flap-top span');
        const flapBottomSpan = unit.querySelector('.flap-bottom span');

        const flapTop = unit.querySelector('.flap-top');
        const flapBottom = unit.querySelector('.flap-bottom');

        // Prevent redundant animations
        if (bottomCurrSpan.innerText == currentVal && currentVal == nextVal) return;

        // 1. Setup DOM for the upcoming animation
        topNextSpan.innerText = nextVal;
        flapBottomSpan.innerText = nextVal;
        flapTopSpan.innerText = currentVal;
        bottomCurrSpan.innerText = currentVal;

        // Reset animation classes
        flapTop.classList.remove('animating');
        flapBottom.classList.remove('animating');

        // Trigger reflow to restart CSS animation
        void flapTop.offsetWidth;

        // 2. Start animation (takes exactly 500ms total)
        flapTop.classList.add('animating');
        flapBottom.classList.add('animating');

        // 3. Clean up and set resting DOM state completely invisibly
        setTimeout(() => {{
            flapTop.classList.remove('animating');
            flapBottom.classList.remove('animating');
            
            // Revert flaps to resting angles, but update the underlying static text
            bottomCurrSpan.innerText = nextVal;
            flapTopSpan.innerText = nextVal;
        }}, 500); // Matches CSS transition duration
    }}

    function tick() {{
        let nextCount = currentCount - 1;
        if (nextCount < 0) nextCount = 99; // Loop back for demonstration

        // Split into digits
        let currTens = Math.floor(currentCount / 10);
        let currOnes = currentCount % 10;
        let nextTens = Math.floor(nextCount / 10);
        let nextOnes = nextCount % 10;

        // Trigger individual flap updates only if the digit changed
        if (currTens !== nextTens) updateDigit('tens', currTens, nextTens);
        if (currOnes !== nextOnes) updateDigit('ones', currOnes, nextOnes);

        currentCount = nextCount;
    }}

    // Start clock cycle
    setInterval(tick, 1000);
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
