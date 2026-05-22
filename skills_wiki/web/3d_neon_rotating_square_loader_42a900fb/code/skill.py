def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Click the square to pause/play the animation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua)
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Rotating Square Loader.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Exact dark background from the tutorial
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f6f9"
        text_color = "#040716"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Neon Rotating Square Loader */
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
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 1px solid var(--surface);
}}

/* Header section for text content */
.content {{
    padding: 2rem;
    text-align: center;
    z-index: 20;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
    font-weight: 300;
}}

/* Interactive container area */
.loader-area {{
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}}

/* The Core Loader Element */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Center positioning independent of transform */
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: 10;
    
    /* Animation setup */
    animation: 2s tumbling ease-in-out infinite;
    
    /* Smooth transition for hover effects */
    transition: filter 0.3s ease;
}}

/* Interactive Hover State */
.loader-area:hover .loading {{
    filter: brightness(1.3) drop-shadow(0 0 10px var(--accent));
}}

/* The 3D Rotation Sequence */
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

/* Badge to show current state */
.status-badge {{
    position: absolute;
    bottom: 20px;
    left: 50%;
    translate: -50% 0;
    padding: 6px 12px;
    background: var(--surface);
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--accent);
    pointer-events: none;
    transition: opacity 0.3s;
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
        <div class="content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader-area" id="interactive-area">
            <div class="loading" id="loader"></div>
            <div class="status-badge" id="status">Running</div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Logic to control animation-play-state
document.addEventListener('DOMContentLoaded', () => {{
    const area = document.getElementById('interactive-area');
    const loader = document.getElementById('loader');
    const status = document.getElementById('status');

    area.addEventListener('click', () => {{
        // Get current play state
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        // Toggle play state
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            status.textContent = 'Paused';
            status.style.color = 'var(--text)';
        }} else {{
            loader.style.animationPlayState = 'running';
            status.textContent = 'Running';
            status.style.color = 'var(--accent)';
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
