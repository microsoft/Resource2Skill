def create_component(
    output_dir: str,
    title_text: str = "Loading Data...",
    body_text: str = "Please wait while we process your request.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # aqua / cyan
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sequential 3D Axis-Rotation Loading Indicator.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Video's exact dark navy background
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Sequential 3D Axis-Rotation Loading Indicator */
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
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    position: relative;
    perspective: 800px; /* Gives realistic depth to the 3D rotation */
}}

.text-wrapper {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* The Core Visual Component */
.loading-indicator {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
    animation: seq-rotate 2s ease-in-out infinite;
    
    /* Play state controlled via JS */
    animation-play-state: running; 
}}

/* The Sequential 3D Keyframes */
@keyframes seq-rotate {{
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

/* Interactive Controls (Demonstrating play-state) */
.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid rgba(128, 128, 128, 0.3);
    padding: 0.5rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}}

button:hover {{
    background: rgba(128, 128, 128, 0.2);
}}

button.active {{
    background: var(--accent);
    color: {bg_color};
    border-color: var(--accent);
    font-weight: 600;
    box-shadow: 0 0 10px var(--accent);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Loading Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <!-- Core Component -->
        <div class="loading-indicator" aria-label="Loading" role="status"></div>

        <!-- Demonstration Controls -->
        <div class="controls">
            <button id="btn-play" class="active">Play</button>
            <button id="btn-pause">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive behavior demonstrating animation-play-state manipulation
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loading-indicator');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');

    // Play Button Logic
    btnPlay.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        btnPlay.classList.add('active');
        btnPause.classList.remove('active');
    }});

    // Pause Button Logic
    btnPause.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        btnPause.classList.add('active');
        btnPlay.classList.remove('active');
    }});

    // Hover effect bonus (Pauses when hovered over)
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    loader.addEventListener('mouseleave', () => {{
        if (btnPlay.classList.contains('active')) {{
            loader.style.animationPlayState = 'running';
        }}
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
