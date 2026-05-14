def create_component(
    output_dir: str,
    title_text: str = "Find Every Hidden Threat in Your System - Before it Finds You.",
    body_text: str = "Futuristic Mask scans your system, detects AI-level threats, and fixes them instantly - securing your future today.",
    color_scheme: str = "dark",
    accent_color: str = "#0044FF", 
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Futuristic Tubelight Hero Glow effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex to rgb for CSS variable interpolation
    hex_code = accent_color.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([c*2 for c in hex_code])
    accent_rgb = f"{int(hex_code[0:2], 16)}, {int(hex_code[2:4], 16)}, {int(hex_code[4:6], 16)}"

    # Set theme colors (Effect requires high contrast, so light mode remains deeply tinted)
    if color_scheme == "dark":
        bg_color = "#030614"
        text_color = "#ffffff"
        text_muted = "#94a3b8"
        nav_bg = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#0f172a"  # Enforce a dark canvas to make the light visible
        text_color = "#f8fafc"
        text_muted = "#cbd5e1"
        nav_bg = "rgba(0, 0, 0, 0.2)"

    css = f"""/* Futuristic Tubelight Hero Glow */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --accent-rgb: {accent_rgb};
    --nav-bg: {nav_bg};
    --max-width: 1200px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
}}

/* --- NAVIGATION --- */
header {{
    width: 100%;
    padding: 24px 0;
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 20;
}}

.nav-container {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background: var(--accent);
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(var(--accent-rgb), 0.5);
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    opacity: 0.8;
    transition: opacity 0.3s ease;
}}

.nav-links a:hover {{
    opacity: 1;
}}

.btn {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 12px 28px;
    border-radius: 30px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(var(--accent-rgb), 0.4);
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(var(--accent-rgb), 0.6);
}}

/* --- HERO SECTION --- */
.hero {{
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    /* Ensure content occupies min height for effect */
    min-height: 700px;
    overflow: hidden;
}}

.hero-content {{
    max-width: 860px;
    text-align: center;
    position: relative;
    z-index: 10;
    margin-bottom: 100px; /* offset upwards to balance bottom light */
}}

h1 {{
    font-size: 4rem;
    line-height: 1.15;
    font-weight: 700;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
    background: linear-gradient(to bottom, #ffffff, #c2d2e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

p.subtitle {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 700px;
    margin: 0 auto 40px auto;
    font-weight: 400;
}}

/* --- TUBELIGHT EFFECT --- */
.tubelight-wrapper {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100vw;
    height: 100%;
    pointer-events: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    z-index: 1;
}}

.light-beam {{
    position: absolute;
    bottom: 10px; /* Sit right above the tube */
    width: 150%;
    height: 80%;
    /* Create the cone shape: Wide at top, narrow at bottom */
    clip-path: polygon(0 0, 100% 0, calc(50% + 200px) 100%, calc(50% - 200px) 100%);
    background: linear-gradient(to top, rgba(var(--accent-rgb), 0.45) 0%, transparent 80%);
    filter: blur(60px);
    mix-blend-mode: screen;
    animation: pulseBeam 5s infinite alternate ease-in-out;
    transform-origin: bottom center;
    will-change: transform;
}}

.light-tube {{
    position: absolute;
    bottom: 0;
    width: 380px;
    height: 8px;
    background: #ffffff;
    border-radius: 10px 10px 0 0;
    box-shadow: 
        0 0 10px #ffffff,
        0 0 20px rgba(var(--accent-rgb), 0.8),
        0 0 50px rgba(var(--accent-rgb), 0.8),
        0 0 100px rgba(var(--accent-rgb), 1);
    z-index: 2;
}}

/* Ambient Glow Animation */
@keyframes pulseBeam {{
    0% {{
        opacity: 0.8;
        filter: blur(55px);
    }}
    100% {{
        opacity: 1;
        filter: blur(65px);
    }}
}}

/* Responsive */
@media (max-width: 768px) {{
    h1 {{ font-size: 2.5rem; }}
    p.subtitle {{ font-size: 1.1rem; }}
    .nav-links {{ display: none; }}
    .light-beam {{
        clip-path: polygon(0 0, 100% 0, calc(50% + 120px) 100%, calc(50% - 120px) 100%);
    }}
    .light-tube {{ width: 240px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Futuristic Tubelight Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="nav-container">
            <div class="logo">
                <div class="logo-icon"></div>
                MASKFU
            </div>
            <ul class="nav-links">
                <li><a href="#">About</a></li>
                <li><a href="#">Pricing</a></li>
                <li><a href="#">Roadmap</a></li>
                <li><a href="#">Blog</a></li>
            </ul>
            <button class="btn">Contact Us</button>
        </div>
    </header>

    <main class="hero">
        <div class="tubelight-wrapper" id="tubelight">
            <div class="light-beam" id="beam"></div>
            <div class="light-tube"></div>
        </div>

        <div class="hero-content">
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
            <button class="btn" style="padding: 16px 36px; font-size: 1.1rem;">Join the Future</button>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>
"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const beam = document.getElementById('beam');
    
    // Subtle parallax effect on mouse move to make the volumetric light feel 3D
    document.addEventListener('mousemove', (e) => {
        const { innerWidth, innerHeight } = window;
        const x = e.clientX;
        const y = e.clientY;
        
        // Calculate offsets (-1 to 1)
        const xOffset = (x / innerWidth) * 2 - 1;
        const yOffset = (y / innerHeight) * 2 - 1;
        
        // Apply a gentle skew and scale to the light beam
        const skewX = xOffset * -5; // Max 5 degrees skew
        const scaleY = 1 + Math.abs(yOffset) * 0.1; // Max 10% height increase
        
        requestAnimationFrame(() => {
            beam.style.transform = `skewX(${skewX}deg) scaleY(${scaleY})`;
        });
    });
});
"""

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
