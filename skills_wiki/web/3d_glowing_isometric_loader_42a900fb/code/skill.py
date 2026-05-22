def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Initializing interface modules...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff", # Aqua / Cyan is best for the neon effect
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Isometric Loader effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#040716" # Deep space blue from tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        button_bg = "rgba(255,255,255,0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"
        button_bg = "rgba(0,0,0,0.1)"

    css = f"""/* 3D Glowing Isometric Loader */
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
    --btn-bg: {button_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
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
    justify-content: space-between;
    padding: 40px;
    background: var(--surface);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
}}

.header {{
    text-align: center;
    z-index: 20;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* === Core Animation Visuals === */
.loader-wrapper {{
    position: relative;
    flex-grow: 1;
    width: 100%;
}}

.loading-element {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), inset 0 0 8px var(--accent);
    
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: 10;
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
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

/* === Controls === */
.controls {{
    display: flex;
    gap: 16px;
    z-index: 20;
}}

button {{
    background: var(--btn-bg);
    color: var(--text);
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-family: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}}

button:hover {{
    background: var(--accent);
    color: {bg_color};
    box-shadow: 0 0 12px var(--accent);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader-wrapper">
            <div class="loading-element" aria-busy="true" role="progressbar"></div>
        </div>
        
        <div class="controls">
            <button id="playBtn">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// 3D Isometric Loader - JavaScript Controls
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loading-element');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Manipulate the animation-play-state property as shown in tutorial
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    // Optional: Pause on hover for enhanced interactivity
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    loader.addEventListener('mouseleave', () => {{
        loader.style.animationPlayState = 'running';
    }});
}});
"""

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
