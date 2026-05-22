def create_component(
    output_dir: str,
    title_text: str = "ANIMATED GRADIENT",
    body_text: str = "BACKGROUND",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Gradient Background effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    # Using the exact signature tutorial colors for the dark (default) scheme
    if color_scheme == "dark":
        bg_color = "#000000"
        c1, c2, c3, c4 = "#a1ffce", "#3494e6", "#ec6ead", "#89253e"
    else:
        # A lighter, pastel variation for light scheme requests
        bg_color = "#ffffff"
        # Overriding default white accent for readability on light schemes
        if accent_color == "#ffffff":
            accent_color = "#111111"
        c1, c2, c3, c4 = "#fbc2eb", "#a6c1ee", "#fccb90", "#d57eeb"

    # === CSS ===
    css = f"""/* Animated Gradient Background — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-page: {bg_color};
    --accent: {accent_color};
    --c1: {c1};
    --c2: {c2};
    --c3: {c3};
    --c4: {c4};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background: var(--bg-page);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* The main animating component */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    
    /* Core Gradient Technique */
    background: linear-gradient(45deg, var(--c1), var(--c2), var(--c3), var(--c4));
    background-size: 800% 800%;
    animation: gradientMove 10s ease infinite;
    
    /* Centering the content */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

/* The rigid structural frame */
.headline {{
    border: 3px solid var(--accent);
    padding: 30px 40px;
    text-align: center;
    user-select: none;
    max-width: 90%;
}}

/* Bold graphical text */
.title {{
    font-weight: 700;
    font-size: clamp(2.5rem, 6vw, 4.8rem);
    color: var(--accent);
    letter-spacing: -0.05em;
    line-height: 1.1;
    text-transform: uppercase;
}}

.subtitle {{
    font-weight: 400;
    font-size: clamp(1rem, 2.5vw, 1.8rem);
    color: var(--accent);
    margin-top: 15px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}

/* Panning animation keyframes */
@keyframes gradientMove {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="headline">
            <h1 class="title">{title_text}</h1>
            {f'<p class="subtitle">{body_text}</p>' if body_text else ''}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Gradient Background
document.addEventListener('DOMContentLoaded', () => {{
    // The core effect is completely CSS-driven.
    // JS placeholder for structural completeness.
    console.log('Gradient animation initialized successfully.');
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
