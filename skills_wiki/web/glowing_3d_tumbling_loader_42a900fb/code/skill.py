def create_component(
    output_dir: str,
    title_text: str = "Processing Request...",
    body_text: str = "Please wait while we gather your data.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glowing 3D Tumbling Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep midnight blue
        container_bg = "#0d1124"
        text_color = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f1f5f9"
        container_bg = "#ffffff"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Glowing 3D Tumbling Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --container-bg: {container_bg};
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
    background: var(--container-bg);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 48px;
    padding: 40px;
    position: relative;
}}

.text-group {{
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
}}

/* --- Core Visual Effect --- */
.loader-wrapper {{
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Adding perspective to the wrapper makes the 3D rotation more pronounced */
    perspective: 400px; 
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 10px var(--accent), inset 0 0 10px var(--accent);
    /* 2s duration, smooth easing, infinite loop */
    animation: 2s tumbling ease-in-out infinite;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
}}

/* Interactive Hover Pause */
.loading-cube:hover {{
    animation-play-state: paused;
    box-shadow: 0 0 20px var(--accent), inset 0 0 15px var(--accent);
}}

/* The tumbling logic */
@keyframes tumbling {{
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

/* --- Controls --- */
.controls {{
    display: flex;
    gap: 16px;
    margin-top: 16px;
}}

.btn {{
    padding: 10px 24px;
    background: var(--surface);
    color: var(--text);
    border: 1px solid rgba(150, 150, 150, 0.2);
    border-radius: 8px;
    font-family: inherit;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn:hover {{
    background: rgba(150, 150, 150, 0.15);
    border-color: rgba(150, 150, 150, 0.4);
}}

.btn:active {{
    transform: scale(0.96);
}}

/* Accessibility: Respect Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    .loading-cube {{
        animation: none;
        transform: rotate(45deg);
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
        
        <div class="text-group">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="loader-wrapper">
            <div class="loading-cube" id="loader" title="Hover to pause"></div>
        </div>

        <div class="controls">
            <button class="btn" id="btn-play">Play Animation</button>
            <button class="btn" id="btn-pause">Pause Animation</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glowing 3D Tumbling Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('btn-play');
    const pauseBtn = document.getElementById('btn-pause');

    // Manipulate the animation-play-state property via JavaScript
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
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
