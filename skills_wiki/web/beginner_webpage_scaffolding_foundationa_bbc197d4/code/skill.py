def create_component(
    output_dir: str,
    title_text: str = "Welcome to My Webpage",
    body_text: str = "My name is mari and I blog about anime and art here!",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "blue",         # CSS color for heading
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the foundational HTML structure and basic styling
    demonstrated in the tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    # Replicating the 'pink' background from the tutorial for the light scheme
    if color_scheme == "dark":
        bg_color = "#1e1e1e"
        text_color = "#e0e0e0"
        link_color = "#80b3ff"
        accent_color = "#66a3ff" # Softer accent for dark mode
    else:
        bg_color = "pink"        # Tutorial specific color
        text_color = "#000000"
        link_color = accent_color

    # === CSS ===
    # Extracting the logic of the tutorial's inline styles into a clean stylesheet
    css = f"""/* Beginner Webpage Scaffolding — generated component */
*, *::before, *::after {{
    box-sizing: border-box;
}}

/* 
 * Replicating tutorial logic: <body style="background-color: pink;"> 
 */
body {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

/* Adding a container to keep content readable within defined bounds */
.container {{
    max-width: {width_px}px;
    width: 100%;
}}

/* 
 * Replicating tutorial logic: <h1 style="color: blue;"> 
 */
h1 {{
    color: {accent_color};
    margin-top: 0;
    font-size: 2.5rem;
}}

/* 
 * Replicating tutorial logic: <img src="..."> 
 */
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin-bottom: 1.5rem;
    border: 2px solid rgba(0,0,0,0.1);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}}

/* 
 * Replicating tutorial logic: <p style="font-size: 25px;"> 
 */
p {{
    font-size: 25px; 
    line-height: 1.6;
    margin-bottom: 1rem;
}}

/* Link styling */
a {{
    color: {link_color};
    text-decoration: underline;
    font-weight: bold;
}}

a:hover {{
    text-decoration: none;
}}
"""

    # === HTML ===
    # Utilizing the structural tags taught in the video
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
        <h1>{title_text}</h1>
        
        <!-- Using a stable placeholder image to demonstrate the img tag -->
        <img src="https://picsum.photos/seed/anime/800/400" alt="A decorative placeholder image">
        
        <!-- Demonstrating bold <b>, italic <i>, and anchor <a> tags as taught -->
        <p>This is a <b>reproduction</b> of the HTML structure and styling logic. {body_text} I have included <i>italic text</i> and <a href="#">a hyperlink</a> to show the full extent of the lesson.</p>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Beginner Webpage Scaffolding
// This component relies purely on HTML and CSS. No JavaScript is required for the core visual effect.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Webpage loaded successfully.");
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
