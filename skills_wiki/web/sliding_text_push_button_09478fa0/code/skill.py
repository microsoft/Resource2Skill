def create_component(
    output_dir: str,
    title_text: str = "Sliding Text Push Button",
    body_text: str = "Hover over the button below to see the continuous sliding text effect.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#eccf00",     # CSS hex color for accent (yellow from video)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sliding Text Push Button visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#262626"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        
    button_label = "CREATIVE"

    # === CSS ===
    css = f"""/* Sliding Text Push Button — generated component */
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
    gap: 40px;
}}

.title {{
    font-size: 2rem;
    font-weight: 600;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* === Core Visual Effect Styles === */

.sliding-button {{
    position: relative;
    display: inline-block;
    width: 200px;
    height: 60px;
    line-height: 60px; /* Vertically centers the text */
    text-align: center;
    text-transform: uppercase;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 24px;
    letter-spacing: 4px;
    color: var(--accent);
    border: 2px solid var(--accent);
    overflow: hidden; /* Crucial for masking the sliding text */
    cursor: pointer;
}}

.sliding-button span {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: transform 0.5s ease-in-out;
}}

/* Incoming text: Starts off-screen to the left */
.sliding-button span:nth-child(1) {{
    transform: translateX(-100%);
}}

/* Incoming text on hover: Slides into the center */
.sliding-button:hover span:nth-child(1) {{
    transform: translateX(0);
}}

/* Outgoing text: Starts in the center */
.sliding-button span:nth-child(2) {{
    transform: translateX(0);
}}

/* Outgoing text on hover: Slides off-screen to the right */
.sliding-button:hover span:nth-child(2) {{
    transform: translateX(100%);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- Button Component -->
        <!-- Note: aria-label is provided for screen readers, and duplicate text spans are hidden to prevent reading the word twice -->
        <a href="#" class="sliding-button" aria-label="{button_label}">
            <span aria-hidden="true">{button_label}</span>
            <span aria-hidden="true">{button_label}</span>
        </a>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sliding Text Push Button — No JS required for the core visual effect.
// The animation is handled entirely by CSS transforms and transitions.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded successfully.");
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
