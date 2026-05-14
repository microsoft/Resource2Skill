def create_component(
    output_dir: str,
    title_text: str = "Loading Application",
    body_text: str = "Click the cube to pause/play the animation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glowing 3D CSS Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Matches the tutorial's background
        text_color = "#f0f0f0"
        muted_text = "#8a93a8"
    else:
        bg_color = "#f4f4f5"
        text_color = "#1a1a2e"
        muted_text = "#646b7a"

    # === CSS ===
    css = f"""/* Glowing 3D CSS Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {muted_text};
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
    max-width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.text-content {{
    text-align: center;
    margin-top: 60px;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.9rem;
    color: var(--muted);
}}

/* === Core Animation Visuals === */

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 
        0 0 8px var(--accent), 
        0 0 8px var(--accent) inset;
    
    /* 
      animation shorthand: 
      duration | name | timing-function | iteration-count 
    */
    animation: 2s loading ease-in-out infinite;
    cursor: pointer;
    transition: scale 0.2s ease;
    
    /* Center transform origin for precise tumbling */
    transform-origin: center center;
}}

.loading-cube:hover {{
    scale: 1.1;
}}

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

/* Accessibility: Respect user's motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-cube {{
        animation: 2s pulse ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(0.95); }}
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
        
        <!-- The Core Loader Component -->
        <div class="loading-cube" id="loader" role="progressbar" aria-label="Loading"></div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glowing 3D CSS Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    
    // Track the play state
    let isPlaying = true;

    // Toggle CSS animation-play-state on click
    loader.addEventListener('click', () => {{
        if (isPlaying) {{
            loader.style.animationPlayState = 'paused';
            isPlaying = false;
        }} else {{
            loader.style.animationPlayState = 'running';
            isPlaying = true;
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
