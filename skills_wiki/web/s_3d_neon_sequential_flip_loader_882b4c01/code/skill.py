def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Fetching resources, please wait...",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua/cyan works best for neon)
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Flip Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark blue/black as seen in the tutorial
        text_color = "#f0f0f0"
        surface_color = "#111526"
        border_color = "rgba(255,255,255,0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0,0,0,0.1)"

    # === CSS ===
    css = f"""/* 3D Neon Sequential Flip Loader — generated component */
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
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    text-align: center;
    padding: 40px;
    position: relative;
    overflow: hidden;
}}

.text-content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.text-content p {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* Core Visual Element: The Loading Square */
.loader-wrapper {{
    /* Providing perspective helps the 3D flips look deeper and more dynamic */
    perspective: 400px; 
    margin: 20px 0;
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Dual Box Shadow for the Neon Glow */
    box-shadow: 
        0 0 12px var(--accent),
        inset 0 0 12px var(--accent);
    /* Shorthand: name duration timing-function iteration-count */
    animation: loadingFlip 2s ease-in-out infinite;
    /* Optional: helps rendering performance */
    will-change: transform;
}}

/* Keyframes for Sequential 3D Axis Rotation */
@keyframes loadingFlip {{
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

/* Controls */
.controls {{
    display: flex;
    gap: 16px;
}}

.btn {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--border);
    padding: 8px 24px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s ease;
    font-family: inherit;
}}

.btn:hover {{
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(255, 255, 255, 0.05);
}}

.btn.active {{
    background: var(--text);
    color: var(--bg);
    border-color: var(--text);
}}

/* Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation-duration: 6s; /* Slows down significantly */
        animation-timing-function: linear;
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
    <div class="container">
        
        <div class="loader-wrapper">
            <!-- The animating element -->
            <div class="loading" id="neonLoader"></div>
        </div>

        <div class="text-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- Interactive Controls -->
        <div class="controls">
            <button class="btn active" id="playBtn">Play</button>
            <button class="btn" id="pauseBtn">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Sequential Flip Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('neonLoader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Manipulate the 'animation-play-state' CSS property dynamically
    
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        
        // Update UI button states
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        
        // Update UI button states
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
