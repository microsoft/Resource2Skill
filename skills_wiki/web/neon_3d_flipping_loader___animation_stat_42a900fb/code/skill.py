def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Controller",
    body_text: str = "Loading sequence with 3D axis rotation.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon 3D Flipping Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a12"
        text_color = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Neon 3D Flipping Loader — generated component */
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
    --border: {border_color};
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
    gap: 60px;
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px;
}}

.header-text {{
    text-align: center;
    z-index: 10;
}}

.header-text h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

.header-text p {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* -- Loader Visual Effect -- */
.stage {{
    position: relative;
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px; /* Gives realistic depth to the 3D transforms */
}}

.loading-cube {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Dual box shadow for neon glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
    animation: flipSequence 2.4s ease-in-out infinite;
    
    /* Ensure hardware acceleration */
    will-change: transform;
}}

/* Pause on hover (CSS alternative method showcased in tutorial) */
.loading-cube:hover {{
    animation-play-state: paused;
    cursor: wait;
}}

@keyframes flipSequence {{
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

/* -- Controls -- */
.controls {{
    display: flex;
    gap: 16px;
    z-index: 10;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}}

button:hover {{
    background: var(--border);
    transform: translateY(-2px);
}}

button.active {{
    border-color: var(--accent);
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.2);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-cube {{
        animation: none;
        transform: rotateX(45deg) rotateY(45deg); /* Static interesting state */
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
    <div class="container">
        <div class="header-text">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="stage">
            <div class="loading-cube" id="target-element" role="status" aria-label="Loading"></div>
        </div>

        <div class="controls">
            <button id="btn-play" class="active">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                Play
            </button>
            <button id="btn-pause">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                Pause
            </button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animation state controller logic
document.addEventListener('DOMContentLoaded', () => {{
    const targetElement = document.getElementById('target-element');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');

    // Handle Play Button Click
    btnPlay.addEventListener('click', () => {{
        // Set animation playback state to running
        targetElement.style.animationPlayState = 'running';
        
        // Update UI
        btnPlay.classList.add('active');
        btnPause.classList.remove('active');
    }});

    // Handle Pause Button Click
    btnPause.addEventListener('click', () => {{
        // Set animation playback state to paused
        targetElement.style.animationPlayState = 'paused';
        
        // Update UI
        btnPause.classList.add('active');
        btnPlay.classList.remove('active');
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
