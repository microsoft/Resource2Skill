def create_component(
    output_dir: str,
    title_text: str = "CSS Animation & Transition Showcase",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#00bfff",  # CSS hex color for secondary accent
    primary_accent_color: str = "#ff4081", # CSS hex color for primary accent
    **kwargs,
) -> dict:
    """
    Create a web component reproducing CSS animation and transition effects from the tutorial.

    Features:
    - A main box with a continuous keyframe animation (move, rotate, scale).
    - Hover effect on the main box to pause its animation.
    - Multiple scrollable blocks that animate (fade in and translate) as they enter the viewport.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
        # primary_accent_color is passed directly now
        # secondary_accent_color is passed directly as accent_color
    else: # light theme
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        primary_accent_color = "#e91e63" # default primary for light if not provided
        accent_color = "#008fcc" # default secondary for light (a slightly darker cyan) if not provided


    # Manually derive slightly lighter versions for animation keyframes for static CSS
    # Primary accent: #ff4081 -> slightly lighter for 25% keyframe
    lighter_primary_accent = "#ff639c"
    # Secondary accent: #00bfff -> slightly lighter for 75% keyframe
    lighter_secondary_accent = "#33ccff"
    # Hover background for main box (darker cyan for contrast on light theme)
    main_box_hover_bg = "#008fcc" if color_scheme == "dark" else "#005f7f"


    # Generate distinct colors for scroll items for visual variety
    scroll_item_colors = [
        "#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#073b4c",
        "#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653",
        "#ff6b6b", "#ffe66d", "#4ecdc4", "#1a535c", "#004040",
        "#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff",
        "#f08080", "#dda0dd", "#98fb98", "#add8e6", "#f0e68c",
        "#d8bfd8", "#ff7f50", "#6a5acd", "#8fbc8f", "#20b2aa"
    ]

    # Animation names
    box_animation_name = "moveRotateScale"
    scroll_animation_name = "fadeInTranslate"


    # === CSS ===
    css = f"""/* CSS Animation & Transition Showcase — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --primary-accent: {primary_accent_color};
    --secondary-accent: {accent_color};
    --lighter-primary-accent: {lighter_primary_accent};
    --lighter-secondary-accent: {lighter_secondary_accent};
    --main-box-hover-bg: {main_box_hover_bg};
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
    overflow-x: hidden; /* Prevent horizontal scroll from translate animations */
    line-height: 1.6;
    scroll-behavior: smooth; /* For smoother scrolling effects */
}}

h1 {{
    font-size: 2.5em;
    margin-bottom: 30px;
    text-align: center;
    color: var(--text);
}}

.intro-section {{
    max-width: 800px; /* Use a max-width for responsiveness */
    width: 100%;
    margin-bottom: 60px;
    text-align: center;
}}
.intro-section p {{
    font-size: 1.1em;
    max-width: 600px;
    margin: 0 auto;
}}

.animated-box-section {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 50vh; /* Ensure section is tall enough */
    width: 100%;
    margin-bottom: 80px;
    padding: 40px 0;
    background-color: var(--bg);
}}

.main-box {{
    width: 150px;
    height: 150px;
    background-color: var(--primary-accent);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.2em;
    color: var(--text);
    box-shadow: 0 0 15px rgba(255, 64, 129, 0.4);
    animation: {box_animation_name} 4s ease-in-out infinite alternate-reverse;
    transition: all 0.3s ease; /* For hover effects */
    cursor: pointer;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    will-change: transform, background-color, box-shadow; /* Optimize animations */
}}

.main-box:hover {{
    transform: translateY(-20px) rotate(45deg) scale(1.1);
    background-color: var(--main-box-hover-bg); /* Use specific hover color */
    box-shadow: 0 0 25px var(--secondary-accent);
    animation-play-state: paused; /* Pause animation on hover */
}}

@keyframes {box_animation_name} {{
    0% {{
        transform: translateX(-200px) translateY(-50px) rotate(0deg) scale(1);
        background-color: var(--primary-accent);
        box-shadow: 0 0 15px rgba(255, 64, 129, 0.4);
    }}
    25% {{
        transform: translateX(0px) translateY(-100px) rotate(90deg) scale(1.2);
        background-color: var(--lighter-primary-accent);
        box-shadow: 0 0 20px rgba(255, 64, 129, 0.6);
    }}
    50% {{
        transform: translateX(200px) translateY(-50px) rotate(180deg) scale(1);
        background-color: var(--secondary-accent);
        box-shadow: 0 0 25px rgba(0, 191, 255, 0.4);
    }}
    75% {{
        transform: translateX(0px) translateY(0px) rotate(270deg) scale(0.9);
        background-color: var(--lighter-secondary-accent);
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.6);
    }}
    100% {{
        transform: translateX(-200px) translateY(-50px) rotate(360deg) scale(1);
        background-color: var(--primary-accent);
        box-shadow: 0 0 15px rgba(255, 64, 129, 0.4);
    }}
}}


.scrolling-animation-section {{
    width: 100%;
    max-width: 1000px; /* Max width for scrollable content */
    margin-top: 80px;
    padding: 20px;
    background-color: var(--bg);
}}

.section-title {{
    font-size: 1.8em;
    color: var(--text);
    margin-bottom: 25px;
    margin-top: 50px;
    text-align: center;
    width: 100%;
}}

.scroll-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
    min-height: 150vh; /* Make container tall enough to scroll */
    background-color: var(--bg);
}}

.scroll-item {{
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-weight: 500;
    font-size: 1.1em;
    color: var(--text);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    will-change: opacity, transform; /* Optimize animations */

    /* Scroll-linked animation properties */
    animation: {scroll_animation_name} 1s ease-out forwards;
    animation-timeline: view();
    animation-range: entry 0% cover 50%; /* Starts when enters viewport, completes when 50% covered */
}}

@keyframes {scroll_animation_name} {{
    from {{
        opacity: 0;
        transform: translateX(-150px); /* Animate from left */
    }}
    to {{
        opacity: 1;
        transform: translateX(0px);
    }}
}}

/* Specific colors for scroll items */
""" + "".join([f".scroll-item:nth-child({i+1}) {{ background-color: {scroll_item_colors[i % len(scroll_item_colors)]}; }}" for i in range(30)]) + """
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
    <div class="intro-section">
        <h1>{title_text}</h1>
        <p>Explore the power of CSS animations and transitions to create dynamic and engaging web experiences. This page demonstrates continuous keyframe animations, interactive hover transitions, and modern scroll-triggered effects.</p>
    </div>

    <h2 class="section-title">Keyframe Animation Demo</h2>
    <div class="animated-box-section">
        <div class="main-box">Animate Me!</div>
    </div>

    <h2 class="section-title">Scroll-Triggered Animation Demo</h2>
    <div class="scrolling-animation-section">
        <div class="scroll-container">
            {''.join([f'<div class="scroll-item">Element {i+1}</div>' for i in range(30)])}
        </div>
    </div>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Animation & Transition Showcase — no explicit JS needed for primary effects.
// Hover effects and scroll-linked animations are handled via CSS properties.
document.addEventListener('DOMContentLoaded', () => {{
    console.log('Document loaded. CSS animations and transitions are active!');
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
