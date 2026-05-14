def create_component(
    output_dir: str,
    title_text: str = "Hello World!",
    body_text: str = "",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#ff00f2",      # Starting color of the gradient
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Gradient Text Reveal visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"

    # Secondary colors for the gradient to match the tutorial's vibrant aesthetic
    gradient_color_2 = "#00ecff"
    gradient_color_3 = "#ff4000"

    # === CSS ===
    css = f"""/* CSS Gradient Text Reveal — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --fallback-text: {text_color};
    --accent-1: {accent_color};
    --accent-2: {gradient_color_2};
    --accent-3: {gradient_color_3};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: Arial, Helvetica, sans-serif;
    background-color: var(--bg-color);
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

.gradient-title {{
    font-size: clamp(3rem, 8vw, 8rem); /* Responsive sizing, maxing around the 6rem mark */
    font-weight: bolder;
    margin: 0;
    
    /* Fallback color if background-clip is not supported */
    color: var(--fallback-text);
    
    /* The Core Effect */
    background: linear-gradient(
        247deg, 
        var(--accent-1), 
        var(--accent-2), 
        var(--accent-3)
    );
    
    /* Cross-browser background clipping */
    -webkit-background-clip: text;
    background-clip: text;
    
    /* Make text transparent to show background */
    -webkit-text-fill-color: transparent; /* better support in webkit than just color: transparent */
    color: transparent; 
}}

/* Optional body text styling if provided */
.body-text {{
    margin-top: 1rem;
    font-size: 1.5rem;
    color: var(--fallback-text);
    opacity: 0.8;
}}
"""

    # === HTML ===
    html_body_block = f'\n        <p class="body-text">{body_text}</p>' if body_text else ""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div>
            <h1 class="gradient-title">{title_text}</h1>{html_body_block}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS required for this purely visual CSS effect, but included for structure
    js = f"""// CSS Gradient Text Reveal — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // This effect is purely CSS-driven.
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
