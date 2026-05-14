def create_component(
    output_dir: str,
    title_text: str = "Isometric View",
    body_text: str = "Pure SVG geometry with synchronized shadow physics.",
    color_scheme: str = "dark",
    accent_color: str = "#08d9d6",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Isometric SVG Cube.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Colors ===
    if color_scheme == "dark":
        bg_color = "#1a1c23"
        text_color = "#f0f0f0"
        text_muted = "#a0a0b0"
        # Deep blue base for the isometric shadow gradient
        grad_base = "rgba(0, 0, 255, 0.6)" 
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        text_muted = "#6b7280"
        # Darkened accent variant for light mode shadow gradient
        grad_base = "rgba(0, 0, 100, 0.5)"

    # === CSS ===
    css = f"""/* Floating Isometric Cube Styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}}

.component-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    padding: 2rem;
}}

.text-content {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--text-muted);
    font-weight: 400;
}}

/* SVG Cube Specifics */
.cube-wrapper {{
    width: 100%;
    max-width: 280px; /* Controls the overall visual size */
    aspect-ratio: 1 / 1;
}}

#isometric-cube {{
    width: 100%;
    height: 100%;
    overflow: visible; /* Prevents shadow clipping during scale */
}}

/* Animation assignments */
.face {{
    animation: floatAnim 1.5s infinite ease-in-out alternate;
}}

.shadow {{
    /* Origin set to the exact center coordinates of the shadow path */
    transform-origin: 50px 80px; 
    animation: shadowAnim 1.5s infinite ease-in-out alternate;
}}

/* Keyframes */
@keyframes floatAnim {{
    0% {{
        transform: translateY(0px);
    }}
    100% {{
        transform: translateY(8px);
    }}
}}

@keyframes shadowAnim {{
    0% {{
        transform: scale(1);
        fill: rgba(0, 0, 0, 0.3);
    }}
    100% {{
        transform: scale(0.85);
        fill: rgba(0, 0, 0, 0.6);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-container">
        
        <div class="cube-wrapper">
            <svg id="isometric-cube" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <!-- Core Gradient spanning the entire geometry -->
                    <linearGradient id="cube-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{accent_color}" stop-opacity="1" />
                        <stop offset="100%" stop-color="{grad_base}" />
                    </linearGradient>
                    
                    <!-- Soft blur for the ground shadow -->
                    <filter id="shadow-blur">
                        <feGaussianBlur in="sourceGraphic" stdDeviation="3" />
                    </filter>
                </defs>

                <!-- Shadow (drawn first so it sits underneath) -->
                <path class="shadow" 
                      d="M5,85 50,100 95,85 50,60" 
                      fill="rgba(0,0,0,0.4)" 
                      filter="url(#shadow-blur)" />

                <!-- The 3 Isometric Faces -->
                <path class="face roof"  d="M10,20 50,5 90,20 50,35" fill="url(#cube-grad)" />
                <path class="face left"  d="M10,20 50,35 50,90 10,75" fill="url(#cube-grad)" />
                <path class="face right" d="M50,90 50,35 90,20 90,75" fill="url(#cube-grad)" />
            </svg>
        </div>

        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Component interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    // The core 3D isometric floating effect is achieved entirely via SVG and CSS keyframes.
    // No JavaScript is required for the animation loop, ensuring smooth, hardware-accelerated performance.
    console.log("Isometric SVG cube successfully mounted.");
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
