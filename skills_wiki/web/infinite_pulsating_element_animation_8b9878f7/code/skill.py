def create_component(
    output_dir: str,
    title_text: str = "Infinite Pulse Animation",
    body_text: str = "CSS-driven heartbeat effect using hardware-accelerated transforms.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Infinite Pulsating Element visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Infinite Pulsating Element — generated component */
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
    --shadow: {shadow_color};
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
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.text-content {{
    margin-bottom: 4rem;
    z-index: 2;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* -- Core Visual Effect Setup -- */
.image-div {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px auto;
    cursor: pointer; /* added to indicate interactivity */
}}

/* Pulsing Element Styles */
.pulsate-fwd {{
    /* Sizing limits to stay responsive but substantial */
    width: clamp(200px, 30vw, 400px);
    height: clamp(200px, 30vw, 400px);
    
    /* Decoration to make it look like a badge/logo if no image is used */
    background: linear-gradient(135deg, var(--surface), var(--bg));
    border: 4px solid var(--accent);
    border-radius: 50%;
    box-shadow: 0 15px 35px var(--shadow), inset 0 0 40px var(--surface);
    
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* The core animation */
    /* Note: Adjusted to 1.5s for a smoother "breathing" effect rather than a rapid flutter */
    animation: pulsate-fwd 1.5s ease-in-out infinite both;
}}

/* Fallback/Placeholder logo text */
.pulsate-fwd span {{
    font-size: 3rem;
    font-weight: 800;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 2px;
}}

/* Paused State via JS Toggle */
.pulsate-fwd.paused {{
    animation-play-state: paused;
}}

/* The Keyframes driving the effect */
@keyframes pulsate-fwd {{
    0% {{
        transform: scale(1);
    }}
    50% {{
        transform: scale(1.1); /* Scales up by 10% */
    }}
    100% {{
        transform: scale(1);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <!-- Core Component HTML -->
        <div class="image-div">
            <!-- Using a stylable div as the pulsing graphic for self-containment without external assets -->
            <div class="pulsate-fwd" role="img" aria-label="Pulsating Logo">
                <span>Logo</span>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Infinite Pulsating Element — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const pulseElement = document.querySelector('.pulsate-fwd');
    const titleElement = document.querySelector('.title');

    // Optional interactivity: clicking the pulsing element pauses/resumes it
    pulseElement.addEventListener('click', () => {{
        pulseElement.classList.toggle('paused');
        
        // Provide user feedback
        if (pulseElement.classList.contains('paused')) {{
            titleElement.textContent = "Animation Paused";
        }} else {{
            titleElement.textContent = "{title_text}";
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
