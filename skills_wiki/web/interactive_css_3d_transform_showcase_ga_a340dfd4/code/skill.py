def create_component(
    output_dir: str,
    title_text: str = "CSS 3D Transforms",
    body_text: str = "Hover over each card to visualize different spatial transformations across the X, Y, and Z axes.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4ade80",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS 3D Transform Showcase.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
        card_border = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.1)"
        shadow = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* CSS 3D Transforms Showcase */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent-color: {accent_color};
    --shadow: {shadow};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.showcase-container {{
    width: 100%;
    max-width: var(--comp-width);
    text-align: center;
}}

.header {{
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--accent-color);
}}

.header p {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 1rem;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 6px var(--shadow);
    cursor: crosshair;
    
    /* 
       Crucial for a polished effect:
       Smooth transition for the transform property.
    */
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s ease;
    
    /* To ensure 3D children behave if we had them, though not strictly needed here */
    transform-style: preserve-3d;
}}

.card:hover {{
    box-shadow: 0 20px 25px -5px var(--shadow), 0 0 15px rgba(255,255,255,0.05);
    border-color: var(--accent-color);
    color: var(--accent-color);
}}

/* --- 3D TRANSFORM RULES --- */

/* Rotations */
.rotate-x:hover {{
    /* perspective() gives depth to the 3D rotation */
    transform: perspective(600px) rotateX(45deg);
}}

.rotate-y:hover {{
    transform: perspective(600px) rotateY(45deg);
}}

.rotate-z:hover {{
    /* Z rotation is identical to 2D rotation */
    transform: rotateZ(45deg); 
}}

/* Translations */
.translate-x:hover {{
    transform: translateX(40px);
}}

.translate-y:hover {{
    transform: translateY(-40px);
}}

.translate-z:hover {{
    /* TranslateZ requires perspective to appear as scaling/moving closer */
    transform: perspective(600px) translateZ(150px);
}}

/* Scaling */
.scale-x:hover {{
    transform: scaleX(1.3);
}}

.scale-y:hover {{
    transform: scaleY(1.3);
}}

.scale-z:hover {{
    /* 
       Scaling on Z alone does nothing to a flat 2D plane. 
       We must rotate it first to expose the Z-depth, then scale that depth.
       The tutorial uses a high scaleZ to make the effect obvious.
    */
    transform: perspective(600px) rotateY(45deg) scaleZ(4);
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
    <div class="showcase-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="grid">
            <div class="card rotate-x">rotateX(45deg)</div>
            <div class="card rotate-y">rotateY(45deg)</div>
            <div class="card rotate-z">rotateZ(45deg)</div>
            
            <div class="card translate-x">translateX(40px)</div>
            <div class="card translate-y">translateY(-40px)</div>
            <div class="card translate-z">translateZ(150px)</div>
            
            <div class="card scale-x">scaleX(1.3)</div>
            <div class="card scale-y">scaleY(1.3)</div>
            <div class="card scale-z">scaleZ(4) + rotateY</div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// No JavaScript is required for pure CSS hover transforms.
// The visual effects are entirely handled by CSS :hover pseudo-classes 
// and the transform/transition properties for maximum performance.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("3D Transform Gallery Loaded. Hover over cards to interact.");
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
