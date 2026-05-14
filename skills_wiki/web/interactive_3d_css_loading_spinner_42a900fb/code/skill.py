def create_component(
    output_dir: str,
    title_text: str = "Loading Data...",
    body_text: str = "Please wait while we process your request.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for the neon spinner
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D CSS Loading Spinner.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep dark navy from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Interactive 3D CSS Loading Spinner */
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

.wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 40px;
    background: var(--bg);
}}

/* Header / Text area */
.header {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* The Core Animated Spinner */
.loading-container {{
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading-spinner {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    z-index: 10;
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
    animation: loading-flip 2s ease-in-out infinite;
    
    /* Smooth transition for when play-state is changed via JS/Hover */
    transition: filter 0.3s ease;
}}

/* Pause animation on hover */
.loading-spinner:hover {{
    animation-play-state: paused !important; /* Forces pause overrides */
    filter: brightness(1.5);
    cursor: pointer;
}}

/* 3D Flip Keyframes */
@keyframes loading-flip {{
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

/* Interactive Controls */
.controls {{
    display: flex;
    gap: 16px;
    z-index: 10;
    background: var(--surface);
    padding: 12px 24px;
    border-radius: 50px;
    backdrop-filter: blur(10px);
}}

button {{
    background: transparent;
    color: var(--text);
    border: 2px solid transparent;
    padding: 8px 16px;
    border-radius: 20px;
    font-family: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button.active {{
    background: var(--accent);
    color: {bg_color};
    box-shadow: 0 0 10px var(--accent);
}}

button:hover:not(.active) {{
    border-color: var(--surface);
    background: var(--surface);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading-spinner {{
        animation-duration: 4s;
        animation-timing-function: linear;
        /* Replace complex 3D flips with a simple, slow opacity pulse */
        animation-name: simple-pulse;
    }}
    
    @keyframes simple-pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
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
    <div class="wrapper">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="loading-container" aria-label="Loading indicator" role="status">
            <!-- The animated element -->
            <div class="loading-spinner" id="spinner"></div>
        </div>

        <!-- UI Controls to demonstrate animation-play-state -->
        <div class="controls">
            <button id="btn-play" class="active">Play</button>
            <button id="btn-pause">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive 3D CSS Loading Spinner Logic
document.addEventListener('DOMContentLoaded', () => {{
    const spinner = document.getElementById('spinner');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');

    // Handle Play Button Click
    btnPlay.addEventListener('click', () => {{
        // Change the CSS animation-play-state property
        spinner.style.animationPlayState = 'running';
        
        // Update UI state
        btnPlay.classList.add('active');
        btnPause.classList.remove('active');
    }});

    // Handle Pause Button Click
    btnPause.addEventListener('click', () => {{
        // Change the CSS animation-play-state property
        spinner.style.animationPlayState = 'paused';
        
        // Update UI state
        btnPause.classList.add('active');
        btnPlay.classList.remove('active');
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
