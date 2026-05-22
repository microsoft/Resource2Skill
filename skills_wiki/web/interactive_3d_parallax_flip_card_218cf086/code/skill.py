def create_component(
    output_dir: str,
    title_text: str = "3D Transform",
    body_text: str = "Hover to experience perspective parallax. Click the card to flip it around and see the backface.",
    color_scheme: str = "dark",        
    accent_color: str = "#10b981",     
    width_px: int = 340,
    height_px: int = 460,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Parallax Flip Card effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Interactive 3D Parallax Flip Card */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
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
    perspective: 1200px; /* Establishes the 3D viewport for the body */
}}

/* 1. SCENE: Creates the 3D space */
.scene {{
    width: var(--width);
    height: var(--height);
    perspective: 1000px; 
    cursor: pointer;
}}

/* 2. TILT WRAPPER: Managed by JS for mouse tracking */
.tilt-wrapper {{
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    will-change: transform;
}}

/* Add a transition only when mouse leaves to snap back smoothly */
.tilt-wrapper.reset {{
    transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
}}

/* 3. FLIP WRAPPER: Handles the 180deg CSS animation */
.flip-wrapper {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

.flip-wrapper.is-flipped {{
    transform: rotateY(180deg);
}}

/* 4. FACES: The actual front and back surfaces */
.card-face {{
    position: absolute;
    inset: 0;
    border-radius: 24px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    backface-visibility: hidden; /* Hides the mirrored back side */
    -webkit-backface-visibility: hidden;
    transform-style: preserve-3d; /* Crucial: Allows content to pop out in Z */
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Back face is pre-rotated 180deg */
.card-back {{
    transform: rotateY(180deg);
    background: linear-gradient(135deg, var(--surface), rgba(0,0,0,0.2));
    border-color: var(--accent);
}}

/* 5. PARALLAX CONTENT: Pushed toward the viewer */
.icon-wrapper {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    transform: translateZ(80px); /* Extreme pop out */
    box-shadow: 0 10px 30px -10px var(--accent);
}}

.title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    transform: translateZ(50px); /* Medium pop out */
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
    transform: translateZ(30px); /* Subtle pop out */
}}

.back-text {{
    font-size: 1.25rem;
    font-weight: 600;
    transform: translateZ(60px);
    color: var(--accent);
}}

/* Floating decorative elements */
.decor-circle {{
    position: absolute;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: var(--accent);
    filter: blur(80px);
    opacity: 0.15;
    z-index: -1;
    top: -50px;
    right: -50px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="decor-circle"></div>
    
    <!-- 3D Scene Container -->
    <div class="scene" id="card-scene">
        
        <!-- Tilt Wrapper handles mouse parallax -->
        <div class="tilt-wrapper" id="tilt-wrapper">
            
            <!-- Flip Wrapper handles click rotation -->
            <div class="flip-wrapper" id="flip-wrapper">
                
                <!-- FRONT FACE -->
                <div class="card-face card-front">
                    <div class="icon-wrapper">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{bg_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                            <line x1="12" y1="22.08" x2="12" y2="12"></line>
                        </svg>
                    </div>
                    <h2 class="title">{title_text}</h2>
                    <p class="body-text">{body_text}</p>
                </div>
                
                <!-- BACK FACE -->
                <div class="card-face card-back">
                    <div class="icon-wrapper" style="background: transparent; border: 2px solid var(--accent);">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <p class="back-text">backface-visibility: hidden</p>
                    <p class="body-text" style="margin-top: 10px;">The backside is revealed.</p>
                </div>

            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive 3D Parallax logic
document.addEventListener('DOMContentLoaded', () => {{
    const scene = document.getElementById('card-scene');
    const tiltWrapper = document.getElementById('tilt-wrapper');
    const flipWrapper = document.getElementById('flip-wrapper');

    // Configurable tilt limit (in degrees)
    const maxTilt = 15; 

    // Handle Parallax Tilt
    scene.addEventListener('mousemove', (e) => {{
        // Remove reset transition for instantaneous tracking
        tiltWrapper.classList.remove('reset');

        // Get bounding box of the scene
        const rect = scene.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the card
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const mouseX = e.clientX - centerX;
        const mouseY = e.clientY - centerY;

        // Convert position to a percentage (-1 to 1) and multiply by max degrees
        // Note: Moving mouse right (positive X) should rotate Y-axis positively.
        // Moving mouse down (positive Y) should rotate X-axis negatively (tilt back).
        const rotateY = (mouseX / (rect.width / 2)) * maxTilt;
        const rotateX = -(mouseY / (rect.height / 2)) * maxTilt;

        // Apply dynamic rotation to the tilt wrapper
        tiltWrapper.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
    }});

    // Reset rotation smoothly when mouse leaves
    scene.addEventListener('mouseleave', () => {{
        tiltWrapper.classList.add('reset');
        tiltWrapper.style.transform = `rotateX(0deg) rotateY(0deg)`;
    }});

    // Handle Card Flip
    scene.addEventListener('click', () => {{
        flipWrapper.classList.toggle('is-flipped');
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
