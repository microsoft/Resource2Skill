def create_component(
    output_dir: str,
    title_text: str = "Liquid Glass",
    body_text: str = "Drag this card around to see the background refract through the simulated liquid displacement map.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        text_color = "#ffffff"
        border_color = "rgba(255, 255, 255, 0.25)"
        glass_bg = "rgba(255, 255, 255, 0.05)"
    else:
        text_color = "#111111"
        border_color = "rgba(255, 255, 255, 0.6)"
        glass_bg = "rgba(255, 255, 255, 0.25)"

    css = f"""/* Liquid Glass Displacement — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text: {text_color};
    --accent: {accent_color};
    --border: {border_color};
    --glass-bg: {glass_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Create a vivid, complex background so the displacement is obvious */
    background-color: #0d111c;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(255, 0, 128, 0.6), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(0, 191, 255, 0.6), transparent 25%),
        radial-gradient(circle at 50% 80%, rgba(255, 191, 0, 0.6), transparent 25%),
        linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    border-radius: 20px;
    background: inherit;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Landscape/Imagery Layer inside container to refract */
.scenery {{
    position: absolute;
    inset: 0;
    background: 
        repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 40px, transparent 40px, transparent 80px),
        repeating-linear-gradient(-45deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 40px, transparent 40px, transparent 80px);
    z-index: 1;
}}

.glass-card {{
    position: absolute;
    z-index: 10;
    width: 380px;
    padding: 40px 30px;
    border-radius: 28px;
    background: var(--glass-bg);
    border: 1px solid var(--border);
    border-top: 1px solid rgba(255, 255, 255, 0.5);
    border-left: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 
        0 15px 35px rgba(0, 0, 0, 0.2),
        inset 0 0 0 1px rgba(255, 255, 255, 0.05);
    
    /* THE MAGIC: Applying the SVG Displacement Filter + Standard Blur */
    backdrop-filter: url(#liquidFilter) blur(3px) brightness(1.15);
    -webkit-backdrop-filter: url(#liquidFilter) blur(3px) brightness(1.15);
    
    cursor: grab;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    transition: box-shadow 0.2s ease, transform 0.1s ease-out;
}}

.glass-card:active {{
    cursor: grabbing;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.3);
}}

/* Content Styling */
.header {{
    text-align: center;
    pointer-events: none;
}}

h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}}

p {{
    font-size: 0.95rem;
    font-weight: 300;
    opacity: 0.9;
    line-height: 1.5;
    text-shadow: 0 1px 5px rgba(0,0,0,0.3);
}}

.icon-dock {{
    display: flex;
    gap: 16px;
    margin-top: 10px;
    pointer-events: none;
}}

.icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), #ff007f);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}

.icon:nth-child(2) {{ background: linear-gradient(135deg, #00c6ff, #0072ff); }}
.icon:nth-child(3) {{ background: linear-gradient(135deg, #f7971e, #ffd200); }}

/* Background decorative circles */
.circle {{
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    z-index: 0;
}}
.circle-1 {{ width: 300px; height: 300px; background: #ff007f; top: 10%; left: 20%; }}
.circle-2 {{ width: 400px; height: 400px; background: #00bfff; bottom: 10%; right: 15%; }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- SVG Filters Definition -->
    <svg style="position: absolute; width: 0; height: 0; pointer-events: none;">
        <defs>
            <filter id="liquidFilter" x="-20%" y="-20%" width="140%" height="140%">
                <!-- Generates a procedural noise texture resembling liquid or ice -->
                <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="3" result="noise" />
                <!-- Maps the noise texture to distort the pixels of the source graphic (the backdrop) -->
                <!-- Scale controls the intensity of the liquid distortion -->
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="40" xChannelSelector="R" yChannelSelector="G" />
            </filter>
        </defs>
    </svg>

    <div class="app-container">
        <!-- Background elements to refract -->
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="scenery"></div>

        <!-- The Liquid Glass Card -->
        <div class="glass-card" id="draggable-card">
            <div class="header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            
            <div class="icon-dock">
                <div class="icon">G</div>
                <div class="icon">W</div>
                <div class="icon">A</div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Liquid Glass — Draggable Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.getElementById('draggable-card');
    const container = document.querySelector('.app-container');
    
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    // Initial centered transform state
    let currentTranslateX = 0;
    let currentTranslateY = 0;

    // Capture mouse down
    card.addEventListener('mousedown', (e) => {{
        isDragging = true;
        // Get the starting mouse position
        startX = e.clientX;
        startY = e.clientY;
        
        // Disable transition during drag for 1:1 responsiveness
        card.style.transition = 'none';
        
        // Prevent text selection while dragging
        e.preventDefault();
    }});

    // Handle mouse move across the document
    document.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        
        // Calculate how far the mouse has moved
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        
        // Update the current translation values
        const newTranslateX = currentTranslateX + dx;
        const newTranslateY = currentTranslateY + dy;
        
        // Apply transform. 
        // As it moves, the CSS backdrop-filter automatically re-calculates the SVG displacement!
        card.style.transform = `translate(${{newTranslateX}}px, ${{newTranslateY}}px)`;
    }});

    // Handle mouse up
    document.addEventListener('mouseup', (e) => {{
        if (!isDragging) return;
        isDragging = false;
        
        // Save the accumulated translation for the next drag
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        currentTranslateX += dx;
        currentTranslateY += dy;
        
        // Re-enable transition for smooth hover/active state animations
        card.style.transition = 'box-shadow 0.2s ease, transform 0.1s ease-out';
    }});
}});
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
