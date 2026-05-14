def create_component(
    output_dir: str,
    title_text: str = "NATURE",
    body_text: str = "Explore the wild, one pixel at a time.",
    color_scheme: str = "light",       
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Text Clipping Mask visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Custom parameter for the background image, defaulting to a lush forest scene similar to the video
    bg_image_url = kwargs.get("bg_image_url", "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80")

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Animated Text Clipping Mask — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

/* The Core Text Clipping Effect */
.mask-text {{
    /* Typography Setup for maximum mask area */
    font-size: clamp(4rem, 15vw, 12rem);
    font-weight: 900;
    text-transform: uppercase;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    
    /* Background Setup */
    background-image: url('{bg_image_url}');
    /* Make background larger than the text to allow for panning */
    background-size: 200% auto; 
    background-repeat: repeat;
    background-position: 0% center;
    
    /* Clipping properties */
    -webkit-background-clip: text;
    background-clip: text;
    
    /* Make the text transparent to reveal the background */
    color: transparent;
    -webkit-text-fill-color: transparent;
    
    /* Animation */
    animation: panBackground 20s linear infinite;
}}

.body-text {{
    font-size: clamp(1rem, 2vw, 1.5rem);
    color: var(--text-color);
    font-weight: 500;
    opacity: 0.8;
    max-width: 600px;
}}

/* Background Panning Keyframes */
@keyframes panBackground {{
    0% {{
        background-position: 0% 50%;
    }}
    100% {{
        /* Moves the background to create a continuous panning effect */
        background-position: 200% 50%;
    }}
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .container {{
        min-height: auto;
        padding: 4rem 1rem;
    }}
    
    .mask-text {{
        background-size: 300% auto;
        animation-duration: 15s;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Mask Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Masked Text Element -->
        <h1 class="mask-text">{title_text}</h1>
        
        <!-- Supporting Subtitle -->
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Text Clipping Mask — No JS required for the core visual effect.
// The animation and masking are handled entirely via CSS for optimal performance.

document.addEventListener('DOMContentLoaded', () => {{
    console.log('Text Clipping Component Initialized.');
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
