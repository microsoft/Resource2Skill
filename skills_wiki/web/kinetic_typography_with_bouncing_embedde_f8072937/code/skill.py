def create_component(
    output_dir: str,
    title_text: str = "MOTION",
    body_text: str = "Kinetic typography inspired by vector animation tools.",
    color_scheme: str = "light",
    accent_color: str = "#FCEE21",  # Vibrant yellow from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Kinetic Typography with Bouncing Shapes effect.
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "light":
        bg_color = accent_color
        text_color = "#111111"
        hover_opacity = "0.6"
    else:
        bg_color = "#111111"
        text_color = accent_color
        hover_opacity = "0.8"

    # === CSS ===
    css = f"""/* Kinetic Typography Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000; /* Outer frame background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
    height: 100vh;
    max-height: var(--height);
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    overflow: hidden;
}}

.kinetic-text {{
    font-size: clamp(4rem, 15vw, 12rem);
    font-weight: 900;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: -0.05em;
    color: var(--text);
    line-height: 1;
    user-select: none;
}}

.letter {{
    display: inline-block;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
    cursor: default;
}}

.letter:hover {{
    transform: scale(1.08) translateY(-5%);
    opacity: {hover_opacity};
}}

.shape-wrapper {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 0.75em;
    height: 1em;
    margin: 0 0.02em;
}}

.shape {{
    display: block;
    width: 0.75em;
    height: 0.75em;
    background-color: var(--text);
    border-radius: 50%;
    will-change: transform;
}}

.bounce-up {{
    animation: bounceUp 2s cubic-bezier(0.45, 0, 0.55, 1) infinite;
}}

.bounce-down {{
    animation: bounceDown 2s cubic-bezier(0.45, 0, 0.55, 1) infinite;
}}

@keyframes bounceUp {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-35%); }}
}}

@keyframes bounceDown {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(35%); }}
}}

.body-text {{
    margin-top: 2rem;
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: var(--text);
    opacity: 0.8;
    font-weight: 500;
    text-align: center;
    max-width: 80%;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kinetic Typography</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <!-- data-target specifies the letter to replace with a bouncing shape -->
        <h1 class="kinetic-text" id="kinetic-container" data-text="{safe_title}" data-target="O"></h1>
        <p class="body-text">{safe_body}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('kinetic-container');
    const titleText = container.getAttribute('data-text') || 'MOTION';
    let targetChar = container.getAttribute('data-target') || 'O';
    
    // Fallback: If target character is not in the text, attempt to find a vowel
    if (!titleText.toUpperCase().includes(targetChar.toUpperCase())) {{
        const match = titleText.match(/[AEIOU]/i);
        if (match) {{
            targetChar = match[0].toUpperCase();
        }} else {{
            // If no vowels, target the middle character
            targetChar = titleText.charAt(Math.floor(titleText.length / 2)).toUpperCase();
        }}
    }}

    let htmlContent = '';
    let shapeCount = 0;
    
    // Parse the text and inject animated shapes
    for (let char of titleText) {{
        if (char.toUpperCase() === targetChar.toUpperCase()) {{
            // Alternate between moving up and moving down
            const bounceClass = shapeCount % 2 === 0 ? 'bounce-up' : 'bounce-down';
            htmlContent += `<span class="shape-wrapper"><span class="shape ${{bounceClass}}"></span></span>`;
            shapeCount++;
        }} else {{
            htmlContent += `<span class="letter">${{char}}</span>`;
        }}
    }}
    
    container.innerHTML = htmlContent;
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
