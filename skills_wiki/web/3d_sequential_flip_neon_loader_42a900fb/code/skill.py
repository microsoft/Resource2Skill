def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Please wait while we initialize the interface...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Sequential Flip Neon Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#f0f0f0"
        subtext_color = "#8b94b0"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a1a2e"
        subtext_color = "#5a6480"
        
        # Ensure light mode has a darker default accent if neon cyan is passed
        if accent_color == "#00ffff":
            accent_color = "#0066ff"

    # === CSS ===
    css = f"""/* 3D Sequential Flip Neon Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
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
    gap: 3rem;
    position: relative;
}}

/* Loader Wrapper for isolation and click target */
.loader-wrapper {{
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    /* Optional: add 'perspective: 400px;' here for a more exaggerated 3D depth effect */
}}

/* Core Loading Square */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 
        0 0 8px var(--accent), 
        0 0 8px var(--accent) inset;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loadingSequence ease-in-out infinite;
}}

/* Text Content */
.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--subtext);
}}

/* The Sequential Flip Keyframes */
@keyframes loadingSequence {{
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

/* Accessibility: Reduced Motion Fallback */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation: 3s pulse ease-in-out infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 0.3; transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1.1); }}
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
    <main class="container">
        
        <!-- Loading Indicator -->
        <div class="loader-wrapper" aria-label="Loading indicator. Hover to pause animation." role="progressbar" aria-busy="true">
            <div class="loading"></div>
        </div>
        
        <!-- Typography -->
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Sequential Flip Neon Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loaderWrapper = document.querySelector('.loader-wrapper');
    const loadingElement = document.querySelector('.loading');

    // Demonstrate animation-play-state property via JavaScript
    // Pauses the 3D flip mid-animation when the user hovers over the loader area
    loaderWrapper.addEventListener('mouseenter', () => {{
        loadingElement.style.animationPlayState = 'paused';
    }});

    loaderWrapper.addEventListener('mouseleave', () => {{
        loadingElement.style.animationPlayState = 'running';
    }});
    
    // Toggle pause/play on click for touch devices
    let isPaused = false;
    loaderWrapper.addEventListener('click', () => {{
        isPaused = !isPaused;
        loadingElement.style.animationPlayState = isPaused ? 'paused' : 'running';
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
