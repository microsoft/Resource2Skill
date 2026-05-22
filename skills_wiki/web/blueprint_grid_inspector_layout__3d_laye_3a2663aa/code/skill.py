def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Topography",
    body_text: str = "Hover over the grid matrix to inspect the 3D Z-index layering, explicit coordinate placements, and interactive tracking mechanics.",
    color_scheme: str = "dark",
    accent_color: str = "#00bcd4",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Blueprint Grid Inspector Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.6)"
        tracker_border = "rgba(255, 255, 255, 0.15)"
        tracker_bg = "rgba(255, 255, 255, 0.02)"
        card_1_bg = "rgba(233, 30, 99, 0.75)"
        card_3_bg = "rgba(255, 193, 7, 0.75)"
        card_4_bg = "rgba(76, 175, 80, 0.75)"
        card_5_bg = "rgba(156, 39, 176, 0.75)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        text_muted = "rgba(0, 0, 0, 0.6)"
        tracker_border = "rgba(0, 0, 0, 0.15)"
        tracker_bg = "rgba(0, 0, 0, 0.02)"
        card_1_bg = "rgba(219, 39, 119, 0.75)"
        card_3_bg = "rgba(217, 119, 6, 0.75)"
        card_4_bg = "rgba(5, 150, 105, 0.75)"
        card_5_bg = "rgba(124, 58, 237, 0.75)"

    # Generate 16 empty trackers for the background matrix
    tracker_html = '\n'.join(['                <div class="tracker"></div>'] * 16)

    css = f"""/* Blueprint Grid Inspector — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --tracker-border: {tracker_border};
    --tracker-bg: {tracker_bg};
    --accent: {accent_color};
    
    --card-1: {card_1_bg};
    --card-3: {card_3_bg};
    --card-4: {card_4_bg};
    --card-5: {card_5_bg};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-main);
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
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    padding: 40px;
}}

.header-text {{
    text-align: center;
    max-width: 600px;
    z-index: 200;
}}

.header-text h1 {{
    font-size: 2.2rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.header-text p {{
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* 3D Perspective Wrapper */
.blueprint-wrapper {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    min-height: 0;
    perspective: 1200px;
}}

/* Main Grid Container */
.css-grid-blueprint {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 16px;
    height: 100%;
    aspect-ratio: 1 / 1;
    max-height: 560px;
    max-width: 100%;
    position: relative;
    padding: 16px;
    border: 1px solid var(--tracker-border);
    border-radius: 16px;
    
    transform-style: preserve-3d;
    transform: rotateX(0) rotateY(0);
    will-change: transform;
}}

/* Ambient Backlight Glow */
.css-grid-blueprint::before {{
    content: '';
    position: absolute;
    inset: -20px;
    background: var(--accent);
    filter: blur(80px);
    opacity: 0.12;
    z-index: -1;
    transform: translateZ(-50px);
    pointer-events: none;
}}

/* Empty background matrix cells */
.tracker {{
    border: 2px dashed var(--tracker-border);
    background: var(--tracker-bg);
    border-radius: 8px;
    pointer-events: none;
    transform: translateZ(0px);
}}

/* Overlapping Forensic Cards */
.grid-card {{
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.85rem;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    
    /* 3D Physical separation */
    transform: translateZ(25px);
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
    cursor: default;
}}

.grid-card:hover {{
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}}

.item-1:hover, .item-3:hover, .item-4:hover, .item-5:hover {{
    transform: translateZ(55px) scale(1.03);
}}

.card-header {{
    font-weight: 700;
    font-size: 1.05rem;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    letter-spacing: 0.05em;
}}

.card-body {{
    line-height: 1.6;
    opacity: 0.95;
}}

/* Specific Grid Area Placements */
.item-1 {{ 
    grid-area: 1 / 1 / 3 / 3; 
    background: var(--card-1); 
}}

.item-2 {{ 
    grid-area: 2 / 2 / 4 / 4; 
    background: color-mix(in srgb, var(--accent) 85%, transparent); 
    border: 1px solid rgba(255, 255, 255, 0.6);
    z-index: 10; 
    transform: translateZ(45px); /* Higher base elevation */
}}

.item-2:hover {{
    transform: translateZ(75px) scale(1.03);
}}

.item-3 {{ 
    grid-area: 4 / 1 / 5 / 3; 
    background: var(--card-3); 
}}

.item-4 {{ 
    grid-area: 1 / 4 / 5 / 5; 
    background: var(--card-4); 
}}

.item-5 {{ 
    grid-area: 3 / 3 / 5 / 4; 
    background: var(--card-5); 
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blueprint Grid Inspector</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header-text">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="blueprint-wrapper">
            <div class="css-grid-blueprint">
{tracker_html}
                
                <!-- Overlaid Items -->
                <div class="grid-card item-1">
                    <div class="card-header">.widget-alpha</div>
                    <div class="card-body">grid-area: 1 / 1 / 3 / 3;<br>span: 2x2</div>
                </div>
                
                <div class="grid-card item-2">
                    <div class="card-header">.widget-beta (accent)</div>
                    <div class="card-body">grid-area: 2 / 2 / 4 / 4;<br>z-index: 10;<br>elevation: high</div>
                </div>
                
                <div class="grid-card item-3">
                    <div class="card-header">.widget-gamma</div>
                    <div class="card-body">grid-area: 4 / 1 / 5 / 3;</div>
                </div>
                
                <div class="grid-card item-4">
                    <div class="card-header">.widget-delta</div>
                    <div class="card-body">grid-area: 1 / 4 / 5 / 5;</div>
                </div>
                
                <div class="grid-card item-5">
                    <div class="card-header">.widget-epsilon</div>
                    <div class="card-body">grid-area: 3 / 3 / 5 / 4;</div>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Smooth 3D tilt interaction tracking mouse position
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.blueprint-wrapper');
    const grid = document.querySelector('.css-grid-blueprint');
    
    if(!wrapper || !grid) return;

    let animationFrameId;

    wrapper.addEventListener('mousemove', (e) => {
        if(animationFrameId) cancelAnimationFrame(animationFrameId);
        
        const rect = wrapper.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the wrapper
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        // Convert position to degrees (max 14 degrees of tilt)
        const rotateX = -(y / (rect.height / 2)) * 14;
        const rotateY = (x / (rect.width / 2)) * 14;
        
        animationFrameId = requestAnimationFrame(() => {
            grid.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
    });

    wrapper.addEventListener('mouseleave', () => {
        if(animationFrameId) cancelAnimationFrame(animationFrameId);
        grid.style.transform = `rotateX(0deg) rotateY(0deg)`;
        grid.style.transition = 'transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1)';
    });
    
    wrapper.addEventListener('mouseenter', () => {
        grid.style.transition = 'transform 0.1s ease-out';
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
