def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Retrieving necessary assets...",
    color_scheme: str = "dark",        
    accent_color: str = "#00FFFF",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sequential 3D Glowing Loader.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Based on the video's dark blue aesthetic
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Sequential 3D Glowing Loader */
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
    max-width: 100%;
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    text-align: center;
}}

.text-content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}}

.text-content p {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* -- Core Loader Visuals & Animations -- */
.loading-wrapper {{
    /* Perspective can optionally be added here, but the tutorial relies on native orthographic 3D flip */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}}

.loading-element {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Core visual signature: standard + inset shadow for neon glow */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Core animation setup */
    animation: loading 2s ease-in-out infinite;
    /* Optional smooth transition if JS changes the play state */
    transition: box-shadow 0.3s ease; 
}}

/* Sequence matches the video transcript perfectly */
@keyframes loading {{
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

/* -- Interactive Controls -- */
.controls {{
    display: flex;
    gap: 1rem;
    background: var(--surface);
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}}

button {{
    background: transparent;
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 0.5rem 1.25rem;
    border-radius: 25px;
    font-family: inherit;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button.active {{
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
}}

button:hover:not(.active) {{
    background: rgba(255, 255, 255, 0.1);
}}

/* Hover interaction fallback (as shown in tutorial) */
.loading-element:hover {{
    animation-play-state: paused;
    cursor: pointer;
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
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="loading-wrapper">
            <!-- The Loader Element -->
            <div class="loading-element" id="loader"></div>
        </div>

        <!-- Animation Play State Controls -->
        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animation Play State Controller
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    playBtn.addEventListener('click', () => {{
        // Set CSS animation-play-state to running
        loader.style.animationPlayState = 'running';
        
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        // Set CSS animation-play-state to paused
        loader.style.animationPlayState = 'paused';
        
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
    }});
    
    // Sync buttons if user hovers to pause (demonstrated in video)
    loader.addEventListener('mouseenter', () => {{
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
    }});
    
    loader.addEventListener('mouseleave', () => {{
        if(loader.style.animationPlayState !== 'paused') {{
            playBtn.classList.add('active');
            pauseBtn.classList.remove('active');
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
