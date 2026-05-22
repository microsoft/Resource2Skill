import os

def create_component(
    output_dir: str,
    title_text: str = "CSS Animations & Transitions Tutorial",
    intro_text: str = "Explore the power of CSS to create dynamic and engaging web interfaces with this tutorial breakdown.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent. Default cyan.
    width_px: int = 1200,              # Max width of the main content area
    height_px: int = 800,              # Min height of the viewport for scrolling
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Animations & Transitions visual effects from the tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#f0f0f0"
        section_border_color = "rgba(255, 255, 255, 0.1)"
        
        # Specific colors for demos, trying to match video and parameter intent
        neon_button_bg = "#ff006e" # Pink from button demo
        neon_button_hover_bg = "#00bcd4" # Cyan from button demo
        box_animation_color_start = "#ff006e" # Pink
        box_animation_color_mid = "#ff88bb" # Light pink/purple blend
        box_animation_color_end = accent_color # Use accent for end state
        loading_spinner_border_color = accent_color # Cyan for loading
        
        scroll_block_colors = [ # Palette from video
            "#fdf9e3", "#f26419", "#d81f20", "#f9e0a0",
            "#25a89b", "#9073a1", "#ed4e40", "#f4d093",
            "#40505b", "#6a5d7b", "#e0634e", "#f0ead6",
            "#80101b", "#5a5a5a", "#1d7874", "#926857",
            "#e6e6e6", "#8d99ae", "#a55a5b", "#b2ac88"
        ]

    else: # light theme
        bg_color = "#f8f9fa"
        text_color = "#212529"
        section_border_color = "rgba(0, 0, 0, 0.1)"

        neon_button_bg = "#007bff"
        neon_button_hover_bg = "#28a745"
        box_animation_color_start = "#007bff"
        box_animation_color_mid = "#5cb85c"
        box_animation_color_end = accent_color
        loading_spinner_border_color = accent_color

        scroll_block_colors = [ # Muted light palette
            "#e9ecef", "#f0f2f5", "#dee2e6", "#f8f9fa",
            "#ced4da", "#e2e6ea", "#adb5bd", "#cfd2d7",
            "#6c757d", "#9a9da3", "#495057", "#888b90",
            "#343a40", "#63666b", "#212529", "#505358",
            "#d7dadd", "#bcc0c4", "#a2a6aa", "#868a8f"
        ]

    # Generate scroll blocks HTML
    scroll_blocks_html = ""
    for i, color in enumerate(scroll_block_colors):
        # Using fixed block width/height for visual consistency with video
        # animation-delay is for staggered entry effect
        scroll_blocks_html += f'<div class="block" style="background-color: {color}; animation-delay: {i * 0.08}s;"></div>'


    # === CSS ===
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@700&display=swap');

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
        --height: {height_px}px; /* Used for scroll section min-height */

        /* Theme-specific animation colors */
        --neon-button-bg: {neon_button_bg};
        --neon-button-hover-bg: {neon_button_hover_bg};
        --box-animation-color-start: {box_animation_color_start};
        --box-animation-color-mid: {box_animation_color_mid};
        --box-animation-color-end: {box_animation_color_end};
        --loading-spinner-border-color: {loading_spinner_border_color};
        --section-border-color: {section_border_color};
    }}

    body {{
        font-family: 'Inter', sans-serif;
        background: var(--bg);
        color: var(--text);
        min-height: 100vh;
        overflow-x: hidden; /* Prevent horizontal scroll for translateX animations */
        line-height: 1.6;
    }}

    .main-wrapper {{
        max-width: var(--width);
        margin: 0 auto;
        padding: 20px;
    }}

    section {{
        padding: 60px 20px;
        margin-bottom: 80px;
        border-bottom: 1px solid var(--section-border-color);
    }}
    section:last-of-type {{
        border-bottom: none;
        margin-bottom: 0;
    }}

    h1, h2 {{
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        margin-bottom: 40px;
        color: var(--accent);
        font-size: 2.5rem;
        letter-spacing: 1px;
    }}
    h1 {{
        font-size: 3.5rem;
    }}

    p.intro-text {{
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 60px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }}

    /* --- Neon Button Transition --- */
    .neon-button-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 150px;
    }}

    .neon-button {{
        background-color: var(--neon-button-bg);
        color: var(--text);
        padding: 15px 30px;
        border: 2px solid var(--neon-button-bg);
        border-radius: 5px;
        font-size: 1.2rem;
        cursor: pointer;
        outline: none;
        box-shadow: 0 0 5px var(--neon-button-bg), 0 0 10px var(--neon-button-bg), 0 0 20px var(--neon-button-bg), 0 0 40px var(--neon-button-bg);
        transition: background-color 0.4s ease-in-out, border-color 0.4s ease-in-out, box-shadow 0.4s ease-in-out;
    }}

    .neon-button:hover {{
        background-color: var(--neon-button-hover-bg);
        border-color: var(--neon-button-hover-bg);
        box-shadow: 0 0 5px var(--neon-button-hover-bg), 0 0 10px var(--neon-button-hover-bg), 0 0 20px var(--neon-button-hover-bg), 0 0 40px var(--neon-button-hover-bg);
    }}

    /* --- Keyframe Box Animation --- */
    .box-animation-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        position: relative;
    }}

    .animated-box {{
        width: 100px;
        height: 100px;
        background-color: var(--box-animation-color-start);
        animation-name: moveRotateScale;
        animation-duration: 4s;
        animation-timing-function: ease-in-out;
        animation-delay: 0s;
        animation-iteration-count: infinite;
        animation-direction: alternate; /* Plays forward then backward */
        animation-fill-mode: both; /* Retains final state before delay */
        animation-play-state: running; /* Can be paused */
        border-radius: 10px;
    }}

    .animated-box:hover {{
        animation-play-state: paused;
    }}

    @keyframes moveRotateScale {{
        0% {{
            transform: translateX(-150px) translateY(-50px) rotate(0deg) scale(1);
            background-color: var(--box-animation-color-start);
        }}
        50% {{
            transform: translateX(0px) translateY(50px) rotate(180deg) scale(1.5);
            background-color: var(--box-animation-color-mid);
        }}
        100% {{
            transform: translateX(150px) translateY(-50px) rotate(360deg) scale(1);
            background-color: var(--box-animation-color-end);
        }}
    }}

    /* --- Loading Animation --- */
    .loading-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 150px;
    }}

    .loading-spinner {{
        width: 50px;
        height: 50px;
        border: 5px solid var(--loading-spinner-border-color);
        border-radius: 3px;
        box-shadow: 0 0 8px var(--loading-spinner-border-color), inset 0 0 8px var(--loading-spinner-border-color);
        animation: loadingRotate 2s ease-in-out infinite;
    }}

    @keyframes loadingRotate {{
        0% {{
            transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
        }}
        33% {{
            transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
        }}
        67% {{
            transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
        }}
        100% {{
            transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
        }}
    }}

    /* --- Scrolling Animation --- */
    .scroll-animation-container {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        padding: 40px;
        min-height: calc(var(--height) + 200px); /* Extend height to allow scrolling interaction */
    }}

    .block {{
        height: 100px;
        border-radius: 8px;
        opacity: 0;
        transform: translateX(-100px); /* Start off-screen to the left */
        animation: scrollFadeInTranslate 1s ease-out forwards;
        animation-timeline: view(); /* This links animation to scroll progress */
        animation-range: entry 0% cover 50%; /* Animates from when 0% enters to when 50% is covered */
    }}

    @keyframes scrollFadeInTranslate {{
        0% {{
            opacity: 0;
            transform: translateX(-100px);
        }}
        100% {{
            opacity: 1;
            transform: translateX(0);
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-wrapper">
        <section class="hero-section">
            <h1>{title_text}</h1>
            <p class="intro-text">{intro_text}</p>
        </section>

        <section>
            <h2>Transitions: Smooth Property Changes</h2>
            <div class="neon-button-container">
                <button class="neon-button">Hover Me!</button>
            </div>
        </section>

        <section>
            <h2>Keyframe Animations: Detailed Control</h2>
            <div class="box-animation-container">
                <div class="animated-box"></div>
            </div>
        </section>

        <section>
            <h2>Loading Animation Example</h2>
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
        </section>

        <section class="scroll-animation-container">
            <h2>Scroll-Driven Animations (Scroll Down!)</h2>
            {scroll_blocks_html}
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """
// All animations and transitions in this example are handled directly by CSS,
// including scroll-driven animations which use native CSS features.
// No JavaScript is strictly necessary for the core visual effects demonstrated.
// For older browser compatibility with scroll-driven animations, polyfills like
// 'scroll-timeline' (github.com/florian-schulte/scroll-timeline) might be considered,
// but for a self-contained CSS-focused example, we rely on native browser support.
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

