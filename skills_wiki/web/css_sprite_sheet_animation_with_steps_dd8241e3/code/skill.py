def create_component(
    output_dir: str,
    title_text: str = "CSS Sprite Animation",
    body_text: str = "Using background-position and steps() timing function.",
    color_scheme: str = "dark",
    accent_color: str = "#f39c12",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a CSS Sprite Sheet Animation using steps().
    Generates an inline SVG to act as the sprite sheet for self-containment.
    """
    import os
    import base64

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#1e1e1e"
    else:
        bg_color = "#f4f4f9"
        text_color = "#333333"
        surface_color = "#ffffff"

    # === Generate a Sprite Sheet (SVG) ===
    # Creating a 4-frame animation of a bouncing dot.
    # Frame size: 100x100. Total sprite width: 400x100.
    frame_w = 100
    frame_h = 100
    frames = 4
    total_w = frame_w * frames

    svg_content = f"""<svg width="{total_w}" height="{frame_h}" xmlns="http://www.w3.org/2000/svg">
      <!-- Frame 1: High -->
      <ellipse cx="50" cy="20" rx="20" ry="20" fill="{accent_color}" />
      <!-- Frame 2: Middle falling -->
      <ellipse cx="150" cy="50" rx="20" ry="20" fill="{accent_color}" />
      <!-- Frame 3: Grounded and squished -->
      <ellipse cx="250" cy="80" rx="28" ry="12" fill="{accent_color}" />
      <!-- Frame 4: Middle rising -->
      <ellipse cx="350" cy="50" rx="18" ry="22" fill="{accent_color}" />
    </svg>"""

    # Encode to base64 to use cleanly in CSS background-image
    encoded_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    sprite_data_uri = f"data:image/svg+xml;base64,{encoded_svg}"

    # === CSS ===
    css = f"""/* CSS Sprite Sheet Animation */
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
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
}}

h1 {{
    margin-bottom: 0.5rem;
    font-size: 2rem;
}}

p {{
    opacity: 0.7;
    margin-bottom: 3rem;
}}

/* Core Visual Pattern Implementation */
.sprite-animation {{
    /* 1. Viewport matches exactly ONE frame's dimensions */
    width: {frame_w}px;
    height: {frame_h}px;
    
    /* 2. Load the entire sprite sheet */
    background-image: url('{sprite_data_uri}');
    background-repeat: no-repeat;
    background-position: left top;
    
    /* Optional styling */
    border-bottom: 2px solid var(--text);
    
    /* 3. Apply animation with steps() timing function */
    /* Syntax: name duration timing-function iteration-count */
    animation: play-sprite 0.6s steps({frames}) infinite;
}}

/* 4. Shift the background to the left by the total width of the sprite */
@keyframes play-sprite {{
    100% {{
        background-position: -{total_w}px 0;
    }}
}}

/* For visual debugging/learning: show the full sprite sheet below */
.debug-view {{
    margin-top: 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    opacity: 0.5;
    transform: scale(0.8);
}}

.debug-view span {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.full-sprite {{
    width: {total_w}px;
    height: {frame_h}px;
    background-image: url('{sprite_data_uri}');
    border: 1px dashed var(--text);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        
        <!-- The animated element -->
        <div class="sprite-animation" aria-label="Animated bouncing dot" role="img"></div>
        
        <!-- Debug view to understand the technique -->
        <div class="debug-view">
            <span>Original Sprite Sheet ({frames} Frames)</span>
            <div class="full-sprite"></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// No JavaScript is required for the core CSS sprite animation technique.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded successfully. Animation is handled purely by CSS steps().");
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
