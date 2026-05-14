def create_component(
    output_dir: str,
    title_text: str = "3D Transform Engine",
    body_text: str = "Hover over this component to experience hardware-accelerated CSS 3D translations, complex rotations, and scaling across a projected perspective space.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Interactive Hover Card visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#e2e8f0"
        surface_color = "linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.6))"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow_idle = "0 10px 30px rgba(0, 0, 0, 0.4)"
        shadow_hover = f"-20px 40px 60px rgba(0, 0, 0, 0.7), 0 0 40px {accent_color}40"
    else:
        bg_color = "#f1f5f9"
        text_color = "#1e293b"
        surface_color = "linear-gradient(145deg, rgba(255, 255, 255, 1), rgba(241, 245, 249, 0.9))"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow_idle = "0 10px 30px rgba(0, 0, 0, 0.05)"
        shadow_hover = f"-20px 40px 60px rgba(0, 0, 0, 0.15), 0 0 30px {accent_color}30"

    # === CSS ===
    css = f"""/* 3D Interactive Hover Card — generated component */
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
    --border: {border_color};
    --shadow-idle: {shadow_idle};
    --shadow-hover: {shadow_hover};
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
}}

.scene-container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
    /* Optional global perspective: perspective: 1200px; */
}}

/* The 3D element */
.card-3d {{
    width: 340px;
    height: 460px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: var(--shadow-idle);
    backdrop-filter: blur(10px);
    
    /* 3D Setup */
    /* Preserve 3D allows nested elements to have their own Z depth */
    transform-style: preserve-3d;
    
    /* Base Transform State */
    transform: perspective(1000px) translate3d(0, 0, 0) rotate3d(0, 0, 0, 0) scale3d(1, 1, 1);
    
    /* Smooth physical easing */
    transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1), 
                box-shadow 0.6s cubic-bezier(0.23, 1, 0.32, 1),
                border-color 0.6s ease;
}}

.card-3d:hover {{
    /* 
       The core tutorial skill: combining 3D functions
       1. perspective(1000px): establishes the vanishing point for this element
       2. translate3d(0, -20px, 40px): move up and towards the viewer
       3. rotate3d(1, -0.6, 0.2, 18deg): rotate on a custom diagonal axis
       4. scale3d(1.03, 1.03, 1.03): slight overall enlargement
    */
    transform: perspective(1000px) 
               translate3d(0, -20px, 40px) 
               rotate3d(1, -0.6, 0.2, 18deg) 
               scale3d(1.03, 1.03, 1.03);
               
    box-shadow: var(--shadow-hover);
    border-color: var(--accent);
}}

/* Nested depths for parallax effect */
.card-content {{
    /* Pushes the text content OUT of the flat surface of the card */
    transform: translateZ(60px);
    transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}}

.card-icon {{
    width: 60px;
    height: 60px;
    border-radius: 16px;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: auto;
    
    /* Extreme pop out for the icon */
    transform: translateZ(90px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

.card-icon svg {{
    width: 30px;
    height: 30px;
    fill: #ffffff;
}}

.title {{
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 40px;
    margin-bottom: 16px;
    color: var(--text);
}}

.body-text {{
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.75;
    font-weight: 400;
}}

/* Interactive light reflection (optional flair) */
.card-3d::after {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(105deg, transparent 20%, rgba(255,255,255,0.1) 25%, transparent 30%);
    opacity: 0;
    transition: opacity 0.6s ease;
    /* Keeps reflection flat on the card surface */
    transform: translateZ(1px); 
    pointer-events: none;
}}

.card-3d:hover::after {{
    opacity: 1;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Transforms Showcase</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scene-container">
        
        <!-- Hover over this card to trigger 3D transforms -->
        <div class="card-3d">
            
            <div class="card-icon">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 16.5c0 .38-.21.71-.53.88l-7.9 4.44c-.16.12-.36.18-.57.18-.21 0-.41-.06-.57-.18l-7.9-4.44A.991.991 0 0 1 3 16.5v-9c0-.38.21-.71.53-.88l7.9-4.44c.16-.12.36-.18.57-.18.21 0 .41.06.57.18l7.9 4.44c.32.17.53.5.53.88v9M12 4.15L6.04 7.5 12 10.85l5.96-3.35L12 4.15M5 15.91l6 3.38v-6.71L5 9.19v6.72m14 0v-6.72l-6 3.39v6.71l6-3.38z"/>
                </svg>
            </div>

            <div class="card-content">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
            
        </div>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// 3D Transform Component
// The core effect is handled by CSS :hover and transform properties.
// JavaScript can be used here if you wanted the 3D rotation to track the mouse coordinates (mousemove),
// but to stay true to the pure CSS tutorial, we maintain the CSS implementation.

document.addEventListener('DOMContentLoaded', () => {
    console.log("3D Card Loaded. Hover the card to trigger the transform.");
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
