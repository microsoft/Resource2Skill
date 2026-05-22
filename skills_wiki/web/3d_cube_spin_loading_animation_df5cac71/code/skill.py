def create_component(
    output_dir: str,
    title_text: str = "Loading Page",
    body_text: str = "Loading content...",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00bfff",  # CSS hex color for accent (cyan-like)
    width_px: int = 1200, # Overall viewport width for demo purposes
    height_px: int = 800, # Overall viewport height for demo purposes
    box_size_px: int = 50,
    border_width_px: int = 5,
    border_radius_px: int = 3,
    animation_duration_s: int = 2,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Cube Spin Loading Animation visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* 3D Cube Spin Loading Animation — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --box-size: {box_size_px}px;
    --border-width: {border_width_px}px;
    --border-radius: {border_radius_px}px;
    --animation-duration: {animation_duration_s}s;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Prevent scrollbars if content overflows viewport bounds */
    width: 100vw; /* Ensure body takes full viewport width */
    height: 100vh; /* Ensure body takes full viewport height */
}}

.loading-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px; /* Space between the box and the text */
}}

.loading-text {{
    font-size: 1.2rem;
    font-weight: 500;
    white-space: nowrap; /* Prevent text from wrapping */
}}

.loading-box {{
    height: var(--box-size);
    width: var(--box-size);
    border: var(--border-width) solid var(--accent);
    border-radius: var(--border-radius);
    /* Creates a glow effect around the box and subtly inside */
    box-shadow: 0 0 8px var(--accent), 0 0 8px var(--accent) inset;
    
    /* Apply the keyframe animation */
    animation: loading var(--animation-duration) ease-in infinite;
}}

/* Define the keyframe animation for the 3D spin */
@keyframes loading {{
    0% {{
        transform: perspective(100px) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: perspective(100px) rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: perspective(100px) rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: perspective(100px) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading-container">
        <div class="loading-box"></div>
        <p class="loading-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (Empty for this CSS-only animation) ===
    js = """// 3D Cube Spin Loading Animation — interactive behavior
// This specific animation is purely CSS-driven, so no JavaScript is required for the core visual effect.
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

