def create_component(
    output_dir: str,
    title_text: str = "My Gradient Text",
    body_text: str = "Pure CSS gradient text clipping.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Gradient Text Fill visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        secondary_gradient_color = kwargs.get("secondary_color", "#ff007f") # Default to vivid pink/magenta
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        secondary_gradient_color = kwargs.get("secondary_color", "#8a2be2") # Default to deep purple

    # === CSS ===
    css = f"""/* CSS Gradient Text Fill — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --secondary: {secondary_gradient_color};
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

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.text-container {{
    /* Using fit-content ensures the gradient wraps tightly around the text */
    width: fit-content;
    display: block;
    margin-bottom: 1rem;
}}

.gradient-color-text {{
    font-size: clamp(4rem, 10vw, 150px);
    font-weight: 800;
    line-height: 1.1;
    text-align: center;
    
    /* 1. Set the background gradient */
    background: linear-gradient(to left, var(--secondary), var(--accent));
    
    /* 2. Make the text transparent */
    color: transparent;
    
    /* 3. Clip the background to the text geometry */
    -webkit-background-clip: text;
    background-clip: text;
}}

.body-text {{
    font-size: 1.25rem;
    color: var(--text);
    opacity: 0.8;
    max-width: 600px;
    font-weight: 400;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Text Container mimicking the tutorial structure -->
        <div class="text-container">
            <span class="gradient-color-text">{title_text}</span>
        </div>
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS required for the core visual effect, but we include an empty init block 
    # to maintain structure and allow future extensibility (e.g., dynamic gradient shifting on mousemove).
    js = f"""// CSS Gradient Text Fill — static component, no JS required.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Gradient text component loaded.");
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
