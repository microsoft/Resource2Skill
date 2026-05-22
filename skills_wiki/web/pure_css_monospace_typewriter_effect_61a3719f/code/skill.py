def create_component(
    output_dir: str,
    title_text: str = "Hello, I am a CSS Typewriter.",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#00ffcc",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Monospace Typewriter Effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Calculate exact character count for the steps() function and width
    char_count = len(title_text)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#f0f0f0"
    else:
        bg_color = "#ffffff"
        text_color = "#111111"

    # === CSS ===
    css = f"""/* Pure CSS Typewriter Effect */
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
    --char-count: {char_count};
}}

body {{
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    font-family: system-ui, -apple-system, sans-serif;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.typewriter-text {{
    /* Crucial Typography settings */
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: clamp(1.5rem, 4vw, 3rem);
    font-weight: 500;
    
    /* Layout constraints for the effect */
    white-space: nowrap;
    overflow: hidden;
    
    /* The Caret/Cursor */
    border-right: 4px solid var(--accent);
    padding-right: 4px; /* Slight breathing room for the cursor */
    
    /* 
       Animations:
       1. typist: duration 10s, uses steps(char_count) for blocky typing
       2. caret: duration 0.75s, uses step-end for instant flash
    */
    animation: 
        typist 10s steps(var(--char-count)) infinite,
        caret 0.75s step-end infinite;
}}

/* Typing, Pausing, and Deleting Sequence */
@keyframes typist {{
    0%   {{ width: 0ch; }}
    30%  {{ width: calc(var(--char-count) * 1ch); }} /* Finished typing */
    80%  {{ width: calc(var(--char-count) * 1ch); }} /* Long pause to read */
    90%  {{ width: 0ch; }} /* Fast delete */
    100% {{ width: 0ch; }} /* Pause before restart */
}}

/* Blinking Cursor Sequence */
@keyframes caret {{
    0%, 100% {{ border-color: transparent; }}
    50%      {{ border-color: var(--accent); }}
}}

/* Accessibility: respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .typewriter-text {{
        animation: none;
        width: auto;
        border-right: none;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typewriter Effect</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The character count is dynamically accounted for in the CSS -->
        <h1 class="typewriter-text">{title_text}</h1>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS required for the core effect, but included for structure.
    js = """// Pure CSS effect - no JavaScript required for core functionality.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Typewriter initialized via CSS.");
});
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
