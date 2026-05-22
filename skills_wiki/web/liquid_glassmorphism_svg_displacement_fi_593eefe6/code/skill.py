def create_component(
    output_dir: str,
    title_text: str = "Liquid Glass",
    body_text: str = "Drag this card around to see the background refract and distort through the SVG displacement filter.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Liquid Glassmorphism visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#050914"
        text_color = "#ffffff"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.1)"
        blob_1 = "#ff007f"
        blob_2 = accent_color
        blob_3 = "#7000ff"
    else:
        bg_color = "#e5e9f0"
        text_color = "#1a1a2e"
        card_bg = "rgba(255, 255, 255, 0.4)"
        card_border = "rgba(255, 255, 255, 0.6)"
        blob_1 = "#ff4d94"
        blob_2 = accent_color
        blob_3 = "#9b4dff"

    # === CSS ===
    css = f"""/* Liquid Glassmorphism */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}}

/* Setup a rich, complex background to make refraction obvious */
.bg-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
    background: 
        radial-gradient(circle at 15% 50%, rgba(255, 255, 255, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.04) 0%, transparent 50%);
}}

.blob {{
    position: absolute;
    filter: blur(80px);
    border-radius: 50%;
    opacity: 0.7;
    animation: float 20s infinite alternate ease-in-out;
}}

.blob:nth-child(1) {{
    top: 10%;
    left: 20%;
    width: 400px;
    height: 400px;
    background: {blob_1};
    animation-delay: 0s;
}}

.blob:nth-child(2) {{
    bottom: 10%;
    right: 15%;
    width: 500px;
    height: 500px;
    background: {blob_2};
    animation-delay: -5s;
}}

.blob:nth-child(3) {{
    top: 40%;
    left: 60%;
    width: 350px;
    height: 350px;
    background: {blob_3};
    animation-delay: -10s;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    33% {{ transform: translate(30px, -50px) scale(1.1); }}
    66% {{ transform: translate(-40px, 20px) scale(0.9); }}
    100% {{ transform: translate(0, 0) scale(1); }}
}}

/* 
 * The Core Liquid Glass Card
 * Z-index ensures it sits above the background.
 */
.card-container {{
    position: absolute;
    z-index: 10;
    /* Center it initially */
    top: 50%;
    left: 50%;
    margin-top: -150px; /* Half of height */
    margin-left: -200px; /* Half of width */
    
    width: 400px;
    height: 300px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 16px;
    
    border-radius: 32px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: 
        0 24px 64px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    
    /* THE LIQUID MAGIC: Combines standard glass blur with SVG displacement map */
    -webkit-backdrop-filter: brightness(1.15) blur(6px) url(#displacementFilter);
    backdrop-filter: brightness(1.15) blur(6px) url(#displacementFilter);
    
    cursor: grab;
    user-select: none;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}}

.card-container:active {{
    cursor: grabbing;
    box-shadow: 
        0 32px 80px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.3);
}}

.card-title {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
    pointer-events: none;
}}

.card-body {{
    font-size: 16px;
    line-height: 1.6;
    font-weight: 300;
    opacity: 0.9;
    pointer-events: none;
}}

.dock {{
    display: flex;
    gap: 16px;
    margin-top: 16px;
    pointer-events: none;
}}

.dock-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- SVG Filter Definition (Hidden) -->
    <svg style="display: none;">
        <filter id="displacementFilter" x="-20%" y="-20%" width="140%" height="140%">
            <!-- Generate a fluid noise map -->
            <feTurbulence 
                type="turbulence" 
                baseFrequency="0.012" 
                numOctaves="2" 
                result="turbulence" 
            />
            <!-- Displace the background (SourceGraphic) using the noise map -->
            <feDisplacementMap 
                in="SourceGraphic" 
                in2="turbulence" 
                scale="100" 
                xChannelSelector="R" 
                yChannelSelector="G" 
            />
        </filter>
    </svg>

    <!-- Rich visual background to showcase refraction -->
    <div class="bg-container">
        <div class="blob"></div>
        <div class="blob"></div>
        <div class="blob"></div>
    </div>

    <!-- Draggable Liquid Glass Component -->
    <div class="card-container" id="liquidCard">
        <h1 class="card-title">{title_text}</h1>
        <p class="card-body">{body_text}</p>
        
        <div class="dock">
            <div class="dock-icon"></div>
            <div class="dock-icon"></div>
            <div class="dock-icon"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Liquid Glass Interaction - Drag Logic
document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('liquidCard');
    
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    
    // We use transform translate to move the card smoothly
    let currentTranslateX = 0;
    let currentTranslateY = 0;
    
    // Store the transform values prior to the current drag
    let previousTranslateX = 0;
    let previousTranslateY = 0;

    card.addEventListener('pointerdown', (e) => {
        isDragging = true;
        
        // Capture initial pointer position
        startX = e.clientX;
        startY = e.clientY;
        
        // Lock pointer to card to prevent losing drag on fast movements
        card.setPointerCapture(e.pointerId);
    });

    window.addEventListener('pointermove', (e) => {
        if (!isDragging) return;
        
        // Calculate delta
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        // Apply delta to previous position
        currentTranslateX = previousTranslateX + deltaX;
        currentTranslateY = previousTranslateY + deltaY;
        
        // Apply transform via requestAnimationFrame for buttery smooth movement
        requestAnimationFrame(() => {
            card.style.transform = `translate(${currentTranslateX}px, ${currentTranslateY}px)`;
        });
    });

    window.addEventListener('pointerup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        
        // Save the current position as the new starting point for the next drag
        previousTranslateX = currentTranslateX;
        previousTranslateY = currentTranslateY;
        
        // Release capture
        if (card.hasPointerCapture(e.pointerId)) {
            card.releasePointerCapture(e.pointerId);
        }
    });
});
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
