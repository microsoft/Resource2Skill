def create_component(
    output_dir: str,
    title_text: str = "Loading Experience",
    body_text: str = "Please wait while we prepare your workspace...",
    color_scheme: str = "dark",
    accent_color: str = "#f6a84d",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Orbital Staggered Comet Loader.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#111116" # Deep dark background
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f4f8"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Orbital Staggered Comet Loader */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
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
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.widget-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

/* Text Styling */
.text-content {{
    text-align: center;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text-color);
    opacity: 0.7;
}}

/* Loader Core Styles */
.loader {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

.circle {{
    --circle-size: 100px;
    height: var(--circle-size);
    width: var(--circle-size);
    position: relative;
}}

.dot {{
    /* Animation Math Variables */
    --total-dots: 8;
    --duration: 3000ms;
    
    /* Size calculation: starts at 15px, gets smaller as --i increases */
    --dot-decrement: calc(1px * var(--i));
    --dot-size: calc(15px - var(--dot-decrement));
    
    height: var(--dot-size);
    width: var(--dot-size);
    background-color: var(--accent-color);
    border-radius: 50%;
    
    /* Positioning */
    position: absolute;
    top: 0;
    left: calc(50% - var(--dot-size) / 2);
    
    /* Move the pivot point to the center of the parent .circle */
    transform-origin: calc(var(--dot-size) / 2) calc(var(--circle-size) / 2);
    
    /* Animation */
    animation: spin var(--duration) ease-out infinite;
    /* Positive delay causes them to stagger and trail */
    animation-delay: calc(var(--duration) / var(--total-dots) * var(--i));
}}

@keyframes spin {{
    0% {{
        transform: rotate(0deg);
    }}
    /* Pausing at 50% allows the trailing dots to catch up and merge */
    50%, 100% {{
        transform: rotate(360deg);
    }}
}}

/* Accessibility: Pause animation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .dot {{
        animation-duration: 10s;
        animation-timing-function: linear;
        animation-delay: 0s;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orbital Loader Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        
        <div class="loader" aria-label="Loading..." role="progressbar">
            <div class="circle">
                <!-- Using inline CSS variables to drive the staggering logic -->
                <div class="dot" style="--i: 0"></div>
                <div class="dot" style="--i: 1"></div>
                <div class="dot" style="--i: 2"></div>
                <div class="dot" style="--i: 3"></div>
                <div class="dot" style="--i: 4"></div>
                <div class="dot" style="--i: 5"></div>
                <div class="dot" style="--i: 6"></div>
                <div class="dot" style="--i: 7"></div>
            </div>
        </div>

        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS implementation. No JavaScript required for this visual mechanism.
// You could dynamically generate the dots here if you wanted a configurable number of dots.
console.log("Orbital loader initialized.");
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
