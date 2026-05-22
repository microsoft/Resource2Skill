def create_component(
    output_dir: str,
    title_text: str = "Loading System",
    body_text: str = "Please wait while we initialize the tumbling sequence...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff", # Aqua / Cyan neon color
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Tumbling Glowing Loader.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark blue from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        btn_bg = "#ffffff"
        btn_text = "#000000"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        btn_bg = "#000000"
        btn_text = "#ffffff"

    # === CSS ===
    css = f"""/* 3D Tumbling Glowing Loader */
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    position: relative;
}}

.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.text-content h1 {{
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 1px;
}}

.text-content p {{
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.95rem;
}}

/* -- Loader Core Styles -- */
.loader-wrapper {{
    perspective: 800px; /* Optional: adds realistic 3D depth to the rotation */
    width: 100px;
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
    box-shadow: 0 0 8px var(--accent), inset 0 0 8px var(--accent);
    
    /* Shorthand: name duration timing-function iteration-count */
    animation: tumbling 2s ease-in-out infinite;
    
    /* Play state defaults to running, can be toggled by JS */
    animation-play-state: running; 
}}

/* Keyframes implementing the 3 axis rotations */
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

/* -- Controls -- */
.controls {{
    display: flex;
    gap: 1rem;
}}

button {{
    padding: 0.6rem 1.5rem;
    font-family: inherit;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    border: none;
    border-radius: 6px;
    transition: transform 0.15s ease, opacity 0.15s ease;
}}

button:active {{
    transform: scale(0.95);
}}

button:hover {{
    opacity: 0.8;
}}

.btn-toggle {{
    background: {btn_bg};
    color: {btn_text};
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="text-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- Component Markup -->
        <div class="loader-wrapper">
            <div class="loading-cube" id="loader"></div>
        </div>

        <!-- Interactive Controls -->
        <div class="controls">
            <button class="btn-toggle" id="toggleBtn">Pause Animation</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Tumbling Loader - interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const toggleBtn = document.getElementById('toggleBtn');

    toggleBtn.addEventListener('click', () => {{
        // Get the current computed style of the animation state
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            toggleBtn.textContent = 'Play Animation';
        }} else {{
            loader.style.animationPlayState = 'running';
            toggleBtn.textContent = 'Pause Animation';
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
