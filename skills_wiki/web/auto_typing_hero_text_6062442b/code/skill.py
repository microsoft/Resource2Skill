def create_component(
    output_dir: str,
    title_text: str = "I'm a ",
    body_text: str = "Programmer, Designer, YouTuber",
    color_scheme: str = "dark",
    accent_color: str = "#fff724",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Typing Hero Text effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#020412"
        text_color = "#ffffff"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"

    # === CSS ===
    css = f"""/* Auto-Typing Hero Text — generated component */
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
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
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
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
}}

h1 {{
    color: var(--text);
    font-size: clamp(2rem, 6vw, 75px);
    font-weight: 700;
    line-height: 1.2;
    margin: 0;
}}

.auto-type {{
    color: var(--accent);
}}

/* Match the default typed.js cursor to the static text size/color */
.typed-cursor {{
    font-size: clamp(2rem, 6vw, 75px);
    color: var(--text);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-Typing Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>
            <span class="static-text">{title_text}</span><span class="auto-type"></span>
        </h1>
    </div>
    
    <!-- Load Typed.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Typing Hero Text — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    
    // Parse the comma-separated string into an array of words
    const rawStrings = "{body_text}";
    const stringsArray = rawStrings.split(',').map(s => s.trim()).filter(s => s.length > 0);
    
    // Fallback if empty
    if (stringsArray.length === 0) {{
        stringsArray.push("Something awesome");
    }}

    // Initialize Typed.js
    var typed = new Typed(".auto-type", {{
        strings: stringsArray,
        typeSpeed: 150,
        backSpeed: 150,
        loop: true,
        smartBackspace: true // Only backspace what doesn't match the previous string
    }});
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
