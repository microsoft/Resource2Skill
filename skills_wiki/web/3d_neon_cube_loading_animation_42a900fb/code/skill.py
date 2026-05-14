def create_component(
    output_dir: str,
    title_text: str = "System Loading",
    body_text: str = "Fetching resources, please wait...",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Cube Loading Animation.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716" # Deep space blue from the tutorial
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Neon Cube Loading Animation */
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
    background: #000; /* Outer page background */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    border-radius: 16px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    perspective: 1000px; /* Gives a slight 3D depth to the container */
}}

.loader-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}}

/* The Core Loader Component */
.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outer glow and inner glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    /* Transform style ensures 3D rendering context */
    transform-style: preserve-3d;
    /* The animation definition */
    animation: loading 2s ease-in-out infinite;
    cursor: pointer;
    will-change: transform;
}}

/* Interactive Pause State */
.loader.paused {{
    animation-play-state: paused;
}}

/* Text styling */
.typography {{
    text-align: center;
}}

h1 {{
    font-size: 1.75rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

p {{
    font-size: 0.95rem;
    color: var(--text);
    opacity: 0.7;
}}

.instruction {{
    margin-top: 30px;
    font-size: 0.8rem;
    opacity: 0.5;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* The tumbling keyframe sequence */
@keyframes loading {{
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

/* Accessibility: Reduced motion preference */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation-duration: 4s; /* Slow down significantly */
        /* Alternatively, replace with a simple opacity pulse */
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
    <div class="container">
        <div class="loader-wrapper">
            <!-- Loader component with ARIA attributes for screen readers -->
            <div class="loader" role="status" aria-label="Loading..." title="Click to pause/play"></div>
            
            <div class="typography">
                <h1>{safe_title}</h1>
                <p>{safe_body}</p>
                <div class="instruction">Click cube to toggle animation</div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive toggle for CSS animation-play-state
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loader');
    
    if (loader) {{
        loader.addEventListener('click', () => {{
            // Toggles the 'paused' class which sets animation-play-state: paused in CSS
            loader.classList.toggle('paused');
        }});
    }}
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
