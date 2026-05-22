def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Please wait while we initialize the 3D interface...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     # Default aqua neon
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Rotating Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Deep blue-black from video
        text_color = "#a0a5b5"
    else:
        bg_color = "#f0f2f5"
        text_color = "#333333"

    # === CSS ===
    css = f"""/* 3D Neon Rotating Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
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
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Optional: Adding perspective to the container gives the tumbling more 3D depth, 
       but keeping it flat matches the isometric orthographic style of the video */
}}

.text-content {{
    position: absolute;
    bottom: 20%;
    text-align: center;
    opacity: 0.8;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--accent);
    letter-spacing: 1px;
}}

.body-text {{
    font-size: 0.9rem;
}}

/* === Core Visual Effect: Rotating Loader === */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    
    /* 2s duration, ease-in-out curve for smooth snaps, infinite loop */
    animation: loading-sequence 2s ease-in-out infinite;
}}

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

/* Accessibility: Stop animation if user prefers reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation: none;
        transform: rotateX(45deg) rotateY(45deg);
        opacity: 0.5;
    }}
    .title::after {{
        content: "...";
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
        
        <!-- Interactive loader element -->
        <div class="loading" role="progressbar" aria-label="Loading Application"></div>
        
        <!-- Contextual text -->
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Rotating Loader
// The core animation is purely CSS-driven, so JS is kept minimal.

document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loading');
    
    // Example interactive behavior: click loader to pause/play
    loader.addEventListener('click', () => {{
        const currentState = getComputedStyle(loader).animationPlayState;
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            loader.style.opacity = '0.5';
        }} else {{
            loader.style.animationPlayState = 'running';
            loader.style.opacity = '1';
        }}
    }});
    
    // Add hover cursor indication
    loader.style.cursor = 'pointer';
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
