import os

def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Showcase",
    body_text: str = "Explore different types of CSS animations and transitions.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200, # Note: width_px/height_px are largely ignored for this scrollable showcase, components adapt responsively
    height_px: int = 800, # Note: width_px/height_px are largely ignored for this scrollable showcase, components adapt responsively
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Transitions & Keyframe Animations Showcase visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        card_bg_color = "#1a1a2e"
        border_color = "rgba(255, 255, 255, 0.1)"
        light_accent = "#e3006a" # Used in video for a glowing button like element
        # Colors for scroll blocks (original video palette is quite diverse)
        scroll_block_colors = ["#f0f0f0", "#e87a5b", "#a0a4c2", "#00bfff", "#e7e0d3", "#e3006a", "#8d7971", "#222222", "#666666", "#444444", "#306e7b", "#8b6e51", "#767272", "#905b4b", "#c2904e"]
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        light_accent = "#ff4081"
        scroll_block_colors = ["#1a1a2e", "#7b3d2c", "#5a5c6a", "#007bff", "#8c8e8d", "#d8004f", "#4f4540", "#eeeeee", "#999999", "#bbbbbb", "#1e4d57", "#4d3a2a", "#3b3939", "#5a3a30", "#8f6b3b"]


    # === CSS ===
    css = f"""/* CSS Transitions & Keyframe Animations Showcase — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg_color};
    --border: {border_color};
    --light-accent: {light_accent};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    gap: 60px;
    overflow-x: hidden; /* Prevent horizontal scroll for transform animations */
}}

h1 {{
    font-size: 2.5em;
    font-weight: 700;
    text-align: center;
    color: var(--accent);
    margin-bottom: 15px;
}}

p.body-text {{
    text-align: center;
    max-width: 800px;
    line-height: 1.6;
    font-size: 1.1em;
    margin-bottom: 30px;
}}

.section-title {{
    font-size: 1.8em;
    font-weight: 600;
    margin-bottom: 20px;
    text-align: center;
    color: var(--text);
}}

.demo-section {{
    width: 100%;
    max-width: 1000px;
    padding: 40px;
    background-color: var(--card-bg);
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
}}

/* --- Transition Demo --- */
.transition-box {{
    width: 150px;
    height: 150px;
    background-color: var(--accent);
    border-radius: 8px;
    transition: transform 0.6s ease-in-out, background-color 0.6s ease-in-out, box-shadow 0.6s ease-in-out;
    cursor: pointer;
}}

.transition-box:hover {{
    background-color: var(--light-accent);
    transform: scale(1.2) rotate(90deg);
    box-shadow: 0 0 20px var(--light-accent);
}}

/* --- Keyframe Animation Demo --- */
.keyframe-box {{
    width: 150px;
    height: 150px;
    background-color: var(--accent);
    border-radius: 8px;
    animation: moveRotateScale 4s ease-in-out infinite alternate;
    cursor: pointer;
}}

.keyframe-box:hover {{
    animation-play-state: paused; /* Pause on hover */
}}

@keyframes moveRotateScale {{
    0% {{
        transform: translateX(-200px) translateY(-50px) rotate(0deg) scale(1);
        background-color: var(--accent);
    }}
    50% {{
        transform: translateX(200px) translateY(50px) rotate(180deg) scale(0.8);
        background-color: var(--light-accent);
    }}
    100% {{
        transform: translateX(-200px) translateY(-50px) rotate(360deg) scale(1);
        background-color: var(--accent);
    }}
}}

/* --- Loading Animation Demo (3D Cube) --- */
.loading-cube {{
    width: 80px;
    height: 80px;
    border: 5px solid {accent_color};
    border-radius: 5px;
    box-shadow: 0 0 10px {accent_color}, inset 0 0 10px {accent_color};
    animation: loading-3d 2s ease-in-out infinite;
    transform-style: preserve-3d; /* Enable 3D transformations */
}}

@keyframes loading-3d {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
        box-shadow: 0 0 10px {accent_color}, inset 0 0 10px {accent_color};
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
        box-shadow: 0 0 20px {accent_color}, inset 0 0 20px {accent_color};
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
        box-shadow: 0 0 10px {accent_color}, inset 0 0 10px {accent_color};
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
        box-shadow: 0 0 20px {accent_color}, inset 0 0 20px {accent_color};
    }}
}}

/* --- Scrolling Animation Demo --- */
.scroll-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    width: 100%;
    margin-top: 20px;
}}

.scroll-block {{
    width: 100%;
    height: 120px;
    border-radius: 8px;
    opacity: 0;
    transform: translateY(50px) scale(0.8); /* Initial state for animation */
    
    animation: scroll-reveal linear forwards;
    animation-timeline: view(); /* Link animation to element's visibility in the viewport */
    animation-range: entry 0% cover 50%; /* Start animating when element enters, complete when 50% is covered */
}}

@keyframes scroll-reveal {{
    from {{
        opacity: 0;
        transform: translateY(50px) scale(0.8);
    }}
    to {{
        opacity: 1;
        transform: translateY(0px) scale(1);
    }}
}}

/* Assign different colors to scroll blocks */
""" + "".join([f"""
.scroll-block:nth-child({i+1}) {{
    background-color: {scroll_block_colors[i % len(scroll_block_colors)]};
}}
""" for i in range(25)]) + """
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
    <h1>{title_text}</h1>
    <p class="body-text">{body_text}</p>

    <section class="demo-section">
        <h2 class="section-title">CSS Transitions Demo</h2>
        <div class="transition-box"></div>
    </section>

    <section class="demo-section">
        <h2 class="section-title">CSS Keyframe Animation Demo</h2>
        <div class="keyframe-box"></div>
        <p style="font-size: 0.9em; text-align: center;">Hover over the box to pause the animation!</p>
    </section>

    <section class="demo-section">
        <h2 class="section-title">Loading Animation Demo (3D Rotation)</h2>
        <div class="loading-cube"></div>
    </section>

    <section class="demo-section">
        <h2 class="section-title">Scroll-Triggered Animation Demo</h2>
        <p style="font-size: 0.9em; text-align: center;">Scroll down to see elements animate into view.</p>
        <div class="scroll-container">
            {''.join([f'<div class="scroll-block" aria-hidden="true"></div>' for _ in range(25)])}
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (Placeholder, as most effects are CSS-driven) ===
    js = f"""// CSS Transitions & Keyframe Animations Showcase — interactive behavior (mostly CSS-driven)
document.addEventListener('DOMContentLoaded', () => {{
    // This script can be used for more complex JS-driven animations or interactions.
    // For this showcase, core animations and scroll-triggered effects are handled by CSS.
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

