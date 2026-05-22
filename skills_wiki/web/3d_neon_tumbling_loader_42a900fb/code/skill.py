def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Initializing system assets. Please wait...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Tumbling Loader visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716" # Very deep, dark blue
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Neon Tumbling Loader */
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
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    position: relative;
}}

/* Text Content */
.text-wrapper {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* Loader Core Styles */
.loader-wrapper {{
    height: 100px; /* fixed height container to prevent layout shifting during rotation */
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px; /* Optional: adds subtle 3D depth to the transform */
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Dual box shadow for neon glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* Animation Configuration */
    animation-name: tumbling;
    animation-duration: 2.5s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    
    /* Ensure play-state transitions are smooth */
    transition: transform 0.2s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

/* Dim glow slightly on hover when paused */
.loader:hover {{
    box-shadow: 0 0 6px var(--accent), inset 0 0 6px var(--accent);
    opacity: 0.8;
}}

/* Core 3D Keyframes Extraction */
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

/* Controls */
.controls {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

button {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1.5rem;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
}}

button:hover {{
    background: var(--text);
    color: var(--bg);
}}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation: none;
        border-style: dashed;
        border-width: 4px;
        box-shadow: none;
        transform: rotate(45deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container" role="status" aria-live="polite">
        
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="loader-wrapper">
            <!-- The tumbling shape -->
            <div class="loader" id="loaderElement" title="Hover to pause"></div>
        </div>

        <div class="controls">
            <button id="playBtn">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Tumbling Loader - Interactive Logic
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loaderElement');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Button controls using animationPlayState
    playBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'running';
    }});

    pauseBtn.addEventListener('click', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    // Hover interaction as demonstrated in the tutorial
    loader.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});

    loader.addEventListener('mouseleave', () => {{
        loader.style.animationPlayState = 'running';
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
