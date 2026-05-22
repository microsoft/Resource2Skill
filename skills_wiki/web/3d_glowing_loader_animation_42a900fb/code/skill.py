def create_component(
    output_dir: str,
    title_text: str = "3D Glowing Loader",
    body_text: str = "Click the button below to control the animation play state.",
    color_scheme: str = "dark",
    accent_color: str = "#00FFFF",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Contextual thematic styling
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep blue from the tutorial
        text_color = "#FFFFFF"
        surface_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#F0F2F5"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # CSS Generation
    css = f"""/* 3D Glowing Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

.text-content {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.7;
}}

/* -- Core Loader Styles -- */
.loader-wrapper {{
    position: relative;
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading-element {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Dual box shadow for inset and outset neon glow */
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    
    /* Animation Shorthand: duration | timing-function | iteration-count | name */
    animation: 2s ease-in-out infinite loading-sequence;
    
    /* Ensure hardware acceleration for smoother 3D transforms */
    will-change: transform;
}}

/* -- Keyframes mapping the X, Y, Z sequence from the tutorial -- */
@keyframes loading-sequence {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* -- Controls -- */
.controls {{
    display: flex;
    gap: 16px;
    z-index: 10;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 10px 24px;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    box-shadow: 0 0 16px var(--accent);
}}

button.active {{
    background: var(--accent);
    color: #000;
}}
"""

    # HTML Generation
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
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader-wrapper">
            <div class="loading-element" id="spinner"></div>
        </div>
        
        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # JS Generation
    js = f"""// 3D Glowing Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const spinner = document.getElementById('spinner');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Controls the animation-play-state property as demonstrated in the tutorial
    playBtn.addEventListener('click', () => {{
        spinner.style.animationPlayState = 'running';
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        spinner.style.animationPlayState = 'paused';
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
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
