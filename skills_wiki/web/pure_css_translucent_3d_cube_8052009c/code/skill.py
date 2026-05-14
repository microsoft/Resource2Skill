def create_component(
    output_dir: str,
    title_text: str = "On Writing Code",
    body_text: str = "Understanding perspective and 3D transforms.",
    color_scheme: str = "dark",
    accent_color: str = "#4ade80",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Translucent 3D Cube.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f8f9fa"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # CSS
    css = f"""/* CSS 3D Cube Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --cube-size: 240px; /* Size of the 3D Cube */
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Space Mono', 'Inter', monospace, sans-serif;
    background-color: var(--bg);
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.header {{
    position: absolute;
    top: 10%;
    left: 10%;
    z-index: 10;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}}

.header p {{
    font-size: 1rem;
    opacity: 0.7;
    font-family: 'Inter', sans-serif;
}}

/* 3D Scene setup */
.scene {{
    width: var(--cube-size);
    height: var(--cube-size);
    perspective: 1000px; /* The 'Camera' distance */
    margin: auto;
}}

/* The Cube container */
.cube {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transform: translateZ(calc(var(--cube-size) * -0.5));
    animation: spin 20s infinite linear;
    transition: transform 0.2s ease-out;
}}

/* Pause animation when user hovers */
.scene:hover .cube {{
    animation-play-state: paused;
}}

/* Core Face Styles */
.face {{
    position: absolute;
    width: var(--cube-size);
    height: var(--cube-size);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--accent);
    /* Soft glowing box-shadow for depth */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.4) inset;
}}

/* Pseudo-element for translucent background to keep borders solid */
.face::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-color: var(--accent);
    opacity: 0.15;
    z-index: -1;
}}

/* Positioning the 6 faces in 3D Space */
.front  {{ transform: rotateY(  0deg) translateZ(calc(var(--cube-size) / 2)); }}
.right  {{ transform: rotateY( 90deg) translateZ(calc(var(--cube-size) / 2)); }}
.back   {{ transform: rotateY(180deg) translateZ(calc(var(--cube-size) / 2)); }}
.left   {{ transform: rotateY(-90deg) translateZ(calc(var(--cube-size) / 2)); }}
.top    {{ transform: rotateX( 90deg) translateZ(calc(var(--cube-size) / 2)); }}
.bottom {{ transform: rotateX(-90deg) translateZ(calc(var(--cube-size) / 2)); }}

/* Distinct opacity/color variations for aesthetics */
.front::before  {{ opacity: 0.25; }}
.right::before  {{ opacity: 0.15; }}
.back::before   {{ opacity: 0.10; }}
.left::before   {{ opacity: 0.20; }}
.top::before    {{ opacity: 0.30; }}
.bottom::before {{ opacity: 0.05; }}

/* Keyframes for continuous multidirectional rotation */
@keyframes spin {{
    0% {{
        transform: translateZ(calc(var(--cube-size) * -0.5)) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    100% {{
        transform: translateZ(calc(var(--cube-size) * -0.5)) rotateX(360deg) rotateY(720deg) rotateZ(180deg);
    }}
}}

/* Responsive scaling */
@media (max-width: 600px) {{
    :root {{
        --cube-size: 150px;
    }}
    .header {{ top: 5%; left: 5%; }}
    .header h1 {{ font-size: 1.8rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="scene">
            <div class="cube" id="cube">
                <div class="face front">Front</div>
                <div class="face back">Back</div>
                <div class="face right">Right</div>
                <div class="face left">Left</div>
                <div class="face top">Top</div>
                <div class="face bottom">Bottom</div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS (Adding subtle interactive mouse tracking to the scene's perspective origin)
    js = f"""// Interactive 3D enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const scene = document.querySelector('.scene');
    
    // Smoothly alter the perspective origin based on mouse movement
    // This makes the 3D effect feel much more physical and reactive
    container.addEventListener('mousemove', (e) => {{
        const x = e.clientX;
        const y = e.clientY;
        
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        // Calculate offset percentage (from 20% to 80%)
        const percentX = ((x - centerX) / centerX) * 50 + 50;
        const percentY = ((y - centerY) / centerY) * 50 + 50;
        
        scene.style.perspectiveOrigin = `${{percentX}}% ${{percentY}}%`;
    }});
    
    // Reset on mouse leave
    container.addEventListener('mouseleave', () => {{
        scene.style.perspectiveOrigin = '50% 50%';
        scene.style.transition = 'perspective-origin 1s ease-out';
    }});
    
    container.addEventListener('mouseenter', () => {{
        scene.style.transition = 'perspective-origin 0.1s ease-out';
    }});
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
