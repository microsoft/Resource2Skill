def create_component(
    output_dir: str,
    title_text: str = "Click Me",
    body_text: str = "",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent hover
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic Soft UI Button visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Safely escape text
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#2a2b2f"
        text_color = "#e0e0e0"
        shadow_dark = "#1d1e21"
        shadow_light = "#37383d"
    else:
        # Match tutorial values exactly
        bg_color = "#ebebeb"
        text_color = "#333333"
        shadow_dark = "#bebebe"
        shadow_light = "#ffffff"

    # === CSS ===
    css = f"""/* Neumorphic Soft UI Button — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --shadow-dark: {shadow_dark};
    --shadow-light: {shadow_light};
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
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

.content-wrapper {{
    text-align: center;
}}

.body-text {{
    margin-top: 10px;
    opacity: 0.7;
    font-size: 14px;
}}

/* Core Visual Pattern: Neumorphic Button */
.neumorphic-button {{
    /* Match background exactly to parent to create the illusion of extrusion */
    background: var(--bg);
    color: var(--text);
    
    border: none;
    outline: none;
    border-radius: 12px;
    padding: 20px 40px;
    font-size: 18px;
    font-weight: 500;
    cursor: pointer;
    
    /* Dual Box Shadows: Bottom-Right Dark, Top-Left Light */
    box-shadow: 
        8px 8px 16px var(--shadow-dark), 
        -8px -8px 16px var(--shadow-light);
        
    transition: all 0.2s ease-in-out;
}}

.neumorphic-button:hover {{
    color: var(--accent);
}}

/* The Pressed State */
.neumorphic-button:active {{
    /* Invert shadows to inner to simulate being pushed into the surface */
    box-shadow: 
        inset 6px 6px 10px var(--shadow-dark), 
        inset -6px -6px 10px var(--shadow-light);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neumorphic Soft UI Button</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <button class="neumorphic-button">{safe_title}</button>
        
        {f'<div class="content-wrapper"><p class="body-text">{safe_body}</p></div>' if safe_body else ''}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const button = document.querySelector('.neumorphic-button');
    
    // Example interaction just to prove JS attachment
    button.addEventListener('click', () => {{
        console.log('Neumorphic button pressed!');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
