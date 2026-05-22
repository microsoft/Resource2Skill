def create_component(
    output_dir: str,
    title_text: str = "CSS 3D Loader",
    body_text: str = "Toggle the play state of the CSS animation.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Default aqua/cyan
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Keyframe Loader.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0e14"
        text_color = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        btn_hover = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.05)"
        btn_hover = "rgba(0, 0, 0, 0.1)"

    css = f"""/* 3D Glowing CSS Loader */
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
    --btn-hover: {btn_hover};
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
    justify-content: space-between;
    padding: 4rem 2rem;
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
    border-radius: 16px;
}}

.header {{
    text-align: center;
}}

h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

p {{
    font-size: 1rem;
    opacity: 0.7;
}}

/* === Core Animation Visuals === */
.loader-wrapper {{
    position: relative;
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px; /* Gives realistic depth to the 3D rotation */
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outer and inner glow */
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    
    /* Animation definition */
    animation-name: loading-sequence;
    animation-duration: 2.4s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    animation-fill-mode: forwards;
    
    /* Will be controlled via JS */
    animation-play-state: running; 
}}

/* The 3D rotation sequence extracted from the tutorial */
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

/* === Controls === */
.controls {{
    display: flex;
    gap: 1rem;
    z-index: 10;
}}

button {{
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    font-family: inherit;
    color: var(--text);
    background: var(--surface);
    border: 2px solid transparent;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--btn-hover);
}}

button.active {{
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation-play-state: paused !important;
    }}
}}
"""

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
        
        <div class="loader-wrapper">
            <div class="loading" id="animated-cube"></div>
        </div>

        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Play-State Controller
document.addEventListener('DOMContentLoaded', () => {{
    const cube = document.getElementById('animated-cube');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    playBtn.addEventListener('click', () => {{
        // Set CSS animation-play-state to running
        cube.style.animationPlayState = 'running';
        
        // Update UI
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        // Set CSS animation-play-state to paused
        cube.style.animationPlayState = 'paused';
        
        // Update UI
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
