def create_component(
    output_dir: str,
    title_text: str = "",
    body_text: str = "",
    color_scheme: str = "light",
    accent_color: str = "#13ddd9",     # The turquoise from the video
    width_px: int = 800,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic Soft UI Icons visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    # Using modern CSS color-mix to automatically generate the highlight and shadow
    # directly from the provided accent_color. This makes the neumorphism dynamic.
    css = f"""/* Neumorphic Soft UI Icons — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Base Color */
    --base-color: {accent_color};
    
    /* Dynamically calculated neumorphic shadows */
    --shadow-light: color-mix(in srgb, var(--base-color), white 20%);
    --shadow-dark: color-mix(in srgb, var(--base-color), black 20%);
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: system-ui, -apple-system, sans-serif;
    background-color: var(--base-color);
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
    justify-content: space-around;
    align-items: center;
    padding: 2rem;
}}

.icon-wrapper {{
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    /* Prevent text selection when clicking rapidly */
    user-select: none; 
}}

/* The Core Neumorphic Text Effect */
.nm-icon {{
    /* Text color MUST match the background color perfectly */
    color: var(--base-color);
    font-size: 8rem;
    
    /* Smooth transition for interactions */
    transition: text-shadow 0.2s ease-out;
    
    /* 
      Top-left shadow: Light highlight (- offset)
      Bottom-right shadow: Dark shadow (+ offset)
    */
    text-shadow: 
        -8px -8px 16px var(--shadow-light),
        8px 8px 16px var(--shadow-dark);
}}

/* Value Add: Hover and Active states for interactivity */
.icon-wrapper:hover .nm-icon {{
    text-shadow: 
        -10px -10px 20px var(--shadow-light),
        10px 10px 20px var(--shadow-dark);
}}

.icon-wrapper:active .nm-icon {{
    /* Pressed state: shadows tighten and pull closer */
    text-shadow: 
        -2px -2px 4px var(--shadow-light),
        2px 2px 4px var(--shadow-dark);
}}

.icon-wrapper:active {{
    transform: scale(0.96);
}}

/* Responsive scaling */
@media (max-width: 600px) {{
    .container {{
        flex-direction: column;
    }}
    .nm-icon {{
        font-size: 6rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neumorphic Icons</title>
    <!-- Font Awesome CDN for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Tree Icon -->
        <div class="icon-wrapper">
            <i class="fa-solid fa-tree nm-icon"></i>
        </div>
        
        <!-- Meteor Icon -->
        <div class="icon-wrapper">
            <i class="fa-solid fa-meteor nm-icon"></i>
        </div>
        
        <!-- Space Shuttle Icon -->
        <div class="icon-wrapper">
            <i class="fa-solid fa-space-shuttle nm-icon"></i>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interaction logic is handled entirely via CSS pseudo-classes (:hover, :active)
// No complex JavaScript is required for this specific visual effect.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Neumorphic icons loaded.");
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
