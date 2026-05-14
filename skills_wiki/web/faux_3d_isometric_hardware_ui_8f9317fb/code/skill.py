def create_component(
    output_dir: str,
    title_text: str = "System Initialized",
    body_text: str = "All hardware modules are functioning within optimal parameters. Awaiting user input to begin the boot sequence.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent (e.g., blue)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Faux-3D Isometric Hardware UI effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        grid_color = "rgba(255, 255, 255, 0.03)"
        surface_color = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        shadow_color = "rgba(0, 0, 0, 0.6)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#e2e8f0"
        grid_color = "rgba(0, 0, 0, 0.04)"
        surface_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#475569"
        shadow_color = "rgba(15, 23, 42, 0.15)"
        border_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Faux-3D Isometric Hardware UI */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --grid: {grid_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow: {shadow_color};
    --border: {border_color};
    
    /* Dynamic orbit variables updated by JS */
    --rot-x: 55deg;
    --rot-z: -45deg;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    background-image:
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: grab;
    user-select: none;
}}

body:active {{
    cursor: grabbing;
}}

.scene {{
    width: {width_px}px;
    height: {height_px}px;
    perspective: 2500px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.pivot {{
    transform-style: preserve-3d;
    transform: rotateX(var(--rot-x)) rotateZ(var(--rot-z));
    transition: transform 0.1s linear;
}}

/* Main Card Chassis */
.isometric-card {{
    width: 360px;
    height: 480px;
    background: var(--surface);
    border: 1px solid var(--border);
    position: relative;
    transform-style: preserve-3d;
    animation: float-card 6s ease-in-out infinite;
}}

/* Chassis Extrusions (Sides) */
.isometric-card::before {{
    content: ''; position: absolute;
    top: 0; left: 0; width: 24px; height: 100%;
    background: linear-gradient(to bottom, rgba(255,255,255,0.05), rgba(0,0,0,0.3)), var(--surface);
    transform-origin: left; transform: rotateY(-90deg);
}}

.isometric-card::after {{
    content: ''; position: absolute;
    bottom: 0; left: 0; width: 100%; height: 24px;
    background: linear-gradient(to right, rgba(0,0,0,0.2), rgba(0,0,0,0.45)), var(--surface);
    transform-origin: bottom; transform: rotateX(-90deg);
}}

/* Floor Drop Shadow */
.card-shadow {{
    position: absolute;
    top: 24px; left: -24px;
    width: 100%; height: 100%;
    background: var(--shadow);
    filter: blur(28px);
    animation: float-shadow 6s ease-in-out infinite;
}}

@keyframes float-card {{
    0%, 100% {{ transform: translateZ(0px); }}
    50% {{ transform: translateZ(30px); }}
}}

@keyframes float-shadow {{
    0%, 100% {{ transform: translateZ(-1px); opacity: 1; }}
    /* Moves down inversely to stay on the floor, reduces opacity to simulate distance */
    50% {{ transform: translateZ(-31px); opacity: 0.5; }}
}}

/* Hardware Accents */
.led-indicator {{
    width: 10px; height: 10px;
    border-radius: 50%;
    position: absolute;
    top: 24px; right: 24px;
    transform: translateZ(1px);
    animation: pulse-led 3s infinite;
}}

@keyframes pulse-led {{
    0%, 100% {{ 
        background-color: #10b981; 
        box-shadow: 0 0 12px #10b981, inset 1px 1px 2px rgba(255,255,255,0.8); 
    }}
    50% {{ 
        background-color: #064e3b; 
        box-shadow: 0 0 2px #064e3b, inset 1px 1px 2px rgba(255,255,255,0.2); 
    }}
}}

.speaker-grill {{
    position: absolute;
    bottom: 24px; right: 24px;
    display: flex;
    gap: 5px;
    transform: translateZ(1px);
}}

.speaker-grill span {{
    width: 4px; height: 28px;
    background: rgba(0,0,0,0.15);
    border-radius: 2px;
    box-shadow: inset 1px 1px 3px rgba(0,0,0,0.4);
}}

/* Content Layout */
.card-content {{
    position: relative;
    padding: 40px;
    height: 100%;
    display: flex;
    flex-direction: column;
    transform-style: preserve-3d;
}}

.card-icon {{
    width: 54px; height: 54px;
    color: var(--accent);
    transform: translateZ(40px);
    margin-bottom: 24px;
}}

.card-title {{
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 12px;
    color: var(--text);
    transform: translateZ(30px);
    letter-spacing: -0.5px;
}}

.card-body {{
    font-size: 15px;
    color: var(--text-muted);
    line-height: 1.6;
    transform: translateZ(20px);
    margin-bottom: auto;
}}

/* 3D Hardware Buttons */
.action-group {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    transform-style: preserve-3d;
    margin-top: 40px;
}}

.iso-button {{
    padding: 16px 20px;
    border: none;
    font-family: inherit;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1), filter 0.2s;
    outline: none;
}}

.iso-button:hover {{
    filter: brightness(1.15);
}}

/* Primary Button Extrusion */
.iso-button.primary {{
    background: var(--accent);
    color: #fff;
    transform: translateZ(20px);
}}
.iso-button.primary::before {{
    content: ''; position: absolute;
    top: 0; left: 0; width: 8px; height: 100%;
    background: linear-gradient(rgba(255,255,255,0.1), rgba(0,0,0,0.25)), var(--accent);
    transform-origin: left; transform: rotateY(-90deg);
}}
.iso-button.primary::after {{
    content: ''; position: absolute;
    bottom: 0; left: 0; width: 100%; height: 8px;
    background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.4)), var(--accent);
    transform-origin: bottom; transform: rotateX(-90deg);
}}
.iso-button.primary:active {{
    transform: translateZ(8px);
}}

/* Secondary Button Extrusion */
.iso-button.secondary {{
    background: var(--bg);
    color: var(--text);
    transform: translateZ(12px);
}}
.iso-button.secondary::before {{
    content: ''; position: absolute;
    top: 0; left: 0; width: 6px; height: 100%;
    background: linear-gradient(rgba(255,255,255,0.3), rgba(0,0,0,0.1)), var(--bg);
    transform-origin: left; transform: rotateY(-90deg);
}}
.iso-button.secondary::after {{
    content: ''; position: absolute;
    bottom: 0; left: 0; width: 100%; height: 6px;
    background: linear-gradient(rgba(0,0,0,0.05), rgba(0,0,0,0.2)), var(--bg);
    transform-origin: bottom; transform: rotateX(-90deg);
}}
.iso-button.secondary:active {{
    transform: translateZ(4px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faux-3D Isometric UI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scene">
        <div class="pivot">
            <div class="isometric-card">
                
                <div class="card-shadow"></div>
                <div class="led-indicator"></div>
                <div class="speaker-grill">
                    <span></span><span></span><span></span><span></span>
                </div>
                
                <div class="card-content">
                    <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                        <polyline points="2 17 12 22 22 17"></polyline>
                        <polyline points="2 12 12 17 22 12"></polyline>
                    </svg>
                    
                    <h1 class="card-title">{title_text}</h1>
                    <p class="card-body">{body_text}</p>
                    
                    <div class="action-group">
                        <button class="iso-button primary">Engage Module</button>
                        <button class="iso-button secondary">Diagnostics</button>
                    </div>
                </div>
                
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Orbit controls for the Isometric 3D Scene
document.addEventListener('DOMContentLoaded', () => {{
    let isDragging = false;
    let previousX = 0;
    let previousY = 0;
    
    // Initial isometric angles corresponding to CSS variables
    let rotX = 55;
    let rotZ = -45;

    document.addEventListener('mousedown', (e) => {{
        // Do not trigger orbit if the user is clicking a button
        if (e.target.closest('.iso-button')) return;
        
        isDragging = true;
        previousX = e.clientX;
        previousY = e.clientY;
    }});

    document.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        
        const deltaX = e.clientX - previousX;
        const deltaY = e.clientY - previousY;
        
        // Adjust sensitivity via multiplier
        rotZ += deltaX * 0.4;
        rotX -= deltaY * 0.4;
        
        // Clamp X rotation to prevent flipping upside down completely
        rotX = Math.max(10, Math.min(85, rotX));
        
        // Push updated angles to CSS custom properties
        document.documentElement.style.setProperty('--rot-x', `${{rotX}}deg`);
        document.documentElement.style.setProperty('--rot-z', `${{rotZ}}deg`);
        
        previousX = e.clientX;
        previousY = e.clientY;
    }});

    document.addEventListener('mouseup', () => {{
        isDragging = false;
    }});
    
    document.addEventListener('mouseleave', () => {{
        isDragging = false;
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
