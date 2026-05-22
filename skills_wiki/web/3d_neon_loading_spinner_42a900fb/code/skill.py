def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Initializing sequence...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan/Aqua neon glow
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Loading Spinner.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#080b12"
        text_color = "#e2e8f0"
        surface_color = "#111827"
        btn_bg = "#1f2937"
        btn_hover = "#374151"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        btn_bg = "#e2e8f0"
        btn_hover = "#cbd5e1"

    # === CSS ===
    css = f"""/* 3D Neon Loading Spinner — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --accent: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
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
    background-color: var(--surface);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    padding: 40px;
    position: relative;
    overflow: hidden;
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* === Core Animation Component === */
.loader-wrapper {{
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Adding perspective makes the 3D transforms look slightly more realistic, 
       though the video relied on orthographic flat 3D projection. */
    perspective: 800px; 
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Combined outset and inset shadows create the neon tube look */
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s spinner ease-in-out infinite;
    
    /* Ensure the play state is running by default */
    animation-play-state: running;
}}

/* The precise sequential rotation logic from the tutorial */
@keyframes spinner {{
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

/* === Controls === */
.controls {{
    display: flex;
    gap: 16px;
    background: rgba(0, 0, 0, 0.1);
    padding: 12px 24px;
    border-radius: 50px;
}}

button {{
    background-color: var(--btn-bg);
    color: var(--text);
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}}

button:hover {{
    background-color: var(--btn-hover);
    transform: translateY(-2px);
}}

button:active {{
    transform: translateY(0);
}}

/* Focus styles for accessibility */
button:focus-visible {{
    outline: 2px solid var(--accent);
    outline-offset: 2px;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <!-- Using FontAwesome for control icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="loader-wrapper">
            <!-- The core visual component -->
            <div class="loading" id="spinner"></div>
        </div>

        <div class="controls">
            <button id="playBtn" aria-label="Play Animation">
                <i class="fa-solid fa-play"></i> Play
            </button>
            <button id="pauseBtn" aria-label="Pause Animation">
                <i class="fa-solid fa-pause"></i> Pause
            </button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Loading Spinner — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const spinner = document.getElementById('spinner');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    // Manipulate the CSS animation-play-state property
    playBtn.addEventListener('click', () => {{
        spinner.style.animationPlayState = 'running';
        
        // Minor visual feedback on buttons
        playBtn.style.opacity = '1';
        pauseBtn.style.opacity = '0.5';
    }});

    pauseBtn.addEventListener('click', () => {{
        spinner.style.animationPlayState = 'paused';
        
        // Minor visual feedback on buttons
        pauseBtn.style.opacity = '1';
        playBtn.style.opacity = '0.5';
    }});

    // Set initial button visual state
    pauseBtn.style.opacity = '0.5';
}});
"""

    # Write files
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
