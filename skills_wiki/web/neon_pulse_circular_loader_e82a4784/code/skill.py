def create_component(
    output_dir: str,
    title_text: str = "Processing Data...",
    body_text: str = "Please wait while we synthesize your results.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ff0a",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Pulse Circular Loader visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Note: This effect is specifically designed for dark backgrounds. 
    # The glow effect gets washed out on light backgrounds, but we adjust accordingly.
    if color_scheme == "dark":
        bg_color = "#040b14"
        text_color = "#ffffff"
    else:
        bg_color = "#e0e5ec"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Neon Pulse Circular Loader — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
    width: var(--width);
    height: var(--height);
}}

/* Text Styling */
.content {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
    opacity: 0.9;
}}

.body-text {{
    font-size: 0.95rem;
    font-weight: 300;
    opacity: 0.6;
}}

/* Core Loader Logic */
.loader-container {{
    position: relative;
    /* The hue-rotate animation shifts the base color across the spectrum continuously */
    animation: animateColor 10s linear infinite;
}}

.loader {{
    position: relative;
    width: 120px;
    height: 120px;
}}

/* The spans act as rotational pivots */
.loader span {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* 360deg / 20 dots = 18deg increment per dot */
    transform: rotate(calc(18deg * var(--i)));
}}

/* The actual glowing dots are attached to the corner of the rotated spans */
.loader span::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: var(--accent);
    /* Stacked box-shadows create the neon bloom */
    box-shadow: 0 0 10px var(--accent),
                0 0 20px var(--accent),
                0 0 40px var(--accent),
                0 0 60px var(--accent),
                0 0 80px var(--accent),
                0 0 100px var(--accent);
    
    /* The scale animation creates the trailing/shrinking effect */
    animation: animateScale 2s linear infinite;
    /* Staggered delay creates the circular wave */
    animation-delay: calc(0.1s * var(--i));
}}

/* Keyframes */
@keyframes animateColor {{
    0% {{
        filter: hue-rotate(0deg);
    }}
    100% {{
        filter: hue-rotate(360deg);
    }}
}}

@keyframes animateScale {{
    0% {{
        transform: scale(1);
    }}
    80%, 100% {{
        transform: scale(0);
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <div class="loader-container">
            <div class="loader" id="loader">
                <!-- Spans will be injected here by JavaScript -->
            </div>
        </div>
        
        <div class="content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Pulse Circular Loader — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader');
    const TOTAL_DOTS = 20;

    // Dynamically generate the dots to keep the DOM clean
    // and allow for easy calculation of the staggered CSS variable '--i'
    const fragment = document.createDocumentFragment();

    for (let i = 1; i <= TOTAL_DOTS; i++) {{
        const span = document.createElement('span');
        // Set the custom property inline. 
        // This is caught by the CSS to calculate rotation and delay.
        span.style.setProperty('--i', i);
        fragment.appendChild(span);
    }}

    loader.appendChild(fragment);
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
