def create_component(
    output_dir: str,
    title_text: str = "Loading System...",
    body_text: str = "Fetching data, please wait.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Neon Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#e5e7eb"
        text_color = "#1f2937"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Glowing Neon Loader — generated component */
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
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 40px;
}}

.header {{
    text-align: center;
    z-index: 20;
}}

.header h1 {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.header p {{
    font-size: 14px;
    opacity: 0.7;
    font-weight: 300;
}}

/* -- Core Loading Animation Styles -- */
.loader-wrapper {{
    position: relative;
    flex-grow: 1;
    width: 100%;
}}

.loading {{
    /* Sizing & Borders */
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Neon Glow */
    box-shadow: 0 0 8px var(--accent), 
                0 0 8px var(--accent) inset;
    
    /* Positioning (Using modern independent translate to avoid transform conflicts) */
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: 10;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading ease-in-out infinite;
}}

/* Multi-axis 3D tumbling sequence */
@keyframes loading {{
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

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 16px;
    z-index: 20;
}}

.btn {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--text);
    padding: 10px 24px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn:hover {{
    background: var(--text);
    color: var(--bg);
}}

.btn.active {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    box-shadow: 0 0 12px var(--accent);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="loader-wrapper">
            <!-- The Loader Element -->
            <div class="loading" id="loader"></div>
        </div>

        <!-- Playback State Controls -->
        <div class="controls">
            <button class="btn active" id="playBtn">Play</button>
            <button class="btn" id="pauseBtn">Pause</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Neon Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Manipulate the animation-play-state property directly
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
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
