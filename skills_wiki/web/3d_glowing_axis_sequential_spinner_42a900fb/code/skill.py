def create_component(
    output_dir: str,
    title_text: str = "Loading Data...",
    body_text: str = "Click the loader to pause/resume the animation.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Axis-Sequential Spinner.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040716" # Matches the deep navy video background
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f6f9"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* 3D Glowing Axis-Sequential Spinner */
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
    max-width: 100%;
    height: var(--height);
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    position: relative;
}}

/* Header Typography */
.text-wrapper {{
    text-align: center;
    z-index: 20;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 8px;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 14px;
    opacity: 0.7;
    font-weight: 300;
}}

/* The Loader Component */
.loader-wrapper {{
    position: relative;
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.3s ease;
}}

.loader-wrapper:hover {{
    background: rgba(255, 255, 255, 0.1);
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), 0 0 12px var(--accent) inset;
    z-index: 10;
    
    /* Animation Shorthand: duration | name | timing-function | iteration-count */
    animation: loading-spin 2.5s ease-in-out infinite;
}}

/* Interactive Play State Class */
.paused {{
    animation-play-state: paused;
    opacity: 0.5;
    box-shadow: 0 0 2px var(--accent), 0 0 2px var(--accent) inset;
    transition: box-shadow 0.3s ease, opacity 0.3s ease;
}}

/* The 3-Axis Sequential Rotation Keyframes */
@keyframes loading-spin {{
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

/* State indicator */
.state-badge {{
    position: absolute;
    bottom: 15px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    color: var(--accent);
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.loader-wrapper.is-paused .state-badge {{
    opacity: 1;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="loader-wrapper" id="loaderWrapper" role="button" aria-pressed="false" tabindex="0">
            <div class="loading" id="spinner"></div>
            <span class="state-badge">Paused</span>
        </div>

        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Axis-Sequential Spinner - Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const wrapper = document.getElementById('loaderWrapper');
    const spinner = document.getElementById('spinner');

    function toggleAnimation() {{
        // Toggle the paused class on the spinner for animation-play-state
        spinner.classList.toggle('paused');
        
        // Toggle class on wrapper for UI badge feedback
        const isPaused = spinner.classList.contains('paused');
        wrapper.classList.toggle('is-paused', isPaused);
        wrapper.setAttribute('aria-pressed', isPaused.toString());
    }}

    // Mouse interaction
    wrapper.addEventListener('click', toggleAnimation);

    // Keyboard accessibility
    wrapper.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            toggleAnimation();
        }}
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
