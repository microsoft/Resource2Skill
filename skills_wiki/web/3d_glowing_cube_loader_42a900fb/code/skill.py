def create_component(
    output_dir: str,
    title_text: str = "Loading System",
    body_text: str = "Initiating spatial rotation matrix...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan/Aqua
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Cube Loader.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html as pyhtml

    os.makedirs(output_dir, exist_ok=True)

    # Escape text to prevent HTML injection
    safe_title = pyhtml.escape(title_text)
    safe_body = pyhtml.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#e0e6ed"
        btn_bg = "rgba(255, 255, 255, 0.1)"
        btn_hover = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f7f9"
        text_color = "#1a202c"
        btn_bg = "rgba(0, 0, 0, 0.05)"
        btn_hover = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Glowing Cube Loader — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
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
    text-align: center;
    gap: 2rem;
}}

/* Loader Styling */
.loader-wrapper {{
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent-color);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent-color), 
                0 0 8px var(--accent-color) inset;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s spin-axes ease-in-out infinite;
}}

/* The 3-axis rotation sequence */
@keyframes spin-axes {{
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

/* Typography */
.content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}}

.content p {{
    font-size: 0.95rem;
    opacity: 0.7;
    max-width: 400px;
    line-height: 1.5;
}}

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

button {{
    background: var(--btn-bg);
    color: var(--text-color);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1.25rem;
    border-radius: 6px;
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background 0.2s ease;
}}

button:hover {{
    background: var(--btn-hover);
}}

button:active {{
    transform: scale(0.96);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="loader-wrapper">
            <div class="loading-cube" id="cube"></div>
        </div>
        
        <div class="content">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>

        <div class="controls">
            <button id="playBtn">Play Animation</button>
            <button id="pauseBtn">Pause Animation</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Cube Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const cube = document.getElementById('cube');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Control the CSS animation-play-state property via JavaScript
    playBtn.addEventListener('click', () => {{
        cube.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        cube.style.animationPlayState = 'paused';
    }});

    // Optional: Pause on hover as demonstrated in the tutorial
    cube.addEventListener('mouseenter', () => {{
        cube.style.animationPlayState = 'paused';
    }});
    
    cube.addEventListener('mouseleave', () => {{
        cube.style.animationPlayState = 'running';
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
