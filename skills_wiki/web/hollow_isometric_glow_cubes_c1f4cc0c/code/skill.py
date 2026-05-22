def create_component(
    output_dir: str,
    title_text: str = "Isometric Data Nodes",
    body_text: str = "Hover over the nodes to examine the core and move your mouse to shift perspective.",
    color_scheme: str = "dark",
    accent_color: str = "#00d2ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Hollow Isometric Glow Cubes visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme processing
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        body_color = "#9ca3af"
        border_color = "rgba(255, 255, 255, 0.15)"
        shadow_opacity = "0.6"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        body_color = "#4b5563"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow_opacity = "0.3"

    # === CSS ===
    css = f"""/* Hollow Isometric Glow Cubes */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --body-text: {body_color};
    --accent: {accent_color};
    --border: {border_color};
    --shadow-op: {shadow_opacity};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
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
    max-width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6rem;
    perspective: 2000px;
    position: relative;
}}

.header {{
    text-align: center;
    z-index: 10;
    padding: 0 2rem;
    pointer-events: none;
}}

.title {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}}

.body-text {{
    color: var(--body-text);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

.scene-wrapper {{
    perspective: 1500px;
}}

.scene {{
    display: flex;
    gap: 6rem;
    flex-wrap: wrap;
    justify-content: center;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
}}

/* === Cube Geometry === */
.cube-wrapper {{
    position: relative;
    width: 120px;
    height: 120px;
}}

.cube-animator {{
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    animation: float 4s ease-in-out infinite;
}}

.cube {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    /* Perfect Isometric rotation */
    transform: rotateX(-35.264deg) rotateY(45deg);
    transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
    cursor: pointer;
}}

.cube-wrapper:hover .cube {{
    transform: rotateX(-15deg) rotateY(65deg) scale(1.1);
}}

.face {{
    position: absolute;
    width: 100%;
    height: 100%;
    border: 1px solid var(--border);
    box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.05);
    transition: border-color 0.3s ease;
}}

.cube-wrapper:hover .face {{
    border-color: rgba(255, 255, 255, 0.4);
}}

/* 
  Gradient logic: 
  Start bright at the intersection corner, fade to base color, then fade to transparent.
  The transparent tails reveal the inner glow and the background.
*/
.top {{
    transform: rotateX(90deg) translateZ(60px);
    background: linear-gradient(315deg, var(--bright) 0%, var(--base) 40%, transparent 80%);
}}

.front {{
    transform: translateZ(60px);
    background: linear-gradient(225deg, var(--bright) 0%, var(--base) 40%, transparent 80%);
}}

.right {{
    transform: rotateY(90deg) translateZ(60px);
    background: linear-gradient(135deg, var(--bright) 0%, var(--base) 40%, transparent 80%);
}}

/* Inner Light Source */
.glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70px;
    height: 70px;
    transform: translate(-50%, -50%) translateZ(0);
    background: var(--base);
    border-radius: 50%;
    filter: blur(25px);
    opacity: 0.8;
    transition: opacity 0.3s ease, filter 0.3s ease;
}}

.cube-wrapper:hover .glow {{
    opacity: 1;
    filter: blur(40px);
    background: var(--bright);
}}

/* Floor Shadow */
.shadow {{
    position: absolute;
    bottom: -60px;
    left: 50%;
    width: 120px; 
    height: 120px;
    transform: translateX(-50%) rotateX(75deg);
    background: var(--base);
    filter: blur(35px);
    opacity: var(--shadow-op);
    border-radius: 50%;
    animation: shadowPulse 4s ease-in-out infinite;
}}

/* Staggered Animations */
.cube-wrapper:nth-child(1) .cube-animator,
.cube-wrapper:nth-child(1) .shadow {{ animation-delay: 0s; }}

.cube-wrapper:nth-child(2) .cube-animator,
.cube-wrapper:nth-child(2) .shadow {{ animation-delay: -1.3s; }}

.cube-wrapper:nth-child(3) .cube-animator,
.cube-wrapper:nth-child(3) .shadow {{ animation-delay: -2.6s; }}

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-25px); }}
}}

@keyframes shadowPulse {{
    0%, 100% {{ transform: translateX(-50%) rotateX(75deg) scale(1); opacity: var(--shadow-op); }}
    50% {{ transform: translateX(-50%) rotateX(75deg) scale(0.7); opacity: calc(var(--shadow-op) / 2); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="scene-wrapper">
            <div class="scene">
                <!-- Node 1: Orange/Red -->
                <div class="cube-wrapper" style="--base: #df3d04; --bright: #ffe5be;">
                    <div class="shadow"></div>
                    <div class="cube-animator">
                        <div class="cube">
                            <div class="face top"></div>
                            <div class="face front"></div>
                            <div class="face right"></div>
                            <div class="glow"></div>
                        </div>
                    </div>
                </div>

                <!-- Node 2: Dynamic Accent User Color -->
                <div class="cube-wrapper" style="--base: var(--accent); --bright: color-mix(in srgb, var(--accent) 30%, white);">
                    <div class="shadow"></div>
                    <div class="cube-animator">
                        <div class="cube">
                            <div class="face top"></div>
                            <div class="face front"></div>
                            <div class="face right"></div>
                            <div class="glow"></div>
                        </div>
                    </div>
                </div>

                <!-- Node 3: Neon Green -->
                <div class="cube-wrapper" style="--base: #00e676; --bright: #e8f5e9;">
                    <div class="shadow"></div>
                    <div class="cube-animator">
                        <div class="cube">
                            <div class="face top"></div>
                            <div class="face front"></div>
                            <div class="face right"></div>
                            <div class="glow"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Parallax Mouse Interaction for the 3D Scene
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const scene = document.querySelector('.scene');
    
    // Check if user prefers reduced motion before applying mouse tracking
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion) {{
        container.addEventListener('mousemove', (e) => {{
            // Calculate mouse position relative to container center
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Normalize and scale to a maximum rotation degree (e.g., +/- 12 degrees)
            const xRotation = -(y / rect.height) * 24; // pitch
            const yRotation = (x / rect.width) * 24;   // yaw
            
            // Apply the 3D transform to the entire scene
            scene.style.transform = `rotateX(${{xRotation}}deg) rotateY(${{yRotation}}deg)`;
        }});
        
        // Reset scene rotation when mouse leaves the container
        container.addEventListener('mouseleave', () => {{
            scene.style.transform = `rotateX(0deg) rotateY(0deg)`;
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
