def create_component(
    output_dir: str,
    title_text: str = "System Initializing",
    body_text: str = "Fetching necessary assets and preparing your environment...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon 3D Tumbling Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#05070a"
        surface_color = "#0d111c"
        text_color = "#f0f0f0"
        text_muted = "#8a94a6"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#e9ecef"
        surface_color = "#f8f9fa"
        text_color = "#1a1a2e"
        text_muted = "#6c757d"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Neon 3D Tumbling Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Loader specific */
    --loader-size: 60px;
    --loader-thickness: 6px;
    --glow-spread: 12px;
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
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    position: relative;
    overflow: hidden;
}}

/* -- The Core Loading Animation -- */
.loader-wrapper {{
    /* Perspective enhances the 3D depth, making the closer edge appear larger */
    perspective: 800px;
    width: var(--loader-size);
    height: var(--loader-size);
    margin-bottom: 3rem;
}}

.loader-box {{
    width: 100%;
    height: 100%;
    border: var(--loader-thickness) solid var(--accent);
    border-radius: 8px;
    /* Inset and outset shadows create the neon tube effect */
    box-shadow: 0 0 var(--glow-spread) var(--accent), 
                inset 0 0 var(--glow-spread) var(--accent);
    
    /* Apply the animation: name, duration, easing, iteration */
    animation: loadingTumble 2.4s ease-in-out infinite;
    
    /* Ensure child elements (if any) or box itself render crisply in 3D */
    transform-style: preserve-3d;
}}

/* 
  The sequence rotates one axis at a time.
  By retaining the previous rotations, the box continuously tumbles 
  rather than resetting to a flat state ungracefully.
*/
@keyframes loadingTumble {{
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

/* -- Content Typography -- */
.content {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 2.5rem;
    max-width: 80%;
}}

.title {{
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* -- Interactive Controls -- */
.controls {{
    display: flex;
    gap: 1rem;
}}

.toggle-btn {{
    background: transparent;
    border: 2px solid var(--border);
    color: var(--text);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-family: inherit;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.toggle-btn:hover {{
    border-color: var(--text);
    background: rgba(255, 255, 255, 0.05);
}}

.toggle-btn:active {{
    transform: scale(0.97);
}}

.toggle-btn.is-paused {{
    border-color: var(--accent);
    color: var(--accent);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- 3D Loader -->
        <div class="loader-wrapper" aria-hidden="true">
            <div class="loader-box" id="loader"></div>
        </div>
        
        <!-- Text Content -->
        <div class="content">
            <h1 class="title" aria-live="polite">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- JavaScript Interaction Demo -->
        <div class="controls">
            <button class="toggle-btn" id="toggleBtn" aria-label="Pause or play animation">
                <svg id="icon-pause" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                <svg id="icon-play" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="display: none;"><path d="M8 5v14l11-7z"/></svg>
                <span id="btnText">Pause Animation</span>
            </button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon 3D Tumbling Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const toggleBtn = document.getElementById('toggleBtn');
    const btnText = document.getElementById('btnText');
    const iconPause = document.getElementById('icon-pause');
    const iconPlay = document.getElementById('icon-play');

    // Toggle animation play state on click
    toggleBtn.addEventListener('click', () => {{
        // Check current computed play state
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        if (currentState === 'running') {{
            // Pause the animation mid-frame
            loader.style.animationPlayState = 'paused';
            
            // Update UI
            btnText.textContent = 'Play Animation';
            iconPause.style.display = 'none';
            iconPlay.style.display = 'block';
            toggleBtn.classList.add('is-paused');
        }} else {{
            // Resume the animation
            loader.style.animationPlayState = 'running';
            
            // Update UI
            btnText.textContent = 'Pause Animation';
            iconPause.style.display = 'block';
            iconPlay.style.display = 'none';
            toggleBtn.classList.remove('is-paused');
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
