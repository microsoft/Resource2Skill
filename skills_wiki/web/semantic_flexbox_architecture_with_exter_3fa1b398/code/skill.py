def create_component(
    output_dir: str,
    title_text: str = "Title",
    body_text: str = "lower-section",
    color_scheme: str = "dark",
    accent_color: str = "#0000ff", # Defaulting to the blue shown at the end of the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Semantic Flexbox Architecture.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "rgb(50, 50, 50)"
        text_color = "#ffffff"
        surface_color = "#000000"
        section_bg = "#ffffff"
        section_text = "gray"
    else:
        bg_color = "#e0e0e0"
        text_color = "#333333"
        surface_color = "#ffffff"
        section_bg = "#f9f9f9"
        section_text = "#555555"

    # === CSS ===
    css = f"""/* Semantic Flexbox Architecture — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --surface-color: {surface_color};
    --section-bg: {section_bg};
    --section-text: {section_text};
    --accent: {accent_color};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    background: var(--bg-color);
    color: var(--text-color);
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}}

/* Main wrapper to enforce dimensions for standalone viewing */
.layout-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--min-height);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    background: var(--bg-color);
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}}

header {{
    background: var(--surface-color);
    padding: 20px;
}}

ul {{
    margin: 0;
    padding: 0;
    list-style-type: none;
}}

li {{
    display: inline-block;
    margin-right: 20px;
}}

a {{
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.2s ease;
}}

a:hover {{
    color: var(--accent);
}}

h1 {{
    margin: 20px 0 0 0;
    font-size: 2em;
}}

.flex-section {{
    background: var(--section-bg);
    color: var(--section-text);
    padding: 20px;
    display: flex;
    flex-direction: row;
}}

.flex-section div {{
    background: var(--accent);
    color: white;
    margin: auto;
    width: 100px;
    padding: 10px;
    text-align: center;
    font-weight: bold;
    border-radius: 2px;
}}

.lower-section {{
    padding: 20px;
    flex-grow: 1; /* Pushes footer to the bottom */
}}

footer {{
    background: var(--surface-color);
    padding: 10px 20px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Linking external stylesheet as demonstrated in tutorial -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-wrapper">
        <header>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Locations</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </nav>
            <h1>{title_text}</h1>
        </header>
        
        <section class="flex-section">
            <div>a</div>
            <div>b</div>
            <div>c</div>
        </section>
        
        <section class="lower-section">
            <p>{body_text}</p>
        </section>
        
        <footer>
            footer
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Minimal JS required as the core pattern is HTML/CSS structure
document.addEventListener('DOMContentLoaded', () => {{
    console.log("External Stylesheet and Semantic Layout loaded successfully.");
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
