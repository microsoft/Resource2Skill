def create_component(
    output_dir: str,
    title_text: str = "Loading System...",
    body_text: str = "Please wait while we initialize the interface.",
    color_scheme: str = "dark",
    accent_color: str = "#00FFFF",  # Defaulting to cyan/aqua as in the video
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Tumbling Neon Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape texts
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep space blue from the video
        text_color = "#f0f0f0"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* 3D Tumbling Neon Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
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
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

/* Typography */
.text-content {{
    text-align: center;
    z-index: 20;
    margin-top: 4rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* Core Loader Styles */
.loading-wrapper {{
    position: relative;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), inset 0 0 8px var(--accent);
    z-index: 10;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s tumbling ease-in-out infinite;
    
    /* Optional: allows pausing via JS state class */
    transition: box-shadow 0.3s ease;
}}

/* Pause animation on hover */
.loading-wrapper:hover .loader {{
    animation-play-state: paused;
    box-shadow: 0 0 16px var(--accent), inset 0 0 16px var(--accent);
    cursor: pointer;
}}

/* 3D Tumbling Keyframes Sequence */
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

/* Optional Controls styling */
.controls {{
    position: absolute;
    bottom: 2rem;
    display: flex;
    gap: 1rem;
}}

button {{
    background: transparent;
    color: var(--text);
    border: 1px solid var(--text);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-family: inherit;
    cursor: pointer;
    font-size: 0.8rem;
    opacity: 0.5;
    transition: all 0.2s;
}}

button:hover, button.active {{
    opacity: 1;
    border-color: var(--accent);
    color: var(--accent);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
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
    <div class="container">
        
        <!-- Interactive loader area -->
        <div class="loading-wrapper" title="Hover to pause">
            <div class="loader" id="loader"></div>
        </div>

        <div class="text-content">
            <h1 class="title">{safe_title}</h1>
            <p class="body-text">{safe_body}</p>
        </div>

        <div class="controls">
            <button id="btnPlay" class="active">Play</button>
            <button id="btnPause">Pause</button>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Tumbling Neon Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const btnPlay = document.getElementById('btnPlay');
    const btnPause = document.getElementById('btnPause');

    // Handle Play button click
    btnPlay.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
        btnPlay.classList.add('active');
        btnPause.classList.remove('active');
    }});

    // Handle Pause button click
    btnPause.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
        btnPause.classList.add('active');
        btnPlay.classList.remove('active');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
