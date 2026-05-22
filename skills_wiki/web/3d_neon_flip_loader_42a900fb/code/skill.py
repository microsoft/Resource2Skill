def create_component(
    output_dir: str,
    title_text: str = "System Initializing",
    body_text: str = "Fetching resources, please wait... (Click loader to pause/resume)",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     # Aqua/Cyan looks best for the neon effect
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the '3D Neon Flip Loader' visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors from color_scheme
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep blue from tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f7f6"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Neon Flip Loader — generated component */
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
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
    border-radius: 16px;
}}

/* Text Container */
.text-content {{
    position: absolute;
    bottom: 25%;
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.body-text {{
    font-size: 0.9rem;
    color: var(--text);
    opacity: 0.7;
}}

/* The Core Loader Component */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Double box-shadow for external and internal neon glow */
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    
    /* Centering */
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    
    /* Animation Assignment */
    animation-name: flipSequence;
    animation-duration: 2s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    
    /* Hardware acceleration hint */
    will-change: transform;
    cursor: pointer;
    transition: filter 0.3s ease;
}}

.loading:hover {{
    filter: brightness(1.3);
}}

/* Keyframes matching the sequence from the tutorial */
@keyframes flipSequence {{
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

/* Accessibility: Stop animation if user prefers reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation: none;
        transform: rotateX(45deg) rotateY(45deg);
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
        <!-- Interactive Loader Element -->
        <div class="loading" id="loader" title="Click to Pause/Play"></div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Flip Loader Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    
    // Demonstrate 'animation-play-state' manipulation taught in the tutorial
    loader.addEventListener('click', () => {{
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            loader.style.filter = 'grayscale(0.8) opacity(0.5)';
        }} else {{
            loader.style.animationPlayState = 'running';
            loader.style.filter = '';
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
