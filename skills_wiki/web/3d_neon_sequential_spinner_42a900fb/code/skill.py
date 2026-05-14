def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Processing your request, please wait...",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for the neon glow
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Sequential Spinner visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark blue from tutorial
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        text_muted = "rgba(0, 0, 0, 0.6)"

    # === CSS ===
    css = f"""/* 3D Neon Sequential Spinner — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    position: relative;
}}

/* The Core Loader Element */
.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outward glow and inner glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    cursor: pointer;
    
    /* Tutorial Animation settings */
    animation-name: loading-sequence;
    animation-duration: 2s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
}}

/* Pause on hover to demonstrate animation-play-state */
.loader:hover {{
    animation-play-state: paused;
}}

/* Text styling */
.text-container {{
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
    color: var(--text-muted);
    font-weight: 400;
}}

.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}}

button {{
    background: transparent;
    border: 1px solid var(--text-muted);
    color: var(--text);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.85rem;
    transition: all 0.2s ease;
}}

button:hover {{
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.2);
}}

button.active {{
    background: var(--text);
    color: var(--bg);
}}

/* The 3D Keyframe Sequence */
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
"""

    # === HTML ===
    # Escaping text inputs to prevent raw HTML breaking
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container" aria-live="polite" aria-busy="true">
        
        <!-- Interactive Loader -->
        <div class="loader" role="progressbar" aria-label="Loading..." tabindex="0"></div>
        
        <div class="text-container">
            <h1 class="title">{safe_title}</h1>
            <p class="body-text">{safe_body}</p>
        </div>

        <!-- JS Controls for Play State -->
        <div class="controls">
            <button id="btn-play" class="active">Play</button>
            <button id="btn-pause">Pause</button>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Sequential Spinner — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loader');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');

    // Toggle logic for the loader itself (click to pause/resume)
    let isPlaying = true;
    
    loader.addEventListener('click', () => {{
        isPlaying = !isPlaying;
        updatePlayState(isPlaying);
    }});

    // Explicit buttons matching the tutorial's JS logic
    btnPlay.addEventListener('click', () => updatePlayState(true));
    btnPause.addEventListener('click', () => updatePlayState(false));

    function updatePlayState(playing) {{
        isPlaying = playing;
        if (isPlaying) {{
            loader.style.animationPlayState = 'running';
            btnPlay.classList.add('active');
            btnPause.classList.remove('active');
        }} else {{
            loader.style.animationPlayState = 'paused';
            btnPause.classList.add('active');
            btnPlay.classList.remove('active');
        }}
    }}
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
