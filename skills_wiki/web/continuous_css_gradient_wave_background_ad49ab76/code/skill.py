def create_component(
    output_dir: str,
    title_text: str = "Fluid Gradient Wave",
    body_text: str = "A pure CSS animated background technique.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Continuous CSS Gradient Wave Background.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050B14" # Deep dark blue for contrast
        text_color = "#ffffff"
        text_shadow = "rgba(0, 0, 0, 0.8)"
    else:
        bg_color = "#e6f0fa" # Light ice blue
        text_color = "#111827"
        text_shadow = "rgba(255, 255, 255, 0.8)"

    # Create the repeating gradient string based on the accent color
    # Repeating 4 times to ensure smooth transitions across the 200% width
    color1 = accent_color
    color2 = bg_color
    gradient_stops = f"{color1}, {color2}, {color1}, {color2}, {color1}, {color2}, {color1}, {color2}"

    # === CSS ===
    css = f"""/* Continuous CSS Gradient Wave Background */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-shadow: {text_shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #1a1a1a; /* Outer background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.wave-container {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background-color: var(--bg-color);
}}

.wave {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 100%;
    /* 200% width allows the gradient to slide horizontally without running out of texture */
    width: 200%; 
    background: linear-gradient(to right, {gradient_stops});
    /* We use transform instead of 'left' (as seen in the tutorial) for GPU acceleration */
    animation: wave-motion 30s ease-in-out infinite;
}}

.content-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    z-index: 10;
    color: var(--text-color);
    text-shadow: 0 4px 12px var(--text-shadow);
}}

.content-overlay h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 1rem;
}}

.content-overlay p {{
    font-size: 1.25rem;
    font-weight: 300;
    opacity: 0.9;
    max-width: 600px;
}}

/* The keyframes mimic the tutorial's logic but use performant transforms */
@keyframes wave-motion {{
    0% {{
        transform: translateX(-40%);
    }}
    25% {{
        transform: translateX(-20%);
    }}
    50% {{
        transform: translateX(0%);
    }}
    75% {{
        transform: translateX(-30%);
    }}
    100% {{
        transform: translateX(-40%); /* Must match 0% for seamless loop */
    }}
}}

/* Respect user preferences for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .wave {{
        animation: none;
        transform: translateX(0);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wave-container">
        <!-- The animated background layer -->
        <div class="wave"></div>
        
        <!-- Foreground content added for practical component usage -->
        <div class="content-overlay">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Continuous CSS Gradient Wave Background
document.addEventListener('DOMContentLoaded', () => {{
    // The animation is entirely CSS-driven. 
    // This JS file is included for structure and future extensibility.
    console.log("Wave background initialized.");
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
