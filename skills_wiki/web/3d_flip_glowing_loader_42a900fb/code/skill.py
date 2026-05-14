def create_component(
    output_dir: str,
    title_text: str = "Authenticating...",
    body_text: str = "A glowing geometric loader with sequenced 3D axis rotations.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the '3D Flip Glowing Loader' visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Safely escape text
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep blue from tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Flip Glowing Loader — generated component */
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

.widget-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    position: relative;
    overflow: hidden;
    padding: 2rem;
    border-radius: 12px;
}}

/* Header text */
.header {{
    text-align: center;
    z-index: 20;
}}

.header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}}

.header p {{
    font-size: 0.95rem;
    opacity: 0.7;
    max-width: 400px;
    line-height: 1.5;
}}

/* --- Core Loader Styles --- */
.loading-wrapper {{
    position: relative;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Neon glow effect using double box-shadow */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading ease-in-out infinite;
    z-index: 10;
}}

/* --- Sequenced 3D Keyframes --- */
@keyframes loading {{
    0% {{
        transform: rotateX(0) rotateY(0) rotateZ(0);
    }}
    33% {{
        /* Flip vertically */
        transform: rotateX(180deg) rotateY(0) rotateZ(0);
    }}
    67% {{
        /* Flip horizontally */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0);
    }}
    100% {{
        /* Spin flatly back to visual start */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* --- Interactive Controls --- */
.controls {{
    display: flex;
    gap: 1rem;
    z-index: 20;
}}

.controls button {{
    background: var(--surface);
    color: var(--text);
    border: 2px solid rgba(255, 255, 255, 0.1);
    padding: 0.6rem 1.5rem;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.controls button:hover {{
    border-color: var(--accent);
    box-shadow: 0 0 12px rgba(0, 255, 255, 0.2);
}}

.controls button:active {{
    transform: scale(0.95);
}}

.controls button.active {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    box-shadow: 0 0 15px var(--accent);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Glowing Loader</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        
        <div class="header">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>

        <!-- The core component -->
        <div class="loading-wrapper">
            <div class="loading" id="loader"></div>
        </div>

        <!-- JavaScript Interaction Demo -->
        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Flip Glowing Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Handle Play Action
    playBtn.addEventListener('click', () => {{
        // Modify the CSS animation-play-state property
        loader.style.animationPlayState = 'running';
        
        // Update UI button states
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    // Handle Pause Action
    pauseBtn.addEventListener('click', () => {{
        // Modify the CSS animation-play-state property
        loader.style.animationPlayState = 'paused';
        
        // Update UI button states
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
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
