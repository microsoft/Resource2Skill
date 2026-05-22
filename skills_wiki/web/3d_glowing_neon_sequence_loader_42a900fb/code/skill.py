def create_component(
    output_dir: str,
    title_text: str = "Authenticating Data...",
    body_text: str = "Please wait while we establish a secure connection.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Sequence Loader.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        btn_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111827"
        surface_color = "#ffffff"
        btn_bg = "rgba(0, 0, 0, 0.05)"
        # Darken the accent slightly for light mode contrast if needed
        if accent_color in ["#00ffff", "aqua"]:
            accent_color = "#00a3cc"

    # === CSS ===
    css = f"""/* 3D Glowing Sequence Loader */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --btn-bg: {btn_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--surface);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 40px;
    text-align: center;
}}

/* Core Loader Styles */
.loader-wrapper {{
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
    box-shadow: 0 0 10px var(--accent), 0 0 10px var(--accent) inset;
    animation: loading-sequence 2.4s ease-in-out infinite;
    cursor: pointer;
    will-change: transform;
}}

.loading-cube:hover {{
    /* Optional: Provide a slight visual cue on hover before clicking */
    filter: brightness(1.2);
}}

/* The Sequential 3D Animation */
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

/* Typography & UI Controls */
.content-wrapper h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}}

.content-wrapper p {{
    font-size: 0.95rem;
    opacity: 0.7;
    margin-bottom: 24px;
    max-width: 300px;
    line-height: 1.5;
}}

.controls {{
    display: flex;
    gap: 12px;
    justify-content: center;
}}

button {{
    background: var(--btn-bg);
    color: var(--text-color);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}

button:hover {{
    background: var(--accent);
    color: {bg_color}; /* Ensure text is visible against bright accent */
    border-color: var(--accent);
}}

button.active {{
    background: var(--accent);
    color: {bg_color};
    box-shadow: 0 0 8px var(--accent);
}}

@media (prefers-reduced-motion: reduce) {{
    .loading-cube {{
        animation-duration: 10s; /* Drastically slow down for accessibility */
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
    <div class="container">
        
        <div class="loader-wrapper">
            <div class="loading-cube" role="progressbar" aria-label="Loading progress"></div>
        </div>

        <div class="content-wrapper">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            
            <div class="controls">
                <button id="btn-play" class="active">Play</button>
                <button id="btn-pause">Pause</button>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Manage CSS animation play-state via DOM
document.addEventListener('DOMContentLoaded', () => {{
    const cube = document.querySelector('.loading-cube');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');

    // Function to update states
    const setPlayState = (state) => {{
        // Update CSS property
        cube.style.animationPlayState = state;
        
        // Update UI Button states
        if (state === 'running') {{
            btnPlay.classList.add('active');
            btnPause.classList.remove('active');
        }} else {{
            btnPause.classList.add('active');
            btnPlay.classList.remove('active');
        }}
    }};

    // Event Listeners for UI buttons
    btnPlay.addEventListener('click', () => setPlayState('running'));
    btnPause.addEventListener('click', () => setPlayState('paused'));

    // Allow clicking the cube itself to toggle
    cube.addEventListener('click', () => {{
        const currentState = window.getComputedStyle(cube).animationPlayState;
        setPlayState(currentState === 'running' ? 'paused' : 'running');
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
