def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Please wait while we establish a secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",     # Default to a bright cyan/aqua
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Tumbling 3D CSS Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep navy from the tutorial
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.15)"
        text_dim = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a202c"
        surface_color = "rgba(0, 0, 0, 0.15)"
        text_dim = "rgba(0, 0, 0, 0.6)"

    # Escape HTML safely
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === CSS ===
    css = f"""/* Neon Tumbling 3D CSS Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-dim: {text_dim};
    --accent: {accent_color};
    --surface: {surface_color};
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
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}}

/* -- Core Loading Animation Elements -- */
.loader-wrapper {{
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Inner and outer glow to create the neon effect */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation definition */
    animation: 2s loading ease-in-out infinite;
    cursor: pointer;
    will-change: transform;
}}

/* Sequence rotates on X, then Y, then Z axis incrementally */
@keyframes loading {{
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

/* -- Typography & Controls -- */
.text-content {{
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 2rem;
}}

.text-content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
}}

.text-content p {{
    color: var(--text-dim);
    font-size: 0.95rem;
}}

.controls {{
    display: flex;
    gap: 1rem;
}}

button {{
    background: transparent;
    color: var(--text-dim);
    border: 1px solid var(--surface);
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.2s ease;
}}

button:hover, button.active {{
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.2);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="loader-wrapper">
            <div class="loading-cube" id="loader" title="Hover to pause"></div>
        </div>
        
        <div class="text-content">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>

        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Tumbling 3D CSS Loader — Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // JS manipulation of animationPlayState
    const setPlayState = (state) => {{
        loader.style.animationPlayState = state;
        
        if (state === 'running') {{
            playBtn.classList.add('active');
            pauseBtn.classList.remove('active');
        }} else {{
            pauseBtn.classList.add('active');
            playBtn.classList.remove('active');
        }}
    }};

    playBtn.addEventListener('click', () => setPlayState('running'));
    pauseBtn.addEventListener('click', () => setPlayState('paused'));
    
    // Additional interactivity: Pause when user hovers over the loading element
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    loader.addEventListener('mouseleave', () => {{
        // Only resume if the Play button is supposed to be active
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
