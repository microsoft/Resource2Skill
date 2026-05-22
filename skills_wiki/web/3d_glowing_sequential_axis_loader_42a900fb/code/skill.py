def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Click anywhere to pause or resume the 3D animation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua/cyan)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Sequential Axis Loader.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Dark blue-black from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Glowing Sequential Axis Loader — generated component */
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
    
    /* Loader specific variables */
    --loader-size: 60px;
    --loader-border: 6px;
    --loader-glow: 12px;
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
    max-height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    cursor: pointer;
    overflow: hidden;
}}

/* Text Content Overlay */
.content {{
    position: absolute;
    bottom: 10%;
    text-align: center;
    z-index: 20;
    pointer-events: none;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* The Core Loader Component */
.loader-wrapper {{
    position: absolute;
    top: 50%;
    left: 50%;
    /* Use independent translate to avoid overriding the transform in animations */
    translate: -50% -50%;
    z-index: 10;
}}

.loader {{
    height: var(--loader-size);
    width: var(--loader-size);
    border: var(--loader-border) solid var(--accent);
    border-radius: 4px;
    /* Paired box-shadow for inner and outer glow */
    box-shadow: 
        0 0 var(--loader-glow) var(--accent), 
        inset 0 0 var(--loader-glow) var(--accent);
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
    animation: 2.4s rotateCube ease-in-out infinite;
}}

/* 
  Sequential 3D Rotation Animation
  Divides the timeline into 3 distinct movement phases.
*/
@keyframes rotateCube {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        /* Phase 1: Flip on X axis */
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        /* Phase 2: Hold X, flip on Y axis */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        /* Phase 3: Hold X and Y, spin on Z axis */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* Accessibility: Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation-duration: 8s;
        animation-timing-function: linear;
    }}
}}
"""

    # === HTML ===
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
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
    <div class="container" id="interactive-zone" aria-label="Interactive loader container" role="button" tabindex="0">
        
        <div class="loader-wrapper">
            <div class="loader" id="animated-loader" aria-hidden="true"></div>
        </div>

        <div class="content">
            <h1 class="title">{safe_title}</h1>
            <p class="body-text" id="status-text">{safe_body}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Sequential Axis Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('interactive-zone');
    const loader = document.getElementById('animated-loader');
    const statusText = document.getElementById('status-text');
    
    // Initial text configuration
    const defaultText = "{html_lib.escape(body_text)}";
    const pausedText = "Animation Paused. Click to resume.";

    // Function to toggle animation state
    const togglePlayState = () => {{
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            statusText.textContent = pausedText;
        }} else {{
            loader.style.animationPlayState = 'running';
            statusText.textContent = defaultText;
        }}
    }};

    // Mouse interaction
    container.addEventListener('click', togglePlayState);

    // Keyboard interaction for accessibility
    container.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            togglePlayState();
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
