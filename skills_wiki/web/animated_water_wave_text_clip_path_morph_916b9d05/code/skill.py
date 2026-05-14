def create_component(
    output_dir: str,
    title_text: str = "Water",
    body_text: str = "",  # Not primarily used in this specific typographic effect
    color_scheme: str = "dark",
    accent_color: str = "#03a9f4",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Water Wave Text effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#000000"
    else:
        bg_color = "#ffffff"

    # === CSS ===
    css = f"""/* Animated Water Wave Text */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background: var(--bg);
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
    align-items: center;
    justify-content: center;
}}

/* The relative wrapper ensures absolute children originate from the center */
.content {{
    position: relative;
}}

.content h2 {{
    position: absolute;
    transform: translate(-50%, -50%);
    font-size: clamp(4rem, 12vw, 12rem);
    font-weight: 700;
    white-space: nowrap;
}}

/* Back layer: Hollow Outline */
.content h2:nth-child(1) {{
    color: transparent;
    -webkit-text-stroke: 3px var(--accent);
}}

/* Front layer: Solid fill with animated clip-path */
.content h2:nth-child(2) {{
    color: var(--accent);
    animation: animateWave 4s ease-in-out infinite;
}}

/* Morphing the polygon coordinates to simulate a moving wave */
@keyframes animateWave {{
    0%, 100% {{
        clip-path: polygon(
            0% 45%, 
            15% 44%, 
            32% 50%, 
            54% 60%, 
            70% 61%, 
            84% 59%, 
            100% 52%, 
            100% 100%, 
            0% 100%
        );
    }}
    50% {{
        clip-path: polygon(
            0% 60%, 
            15% 65%, 
            34% 66%, 
            51% 62%, 
            67% 50%, 
            84% 45%, 
            100% 46%, 
            100% 100%, 
            0% 100%
        );
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Water Wave Text</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="content">
            <!-- Back layer (Outline) -->
            <h2>{title_text}</h2>
            <!-- Front layer (Animated Wave) - aria-hidden prevents duplicate screen reader announcements -->
            <h2 aria-hidden="true">{title_text}</h2>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required for the core visual wave effect.
// Animation is handled entirely via CSS @keyframes and clip-path.
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
