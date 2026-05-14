def create_component(
    output_dir: str,
    title_text: str = "Processing Data",
    body_text: str = "Please wait while we establish a secure connection...",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "aqua",        # CSS color for neon glow
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon 3D Sequential CSS Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#040716" # Matches video background
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f6f9"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Neon 3D Sequential CSS Loader — generated component */
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
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
    position: relative;
}}

.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--accent);
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
}}

/* === Core Animation Visuals === */
.loading-wrapper {{
    position: relative;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Adding perspective enhances the 3D effect slightly, though optional */
    perspective: 400px; 
    cursor: pointer;
}}

.loading-indicator {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading-sequence ease-in-out infinite;
}}

/* Pause animation on hover to demonstrate animation-play-state */
.loading-wrapper:hover .loading-indicator {{
    animation-play-state: paused;
}}

.loading-wrapper::after {{
    content: 'HOVER TO PAUSE';
    position: absolute;
    bottom: -30px;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    opacity: 0;
    transition: opacity 0.3s ease;
    color: var(--text);
    white-space: nowrap;
}}

.loading-wrapper:hover::after {{
    opacity: 0.5;
}}

/* 
  Sequential Keyframes: 
  Divides 100% into roughly three 33% chunks.
  Rotates X, then adds Y, then adds Z. 
*/
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

/* Interactive Control Button styling */
.controls {{
    display: flex;
    gap: 16px;
    margin-top: 20px;
}}

button {{
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--text);
    padding: 8px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--accent);
    color: var(--bg);
    box-shadow: 0 0 12px var(--accent);
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
        
        <div class="loading-wrapper" id="loaderWrapper">
            <div class="loading-indicator" id="loaderElement"></div>
        </div>

        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="controls">
            <button id="btnPlay">Play</button>
            <button id="btnPause">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon 3D Sequential CSS Loader — Interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loaderElement = document.getElementById('loaderElement');
    const btnPlay = document.getElementById('btnPlay');
    const btnPause = document.getElementById('btnPause');

    // Demonstrating JS control over CSS animation-play-state
    // This connects to the specific segment of the tutorial regarding play state manipulation
    
    btnPlay.addEventListener('click', () => {{
        loaderElement.style.animationPlayState = 'running';
    }});

    btnPause.addEventListener('click', () => {{
        loaderElement.style.animationPlayState = 'paused';
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
