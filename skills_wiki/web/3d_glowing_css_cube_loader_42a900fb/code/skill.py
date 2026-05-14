def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Establishing secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Default to aqua from the tutorial
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing CSS Cube Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Matches tutorial background
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* 3D Glowing CSS Cube Loader — generated component */
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
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid var(--surface);
}}

.text-content {{
    text-align: center;
    z-index: 20;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 0.9rem;
    color: var(--text);
    opacity: 0.7;
}}

/* Core Loading Animation Styles */
.loading-wrapper {{
    position: relative;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px; /* Adds 3D perspective to the container */
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    z-index: 10;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s spinXyz ease-in-out infinite;
    animation-play-state: running;
}}

/* 3D Rotation Keyframes */
@keyframes spinXyz {{
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

/* Controls */
.controls {{
    display: flex;
    gap: 16px;
    margin-top: 20px;
}}

.btn {{
    padding: 10px 24px;
    border: none;
    border-radius: 6px;
    font-family: inherit;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
}}

.btn-play {{
    background: var(--text);
    color: var(--bg);
}}

.btn-pause {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.btn:active {{
    transform: scale(0.96);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="loading-wrapper">
            <!-- The animated element -->
            <div class="loading-cube" id="loader"></div>
        </div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="controls">
            <button class="btn btn-play" id="playBtn">Play</button>
            <button class="btn btn-pause" id="pauseBtn">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing CSS Cube Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Utilize the CSS animation-play-state property to control the animation
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        // Visual feedback for buttons
        playBtn.style.opacity = '1';
        pauseBtn.style.opacity = '0.6';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        // Visual feedback for buttons
        pauseBtn.style.opacity = '1';
        playBtn.style.opacity = '0.6';
    }});

    // Set initial button states
    pauseBtn.style.opacity = '0.6';
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
