def create_component(
    output_dir: str,
    title_text: str = "Interactive Depth",
    body_text: str = "Move your cursor to explore the parallax dimension.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff4757",     # Used for gradient accents
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Parallax Depth Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_start = "#1a1a2e"
        bg_end = "#16213e"
        text_color = "#ffffff"
        particle_bg = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_start = "#f8f9fa"
        bg_end = "#e9ecef"
        text_color = "#2d3436"
        particle_bg = "rgba(0, 0, 0, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Interactive Parallax Depth Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, sans-serif;
}}

.interactive-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    background: linear-gradient(135deg, {bg_start}, {bg_end});
    box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    
    /* Crucial for the 3D effect */
    perspective: 1200px;
    
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Decorative gradient orb based on accent color */
.interactive-container::before {{
    content: '';
    position: absolute;
    width: 60%;
    height: 60%;
    background: {accent_color};
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.3;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 0;
    pointer-events: none;
}}

#particle-canvas {{
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
}}

.parallax-particle {{
    position: absolute;
    border-radius: 50%;
    background: {particle_bg};
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    /* Soft transition to smooth out mouse movement */
    transition: transform 0.15s cubic-bezier(0.2, 0, 0.2, 1);
    will-change: transform;
}}

.content-wrapper {{
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 40px;
    pointer-events: none; /* Let mouse events pass through to container */
    
    /* Allows children to pop out in Z-space */
    transform-style: preserve-3d;
    transition: transform 0.15s cubic-bezier(0.2, 0, 0.2, 1);
    will-change: transform;
}}

.title {{
    color: {text_color};
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 20px;
    
    /* Pop out from the screen */
    transform: translateZ(80px);
    text-shadow: 0 25px 50px {shadow_color};
}}

.subtitle {{
    color: {text_color};
    font-size: 1.5rem;
    font-weight: 400;
    opacity: 0.9;
    
    /* Pop out slightly less than the title */
    transform: translateZ(40px);
    text-shadow: 0 15px 30px {shadow_color};
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="interactive-container" id="hero-container">
        <div id="particle-canvas"></div>
        <div class="content-wrapper" id="hero-content">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('hero-container');
    const content = document.getElementById('hero-content');
    const canvas = document.getElementById('particle-canvas');
    
    const PARTICLE_COUNT = 35;
    const particles = [];

    // Generate random parallax particles
    for (let i = 0; i < PARTICLE_COUNT; i++) {{
        const p = document.createElement('div');
        p.className = 'parallax-particle';
        
        // Randomize size between 20px and 120px
        const size = Math.random() * 100 + 20;
        p.style.width = `${{size}}px`;
        p.style.height = `${{size}}px`;
        
        // Randomize initial position
        p.style.left = `${{Math.random() * 100}}%`;
        p.style.top = `${{Math.random() * 100}}%`;
        
        // Assign a random depth multiplier (parallax speed)
        // Higher value = moves faster/feels closer
        const depth = Math.random() * 2 + 0.2;
        p.dataset.depth = depth;
        
        canvas.appendChild(p);
        particles.push(p);
    }}

    // Handle mouse movement for 3D tilt and parallax
    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        
        // Calculate normalized mouse position relative to container (-0.5 to 0.5)
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        // 1. Tilt the content wrapper
        // Multiplying by negative values reverses the tilt direction for a natural feel
        const tiltMaxDegrees = 20;
        const rotateX = y * -tiltMaxDegrees; 
        const rotateY = x * tiltMaxDegrees;
        content.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;

        // 2. Translate the background particles
        // Particles move in opposition to the mouse to create parallax depth
        particles.forEach(p => {{
            const depth = parseFloat(p.dataset.depth);
            const moveMaxPx = 80;
            const moveX = x * -moveMaxPx * depth;
            const moveY = y * -moveMaxPx * depth;
            p.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
    }});

    // Reset transforms when mouse leaves the container
    container.addEventListener('mouseleave', () => {{
        content.style.transform = `rotateX(0deg) rotateY(0deg)`;
        particles.forEach(p => {{
            p.style.transform = `translate(0px, 0px)`;
        }});
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
