def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Masterclass",
    body_text: str = "Observe the 3D multi-axis rotation. Use the controls to pause and play.",
    color_scheme: str = "dark",        
    accent_color: str = "#00FFFF",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Infinite Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        button_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"
        button_bg = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Glowing Infinite Loader — generated component */
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
    max-width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rem;
    padding: 2rem;
}}

.header {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

/* The Core Loading Animation Component */
.loader-wrapper {{
    position: relative;
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px; /* Gives realistic depth to the 3D rotation */
}}

.loading-cube {{
    height: 60px;
    width: 60px;
    border: 6px solid var(--accent);
    border-radius: 6px;
    background: transparent;
    
    /* Outset and inset glow using the accent color */
    box-shadow: 
        0 0 15px var(--accent), 
        inset 0 0 15px var(--accent);
        
    /* 
      Shorthand: name | duration | timing-function | iteration-count
      Tutorial specific: 2s loading ease-in-out infinite
    */
    animation: multi-axis-spin 2s ease-in-out infinite;
}}

/* Keyframes mirroring the tutorial's exact rotation arc */
@keyframes multi-axis-spin {{
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

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 1rem;
    z-index: 10;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 2px solid var(--btn-bg);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

button:hover {{
    border-color: var(--accent);
    background: var(--btn-bg);
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}}

button.active {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    box-shadow: 0 0 15px var(--accent);
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
        
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="loader-wrapper">
            <div class="loading-cube" id="loader"></div>
        </div>

        <div class="controls">
            <button id="btn-play" class="active">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M8 5v14l11-7z"/></svg>
                Play
            </button>
            <button id="btn-pause">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                Pause
            </button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Infinite Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('btn-play');
    const pauseBtn = document.getElementById('btn-pause');

    // Utilize animation-play-state to control the CSS animation
    
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
    
    // Optional: Also pause on hover over the loader itself
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    loader.addEventListener('mouseleave', () => {{
        // Only resume if the Play button is the active state
        if (playBtn.classList.contains('active')) {{
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
