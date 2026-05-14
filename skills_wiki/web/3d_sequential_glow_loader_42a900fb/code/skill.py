def create_component(
    output_dir: str,
    title_text: str = "Processing Data",
    body_text: str = "Please wait while we synthesize your request...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Aqua/Cyan glow by default
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Sequential Glow Loader visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark blue from the video
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Sequential Glow Loader — generated component */
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
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
    border-radius: 24px;
}}

.text-wrapper {{
    position: absolute;
    top: 20%;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.body-text {{
    font-size: 0.9rem;
    color: var(--text);
    opacity: 0.7;
}}

/* === Core Loader Styles === */
.loader-wrapper {{
    position: relative;
    width: 200px;
    height: 200px;
    /* Optional perspective to enhance the 3D effect slightly */
    perspective: 800px; 
}}

.loading-box {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outer glow + Inner glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: 10;
    /* Shorthand: duration | timing-function | iteration-count | name */
    animation: 2s ease-in-out infinite tumbling;
}}

/* Keyframes mapped exactly to the tutorial's logic */
@keyframes tumbling {{
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

/* === Controls (Interactive feature from video) === */
.controls {{
    position: absolute;
    bottom: 20%;
    display: flex;
    gap: 1rem;
}}

.btn-toggle {{
    background: transparent;
    border: 2px solid var(--accent);
    color: var(--accent);
    padding: 0.5rem 1.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-toggle:hover {{
    background: var(--accent);
    color: var(--bg);
    box-shadow: 0 0 15px var(--accent);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-box {{
        animation-duration: 8s;
        box-shadow: none; /* Remove intensive shadow rendering */
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
    <main class="container" aria-live="polite" aria-busy="true">
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader-wrapper">
            <!-- Core Component -->
            <div class="loading-box" id="activeLoader"></div>
        </div>

        <div class="controls">
            <button class="btn-toggle" id="playPauseBtn" aria-controls="activeLoader">Pause Animation</button>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Sequential Glow Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('activeLoader');
    const playPauseBtn = document.getElementById('playPauseBtn');
    
    let isPlaying = true;

    // Toggle CSS animation-play-state
    playPauseBtn.addEventListener('click', () => {{
        if (isPlaying) {{
            loader.style.animationPlayState = 'paused';
            playPauseBtn.textContent = 'Play Animation';
        }} else {{
            loader.style.animationPlayState = 'running';
            playPauseBtn.textContent = 'Pause Animation';
        }}
        isPlaying = !isPlaying;
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
