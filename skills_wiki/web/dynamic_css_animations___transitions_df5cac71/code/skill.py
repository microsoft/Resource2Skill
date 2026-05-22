def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Demo",
    body_text: str = "Hover over the box or watch its continuous animation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff0077",     # CSS hex color for accent
    width_px: int = 200,
    height_px: int = 200,
    **kwargs,
) -> dict:
    """
    Create a web component demonstrating CSS transitions and keyframe animations.

    A square box continuously moves, rotates, and scales using @keyframes.
    On hover, it smoothly changes its background color and scales further using CSS transitions,
    while also pausing its continuous animation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e" # Darker background for contrast
        text_color = "#f0f0f0"
        box_initial_color = "#00bfff" # Cyan from video example
        box_glow_color = "rgba(0, 191, 255, 0.5)" # Cyan glow
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        box_initial_color = "#28a745" # Green for light mode
        box_glow_color = "rgba(40, 167, 69, 0.5)" # Green glow

    # Use accent_color for hover effects consistently
    box_hover_color = accent_color
    box_hover_glow_color = f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.7)"


    # === CSS ===
    css = f"""/* Dynamic CSS Animations & Transitions — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --box-initial: {box_initial_color};
    --box-hover: {box_hover_color};
    --box-glow-initial: {box_glow_color};
    --box-glow-hover: {box_hover_glow_color};
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
    overflow: hidden; /* To prevent scrollbars from element movement */
}}

h1 {{
    margin-bottom: 10px;
    font-size: 2.5em;
    color: var(--text);
    text-align: center;
}}

p {{
    margin-bottom: 50px;
    font-size: 1.1em;
    color: var(--text);
    text-align: center;
    max-width: 80%;
}}

.box {{
    width: {width_px}px;
    height: {height_px}px;
    background-color: var(--box-initial);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    color: var(--text);
    font-weight: bold;
    cursor: pointer;
    position: relative; /* Allows transform to work relative to its position */
    
    /* Continuous Keyframe Animation */
    animation: continuousAnimation 4s ease-in-out infinite alternate;
    
    /* Hover Transition */
    transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 0 15px var(--box-glow-initial); /* Initial glow */
}}

.box:hover {{
    background-color: var(--box-hover);
    transform: scale(1.1); /* Scale up slightly on hover */
    animation-play-state: paused; /* Pause continuous animation on hover */
    box-shadow: 0 0 25px var(--box-hover), 0 0 40px var(--box-hover-glow-color); /* Stronger glow on hover */
}}

/* Keyframe definition for continuous animation */
@keyframes continuousAnimation {{
    0% {{
        transform: translateY(0px) rotate(0deg) scale(1);
        box-shadow: 0 0 15px var(--box-glow-initial);
    }}
    25% {{
        transform: translateY(-50px) rotate(45deg) scale(1.05);
        box-shadow: 0 0 20px var(--box-glow-initial);
    }}
    50% {{
        transform: translateX(50px) translateY(0px) rotate(90deg) scale(1);
        box-shadow: 0 0 15px var(--box-glow-initial);
    }}
    75% {{
        transform: translateX(0px) translateY(50px) rotate(135deg) scale(0.95);
        box-shadow: 0 0 20px var(--box-glow-initial);
    }}
    100% {{
        transform: translateY(0px) rotate(180deg) scale(1);
        box-shadow: 0 0 15px var(--box-glow-initial);
    }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{title_text}</h1>
    <p>{body_text}</p>
    <div class="box">Animate Me!</div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic CSS Animations & Transitions — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // No specific JS interaction needed for this demo, as effects are pure CSS.
    // CSS-based animations and transitions are generally handled directly by the browser.
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
