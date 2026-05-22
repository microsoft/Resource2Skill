def create_component(
    output_dir: str,
    title_text: str = "I am Pratham",
    body_text: str = "This text uses CSS background-clip to mask a gradient to the shape of the typography.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Gradient Text Clipping visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#e0e0e0"
        # Create a dynamic secondary color for the gradient based on theme
        secondary_gradient_color = "#ff00cc"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        secondary_gradient_color = "#f43f5e"

    # === CSS ===
    css = f"""/* CSS Gradient Text Clipping — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --gradient-secondary: {secondary_gradient_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

/* Core Visual Pattern: Gradient Text */
.gradient-title {{
    font-size: clamp(3rem, 8vw, 8rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
    
    /* 1. Set the background gradient */
    background: linear-gradient(
        to right, 
        var(--accent), 
        var(--gradient-secondary), 
        var(--accent)
    );
    background-size: 200% auto;
    
    /* 2. Clip the background to the text */
    -webkit-background-clip: text;
    background-clip: text;
    
    /* 3. Make the actual text transparent so the background shows through */
    color: transparent;
    
    /* Optional: Animate the gradient for a dynamic feel */
    animation: shine 5s linear infinite;
}}

.body-text {{
    font-size: 1.125rem;
    font-weight: 400;
    max-width: 600px;
    opacity: 0.8;
    line-height: 1.6;
}}

@keyframes shine {{
    to {{
        background-position: 200% center;
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="gradient-title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS is strictly required for this CSS effect, but included for structure completeness.
    js = f"""// CSS Gradient Text Clipping Component
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded. The gradient text effect is handled entirely via CSS properties: background-clip and color: transparent.");
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
