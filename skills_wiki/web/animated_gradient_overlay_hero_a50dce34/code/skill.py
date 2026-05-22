def create_component(
    output_dir: str,
    title_text: str = "Hero Image + CSS Gradient",
    body_text: str = "- Gradient Animation -",
    color_scheme: str = "dark",        
    accent_color: str = "#34dbd8",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Gradient Overlay Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper function to convert hex color to rgba with specific opacity
    def hex_to_rgba(hex_val, alpha):
        hex_val = hex_val.lstrip('#')
        if len(hex_val) == 3:
            hex_val = ''.join([c*2 for c in hex_val])
        if len(hex_val) == 6:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        return f"rgba(0, 0, 0, {alpha})"

    # Configure theme
    if color_scheme == "dark":
        text_color = "#ffffff"
        opacity = "0.7"
        bg_image = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070&auto=format&fit=crop"
    else:
        text_color = "#111827"
        opacity = "0.55"
        bg_image = "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=80&w=2041&auto=format&fit=crop"

    # Define the 5 color stops. We swap the final tutorial color for the user's accent_color.
    c1 = hex_to_rgba("#ffafbd", opacity)
    c2 = hex_to_rgba("#64d8f3", opacity)
    c3 = hex_to_rgba("#eaeac6", opacity)
    c4 = hex_to_rgba("#f592b0", opacity)
    c5 = hex_to_rgba(accent_color, opacity)

    # === CSS ===
    css = f"""/* Animated Gradient Overlay Hero */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #1a1a1a;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, sans-serif;
}}

.container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

.hero {{
    width: 100%;
    height: 100%;
    position: relative;
    /* The core technique: stacking a 1000% wide linear gradient over a static background image */
    background: 
        linear-gradient(45deg, {c1}, {c2}, {c3}, {c4}, {c5}) 0 0 / 1000% no-repeat,
        url("{bg_image}") center center / cover no-repeat;
    animation: gradient-pan 40s ease infinite;
}}

.hero-content {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: {text_color};
    width: 90%;
}}

.hero-title {{
    font-weight: 600;
    font-size: clamp(40px, 6vw, 72px);
    line-height: 1.1;
    letter-spacing: -0.02em;
    text-shadow: 0 4px 24px rgba(0,0,0,0.1);
}}

.hero-subtitle {{
    display: block;
    margin-top: 0.8em;
    font-size: clamp(20px, 3vw, 40px);
    font-weight: 300;
    opacity: 0.95;
}}

/* 
  Keyframes animate the gradient's background-position.
  Note the second value pair (center center) keeps the image layer stationary. 
*/
@keyframes gradient-pan {{
    0% {{ background-position: 0% 30%, center center; }}
    50% {{ background-position: 100% 70%, center center; }}
    100% {{ background-position: 0% 30%, center center; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <span class="hero-subtitle">{body_text}</span>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Gradient Overlay Hero
// This effect is purely CSS-driven. No JavaScript required.
console.log("Component loaded successfully.");
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
