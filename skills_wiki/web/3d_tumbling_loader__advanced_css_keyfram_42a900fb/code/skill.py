def create_component(
    output_dir: str,
    title_text: str = "Processing Data...",
    body_text: str = "Hover over the loader to pause the animation sequence.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Tumbling Loader visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#040716" # Matches the deep blue from the video
        text_color = "#e0e0e0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* 3D Tumbling Loader — generated component */
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
    
    /* Loader specific variables */
    --loader-size: 60px;
    --loader-border: 8px;
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

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rem;
    background: var(--surface);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2rem;
    text-align: center;
}}

.text-content {{
    z-index: 10;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* === Core Visual Effect: The Tumbling Loader === */
.loader-wrapper {{
    position: relative;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 400px; /* Adds 3D depth to the rotations */
}}

.loading-cube {{
    height: var(--loader-size);
    width: var(--loader-size);
    border: var(--loader-border) solid var(--accent);
    border-radius: 6px;
    /* Inset and outset shadow for neon glow */
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    /* 
      Animation shorthand: 
      duration | timing-function | iteration-count | name 
    */
    animation: 2.4s ease-in-out infinite tumbling;
    
    cursor: pointer;
    transition: box-shadow 0.3s ease;
}}

/* Interaction demonstrating animation-play-state */
.loading-cube:hover {{
    animation-play-state: paused;
    box-shadow: 
        0 0 20px var(--accent), 
        0 0 20px var(--accent) inset;
}}

/* Sequence rotates X, then Y, then Z sequentially */
@keyframes tumbling {{
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
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Tumbling Loader</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- The interactive component -->
        <div class="loader-wrapper">
            <div class="loading-cube" title="Hover to pause"></div>
        </div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Interactive behavior is handled via CSS (:hover -> animation-play-state: paused)
// JS included for future extensibility (e.g., listening to custom pause/play events)

document.addEventListener('DOMContentLoaded', () => {{
    const cube = document.querySelector('.loading-cube');
    
    // Example of toggling via JS, though CSS :hover is primary in this demo
    cube.addEventListener('click', () => {{
        const currentState = window.getComputedStyle(cube).animationPlayState;
        if (currentState === 'running') {{
            cube.style.animationPlayState = 'paused';
        }} else {{
            cube.style.animationPlayState = 'running';
        }}
    }});
}});
"""

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
