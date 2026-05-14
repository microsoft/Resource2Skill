def create_component(
    output_dir: str,
    title_text: str = "Processing Data",
    body_text: str = "Please wait while we secure your connection...",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua/cyan looks best)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Keyframe Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Deep tutorial-style blue/black
        text_color = "#ffffff"
        btn_bg = "rgba(255, 255, 255, 0.1)"
        btn_hover = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        btn_bg = "rgba(0, 0, 0, 0.05)"
        btn_hover = "rgba(0, 0, 0, 0.1)"

    # Escape safe strings
    title_safe = title_text.replace("<", "&lt;").replace(">", "&gt;")
    body_safe = body_text.replace("<", "&lt;").replace(">", "&gt;")

    # === CSS ===
    css = f"""/* 3D Neon Keyframe Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    position: relative;
    padding: 2rem;
    text-align: center;
}}

/* -- Typographics -- */
.text-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

h1 {{
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: 1px;
}}

p {{
    font-size: 1rem;
    opacity: 0.7;
    font-weight: 400;
}}

/* -- Core Skill: The Loader -- */
.loading-box {{
    height: 60px;
    width: 60px;
    border: 6px solid var(--accent-color);
    border-radius: 6px;
    /* Outer glow and Inner (inset) glow */
    box-shadow: 0 0 12px var(--accent-color), inset 0 0 12px var(--accent-color);
    z-index: 10;
    
    /* Animation Assignment */
    /* animation: name duration timing-function iteration-count */
    animation: flip-3d 2.4s ease-in-out infinite;
}}

/* Pause animation on hover as a pure CSS fallback/extra feature */
.loading-box:hover {{
    animation-play-state: paused;
    cursor: grab;
}}

/* The Multi-axis 3D sequence */
@keyframes flip-3d {{
    0% {{
        transform: rotateX(0) rotateY(0) rotateZ(0);
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0) rotateZ(0);
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0);
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* -- Interactive Controls -- */
.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

button {{
    background: var(--btn-bg);
    color: var(--text-color);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 0.6rem 1.5rem;
    border-radius: 50px;
    font-family: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}}

button:hover {{
    background: var(--btn-hover);
    transform: translateY(-2px);
}}

button:active {{
    transform: translateY(0);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_safe}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <!-- The Animated Element -->
        <div class="loading-box" id="loader"></div>
        
        <div class="text-wrapper">
            <h1>{title_safe}</h1>
            <p>{body_safe}</p>
        </div>

        <!-- Animation Controls (JS bound) -->
        <div class="controls">
            <button id="btn-play">Play</button>
            <button id="btn-pause">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Keyframe Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('btn-play');
    const pauseBtn = document.getElementById('btn-pause');

    // Control the animation-play-state property via JavaScript
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
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
