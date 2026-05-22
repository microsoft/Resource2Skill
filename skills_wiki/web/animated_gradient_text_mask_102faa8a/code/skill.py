def create_component(
    output_dir: str,
    title_text: str = "HAPPY NEW YEAR",
    body_text: str = "",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Gradient Text Mask visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        grid_line = "rgba(255, 255, 255, 0.05)"
        fallback_text = "#ffffff"
    else:
        bg_color = "#f4f4f5"
        grid_line = "rgba(0, 0, 0, 0.05)"
        fallback_text = "#18181b"

    # Secondary colors to form a vibrant, looping gradient based on the accent
    # To ensure a smooth loop, the first and last colors must be identical.
    gradient_str = f"linear-gradient(to right, {accent_color}, #ff007a, #ffd600, #00e676, {accent_color})"

    # === CSS ===
    css = f"""/* Animated Gradient Text Mask — generated component */
:root {{
    --bg-color: {bg_color};
    --grid-line: {grid_line};
    --fallback-text: {fallback_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    /* Subtle blueprint grid pattern as seen in the video */
    background-color: var(--bg-color);
    background-image: 
        repeating-linear-gradient(to right, var(--grid-line) 0, var(--grid-line) 1px, transparent 1px, transparent 40px),
        repeating-linear-gradient(to bottom, var(--grid-line) 0, var(--grid-line) 1px, transparent 1px, transparent 40px);
    background-attachment: fixed;
    
    /* Layout */
    display: grid;
    place-content: center;
    min-height: 100vh;
    color: var(--fallback-text);
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    text-align: center;
    padding: 2rem;
}}

.animated-title {{
    /* Fluid typography that scales with the screen */
    font-size: clamp(2rem, 6vw + 1rem, 6rem);
    font-weight: 800;
    text-transform: uppercase;
    line-height: 1.2;
    letter-spacing: -0.02em;
    
    /* Default solid color for unsupported browsers */
    color: var(--fallback-text);
}}

/* Feature Query: Apply the gradient only if the browser supports clipping */
@supports ((background-clip: text) or (-webkit-background-clip: text)) {{
    .animated-title {{
        background-image: {gradient_str};
        background-size: 200% auto;
        
        /* Clip the background to the text */
        -webkit-background-clip: text;
        background-clip: text;
        
        /* Make the actual text transparent to show the background */
        color: transparent;
        
        /* Run the animation */
        animation: flowGradient 3s linear infinite;
    }}
}}

/* The looping keyframe animation */
@keyframes flowGradient {{
    0% {{
        background-position: 0% center;
    }}
    100% {{
        /* Shift by exactly the background size to loop seamlessly */
        background-position: 200% center;
    }}
}}

/* Accessibility: Pause animation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .animated-title {{
        animation: none;
        background-position: 0% center;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Text Effect Animation</title>
    <!-- Use Google Fonts for the bold Poppins typography seen in the tutorial -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The core element utilizing the gradient mask -->
        <h1 class="animated-title">{title_text}</h1>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Gradient Text Mask
// Pure CSS implementation. JS provided as placeholder for extended interactivity.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Gradient text initialized.");
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
