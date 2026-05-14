def create_component(
    output_dir: str,
    title_text: str = "System Initializing",
    body_text: str = "Please wait while we establish a secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Aqua neon
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Sequential Axis Loader.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        button_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f6f9"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        button_bg = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Sequential Axis Loader */
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
    --button-bg: {button_bg};
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
    background: var(--surface);
    border-radius: 16px;
    border: 1px solid rgba(128, 128, 128, 0.1);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px;
    text-align: center;
    backdrop-filter: blur(10px);
}}

.header {{
    z-index: 20;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 14px;
    opacity: 0.7;
    font-weight: 400;
}}

/* The specific technique demonstrated in the tutorial */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Inset and outset box shadow for the neon tube glow */
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    
    position: absolute;
    top: 50%;
    left: 50%;
    /* Using independent translate property avoids conflicting with transform keyframes */
    translate: -50% -50%;
    z-index: 10;
    
    /* shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading ease-in-out infinite;
}}

@keyframes loading {{
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

/* Interactive controls to demonstrate animation-play-state */
.controls {{
    display: flex;
    gap: 16px;
    justify-content: center;
    z-index: 20;
}}

.btn {{
    background: var(--button-bg);
    color: var(--text);
    border: 1px solid rgba(128, 128, 128, 0.2);
    padding: 10px 24px;
    border-radius: 8px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn:hover {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    box-shadow: 0 0 16px var(--accent);
}}

/* Optional: Pause animation strictly on hover of the loader itself */
.loading:hover {{
    animation-play-state: paused;
    cursor: wait;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loading" id="loader"></div>
        
        <div class="controls">
            <button class="btn" id="playBtn">Play Animation</button>
            <button class="btn" id="pauseBtn">Pause Animation</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Exposing the animation-play-state property via JavaScript
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Dynamically update the CSS animation-play-state property
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
