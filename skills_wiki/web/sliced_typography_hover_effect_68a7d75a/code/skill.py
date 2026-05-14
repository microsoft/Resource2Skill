def create_component(
    output_dir: str,
    title_text: str = "GLITCH MENU",
    body_text: str = "Hover over the menu items to see the slice effect.",
    color_scheme: str = "light",
    accent_color: str = "#ff0000",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Sliced Typography Hover Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configuration
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f4f4f4"
    else:
        bg_color = "#ffffff"
        text_color = "#262626"

    # === CSS ===
    css = f"""/* Sliced Typography Hover Effect */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Catamaran', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

.header-info {{
    text-align: center;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}}

.header-info h1 {{
    font-size: 1.2rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent-color);
    margin-bottom: 0.5rem;
}}

.header-info p {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

.sliced-menu {{
    list-style: none;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.menu-item {{
    position: relative;
    /* Hide the animated line when it travels outside the item */
    overflow: hidden; 
    margin: 5px 0;
    /* Padding provides space so shifted text isn't cut off by overflow:hidden */
    padding: 10px 25px; 
}}

/* The Animated Strike-through Line */
.menu-item::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--text-color);
    /* Start entirely out of view to the left */
    transform: translate(-101%, -50%);
    transition: transform 0.5s ease-in-out;
    z-index: 10;
    pointer-events: none;
}}

.menu-item:hover::before {{
    /* Travel all the way across to the right out of view */
    transform: translate(101%, -50%);
}}

.menu-link {{
    position: relative;
    display: inline-block;
    font-size: 3.5rem;
    font-weight: 900;
    text-transform: uppercase;
    text-decoration: none;
    /* Hide the original DOM text, rely purely on pseudo-elements */
    color: transparent; 
    line-height: 1;
    letter-spacing: 2px;
}}

/* Setup overlapping text layers */
.menu-link::before,
.menu-link::after {{
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    color: var(--text-color);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), color 0.4s ease;
    white-space: nowrap;
}}

/* Clip Top Half */
.menu-link::before {{
    clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%);
}}

/* Clip Bottom Half */
.menu-link::after {{
    clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%);
}}

/* Hover Displacements */
.menu-item:hover .menu-link::before {{
    transform: translate(10px, -2px);
    color: var(--accent-color);
}}

.menu-item:hover .menu-link::after {{
    transform: translate(-10px, 2px);
    color: var(--accent-color);
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
    <link href="https://fonts.googleapis.com/css2?family=Catamaran:wght@900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header-info">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <ul class="sliced-menu">
            <li class="menu-item"><a href="#" class="menu-link" data-text="HOME">HOME</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="ABOUT">ABOUT</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="SERVICES">SERVICES</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="PORTFOLIO">PORTFOLIO</a></li>
            <li class="menu-item"><a href="#" class="menu-link" data-text="CONTACT">CONTACT</a></li>
        </ul>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS effect. No JavaScript required for interactions.
console.log("Sliced typography component successfully initialized.");
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
