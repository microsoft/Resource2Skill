def create_component(
    output_dir: str,
    title_text: str = "CSS Transform Animations",
    body_text: str = "Explore keyframes for complex motion and transitions for smooth interactivity.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff007f",     # CSS hex color for accent (pink by default)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing CSS Transform Animations with Keyframes and Transitions.

    Demonstrates a looping keyframe animation and a smooth hover transition on a button.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.1)"
        button_text_color = "#0d111c"
        button_bg_color = accent_color
        button_hover_shadow = f"0 0 15px {accent_color}, 0 0 30px {accent_color}, 0 0 45px {accent_color}"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.08)"
        button_text_color = "#f0f0f0"
        button_bg_color = accent_color
        button_hover_shadow = f"0 0 15px {accent_color}, 0 0 30px {accent_color}, 0 0 45px {accent_color}"

    # === CSS ===
    css = f"""/* CSS Transform Animations with Keyframes and Transitions — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --button-text: {button_text_color};
    --button-bg: {button_bg_color};
    --button-hover-shadow: {button_hover_shadow};
    --component-width: {width_px}px;
    --component-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Hide overflow for animating box */
    padding: 20px;
}}

.content-wrapper {{
    max-width: 800px;
    text-align: center;
    margin-bottom: 50px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 15px;
    color: var(--accent);
}}

.body-text {{
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 30px;
}}

/* --- Keyframe Animation Example --- */
.animated-box {{
    width: 100px;
    height: 100px;
    background-color: var(--accent);
    position: relative;
    border-radius: 8px;
    animation: moveRotateScale 4s ease-in-out infinite alternate-reverse;
    margin-top: 50px; /* Space from text */
}}

@keyframes moveRotateScale {{
    0% {{
        transform: translateX(0) translateY(0) rotate(0deg) scale(1);
        background-color: var(--accent);
    }}
    25% {{
        transform: translateX(calc(var(--component-width) * 0.2)) translateY(-50px) rotate(90deg) scale(0.8);
        background-color: #ffcc00; /* Yellowish */
    }}
    50% {{
        transform: translateX(calc(var(--component-width) * 0.4)) translateY(0px) rotate(180deg) scale(1.2);
        background-color: #00e676; /* Greenish */
    }}
    75% {{
        transform: translateX(calc(var(--component-width) * 0.2)) translateY(50px) rotate(270deg) scale(0.8);
        background-color: #00bfff; /* Cyan */
    }}
    100% {{
        transform: translateX(0) translateY(0) rotate(360deg) scale(1);
        background-color: var(--accent);
    }}
}}

/* --- Transition Example (Button) --- */
.action-button {{
    padding: 15px 30px;
    background-color: var(--button-bg);
    color: var(--button-text);
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    outline: none;
    transition: transform 0.3s ease-out, background-color 0.3s ease-out, box-shadow 0.3s ease-out;
    margin-top: 50px;
    text-decoration: none; /* For anchor buttons */
}}

.action-button:hover {{
    transform: scale(1.05);
    background-color: {accent_color}; /* Ensure consistent accent color on hover */
    box-shadow: var(--button-hover-shadow);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="content-wrapper">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    <div class="animated-box"></div>
    <a href="#" class="action-button">Click Me!</a>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Transform Animations with Keyframes and Transitions — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // No specific JS required for these pure CSS effects,
    // but this is where any dynamic JS interactions would go.
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

