def create_component(
    output_dir: str,
    title_text: str = "Tumbling Neon Loader",
    body_text: str = "Use the buttons to control the animation play state, as demonstrated in the tutorial.",
    color_scheme: str = "dark",
    accent_color: str = "#00FFFF",  # Aqua neon glow
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Tumbling Neon Loader visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep blue from tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a1a"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Tumbling Neon Loader */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    gap: 3rem;
}}

.header {{
    z-index: 10;
}}

.header h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.header p {{
    opacity: 0.8;
    font-size: 0.95rem;
}}

/* === Core Loader CSS === */
.loader-wrapper {{
    position: relative;
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface-color);
    border-radius: 12px;
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent-color);
    border-radius: 4px;
    /* Outset and Inset shadow for true neon tube effect */
    box-shadow: 0 0 8px var(--accent-color), inset 0 0 8px var(--accent-color);
    z-index: 10;
    
    /* Animation shorthand: name | duration | timing-function | iteration-count */
    animation: loadingFlip 2s ease-in-out infinite;
    
    /* Ensure hardware acceleration for smooth 3D flipping */
    will-change: transform;
}}

@keyframes loadingFlip {{
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

/* Interaction Controls */
.controls {{
    display: flex;
    gap: 1rem;
    z-index: 10;
}}

button {{
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--text-color);
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button.active, button:hover {{
    background: var(--text-color);
    color: var(--bg-color);
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
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- The Loader -->
        <div class="loader-wrapper">
            <div class="loading" id="loader"></div>
        </div>

        <!-- Animation Play State Controls -->
        <div class="controls">
            <button id="playButton" class="active">Play</button>
            <button id="pauseButton">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Tumbling Neon Loader - JS Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playButton');
    const pauseBtn = document.getElementById('pauseButton');

    // Control animation-play-state via JS
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
