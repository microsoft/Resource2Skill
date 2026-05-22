def create_component(
    output_dir: str,
    title_text: str = "System Processing",
    body_text: str = "Please wait while we initialize the 3D environment.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon 3D CSS Loader visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape text inputs to prevent HTML injection
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716"  # Deep dark blue from the tutorial
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Neon 3D CSS Loader — generated component */
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
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    background: var(--surface);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    padding: 40px;
    text-align: center;
    /* Adding perspective to the container gives the 3D rotation more depth, 
       though it works orthographically without it as well */
    perspective: 800px; 
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1rem;
    opacity: 0.7;
    max-width: 400px;
    line-height: 1.5;
}}

/* === Core Skill: 3D Loader === */
.loader-wrapper {{
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    /* Shorthand: name | duration | timing-function | iteration-count */
    animation: loadingAnim 2s ease-in-out infinite;
    /* Play state can be manipulated via JS or CSS hover */
    animation-play-state: running; 
}}

/* Pause animation natively on hover as a fallback/alternative */
.loading:hover {{
    animation-play-state: paused;
    cursor: pointer;
}}

/* The sequential 3D rotation sequence */
@keyframes loadingAnim {{
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

/* Controls UI */
.controls {{
    display: flex;
    gap: 16px;
}}

button {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--text);
    padding: 10px 24px;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}}

button:hover {{
    background: var(--text);
    color: var(--bg);
}}

button.active {{
    border-color: var(--accent);
    color: var(--accent);
}}

button.active:hover {{
    background: var(--accent);
    color: var(--bg);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>
        
        <div class="loader-wrapper">
            <div class="loading" id="loader"></div>
        </div>

        <div class="controls">
            <button id="playBtn" class="active">Play</button>
            <button id="pauseBtn">Pause</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive control of CSS animation-play-state
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');

    playBtn.addEventListener('click', () => {{
        // Set CSS property programmatically
        loader.style.animationPlayState = 'running';
        
        // Update UI
        playBtn.classList.add('active');
        pauseBtn.classList.remove('active');
    }});

    pauseBtn.addEventListener('click', () => {{
        // Pause the CSS animation in its current state
        loader.style.animationPlayState = 'paused';
        
        // Update UI
        pauseBtn.classList.add('active');
        playBtn.classList.remove('active');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
