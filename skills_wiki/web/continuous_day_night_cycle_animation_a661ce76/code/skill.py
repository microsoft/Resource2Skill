def create_component(
    output_dir: str,
    title_text: str = "Atmospheric Day/Night Cycle",
    body_text: str = "A fully synchronized 24-second CSS animation timeline.",
    color_scheme: str = "dark",
    accent_color: str = "#FFD700",
    width_px: int = 900,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Day/Night Cycle animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Continuous Day/Night Cycle Animation */
:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --bg: #0f172a;
    --text: #f8fafc;
    --accent: {accent_color};
    --sky-day: #71B4E3;
    --sky-night: #0F172A;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 0.5rem;
}}

.header p {{
    color: #94a3b8;
}}

/* -- Main Window Frame -- */
.window-frame {{
    padding: 12px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

.container {{
    width: var(--width);
    max-width: 90vw;
    height: var(--height);
    max-height: 70vh;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
}}

/* -- The Animated Scene -- */
.scene {{
    width: 100%;
    height: 100%;
    position: relative;
    background-color: var(--sky-day);
    animation: skyCycle 24s infinite;
}}

/* -- Celestial Bodies -- */
.sun-wrapper, .moon-wrapper {{
    position: absolute;
    top: 12%;
    width: 80px;
    height: 80px;
    z-index: 5;
    animation: celestialMove 24s linear infinite;
}}

.moon-wrapper {{
    /* Offsets the moon by exactly half the day loop so it appears at night */
    animation-delay: -12s; 
}}

.sun {{
    width: 100%;
    height: 100%;
    background: #FFD700;
    border-radius: 50%;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.6), 0 0 80px rgba(255, 215, 0, 0.4);
}}

.moon {{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: transparent;
    /* Inset shadow creates the crescent shape perfectly */
    box-shadow: inset 16px -8px 0 0px rgba(255, 255, 255, 0.95);
    transform: rotate(-20deg);
}}

/* -- Clouds -- */
.clouds {{
    position: absolute;
    inset: 0;
    bottom: 25%;
    z-index: 6;
    pointer-events: none;
    animation: cloudsFade 24s infinite;
}}

.cloud-track {{
    position: absolute;
}}

/* Multiple tracks with different float speeds and starting offsets */
.ct-1 {{ top: 10%; animation: cloudFloat 18s linear infinite; }}
.ct-2 {{ top: 30%; animation: cloudFloat 26s linear infinite -8s; }}
.ct-3 {{ top: 15%; animation: cloudFloat 22s linear infinite -14s; }}
.ct-4 {{ top: 25%; animation: cloudFloat 32s linear infinite -3s; }}

.cloud {{
    width: 120px;
    height: 35px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50px;
    position: relative;
}}

.cloud::before, .cloud::after {{
    content: '';
    position: absolute;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50%;
}}

.cloud::before {{
    width: 60px; height: 60px;
    top: -25px; left: 15px;
}}

.cloud::after {{
    width: 50px; height: 50px;
    top: -15px; right: 20px;
}}

/* -- Stars -- */
.stars {{
    position: absolute;
    inset: 0;
    bottom: 25%;
    z-index: 2;
    pointer-events: none;
    animation: starsFade 24s infinite;
}}

.star {{
    position: absolute;
    background: #ffffff;
    border-radius: 50%;
    animation: starPulse linear infinite alternate;
}}

/* -- Ground -- */
.ground {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 25%;
    background: linear-gradient(180deg, #22C55E 0%, #16A34A 100%);
    z-index: 10;
    box-shadow: inset 0 10px 20px rgba(0,0,0,0.1);
}}

/* Ground overlay that darkens during the night phase */
.ground::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(2, 6, 23, 0.7);
    animation: starsFade 24s infinite; /* Reusing the night-fade keyframe */
}}

/* === The 24-Second Timeline Keyframes === */

/* 1. Environment Colors */
@keyframes skyCycle {{
    0%, 30%   {{ background-color: var(--sky-day); }}
    45%, 80%  {{ background-color: var(--sky-night); }}
    95%, 100% {{ background-color: var(--sky-day); }}
}}

/* 2. Shared Sun/Moon Path */
@keyframes celestialMove {{
    0%          {{ left: -150px; opacity: 1; }}
    45%         {{ left: 100%; opacity: 1; }} /* 100% left pushes it fully past the right edge */
    45.1%, 100% {{ left: 100%; opacity: 0; }} /* Wait offscreen for loop */
}}

/* 3. Nighttime Visibilities (Stars and Ground Shadow) */
@keyframes starsFade {{
    0%, 35%   {{ opacity: 0; }}
    45%, 85%  {{ opacity: 1; }}
    95%, 100% {{ opacity: 0; }}
}}

/* 4. Daytime Visibilities (Clouds) */
@keyframes cloudsFade {{
    0%, 30%   {{ opacity: 0.9; }}
    45%, 80%  {{ opacity: 0; }}
    95%, 100% {{ opacity: 0.9; }}
}}

/* 5. Endless Cloud Scrolling */
@keyframes cloudFloat {{
    0%   {{ left: -200px; }}
    100% {{ left: 100%; }}
}}

/* 6. Individual Star Twinkle */
@keyframes starPulse {{
    0%   {{ transform: scale(0.6); opacity: 0.3; }}
    100% {{ transform: scale(1.3); opacity: 1; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    
    <div class="window-frame">
        <div class="container">
            <div class="scene">
                <!-- Javascript will inject star divs here -->
                <div class="stars"></div>
                
                <div class="sun-wrapper">
                    <div class="sun"></div>
                </div>
                
                <div class="moon-wrapper">
                    <div class="moon"></div>
                </div>
                
                <div class="clouds">
                    <div class="cloud-track ct-1"><div class="cloud"></div></div>
                    <div class="cloud-track ct-2"><div class="cloud" style="transform: scale(0.7);"></div></div>
                    <div class="cloud-track ct-3"><div class="cloud" style="transform: scale(1.15);"></div></div>
                    <div class="cloud-track ct-4"><div class="cloud" style="transform: scale(0.5);"></div></div>
                </div>
                
                <div class="ground"></div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Generate the Starfield dynamically to keep HTML clean
document.addEventListener('DOMContentLoaded', () => {
    const starsContainer = document.querySelector('.stars');
    const starCount = 100; // Number of stars

    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        
        // Random placement (X axis, and upper 75% of Y axis to avoid ground)
        const xPos = Math.random() * 100;
        const yPos = Math.random() * 100; 
        
        // Randomize size, twinkle speed, and initial twinkle offset
        const size = Math.random() * 2 + 1;
        const duration = Math.random() * 3 + 2; 
        const delay = Math.random() * 5;

        star.style.left = `${xPos}%`;
        star.style.top = `${yPos}%`;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.animationDuration = `${duration}s`;
        star.style.animationDelay = `-${delay}s`; // start at random phase

        starsContainer.appendChild(star);
    }
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
