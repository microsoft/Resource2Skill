def create_component(
    output_dir: str,
    title_text: str = "Moon Light",
    body_text: str = "Scroll down to experience the multi-layered parallax effect. The background, moon, mountains, and text all move at different speeds to create a sense of depth and immersion.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffffff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Parallax Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a2a43"
        sky_color = "#051624"
        text_color = "#ffffff"
        mountain_back_fill = "#14456b"
        mountain_front_fill = "#0a2a43"
        moon_glow = "rgba(255, 255, 255, 0.8)"
    else:
        bg_color = "#e2e8f0"
        sky_color = "#cbd5e1"
        text_color = "#0f172a"
        mountain_back_fill = "#94a3b8"
        mountain_front_fill = "#e2e8f0"
        moon_glow = "rgba(255, 255, 255, 1)"

    # === CSS ===
    css = f"""/* Vanilla JS Layered Parallax Hero */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --sky-color: {sky_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --moon-glow: {moon_glow};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    min-height: 200vh; /* Allow scrolling */
    overflow-x: hidden;
}}

/* Parallax Section Container */
.parallax-section {{
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--sky-color);
}}

/* Bottom Fade Overlay to blend smoothly into content */
.parallax-section::before {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 150px;
    background: linear-gradient(to top, var(--bg-color), transparent);
    z-index: 100;
}}

/* Common styling for all image/shape layers */
.parallax-layer {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    will-change: transform;
}}

/* Sky Layer (Starry Background) */
.layer-sky {{
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 120px, #ddd, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    z-index: 1;
}}

/* Moon Layer */
.layer-moon {{
    z-index: 2;
    display: flex;
    justify-content: flex-end;
    padding: 10% 15% 0 0;
}}
.moon-shape {{
    width: 150px;
    height: 150px;
    background: radial-gradient(circle at 30% 30%, #fff, #f0f0f0);
    border-radius: 50%;
    box-shadow: 0 0 80px 20px var(--moon-glow);
}}

/* Mountain Back Layer */
.layer-mountain-back {{
    z-index: 3;
    display: flex;
    align-items: flex-end;
}}
.layer-mountain-back svg {{
    width: 100vw;
    height: auto;
    min-height: 60vh;
    display: block;
}}

/* Typography Layer */
.parallax-title {{
    position: relative;
    color: var(--text-color);
    font-size: clamp(4rem, 10vw, 10rem);
    font-weight: 700;
    text-align: center;
    text-transform: capitalize;
    z-index: 4;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    will-change: transform;
}}

/* Mountain Front Layer */
.layer-mountain-front {{
    z-index: 5;
    display: flex;
    align-items: flex-end;
}}
.layer-mountain-front svg {{
    width: 100vw;
    height: auto;
    min-height: 40vh;
    display: block;
}}

/* Standard Page Content Setup */
.content-section {{
    position: relative;
    z-index: 10;
    padding: 80px 10%;
    background: var(--bg-color);
    min-height: 100vh;
}}
.content-section h2 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}
.content-section p {{
    font-size: 1.2rem;
    line-height: 1.8;
    max-width: 800px;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section class="parallax-section">
        
        <!-- Sky / Stars -->
        <div class="parallax-layer layer-sky" id="sky"></div>
        
        <!-- Moon -->
        <div class="parallax-layer layer-moon" id="moon">
            <div class="moon-shape"></div>
        </div>
        
        <!-- Distant Mountains -->
        <div class="parallax-layer layer-mountain-back" id="mountain-back">
            <svg viewBox="0 0 1440 600" preserveAspectRatio="none">
                <path d="M0,600 L0,300 L200,200 L400,450 L700,100 L1000,400 L1250,250 L1440,400 L1440,600 Z" fill="{mountain_back_fill}"></path>
            </svg>
        </div>
        
        <!-- Main Text -->
        <h2 class="parallax-title" id="text">{title_text}</h2>
        
        <!-- Foreground Mountains/Terrain -->
        <div class="parallax-layer layer-mountain-front" id="mountain-front">
            <svg viewBox="0 0 1440 400" preserveAspectRatio="none">
                <path d="M0,400 L0,150 L300,50 L600,200 L900,0 L1200,150 L1440,50 L1440,400 Z" fill="{mountain_front_fill}"></path>
            </svg>
        </div>

    </section>

    <!-- Post-Hero Content to enable scrolling -->
    <section class="content-section">
        <h2>Journey Continues</h2>
        <p>{body_text}</p>
        <br><br>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam nec efficitur turpis. Fusce eget lacus eget tellus ullamcorper vestibulum vel eget lectus. Integer pulvinar dui vitae est varius tristique. Nullam tristique dui in augue luctus tincidunt.</p>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Layered Parallax Hero Animation

document.addEventListener('DOMContentLoaded', () => {{
    // Select layers
    const sky = document.getElementById('sky');
    const moon = document.getElementById('moon');
    const mountainBack = document.getElementById('mountain-back');
    const mountainFront = document.getElementById('mountain-front');
    const text = document.getElementById('text');

    // Scroll event listener
    window.addEventListener('scroll', () => {{
        // Get current scroll position
        let value = window.scrollY;

        // Apply distinct translation factors to each layer.
        // We use translate3d instead of 'top' or 'left' for GPU hardware acceleration
        // and to avoid expensive layout repaints on scroll.

        // Sky moves down slowly
        if (sky) sky.style.transform = `translate3d(0, ${{value * 0.5}}px, 0)`;
        
        // Moon moves left and down
        if (moon) moon.style.transform = `translate3d(${{value * -0.5}}px, ${{value * 0.5}}px, 0)`;
        
        // Back mountains move down slightly (creates depth)
        if (mountainBack) mountainBack.style.transform = `translate3d(0, ${{value * 0.25}}px, 0)`;
        
        // Text moves down faster than mountains, slower than foreground
        if (text) text.style.transform = `translate3d(0, ${{value * 1.2}}px, 0)`;
        
        // Front mountains remain anchored or move slightly to ground them
        // In some effects they are static (`translateY(0)`), here we move them very subtly
        if (mountainFront) mountainFront.style.transform = `translate3d(0, ${{value * 0.05}}px, 0)`;
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
