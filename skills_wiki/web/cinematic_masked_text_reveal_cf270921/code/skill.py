def create_component(
    output_dir: str,
    title_text: str = "WELCOME IN",
    body_text: str = "DARKCODE",
    color_scheme: str = "dark",
    accent_color: str = "#6ab04c",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Masked Text Reveal visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#08080c" # Deep black/dark
        text_color = "#ffffff"
    else:
        bg_color = "#f4f4f5" # Off-white
        text_color = "#121212"

    # === CSS ===
    css = f"""/* Cinematic Masked Text Reveal */
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
    align-items: center;
    justify-content: center;
}}

.reveal-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    /* Ensure the entire block remains centered during expansion */
    justify-content: center; 
}}

.primary-text {{
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text);
    /* The core trick: solid background to mask the text underneath */
    background: var(--bg);
    position: relative;
    z-index: 2;
    /* Padding prevents text clipping during extreme letter-spacing */
    padding: 0.1em 0.5em; 
    line-height: 1.1;
    
    /* Animation definition */
    animation: sequence-reveal 3.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
}}

.secondary-text {{
    font-size: clamp(1.2rem, 2.5vw, 2.2rem);
    font-weight: 600;
    text-transform: uppercase;
    color: var(--accent);
    position: relative;
    z-index: 1;
    letter-spacing: 0.1em;
}}

@keyframes sequence-reveal {{
    0% {{
        color: transparent;
        /* Pulls the secondary text up to be hidden behind the primary text's background */
        margin-bottom: -0.7em; 
        letter-spacing: 0.6em;
        transform: translateY(10px);
    }}
    20% {{
        color: var(--text);
        margin-bottom: -0.7em;
        letter-spacing: 0.5em;
        transform: translateY(0);
    }}
    60% {{
        /* Text finishes contracting */
        margin-bottom: -0.7em;
        letter-spacing: 0.1em;
    }}
    75% {{
        /* Pause to read the word before revealing */
        margin-bottom: -0.7em;
        letter-spacing: 0.1em;
    }}
    100% {{
        /* Pushes the secondary text down, revealing it from behind the mask */
        margin-bottom: 0.25em; 
        letter-spacing: 0.1em;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Reveal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="reveal-wrapper">
            <h1 class="primary-text">{title_text}</h1>
            <h2 class="secondary-text">{body_text}</h2>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Cinematic Masked Text Reveal
// This component relies entirely on CSS keyframes and box-model manipulations.
// JavaScript can be used here to re-trigger the animation on demand.

document.addEventListener('DOMContentLoaded', () => {{
    const primaryText = document.querySelector('.primary-text');
    
    // Example: Click the container to replay the animation
    document.querySelector('.container').addEventListener('click', () => {{
        // Force reflow to restart CSS animation
        primaryText.style.animation = 'none';
        void primaryText.offsetWidth; 
        primaryText.style.animation = 'sequence-reveal 3.5s cubic-bezier(0.25, 1, 0.5, 1) forwards';
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
