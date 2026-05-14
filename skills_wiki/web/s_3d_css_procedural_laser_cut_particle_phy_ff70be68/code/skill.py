def create_component(
    output_dir: str,
    title_text: str = "Precision Execution",
    body_text: str = "Deploying automated cutting sequence to separate the instance module.",
    color_scheme: str = "dark",
    accent_color: str = "#ff0055",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Laser Cut & Spark Particle visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#020617"
        text_color = "#f8fafc"
        surface_color = "rgba(30, 41, 59, 0.85)"
        surface_dark = "#0f172a"
        grid_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        surface_color = "rgba(255, 255, 255, 0.95)"
        surface_dark = "#cbd5e1"
        grid_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D CSS Procedural Laser Cut */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-dark: {surface_dark};
    --grid: {grid_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --duration: 6s;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
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
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1200px;
}}

/* 3D Stage */
.scene {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transform: rotateX(-20deg) rotateY(35deg);
    animation: scene-idle 20s infinite ease-in-out alternate;
}}

@keyframes scene-idle {{
    0% {{ transform: rotateX(-25deg) rotateY(30deg); }}
    100% {{ transform: rotateX(-15deg) rotateY(40deg); }}
}}

/* Grid Floor for spatial context */
.floor {{
    position: absolute;
    left: 50%; top: 50%;
    width: 2000px; height: 2000px;
    margin-left: -1000px; margin-top: -1000px;
    transform: translateY(250px) rotateX(90deg);
    background: 
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(circle at 50% 50%, black 20%, transparent 60%);
    -webkit-mask-image: radial-gradient(circle at 50% 50%, black 20%, transparent 60%);
}}

/* Shared Panel Properties */
.panel {{
    position: absolute;
    left: 50%; top: 50%;
    height: 160px; /* This becomes Z-depth upon rotation */
    margin-top: -80px; 
    transform-style: preserve-3d;
    will-change: transform;
}}

.panel-surface {{
    position: absolute;
    inset: 0;
    background: var(--surface);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
}}

/* Pseudo Extrusion Edges */
.panel-edge {{
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 12px;
    background: var(--surface-dark);
    border: 1px solid rgba(255,255,255,0.1);
    border-top: none;
    transform-origin: bottom;
    transform: rotateX(-90deg);
}}

.panel-cut-edge {{
    position: absolute;
    top: 0;
    width: 12px; height: 100%;
    background: var(--surface-dark);
    border: 1px solid var(--accent);
    box-shadow: inset 0 0 15px var(--accent);
}}

/* Main Block (Stays in place) */
.panel-main {{
    width: 400px;
    margin-left: 2px; /* 2px offset to open cut seam */
    transform-origin: left center;
    transform: translate3d(0, 0, 0) rotateX(90deg);
}}
.panel-main .panel-cut-edge {{
    left: 0;
    transform-origin: left;
    transform: rotateY(90deg);
}}

/* Text Content placed physically on the main slab */
.content {{
    padding: 0 40px;
    transform: translateZ(1px); /* Elevate slightly to avoid Z-fighting */
}}
.content h1 {{
    font-size: 28px;
    color: var(--accent);
    margin-bottom: 8px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}}
.content p {{
    font-size: 14px;
    opacity: 0.8;
    line-height: 1.6;
    max-width: 280px;
}}

/* Drop Block (Falls away) */
.panel-drop {{
    width: 140px;
    margin-left: -142px; /* -140px width + -2px offset to open cut seam */
    transform-origin: right center;
    animation: drop-fall var(--duration) infinite linear;
}}
.panel-drop .panel-cut-edge {{
    right: 0;
    transform-origin: right;
    transform: rotateY(-90deg);
}}

@keyframes drop-fall {{
    0% {{
        transform: translate3d(0, 0, 0) rotateX(90deg);
        opacity: 0;
        box-shadow: 0 0 60px var(--accent);
    }}
    8% {{
        transform: translate3d(0, 0, 0) rotateX(90deg);
        opacity: 1;
        box-shadow: 0 0 0px transparent;
    }}
    47.5% {{ /* Laser finishes cutting exactly here */
        transform: translate3d(0, 0, 0) rotateX(90deg);
    }}
    48.5% {{
        transform: translate3d(-4px, 0, 0) rotateX(90deg); /* Snap detach */
        opacity: 1;
    }}
    68% {{
        transform: translate3d(-40px, 400px, 40px) rotateX(60deg) rotateY(-30deg) rotateZ(15deg);
        opacity: 0;
    }}
    100% {{
        transform: translate3d(-40px, 400px, 40px) rotateX(60deg) rotateY(-30deg) rotateZ(15deg);
        opacity: 0;
    }}
}}

/* Laser Beam */
.laser {{
    position: absolute;
    left: 50%; top: 50%;
    width: 4px; height: 300px;
    margin-left: -2px; margin-top: -150px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 
        0 0 10px var(--accent),
        0 0 20px var(--accent),
        0 0 40px var(--accent),
        0 0 80px var(--accent);
    transform-origin: top center;
    animation: laser-cut var(--duration) infinite linear;
    will-change: transform, opacity;
}}

@keyframes laser-cut {{
    0%, 15% {{ transform: translate3d(0, -100px, -180px) scaleY(0); opacity: 0; }}
    20%     {{ transform: translate3d(0, -50px, -180px) scaleY(1); opacity: 1; }}
    25%     {{ transform: translate3d(0, -50px, -180px) scaleY(1); opacity: 1; }}
    55%     {{ transform: translate3d(0, -50px, 180px) scaleY(1); opacity: 1; }}
    60%     {{ transform: translate3d(0, -100px, 180px) scaleY(0); opacity: 0; }}
    100%    {{ transform: translate3d(0, -100px, 180px) scaleY(0); opacity: 0; }}
}}

/* Procedural Sparks System */
.sparks {{
    position: absolute;
    left: 50%; top: 50%;
    width: 0; height: 0;
    transform-style: preserve-3d;
}}

.spark {{
    position: absolute;
    left: 0; top: 0;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 0 6px var(--accent), 0 0 12px var(--accent);
    animation: spark-burst var(--duration) infinite linear;
    transform: scale(0);
    opacity: 0;
    will-change: transform, opacity;
}}

@keyframes spark-burst {{
    0% {{
        opacity: 0;
        transform: translate3d(0, 0, var(--tz)) scale(0);
    }}
    0.5% {{ /* Instant violent spawn */
        opacity: 1;
        transform: translate3d(0, 0, var(--tz)) scale(1.5);
    }}
    4% {{ /* Ballistic Apex */
        opacity: 1;
        transform: translate3d(calc(var(--tx) * 0.4), var(--ty-apex), var(--tz-apex)) scale(1);
    }}
    10% {{ /* Hits ground / fizzles */
        opacity: 0;
        transform: translate3d(var(--tx), var(--ty-end), var(--tz-end)) scale(0);
    }}
    100% {{
        opacity: 0;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="scene">
            <div class="floor"></div>
            
            <div class="panel panel-main">
                <div class="panel-surface">
                    <div class="content">
                        <h1>{title_text}</h1>
                        <p>{body_text}</p>
                    </div>
                </div>
                <div class="panel-edge"></div>
                <div class="panel-cut-edge left-edge"></div>
            </div>
            
            <div class="panel panel-drop">
                <div class="panel-surface"></div>
                <div class="panel-edge"></div>
                <div class="panel-cut-edge right-edge"></div>
            </div>
            
            <div class="laser"></div>
            <div class="sparks"></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Procedural Spark Generation synced perfectly with CSS Animation Timing
document.addEventListener('DOMContentLoaded', () => {{
    const sparksContainer = document.querySelector('.sparks');
    const NUM_SPARKS = 100;
    const DURATION = 6; // Matching CSS var(--duration)
    
    // Panel Depth Geometry (corresponds to CSS panel height logic)
    const Z_START = -80; 
    const Z_END = 80;
    const Z_DEPTH = Math.abs(Z_START - Z_END);
    
    // Laser Timing Data from CSS keyframes
    // Laser translates from Z = -180px to Z = 180px
    // Movement phase is from t=25% (1.5s) to t=55% (3.3s) -> Total movement time = 1.8s
    const LASER_START_Z = -180;
    const LASER_END_Z = 180;
    const LASER_TRAVEL_DIST = Math.abs(LASER_START_Z - LASER_END_Z);
    const TIME_START = 1.5; 
    const TIME_TRAVEL = 1.8;

    for (let i = 0; i < NUM_SPARKS; i++) {{
        const spark = document.createElement('div');
        spark.classList.add('spark');
        
        // Distribution of sparks evenly along the Z axis (the cut depth)
        const progress = i / (NUM_SPARKS - 1);
        const tz = Z_START + progress * Z_DEPTH;
        
        // Calculate EXACT second the laser beam intersects this spark's Z coordinate
        const distanceCovered = tz - LASER_START_Z;
        const timeOffset = (distanceCovered / LASER_TRAVEL_DIST) * TIME_TRAVEL;
        const t_explode = TIME_START + timeOffset;
        
        // The infinite loop trick: negative delay forces animation to spawn exactly at our calculated phase
        const delay = t_explode - DURATION;
        
        // Random Ballistic Physics
        const tx = (Math.random() - 0.5) * 160; // Scatter X
        const tyApex = -(Math.random() * 80 + 30); // Erupt Upwards
        const tyEnd = tyApex + (Math.random() * 120 + 80); // Fall downward past origin
        const tzEnd = tz + (Math.random() - 0.5) * 100; // Drift Z
        
        const size = Math.random() * 2.5 + 1.5;
        
        // Push raw math into CSS Custom Properties
        spark.style.setProperty('--tz', `${tz}px`);
        spark.style.setProperty('--tx', `${tx}px`);
        spark.style.setProperty('--ty-apex', `${tyApex}px`);
        spark.style.setProperty('--ty-end', `${tyEnd}px`);
        spark.style.setProperty('--tz-apex', `${(tz + tzEnd)/2}px`);
        spark.style.setProperty('--tz-end', `${tzEnd}px`);
        
        spark.style.width = `${size}px`;
        spark.style.height = `${size}px`;
        spark.style.marginLeft = `${-(size/2)}px`;
        spark.style.marginTop = `${-(size/2)}px`;
        
        // Apply synchronized chronometry 
        spark.style.animationDelay = `${delay}s`;
        
        sparksContainer.appendChild(spark);
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
