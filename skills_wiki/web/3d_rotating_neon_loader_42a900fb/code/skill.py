def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Establishing secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan/Aqua
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Rotating Neon Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716"  # Exact dark background from tutorial
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.1)"
        btn_hover = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f7fb"
        text_color = "#040716"
        surface_color = "rgba(0, 0, 0, 0.1)"
        btn_hover = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* 3D Rotating Neon Loader — generated component */
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

.app-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    border-radius: 16px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    border: 1px solid var(--surface);
}}

/* Visual Stage for the 3D Element */
.visual-stage {{
    position: relative;
    width: 100%;
    height: 200px;
    margin-bottom: 1rem;
}}

.loading-box {{
    /* Modern Centering: Independent Translate */
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    
    /* Box Styles */
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Neon Glow */
    box-shadow: 0 0 12px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation Configuration */
    animation: 2s loading ease-in-out infinite;
    cursor: pointer;
}}

/* 3D Rotation Keyframes */
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

/* Typography */
.content-wrapper {{
    text-align: center;
    z-index: 10;
}}

h1.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}}

p.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
    max-width: 400px;
    margin: 0 auto 2rem auto;
    line-height: 1.5;
}}

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 1rem;
}}

.control-btn {{
    background: transparent;
    color: var(--text);
    border: 1px solid var(--surface);
    padding: 0.5rem 1.25rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
    outline: none;
}}

.control-btn:hover, .control-btn:focus-visible {{
    background: var(--btn-hover);
    border-color: var(--accent);
}}

/* Accessibility: Respect Reduced Motion Preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-box {{
        animation: none;
        transform: rotate(45deg); /* Static, aesthetically pleasing resting state */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <div class="visual-stage">
            <div class="loading-box" id="loaderElement" aria-label="Loading animation" role="progressbar"></div>
        </div>
        
        <div class="content-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="controls">
            <button id="playBtn" class="control-btn" aria-label="Play Animation">Play</button>
            <button id="pauseBtn" class="control-btn" aria-label="Pause Animation">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Rotating Neon Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loaderElement');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Control animation state via buttons
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    // Provide interactive pausing on hover (as demonstrated in tutorial)
    // Using JS events avoids CSS specificity conflicts with inline styles
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    loader.addEventListener('mouseleave', () => {{
        loader.style.animationPlayState = 'running';
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
