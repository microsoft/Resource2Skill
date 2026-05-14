def create_component(
    output_dir: str,
    title_text: str = "Loading Data...",
    body_text: str = "Please wait while we prepare your experience.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua/cyan works best)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Keyframe Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep blue from the tutorial
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.6)"

    # === CSS ===
    css = f"""/* 3D Glowing Keyframe Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 48px;
    text-align: center;
    perspective: 800px; /* Gives 3D depth to the transforms */
}}

/* Loader Element */
.loading {{
    height: 60px;
    width: 60px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Simultaneous outer and inner glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* Apply the animation */
    animation: loading-sequence 2s ease-in-out infinite;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
}}

/* Interactive play state control */
.loading:hover {{
    animation-play-state: paused;
    box-shadow: 0 0 24px var(--accent), inset 0 0 24px var(--accent);
}}

/* Keyframe Sequence extracting from tutorial */
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

/* Typography */
.content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
}}

.content p {{
    font-size: 0.95rem;
    color: var(--text-muted);
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
        
        <!-- The core visual component -->
        <div class="loading" title="Hover to pause"></div>
        
        <div class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Keyframe Loader
document.addEventListener('DOMContentLoaded', () => {{
    // The core animation is handled purely by CSS.
    // However, we can use JS to toggle the play state on click as an alternative to hover.
    
    const loader = document.querySelector('.loader');
    
    if(loader) {{
        loader.addEventListener('click', () => {{
            const currentState = window.getComputedStyle(loader).getPropertyValue('animation-play-state');
            loader.style.animationPlayState = currentState === 'running' ? 'paused' : 'running';
        }});
    }}
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
