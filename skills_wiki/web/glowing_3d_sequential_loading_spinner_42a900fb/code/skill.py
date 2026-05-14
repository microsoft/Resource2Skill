def create_component(
    output_dir: str,
    title_text: str = "Loading Component",
    body_text: str = "Please wait while we prepare your data...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan / Aqua
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glowing 3D Sequential Loading Spinner.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Deep navy from the tutorial
        text_color = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Glowing 3D Sequential Loading Spinner — generated component */
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
    max-width: 100%;
    height: var(--height);
    background: var(--surface);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
    text-align: center;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    /* Adding perspective to the parent enhances the 3D effect, 
       though the original tutorial omitted it for an orthographic look. */
    perspective: 800px; 
}}

.text-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    opacity: 0.7;
    font-weight: 400;
}}

/* === Core Animation Visuals === */
.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    
    /* Dual shadow for internal and external glow */
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    /* Shorthand: duration | name | timing-function | iteration-count */
    animation: 2s loading-sequence ease-in-out infinite;
    
    /* Ensure hardware acceleration for smooth 3D transforms */
    will-change: transform;
}}

/* === Core Keyframes Logic === */
@keyframes loading-sequence {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        /* Flip forward vertically */
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        /* Add horizontal flip */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        /* Add rotational spin to return visually to the starting shape */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
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
    <div class="container">
        
        <!-- The core loading element -->
        <div class="loading" role="status" aria-label="Loading"></div>
        
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glowing 3D Sequential Loading Spinner — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // The core effect relies entirely on CSS keyframes.
    // However, we can use JS to interact with the animation-play-state 
    // as demonstrated conceptually in the tutorial.
    
    const loader = document.querySelector('.loading');
    const container = document.querySelector('.container');
    
    // Pause animation when hovering over the container (optional interaction feature)
    container.addEventListener('mouseenter', () => {{
        loader.style.animationPlayState = 'paused';
    }});
    
    container.addEventListener('mouseleave', () => {{
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
