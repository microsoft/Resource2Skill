def create_component(
    output_dir: str,
    title_text: str = "Loading System...",
    body_text: str = "Please wait while we establish a connection.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00FFFF",     # CSS hex color for the glowing accent (cyan/aqua)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Holographic Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep space blue from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#e9ecef"
        text_color = "#212529"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # The loader is a square, we define its size specifically to keep proportions intact
    loader_size = 60

    # === CSS ===
    css = f"""/* 3D Glowing Holographic Loader — generated component */
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
    background: var(--bg);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border-radius: 16px;
    overflow: hidden;
}}

.text-wrapper {{
    position: absolute;
    bottom: 20%;
    text-align: center;
    animation: pulse 2s infinite alternate ease-in-out;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 8px;
    text-transform: uppercase;
    color: var(--accent);
    text-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* === Core Visual Effect: 3D Glowing Loader === */
.loading {{
    height: {loader_size}px;
    width: {loader_size}px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    /* Absolute centering */
    position: absolute;
    top: 50%;
    left: 50%;
    /* Accounting for its own dimensions to center perfectly */
    translate: -50% -50%;
    z-index: 10;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading ease-in-out infinite;
    
    /* Subtle transition for interaction */
    cursor: pointer;
    transition: scale 0.3s ease;
}}

/* Allow users to pause the animation by hovering over it */
.loading:hover {{
    animation-play-state: paused;
    scale: 1.1;
}}

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

@keyframes pulse {{
    0% {{ opacity: 0.6; }}
    100% {{ opacity: 1; }}
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
    <div class="container" role="status" aria-live="polite" aria-label="Loading content">
        
        <!-- The Animated 3D Loader -->
        <div class="loading" id="loader" title="Hover to pause"></div>
        
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Holographic Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    
    // Optional: Add click-to-toggle pause state in addition to CSS hover
    let isPaused = false;
    
    loader.addEventListener('click', () => {{
        isPaused = !isPaused;
        if (isPaused) {{
            loader.style.animationPlayState = 'paused';
            loader.style.borderColor = '#ff3366'; // visual feedback on pause
            loader.style.boxShadow = '0 0 12px #ff3366, 0 0 12px #ff3366 inset';
        }} else {{
            loader.style.animationPlayState = 'running';
            loader.style.borderColor = 'var(--accent)';
            loader.style.boxShadow = '0 0 12px var(--accent), 0 0 12px var(--accent) inset';
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
