def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Initializing secure connection protocols...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Cube Loading Animation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep midnight blue from the video
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Glowing Cube Loading Animation */
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
    --border: {border_color};
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
    gap: 60px;
}}

.text-content {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 14px;
    color: var(--text);
    opacity: 0.7;
}}

/* === Core Animation Component === */
.loading-wrapper {{
    perspective: 800px; /* Adds 3D depth to the rotation */
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100px;
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outer glow and inner glow */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Animation Configuration */
    animation-name: loading-tumble;
    animation-duration: 2s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    animation-play-state: running; /* Default state */
}}

/* Sequence: X-axis -> Y-axis -> Z-axis */
@keyframes loading-tumble {{
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

/* === Interactive Controls === */
.controls {{
    margin-top: 20px;
}}

.toggle-btn {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}}

.toggle-btn:hover {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
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
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loading-wrapper">
            <!-- The Loader Element -->
            <div class="loading" id="loader"></div>
        </div>
        
        <div class="controls">
            <button class="toggle-btn" id="toggleBtn">Pause Animation</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Cube Loading Animation - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const toggleBtn = document.getElementById('toggleBtn');
    
    // Track the current animation state
    let isPlaying = true;
    
    toggleBtn.addEventListener('click', () => {{
        if (isPlaying) {{
            // Pause the animation freezing it at its current keyframe
            loader.style.animationPlayState = 'paused';
            toggleBtn.textContent = 'Play Animation';
        }} else {{
            // Resume the animation
            loader.style.animationPlayState = 'running';
            toggleBtn.textContent = 'Pause Animation';
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
