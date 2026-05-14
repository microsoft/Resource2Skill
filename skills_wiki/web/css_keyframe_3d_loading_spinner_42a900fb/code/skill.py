def create_component(
    output_dir: str,
    title_text: str = "Loading Animation",
    body_text: str = "", # Not used for this specific loading animation, but kept for consistency
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00FFFF",  # CSS hex color for accent (aqua)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Keyframe 3D Loading Spinner visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716"  # Dark blue/black from tutorial
        text_color = "#f0f0f0" # Fallback, not used in this specific component
        surface_color = "rgba(255, 255, 255, 0.06)" # Fallback
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* CSS Keyframe 3D Loading Spinner — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text); /* Not explicitly used by the spinner, but good practice */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Hide potential overflow from animation */
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--accent), inset 0 0 8px var(--accent);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    animation: loading 2s ease-in-out infinite; /* Shorthand used as per tutorial */
}}

@keyframes loading {{
    0% {{
        transform: translate(-50%, -50%) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: translate(-50%, -50%) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading"></div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For this looping loading animation, no specific JS is needed to control the animation state.
    # The interactivity demo (play/pause buttons) from the tutorial is a separate concept
    # not part of the final loading animation exercise.
    js = f"""// CSS Keyframe 3D Loading Spinner — no specific JavaScript required for this looping animation.
// Interactive play/pause could be implemented here by toggling animation-play-state
// based on user events (e.g., button clicks or hover).
document.addEventListener('DOMContentLoaded', () => {{
    console.log('Loading animation is active.');
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

