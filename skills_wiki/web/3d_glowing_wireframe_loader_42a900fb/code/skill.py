def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Fetching application data...",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Wireframe Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape HTML inputs to prevent XSS
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Specific deep dark blue from the tutorial
        text_color = "#f0f0f0"
        text_muted = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        text_muted = "rgba(0, 0, 0, 0.6)"

    # === CSS ===
    css = f"""/* 3D Glowing Wireframe Loader */
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
    --loader-size: 60px;
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
    max-width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

.text-wrapper {{
    position: absolute;
    bottom: 20%;
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}}

p {{
    font-size: 0.95rem;
    color: var(--text-muted);
}}

/* Interactive UI hint */
.hint {{
    position: absolute;
    top: 20%;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
    opacity: 0.7;
    transition: opacity 0.3s ease;
}}

/* --- Core Loader Effect --- */
.loading {{
    height: var(--loader-size);
    width: var(--loader-size);
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Outset and Inset glowing shadows */
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    position: absolute;
    top: 50%;
    left: 50%;
    
    /* Center aligning using modern translate */
    translate: -50% -50%;
    
    /* Apply the animation */
    animation: loadingAnim 2s ease-in-out infinite;
    
    cursor: pointer;
    z-index: 10;
}}

/* Hover interaction */
.loading:hover {{
    animation-play-state: paused;
}}

.loading:hover ~ .hint {{
    opacity: 1;
}}

/* The 3D sequence keyframes */
@keyframes loadingAnim {{
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

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loading {{
        animation: none;
        /* Add a pulsing opacity instead of spinning */
        animation: pulse 2s ease-in-out infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 0.5; }}
        100% {{ opacity: 1; box-shadow: 0 0 24px var(--accent), 0 0 24px var(--accent) inset; }}
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- The Loader Component -->
        <div class="loading" role="progressbar" aria-label="Loading animation" tabindex="0"></div>
        
        <div class="hint">Hover to Pause</div>
        
        <div class="text-wrapper">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Wireframe Loader
// The core animation is driven entirely by CSS.
// JS is included here to handle potential keyboard accessibility (pausing on focus).

document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loading');
    
    if (loader) {{
        // Allow keyboard users to pause the animation just like hover users
        loader.addEventListener('focus', () => {{
            loader.style.animationPlayState = 'paused';
        }});
        
        loader.addEventListener('blur', () => {{
            loader.style.animationPlayState = 'running';
        }});
    }}
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
