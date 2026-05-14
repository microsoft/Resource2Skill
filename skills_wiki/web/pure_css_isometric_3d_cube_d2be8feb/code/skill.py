def create_component(
    output_dir: str,
    title_text: str = "CSS Isometric Cube",
    body_text: str = "Pure CSS 3D projection using preserve-3d and dynamic shading.",
    color_scheme: str = "light",        
    accent_color: str = "#ff2a85",     # Vibrant pink matching the tutorial
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Isometric Cube visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f9fafb"
    else:
        bg_color = "#ffffff"
        text_color = "#1f2937"

    # CSS
    css = f"""/* Pure CSS Isometric Cube generated styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --cube-size: 160px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    gap: 4rem;
}}

.header {{
    text-align: center;
    z-index: 10;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

p {{
    color: {text_color};
    opacity: 0.7;
    font-size: 1.1rem;
}}

/* --- Isometric Cube Scene --- */
.scene {{
    width: var(--cube-size);
    height: var(--cube-size);
    /* Perspective isn't strictly necessary for true isometric (which lacks perspective), 
       but a very high value keeps the 3D engine engaged while appearing orthographic */
    perspective: 4000px; 
    position: relative;
}}

.cube {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    /* Standard isometric projection angles */
    transform: rotateX(-35.264deg) rotateY(45deg);
    transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}}

/* Value Addition: Interactive Hover State */
.scene:hover .cube {{
    transform: rotateX(-35.264deg) rotateY(45deg) translateY(-15px) scale(1.05);
}}

.face {{
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--accent);
    /* Smooth edges slightly */
    outline: 1px solid transparent; 
}}

/* Dynamic Shading System using overlays */
.face::after {{
    content: '';
    position: absolute;
    inset: 0;
}}

/* Position faces to form a cube */
.top {{
    transform: rotateX(90deg) translateZ(calc(var(--cube-size) / 2));
}}
.top::after {{
    /* Lightest face */
    background-color: rgba(255, 255, 255, 0.15);
}}

.left {{
    transform: rotateY(-90deg) translateZ(calc(var(--cube-size) / 2));
}}
.left::after {{
    /* Darkest face (shadow) */
    background-color: rgba(0, 0, 0, 0.25);
}}

.right {{
    transform: translateZ(calc(var(--cube-size) / 2));
}}
.right::after {{
    /* Mid-tone face */
    background-color: rgba(0, 0, 0, 0.08);
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- 3D Component -->
    <div class="scene">
        <div class="cube">
            <div class="face top"></div>
            <div class="face left"></div>
            <div class="face right"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # JS (Empty but included for strict structural compliance, interaction is pure CSS)
    js = f"""// Component logic
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Isometric Cube initialized.");
    // 3D rotation and shading are handled entirely via CSS preserve-3d
}});
"""

    # Write files
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
