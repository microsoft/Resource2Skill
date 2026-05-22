def create_component(
    output_dir: str,
    title_text: str = "Gradient Stroke",
    body_text: str = "A beautiful and scalable technique for gradient text outlines using CSS background-clip and text-stroke.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Gradient Text Stroke visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        accent_secondary = "#ff007f" # Vibrant pink
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        accent_secondary = "#ff007f"

    # === CSS ===
    css = f"""/* Gradient Text Stroke Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --accent-secondary: {accent_secondary};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    /* Using Raleway as recommended in the tutorial to avoid stroke artifacts */
    font-family: 'Raleway', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: calc(var(--height) * 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 4rem;
}}

.headline-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

/* Base properties for the text */
.stroke-text {{
    font-size: clamp(3rem, 8vw, 7rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: 0.02em;
    /* Fallback color for unsupported browsers */
    color: var(--text); 
}}

/* 
 * Method 1: Hollow Gradient Stroke 
 * The fill matches the background, making it look transparent.
 */
.stroke-hollow {{
    /* 1. Define gradient background spanning the text footprint */
    background-image: linear-gradient(
        135deg, 
        var(--accent) 0%, 
        var(--accent-secondary) 50%, 
        var(--accent) 100%
    );
    background-size: 200% auto;
    
    /* 2. Clip background to text (which includes the stroke area footprint) */
    -webkit-background-clip: text;
    background-clip: text;
    
    /* 3. Create transparent stroke so the background gradient shines through.
          Note: An 8px stroke expands 4px inside the letter shape and 4px outside. */
    -webkit-text-stroke: 8px transparent;
    
    /* 4. Mask the interior text with the page background color.
          This covers the inside 4px of the stroke, leaving a crisp 4px outer gradient. */
    -webkit-text-fill-color: var(--bg);
    
    animation: gradientFlow 4s linear infinite;
}}

/* 
 * Method 2: Solid Fill Gradient Stroke 
 * The fill is a solid contrasting color.
 */
.stroke-filled {{
    background-image: radial-gradient(
        circle at top left, 
        var(--accent-secondary), 
        var(--accent)
    );
    -webkit-background-clip: text;
    background-clip: text;
    
    -webkit-text-stroke: 6px transparent;
    
    /* Mask the interior with the standard text color */
    -webkit-text-fill-color: var(--text);
}}

.description {{
    font-family: system-ui, -apple-system, sans-serif;
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 500;
    max-width: 600px;
    opacity: 0.8;
    line-height: 1.6;
    margin: 0 auto;
}}

@keyframes gradientFlow {{
    0% {{ background-position: 0% center; }}
    100% {{ background-position: 200% center; }}
}}

@media (max-width: 768px) {{
    .stroke-hollow {{ -webkit-text-stroke: 4px transparent; }}
    .stroke-filled {{ -webkit-text-stroke: 3px transparent; }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- Using Raleway font to ensure no spiky artifacts on stroke path generation -->
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="headline-wrapper">
            <h1 class="stroke-text stroke-hollow">Linear Gradient<br>Stroke Effect</h1>
        </div>
        
        <div class="headline-wrapper">
            <h1 class="stroke-text stroke-filled">Radial Gradient<br>Stroke Effect</h1>
        </div>
        
        <p class="description">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// The gradient text stroke is entirely CSS-driven.
// JS is included for potential future interactivity hooks (e.g., mouse-tracking radial gradients).

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Gradient Stroke component initialized.");
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
