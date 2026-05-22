def create_component(
    output_dir: str,
    title_text: str = "System Loading...",
    body_text: str = "Click the cube to pause/play the animation",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan/Aqua
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the '3D Glowing Flip Loader' visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Glowing Flip Loader — generated component */
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
    background-color: var(--bg);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

.text-wrapper {{
    position: absolute;
    top: 20%;
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.6;
    font-weight: 300;
}}

/* Core Visual Effect Styles */
.loading-wrapper {{
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    /* Add perspective to parent for better 3D depth, though video didn't strictly use it, it enhances the effect */
    perspective: 800px; 
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outer and inner glow */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading ease-in-out infinite;
    
    /* Interactive pointer */
    cursor: pointer;
    z-index: 10;
}}

/* The 3-stage 3D tumbling sequence */
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

/* Visual feedback on hover to indicate interactability */
.loading-cube:hover {{
    filter: brightness(1.3);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loading-wrapper">
            <div class="loading-cube" id="loader" title="Click to Play/Pause"></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Flip Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const statusText = document.querySelector('.body-text');
    let isRunning = true;
    const defaultText = "{body_text}";

    // Toggle animation play state on click
    loader.addEventListener('click', () => {{
        isRunning = !isRunning;
        
        if (isRunning) {{
            loader.style.animationPlayState = 'running';
            statusText.innerText = defaultText;
        }} else {{
            loader.style.animationPlayState = 'paused';
            statusText.innerText = "Animation Paused";
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
