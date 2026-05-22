def create_component(
    output_dir: str,
    title_text: str = "Processing Data...",
    body_text: str = "Please wait while we initialize the environment.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Default to the 'aqua' from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Axis-Rotating Loading Spinner.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#f0f0f0"
        surface_color = "#161b22"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"

    # === CSS ===
    css = f"""/* 3D Neon Axis-Rotating Loading Spinner */
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
}}

.wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background: var(--surface);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

/* Typography */
.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
    max-width: 400px;
}}

/* Loader Container for spatial isolation */
.loader-container {{
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
}}

/* === The Core Loading Component === */
.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 6px; /* Soften the edges slightly */
    
    /* Neon Glow: Inner and Outer shadow */
    box-shadow: 
        0 0 12px var(--accent), 
        inset 0 0 12px var(--accent);
    
    /* 
       animation shorthand:
       name duration timing-function delay iteration-count direction fill-mode
    */
    animation: loadingFlip 2s ease-in-out infinite;
    cursor: pointer;
}}

/* Pause on hover (pure CSS method) */
.loading:hover {{
    animation-play-state: paused;
    box-shadow: 
        0 0 25px var(--accent), 
        inset 0 0 20px var(--accent);
    transition: box-shadow 0.3s ease;
}}

/* Keyframes implementing the 3-axis flip sequence */
@keyframes loadingFlip {{
    0% {{
        /* perspective added to give depth to the 3D flip */
        transform: perspective(200px) rotateX(0) rotateY(0) rotateZ(0);
    }}
    33% {{
        /* Flip forward over the X axis */
        transform: perspective(200px) rotateX(180deg) rotateY(0) rotateZ(0);
    }}
    67% {{
        /* Maintain X flip, flip sideways over the Y axis */
        transform: perspective(200px) rotateX(180deg) rotateY(180deg) rotateZ(0);
    }}
    100% {{
        /* Maintain X and Y flips, rotate like a steering wheel on Z axis */
        transform: perspective(200px) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* Controls UI */
.controls {{
    display: flex;
    gap: 12px;
    margin-top: 30px;
}}

button {{
    background: transparent;
    border: 2px solid var(--accent);
    color: var(--accent);
    padding: 8px 24px;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 1px;
}}

button:hover {{
    background: var(--accent);
    color: var(--bg);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation-duration: 6s; /* Greatly slow down */
        animation-timing-function: linear; /* Remove sudden accelerations */
    }}
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
    <div class="wrapper">
        <div class="loader-container">
            <!-- The extracted component -->
            <div class="loading" aria-busy="true" aria-label="Loading content" title="Hover to pause"></div>
        </div>
        
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>

        <!-- JS Interaction Controls shown in the tutorial -->
        <div class="controls">
            <button id="playBtn">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Loader Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loading');
    const playButton = document.getElementById('playBtn');
    const pauseButton = document.getElementById('pauseBtn');

    // Manipulate the CSS animation-play-state property via JavaScript
    playButton.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseButton.addEventListener('click', () => {{
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
